import numpy as np
import csv
import json
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence
import tkinter as _tk
from tkinter import filedialog as _filedlg

import cv2
import rclpy
from rclpy.node import Node

from .AssemblyRobot import AssemblyRobot, assembly_robot_command_loop
from .CrimperRobot import CrimperRobot, crimper_robot_command_loop
from .LiquidRobot import LiquidRobot, liquid_robot_command_loop
from BatteryLab.electrolyte_planner import (
    DEFAULT_STATE_PATH,
    DEFAULT_TIP_RACK_PATH,
    ElectrolyteSpec,
    clear_vial,
    load_inventory_state,
    print_vial_statuses,
    save_inventory_state,
    show_save_location,
    set_vial_contents,
    evaluate_formulation,
    Inventory,
    load_tip_rack_state,
    save_tip_rack_state,
    TipRack,
    VIAL_MAX_VOLUME_UL,
)
from BatteryLab.robots.Constants import Components

LAST_RECIPE_DIR_PATH = Path.home() / ".batterylab" / "last_recipe_dir.txt"


def _component_slug(component_name: str) -> str:
    component_name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", component_name)
    component_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", component_name)
    return component_name.lower()


def _tip_index_to_coordinates(tip_index: int) -> tuple[int, int]:
    """Convert a linear tip index (0-95) to 96-well plate (x, y) coordinates.
    
    96-well plates are typically 8 rows x 12 columns:
    - x ranges 0-11 (columns)
    - y ranges 0-7  (rows)
    """
    if not (0 <= tip_index <= 95):
        raise ValueError(f"Tip index must be 0-95, got {tip_index}")
    x = tip_index % 12
    y = tip_index // 12
    return x, y


def _tip_index_for_substance_or_error(
    tip_rack: TipRack, substance_name: Optional[str]
) -> int:
    tip_index = tip_rack.find_clean_tip_for_substance(substance_name)
    if tip_index is not None:
        return tip_index

    if substance_name is None:
        raise RuntimeError("No clean pipette tips are available for this batch.")

    raise RuntimeError(
        f"No clean pipette tips are available for substance '{substance_name}' without contamination."
    )


def _load_recipes_file(recipe_path: Path) -> list[dict]:
    with recipe_path.open("r", encoding="utf-8") as handle:
        raw_payload = json.load(handle)

    if isinstance(raw_payload, dict):
        if "recipes" in raw_payload:
            raw_payload = raw_payload["recipes"]
        elif "cells" in raw_payload:
            raw_payload = raw_payload["cells"]
        else:
            raw_payload = [raw_payload]

    if not isinstance(raw_payload, list) or not raw_payload:
        raise ValueError("recipes file must contain a non-empty list of recipe objects")

    normalized_recipes: list[dict] = []
    for index, recipe in enumerate(raw_payload, start=1):
        if not isinstance(recipe, dict):
            raise ValueError(f"recipe entry {index} must be a JSON object")
        normalized_recipes.append(recipe)

    return normalized_recipes


def _assess_batch_requirements(recipes: list[dict], inventory: Inventory) -> tuple[dict, dict]:
    """Return (required_by_solution, deficits) for a list of recipes against current inventory.

    required_by_solution maps solution_name -> total required uL across all recipes.
    deficits maps solution_name -> deficit uL (required - available) if positive.
    """
    required_by_solution: dict[str, float] = {}

    for recipe in recipes:
        plan = evaluate_formulation(inventory, recipe)
        instructions = plan.get("instructions") or []
        if instructions:
            for instruction in instructions:
                name = instruction.get("source_solution")
                vol = float(instruction.get("volume_ul", 0.0) or 0.0)
                if not name:
                    raise ValueError("Planner instruction missing source_solution")
                required_by_solution[name] = required_by_solution.get(name, 0.0) + vol
            continue

        for issue in plan.get("issues", []):
            name = issue.get("solution_name")
            required = float(issue.get("required_volume_ul", 0.0) or 0.0)
            if not name or required <= 0:
                continue
            required_by_solution[name] = required_by_solution.get(name, 0.0) + required

    # Compare to available inventory
    deficits: dict[str, float] = {}
    for sol, req in required_by_solution.items():
        avail = inventory.available_volume(sol)
        if avail < req:
            deficits[sol] = req - avail

    return required_by_solution, deficits


def _recipe_tip_sequence(recipe: dict, inventory: Inventory) -> list[Optional[str]]:
    """Generate a sequence of source solution names in the order tips are needed."""

    plan = evaluate_formulation(inventory, recipe)
    instructions = plan.get("instructions") or []
    if instructions:
        sequence: list[Optional[str]] = []
        seen: set[Optional[str]] = set()
        for instruction in instructions:
            substance_name = instruction.get("source_solution")
            if substance_name is None:
                continue
            if substance_name not in seen:
                sequence.append(substance_name)
                seen.add(substance_name)
        if sequence:
            return sequence

    return [None]


def _assess_batch_tip_requirements(recipes: list[dict], tip_rack: TipRack, inventory: Inventory) -> tuple[int, int]:
    """Return (additional_clean_tips_needed, current_clean_tips)."""

    clean_tip_count = sum(1 for tip in tip_rack.tips if tip.current_substance_name is None)
    assigned_substances = {
        tip.current_substance_name for tip in tip_rack.tips if tip.current_substance_name is not None
    }
    additional_clean_tips_needed = 0

    for recipe in recipes:
        for substance_name in _recipe_tip_sequence(recipe, inventory):
            if substance_name is None:
                if clean_tip_count <= 0:
                    additional_clean_tips_needed += 1
                    clean_tip_count += 1
                continue

            if substance_name in assigned_substances:
                continue

            if clean_tip_count <= 0:
                additional_clean_tips_needed += 1
                clean_tip_count += 1

            clean_tip_count -= 1
            assigned_substances.add(substance_name)

    return additional_clean_tips_needed, clean_tip_count


def _recipe_metadata_snapshot(recipe: dict) -> dict:
    return {
        "recipe_name": str(recipe.get("recipe_name", "")).strip(),
        "target_electrolyte": recipe.get("target_electrolyte"),
    }


def _electrolyte_spec_dump(spec: ElectrolyteSpec) -> dict:
    if hasattr(spec, "model_dump"):
        return spec.model_dump()
    return spec.dict()


def _read_electrolyte_spec_or_cancel(prompt: str="\n") -> Optional[dict]:
    print(prompt)
    print("""The following information is required to specify an electrolyte: 
    name (for user reference)
    volume (total, uL)
    v = dictionary of solvent_name:volume_amounts or volume_fractions of each component. This is normalized internally
    s = dictionary of salt_name:molarity for each salt
    a = dictionary of additive_name:molarity for each additive
    local_smiles = optional dictionary of component_name:SMILES for each component
    use_pubchem = boolean indicating whether to attempt querying PubChem for SMILES not provided by the user
        NOTE: if use_pubchem is False, local_smiles must contain entries for all components.""")
    while True:
        params = {'name': "",
                  'volume': "",
                  'v': "",
                  's': "",
                  'a': "",
                  'local_smiles': "",
                  'use_pubchem': ""}
        types = {'name': str,
                'volume': float,
                'v': dict,
                's': dict,
                'a': dict,
                'local_smiles': dict,
                'use_pubchem': bool}
        valid_none = ('s', 'a', 'local_smiles') # these fields can validly be None
        done = False

        while not done:
            for param in params.keys():
                while params[param] == "":
                    raw = input(f"{types[param].__name__} for {param}: ").strip()
                    if _is_cancel(raw):
                        confirm = input("Quit operation? All progress for this electroyte will be lost.")
                        if _is_confirm(confirm):
                            return None
                        else:
                            continue
                    if raw == "" or raw.lower() == "none":
                        if param in valid_none:
                            confirm = input(f"Confirm 'None' for {param}? (y/n) ").strip().lower()
                            if _is_confirm(confirm):
                                params[param] = {} if types[param] == dict else None
                        else:
                            print(f"{param} cannot be empty. Please provide a valid {types[param].__name__}.")
                    else:
                        try:
                            if types[param] == bool:
                                try:
                                    params[param] = _parse_bool(raw)
                                except ValueError as exc:
                                    print(f"Invalid boolean input for {param}: {exc}. Please provide a valid boolean value (e.g., true/false).")
                            elif types[param] is dict:
                                    try: 
                                        params[param] = json.loads(raw.replace("'", "\""))
                                    except json.JSONDecodeError as exc:
                                        print(f"Invalid input for {param}: {exc}. Please provide a valid {types[param].__name__}.")
                            else:
                                params[param] = types[param](raw)
                                if param == "volume" and params[param] > VIAL_MAX_VOLUME_UL:
                                    raise ValueError(f"Specified volume {params[param]} uL exceeds preset max vial capacity of {VIAL_MAX_VOLUME_UL} uL.")
                        except Exception as exc:
                            print(f"Invalid input for {param}: {exc}. Please provide a valid {types[param].__name__}.")
                            params[param] = ""
            
            # Confirm input
            print("\nYou have entered the following electrolyte specification:")
            for key, value in params.items():
                print(f"  {key}: {value}")
            confirm = input("Is this correct? (y/n) ").strip().lower()
            if not _is_confirm(confirm):
                print("Which specs would you like to correct? (type names separated by commas, or 'all' to re-enter everything)")
                to_correct = input("Specifications to correct: ").strip().lower()
                if to_correct == "all":
                    params = {key: "" for key in params.keys()}
                else:
                    to_correct_set = {name.strip() for name in to_correct.split(",")}
                    for name in to_correct_set:
                        if name in params:
                            params[name] = ""
                        else:
                            while name not in params:
                                name = input(f"Specification '{name}' not recognized. Please re-try ('none' to move on): ").strip().lower()
                                if name.lower() == 'none':
                                    to_correct_set.remove(name)
                            params[name] = ""
            else:
                done = True

        try:
            return _electrolyte_spec_dump(ElectrolyteSpec(**params))
        except Exception as exc:
            print(f"Invalid electrolyte spec: {exc}")
            continue

def _parse_bool(raw: str) -> bool:
    if raw.lower() in {"true", "t", "yes", "y", "1"}:
        return True
    if raw.lower() in {"false", "f", "no", "n", "0"}:
        return False
    raise ValueError(f"Cannot parse boolean value from '{raw}'")


def _prompt_batch_component_metadata(component_order: Sequence[Components]) -> dict:
    print("Enter the component details for this batch campaign. Leave a field blank to skip it.")
    metadata: dict[str, dict[str, str]] = {}
    for component in component_order:
        details = input(
            f"{component.name} details (material / lot / supplier / notes): "
        ).strip()
        metadata[component.name] = {"details": details}
    return metadata


def _batch_component_metadata_path() -> Path:
    return Path(__file__).resolve().parents[4] / "metadata" / "last_batch_component_metadata.json"


def _load_last_batch_component_metadata() -> Optional[dict]:
    metadata_path = _batch_component_metadata_path()
    if not metadata_path.exists():
        return None

    with metadata_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Stored batch component metadata must be a JSON object")
    return payload


def _save_last_batch_component_metadata(metadata: dict) -> None:
    metadata_path = _batch_component_metadata_path()
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with metadata_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _prompt_batch_component_metadata_with_reuse(component_order: Sequence[Components]) -> dict:
    last_metadata = None
    try:
        last_metadata = _load_last_batch_component_metadata()
    except Exception as e:
        print(f"Warning: could not load last-used batch component metadata: {e}")

    if last_metadata is not None:
        while True:
            print("Last-used batch component metadata:")
            print(json.dumps(last_metadata, indent=2, sort_keys=True))
            confirm = input(
                'Type exactly "yEs!" to reuse this metadata, or type "new" to enter new data: '
            ).strip()
            if confirm == "yEs!":
                return last_metadata
            if confirm.lower() in {"n", "ne", "new"}:
                break
            print('Please type exactly "yEs!" to reuse, or "new" to enter new data.')

    metadata = _prompt_batch_component_metadata(component_order)
    try:
        _save_last_batch_component_metadata(metadata)
    except Exception as e:
        print(f"Warning: failed to save last-used batch component metadata: {e}")
    return metadata


def _simulate_recipe_execution(recipe: dict, inventory: Inventory) -> None:
    """Print a simulated sequence of liquid-robot actions for a recipe without moving hardware.

    Uses `evaluate_formulation` to generate instructions and prints human-friendly
    messages that mirror what the MG400 would do (tip pickup, aspirate from vial,
    dispense to assembly post, return tip).
    """
    # Note: I initially thought of trying to merge this into 
    # `dispense_electrolyte_recipe`, but I think it's cleaner to keep it separate. 
    # This function is small enough as-is, and the printing interface looks cleaner
    # in the CLI than the logger does for such long-form output. Further, the purpose
    # of the logger is as a record of machine movements and assembly actions, so adding
    # this kind of transient user-serving output there doesn't really make sense.
    name = recipe.get("recipe_name", "<unnamed>")
    print(f"\n--- Simulation for recipe: {name} ---")
    try:
        plan = evaluate_formulation(inventory, recipe)
    except Exception as e:
        print(f"Failed to evaluate recipe '{name}': {e}")
        return

    if not plan.get("feasible", False):
        print(f"Recipe '{name}' is NOT feasible. Issues: {plan.get('issues', [])}")
        return

    instructions = plan.get("instructions", [])
    if not instructions:
        # Fall back to a single-volume action if planner produced no instructions
        print("Something went wrong: planner produced no instructions.")
        return

    print("Simulated pipetting instructions:")
    print(" - Acquire tip (simulated)")
    for instr in instructions:
        step = instr.get("step_index")
        name_ing = instr.get("ingredient_name")
        sx = instr.get("source_x_ind")
        sy = instr.get("source_y_ind")
        src = instr.get("source_solution")
        vol = float(instr.get("volume_ul", 0.0) or 0.0)

        print(
            f"   Step {step}: move to vial ({sx},{sy}) containing '{src}' -> "
            f"aspirate {vol:.1f} uL of '{name_ing}' (simulated)"
        )
        print(f"            move to assembly post -> dispense {vol:.1f} uL (simulated)")
        print(f"            return tip to waste/stand (simulated for step {step})")
    print(" - Drop tip (simulated)")
    print(f"--- End simulation for recipe: {name} ---\n")


# def _simulate_recipe_execution_with_movements(recipe: dict, inventory: Inventory, liquid_robot) -> None:
#     """Simulate the recipe while commanding only MG400 movements (no aspirate/dispense).

#     Behavior:
#     - Load the tip rack and select an appropriate tip based on substances used (like real assembly).
#     - Move the MG400 to acquire the correct tip (down then up) but do NOT call the aspirate
#       method used to physically pick a tip.
#     - Move (without descending) to each source vial location for the planned instructions.
#     - Return the tip to the tip rack (movement only, no eject).
#     """
#     # Get recipe, confirm feasibility
#     name = recipe.get("recipe_name", "<unnamed>")
#     print(f"\n--- Movement-simulation for recipe: {name} ---")
#     try:
#         plan = evaluate_formulation(inventory, recipe)
#     except Exception as e:
#         print(f"Failed to evaluate recipe '{name}': {e}")
#         return

#     if not plan.get("feasible", False):
#         print(f"Recipe '{name}' is NOT feasible. Issues: {plan.get('issues', [])}")
#         return

#     # Get instructions
#     instructions = plan.get("instructions", [])
#     if not instructions:
#         # Fall back to a single-volume action if planner produced no instructions
#         print("Something went wrong: planner produced no instructions.")
#         return
    
#     # Connect to liquid handler
#     mg = liquid_robot.MG400
#     print("Re-homing liquid robot...")
#     mg.move_home()  # ensure we start from a known position
    
#     # Load tip rack and select an appropriate tip (matching real assembly behavior)
#     try:
#         tip_rack = load_tip_rack_state()
#     except Exception as e:
#         print(f"Failed to load tip rack state: {e}")
#         return
    
#     # Mime movements for each instruction, getting fresh tips when substance changes
#     print("Simulated pipetting movements:")
#     current_substance = None
#     tip_index = None
#     tip_x = None
#     tip_y = None
    
#     for instr in instructions:
#         step = instr.get("step_index")
#         name_ing = instr.get("ingredient_name")
#         sx = int(instr.get("source_x_ind", 0))
#         sy = int(instr.get("source_y_ind", 0))
#         src = instr.get("source_solution")
#         vol = float(instr.get("volume_ul", 0.0) or 0.0)
        
#         # Check if substance changed; if so, drop current tip and get a new one
#         if src != current_substance: 
#             # Drop the current tip if we have one and mark it as used
#             if tip_index is not None:
#                 print(f"  Returning tip {tip_index} to tip rack (substance changed)")
#                 try:
#                     mg.drop_tip(tip_x, tip_y)
#                 except Exception as e:
#                     print(f"    Movement to return tip failed (simulated): {e}")
#                 # Mark the tip as used for its substance
#                 tip_rack.mark_tip_used(tip_index, current_substance)
            
#             # Get a new tip for the new substance
#             current_substance = src
#             try:
#                 tip_index = _tip_index_for_substance_or_error(tip_rack, current_substance)
#                 tip_x, tip_y = _tip_index_to_coordinates(tip_index)
#             except ValueError as e:
#                 print(f"    Error occurred while acquiring tip: {e}")
#                 return # Should have no tip attached, so ending here is safe

#             print(f"  Acquiring tip {tip_index} at ({tip_x}, {tip_y}) for substance '{current_substance}'")
#             try:
#                 mg.get_tip(tip_x, tip_y)
#             except Exception as e:
#                 print(f"    Movement to tip failed (simulated): {e}")
#                 print("     WARNING: remove tip before continuing to avoid collisions.")
#                 return 
        
#         # Execute the instruction
#         print(f"  Step {step}: move to vial ({sx},{sy}) containing '{src}' (movement only)")
#         try:
#             # Move to vial up-position only so we do not descend into liquid
#             mg.get_liquid(sx, sy, vol, mime=True)
#         except Exception as e:
#             print(f"    Movement to vial failed (simulated): {e}")
#             print("     WARNING: remove tip before continuing to avoid collisions.")
#             return
#         print(f"           would aspirate {vol:.1f} uL (no action), then move to assembly post (no action)")
    
#     # Return the final tip to the tip rack and mark as used
#     if tip_index is not None:
#         print(f"  Returning final tip {tip_index} to tip rack")
#         try:
#             mg.drop_tip(tip_x, tip_y)
#             mg.move_home()
#         except Exception:
#             print(f"     Something went wrong while returning tip ({tip_x}, {tip_y}) and re-homing the robot.")
#             print( "     WARNING: remove tip before continuing to avoid collisions.")
#             return
#         # Mark the final tip as used to persist state across simulations
#         tip_rack.mark_tip_used(tip_index, current_substance)
    
#     # Persist tip rack state so subsequent simulations use updated state
#     try:
#         save_tip_rack_state(tip_rack)
#         print(f"  Tip rack state persisted to disk")
#     except Exception as e:
#         print(f"  Warning: Failed to save tip rack state: {e}")

#     print(f"--- End movement-simulation for recipe: {name} ---\n")

class BatterySessionTracker:
    LARGE_ADJUSTMENT_STATIC_THRESHOLD = 1.0
    LARGE_ADJUSTMENT_MIN_SAMPLES = 5
    LARGE_ADJUSTMENT_MAD_MULTIPLIER = 3.0

    def __init__(self, session_root: Path):
        self.session_root = session_root
        self.session_id: Optional[str] = None
        self.session_dir: Optional[Path] = None
        self.lookup_image_dir: Optional[Path] = None
        self.records_path: Optional[Path] = None
        self._battery_records = []
        self._battery_index = 0
        self._component_adjust_history = {}
        self.component_order = [
            Components.CathodeCase,
            Components.Washer,
            Components.Spacer,
            Components.Cathode,
            Components.Separator,
            Components.Anode,
            Components.SpacerExtra,
            Components.AnodeCase,
        ]
        self.fieldnames = [
            "battery_id",
            "session_id",
            "battery_start_time",
            "battery_end_time",
            "battery_status",
            "recipe_source_path",
            "recipe_sequence_index",
            "recipe_name",
            "recipe_total_volume_ul",
            "recipe_snapshot_json",
            "batch_component_metadata_json",
        ]
        for component in self.component_order:
            slug = _component_slug(component.name)
            self.fieldnames.extend(
                [
                    f"{slug}_dx",
                    f"{slug}_dy",
                    f"{slug}_detected",
                    f"{slug}_lookup_image",
                    f"{slug}_lookup_reason",
                ]
            )
            self._component_adjust_history[slug] = {"dx": [], "dy": []}

    def _initialize_session_storage(self):
        if self.session_dir is not None:
            return

        self.session_id = datetime.now().strftime("%m%d_%H%M")
        self.session_dir = self.session_root / f"session_{self.session_id}"
        self.lookup_image_dir = self.session_dir / "images"

        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.lookup_image_dir.mkdir(parents=True, exist_ok=True)
        self.records_path = self.session_dir / "battery_records.csv"

    def _require_session_storage(self):
        if (
            self.session_id is None
            or self.session_dir is None
            or self.lookup_image_dir is None
            or self.records_path is None
        ):
            raise RuntimeError("Battery session storage has not been initialized yet.")

    def start_battery(
        self,
        recipe: Optional[dict] = None,
        recipe_index: Optional[int] = None,
        recipe_source_path: Optional[str] = None,
        batch_component_metadata: Optional[dict] = None,
    ):
        self._initialize_session_storage()
        self._require_session_storage()
        self._battery_index += 1
        record = {
            "battery_id": self._battery_index,
            "session_id": self.session_id,
            "battery_start_time": datetime.now().isoformat(timespec="seconds"),
            "battery_end_time": "",
            "battery_status": "running",
            "recipe_source_path": recipe_source_path or "",
            "recipe_sequence_index": "" if recipe_index is None else str(recipe_index),
            "recipe_name": "",
            "recipe_total_volume_ul": "",
            "recipe_snapshot_json": "",
            "batch_component_metadata_json": "",
        }
        if recipe is not None:
            recipe_snapshot = _recipe_metadata_snapshot(recipe)
            record["recipe_name"] = recipe_snapshot["recipe_name"]
            target = recipe_snapshot.get("target_electrolyte") or {}
            target_volume = target.get("volume")
            if target_volume is not None:
                record["recipe_total_volume_ul"] = str(float(target_volume))
            record["recipe_snapshot_json"] = json.dumps(recipe_snapshot, sort_keys=True)
        if batch_component_metadata is not None:
            record["batch_component_metadata_json"] = json.dumps(
                batch_component_metadata,
                sort_keys=True,
            )
        for component in self.component_order:
            slug = _component_slug(component.name)
            record[f"{slug}_dx"] = ""
            record[f"{slug}_dy"] = ""
            record[f"{slug}_detected"] = ""
            record[f"{slug}_lookup_image"] = ""
            record[f"{slug}_lookup_reason"] = ""
        self._battery_records.append(record)
        self._flush()
        return record

    def _is_large_adjustment_outlier(self, slug: str, dx: float, dy: float) -> bool:
        axis_values = {
            "dx": abs(dx),
            "dy": abs(dy),
        }
        for axis, value in axis_values.items():
            history = self._component_adjust_history[slug][axis]
            if len(history) < self.LARGE_ADJUSTMENT_MIN_SAMPLES:
                continue
            median = statistics.median(history)
            deviations = [abs(v - median) for v in history]
            mad = statistics.median(deviations)
            if mad <= 1e-9:
                continue
            if abs(value - median) > self.LARGE_ADJUSTMENT_MAD_MULTIPLIER * mad:
                return True
        return False

    def _append_adjustment_history(self, slug: str, dx: float, dy: float):
        self._component_adjust_history[slug]["dx"].append(abs(dx))
        self._component_adjust_history[slug]["dy"].append(abs(dy))

    def record_component_result(
        self,
        battery_record: dict,
        component: Components,
        result: dict,
        order: int,
    ):
        slug = _component_slug(component.name)
        dx = float(result.get("dx", 0.0))
        dy = float(result.get("dy", 0.0))
        component_detected = bool(result.get("component_detected", False))

        battery_record[f"{slug}_dx"] = f"{dx:.6f}"
        battery_record[f"{slug}_dy"] = f"{dy:.6f}"
        battery_record[f"{slug}_detected"] = component_detected

        capture_reasons = []
        if not component_detected:
            capture_reasons.append("detection_failed")

        large_static = (
            abs(dx) > self.LARGE_ADJUSTMENT_STATIC_THRESHOLD
            or abs(dy) > self.LARGE_ADJUSTMENT_STATIC_THRESHOLD
        )
        if large_static:
            capture_reasons.append("large_adjustment_static")

        large_outlier = self._is_large_adjustment_outlier(slug, dx, dy)
        if large_outlier:
            capture_reasons.append("large_adjustment_outlier")

        should_capture = len(capture_reasons) > 0

        if should_capture:
            lookup_image = result.get("lookup_image")
            if lookup_image is not None:
                self._require_session_storage()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = (
                    self.lookup_image_dir
                    / f"battery_{battery_record['battery_id']:03d}_step_{order:02d}_{slug}_{timestamp}.png"
                )
                cv2.imwrite(str(filename), lookup_image)
                battery_record[f"{slug}_lookup_image"] = str(filename)
                battery_record[f"{slug}_lookup_reason"] = ";".join(capture_reasons)
            else:
                battery_record[f"{slug}_lookup_reason"] = (
                    ";".join(capture_reasons) + ";image_unavailable"
                )

        self._append_adjustment_history(slug, dx, dy)
        self._flush()

    def finish_battery(self, battery_record: dict, status: str):
        self._require_session_storage()
        battery_record["battery_end_time"] = datetime.now().isoformat(timespec="seconds")
        battery_record["battery_status"] = status
        self._flush()

    def _flush(self):
        self._require_session_storage()
        with open(self.records_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._battery_records:
                writer.writerow(record)


class AutoBatteryLab(Node):
    def __init__(self):
        super().__init__("auto_battery_lab")
        logger = self.get_logger()
        session_root = Path(__file__).resolve().parents[4] / "metadata"
        self.session_tracker = BatterySessionTracker(session_root)
        logger.info("Battery session metadata will be created only when a full battery run starts.")
        # Initialize the Assembly Robot
        self.assembly_robot = AssemblyRobot(
            logger=logger, robot_address="192.168.0.100"
        )
        self.assembly_robot.initialize_and_home_robots()
        self.assembly_robot.calibrate_machine_vision(force=False)
        logger.info("Assembly robot vision calibration complete (or reused).")
        self.assembly_robot.move_home_and_out_of_way()

        # Initialize the Liquid Robot
        self.liquid_robot = LiquidRobot(ip="192.168.0.107", logger=logger)
        ok = self.liquid_robot.initialize_robot()
        if not ok:
            print("Failed to initialize the Liquid Robot, program aborted!")
            exit()
        # Initialize the Crimper Robot
        self.crimper_robot = CrimperRobot(logger=logger, robot_address="192.168.0.101")
        self.crimper_robot.initialize_and_home_robots()
        logger.info("Finished intializing the Auto Battery Lab")

    @staticmethod
    def _electrolyte_volume_for_recipe(recipe: Optional[dict]) -> float:
        if recipe is None:
            # If no recipe is provided, don't aspirate anything!
            return 0.0

        target = recipe.get("target_electrolyte") or {}
        value = target.get("volume")
        if value is not None:
            volume_ul = float(value)
            if volume_ul <= 0:
                raise ValueError("Recipe electrolyte volume must be greater than zero.")
            return volume_ul

        return 0.0

    def assemble_batteries_in_series(
        self,
        recipes: Sequence[dict],
        recipe_source_path: Optional[str] = None,
        batch_component_metadata: Optional[dict] = None,
    ):
        if not recipes:
            raise ValueError("recipes file did not contain any cells to assemble")

        logger = self.get_logger()
        total_recipes = len(recipes)
        success_record = np.zeros(total_recipes, dtype=bool)
        for recipe_index, recipe in enumerate(recipes, start=1):
            recipe_name = str(recipe.get("recipe_name", f"recipe_{recipe_index}"))
            logger.info(
                f"Preparing to assemble battery {recipe_index}/{total_recipes} for recipe '{recipe_name}'"
            )

            # Reload inventory to reflect any changes from prior batch items
            inventory = load_inventory_state()
            try:
                plan = evaluate_formulation(inventory, recipe)
            except Exception as e:
                logger.error(f"Skipping recipe '{recipe_name}': failed to evaluate formulation ({e})")
                continue

            if not plan.get("feasible", False):
                logger.error(
                    f"Skipping recipe '{recipe_name}': formulation not feasible: {plan.get('issues', [])}"
                )
                continue

            logger.info(f"Recipe '{recipe_name}' feasible — beginning assembly")
            try:
                self.assemble_a_battery(
                    recipe=recipe,
                    recipe_index=recipe_index,
                    recipe_source_path=recipe_source_path,
                    batch_component_metadata=batch_component_metadata,
                )
            except Exception as e:
                logger.error(f"Failed to assemble recipe '{recipe_name}': {e}")
                # TODO: what's the best way to handle a failure mid-assembly? For now, get user input.
                answer = input("To continue with next recipe, reset the system and type 'continue': ").strip().lower()
                if answer != "continue":
                    success_record[recipe_index - 1] = False
                    logger.info("Aborting batch assembly.")
                    break
                else:
                    logger.info("Continuing with next recipe in batch.")

            else:
                success_record[recipe_index - 1] = True
                logger.info(f"Finished assembly for recipe '{recipe_name}'")

        logger.info("\n\n=========================\nAssembly completed. Success record:")
        for recipe_index, (recipe, success) in enumerate(zip(recipes, success_record), start=1):
            recipe_name = str(recipe.get("recipe_name", f"recipe_{recipe_index}"))
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"  {recipe_index}/{total_recipes}: {recipe_name} — {status}")

    def put_a_component_on_assembly_post(
        self,
        component: Components,
        order: int,
        battery_record: Optional[dict] = None,
    ):
        component_name = component.name
        global_index, subtray_shape, well_grab_pos, rail_pos, subtray_name = (
            self.assembly_robot.get_next_well_of_component(component_name)
        )
        # If separator, crimper needs to close to grab it before assembly robot moves out of the way
        premove_callback = None
        if component == Components.Separator:
            # TESTING: use crimper robot to hold down separator
            if self.assembly_robot.get_rail_pos() > 100.0:
                # Assembly robot too close for crimper operation
                self.assembly_robot.move_zaber_rail(100.0)
            # Move crimper robot into position
            self.crimper_robot.move_to_hold_separator()
            premove_callback = (
                self.crimper_robot.close_gripper_to_hold_separator
            )  # don't call yet!

        self.assembly_robot.grab_component(
            rail_position=rail_pos,
            grab_position=well_grab_pos,
            is_grab=True,
            component_name=component_name,
        )

        result = self.assembly_robot.drop_current_component_to_assembly_post(
            order=order, component=component, premove_callback=premove_callback
        )
        if battery_record is not None:
            self.session_tracker.record_component_result(
                battery_record=battery_record,
                component=component,
                result=result,
                order=order,
            )

        if premove_callback is not None:
            self.crimper_robot.release_separator()  # open gripper and move back home

    def dispense_electrolyte_recipe(self, recipe: dict, mime:bool=False, demo:bool=False):
        """Used to follow the steps prescribed by the recipe to mix an electrolyte. 
        When the 'mime' flag (default: False) is set to true, the liquid handler will
        retrieve each pipette tip and 'gesture' at the vial it would use, but will not
        contact the liquids or aspirate any fluids. This function can be used to investigate
        the system's correct loading/understanding of a recipe before completing it.
        
        Similarly, the `demo` flag (default: False) can be used to demonstrate the system
        using a default 'recipe' of 0 uL from the vial at (0, 0). """

        name = recipe.get("name", "<unnamed>") if not demo else "DEMO"
        logger = self.get_logger()
        extra = "SIMULATING:  " if mime else ""
        logger.info(f"----- {extra}Dispensing electrolyte recipe {name}-----")

        inventory = load_inventory_state()
        if not demo:
            try: 
                plan = evaluate_formulation(inventory, recipe)
            except Exception as e:
                logger.error(f"Error evaluating formulation for recipe {name}: {e}")
                return "failed_formulation"
            if not plan.get("feasible", False):
                issues = plan.get("issues", [])
                logger.error(f"Recipe '{name}' is NOT feasible. Issues: {issues}")
                return "failed_feasibility"
        
            instructions = plan.get("instructions", [])
            if not instructions:
                logger.error(f"Recipe '{name}' returned no instructions to execute.")
                return "failed_instructions"
        else:
            # In demo mode, we'll use a default recipe
            logger.info("Running in demo mode with default 'recipe'.")
            try:
                demo_solution = inventory.solution_at(0, 0)
            except:
                # No solution loaded at (0, 0) yet, so create a dummy
                demo_solution = {
                    'name': 'DEMO_SOLUTION(none)',
                    'volume': 1500,
                    'v': {'DEMO': 1.0},
                    's': {}, 
                    'a': {},
                    'local_smiles': {'DEMO': 'DEMO'},
                    'use_pubchem': False
                }
                inventory = set_vial_contents(
                    inventory, 
                    x_ind=0,
                    y_ind=0,
                    electrolyte=demo_solution,
                    volume_ul=1500.0
                )
                save_inventory_state(inventory)
                logger.info("Default demo solution initialized and saved.")

            instructions = [
                {
                    "step_index": 0,
                    "source_x_ind": 0,
                    "source_y_ind": 0,
                    "source_solution": demo_solution['name'],
                    "volume_ul": 0.0
                }
            ]

        mg = self.liquid_robot.MG400
        logger.info("Re-homing liquid robot before following recipe instructions.")
        mg.move_home()

        try:
            tip_rack = load_tip_rack_state()
        except Exception as e:
            logger.error(f"Error loading tip rack state: {e}")
            return "failed_to_load_tip_rack"
    
        current_substance = None
        tip_index = None
        tip_x = None
        tip_y = None

        for instr in instructions:
            step = instr.get("step_index")
            sx = int(instr.get("source_x_ind", 0))
            sy = int(instr.get("source_y_ind", 0))
            src = instr.get("source_solution")
            vol = float(instr.get("volume_ul", 0.0) or 0.0)
            if vol == 0 and not demo:
                logger.warning(f"Instruction with zero volume detected: {instr}")
            elif vol < 0:
                logger.error(f"Instruction with negative volume detected: {instr}")
                return "negative_volume_requested"

            logger.info(f"Executing instruction {step}: {vol} ul of {src} from ({sx}, {sy}) ")
            if src != current_substance:
                # Drop the current tip if we have one and mark it as used
                if tip_index is not None:
                    logger.info(f"Returning tip {tip_index} to tip rack (substance changed)")
                    try:
                        mg.drop_tip(tip_x, tip_y)
                    except Exception as e:
                        logger.error(f"Movement to return tip failed: {e}")
                        return "failed_to_return_tip"
                    # Mark the tip as used for its substance
                    tip_rack.mark_tip_used(tip_index, current_substance)

                # Get a new tip for the new substance
                current_substance = src
                try:
                    tip_index = _tip_index_for_substance_or_error(tip_rack, current_substance)
                    tip_x, tip_y = _tip_index_to_coordinates(tip_index)
                except Exception as e:
                    logger.error(f"Failed to get a new tip for substance {current_substance}: {e}")
                    return "failed_to_acquire_tip"

                logger.info(f"Using new tip {tip_index} for substance {current_substance}")
                try:
                    mg.get_tip(tip_x, tip_y)
                except Exception as e:
                    logger.error(f"Failed to get tip {tip_index} for substance {current_substance}: {e}")
                    logger.warning("WARNING: remove tip before continuing to avoid collisions.")
                    return "failed_to_get_tip"
            
            # Execute the instruction
            try:
                mg.get_liquid(sx, sy, vol, mime=mime or demo)
            except Exception as e:
                logger.error(f" Movement to vial ({sx}, {sy}) failed: {e}")
                return "failed_to_get_liquid"
            
            if not mime:
                # aspirate the liquid, then move to the post, then return the tip
                try:
                    mg.add_liquid_to_post(vol)
                except Exception as e:
                    logger.error(f"Failed to add liquid to post: {e}")
                    return "failed_to_add_liquid_to_post"
                try:
                    mg.return_liquid(sx, sy)
                except Exception as e:
                    logger.error(f"Failed to return liquid to vial ({sx}, {sy}): {e}")
                    return "failed_to_return_liquid"
                
                # Consume liquid from inventory only after successful aspiration and dispensing
                try:
                    inventory.consume_solution_from_vial(sx, sy, vol)
                    try:
                        save_inventory_state(inventory)
                    except Exception as e:
                        logger.error(f"Failed to save inventory state: {e}")
                except Exception as e:
                    logger.error(f"Failed to consume solution from vial ({sx}, {sy}): {e}")
                
                # Build vial alerts and update inventory state if necessary
                try:
                    alerts = inventory.build_vial_alerts()
                    # log alerts if any
                    if alerts:
                        for ind, alert in enumerate(alerts):
                            logger.warning(f"Vial alert {ind+1}: {alert}")
                    else:
                        logger.info("No vial alerts found for this step. Continuing...")
                except Exception as e:
                    logger.error("Failed to build vial alerts")

                # Save updated inventory state
                try:
                    save_inventory_state(inventory)
                except Exception as e:
                    logger.warning(f"Failed to save updated inventory: {e}")

        # Return the final tip to the tip rack and mark as used
        if tip_index is not None:
            logger.info(f"Returning final tip {tip_index} to tip rack")
            try:
                mg.drop_tip(tip_x, tip_y)
                mg.move_home()
            except Exception as e:
                logger.error(f"Something went wrong while returning tip ({tip_x}, {tip_y}) and re-homing the robot.")
                logger.warning("WARNING: remove tip before continuing to avoid collisions")
                returnc
            # Mark the final tip as used to persist state across simulations
            tip_rack.mark_tip_used(tip_index, current_substance)

        # Persist tip rack state 
        try:
            save_tip_rack_state(tip_rack)
            logger.info("Tip rack state saved to disk")
        except Exception as e:
            logger.warning(f"Failed to save tip rack state: {e}")
        
        logger.info(f"----- Finished recipe {name} -----\n")



    def assemble_a_battery(
        self,
        recipe: Optional[dict] = None,
        recipe_index: Optional[int] = None,
        recipe_source_path: Optional[str] = None,
        batch_component_metadata: Optional[dict] = None,
        demo:Optional[bool] = False,
    ):
        battery_record = self.session_tracker.start_battery(
            recipe=recipe,
            recipe_index=recipe_index,
            recipe_source_path=recipe_source_path,
            batch_component_metadata=batch_component_metadata,
        )
        # Prepare all the robots and home them
        try:
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1:
                raise RuntimeError(
                    "The current linear rail pos cannot be determined! Check the status!"
                )
            if rail_pos > 15:
                self.assembly_robot.move_home_and_out_of_way()
            self.liquid_robot.move_home()
            self.crimper_robot.move_home()
            order = 0
            # 1. Put a Cathode Case on the assembly post
            self.put_a_component_on_assembly_post(
                Components.CathodeCase, order, battery_record=battery_record
            )
            order += 1
            # 2. Put the Washer
            self.put_a_component_on_assembly_post(
                Components.Washer, order, battery_record=battery_record
            )
            order += 1
            # 3. Put the Spacer
            self.put_a_component_on_assembly_post(
                Components.Spacer, order, battery_record=battery_record
            )
            order += 1
            # 4. Put the Cathode
            self.put_a_component_on_assembly_post(
                Components.Cathode, order, battery_record=battery_record
            )
            order += 1
            # 5. Put the Separator
            self.put_a_component_on_assembly_post(
                Components.Separator, order, battery_record=battery_record
            )
            order += 1
            # 6. Add the electrolyte - (1) Move assembly robot out of the way
            self.assembly_robot.move_home_and_out_of_way(home=8.0)
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1 or rail_pos > 10:
                raise RuntimeError(
                    "The current linear rail pos cannot be cleared! Check the status!"
                )
            # 6.(2) Add electrolyte using planner instructions when recipe provided
            self.liquid_robot.MG400.move_home()
            try:
                # Load tip rack and select an appropriate tip
                try:
                    tip_rack = load_tip_rack_state()
                except Exception as e:
                    self.get_logger().error(f"Error loading tip rack: {e}")
                    self.session_tracker.finish_battery(battery_record, status="failed_tip_rack")
                    return

                # if recipe is None or not recipe.get("target_electrolyte"):
                #     print("No solvency electrolyte recipe provided. Using default demo behavior.")
                #     # This should only happen during a demo (no recipe)
                #     volume_to_get = self._electrolyte_volume_for_recipe(recipe)
                #     # default to the first vial for a demo
                #     liquid_x, liquid_y = 0, 0
                #     try: 
                #         substance_name = inventory.solution_at(liquid_x, liquid_y)
                #     except Exception:
                #         substance_name = None
                #     tip_index = _tip_index_for_substance_or_error(tip_rack, substance_name)
                #     tip_x, tip_y = _tip_index_to_coordinates(tip_index)
                    
                #     self.liquid_robot.MG400.get_tip(tip_x, tip_y)
                #     self.liquid_robot.MG400.get_liquid(liquid_x, liquid_y, volume_to_get)
                #     self.liquid_robot.MG400.add_liquid_to_post(volume_to_get)
                #     self.liquid_robot.MG400.return_liquid(liquid_x, liquid_y)
                #     self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                #     self.liquid_robot.MG400.move_home()
                    
                #     # Mark tip as used for unknown substance
                #     tip_rack.mark_tip_used(tip_index, substance_name)
                #     save_tip_rack_state(tip_rack)
                if demo:
                    self.dispense_electrolyte_recipe(recipe={}, demo=True)
                else:
                    self.dispense_electrolyte_recipe(recipe)
                    # # Use electrolyte planner to allocate from vials and update inventory
                    # inventory = load_inventory_state()

                    # try:
                    #     plan = evaluate_formulation(inventory, recipe)
                    # except Exception as e:
                    #     self.get_logger().error(f"Error evaluating formulation: {e}")
                    #     self.session_tracker.finish_battery(battery_record, status="failed_evaluation")
                    #     return

                    # if not plan.get("feasible", False):
                    #     issues = plan.get("issues", [])
                    #     self.get_logger().error(
                    #         f"Formulation not feasible for recipe '{recipe.get('recipe_name')}', issues: {issues}"
                    #     )
                    #     self.session_tracker.finish_battery(battery_record, status="failed_feasibility")
                    #     return

                    # instructions = plan.get("instructions", [])
                    # if not instructions:
                    #     self.get_logger().error(f"No instructions generated for recipe '{recipe.get('recipe_name')}'")
                    #     self.session_tracker.finish_battery(battery_record, status="failed_instructions")
                    #     return

                    # # Re-home liquid robot before starting
                    # self.liquid_robot.MG400.move_home()
                    
                    # # Execute instructions, getting a fresh tip each time the substance changes
                    # current_substance = None
                    # tip_index = None
                    # tip_x = None
                    # tip_y = None

                    # for instr in instructions:
                    #     sx = int(instr.get("source_x_ind", 0))
                    #     sy = int(instr.get("source_y_ind", 0))
                    #     src = instr.get("source_solution")
                    #     vol = float(instr.get("volume_ul", 0.0))
                    #     if vol == 0:
                    #         continue
                    #     elif vol < 0:
                    #         self.get_logger().warning(f"Invalid volume for substance {current_substance} at vial ({sx}, {sy}): {vol}")
                    #         continue
                        
                    #     # Check if substance changed; if so, drop current tip and get a new one
                    #     if src != current_substance:
                    #         # Drop the current tip if we have one
                    #         if tip_index is not None:
                    #             try:
                    #                 self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                    #             except Exception as e:
                    #                 self.get_logger().error(f"Error dropping tip: {e}")
                    #             tip_rack.mark_tip_used(tip_index, current_substance)

                    #         # Get a new tip for the new substance
                    #         current_substance = src
                    #         try:
                    #             tip_index = _tip_index_for_substance_or_error(tip_rack, current_substance)
                    #             tip_x, tip_y = _tip_index_to_coordinates(tip_index)
                    #         except Exception as e:
                    #             self.get_logger().error(f"Error getting tip for substance {current_substance}: {e}")
                    #             continue

                    #         try:
                    #             self.liquid_robot.MG400.get_tip(tip_x, tip_y)
                    #         except Exception as e:
                    #             self.get_logger().error(f"Error getting tip: {e}")
                    #             continue

                    #     # Aspirate from source vial and dispense to assembly post
                    #     self.liquid_robot.MG400.get_liquid(sx, sy, vol)
                    #     self.liquid_robot.MG400.add_liquid_to_post(vol)
                    #     # Blowout/return to source to clear the tip
                    #     self.liquid_robot.MG400.return_liquid(sx, sy)

                    #     # Consume liquid from inventory in-memory only after successful aspiration
                    #     try:
                    #         inventory.consume_solution_from_vial(sx, sy, vol)
                    #         try:
                    #             save_inventory_state(inventory)
                    #         except Exception as e:
                    #             self.get_logger().warning(f"Failed to save updated inventory: {e}")
                    #     except Exception as e:
                    #         self.get_logger().warning(f"Failed to consume solution from digital vial: {e}")
                        
                    #     # Build vial alerts and update inventory state in-memory after each instruction to reflect changes for subsequent instructions in the same recipe
                    #     try:
                    #         alerts = inventory.update_vial_alerts()
                    #         # log alerts if any
                    #         if alerts:
                    #             for ind, alert in enumerate(alerts):
                    #                 self.get_logger().warning(f"Vial alert {ind+1}: {alert}")
                    #         else: 
                    #             self.get_logger().info("No vial alerts found for this step. Continuing...")
                    #     except Exception as e:
                    #         self.get_logger().warning(f"Failed to update vial alerts: {e}")
                        
                    #     # Save the updated inventory state
                    #     try:
                    #         save_inventory_state(inventory)
                    #     except Exception as e:
                    #         self.get_logger().warning(f"Failed to save updated inventory: {e}")

                    # # Drop the final tip and mark as used
                    # if tip_index is not None:
                    #     self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                    #     tip_rack.mark_tip_used(tip_index, current_substance)
                    
                    # self.liquid_robot.MG400.move_home()
                    # save_tip_rack_state(tip_rack)

                    
            except Exception:
                self.session_tracker.finish_battery(battery_record, status="failed")
                raise
            # 7. Put the Anode
            self.put_a_component_on_assembly_post(
                Components.Anode, order, battery_record=battery_record
            )
            order += 1
            # 8. Put the SpacerExtra
            self.put_a_component_on_assembly_post(
                Components.SpacerExtra, order, battery_record=battery_record
            )
            order += 1
            # 9. Put the AnodeCase
            self.put_a_component_on_assembly_post(
                Components.AnodeCase, order, battery_record=battery_record
            )
            order += 1
            self.assembly_robot.move_home_and_out_of_way()
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1 or rail_pos > 35:
                raise RuntimeError(
                    "The current linear rail pos cannot be cleared! Check the status!"
                )
            # 10. Crimper Robot
            self.crimper_robot.crimp_a_battery(False)
            self.crimper_robot.put_to_storage()
            self.crimper_robot.move_home()
            self.assembly_robot.save_counter_config()
            self.session_tracker.finish_battery(battery_record, status="completed")
        except Exception:
            self.session_tracker.finish_battery(
                battery_record, status="failed"
            )
            raise

    def test_separator_placement(self):
        # Test new crimper-assisted separator placement method
        self.put_a_component_on_assembly_post(Components.Separator, order=4)


def _is_cancel(value: str) -> bool:
    return value.strip().lower() in {"q", "x", "cancel"}

def _is_confirm(value: str) -> bool:
    return value.strip().lower() in {"y", "yes", "confirm"}


def _read_positive_float_or_cancel(prompt: str):
    while True:
        raw = input(prompt).strip()
        if _is_cancel(raw):
            return None
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a numeric value, or type 'q' to cancel.")
            continue
        if value <= 0:
            print("Please enter a value greater than zero.")
            continue
        return value


def _read_non_negative_int_or_cancel(prompt: str):
    while True:
        raw = input(prompt).strip()
        if _is_cancel(raw):
            return None
        try:
            value = int(raw)
        except ValueError:
            print("Please enter an integer value, or type 'q' to cancel.")
            continue
        if value < 0:
            print("Please enter a value greater than or equal to zero.")
            continue
        return value


def electrolyte_planner_menu(batterylab: AutoBatteryLab):
    logger = batterylab.get_logger()
    try:
        inventory = load_inventory_state()
        logger.info(f"Loaded electrolyte inventory from {DEFAULT_STATE_PATH}")
    except Exception as e:
        logger.warning(f"Initial electrolyte inventory load failed: {e}")
        print(f"Unable to open electrolyte planner: {e}")
        return

    prompt = """
--------------------------------------------------
Electrolyte Planner Menu
[V]iew vial status
[A]dd/update vial contents (after physical refill)
[C]lean vial (mark as empty)
[R]eload inventory from disk
[S]ave inventory to disk
[P]rint the location of the inventory file on disk
[Enter] Back to main menu
:> """

    while True:
        user_input = input(prompt).strip().lower()
        if len(user_input) > 1:
            user_input = user_input[0]
        if user_input == "":
            break
        if user_input == "v":
            print_vial_statuses(inventory)
            continue
        if user_input == "a":
            print("Type 'q' at any prompt to cancel this operation.")
            x_ind = _read_non_negative_int_or_cancel("Liquid bottle index x: ")
            if x_ind is None:
                print("Canceled add/update operation.")
                continue

            y_ind = _read_non_negative_int_or_cancel("Liquid bottle index y: ")
            if y_ind is None:
                print("Canceled add/update operation.")
                continue

            # Check if vial is currently occupied
            try:
                current_solution = inventory.solution_at(x_ind, y_ind)
                current_volume = inventory.volume_at(x_ind, y_ind)
                if current_solution is not None and current_volume > 0:
                    print(
                        f"Warning: vial at (x={x_ind}, y={y_ind}) currently contains '{current_solution}' with volume {current_volume:.1f} uL."
                    )
                    confirm = input(
                        "Do you want to overwrite this vial's contents? (y/n or q to cancel): "
                    ).strip().lower()
                    if _is_cancel(confirm):
                        print("Canceled add/update operation.")
                        continue
                    if confirm != "y":
                        print("Canceled.")
                        continue
            except Exception as e:
                # If there's an error accessing the vial, assume it's empty and proceed
                print(f"An error occurred while checking vial contents: {e}. Proceeding with add/update operation.")
                pass

            electrolyte_payload = _read_electrolyte_spec_or_cancel()
            if electrolyte_payload is None:
                print("Canceled add/update operation.")
                continue

            volume_ul = electrolyte_payload['volume'] # should have been provided when loading in electrolytes

            try:
                inventory = set_vial_contents(
                    inventory,
                    x_ind=x_ind,
                    y_ind=y_ind,
                    electrolyte=electrolyte_payload,
                    volume_ul=volume_ul,
                )
                save_inventory_state(inventory)
                print(
                    f"Updated vial at (x={x_ind}, y={y_ind}) and saved inventory."
                )
            except Exception as e:
                print(f"Failed to update vial: {e}")
            continue
        if user_input == "c":
            print("Type 'q' to cancel this operation.")
            x_ind = _read_non_negative_int_or_cancel(
                "Liquid bottle index x to mark cleaned/empty: "
            )
            if x_ind is None:
                print("Canceled clean operation.")
                continue

            y_ind = _read_non_negative_int_or_cancel(
                "Liquid bottle index y to mark cleaned/empty: "
            )
            if y_ind is None:
                print("Canceled clean operation.")
                continue

            confirm = input(
                f"Confirm cleaning vial at (x={x_ind}, y={y_ind})? This sets its volume to 0.0 uL (y/n or q to cancel): "
            ).strip().lower()
            if _is_cancel(confirm):
                print("Canceled clean operation.")
                continue
            if confirm != "y":
                print("Canceled.")
                continue
            try:
                inventory = clear_vial(inventory, x_ind=x_ind, y_ind=y_ind)
                save_inventory_state(inventory)
                print(
                    f"Marked vial at (x={x_ind}, y={y_ind}) as cleaned and saved inventory."
                )
            except Exception as e:
                print(f"Failed to clear vial: {e}")
            continue
        if user_input == "r":
            try:
                inventory = load_inventory_state()
                print("Reloaded inventory from disk.")
            except Exception as e:
                logger.error(f"Failed to reload electrolyte inventory: {e}")
                print(f"Failed to reload inventory: {e}")
            continue
        if user_input == "s":
            save_inventory_state(inventory)
            print("Saved inventory to disk.")
            continue
        if user_input == "p":
            show_save_location(inventory)
            print("Inventory file location displayed.")
            continue
        print("The choice is not valid. Please try again.")


def tip_management_menu(batterylab: AutoBatteryLab):
    """Menu for managing pipette tips (96-tip rack) and tracking usage."""
    logger = batterylab.get_logger()
    try:
        tip_rack = load_tip_rack_state()
        logger.info(f"Loaded tip rack state from {DEFAULT_TIP_RACK_PATH}")
    except Exception as e:
        logger.warning(f"Initial tip rack load failed: {e}")
        print(f"Unable to open tip manager: {e}")
        return

    prompt = """------------------------
Tip Management Menu
[V]iew tip status
[M]ark tip as used for substance
[C]lean/replace tip
[L]ist recent tip usage
[R]eset all tips to clean
[S]ave tip state to disk
[Enter] Back to main menu
:> """

    while True:
        user_input = input(prompt).strip().lower()
        if len(user_input) > 1:
            user_input = user_input[0]
        if user_input == "":
            break
        if user_input == "v":
            # Show tip status
            clean_tips = [tip.index for tip in tip_rack.tips if tip.current_substance_name is None]
            used_tips = [tip for tip in tip_rack.tips if tip.current_substance_name is not None]
            print(f"\n--- Tip Rack Status ---")
            print(f"Clean tips ({len(clean_tips)}): {clean_tips[:20]}", end="")
            if len(clean_tips) > 20:
                print(f" ... and {len(clean_tips) - 20} more")
            else:
                print()
            print(f"\nUsed tips ({len(used_tips)}):")
            for tip in sorted(used_tips, key=lambda t: t.index):
                substance = tip.current_substance_name or "<unknown>"
                timestamp = tip.last_used_timestamp or "unknown time"
                print(f"  Tip {tip.index}: {substance} (last used: {timestamp})")
            continue
        if user_input == "m":
            print("Type 'q' to cancel.")
            tip_index = _read_non_negative_int_or_cancel(
                "Tip index to mark as used (0-95): "
            )
            if tip_index is None or tip_index < 0 or tip_index > 95:
                print("Invalid tip index.")
                continue

            substance_name = input("Substance/solution name (or press Enter for unknown): ").strip()
            if _is_cancel(substance_name):
                print("Canceled.")
                continue
            if not substance_name:
                substance_name = None

            try:
                tip_rack.mark_tip_used(tip_index, substance_name)
                save_tip_rack_state(tip_rack)
                print(f"Marked tip {tip_index} as used for '{substance_name or 'unknown'}'.")
            except Exception as e:
                print(f"Failed to mark tip: {e}")
            continue
        if user_input == "c":
            print("Type 'q' to cancel.")
            tip_index = _read_non_negative_int_or_cancel(
                "Tip index to clean/replace (0-95): "
            )
            if tip_index is None or tip_index < 0 or tip_index > 95:
                print("Invalid tip index.")
                continue

            confirm = input(
                f"Confirm cleaning tip {tip_index}? (y/n): "
            ).strip().lower()
            if _is_cancel(confirm):
                print("Canceled.")
                continue
            if confirm != "y":
                print("Canceled.")
                continue
            try:
                tip_rack.mark_tip_clean(tip_index)
                save_tip_rack_state(tip_rack)
                print(f"Marked tip {tip_index} as clean.")
            except Exception as e:
                print(f"Failed to clean tip: {e}")
            continue
        if user_input == "l":
            # Show recently used tips
            used_tips = [tip for tip in tip_rack.tips if tip.current_substance_name is not None]
            if not used_tips:
                print("No tips are currently in use.")
                continue
            sorted_tips = sorted(used_tips, key=lambda t: t.last_used_timestamp or "", reverse=True)
            print("\n--- Recent Tip Usage ---")
            for tip in sorted_tips[:10]:
                substance = tip.current_substance_name or "<unknown>"
                timestamp = tip.last_used_timestamp or "unknown time"
                print(f"  Tip {tip.index}: {substance} ({timestamp})")
            continue
        if user_input == "r":
            confirm = input(
                "Reset ALL tips to clean state? This will clear usage history. (y/n): "
            ).strip().lower()
            if confirm != "y":
                print("Canceled.")
                continue
            try:
                for tip in tip_rack.tips:
                    tip.current_substance_name = None
                    tip.last_used_timestamp = None
                save_tip_rack_state(tip_rack)
                print("All tips reset to clean state.")
            except Exception as e:
                print(f"Failed to reset tips: {e}")
            continue
        if user_input == "s":
            try:
                save_tip_rack_state(tip_rack)
                print("Tip rack state saved to disk.")
            except Exception as e:
                logger.error(f"Failed to save tip rack: {e}")
                print(f"Failed to save tip state: {e}")
            continue
        print("The choice is not valid. Please try again.")

def get_recipe_file_path(goal='file'):
    """"Determine location of recipes JSON file, or get a folder in which to place a new recipe file.
    Parameter 'goal' can be either 'file' (default) or 'folder' to indicate the intent."""
    recipes_path = input("Enter path to recipes JSON file (or type 'f' to open file chooser): ").strip()
    
    # Attempt to use GUI file chooser if user types 'f', but fall back to text input if there's any issue with the GUI
    if recipes_path.lower() == "f":
        try:
            # Initialize TK root in a safe/hidden way
            _root = _tk.Tk()
            _root.withdraw()
            initial_dir = None
            try:
                if LAST_RECIPE_DIR_PATH.exists():
                    initial_dir_str = LAST_RECIPE_DIR_PATH.read_text(encoding="utf-8").strip()
                    if initial_dir_str:
                        initial_dir = initial_dir_str
            except Exception:
                initial_dir = None

            if goal == 'file':
                filename = _filedlg.askopenfilename(
                    title="Select recipes JSON file",
                    initialdir=initial_dir or str(Path.cwd()),
                    filetypes=[("JSON files", "*.json"), ("All files", "*")],
                )
            elif goal == 'folder':
                filename = _filedlg.askdirectory(
                    title="Select folder to save new recipes JSON file",
                    initialdir=initial_dir or str(Path.cwd()),
                )
            else:
                print(f"Invalid goal '{goal}' for get_recipe_file_path. Defaulting to file selection.")
                filename = _filedlg.askopenfilename(
                    title="Select recipes JSON file",
                    initialdir=initial_dir or str(Path.cwd()),
                    filetypes=[("JSON files", "*.json"), ("All files", "*")],
                )
            
            try:
                _root.destroy()
            except Exception:
                pass

            if not filename:
                print("Canceled.")
                return False  # signal cancellation with False
            recipes_path = str(filename)
            # Persist last folder
            try:
                LAST_RECIPE_DIR_PATH.parent.mkdir(parents=True, exist_ok=True)
                LAST_RECIPE_DIR_PATH.write_text(str(Path(recipes_path).parent), encoding="utf-8")
            except Exception:
                # non-fatal
                pass
        except Exception as e:
            print(f"File chooser unavailable: {e}. Falling back to text input.")
            recipes_path = input("Enter path to recipes JSON file: ").strip()
    
    return recipes_path

def _recipes_batch_menu(batterylab: AutoBatteryLab):
    logger = batterylab.get_logger()

    # Get path to recipe file
    recipes_path = get_recipe_file_path()
    if not recipes_path:
        print("Canceled.")
        return
    
    try:
        recipe_file = Path(recipes_path)
        if not recipe_file.exists():
            print(f"File not found: {recipe_file}")
            return
        recipes = _load_recipes_file(recipe_file)

        # Pre-assess aggregated requirements across all recipes
        inventory = load_inventory_state()
        try:
            required, deficits = _assess_batch_requirements(recipes, inventory)
        except Exception as e:
            print(f"Failed to assess recipes: {e}")
            return

        try:
            tip_rack = load_tip_rack_state()
            additional_tips_needed, clean_tip_count = _assess_batch_tip_requirements(recipes, tip_rack, inventory)
        except Exception as e:
            print(f"Failed to assess pipette tip requirements: {e}")
            return

        if required:
            print("Aggregated chemical requirements for this batch:")
            for sol, vol in required.items():
                avail = inventory.available_volume(sol)
                deficit = deficits.get(sol, 0.0)
                status = f"DEFICIT {deficit:.1f} uL" if deficit > 0 else "OK"
                print(f" - {sol}: required {vol:.1f} uL, available {avail:.1f} uL -> {status}")
        else:
            print("No ingredient-based requirements detected in recipes; proceeding with volume-only dispenses.")

        print(
            f"Pipette tips available: {clean_tip_count} clean tip(s) on the loaded rack; "
            f"additional clean tip(s) needed for this batch: {additional_tips_needed}"
        )
        if additional_tips_needed > 0:
            print(
                "TIP DEFICIT: the current tip rack does not have enough clean tips to finish this batch without contamination."
            )
        # Offer test/dry-run and movement-simulation options
        logger.info("ATTENTION: before assembling a battery, confirm there is no pipette tip attached to the MG400, the lookup camera lights are powered on, and the required materials are loaded.")
        action = input(
            "Choose action: [T]est recipes (simulate text), [M]ovements (simulate MG400 movements), [A]ssemble now, [C]ancel (default C): "
        ).strip().lower()
        if action == "t":
            # Run text-only simulation for each recipe using a snapshot of inventory
            for recipe in recipes:
                _simulate_recipe_execution(recipe, inventory)
            # After testing, ask whether to proceed
            action = input("Proceed to assemble these recipes now? (y/n): ").strip().lower()
            if action != "y":
                print("Canceled after test.")
                return
            else:
                action = "a"  # set to assemble after testing
        if action == "m":
            # Run movement-only simulation (commands MG400 to move to tips/vials but does not aspirate)
            # Allow user to select which recipe(s) to simulate
            while True:
                print("\n--- Available Recipes for Simulation ---")
                for idx, recipe in enumerate(recipes, start=1):
                    recipe_name = recipe.get("recipe_name", f"recipe_{idx}")
                    print(f"{idx}. {recipe_name}")
                print("q. Quit simulation and proceed to assembly")
                
                selection = input("Select recipe number to simulate (or 'q' to quit): ").strip().lower()
                
                if selection == "q":
                    break
                
                try:
                    recipe_idx = int(selection) - 1
                    if 0 <= recipe_idx < len(recipes):
                        batterylab.dispense_electrolyte_recipe(recipes[recipe_idx], mime=True)
                        #_simulate_recipe_execution_with_movements(recipes[recipe_idx], inventory, batterylab.liquid_robot)
                    else:
                        print(f"Invalid selection. Please enter a number between 1 and {len(recipes)}.")
                except ValueError:
                    print("Invalid input. Please enter a recipe number or 'q'.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            action = input("Proceed to assemble these recipes now? (y/n): ").strip().lower()
            if action != "y":
                print("Canceled after movement-simulation.")
                return
            else:
                action = "a"  # set to assemble after movement simulation
        if action == "a":
            batch_component_metadata = _prompt_batch_component_metadata_with_reuse(
                batterylab.session_tracker.component_order
            )
            batterylab.assemble_batteries_in_series(
                recipes,
                recipe_source_path=str(recipe_file.resolve()),
                batch_component_metadata=batch_component_metadata,
            )
        else:
            print("Canceled.")
        logger.info(f"Completed batch assembly of {len(recipes)} batteries.")
    except FileNotFoundError:
        print(f"File not found: {recipes_path}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON file: {e}")
    except ValueError as e:
        print(f"Invalid recipes file: {e}")
    except Exception as e:
        logger.error(f"Batch assembly failed: {e}")
        print(f"Error: {e}")

def _create_recipe_file(name, volume, v, s={}, a={}, local_smiles={}, use_pubchem=True):
    """Auxiliary function to create a recipe JSON file from user inputs"""
    recipe_path = get_recipe_file_path(goal='folder')
    if not recipe_path:
        print("Canceled.")
        return

    # Combine directory with recipe name
    recipe_file = Path(recipe_path) / f"{name}_RMI.json"
    # Ensure the directory exists
    try:
        recipe_file.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory for recipe file: {e}")
        return
    
    # Create the recipe and save it
    try:
        recipe = {
            'recipe_name': name,
            'target_electrolyte': {
                'name': name,
                'volume': volume, 
                'v': v, 
                's': s, 
                'a': a,
                'local_smiles': local_smiles,
                'use_pubchem': use_pubchem,
            }
        }
        with recipe_file.open('w', encoding='utf-8') as f:
            json.dump(recipe, f, indent=4)
        print(f"Recipe saved to {recipe_file}")
    except Exception as e: 
        print(f"Failed to save recipe file: {e}")

def create_recipe_interactive():
    """Create a JSON recipe file through interactive user inputs in the terminal"""
    payload = _read_electrolyte_spec_or_cancel()
    if payload is None:
        print("Canceled recipe creation.")
        return
    
    name = payload['name']
    volume = payload['volume']
    v = payload['v']
    s = payload['s']
    a = payload['a']
    local_smiles = payload['local_smiles']
    use_pubchem = payload['use_pubchem']

    _create_recipe_file(name, volume, v, s, a, local_smiles, use_pubchem)
    return None

def command_loop(batterylab: AutoBatteryLab):
    prompt = """
===============================================
Welcome to BatteryLab! Please select a command:
[Enter] to quit
[A]ssembly robot submenu
[L]iquid   robot submenu
[C]rimper  robot submenu
[B]atch recipes file input to assemble series of batteries
[R]ecipe creation (interactive)
[D]emo battery (single assembly using defaults and no recipe)
[E]lectrolyte vial manager
[T]ip (pipette) manager
[S]eparator test (coordinated movement using both Meca robots)
:> """
    batterylab.assembly_robot.load_counter_config()
    while True:
        user_input = input(prompt).strip().lower()
        if len(user_input) > 1:
            user_input = user_input[0]
        if user_input == "":
            break
        elif user_input == "a":
            assembly_robot_command_loop(batterylab.assembly_robot)
        elif user_input == "l":
            liquid_robot_command_loop(batterylab.liquid_robot)
        elif user_input == "c":
            crimper_robot_command_loop(batterylab.crimper_robot)
        elif user_input == "b":
            _recipes_batch_menu(batterylab)
        elif user_input == "r":
            create_recipe_interactive()
        elif user_input == "d":
            try:
                batterylab.assemble_a_battery()
            except Exception as e:
                batterylab.get_logger().error(f"Battery assembly failed: {e}")
        elif user_input == "e":
            electrolyte_planner_menu(batterylab)
        elif user_input == "t":
            tip_management_menu(batterylab)
        elif user_input == "s":
            if input("Run separator placement test? (y/n, default n): ").strip().lower() == "y":
                batterylab.test_separator_placement()
        else:
            print("The choice is not valid. Please try again.")


def main():
    rclpy.init()
    batterylab = AutoBatteryLab()

    try:
        command_loop(batterylab)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        batterylab.liquid_robot.disconnect()
        print("MG400 disconnected safely.")
        batterylab.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
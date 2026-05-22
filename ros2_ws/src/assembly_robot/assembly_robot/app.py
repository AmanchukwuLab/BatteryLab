import csv
import json
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence

import cv2
import rclpy
from rclpy.node import Node

from .AssemblyRobot import AssemblyRobot, assembly_robot_command_loop
from .CrimperRobot import CrimperRobot, crimper_robot_command_loop
from .LiquidRobot import LiquidRobot, liquid_robot_command_loop
from BatteryLab.electrolyte_planner import (
    DEFAULT_STATE_PATH,
    DEFAULT_TIP_RACK_PATH,
    clear_vial,
    load_inventory_state,
    print_vial_statuses,
    save_inventory_state,
    show_save_location,
    set_vial_contents,
    evaluate_formulation,
    evaluate_formulation_with_vials,
    Inventory,
    load_tip_rack_state,
    save_tip_rack_state,
    TipRack,
)
from BatteryLab.robots.Constants import Components


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
        ingredients = recipe.get("ingredients") or []
        if not ingredients:
            continue

        is_weight = ingredients[0].get("weight_percent") is not None
        if not is_weight:
            for ing in ingredients:
                name = ing.get("solution_name")
                vol = float(ing.get("volume_ul", 0.0) or 0.0)
                if not name:
                    raise ValueError("Ingredient missing solution_name")
                required_by_solution[name] = required_by_solution.get(name, 0.0) + vol
            continue

        # weight-percent recipe: convert to volumes using inventory densities
        electrolyte_volume_ul = recipe.get("electrolyte_volume_ul")
        if electrolyte_volume_ul is None:
            raise ValueError(
                f"Weight-percent recipe '{recipe.get('recipe_name')}' missing electrolyte_volume_ul"
            )
        target_volume_ml = float(electrolyte_volume_ul) / 1000.0

        weight_over_density = []
        for ing in ingredients:
            sol = ing.get("solution_name")
            wt = float(ing.get("weight_percent") or 0.0) / 100.0
            if sol is None:
                raise ValueError("Ingredient missing solution_name")
            # get density from inventory (may raise if missing)
            density = inventory.density_for_solution(sol)
            weight_over_density.append((sol, wt / density))

        denominator = sum(item[1] for item in weight_over_density)
        if denominator <= 0:
            raise ValueError("Invalid weight_percent/density combination for conversion")

        for sol, term in weight_over_density:
            vol_ul = (target_volume_ml * term / denominator) * 1000.0
            required_by_solution[sol] = required_by_solution.get(sol, 0.0) + vol_ul

    # Compare to available inventory
    deficits: dict[str, float] = {}
    for sol, req in required_by_solution.items():
        avail = inventory.available_volume(sol)
        if avail < req:
            deficits[sol] = req - avail

    return required_by_solution, deficits


def _simulate_recipe_execution(recipe: dict, inventory: Inventory) -> None:
    """Print a simulated sequence of liquid-robot actions for a recipe without moving hardware.

    Uses `evaluate_formulation` to generate instructions and prints human-friendly
    messages that mirror what the MG400 would do (tip pickup, aspirate from vial,
    dispense to assembly post, return tip).
    """
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
        vol = recipe.get("electrolyte_volume_ul") or 0
        print(f"Simulate: Acquire tip (simulated)")
        print(f"Simulate: Dispense {float(vol):.1f} uL to assembly post (single-vessel fallback)")
        print(f"Simulate: Return/drop tip (simulated)")
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


def _simulate_recipe_execution_with_movements(recipe: dict, inventory: Inventory, liquid_robot) -> None:
    """Simulate the recipe while commanding only MG400 movements (no aspirate/dispense).

    Behavior:
    - Load the tip rack and select an appropriate tip based on substances used (like real assembly).
    - Move the MG400 to acquire the correct tip (down then up) but do NOT call the aspirate
      method used to physically pick a tip.
    - Move (without descending) to each source vial location for the planned instructions.
    - Return the tip to the tip rack (movement only, no eject).
    """
    # Get recipe, confirm feasibility
    name = recipe.get("recipe_name", "<unnamed>")
    print(f"\n--- Movement-simulation for recipe: {name} ---")
    try:
        plan = evaluate_formulation(inventory, recipe)
    except Exception as e:
        print(f"Failed to evaluate recipe '{name}': {e}")
        return

    if not plan.get("feasible", False):
        print(f"Recipe '{name}' is NOT feasible. Issues: {plan.get('issues', [])}")
        return

    # Get instructions, connect to liquid handler
    instructions = plan.get("instructions", [])
    mg = liquid_robot.MG400
    mg.move_home()  # ensure we start from a known position
    
    # Load tip rack and select an appropriate tip (matching real assembly behavior)
    try:
        tip_rack = load_tip_rack_state()
    except Exception as e:
        print(f"Failed to load tip rack state: {e}")
        return
    
    # Mime movements for each instruction, getting fresh tips when substance changes
    print("Simulated pipetting movements:")
    current_substance = None
    tip_index = None
    tip_x = None
    tip_y = None
    
    for instr in instructions:
        step = instr.get("step_index")
        instr_substance = instr.get("source_solution")
        sx = int(instr.get("source_x_ind", 0))
        sy = int(instr.get("source_y_ind", 0))
        vol = float(instr.get("volume_ul", 0.0) or 0.0)
        
        # Check if substance changed; if so, drop current tip and get a new one
        if instr_substance != current_substance:
            # Drop the current tip if we have one and mark it as used
            if tip_index is not None:
                print(f"  Returning tip {tip_index} to tip rack (substance changed)")
                try:
                    mg.drop_tip(tip_x, tip_y)
                except Exception as e:
                    print(f"    Movement to return tip failed (simulated): {e}")
                # Mark the tip as used for its substance
                tip_rack.mark_tip_used(tip_index, current_substance)
            
            # Get a new tip for the new substance
            current_substance = instr_substance
            tip_index = tip_rack.find_clean_tip_for_substance(current_substance)
            if tip_index is None:
                tip_index = tip_rack.find_clean_tip_for_substance(None)
            if tip_index is None:
                tip_index = 0  # Force use of first tip if none are clean
            
            tip_x, tip_y = _tip_index_to_coordinates(tip_index)
            print(f"  Acquiring tip {tip_index} at ({tip_x}, {tip_y}) for substance '{current_substance}'")
            try:
                mg.get_tip(tip_x, tip_y)
            except Exception as e:
                print(f"    Movement to tip failed (simulated): {e}")
        
        # Execute the instruction
        print(f"  Step {step}: move to vial ({sx},{sy}) containing '{instr_substance}' (movement only)")
        try:
            # Move to vial up-position only so we do not descend into liquid
            mg.get_liquid(sx, sy, vol, mime=True)
        except Exception as e:
            print(f"    Movement to vial failed (simulated): {e}")
        print(f"           would aspirate {vol:.1f} uL (no action), then move to assembly post (no action)")
    
    # Return the final tip to the tip rack and mark as used
    if tip_index is not None:
        print(f"  Returning final tip {tip_index} to tip rack")
        try:
            mg.drop_tip(tip_x, tip_y)
            mg.move_home()
        except Exception:
            pass
        # Mark the final tip as used to persist state across simulations
        tip_rack.mark_tip_used(tip_index, current_substance)
    
    # Persist tip rack state so subsequent simulations use updated state
    try:
        save_tip_rack_state(tip_rack)
        print(f"  Tip rack state persisted to disk")
    except Exception as e:
        print(f"  Warning: Failed to save tip rack state: {e}")

    print(f"--- End movement-simulation for recipe: {name} ---\n")


class BatterySessionTracker:
    LARGE_ADJUSTMENT_STATIC_THRESHOLD = 1.0
    LARGE_ADJUSTMENT_MIN_SAMPLES = 5
    LARGE_ADJUSTMENT_MAD_MULTIPLIER = 3.0

    def __init__(self, session_root: Path):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = session_root / f"session_{self.session_id}"
        self.lookup_image_dir = self.session_dir / "lookup_images"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.lookup_image_dir.mkdir(parents=True, exist_ok=True)

        self.records_path = self.session_dir / "battery_records.csv"
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
            "recipe_payload_json",
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
        self._flush()

    def start_battery(
        self,
        recipe: Optional[dict] = None,
        recipe_index: Optional[int] = None,
        recipe_source_path: Optional[str] = None,
    ):
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
            "recipe_payload_json": "",
        }
        if recipe is not None:
            record["recipe_name"] = str(recipe.get("recipe_name", "")).strip()
            recipe_total_volume = recipe.get("electrolyte_volume_ul")
            if recipe_total_volume is not None:
                record["recipe_total_volume_ul"] = str(recipe_total_volume)
            record["recipe_payload_json"] = json.dumps(recipe, sort_keys=True)
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
        battery_record["battery_end_time"] = datetime.now().isoformat(timespec="seconds")
        battery_record["battery_status"] = status
        self._flush()

    def _flush(self):
        with open(self.records_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._battery_records:
                writer.writerow(record)


class AutoBatteryLab(Node):
    def __init__(self):
        super().__init__("auto_battery_lab")
        logger = self.get_logger()
        session_root = Path(__file__).resolve().parents[4] / "images" / "battery_sessions"
        self.session_tracker = BatterySessionTracker(session_root)
        logger.info(f"Battery session records will be stored in {self.session_tracker.session_dir}")
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
            return 50.0

        for key in ("electrolyte_volume_ul",):
            value = recipe.get(key)
            if value is not None:
                volume_ul = float(value)
                if volume_ul <= 0:
                    raise ValueError("Recipe electrolyte volume must be greater than zero.")
                return volume_ul

        return 50.0

    def assemble_batteries_in_series(
        self,
        recipes: Sequence[dict],
        recipe_source_path: Optional[str] = None,
    ):
        if not recipes:
            raise ValueError("recipes file did not contain any cells to assemble")

        logger = self.get_logger()
        total_recipes = len(recipes)
        for recipe_index, recipe in enumerate(recipes, start=1):
            recipe_name = str(recipe.get("recipe_name", f"recipe_{recipe_index}"))
            logger.info(
                f"Preparing to assemble battery {recipe_index}/{total_recipes} for recipe '{recipe_name}'"
            )

            # Reload inventory to reflect any changes from prior batch items
            inventory = load_inventory_state()
            try:
                feas = evaluate_formulation(inventory, recipe)
            except Exception as e:
                logger.error(f"Failed to evaluate recipe '{recipe_name}': {e}")
                continue

            if not feas.get("feasible", False):
                logger.error(
                    f"Skipping recipe '{recipe_name}': formulation not feasible: {feas.get('issues', [])}"
                )
                continue

            logger.info(f"Recipe '{recipe_name}' feasible — beginning assembly")
            self.assemble_a_battery(
                recipe=recipe,
                recipe_index=recipe_index,
                recipe_source_path=recipe_source_path,
            )

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

    def assemble_a_battery(
        self,
        recipe: Optional[dict] = None,
        recipe_index: Optional[int] = None,
        recipe_source_path: Optional[str] = None,
    ):
        battery_record = self.session_tracker.start_battery(
            recipe=recipe,
            recipe_index=recipe_index,
            recipe_source_path=recipe_source_path,
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
                tip_rack = load_tip_rack_state()
                
                if recipe is None or not recipe.get("ingredients"):
                    # Fall back to single-volume dispense
                    volume_to_get = self._electrolyte_volume_for_recipe(recipe)
                    # Try to find a clean tip; if none, use first tip and mark as used
                    tip_index = tip_rack.find_clean_tip_for_substance(None)
                    if tip_index is None:
                        tip_index = 0  # Force use of first tip if none are clean
                    tip_x, tip_y = _tip_index_to_coordinates(tip_index)
                    
                    self.liquid_robot.MG400.get_tip(tip_x, tip_y)
                    # default single-bottle coordinates
                    liquid_x, liquid_y = 0, 0
                    self.liquid_robot.MG400.get_liquid(liquid_x, liquid_y, volume_to_get)
                    self.liquid_robot.MG400.add_liquid_to_post(volume_to_get)
                    self.liquid_robot.MG400.return_liquid(liquid_x, liquid_y)
                    self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                    self.liquid_robot.MG400.move_home()
                    
                    # Mark tip as used for unknown substance
                    tip_rack.mark_tip_used(tip_index, None)
                    save_tip_rack_state(tip_rack)
                else:
                    # Use electrolyte planner to allocate from vials and update inventory
                    inventory = load_inventory_state()
                    plan_payload = evaluate_formulation_with_vials(inventory, recipe)
                    if not plan_payload.get("feasible", False):
                        issues = plan_payload.get("issues", [])
                        self.get_logger().error(
                            f"Formulation not feasible for recipe '{recipe.get('recipe_name')}', issues: {issues}"
                        )
                        self.session_tracker.finish_battery(battery_record, status="failed_feasibility")
                        return

                    instructions = plan_payload.get("instructions", [])
                    
                    # Execute instructions, getting a fresh tip each time the substance changes
                    current_substance = None
                    tip_index = None
                    tip_x = None
                    tip_y = None
                    
                    for instr in instructions:
                        instr_substance = instr.get("source_solution")
                        
                        # Check if substance changed; if so, drop current tip and get a new one
                        if instr_substance != current_substance:
                            # Drop the current tip if we have one
                            if tip_index is not None:
                                self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                                tip_rack.mark_tip_used(tip_index, current_substance)
                            
                            # Get a new tip for the new substance
                            current_substance = instr_substance
                            tip_index = tip_rack.find_clean_tip_for_substance(current_substance)
                            if tip_index is None:
                                tip_index = tip_rack.find_clean_tip_for_substance(None)
                            if tip_index is None:
                                tip_index = 0  # Force use of first tip if none are clean
                            
                            tip_x, tip_y = _tip_index_to_coordinates(tip_index)
                            self.liquid_robot.MG400.get_tip(tip_x, tip_y)
                        
                        # Execute the instruction
                        sx = int(instr.get("source_x_ind", 0))
                        sy = int(instr.get("source_y_ind", 0))
                        vol = float(instr.get("volume_ul", 0.0))
                        if vol <= 0:
                            continue
                        # Aspirate from source vial and dispense to assembly post
                        self.liquid_robot.MG400.get_liquid(sx, sy, vol)
                        self.liquid_robot.MG400.add_liquid_to_post(vol)
                        # Blowout/return to source to clear the tip
                        self.liquid_robot.MG400.return_liquid(sx, sy)
                    
                    # Drop the final tip and mark as used
                    if tip_index is not None:
                        self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
                        tip_rack.mark_tip_used(tip_index, current_substance)
                    
                    self.liquid_robot.MG400.move_home()
                    save_tip_rack_state(tip_rack)

                    # Persist updated inventory returned by the planner
                    updated_inv = plan_payload.get("updated_inventory")
                    if updated_inv is not None:
                        try:
                            save_inventory_state(Inventory(**updated_inv))
                        except Exception:
                            # As a fallback, try saving the in-memory Inventory object
                            try:
                                save_inventory_state(inventory)
                            except Exception as e:
                                self.get_logger().warning(f"Failed to save updated inventory: {e}")
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

    prompt = """------------------------
Electrolyte Planner Menu
[V]iew vial status
[A]dd/update vial contents (after physical refill)
[C]leaned vial (mark as empty)
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

            solution_name = input("Solution name: ").strip()
            if _is_cancel(solution_name):
                print("Canceled add/update operation.")
                continue

            density_g_per_ml = _read_positive_float_or_cancel("Density (g/mL): ")
            if density_g_per_ml is None:
                print("Canceled add/update operation.")
                continue

            volume_ul = _read_positive_float_or_cancel("Current volume in vial (uL): ")
            if volume_ul is None:
                print("Canceled add/update operation.")
                continue

            try:
                inventory = set_vial_contents(
                    inventory,
                    x_ind=x_ind,
                    y_ind=y_ind,
                    solution_name=solution_name,
                    volume_ul=volume_ul,
                    density_g_per_ml=density_g_per_ml,
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


def _recipes_batch_menu(batterylab: AutoBatteryLab):
    logger = batterylab.get_logger()
    recipes_path = input("Enter path to recipes JSON file (or type 'f' to open file chooser): ").strip()
    # Support opening a GUI file chooser and remember last-used folder
    LAST_RECIPE_DIR_PATH = Path.home() / ".batterylab" / "last_recipe_dir.txt"
    if recipes_path.lower() == "f":
        try:
            import tkinter as _tk
            from tkinter import filedialog as _filedlg

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
                return
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

        if required:
            print("Aggregated chemical requirements for this batch:")
            for sol, vol in required.items():
                avail = inventory.available_volume(sol)
                deficit = deficits.get(sol, 0.0)
                status = f"DEFICIT {deficit:.1f} uL" if deficit > 0 else "OK"
                print(f" - {sol}: required {vol:.1f} uL, available {avail:.1f} uL -> {status}")
        else:
            print("No ingredient-based requirements detected in recipes; proceeding with volume-only dispenses.")
        # Offer test/dry-run and movement-simulation options
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
                        _simulate_recipe_execution_with_movements(recipes[recipe_idx], inventory, batterylab.liquid_robot)
                    else:
                        print(f"Invalid selection. Please enter a number between 1 and {len(recipes)}.")
                except ValueError:
                    print("Invalid input. Please enter a recipe number or 'q'.")
            
            action = input("Proceed to assemble these recipes now? (y/n): ").strip().lower()
            if action != "y":
                print("Canceled after movement-simulation.")
                return
        if action == "a":
            batterylab.assemble_batteries_in_series(
                recipes,
                recipe_source_path=str(recipe_file.resolve()),
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


def command_loop(batterylab: AutoBatteryLab):
    prompt = """
===============================================
Welcome to BatteryLab! Please select a command:
[Enter] to quit
[A]ssembly robot submenu
[L]iquid   robot submenu
[C]rimper  robot submenu
[B]atch recipes file input to assemble series of batteries
[O]ne battery demonstration (single assembly using defaults and no recipe)
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
        elif user_input == "o":
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
    finally:
        batterylab.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

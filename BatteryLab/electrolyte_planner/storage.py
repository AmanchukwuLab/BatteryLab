"""Persistent storage helpers for electrolyte planner inventory state."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .models import Inventory, TipRack


DEFAULT_STATE_PATH = Path.home() / ".batterylab" / "electrolyte_inventory.json"
DEFAULT_TIP_RACK_PATH = Path.home() / ".batterylab" / "tip_rack.json"


def _serialize_inventory(inventory: Inventory) -> dict:
    if hasattr(inventory, "model_dump"):
        return inventory.model_dump()
    return inventory.dict()


def _find_vials_missing_density(raw: dict) -> list:
    vials = raw.get("vials") or []
    missing = []
    for i, vial in enumerate(vials):
        name = vial.get("current_solution_name")
        density = vial.get("current_solution_density_g_per_ml")
        # Treat None, non-numeric, or non-positive values as missing/invalid.
        is_invalid = False
        if density is None:
            is_invalid = True
        else:
            try:
                dval = float(density)
                if dval <= 0:
                    is_invalid = True
            except Exception:
                is_invalid = True

        if name and is_invalid:
            missing.append((i, vial))
    return missing


def _normalize_empty_vial_densities(raw: dict) -> dict:
    """Ensure empty/unassigned vials always carry a valid placeholder density.

    The `VialContents` model now requires a positive density for every vial,
    including empty ones. Older inventory files may have null density values on
    empty vials; normalize those to 1.0 before model validation.
    """
    vials = raw.get("vials") or []
    changed = False
    for vial in vials:
        current_solution = vial.get("current_solution_name")
        density = vial.get("current_solution_density_g_per_ml")

        if current_solution is not None:
            continue

        invalid = False
        if density is None:
            invalid = True
        else:
            try:
                invalid = float(density) <= 0
            except Exception:
                invalid = True

        if invalid:
            vial["current_solution_density_g_per_ml"] = 1.0
            changed = True

    if changed:
        raw["vials"] = vials
    return raw


def _interactive_fill_missing_densities(raw: dict, state_path: Path) -> dict:
    missing = _find_vials_missing_density(raw)
    if not missing:
        return raw

    if not sys.stdin.isatty():
        raise RuntimeError(
            f"Inventory file {state_path} contains vials with missing densities. Run interactively to supply densities or clear vials."
        )

    print(f"Found {len(missing)} vial(s) with missing or invalid densities in {state_path}.")
    for idx, vial in missing:
        x = vial.get("x_ind")
        y = vial.get("y_ind")
        name = vial.get("current_solution_name")
        vol = vial.get("volume_ul", 0)
        prompt = (
            f"Vial at (x={x}, y={y}) contains '{name}' with volume {vol} uL.\n"
            "Enter density in g/mL (e.g. 1.03), or type 'c' to clear this vial: "
        )
        while True:
            resp = input(prompt).strip()
            if resp.lower() in {"c", "clear"}:
                # Clear vial but keep density placeholder (1.0) to satisfy model
                raw_vial = raw.setdefault("vials")[idx]
                raw_vial["previous_solution_name"] = raw_vial.get("current_solution_name")
                raw_vial["current_solution_name"] = None
                raw_vial["current_solution_density_g_per_ml"] = 1.0
                raw_vial["volume_ul"] = 0.0
                print(f"Cleared vial at (x={x}, y={y}).")
                break
            try:
                d = float(resp)
            except Exception:
                print("Please enter a numeric density (e.g. 1.03) or 'c' to clear the vial.")
                continue
            if d <= 0:
                print("Density must be greater than zero.")
                continue
            raw_vial = raw.setdefault("vials")[idx]
            raw_vial["current_solution_density_g_per_ml"] = d
            print(f"Set density for vial (x={x}, y={y}) to {d} g/mL.")
            break

    # Persist fixes back to disk
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(raw, handle, indent=2, sort_keys=True)
    print(f"Updated inventory saved to {state_path}")
    return raw


def load_inventory_state(path: str | Path = DEFAULT_STATE_PATH) -> Inventory:
    """Load inventory state from disk. Missing files return an empty inventory."""

    state_path = Path(path)
    if not state_path.exists():
        return Inventory()

    with state_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    raw = _normalize_empty_vial_densities(raw)

    # If any vials have missing densities, require interactive resolution before validation.
    raw = _interactive_fill_missing_densities(raw, state_path)

    try:
        return Inventory(**raw)
    except ValidationError as exc:
        raw = _normalize_empty_vial_densities(raw)
        # Catch the common density-missing case early and let the user repair it.
        remaining_missing = _find_vials_missing_density(raw)
        if remaining_missing:
            raw = _interactive_fill_missing_densities(raw, state_path)
            remaining_missing = _find_vials_missing_density(raw)
            if remaining_missing:
                details = ", ".join(
                    f"(x={vial.get('x_ind')}, y={vial.get('y_ind')}, solution={vial.get('current_solution_name')})"
                    for _, vial in remaining_missing
                )
                raise RuntimeError(
                    "Inventory still contains vials with missing densities after repair: "
                    f"{details}. Provide densities or empty those vials before starting the planner."
                ) from exc
            return Inventory(**raw)
        raise RuntimeError(
            f"Inventory validation failed for {state_path}: {exc}."
        ) from exc


def save_inventory_state(inventory: Inventory, path: str | Path = DEFAULT_STATE_PATH) -> Path:
    """Persist inventory state to disk and return the saved path."""

    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    payload = _serialize_inventory(inventory)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return state_path

def show_save_location(inventory: Inventory, path: str | Path = DEFAULT_STATE_PATH) -> Path:
    """Show the location where the inventory state would be saved without actually saving."""

    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    return state_path


def _serialize_tip_rack(tip_rack: TipRack) -> dict:
    if hasattr(tip_rack, "model_dump"):
        return tip_rack.model_dump()
    return tip_rack.dict()


def _initialize_default_tip_rack() -> TipRack:
    """Create a new tip rack with 96 clean tips."""
    from .models import TipContents
    tips = [TipContents(index=i, is_clean=True) for i in range(96)]
    return TipRack(tips=tips)


def load_tip_rack_state(path: str | Path = DEFAULT_TIP_RACK_PATH) -> TipRack:
    """Load tip rack state from disk. Missing files return a new 96-tip rack."""

    state_path = Path(path)
    if not state_path.exists():
        return _initialize_default_tip_rack()

    try:
        with state_path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return TipRack(**raw)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load tip rack state from {state_path}: {exc}."
        ) from exc


def save_tip_rack_state(tip_rack: TipRack, path: str | Path = DEFAULT_TIP_RACK_PATH) -> Path:
    """Persist tip rack state to disk and return the saved path."""

    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    payload = _serialize_tip_rack(tip_rack)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    return state_path

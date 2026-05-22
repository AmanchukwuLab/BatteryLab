"""Inventory mutation helpers for vial assignment and reset operations."""

from __future__ import annotations

from typing import Optional

from .models import Inventory, VialContents


def _to_inventory(inventory_data: Inventory | dict) -> Inventory:
    return inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)


def _find_vial(inventory: Inventory, x_ind: int, y_ind: int) -> Optional[VialContents]:
    for vial in inventory.vials:
        if vial.x_ind == x_ind and vial.y_ind == y_ind:
            return vial
    return None


def set_vial_contents(
    inventory_data: Inventory | dict,
    x_ind: int,
    y_ind: int,
    solution_name: str,
    volume_ul: float,
    density_g_per_ml: float,
    *,
    create_if_missing: bool = True,
) -> Inventory:
    """Set or replace the solution assignment for a vial.

    Behavior:
    - If the vial exists, update its current solution/volume/density.
    - If the solution changes, preserve the old value in previous_solution_name.
    - If the vial does not exist, optionally create it.
    """

    inventory = _to_inventory(inventory_data)
    solution_name = solution_name.strip()

    if x_ind < 0 or y_ind < 0:
        raise ValueError("x_ind and y_ind must be >= 0")
    if not solution_name:
        raise ValueError("solution_name must not be empty")
    if density_g_per_ml <= 0:
        raise ValueError("density_g_per_ml must be > 0")

    target = _find_vial(inventory, x_ind, y_ind)
    if target is None:
        if not create_if_missing:
            raise KeyError(f"vial coordinates not found: x_ind={x_ind}, y_ind={y_ind}")
        inventory.vials.append(
            VialContents(
                x_ind=x_ind,
                y_ind=y_ind,
                current_solution_name=solution_name,
                previous_solution_name=None,
                current_solution_density_g_per_ml=density_g_per_ml,
                volume_ul=volume_ul,
            )
        )
        return inventory

    if target.current_solution_name and target.current_solution_name != solution_name:
        target.previous_solution_name = target.current_solution_name

    target.current_solution_name = solution_name
    target.current_solution_density_g_per_ml = density_g_per_ml
    target.volume_ul = volume_ul

    # Re-validate constraints by round-tripping through model parsing.
    return Inventory(**(inventory.model_dump() if hasattr(inventory, "model_dump") else inventory.dict()))


def clear_vial(inventory_data: Inventory | dict, x_ind: int, y_ind: int) -> Inventory:
    """Clear a vial while preserving previous solution identity for reuse decisions."""

    inventory = _to_inventory(inventory_data)
    if x_ind < 0 or y_ind < 0:
        raise ValueError("x_ind and y_ind must be >= 0")

    target = _find_vial(inventory, x_ind, y_ind)
    if target is None:
        raise KeyError(f"vial coordinates not found: x_ind={x_ind}, y_ind={y_ind}")

    if target.current_solution_name:
        target.previous_solution_name = target.current_solution_name
    target.current_solution_name = None
    # When clearing a vial, keep a valid density value to satisfy the model; use 1.0 as a neutral placeholder.
    target.current_solution_density_g_per_ml = 1.0
    target.volume_ul = 0.0

    return Inventory(**(inventory.model_dump() if hasattr(inventory, "model_dump") else inventory.dict()))

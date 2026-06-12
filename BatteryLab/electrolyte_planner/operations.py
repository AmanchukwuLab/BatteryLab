"""Inventory mutation helpers for vial assignment and reset operations."""

from __future__ import annotations

from typing import Optional

from .models import ElectrolyteSpec, Inventory, VialContents


def _to_inventory(inventory_data: Inventory | dict) -> Inventory:
    return inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)


def _find_vial(inventory: Inventory, x_ind: int, y_ind: int) -> Optional[VialContents]:
    for vial in inventory.vials:
        if vial.x_ind == x_ind and vial.y_ind == y_ind:
            return vial
    return None


def _to_electrolyte(electrolyte_data: ElectrolyteSpec | dict) -> ElectrolyteSpec:
    return electrolyte_data if isinstance(electrolyte_data, ElectrolyteSpec) else ElectrolyteSpec(**electrolyte_data)


def set_vial_contents(
    inventory_data: Inventory | dict,
    x_ind: int,
    y_ind: int,
    electrolyte: ElectrolyteSpec | dict,
    volume_ul: float,
    *,
    create_if_missing: bool = True,
) -> Inventory:
    """Set or replace the electrolyte assignment for a vial."""

    inventory = _to_inventory(inventory_data)
    electrolyte_spec = _to_electrolyte(electrolyte)

    if x_ind < 0 or y_ind < 0:
        raise ValueError("x_ind and y_ind must be >= 0")

    target = _find_vial(inventory, x_ind, y_ind)
    if target is None:
        if not create_if_missing:
            raise KeyError(f"vial coordinates not found: x_ind={x_ind}, y_ind={y_ind}")
        inventory.vials.append(
            VialContents(
                x_ind=x_ind,
                y_ind=y_ind,
                current_electrolyte=electrolyte_spec,
                previous_electrolyte=None,
                volume_ul=volume_ul,
            )
        )
        return inventory

    if target.current_electrolyte and target.current_electrolyte.name != electrolyte_spec.name:
        target.previous_electrolyte = target.current_electrolyte

    target.current_electrolyte = electrolyte_spec
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

    if target.current_electrolyte:
        target.previous_electrolyte = target.current_electrolyte
    target.current_electrolyte = None
    target.volume_ul = 0.0

    return Inventory(**(inventory.model_dump() if hasattr(inventory, "model_dump") else inventory.dict()))

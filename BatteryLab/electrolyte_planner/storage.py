"""Persistent storage helpers for electrolyte planner inventory state."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Inventory


DEFAULT_STATE_PATH = Path.home() / ".batterylab" / "electrolyte_inventory.json"


def _serialize_inventory(inventory: Inventory) -> dict:
    if hasattr(inventory, "model_dump"):
        return inventory.model_dump()
    return inventory.dict()


def load_inventory_state(path: str | Path = DEFAULT_STATE_PATH) -> Inventory:
    """Load inventory state from disk. Missing files return an empty inventory."""

    state_path = Path(path)
    if not state_path.exists():
        return Inventory()

    with state_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return Inventory(**raw)


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

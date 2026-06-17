# Electrolyte Planner

This subpackage provides a minimal, standalone interface for:

- tracking which stock solutions are stored in each robot-accessible vial,
- storing solvency `Electrolyte` identities for each currently assigned vial,
- accessing solvency's interface for checking whether a requested formulation is possible from current inventory,
- generating machine-readable pipetting instructions.

It also supports persistence of vial inventory to JSON so state can survive
application restarts.

Recipes now use solvency-style electrolyte objects directly, with fields for `name`, `volume`, `v`olume fractions, `s`alt molarities, and `a`dditive molarities (see below).

## Solvency feasibility example

```python
from BatteryLab.electrolyte_planner import evaluate_formulation
inventory = {
    "vials": [
        {"x_ind": 0, "y_ind": 0, "current_electrolyte": {"name": "water_stock", "v": {"water": 1.0}}, "volume_ul": 800},
        {"x_ind": 0, "y_ind": 1, "current_electrolyte": {"name": "PG_stock", "v": {"propylene glycol": 1.0}}, "volume_ul": 800},
    ]
}

request = {
    "recipe_name": "baseline_mix",
    "target_electrolyte": {
        "name": "baseline_target",
        "volume": 0.05,
        "v": {"water": 0.5, "propylene glycol": 0.5},
    }
}

plan = evaluate_formulation(inventory, request)
```

TODO: continue editing here

`evaluate_formulation(...)` returns a plain dictionary with:

- `feasible`: whether the formulation can be made,
- `instructions`: a list of transfer steps,
- `issues`: why the request could not be satisfied, if applicable.

## Vial tracking and low-volume flags

Vials are modeled with a 1500 uL maximum. The helper
`evaluate_formulation_with_vials(...)` will:

- evaluate feasibility,
- consume required volume from matching vials,
- return `low_volume_flag` and detailed `vial_alerts`,
- return `vial_usage` records for per-operation reporting,
- preserve `previous_solution_name` even when a vial reaches zero (for
  cleaning/reuse evaluation).

By default, a vial is considered:

- low when remaining volume is `<= 120 uL`,
- empty/unusable when remaining volume is `<= 30 uL`.

## Persistence
Use the storage helpers to keep state across restarts:

```python
from BatteryLab.electrolyte_planner import (
    evaluate_formulation_with_vials,
    load_inventory_state,
    save_inventory_state,
)

inventory = load_inventory_state()
result = evaluate_formulation_with_vials(inventory, request)
save_inventory_state(inventory)
```

If you call `evaluate_formulation_with_vials(...)` with plain dictionaries,
persist `result["updated_inventory"]` instead of the original input dictionary.

## Manual vial assignment

Use helper functions to update vial identity and volume:

```python
from BatteryLab.electrolyte_planner import (
    clear_vial,
    load_inventory_state,
    save_inventory_state,
    set_vial_contents,
)

inventory = load_inventory_state()

# Set or replace what is in a vial
inventory = set_vial_contents(inventory, 0, 0, "ZnSO4_1M", 1450, 1.03)

# Clear a vial while preserving previous_solution_name
inventory = clear_vial(inventory, 0, 1)

save_inventory_state(inventory)
```

## Status and operation reporting

You can print current vial statuses (with LOW/EMPTY highlighting):

```python
from BatteryLab.electrolyte_planner import print_vial_statuses

print_vial_statuses(inventory)
```

After an operation, print a usage/update summary:

```python
from BatteryLab.electrolyte_planner import (
    evaluate_formulation_with_vials,
    print_operation_update,
)

result = evaluate_formulation_with_vials(inventory, request)
print_operation_update(result)
```

This includes:

- feasibility + warning flags,
- per-vial consumption (`solution_name`, `x_ind`, `y_ind`, `used_volume_ul`, `remaining_volume_ul`),
- current low/empty alerts.
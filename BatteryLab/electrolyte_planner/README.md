# Electrolyte Planner

This subpackage provides a minimal, standalone interface for:

- tracking which stock solutions are stored in each robot-accessible vial,
- storing density for each currently assigned solution,
- checking whether a requested formulation is possible from current inventory,
- generating machine-readable pipetting instructions.

It also supports persistence of vial inventory to JSON so state can survive
application restarts.

The planner supports two recipe input modes:

- volume-based ingredients (`volume_ul` per component),
- weight-percent ingredients (`weight_percent` per component) with
    `electrolyte_volume_ul`.

For weight-percent mode, each component's density is read from its assigned vial
(`current_solution_density_g_per_ml`) and used to convert weight fractions to
required dispense volumes.

## Volume-based feasibility example

```python
from BatteryLab.electrolyte_planner import evaluate_formulation
inventory = {
    "vials": [
        {"x_ind": 0, "y_ind": 0, "current_solution_name": "ZnSO4_1M_water", "current_solution_density_g_per_ml": 1.02, "volume_ul": 800},
        {"x_ind": 0, "y_ind": 1, "current_solution_name": "H2O", "current_solution_density_g_per_ml": 1.000, "volume_ul": 2000},
        {"x_ind": 1, "y_ind": 0, "current_solution_name": "ZnCl2_1M_water", "current_solution_density_g_per_ml": 1.04, "volume_ul": 400},
    ]
}

request = {
    "recipe_name": "zn_aqueous_baseline",
    "destination": "mix_vessel_01",
    "ingredients": [
        {"solution_name": "ZnSO4_1M_water", "volume_ul": 600},
        {"solution_name": "H2O", "volume_ul": 800},
    ],
}

plan = evaluate_formulation(inventory, request)
```

`evaluate_formulation(...)` returns a plain dictionary with:

- `feasible`: whether the formulation can be made,
- `instructions`: a list of transfer steps,
- `issues`: why the request could not be satisfied, if applicable.

Transfer instructions use `source_x_ind` and `source_y_ind`.

## Weight-percent recipe example

```python
from BatteryLab.electrolyte_planner import evaluate_formulation
inventory = {
    "vials": [
        {"x_ind": 0, "y_ind": 0, "current_solution_name": "ZnSO4_stock", "current_solution_density_g_per_ml": 1.030, "volume_ul": 1200},
        {"x_ind": 0, "y_ind": 1, "current_solution_name": "H2O", "current_solution_density_g_per_ml": 1.000, "volume_ul": 2000},
    ]
}

request = {
    "recipe_name": "zn_water_50wt",
    "destination": "mix_vessel_01",
    "electrolyte_volume_ul": 600,
    "ingredients": [
        {"solution_name": "ZnSO4_stock", "weight_percent": 50.0},
        {"solution_name": "H2O", "weight_percent": 50.0},
    ],
}

plan = evaluate_formulation(inventory, request)
```

## Vial tracking and low-volume flags

Vials are modeled with a 1.5 mL maximum (`1500 uL`). The helper
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
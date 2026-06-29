"""Feasibility checks and instruction generation for formulations."""

from __future__ import annotations

from typing import Dict, List, Sequence

from .. import solvency
Electrolyte = solvency.core.Electrolyte
e_solver = solvency.core.e_solver

from .models import (
    DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
    FeasibilityIssue,
    FormulationPlan,
    FormulationRequest,
    Inventory,
    TransferInstruction,
    VialAlert,
    VialContents,
    VialUsageRecord,
)


def _serialize_model(model: FormulationPlan) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _sort_vials(vials: Sequence[VialContents]) -> List[VialContents]:
    """Sort vials by (x_ind, y_ind) for deterministic allocation order."""
    return sorted(vials, key=lambda item: (item.x_ind, item.y_ind))


def _build_solvency_bank(inventory: Inventory) -> List[Electrolyte]:
    """Convert inventory vials to a list of solvency Electrolyte objects for planning."""
    bank: List[Electrolyte] = []
    for vial in inventory.vials:
        if vial.current_electrolyte is not None:
            bank.append(vial.current_electrolyte.to_solvency())
    return bank
    


def _resolve_required_volumes(
    inventory: Inventory, request: FormulationRequest
) -> Dict[str, float]:
    """Determine how much volume of each stock solution is needed for the target electrolyte."""
    bank   = _build_solvency_bank(inventory)
    target = request.target_electrolyte.to_solvency()

    solution = e_solver(bank, target)
    required_by_solution: Dict[str, float] = {}
    for solution_name, fraction in solution.items():
        required_by_solution[solution_name] = fraction * (request.target_electrolyte.volume)
    return required_by_solution

def _allocate_from_vials(
    vials: Sequence[VialContents], solution_name: str, required_volume_ul: float
) -> List[tuple[int, int, str, float]]:
    """Determine which vials to draw from and how much for each to meet the required volume."""
    remaining = required_volume_ul
    transfers: List[tuple[int, int, str, float]] = []

    for vial in _sort_vials(vials):
        if remaining <= 0:
            break
        if vial.current_electrolyte is None or vial.current_electrolyte.name != solution_name:
            continue

        transfer_volume = min(vial.volume_ul, remaining)
        if transfer_volume > 0:
            transfers.append((vial.x_ind, vial.y_ind, solution_name, transfer_volume))
            remaining -= transfer_volume

    return transfers


# DEPRECATED: used in an older version of the planner
# def _consume_solution_from_vials(
#     vials: List[VialContents],
#     solution_name: str,
#     required_volume_ul: float,
# ) -> List[VialUsageRecord]:
#     """Update vial volumes to reflect consumption and return usage records for any vials that were drawn from."""
#     remaining = required_volume_ul
#     usage_records: List[VialUsageRecord] = []
#     for vial in _sort_vials(vials):
#         if remaining <= 0:
#             break
#         if vial.current_electrolyte is None or vial.current_electrolyte.name != solution_name:
#             continue

#         draw_volume = min(vial.volume_ul, remaining)
#         vial.volume_ul -= draw_volume
#         remaining -= draw_volume
#         if draw_volume > 0:
#             usage_records.append(
#                 VialUsageRecord(
#                     x_ind=vial.x_ind,
#                     y_ind=vial.y_ind,
#                     solution_name=solution_name,
#                     used_volume_ul=draw_volume,
#                     remaining_volume_ul=vial.volume_ul,
#                 )
#             )

#         if vial.volume_ul <= 0:
#             # Consider adding a warning if volume is negative. This would indicate a bug in the planner
#             vial.volume_ul = 0.0
#             # Preserve history to support cleaning/reuse decisions.
#             vial.previous_electrolyte = vial.current_electrolyte
#             vial.current_electrolyte = None

#     return usage_records


def plan_formulation(inventory: Inventory, request: FormulationRequest) -> FormulationPlan:
    """Return a feasibility result and pipetting instructions.

    The planner treats each ingredient as a required stock solution and allocates
    from vials in deterministic vial-id order. The output is intentionally JSON-
    friendly so a robot process can parse it without understanding the planner.
    """

    issues: List[FeasibilityIssue] = []
    instructions: List[TransferInstruction] = []
    step_index = 1
    try:
        required_by_solution = _resolve_required_volumes(inventory, request)
    except ValueError as ve:
        print(f"Error resolving required volumes: {ve}")
        target_volume_ul = (request.target_electrolyte.volume)
        return FormulationPlan(
            feasible=False,
            recipe_name=request.recipe_name,
            total_required_volume_ul=target_volume_ul,
            instructions=[],
            issues=[
                FeasibilityIssue(
                    solution_name=request.target_electrolyte.name,
                    required_volume_ul=target_volume_ul,
                    available_volume_ul=0.0,
                    deficit_volume_ul=target_volume_ul,
                )
            ],
            low_volume_flag=False,
            vial_alerts=[],
            vial_usage=[],
        )
    
    total_required_volume_ul = sum(required_by_solution.values())

    # Confirm that inventory can meet required volumes before generating instructions
    for solution_name, required_volume in required_by_solution.items():
        available_volume = inventory.available_volume(solution_name)
        if available_volume < required_volume:
            issues.append(
                FeasibilityIssue(
                    solution_name=solution_name,
                    required_volume_ul=required_volume,
                    available_volume_ul=available_volume,
                    deficit_volume_ul=required_volume - available_volume,
                )
            )

    if issues:
        return FormulationPlan(
            feasible=False,
            recipe_name=request.recipe_name,
            total_required_volume_ul=total_required_volume_ul,
            instructions=[],
            issues=issues,
            low_volume_flag=False,
            vial_alerts=[],
            vial_usage=[],
        )

    # No issues found, so generate instructions to return
    for solution_name, required_volume in required_by_solution.items():
        transfers = _allocate_from_vials(
            inventory.vials,
            solution_name,
            required_volume,
        )
        for source_x_ind, source_y_ind, source_solution, volume_ul in transfers:
            instructions.append(
                TransferInstruction(
                    step_index=step_index,
                    ingredient_name=solution_name,
                    source_x_ind=source_x_ind,
                    source_y_ind=source_y_ind,
                    source_solution=source_solution,
                    volume_ul=volume_ul,
                )
            )
            step_index += 1

    return FormulationPlan(
        feasible=True,
        recipe_name=request.recipe_name,
        total_required_volume_ul=total_required_volume_ul,
        instructions=instructions,
        issues=[],
        low_volume_flag=False,
        vial_alerts=[],
        vial_usage=[],
    )


# def plan_and_update_vials(
#     inventory: Inventory,
#     request: FormulationRequest,
#     empty_threshold_ul: float = DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
# ) -> FormulationPlan:
#     """Plan a formulation and update in-memory vial volumes.

#     This function mutates ``inventory.vials`` to represent post-dispense vial
#     state. It also returns vial alerts and a top-level low-volume flag so the
#     caller can surface warnings in the main application.
#     """

#     plan = plan_formulation(inventory, request)
#     if not plan.feasible:
#         plan.vial_alerts = inventory.update_vial_alerts()
#         plan.low_volume_flag = any(
#             alert.low_volume_flag or alert.empty_or_unusable_flag
#             for alert in plan.vial_alerts
#         )
#         return plan

#     required_by_solution = _resolve_required_volumes(inventory, request)
#     vial_usage_records: List[VialUsageRecord] = []

#     for solution_name, required_volume in required_by_solution.items():
#         usage = _consume_solution_from_vials(inventory.vials, solution_name, required_volume)
#         vial_usage_records.extend(usage)

#     plan.vial_alerts = inventory.update_vial_alerts()
#     plan.vial_usage = vial_usage_records
#     plan.low_volume_flag = any(
#         alert.low_volume_flag or alert.empty_or_unusable_flag
#         for alert in plan.vial_alerts
#     )
#     return plan


def evaluate_formulation(
    inventory_data: Inventory | dict, 
    request_data: FormulationRequest | dict
) -> dict:
    """Convenience wrapper for JSON-like input and output."""

    inventory = inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)
    request = (
        request_data
        if isinstance(request_data, FormulationRequest)
        else FormulationRequest(**request_data)
    )
    plan = plan_formulation(inventory, request)

    if not plan.feasible:
        plan.vial_alerts = inventory.update_vial_alerts()
        plan.low_volume_flag = any(
            alert.low_volume_flag or alert.empty_or_unusable_flag
            for alert in plan.vial_alerts
        )
        return plan
    
    return _serialize_model(plan)
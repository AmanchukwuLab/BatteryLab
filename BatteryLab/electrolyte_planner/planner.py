"""Feasibility checks and instruction generation for formulations."""

from __future__ import annotations

from typing import Dict, List, Sequence

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
    return sorted(vials, key=lambda item: item.vial_id)


def _resolve_required_volumes(
    inventory: Inventory, request: FormulationRequest
) -> Dict[str, float]:
    required_by_solution: Dict[str, float] = {}
    if not request.ingredients:
        return required_by_solution

    is_weight_recipe = request.ingredients[0].weight_percent is not None

    if not is_weight_recipe:
        for ingredient in request.ingredients:
            ingredient_volume = ingredient.volume_ul or 0.0
            required_by_solution[ingredient.solution_name] = (
                required_by_solution.get(ingredient.solution_name, 0.0)
                + ingredient_volume
            )
        return required_by_solution

    # Weight-percent to volume conversion from target total volume using densities.
    # For each ingredient i: v_i = V_total * (w_i/rho_i) / sum_j(w_j/rho_j)
    target_volume_ml = (request.target_total_volume_ul or 0.0) / 1000.0
    weight_over_density = []
    for ingredient in request.ingredients:
        density = inventory.density_for_solution(ingredient.solution_name)
        weight_fraction = (ingredient.weight_percent or 0.0) / 100.0
        weight_over_density.append((ingredient.solution_name, weight_fraction / density))

    denominator = sum(item[1] for item in weight_over_density)
    if denominator <= 0:
        raise ValueError("Invalid weight_percent/density combination for conversion")

    for solution_name, term in weight_over_density:
        ingredient_volume_ul = (target_volume_ml * term / denominator) * 1000.0
        required_by_solution[solution_name] = (
            required_by_solution.get(solution_name, 0.0)
            + ingredient_volume_ul
        )
    return required_by_solution


def _allocate_from_vials(
    vials: Sequence[VialContents], solution_name: str, required_volume_ul: float
) -> List[tuple[str, str, float]]:
    remaining = required_volume_ul
    transfers: List[tuple[str, str, float]] = []

    for vial in _sort_vials(vials):
        if remaining <= 0:
            break
        if vial.current_solution_name != solution_name:
            continue

        transfer_volume = min(vial.volume_ul, remaining)
        if transfer_volume > 0:
            transfers.append((vial.vial_id, solution_name, transfer_volume))
            remaining -= transfer_volume

    return transfers


def _consume_solution_from_vials(
    vials: List[VialContents],
    solution_name: str,
    required_volume_ul: float,
) -> List[VialUsageRecord]:
    remaining = required_volume_ul
    usage_records: List[VialUsageRecord] = []
    for vial in _sort_vials(vials):
        if remaining <= 0:
            break
        if vial.current_solution_name != solution_name:
            continue

        draw_volume = min(vial.volume_ul, remaining)
        vial.volume_ul -= draw_volume
        remaining -= draw_volume
        if draw_volume > 0:
            usage_records.append(
                VialUsageRecord(
                    vial_id=vial.vial_id,
                    solution_name=solution_name,
                    used_volume_ul=draw_volume,
                    remaining_volume_ul=vial.volume_ul,
                )
            )

        if vial.volume_ul <= 0:
            vial.volume_ul = 0.0
            # Preserve history to support cleaning/reuse decisions.
            vial.previous_solution_name = vial.current_solution_name
            vial.current_solution_name = None
            vial.current_solution_density_g_per_ml = None

    return usage_records


def _build_vial_alerts(
    vials: Sequence[VialContents],
    empty_threshold_ul: float,
) -> List[VialAlert]:
    alerts: List[VialAlert] = []
    for vial in _sort_vials(vials):
        low_flag = vial.volume_ul <= vial.low_volume_threshold_ul
        empty_flag = vial.volume_ul <= empty_threshold_ul
        if low_flag or empty_flag:
            alerts.append(
                VialAlert(
                    vial_id=vial.vial_id,
                    current_solution_name=vial.current_solution_name,
                    previous_solution_name=vial.previous_solution_name,
                    remaining_volume_ul=vial.volume_ul,
                    low_volume_flag=low_flag,
                    empty_or_unusable_flag=empty_flag,
                )
            )
    return alerts


def plan_formulation(inventory: Inventory, request: FormulationRequest) -> FormulationPlan:
    """Return a feasibility result and pipetting instructions.

    The planner treats each ingredient as a required stock solution and allocates
    from vials in deterministic vial-id order. The output is intentionally JSON-
    friendly so a robot process can parse it without understanding the planner.
    """

    issues: List[FeasibilityIssue] = []
    instructions: List[TransferInstruction] = []
    step_index = 1
    required_by_solution = _resolve_required_volumes(inventory, request)
    total_required_volume_ul = sum(required_by_solution.values())

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
            destination=request.destination,
            total_required_volume_ul=total_required_volume_ul,
            instructions=[],
            issues=issues,
            low_volume_flag=False,
            vial_alerts=[],
            vial_usage=[],
        )

    for solution_name, required_volume in required_by_solution.items():
        transfers = _allocate_from_vials(
            inventory.vials,
            solution_name,
            required_volume,
        )
        for source_vial, source_solution, volume_ul in transfers:
            instructions.append(
                TransferInstruction(
                    step_index=step_index,
                    ingredient_name=solution_name,
                    source_vial=source_vial,
                    source_solution=source_solution,
                    destination=request.destination,
                    volume_ul=volume_ul,
                )
            )
            step_index += 1

    return FormulationPlan(
        feasible=True,
        recipe_name=request.recipe_name,
        destination=request.destination,
        total_required_volume_ul=total_required_volume_ul,
        instructions=instructions,
        issues=[],
        low_volume_flag=False,
        vial_alerts=[],
        vial_usage=[],
    )


def plan_and_update_vials(
    inventory: Inventory,
    request: FormulationRequest,
    empty_threshold_ul: float = DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
) -> FormulationPlan:
    """Plan a formulation and update in-memory vial volumes.

    This function mutates ``inventory.vials`` to represent post-dispense vial
    state. It also returns vial alerts and a top-level low-volume flag so the
    caller can surface warnings in the main application.
    """

    plan = plan_formulation(inventory, request)
    if not plan.feasible:
        plan.vial_alerts = _build_vial_alerts(inventory.vials, empty_threshold_ul)
        plan.low_volume_flag = any(
            alert.low_volume_flag or alert.empty_or_unusable_flag
            for alert in plan.vial_alerts
        )
        return plan

    required_by_solution = _resolve_required_volumes(inventory, request)
    vial_usage_records: List[VialUsageRecord] = []

    for solution_name, required_volume in required_by_solution.items():
        usage = _consume_solution_from_vials(inventory.vials, solution_name, required_volume)
        vial_usage_records.extend(usage)

    plan.vial_alerts = _build_vial_alerts(inventory.vials, empty_threshold_ul)
    plan.vial_usage = vial_usage_records
    plan.low_volume_flag = any(
        alert.low_volume_flag or alert.empty_or_unusable_flag
        for alert in plan.vial_alerts
    )
    return plan


def evaluate_formulation(
    inventory_data: Inventory | dict, request_data: FormulationRequest | dict
) -> dict:
    """Convenience wrapper for JSON-like input and output."""

    inventory = inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)
    request = (
        request_data
        if isinstance(request_data, FormulationRequest)
        else FormulationRequest(**request_data)
    )
    plan = plan_formulation(inventory, request)
    return _serialize_model(plan)


def evaluate_formulation_with_vials(
    inventory_data: Inventory | dict,
    request_data: FormulationRequest | dict,
    empty_threshold_ul: float = DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
) -> dict:
    """Evaluate feasibility, update vial inventory, and return alerts.

    Output includes:
    - normal feasibility result/instructions
    - ``low_volume_flag`` for easy application-level warning handling
    - ``vial_alerts`` with detailed per-vial state
    """

    inventory = (
        inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)
    )
    request = (
        request_data
        if isinstance(request_data, FormulationRequest)
        else FormulationRequest(**request_data)
    )
    plan = plan_and_update_vials(inventory, request, empty_threshold_ul=empty_threshold_ul)
    payload = _serialize_model(plan)

    # Include updated vial state so callers can persist it between sessions.
    if hasattr(inventory, "model_dump"):
        payload["updated_inventory"] = inventory.model_dump()
    else:
        payload["updated_inventory"] = inventory.dict()
    return payload
"""Console-friendly reporting helpers for vial state and operation updates."""

from __future__ import annotations

from .models import DEFAULT_EMPTY_VOLUME_THRESHOLD_UL, Inventory, VialContents


def _to_inventory(inventory_data: Inventory | dict) -> Inventory:
    return inventory_data if isinstance(inventory_data, Inventory) else Inventory(**inventory_data)


def _status_label(vial: VialContents, empty_threshold_ul: float) -> str:
    if vial.volume_ul <= empty_threshold_ul:
        return "EMPTY"
    if vial.volume_ul <= vial.low_volume_threshold_ul:
        return "LOW"
    return "OK"


def format_vial_statuses(
    inventory_data: Inventory | dict,
    empty_threshold_ul: float = DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
) -> str:
    """Return a text table for current vial status with low/empty highlighting."""

    inventory = _to_inventory(inventory_data)
    if not inventory.vials:
        return "No vials configured."

    rows = []
    for vial in sorted(inventory.vials, key=lambda item: (item.x_ind, item.y_ind)):
        status = _status_label(vial, empty_threshold_ul)
        current_name = vial.current_electrolyte.name if vial.current_electrolyte else "-"
        previous_name = vial.previous_electrolyte.name if vial.previous_electrolyte else "-"
        rows.append(
            {
                "x_ind": str(vial.x_ind),
                "y_ind": str(vial.y_ind),
                "status": status,
                "current_solution": current_name,
                "previous_solution": previous_name,
                "remaining_uL": f"{vial.volume_ul:.1f}",
                "low_threshold_uL": f"{vial.low_volume_threshold_ul:.1f}",
            }
        )

    columns = [
        ("x_ind", "x_ind"),
        ("y_ind", "y_ind"),
        ("status", "status"),
        ("current_solution", "current_solution"),
        ("previous_solution", "previous_solution"),
        ("remaining_uL", "remaining_uL"),
        ("low_threshold_uL", "low_threshold_uL"),
    ]
    widths = {
        key: max(len(label), *(len(row[key]) for row in rows))
        for key, label in columns
    }

    lines = [
        "Vial Status",
        " | ".join(
            f"{label:<{widths[key]}}" for key, label in columns
        ),
        "-+-".join("-" * widths[key] for key, _ in columns),
    ]

    for row in rows:
        lines.append(
            " | ".join(
                f"{row[key]:<{widths[key]}}" for key, _ in columns
            )
        )

    return "\n".join(lines)


def print_vial_statuses(
    inventory_data: Inventory | dict,
    empty_threshold_ul: float = DEFAULT_EMPTY_VOLUME_THRESHOLD_UL,
) -> None:
    """Print vial status table to stdout."""

    print(format_vial_statuses(inventory_data, empty_threshold_ul=empty_threshold_ul))


def format_operation_update(result_payload: dict) -> str:
    """Return a post-operation summary from evaluator output."""

    lines = [
        "Operation Update",
        f"feasible={result_payload.get('feasible', False)}",
        f"low_volume_flag={result_payload.get('low_volume_flag', False)}",
    ]

    usage = result_payload.get("vial_usage", [])
    if usage:
        lines.append("vial_usage (solution, x_ind, y_ind, used_uL, remaining_uL):")
        for item in usage:
            lines.append(
                "- "
                f"{item.get('solution_name')} | {item.get('x_ind')} | {item.get('y_ind')} | "
                f"{float(item.get('used_volume_ul', 0.0)):.1f} | "
                f"{float(item.get('remaining_volume_ul', 0.0)):.1f}"
            )
    else:
        lines.append("vial_usage: none")

    alerts = result_payload.get("vial_alerts", [])
    if alerts:
        lines.append("alerts (x_ind, y_ind, remaining_uL, low, empty_or_unusable):")
        for alert in alerts:
            lines.append(
                "- "
                f"{alert.get('x_ind')} | {alert.get('y_ind')} | "
                f"{float(alert.get('remaining_volume_ul', 0.0)):.1f} | "
                f"{bool(alert.get('low_volume_flag', False))} | "
                f"{bool(alert.get('empty_or_unusable_flag', False))}"
            )

    return "\n".join(lines)


def print_operation_update(result_payload: dict) -> None:
    """Print a post-operation summary including vial usage and alerts."""

    print(format_operation_update(result_payload))

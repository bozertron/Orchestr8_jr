"""Canonical status merge policy — combat > broken > working."""

from typing import Literal

StatusType = Literal["working", "broken", "combat"]

STATUS_PRIORITY = {
    "combat": 3,
    "broken": 2,
    "working": 1,
}


def merge_status(*statuses: StatusType) -> StatusType:
    """Merge multiple status values using canonical precedence.

    Rule: combat > broken > working

    Returns 'working' for empty input or all-None input.
    Raises ValueError for unknown status values.
    """
    if not statuses:
        return "working"

    valid = [s for s in statuses if s is not None]
    if not valid:
        return "working"

    for s in valid:
        if s not in STATUS_PRIORITY:
            raise ValueError(f"Unknown status value: {s}")

    return max(valid, key=lambda s: STATUS_PRIORITY[s])


def get_status_color(status: StatusType) -> str:
    """Get canonical hex color for a status value."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
    }
    return colors.get(status, "#D4AF37")

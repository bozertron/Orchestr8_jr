"""Layout helpers for a_codex_plan.

Simplified layout utilities inspired by Orchestr8 patterns.
"""

import marimo as mo
from typing import Sequence, Any


def vstack(
    *elements: Any,
    gap: int = 1,
    align: str = "start",
    justify: str = "start",
) -> mo.ui.vstack:
    """Create a vertical stack layout.

    Args:
        *elements: Elements to stack vertically
        gap: Gap between elements
        align: Alignment (start, center, end, stretch)
        justify: Justification (start, center, end, space-between)

    Returns:
        mo.ui.vstack instance
    """
    return mo.ui.vstack(
        list(elements),
        gap=gap,
        align=align,
        justify=justify,
    )


def hstack(
    *elements: Any,
    gap: int = 1,
    align: str = "start",
    justify: str = "start",
) -> mo.ui.hstack:
    """Create a horizontal stack layout.

    Args:
        *elements: Elements to stack horizontally
        gap: Gap between elements
        align: Alignment (start, center, end, stretch)
        justify: Justification (start, center, end, space-between)

    Returns:
        mo.ui.hstack instance
    """
    return mo.ui.hstack(
        list(elements),
        gap=gap,
        align=align,
        justify=justify,
    )


def grid(
    *elements: Any,
    columns: int = 2,
    gap: int = 1,
) -> mo.ui.grid:
    """Create a grid layout.

    Args:
        *elements: Elements to place in grid
        columns: Number of columns
        gap: Gap between cells

    Returns:
        mo.ui.grid instance
    """
    return mo.ui.grid(
        list(elements),
        columns=columns,
        gap=gap,
    )


def stack(
    *elements: Any,
    direction: str = "vertical",
    gap: int = 1,
) -> mo.ui.vstack | mo.ui.hstack:
    """Create a stack layout (vertical or horizontal).

    Args:
        *elements: Elements to stack
        direction: "vertical" or "horizontal"
        gap: Gap between elements

    Returns:
        mo.ui.vstack or mo.ui.hstack
    """
    if direction == "vertical":
        return vstack(*elements, gap=gap)
    else:
        return hstack(*elements, gap=gap)

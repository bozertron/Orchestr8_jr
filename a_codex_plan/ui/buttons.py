"""Button components for a_codex_plan.

Stub implementations inspired by Orchestr8 button patterns.
"""

import marimo as mo


def create_header_button(
    label: str,
    on_click=None,
    *,
    variant: str = "primary",
    disabled: bool = False,
) -> mo.ui.button:
    """Create a header button with orchestr8 styling.

    Args:
        label: Button label text
        on_click: Callback function for button click
        variant: Button variant (primary, secondary, ghost)
        disabled: Whether button is disabled

    Returns:
        mo.ui.button instance
    """
    return mo.ui.button(
        label=label,
        on_click=on_click,
        disabled=disabled,
    )


def create_maestro_button(
    label: str,
    on_click=None,
    *,
    variant: str = "default",
    icon: str | None = None,
) -> mo.ui.button:
    """Create a maestro-style button for main actions.

    Args:
        label: Button label text
        on_click: Callback function
        variant: Visual variant (default, primary, danger)
        icon: Optional icon to include

    Returns:
        mo.ui.button instance
    """
    return mo.ui.button(
        label=label,
        on_click=on_click,
    )


def create_mini_button(
    label: str,
    on_click=None,
    *,
    compact: bool = True,
) -> mo.ui.button:
    """Create a mini button for compact UI contexts.

    Args:
        label: Button label
        on_click: Callback function
        compact: Whether to use compact styling

    Returns:
        mo.ui.button instance
    """
    return mo.ui.button(
        label=label,
        on_click=on_click,
    )

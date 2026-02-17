"""UI Component Library for a_codex_plan.

Simplified component stubs inspired by Orchestr8 patterns.
"""

from ui.buttons import (
    create_header_button,
    create_maestro_button,
    create_mini_button,
)
from ui.panels import (
    DeployPanel,
    TicketPanel,
    CommsPanel,
)
from ui.layouts import (
    vstack,
    hstack,
)
from ui.styles import load_css

__all__ = [
    # Buttons
    "create_header_button",
    "create_maestro_button",
    "create_mini_button",
    # Panels
    "DeployPanel",
    "TicketPanel",
    "CommsPanel",
    # Layouts
    "vstack",
    "hstack",
    # Styles
    "load_css",
]

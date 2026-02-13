"""Code City Contract Schemas - Blind Integration Safety Layer

Strongly-typed contracts for the surfaces where Code City, the Settlement System,
and the Marimo runtime meet. These schemas enforce deterministic behavior at
integration boundaries so that any future agent can wire components without
recovering prior context.

Color System:
    Gold   #D4AF37  = working
    Teal   #1fbdea  = broken
    Purple #9D4EDD  = combat

Status Precedence: combat > broken > working
"""

from .code_city_node_event import (
    CodeCityNodeEvent,
    validate_code_city_node_event,
    EXAMPLE_NODE_EVENT,
)
from .camera_state import CameraState, get_default_camera_state
from .settlement_survey import SettlementSurvey, parse_settlement_survey
from .status_merge_policy import merge_status, get_status_color, STATUS_PRIORITY
from .building_panel import (
    BuildingPanel,
    BuildingRoom,
    validate_building_panel,
    EXAMPLE_BUILDING_PANEL,
)
from .connection_action_event import (
    ConnectionActionEvent,
    ConnectionEdge,
    validate_connection_action_event,
    EXAMPLE_CONNECTION_ACTION,
)
from .lock_overlay import (
    LockOverlay,
    EXAMPLE_LOCK_OVERLAY,
)
from .town_square_classification import (
    TownSquareClassification,
    EXAMPLE_TOWN_SQUARE_CLASSIFICATION,
)

__all__ = [
    "CodeCityNodeEvent",
    "validate_code_city_node_event",
    "EXAMPLE_NODE_EVENT",
    "CameraState",
    "get_default_camera_state",
    "SettlementSurvey",
    "parse_settlement_survey",
    "merge_status",
    "get_status_color",
    "STATUS_PRIORITY",
    "BuildingPanel",
    "BuildingRoom",
    "validate_building_panel",
    "EXAMPLE_BUILDING_PANEL",
    "ConnectionActionEvent",
    "ConnectionEdge",
    "validate_connection_action_event",
    "EXAMPLE_CONNECTION_ACTION",
    "LockOverlay",
    "EXAMPLE_LOCK_OVERLAY",
    "TownSquareClassification",
    "EXAMPLE_TOWN_SQUARE_CLASSIFICATION",
]

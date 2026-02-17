"""Maestro feature modules."""

from .agent_groups import get_settlement_agent_groups
from .connection_actions import handle_connection_action
from .config import (
    BG_ELEVATED,
    BG_PRIMARY,
    BLUE_DOMINANT,
    FLAGSHIP_AGENT_SLUG,
    GOLD_DARK,
    GOLD_METALLIC,
    GOLD_SAFFRON,
    MAESTRO_STATES,
    PLUGIN_NAME,
    PLUGIN_ORDER,
    PURPLE_COMBAT,
    get_model_config,
    get_ui_font_profile,
    load_orchestr8_css,
)
from .views import (
    build_app_matrix_view,
    build_attachment_bar_view,
    build_control_surface_view,
    build_panels_view,
    build_summon_results_view,
    build_void_messages_view,
)

__all__ = [
    "FLAGSHIP_AGENT_SLUG",
    "PLUGIN_NAME",
    "PLUGIN_ORDER",
    "BLUE_DOMINANT",
    "GOLD_METALLIC",
    "GOLD_DARK",
    "GOLD_SAFFRON",
    "BG_PRIMARY",
    "BG_ELEVATED",
    "PURPLE_COMBAT",
    "MAESTRO_STATES",
    "get_model_config",
    "get_ui_font_profile",
    "load_orchestr8_css",
    "get_settlement_agent_groups",
    "handle_connection_action",
    "build_summon_results_view",
    "build_void_messages_view",
    "build_app_matrix_view",
    "build_attachment_bar_view",
    "build_panels_view",
    "build_control_surface_view",
]

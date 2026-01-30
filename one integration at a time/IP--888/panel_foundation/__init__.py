# IP/888/panel_foundation/__init__.py
"""
Panel Foundation - Base architecture for all [name]8 tools
Provides standardized interface and global registry for panel lifecycle management
"""

try:
    from .base_panel import BasePanel, PanelCapabilities
    from .panel_registry import PanelRegistry, get_panel_registry
except ImportError:
    # Fallback for direct execution
    from IP_888.panel_foundation.base_panel import BasePanel, PanelCapabilities
    from IP_888.panel_foundation.panel_registry import PanelRegistry, get_panel_registry

__all__ = ["BasePanel", "PanelCapabilities", "PanelRegistry", "get_panel_registry"]

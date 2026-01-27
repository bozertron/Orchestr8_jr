"""
Panel Foundation for future [name]8 applications.

This module provides the base architecture for communic8, actu8, cre8, and innov8
panels, establishing consistent patterns for future application integrations.
"""

from .base_panel import BasePanel, PanelCapabilities
from .panel_registry import PanelRegistry

__all__ = ['BasePanel', 'PanelCapabilities', 'PanelRegistry']

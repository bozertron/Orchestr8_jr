# IP/888/panel_foundation/panel_registry.py
"""
Panel Registry - Global registry for panel lifecycle management
Provides centralized management of all [name]8 tools
"""

from typing import Dict, List, Optional, Type, Callable
from datetime import datetime, timedelta
import threading
import time
import logging

from .base_panel import BasePanel, PanelSession, PanelStatus, PanelCapabilities

# Setup logging
logger = logging.getLogger(__name__)


class PanelRegistry:
    """
    Global registry for managing panel lifecycle

    This registry:
    - Tracks all registered panels
    - Manages panel initialization and cleanup
    - Provides health monitoring
    - Handles inter-panel communication
    - Manages session lifecycle
    """

    def __init__(self):
        self.panels: Dict[str, BasePanel] = {}
        self.panel_classes: Dict[str, Type[BasePanel]] = {}
        self.health_monitor_thread = None
        self.health_monitoring = False
        self.inter_panel_handlers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()

        # Health monitoring settings
        self.health_check_interval = 30  # seconds
        self.stale_threshold_minutes = 5

    def register_panel_class(self, panel_class: Type[BasePanel]) -> bool:
        """
        Register a panel class for later instantiation

        Args:
            panel_class: Panel class to register

        Returns:
            True if registration successful
        """
        try:
            # Validate panel class
            if not issubclass(panel_class, BasePanel):
                logger.error(
                    f"Panel class {panel_class.__name__} does not inherit from BasePanel"
                )
                return False

            # Get panel info (temporary instance)
            temp_instance = panel_class("temp", "temp")
            panel_id = temp_instance.get_panel_id()

            with self._lock:
                self.panel_classes[panel_id] = panel_class

            logger.info(f"Registered panel class: {panel_id} ({panel_class.__name__})")
            return True

        except Exception as e:
            logger.error(f"Failed to register panel class {panel_class.__name__}: {e}")
            return False

    def instantiate_panel(
        self, panel_id: str, config: Dict = None
    ) -> Optional[BasePanel]:
        """
        Instantiate a registered panel class

        Args:
            panel_id: ID of panel to instantiate
            config: Configuration for the panel

        Returns:
            Panel instance or None if failed
        """
        if panel_id not in self.panel_classes:
            logger.error(f"Panel class not registered: {panel_id}")
            return None

        try:
            panel_class = self.panel_classes[panel_id]
            panel = panel_class(panel_id, panel_class.__name__)

            # Initialize with config
            if config:
                if panel.initialize(config):
                    with self._lock:
                        self.panels[panel_id] = panel
                    logger.info(f"Instantiated panel: {panel_id}")
                    return panel
                else:
                    logger.error(f"Failed to initialize panel: {panel_id}")
                    return None
            else:
                logger.warning(f"No config provided for panel: {panel_id}")
                return None

        except Exception as e:
            logger.error(f"Failed to instantiate panel {panel_id}: {e}")
            return None

    def get_panel(self, panel_id: str) -> Optional[BasePanel]:
        """
        Get a panel instance by ID

        Args:
            panel_id: ID of panel to retrieve

        Returns:
            Panel instance or None if not found
        """
        return self.panels.get(panel_id)

    def get_all_panels(self) -> List[BasePanel]:
        """Get all registered panel instances"""
        return list(self.panels.values())

    def get_active_panels(self) -> List[BasePanel]:
        """Get all active panels"""
        return [p for p in self.panels.values() if p.get_status().status == "active"]

    def get_panels_by_capability(self, capability: str) -> List[BasePanel]:
        """
        Get all panels that support a specific capability

        Args:
            capability: Capability to filter by

        Returns:
            List of panels that support the capability
        """
        return [p for p in self.panels.values() if p.supports_feature(capability)]

    def register_panel(self, panel: BasePanel, config: Dict = None) -> bool:
        """
        Register an existing panel instance

        Args:
            panel: Panel instance to register
            config: Configuration for the panel

        Returns:
            True if registration successful
        """
        try:
            panel_id = panel.get_panel_id()

            # Initialize panel
            if config and not panel.initialize(config):
                logger.error(f"Failed to initialize panel: {panel_id}")
                return False

            with self._lock:
                self.panels[panel_id] = panel

            logger.info(f"Registered panel: {panel_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to register panel {panel.get_panel_id()}: {e}")
            return False

    def unregister_panel(self, panel_id: str) -> bool:
        """
        Unregister and cleanup a panel

        Args:
            panel_id: ID of panel to unregister

        Returns:
            True if unregistration successful
        """
        if panel_id not in self.panels:
            logger.warning(f"Panel not found for unregistration: {panel_id}")
            return False

        try:
            panel = self.panels[panel_id]

            # Cleanup panel
            panel.cleanup()

            # Close all sessions
            for session in panel.get_all_sessions():
                panel.close_session(session.session_id)

            with self._lock:
                del self.panels[panel_id]

            logger.info(f"Unregistered panel: {panel_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to unregister panel {panel_id}: {e}")
            return False

    def start_health_monitoring(self):
        """Start background health monitoring thread"""
        if self.health_monitoring:
            return

        self.health_monitoring = True
        self.health_monitor_thread = threading.Thread(
            target=self._health_monitor_loop, daemon=True
        )
        self.health_monitor_thread.start()
        logger.info("Started panel health monitoring")

    def stop_health_monitoring(self):
        """Stop background health monitoring"""
        self.health_monitoring = False
        if self.health_monitor_thread:
            self.health_monitor_thread.join(timeout=5)
        logger.info("Stopped panel health monitoring")

    def _health_monitor_loop(self):
        """Background health monitoring loop"""
        while self.health_monitoring:
            try:
                self._perform_health_checks()
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                time.sleep(5)  # Brief pause on error

    def _perform_health_checks(self):
        """Perform health checks on all panels"""
        for panel in self.get_all_panels():
            try:
                health_result = panel.health_check()

                # Update panel status based on health check
                if health_result.get("healthy", False):
                    panel.update_status(
                        "active", health_score=health_result.get("score", 1.0)
                    )
                else:
                    panel.update_status(
                        "error",
                        health_score=health_result.get("score", 0.0),
                        error=health_result.get("error", "Health check failed"),
                    )

                # Log health issues
                panel_status = panel.get_status()
                if panel_status.health_score < 0.5:
                    logger.warning(
                        f"Panel {panel.get_panel_id()} has low health score: {panel_status.health_score}"
                    )

            except Exception as e:
                logger.error(
                    f"Health check failed for panel {panel.get_panel_id()}: {e}"
                )
                panel.update_status("error", health_score=0.0, error=str(e))

    def get_system_status(self) -> Dict:
        """Get overall system status"""
        panels = self.get_all_panels()
        active_panels = self.get_active_panels()

        # Calculate overall health
        if panels:
            avg_health = sum(p.get_status().health_score for p in panels) / len(panels)
        else:
            avg_health = 0.0

        return {
            "total_panels": len(panels),
            "active_panels": len(active_panels),
            "health_monitoring": self.health_monitoring,
            "average_health": avg_health,
            "last_check": datetime.now().isoformat(),
        }

    def register_inter_panel_handler(self, event_type: str, handler: Callable):
        """
        Register handler for inter-panel communication

        Args:
            event_type: Type of event to handle
            handler: Function to call when event occurs
        """
        if event_type not in self.inter_panel_handlers:
            self.inter_panel_handlers[event_type] = []

        self.inter_panel_handlers[event_type].append(handler)
        logger.info(f"Registered inter-panel handler for {event_type}")

    def send_inter_panel_event(self, event_type: str, data: Dict, source_panel: str):
        """
        Send event to other panels

        Args:
            event_type: Type of event
            data: Event data
            source_panel: ID of panel sending the event
        """
        if event_type in self.inter_panel_handlers:
            for handler in self.inter_panel_handlers[event_type]:
                try:
                    handler(data, source_panel)
                except Exception as e:
                    logger.error(f"Inter-panel handler failed for {event_type}: {e}")

    # --- Restored from 888 version: Default capabilities per panel type ---
    def _get_default_capabilities(self, panel_name: str) -> PanelCapabilities:
        """Get default capabilities for a panel type."""
        defaults = {
            'orchestr8': PanelCapabilities(
                supports_sessions=True,
                supports_real_time=True,
                supports_collaboration=False
            ),
            'integr8': PanelCapabilities(
                supports_files=True,
                supports_sessions=True,
                supports_real_time=False,
                supports_collaboration=True
            ),
            'communic8': PanelCapabilities(
                supports_sessions=True,
                supports_real_time=True,
                supports_collaboration=True
            ),
            'actu8': PanelCapabilities(
                supports_files=True,
                supports_sessions=True,
                supports_real_time=False
            ),
            'cre8': PanelCapabilities(
                supports_files=True,
                supports_sessions=True,
                supports_real_time=True,
                supports_plugins=True
            ),
            'innov8': PanelCapabilities(
                supports_sessions=True,
                supports_real_time=True,
                supports_plugins=True,
                custom_capabilities={'experimental': True}
            )
        }
        return defaults.get(panel_name, PanelCapabilities())


# Global registry instance
_registry = None


def get_panel_registry() -> PanelRegistry:
    """Get the global panel registry instance"""
    global _registry
    if _registry is None:
        _registry = PanelRegistry()
        _registry.start_health_monitoring()
    return _registry

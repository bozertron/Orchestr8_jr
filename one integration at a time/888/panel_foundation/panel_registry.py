"""
Panel Registry for managing [name]8 panel instances.
"""

from typing import Dict, List, Optional, Any, Type
from .base_panel import BasePanel, PanelCapabilities
import time


class PanelRegistry:
    """
    Registry for managing all [name]8 panel instances.
    
    This provides centralized management of panel lifecycle, discovery,
    and inter-panel communication capabilities.
    """
    
    def __init__(self):
        self._panels: Dict[str, BasePanel] = {}
        self._panel_types: Dict[str, Type[BasePanel]] = {}
        self._registry_created_at = int(time.time() * 1000)
    
    def register_panel_type(self, panel_name: str, panel_class: Type[BasePanel]) -> bool:
        """
        Register a panel type for future instantiation.
        
        Args:
            panel_name: Name of the panel (e.g., 'communic8', 'actu8')
            panel_class: Panel class that extends BasePanel
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not issubclass(panel_class, BasePanel):
                return False
            
            self._panel_types[panel_name] = panel_class
            return True
            
        except Exception:
            return False
    
    def create_panel(self, panel_name: str, capabilities: Optional[PanelCapabilities] = None, 
                    config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create and initialize a panel instance.
        
        Args:
            panel_name: Name of the panel to create
            capabilities: Optional capabilities override
            config: Optional initialization configuration
            
        Returns:
            Dictionary containing creation result
        """
        try:
            if panel_name in self._panels:
                return {
                    'success': False,
                    'error': f'Panel {panel_name} already exists'
                }
            
            if panel_name not in self._panel_types:
                return {
                    'success': False,
                    'error': f'Panel type {panel_name} not registered'
                }
            
            # Create panel instance
            panel_class = self._panel_types[panel_name]
            if capabilities is None:
                capabilities = self._get_default_capabilities(panel_name)
            
            panel = panel_class(panel_name, capabilities)
            
            # Initialize panel
            init_result = panel.initialize(config)
            if not init_result.get('success', False):
                return {
                    'success': False,
                    'error': f'Failed to initialize panel {panel_name}: {init_result.get("error", "Unknown error")}'
                }
            
            # Register panel
            self._panels[panel_name] = panel
            
            return {
                'success': True,
                'panel_name': panel_name,
                'capabilities': panel.get_capabilities(),
                'created_at': int(time.time() * 1000)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_panel(self, panel_name: str) -> Optional[BasePanel]:
        """Get a panel instance by name."""
        return self._panels.get(panel_name)
    
    def list_panels(self) -> Dict[str, Any]:
        """List all active panels."""
        panels_info = []
        
        for name, panel in self._panels.items():
            panels_info.append({
                'name': name,
                'capabilities': panel.get_capabilities(),
                'health': panel.health_check(),
                'sessions': len(panel.sessions)
            })
        
        return {
            'success': True,
            'panels': panels_info,
            'total_panels': len(self._panels),
            'registry_created_at': self._registry_created_at
        }
    
    def remove_panel(self, panel_name: str) -> Dict[str, Any]:
        """Remove a panel from the registry."""
        try:
            if panel_name not in self._panels:
                return {
                    'success': False,
                    'error': f'Panel {panel_name} not found'
                }
            
            panel = self._panels[panel_name]
            
            # Close all sessions
            for session_id in list(panel.sessions.keys()):
                panel.close_session(session_id)
            
            # Remove from registry
            del self._panels[panel_name]
            
            return {
                'success': True,
                'panel_name': panel_name,
                'removed_at': int(time.time() * 1000)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
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
_global_registry: Optional[PanelRegistry] = None


def get_global_registry() -> PanelRegistry:
    """Get the global panel registry instance."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PanelRegistry()
    return _global_registry

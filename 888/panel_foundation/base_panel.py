"""
Base panel architecture for [name]8 applications.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import time


@dataclass
class PanelCapabilities:
    """Defines the capabilities of a panel application."""
    supports_files: bool = False
    supports_sessions: bool = True
    supports_real_time: bool = False
    supports_collaboration: bool = False
    supports_plugins: bool = False
    custom_capabilities: Dict[str, Any] = None


class BasePanel(ABC):
    """
    Base class for all [name]8 panel integrations.
    
    This provides the common interface that all panels must implement,
    ensuring consistency across orchestr8, integr8, communic8, actu8, cre8, innov8.
    """
    
    def __init__(self, panel_name: str, capabilities: PanelCapabilities):
        self.panel_name = panel_name
        self.capabilities = capabilities
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.is_initialized = False
    
    @abstractmethod
    def get_version(self) -> str:
        """Get the panel wrapper version."""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the panel system."""
        pass
    
    @abstractmethod
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize the panel with optional configuration."""
        pass
    
    @abstractmethod
    def create_session(self, session_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new session within the panel."""
        pass
    
    @abstractmethod
    def close_session(self, session_id: str) -> Dict[str, Any]:
        """Close an existing session."""
        pass
    
    @abstractmethod
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about a specific session."""
        pass
    
    @abstractmethod
    def list_sessions(self) -> Dict[str, Any]:
        """List all active sessions."""
        pass
    
    # Optional methods that panels can override if they support the capability
    def open_file(self, session_id: str, file_path: str) -> Dict[str, Any]:
        """Open a file (if panel supports files)."""
        if not self.capabilities.supports_files:
            return {
                'success': False,
                'error': f'{self.panel_name} does not support file operations'
            }
        return {'success': False, 'error': 'Not implemented'}
    
    def save_file(self, session_id: str, file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Save a file (if panel supports files)."""
        if not self.capabilities.supports_files:
            return {
                'success': False,
                'error': f'{self.panel_name} does not support file operations'
            }
        return {'success': False, 'error': 'Not implemented'}
    
    def get_real_time_data(self, session_id: str, data_type: str) -> Dict[str, Any]:
        """Get real-time data (if panel supports real-time)."""
        if not self.capabilities.supports_real_time:
            return {
                'success': False,
                'error': f'{self.panel_name} does not support real-time data'
            }
        return {'success': False, 'error': 'Not implemented'}
    
    # Common utility methods
    def generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"{self.panel_name}_session_{int(time.time() * 1000)}"
    
    def validate_session(self, session_id: str) -> bool:
        """Validate that a session exists."""
        return session_id in self.sessions
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get panel capabilities."""
        return {
            'panel_name': self.panel_name,
            'supports_files': self.capabilities.supports_files,
            'supports_sessions': self.capabilities.supports_sessions,
            'supports_real_time': self.capabilities.supports_real_time,
            'supports_collaboration': self.capabilities.supports_collaboration,
            'supports_plugins': self.capabilities.supports_plugins,
            'custom_capabilities': self.capabilities.custom_capabilities or {}
        }

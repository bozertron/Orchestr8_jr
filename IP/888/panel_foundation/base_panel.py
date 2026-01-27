# IP/888/panel_foundation/base_panel.py
"""
Base Panel - Abstract base class that ALL [name]8 tools must implement
Provides standardized interface and capability flags
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


@dataclass
class PanelCapabilities:
    """Capability flags for panels"""

    supports_files: bool = False
    supports_sessions: bool = True  # Restored from 888 version
    supports_real_time: bool = False
    supports_ai_models: bool = False
    supports_external_apps: bool = False
    supports_multimodal: bool = False
    supports_collaboration: bool = False
    supports_streaming: bool = False
    supports_plugins: bool = False  # Restored from 888 version
    max_file_size_mb: Optional[int] = None
    supported_formats: List[str] = None
    custom_capabilities: Dict[str, Any] = None  # Restored from 888 version - flexible extension

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = []
        if self.custom_capabilities is None:
            self.custom_capabilities = {}


@dataclass
class PanelStatus:
    """Panel status information"""

    panel_id: str
    name: str
    version: str
    status: str  # "active", "inactive", "error", "loading"
    health_score: float  # 0.0 to 1.0
    last_check: str
    error_count: int = 0
    last_error: Optional[str] = None
    session_count: int = 0
    uptime_seconds: int = 0


@dataclass
class PanelSession:
    """Panel session information"""

    session_id: str
    panel_id: str
    created_at: str
    user_context: Dict[str, Any]
    active: bool = True
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class BasePanel(ABC):
    """
    Abstract base class for all [name]8 tools

    All panels must implement this interface to work with Orchestr8's
    plugin system and panel registry.
    """

    def __init__(self, panel_id: str, name: str, version: str = "1.0.0"):
        self.panel_id = panel_id
        self.name = name
        self.version = version
        self.status = PanelStatus(
            panel_id=panel_id,
            name=name,
            version=version,
            status="loading",
            health_score=0.0,
            last_check=datetime.now().isoformat(),
        )
        self.capabilities = self._define_capabilities()
        self.sessions: Dict[str, PanelSession] = {}
        self.config: Dict[str, Any] = {}
        self._initialized = False

    @abstractmethod
    def _define_capabilities(self) -> PanelCapabilities:
        """
        Define what this panel can do

        Returns:
            PanelCapabilities object with supported features
        """
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the panel with configuration

        Args:
            config: Panel configuration from orchestr8_settings.toml

        Returns:
            True if initialization successful
        """
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """
        Clean up resources when panel is shutting down

        Returns:
            True if cleanup successful
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the panel

        Returns:
            Health check results with status, metrics, and any issues
        """
        pass

    @abstractmethod
    def create_session(self, user_context: Dict[str, Any]) -> PanelSession:
        """
        Create a new session for user interaction

        Args:
            user_context: Context information about the user/session

        Returns:
            PanelSession object
        """
        pass

    @abstractmethod
    def render(self, session: PanelSession) -> Any:
        """
        Render the panel UI for the given session

        Args:
            session: Active panel session

        Returns:
            Marimo UI element or HTML string
        """
        pass

    # Optional methods with default implementations

    def get_version(self) -> str:
        """Get panel version"""
        return self.version

    def get_panel_id(self) -> str:
        """Get panel ID"""
        return self.panel_id

    def get_name(self) -> str:
        """Get panel name"""
        return self.name

    def get_capabilities(self) -> PanelCapabilities:
        """Get panel capabilities"""
        return self.capabilities

    def get_status(self) -> PanelStatus:
        """Get current panel status"""
        return self.status

    def update_status(self, status: str, health_score: float = None, error: str = None):
        """Update panel status"""
        self.status.status = status
        self.status.last_check = datetime.now().isoformat()

        if health_score is not None:
            self.status.health_score = health_score

        if error:
            self.status.error_count += 1
            self.status.last_error = error
            self.status.health_score = max(0.0, self.status.health_score - 0.1)

    def get_session(self, session_id: str) -> Optional[PanelSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def get_all_sessions(self) -> List[PanelSession]:
        """Get all active sessions"""
        return [s for s in self.sessions.values() if s.active]

    def close_session(self, session_id: str) -> bool:
        """Close a session"""
        if session_id in self.sessions:
            self.sessions[session_id].active = False
            return True
        return False

    def is_initialized(self) -> bool:
        """Check if panel is initialized"""
        return self._initialized

    def set_initialized(self, initialized: bool):
        """Set initialization status"""
        self._initialized = initialized
        if initialized:
            self.update_status("active", 1.0)
        else:
            self.update_status("inactive", 0.0)

    def supports_feature(self, feature: str) -> bool:
        """
        Check if panel supports a specific feature

        Args:
            feature: Feature name to check

        Returns:
            True if feature is supported
        """
        feature_map = {
            "files": self.capabilities.supports_files,
            "real_time": self.capabilities.supports_real_time,
            "ai_models": self.capabilities.supports_ai_models,
            "external_apps": self.capabilities.supports_external_apps,
            "multimodal": self.capabilities.supports_multimodal,
            "collaboration": self.capabilities.supports_collaboration,
            "streaming": self.capabilities.supports_streaming,
        }
        return feature_map.get(feature, False)

    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return self.capabilities.supported_formats

    def validate_file(self, file_path: str) -> bool:
        """
        Validate if file is supported by this panel

        Args:
            file_path: Path to file to validate

        Returns:
            True if file is supported
        """
        if not self.capabilities.supports_files:
            return False

        if not self.capabilities.supported_formats:
            return True  # No format restrictions

        file_ext = file_path.lower().split(".")[-1]
        return any(
            file_ext in fmt.lower() for fmt in self.capabilities.supported_formats
        )

    # --- Restored from 888 version: Optional file operation methods ---
    def open_file(self, session_id: str, file_path: str) -> Dict[str, Any]:
        """Open a file (if panel supports files)."""
        if not self.capabilities.supports_files:
            return {
                'success': False,
                'error': f'{self.name} does not support file operations'
            }
        return {'success': False, 'error': 'Not implemented'}

    def save_file(self, session_id: str, file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Save a file (if panel supports files)."""
        if not self.capabilities.supports_files:
            return {
                'success': False,
                'error': f'{self.name} does not support file operations'
            }
        return {'success': False, 'error': 'Not implemented'}

    def get_real_time_data(self, session_id: str, data_type: str) -> Dict[str, Any]:
        """Get real-time data (if panel supports real-time)."""
        if not self.capabilities.supports_real_time:
            return {
                'success': False,
                'error': f'{self.name} does not support real-time data'
            }
        return {'success': False, 'error': 'Not implemented'}

    def generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"{self.name}_session_{int(datetime.now().timestamp() * 1000)}"

    def validate_session(self, session_id: str) -> bool:
        """Validate that a session exists."""
        return session_id in self.sessions

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about a specific session."""
        session = self.sessions.get(session_id)
        if not session:
            return {'success': False, 'error': f'Session {session_id} not found'}
        return {
            'success': True,
            'session_id': session.session_id,
            'panel_id': session.panel_id,
            'created_at': session.created_at,
            'active': session.active,
            'metadata': session.metadata
        }

    def list_sessions(self) -> Dict[str, Any]:
        """List all active sessions."""
        return {
            'success': True,
            'sessions': [self.get_session_info(sid) for sid in self.sessions.keys()],
            'total': len(self.sessions)
        }

    def get_capabilities_dict(self) -> Dict[str, Any]:
        """Get panel capabilities as dictionary (for API responses)."""
        return {
            'panel_id': self.panel_id,
            'panel_name': self.name,
            'supports_files': self.capabilities.supports_files,
            'supports_sessions': self.capabilities.supports_sessions,
            'supports_real_time': self.capabilities.supports_real_time,
            'supports_collaboration': self.capabilities.supports_collaboration,
            'supports_plugins': self.capabilities.supports_plugins,
            'supports_ai_models': self.capabilities.supports_ai_models,
            'supports_streaming': self.capabilities.supports_streaming,
            'custom_capabilities': self.capabilities.custom_capabilities or {}
        }

    def __str__(self) -> str:
        return f"{self.name} (v{self.version}) - {self.status.status}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self.panel_id}', name='{self.name}', status='{self.status.status}')>"

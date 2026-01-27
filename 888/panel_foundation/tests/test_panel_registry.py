"""
Tests for panel foundation functionality.
"""

import pytest
import sys
import os

# Import the panel foundation modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from base_panel import BasePanel, PanelCapabilities
from panel_registry import PanelRegistry, get_global_registry


class MockPanel(BasePanel):
    """Mock panel implementation for testing."""
    
    def __init__(self, panel_name: str, capabilities: PanelCapabilities):
        super().__init__(panel_name, capabilities)
        self.initialized = False
    
    def get_version(self) -> str:
        return "1.0.0-test"
    
    def health_check(self) -> dict:
        return {
            'success': True,
            'status': 'healthy',
            'panel_name': self.panel_name,
            'initialized': self.initialized
        }
    
    def initialize(self, config=None) -> dict:
        self.initialized = True
        self.is_initialized = True
        return {
            'success': True,
            'initialized_at': 1234567890,
            'config': config
        }
    
    def create_session(self, session_config=None) -> dict:
        if not self.is_initialized:
            return {'success': False, 'error': 'Panel not initialized'}
        
        session_id = self.generate_session_id()
        self.sessions[session_id] = {
            'created_at': 1234567890,
            'config': session_config
        }
        
        return {
            'success': True,
            'session_id': session_id,
            'created_at': 1234567890
        }
    
    def close_session(self, session_id: str) -> dict:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {'success': True, 'session_id': session_id}
        else:
            return {'success': False, 'error': f'Session {session_id} not found'}
    
    def get_session_info(self, session_id: str) -> dict:
        if session_id in self.sessions:
            return {
                'success': True,
                'session_id': session_id,
                'info': self.sessions[session_id]
            }
        else:
            return {'success': False, 'error': f'Session {session_id} not found'}
    
    def list_sessions(self) -> dict:
        return {
            'success': True,
            'sessions': list(self.sessions.keys()),
            'count': len(self.sessions)
        }


class TestPanelCapabilities:
    """Test suite for PanelCapabilities."""
    
    def test_default_capabilities(self):
        """Test default capabilities."""
        caps = PanelCapabilities()
        
        assert caps.supports_files is False
        assert caps.supports_sessions is True
        assert caps.supports_real_time is False
        assert caps.supports_collaboration is False
        assert caps.supports_plugins is False
        assert caps.custom_capabilities is None
    
    def test_custom_capabilities(self):
        """Test custom capabilities."""
        custom_caps = {'feature_x': True, 'feature_y': 'enabled'}
        caps = PanelCapabilities(
            supports_files=True,
            supports_real_time=True,
            custom_capabilities=custom_caps
        )
        
        assert caps.supports_files is True
        assert caps.supports_real_time is True
        assert caps.custom_capabilities == custom_caps


class TestBasePanel:
    """Test suite for BasePanel."""
    
    def test_panel_creation(self):
        """Test panel creation."""
        capabilities = PanelCapabilities(supports_files=True)
        panel = MockPanel("test_panel", capabilities)
        
        assert panel.panel_name == "test_panel"
        assert panel.capabilities.supports_files is True
        assert panel.is_initialized is False
        assert len(panel.sessions) == 0
    
    def test_panel_initialization(self):
        """Test panel initialization."""
        panel = MockPanel("test_panel", PanelCapabilities())
        
        config = {'setting1': 'value1'}
        result = panel.initialize(config)
        
        assert result['success'] is True
        assert result['config'] == config
        assert panel.is_initialized is True
    
    def test_session_management(self):
        """Test session creation and management."""
        panel = MockPanel("test_panel", PanelCapabilities())
        panel.initialize()
        
        # Create session
        result = panel.create_session({'test': 'config'})
        assert result['success'] is True
        session_id = result['session_id']
        assert session_id.startswith('test_panel_session_')
        
        # Get session info
        info_result = panel.get_session_info(session_id)
        assert info_result['success'] is True
        assert info_result['info']['config'] == {'test': 'config'}
        
        # List sessions
        list_result = panel.list_sessions()
        assert list_result['success'] is True
        assert session_id in list_result['sessions']
        assert list_result['count'] == 1
        
        # Close session
        close_result = panel.close_session(session_id)
        assert close_result['success'] is True
        
        # Verify session is closed
        list_result = panel.list_sessions()
        assert list_result['count'] == 0
    
    def test_session_operations_without_initialization(self):
        """Test session operations fail without initialization."""
        panel = MockPanel("test_panel", PanelCapabilities())
        
        result = panel.create_session()
        assert result['success'] is False
        assert 'not initialized' in result['error']
    
    def test_file_operations_not_supported(self):
        """Test file operations when not supported."""
        capabilities = PanelCapabilities(supports_files=False)
        panel = MockPanel("test_panel", capabilities)
        
        result = panel.open_file("session_id", "/path/to/file")
        assert result['success'] is False
        assert 'does not support file operations' in result['error']
        
        result = panel.save_file("session_id", "/path/to/file")
        assert result['success'] is False
        assert 'does not support file operations' in result['error']
    
    def test_real_time_operations_not_supported(self):
        """Test real-time operations when not supported."""
        capabilities = PanelCapabilities(supports_real_time=False)
        panel = MockPanel("test_panel", capabilities)
        
        result = panel.get_real_time_data("session_id", "data_type")
        assert result['success'] is False
        assert 'does not support real-time data' in result['error']
    
    def test_get_capabilities(self):
        """Test getting panel capabilities."""
        custom_caps = {'experimental': True}
        capabilities = PanelCapabilities(
            supports_files=True,
            supports_real_time=True,
            supports_collaboration=True,
            custom_capabilities=custom_caps
        )
        panel = MockPanel("test_panel", capabilities)
        
        caps = panel.get_capabilities()
        
        assert caps['panel_name'] == "test_panel"
        assert caps['supports_files'] is True
        assert caps['supports_sessions'] is True
        assert caps['supports_real_time'] is True
        assert caps['supports_collaboration'] is True
        assert caps['supports_plugins'] is False
        assert caps['custom_capabilities'] == custom_caps
    
    def test_validate_session(self):
        """Test session validation."""
        panel = MockPanel("test_panel", PanelCapabilities())
        panel.initialize()
        
        # Create a session
        result = panel.create_session()
        session_id = result['session_id']
        
        # Validate existing session
        assert panel.validate_session(session_id) is True
        
        # Validate non-existent session
        assert panel.validate_session("nonexistent") is False


class TestPanelRegistry:
    """Test suite for PanelRegistry."""
    
    def test_registry_creation(self):
        """Test registry creation."""
        registry = PanelRegistry()
        
        assert len(registry._panels) == 0
        assert len(registry._panel_types) == 0
        assert registry._registry_created_at > 0
    
    def test_register_panel_type(self):
        """Test panel type registration."""
        registry = PanelRegistry()
        
        # Register valid panel type
        result = registry.register_panel_type("test_panel", MockPanel)
        assert result is True
        assert "test_panel" in registry._panel_types
        
        # Try to register invalid type
        result = registry.register_panel_type("invalid", str)
        assert result is False
    
    def test_create_panel(self):
        """Test panel creation."""
        registry = PanelRegistry()
        registry.register_panel_type("test_panel", MockPanel)
        
        result = registry.create_panel("test_panel")
        
        assert result['success'] is True
        assert result['panel_name'] == "test_panel"
        assert 'capabilities' in result
        assert 'created_at' in result
        
        # Verify panel is in registry
        panel = registry.get_panel("test_panel")
        assert panel is not None
        assert isinstance(panel, MockPanel)
    
    def test_create_panel_already_exists(self):
        """Test creating panel that already exists."""
        registry = PanelRegistry()
        registry.register_panel_type("test_panel", MockPanel)
        
        # Create first panel
        result1 = registry.create_panel("test_panel")
        assert result1['success'] is True
        
        # Try to create again
        result2 = registry.create_panel("test_panel")
        assert result2['success'] is False
        assert 'already exists' in result2['error']
    
    def test_create_panel_unregistered_type(self):
        """Test creating panel with unregistered type."""
        registry = PanelRegistry()
        
        result = registry.create_panel("unregistered_panel")
        assert result['success'] is False
        assert 'not registered' in result['error']
    
    def test_list_panels(self):
        """Test listing panels."""
        registry = PanelRegistry()
        registry.register_panel_type("panel1", MockPanel)
        registry.register_panel_type("panel2", MockPanel)
        
        # Initially no panels
        result = registry.list_panels()
        assert result['success'] is True
        assert result['total_panels'] == 0
        assert len(result['panels']) == 0
        
        # Create some panels
        registry.create_panel("panel1")
        registry.create_panel("panel2")
        
        result = registry.list_panels()
        assert result['success'] is True
        assert result['total_panels'] == 2
        assert len(result['panels']) == 2
        
        panel_names = [p['name'] for p in result['panels']]
        assert 'panel1' in panel_names
        assert 'panel2' in panel_names
    
    def test_remove_panel(self):
        """Test panel removal."""
        registry = PanelRegistry()
        registry.register_panel_type("test_panel", MockPanel)
        
        # Create panel
        registry.create_panel("test_panel")
        assert registry.get_panel("test_panel") is not None
        
        # Remove panel
        result = registry.remove_panel("test_panel")
        assert result['success'] is True
        assert result['panel_name'] == "test_panel"
        
        # Verify panel is removed
        assert registry.get_panel("test_panel") is None
        
        list_result = registry.list_panels()
        assert list_result['total_panels'] == 0
    
    def test_remove_nonexistent_panel(self):
        """Test removing non-existent panel."""
        registry = PanelRegistry()
        
        result = registry.remove_panel("nonexistent")
        assert result['success'] is False
        assert 'not found' in result['error']
    
    def test_default_capabilities(self):
        """Test default capabilities for known panel types."""
        registry = PanelRegistry()
        
        # Test orchestr8 defaults
        caps = registry._get_default_capabilities("orchestr8")
        assert caps.supports_sessions is True
        assert caps.supports_real_time is True
        assert caps.supports_collaboration is False
        
        # Test integr8 defaults
        caps = registry._get_default_capabilities("integr8")
        assert caps.supports_files is True
        assert caps.supports_sessions is True
        assert caps.supports_collaboration is True
        
        # Test unknown panel defaults
        caps = registry._get_default_capabilities("unknown")
        assert caps.supports_files is False
        assert caps.supports_sessions is True


class TestGlobalRegistry:
    """Test suite for global registry."""
    
    def test_global_registry_singleton(self):
        """Test global registry is singleton."""
        registry1 = get_global_registry()
        registry2 = get_global_registry()
        
        assert registry1 is registry2
        assert isinstance(registry1, PanelRegistry)


if __name__ == '__main__':
    pytest.main([__file__])

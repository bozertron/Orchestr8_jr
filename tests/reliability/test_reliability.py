import pytest
import logging
from unittest.mock import MagicMock
from orchestr8_next.shell.store import Store
from orchestr8_next.shell.contracts import State, ActionType
from orchestr8_next.shell.reducer import root_reducer
from orchestr8_next.shell.actions import UIAction
from orchestr8_next.city.bridge import CityBridge
from orchestr8_next.city.contracts import NodeClickedEvent

def test_system_startup_reliability():
    """Verify clean initialization of core state components."""
    try:
        # State.initial() factory method
        initial_state = State.initial()
        store = Store(root_reducer, initial_state)
        # Use get_state()
        state = store.get_state()
        assert state is not None
        assert isinstance(state, State)
        # Check initial state properties
        assert state.shell.current_view == "matrix"
    except Exception as e:
        pytest.fail(f"System startup failed: {e}")

def test_core_control_integrity():
    """Verify basic action dispatch doesn't destabilize the store."""
    store = Store(root_reducer, State.initial())
    
    # Valid Action
    action = UIAction(type=ActionType.NAVIGATE_APPS, payload="apps")
    
    # Dispatch
    try:
        store.dispatch(action)
        # Verify state is consistent
        assert isinstance(store.get_state(), State)
    except Exception as e:
        pytest.fail(f"Action dispatch caused crash: {e}")

def test_adapter_failure_isolation_bridge():
    """Verify CityBridge isolates handler failures."""
    bridge = CityBridge()
    
    # Mock Handler that raises exception
    handler = MagicMock(side_effect=Exception("Simulated Crash"))
    
    # Register for specific event type
    event_type = "node_clicked"
    bridge.register_handler(event_type, handler) # Note: contract uses "register_handler(event_type, callback)"
    
    # Create valid event instance
    event = NodeClickedEvent(node_id="n1", timestamp=12345.0)
    
    # Execution should not raise exception to caller because _dispatch catches it
    try:
        # Access protected method for testing harness checks
        bridge._dispatch(event) 
    except Exception:
        pytest.fail("Bridge did not isolate handler failure")
        
    # Verify handler was called
    handler.assert_called_once()

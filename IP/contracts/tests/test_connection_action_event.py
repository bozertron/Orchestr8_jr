"""Unit tests for connection_action_event.py schema module."""

import pytest

from IP.contracts.connection_action_event import (
    ConnectionActionEvent,
    validate_connection_action_event,
    EXAMPLE_CONNECTION_ACTION,
)


def test_valid_connection_action_event():
    """Full example payload should validate and parse."""
    event = validate_connection_action_event(EXAMPLE_CONNECTION_ACTION)

    assert isinstance(event, ConnectionActionEvent)
    assert event.action == "dry_run_rewire"
    assert event.connection.source == "IP/plugins/06_maestro.py"
    assert event.connection.target == "IP/woven_maps.py"
    assert event.connection.lineNumber == 98
    assert event.proposedTarget == "IP/woven_maps_gpu.py"
    assert event.actorRole == "operator"
    assert len(event.signalNodes) == 2


def test_minimal_connection_action_event():
    """Minimal payload with only required fields should validate."""
    payload = {
        "action": "dry_run_rewire",
        "connection": {"source": "a.py", "target": "b.py"},
    }

    event = validate_connection_action_event(payload)
    assert event.action == "dry_run_rewire"
    assert event.connection.source == "a.py"
    assert event.connection.target == "b.py"
    assert event.connection.resolved is True
    assert event.connection.lineNumber == 0
    assert event.proposedTarget is None


def test_apply_action_is_valid():
    """apply_rewire should validate as a supported action."""
    payload = {
        "action": "apply_rewire",
        "connection": {"source": "a.py", "target": "b.py"},
        "proposedTarget": "c.py",
        "actorRole": "Founder ",
    }
    event = validate_connection_action_event(payload)
    assert event.action == "apply_rewire"
    assert event.proposedTarget == "c.py"
    assert event.actorRole == "founder"


def test_missing_action():
    payload = {"connection": {"source": "a.py", "target": "b.py"}}
    with pytest.raises(ValueError, match="Missing required field: action"):
        validate_connection_action_event(payload)


def test_invalid_action():
    payload = {
        "action": "unknown_action",
        "connection": {"source": "a.py", "target": "b.py"},
    }
    with pytest.raises(ValueError, match="Invalid action: unknown_action"):
        validate_connection_action_event(payload)


def test_missing_connection():
    payload = {"action": "dry_run_rewire"}
    with pytest.raises(ValueError, match="Missing required field: connection"):
        validate_connection_action_event(payload)


def test_missing_connection_source():
    payload = {
        "action": "dry_run_rewire",
        "connection": {"target": "b.py"},
    }
    with pytest.raises(ValueError, match="Missing required field: connection.source"):
        validate_connection_action_event(payload)


def test_missing_connection_target():
    payload = {
        "action": "dry_run_rewire",
        "connection": {"source": "a.py"},
    }
    with pytest.raises(ValueError, match="Missing required field: connection.target"):
        validate_connection_action_event(payload)


def test_to_dict_roundtrip():
    """Event should serialize back to dictionary cleanly."""
    event = validate_connection_action_event(EXAMPLE_CONNECTION_ACTION)
    payload = event.to_dict()

    assert payload["action"] == "dry_run_rewire"
    assert payload["connection"]["source"] == "IP/plugins/06_maestro.py"
    assert payload["connection"]["target"] == "IP/woven_maps.py"
    assert payload["proposedTarget"] == "IP/woven_maps_gpu.py"

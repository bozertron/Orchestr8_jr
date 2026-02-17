"""Unit tests for code_city_node_event.py schema module."""

import pytest
from IP.contracts.code_city_node_event import (
    CodeCityNodeEvent,
    validate_code_city_node_event,
    EXAMPLE_NODE_EVENT,
)


def test_valid_full_payload():
    """Test that EXAMPLE_NODE_EVENT validates correctly with all fields."""
    event = validate_code_city_node_event(EXAMPLE_NODE_EVENT)

    assert event.path == "IP/woven_maps.py"
    assert event.status == "broken"
    assert event.loc == 2847
    assert event.errors == ["TypeError on line 42"]
    assert event.nodeType == "file"
    assert event.centrality == 0.85
    assert event.inCycle is False
    assert event.incomingCount == 12
    assert event.outgoingCount == 8


def test_valid_minimal_payload():
    """Test validation with only required fields."""
    minimal = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
    }
    event = validate_code_city_node_event(minimal)

    assert event.path == "test.py"
    assert event.status == "working"
    assert event.loc == 100
    assert event.errors == []
    assert event.nodeType is None
    assert event.centrality is None
    assert event.inCycle is None
    assert event.incomingCount is None
    assert event.outgoingCount is None


def test_missing_path():
    """Test that missing path raises ValueError."""
    payload = {"status": "working", "loc": 100}

    with pytest.raises(ValueError, match="Missing required field: path"):
        validate_code_city_node_event(payload)


def test_missing_status():
    """Test that missing status raises ValueError."""
    payload = {"path": "test.py", "loc": 100}

    with pytest.raises(ValueError, match="Missing required field: status"):
        validate_code_city_node_event(payload)


def test_missing_loc():
    """Test that missing loc raises ValueError."""
    payload = {"path": "test.py", "status": "working"}

    with pytest.raises(ValueError, match="Missing required field: loc"):
        validate_code_city_node_event(payload)


def test_invalid_status():
    """Test that invalid status raises ValueError."""
    payload = {"path": "test.py", "status": "invalid", "loc": 100}

    with pytest.raises(ValueError, match="Invalid status: invalid"):
        validate_code_city_node_event(payload)


def test_loc_coercion():
    """Test that string loc values are coerced to int."""
    payload = {"path": "test.py", "status": "working", "loc": "100"}
    event = validate_code_city_node_event(payload)

    assert event.loc == 100
    assert isinstance(event.loc, int)


def test_to_dict_roundtrip():
    """Test that to_dict() produces valid dictionary representation."""
    event = validate_code_city_node_event(EXAMPLE_NODE_EVENT)
    event_dict = event.to_dict()

    assert isinstance(event_dict, dict)
    assert event_dict["path"] == "IP/woven_maps.py"
    assert event_dict["status"] == "broken"
    assert event_dict["loc"] == 2847
    assert event_dict["errors"] == ["TypeError on line 42"]

    # Verify roundtrip
    event2 = validate_code_city_node_event(event_dict)
    assert event2.path == event.path
    assert event2.status == event.status
    assert event2.loc == event.loc


def test_optional_fields_default_none():
    """Test that optional fields default to None or empty list as appropriate."""
    minimal = {"path": "test.py", "status": "combat", "loc": 50}
    event = validate_code_city_node_event(minimal)

    # errors should be empty list (not None)
    assert event.errors == []

    # Optional fields should be None
    assert event.nodeType is None
    assert event.centrality is None
    assert event.inCycle is None
    assert event.incomingCount is None
    assert event.outgoingCount is None


def test_errors_list_preservation():
    """Test that errors list is properly handled."""
    payload = {
        "path": "test.py",
        "status": "broken",
        "loc": 100,
        "errors": ["Error 1", "Error 2"],
    }
    event = validate_code_city_node_event(payload)

    assert event.errors == ["Error 1", "Error 2"]
    assert len(event.errors) == 2


def test_errors_none_becomes_empty_list():
    """Test that None errors becomes empty list."""
    payload = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
        "errors": None,
    }
    event = validate_code_city_node_event(payload)

    assert event.errors == []


def test_all_valid_statuses():
    """Test that all three valid status values work."""
    for status in ["working", "broken", "combat"]:
        payload = {"path": "test.py", "status": status, "loc": 100}
        event = validate_code_city_node_event(payload)
        assert event.status == status

"""Unit tests for building_panel.py schema module."""

import pytest
from IP.contracts.building_panel import (
    BuildingPanel,
    BuildingRoom,
    validate_building_panel,
    EXAMPLE_BUILDING_PANEL,
)


def test_valid_full_payload():
    """Test that EXAMPLE_BUILDING_PANEL validates correctly with all fields."""
    panel = validate_building_panel(EXAMPLE_BUILDING_PANEL)

    assert panel.path == "IP/woven_maps.py"
    assert panel.status == "working"
    assert panel.loc == 2940
    assert panel.export_count == 8
    assert panel.building_height == 9.4
    assert panel.footprint == 25.52
    assert panel.imports == [
        "IP/contracts/status_merge_policy.py",
        "IP/connection_verifier.py",
    ]
    assert panel.exports == ["create_code_city", "build_graph_data", "CodeNode", "EdgeData"]
    assert len(panel.rooms) == 2
    assert panel.rooms[0].name == "create_code_city"
    assert panel.rooms[0].line_start == 2922
    assert panel.rooms[0].line_end == 2940
    assert panel.rooms[0].room_type == "function"
    assert panel.connections_in == ["IP/plugins/06_maestro.py", "orchestr8.py"]
    assert panel.connections_out == ["IP/contracts/status_merge_policy.py"]
    assert panel.locked is False
    assert panel.lock_state is None
    assert panel.centrality == 0.85
    assert panel.in_cycle is False
    assert panel.health_errors == []


def test_valid_minimal_payload():
    """Test validation with only required fields."""
    minimal = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
    }
    panel = validate_building_panel(minimal)

    assert panel.path == "test.py"
    assert panel.status == "working"
    assert panel.loc == 100
    assert panel.export_count == 0
    assert panel.building_height == 3.0
    assert panel.footprint == 2.0
    assert panel.imports == []
    assert panel.exports == []
    assert panel.rooms == []
    assert panel.connections_in == []
    assert panel.connections_out == []
    assert panel.lock_state is None
    assert panel.locked is False
    assert panel.centrality == 0.0
    assert panel.in_cycle is False
    assert panel.health_errors == []


def test_missing_path():
    """Test that missing path raises ValueError."""
    payload = {"status": "working", "loc": 100}

    with pytest.raises(ValueError, match="Missing required field: path"):
        validate_building_panel(payload)


def test_missing_status():
    """Test that missing status raises ValueError."""
    payload = {"path": "test.py", "loc": 100}

    with pytest.raises(ValueError, match="Missing required field: status"):
        validate_building_panel(payload)


def test_missing_loc():
    """Test that missing loc raises ValueError."""
    payload = {"path": "test.py", "status": "working"}

    with pytest.raises(ValueError, match="Missing required field: loc"):
        validate_building_panel(payload)


def test_invalid_status():
    """Test that invalid status raises ValueError."""
    payload = {"path": "test.py", "status": "invalid", "loc": 100}

    with pytest.raises(ValueError, match="Invalid status: invalid"):
        validate_building_panel(payload)


def test_rooms_parsing():
    """Test that rooms are properly parsed from dict payloads."""
    payload = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
        "rooms": [
            {
                "name": "test_func",
                "line_start": 10,
                "line_end": 20,
                "room_type": "function",
                "status": "working",
                "errors": [],
            },
            {
                "name": "TestClass",
                "line_start": 30,
                "line_end": 50,
                "room_type": "class",
                "status": "broken",
                "errors": ["SyntaxError"],
            },
        ],
    }
    panel = validate_building_panel(payload)

    assert len(panel.rooms) == 2
    assert isinstance(panel.rooms[0], BuildingRoom)
    assert panel.rooms[0].name == "test_func"
    assert panel.rooms[0].room_type == "function"
    assert panel.rooms[0].status == "working"
    assert panel.rooms[0].errors == []

    assert isinstance(panel.rooms[1], BuildingRoom)
    assert panel.rooms[1].name == "TestClass"
    assert panel.rooms[1].room_type == "class"
    assert panel.rooms[1].status == "broken"
    assert panel.rooms[1].errors == ["SyntaxError"]


def test_to_dict_roundtrip():
    """Test that to_dict() produces valid dictionary representation."""
    panel = validate_building_panel(EXAMPLE_BUILDING_PANEL)
    panel_dict = panel.to_dict()

    assert isinstance(panel_dict, dict)
    assert panel_dict["path"] == "IP/woven_maps.py"
    assert panel_dict["status"] == "working"
    assert panel_dict["loc"] == 2940
    assert panel_dict["export_count"] == 8

    # Verify rooms are dicts
    assert isinstance(panel_dict["rooms"], list)
    assert len(panel_dict["rooms"]) == 2
    assert isinstance(panel_dict["rooms"][0], dict)
    assert panel_dict["rooms"][0]["name"] == "create_code_city"

    # Verify roundtrip
    panel2 = validate_building_panel(panel_dict)
    assert panel2.path == panel.path
    assert panel2.status == panel.status
    assert panel2.loc == panel.loc
    assert len(panel2.rooms) == len(panel.rooms)
    assert panel2.rooms[0].name == panel.rooms[0].name


def test_example_validates():
    """Test that EXAMPLE_BUILDING_PANEL is valid."""
    panel = validate_building_panel(EXAMPLE_BUILDING_PANEL)

    assert panel is not None
    assert isinstance(panel, BuildingPanel)
    assert panel.path == "IP/woven_maps.py"
    assert len(panel.rooms) == 2


def test_all_valid_statuses():
    """Test that all three valid status values work."""
    for status in ["working", "broken", "combat"]:
        payload = {"path": "test.py", "status": status, "loc": 100}
        panel = validate_building_panel(payload)
        assert panel.status == status


def test_locked_building():
    """Test that locked state and lock_state are properly handled."""
    payload = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
        "locked": True,
        "lock_state": "Protected by Louis: Core module",
    }
    panel = validate_building_panel(payload)

    assert panel.locked is True
    assert panel.lock_state == "Protected by Louis: Core module"


def test_building_room_to_dict():
    """Test BuildingRoom to_dict method."""
    room = BuildingRoom(
        name="test_func",
        line_start=10,
        line_end=20,
        room_type="function",
        status="working",
        errors=["Error 1"],
    )
    room_dict = room.to_dict()

    assert isinstance(room_dict, dict)
    assert room_dict["name"] == "test_func"
    assert room_dict["line_start"] == 10
    assert room_dict["line_end"] == 20
    assert room_dict["room_type"] == "function"
    assert room_dict["status"] == "working"
    assert room_dict["errors"] == ["Error 1"]


def test_numeric_coercion():
    """Test that numeric fields are properly coerced."""
    payload = {
        "path": "test.py",
        "status": "working",
        "loc": "100",
        "export_count": "5",
        "building_height": "10.5",
        "footprint": "20.3",
        "centrality": "0.75",
    }
    panel = validate_building_panel(payload)

    assert panel.loc == 100
    assert isinstance(panel.loc, int)
    assert panel.export_count == 5
    assert isinstance(panel.export_count, int)
    assert panel.building_height == 10.5
    assert isinstance(panel.building_height, float)
    assert panel.footprint == 20.3
    assert isinstance(panel.footprint, float)
    assert panel.centrality == 0.75
    assert isinstance(panel.centrality, float)


def test_health_errors_preservation():
    """Test that health_errors list is properly handled."""
    payload = {
        "path": "test.py",
        "status": "broken",
        "loc": 100,
        "health_errors": ["Import cycle detected", "Missing dependency"],
    }
    panel = validate_building_panel(payload)

    assert panel.health_errors == ["Import cycle detected", "Missing dependency"]
    assert len(panel.health_errors) == 2


def test_connections_lists():
    """Test that connections_in and connections_out are properly handled."""
    payload = {
        "path": "test.py",
        "status": "working",
        "loc": 100,
        "connections_in": ["module_a.py", "module_b.py"],
        "connections_out": ["module_c.py"],
    }
    panel = validate_building_panel(payload)

    assert panel.connections_in == ["module_a.py", "module_b.py"]
    assert panel.connections_out == ["module_c.py"]


def test_room_with_combat_status():
    """Test room with combat status."""
    payload = {
        "path": "test.py",
        "status": "combat",
        "loc": 100,
        "rooms": [
            {
                "name": "broken_func",
                "line_start": 10,
                "line_end": 20,
                "room_type": "method",
                "status": "combat",
                "errors": ["Active refactoring", "Agent deployed"],
            }
        ],
    }
    panel = validate_building_panel(payload)

    assert panel.rooms[0].status == "combat"
    assert len(panel.rooms[0].errors) == 2

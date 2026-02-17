"""Tests for Code City context assembly helpers."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from IP.features.maestro.code_city_context import (
    build_building_panel_for_node,
    build_code_city_context_payload,
    derive_context_scope,
    select_room_entry,
)


def test_derive_context_scope_for_file_and_dir() -> None:
    assert derive_context_scope("IP/plugins/06_maestro.py") == "IP/plugins"
    assert derive_context_scope("orchestr8.py") == "orchestr8.py"
    assert derive_context_scope("") == "IP"


def test_build_building_panel_marks_broken_room(tmp_path: Path) -> None:
    project_root = tmp_path
    file_path = project_root / "IP" / "sample.py"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "def alpha():\n"
        "    return 1\n\n"
        "def beta():\n"
        "    return 2\n",
        encoding="utf-8",
    )

    context = SimpleNamespace(
        health={
            "errors": [{"file": "IP/sample.py", "line": 4, "message": "Boom"}],
            "warnings": [],
        },
        connections={
            "imports_from": ["IP/common.py"],
            "broken": [{"import": "missing.module", "line": 1}],
        },
        locks=[],
    )

    panel = build_building_panel_for_node(
        {
            "path": "IP/sample.py",
            "status": "broken",
            "loc": 5,
            "exportCount": 2,
            "buildingHeight": 4.6,
            "footprint": 2.8,
            "centrality": 0.3,
            "inCycle": False,
            "errors": ["IP/sample.py:4 - Boom"],
        },
        project_root=project_root,
        context=context,
    )

    assert panel.path == "IP/sample.py"
    assert panel.status == "broken"
    assert len(panel.rooms) == 2
    assert panel.rooms[1].name == "beta"
    assert panel.rooms[1].status == "broken"
    assert "missing.module" in panel.imports
    assert panel.health_errors


def test_select_room_entry_prefers_broken_room(tmp_path: Path) -> None:
    project_root = tmp_path
    file_path = project_root / "IP" / "roomed.py"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "def ok_room():\n"
        "    return 1\n\n"
        "def bad_room():\n"
        "    return nope\n",
        encoding="utf-8",
    )

    context = SimpleNamespace(
        health={"errors": [{"file": "IP/roomed.py", "line": 4, "message": "NameError"}]},
        connections={},
        locks=[],
    )

    panel = build_building_panel_for_node(
        {
            "path": "IP/roomed.py",
            "status": "broken",
            "loc": 5,
            "errors": ["IP/roomed.py:4 - NameError"],
        },
        project_root=project_root,
        context=context,
    )
    room = select_room_entry(panel)

    assert room is not None
    assert room["trigger"] == "broken_room_click"
    assert room["name"] == "bad_room"


def test_build_code_city_context_payload_includes_sitting_room(tmp_path: Path) -> None:
    project_root = tmp_path
    file_path = project_root / "IP" / "sitting.py"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "def target_room():\n"
        "    return missing_name\n",
        encoding="utf-8",
    )

    context = SimpleNamespace(
        health={"errors": [{"file": "IP/sitting.py", "line": 2, "message": "NameError"}]},
        connections={},
        locks=[{"file": "IP/sitting.py", "reason": "Protected by Louis"}],
    )

    payload = build_code_city_context_payload(
        {
            "path": "IP/sitting.py",
            "status": "broken",
            "loc": 2,
            "errors": ["IP/sitting.py:2 - NameError"],
        },
        project_root=project_root,
        context=context,
    )

    assert payload["context_scope"] == "IP"
    assert payload["sitting_room"] is not None
    assert payload["sitting_room"]["mode"] == "sitting_room"
    assert payload["building_panel"]["locked"] is True

"""Code City node-click context assembly for Maestro handoff flows."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from IP.contracts.building_panel import BuildingPanel, BuildingRoom, validate_building_panel

_ERROR_LINE_PATTERNS = (
    re.compile(r":(?P<line>\d+)\b"),
    re.compile(r"\bline\s+(?P<line>\d+)\b", re.IGNORECASE),
)


def derive_context_scope(file_path: str) -> str:
    """Return a stable scope key for context lookup from a file path."""
    raw_path = (file_path or "").strip()
    if raw_path in {"", "."}:
        return "IP"
    p = Path(raw_path)
    if str(p.parent) in {"", "."}:
        return str(p)
    return str(p.parent)


def _coerce_error_messages(errors: Iterable[Any]) -> List[str]:
    msgs: List[str] = []
    for err in errors or []:
        if isinstance(err, dict):
            file_name = err.get("file", "")
            line_no = err.get("line", "")
            message = err.get("message", "")
            prefix = f"{file_name}:{line_no} - " if file_name or line_no else ""
            msgs.append(f"{prefix}{message}".strip())
        else:
            msgs.append(str(err))
    return [m for m in msgs if m]


def _extract_error_line_map(messages: Iterable[str]) -> Dict[int, List[str]]:
    line_map: Dict[int, List[str]] = {}
    for message in messages:
        for pattern in _ERROR_LINE_PATTERNS:
            match = pattern.search(message)
            if not match:
                continue
            line_no = int(match.group("line"))
            line_map.setdefault(line_no, []).append(message)
            break
    return line_map


def _extract_python_rooms(abs_path: Path) -> Tuple[List[BuildingRoom], List[str]]:
    try:
        source = abs_path.read_text(encoding="utf-8")
    except OSError:
        return [], []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [], []

    rooms: List[BuildingRoom] = []
    exports: List[str] = []

    def add_room(
        name: str,
        node: ast.AST,
        room_type: str,
    ) -> None:
        line_start = int(getattr(node, "lineno", 0) or 0)
        line_end = int(getattr(node, "end_lineno", line_start) or line_start)
        rooms.append(
            BuildingRoom(
                name=name,
                line_start=max(1, line_start),
                line_end=max(1, line_end),
                room_type=room_type,  # type: ignore[arg-type]
                status="working",
                errors=[],
            )
        )

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            exports.append(node.name)
            add_room(node.name, node, "function")
        elif isinstance(node, ast.ClassDef):
            exports.append(node.name)
            add_room(node.name, node, "class")
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add_room(f"{node.name}.{child.name}", child, "method")

    return rooms, exports


def _extract_generic_rooms(abs_path: Path) -> Tuple[List[BuildingRoom], List[str]]:
    """Best-effort room extraction for non-Python files."""
    try:
        lines = abs_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return [], []

    rooms: List[BuildingRoom] = []
    exports: List[str] = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("function "):
            name = stripped.split("function ", 1)[1].split("(", 1)[0].strip()
            if name:
                rooms.append(
                    BuildingRoom(
                        name=name,
                        line_start=idx,
                        line_end=idx,
                        room_type="function",
                    )
                )
                exports.append(name)
        elif stripped.startswith("class "):
            name = stripped.split("class ", 1)[1].split("{", 1)[0].split(" ", 1)[0].strip()
            if name:
                rooms.append(
                    BuildingRoom(
                        name=name,
                        line_start=idx,
                        line_end=idx,
                        room_type="class",
                    )
                )
                exports.append(name)

    return rooms, exports


def _mark_room_statuses(
    rooms: List[BuildingRoom],
    line_map: Dict[int, List[str]],
    node_status: str,
) -> None:
    if not rooms:
        return

    for room in rooms:
        matched_errors: List[str] = []
        for line_no, messages in line_map.items():
            if room.line_start <= line_no <= room.line_end:
                matched_errors.extend(messages)
        if matched_errors:
            room.status = "broken"
            room.errors = matched_errors

    if node_status == "combat" and all(room.status == "working" for room in rooms):
        rooms[0].status = "combat"


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def build_building_panel_for_node(
    node_data: Dict[str, Any],
    *,
    project_root: Path,
    context: Optional[Any],
) -> BuildingPanel:
    """Create validated BuildingPanel payload from node click + context signals."""
    file_path = str(node_data.get("path", ""))
    abs_path = (project_root / file_path).resolve()

    if abs_path.suffix == ".py":
        rooms, exports = _extract_python_rooms(abs_path)
    else:
        rooms, exports = _extract_generic_rooms(abs_path)

    health = _safe_dict(getattr(context, "health", {}))
    health_errors = _coerce_error_messages(health.get("errors", []))
    node_errors = _coerce_error_messages(node_data.get("errors", []))
    line_map = _extract_error_line_map([*node_errors, *health_errors])

    status = str(node_data.get("status", "working") or "working")
    _mark_room_statuses(rooms, line_map, status)

    connections = _safe_dict(getattr(context, "connections", {}))
    imports_from = [str(x) for x in connections.get("imports_from", []) if x]
    broken_imports = [
        str(item.get("import", "")).strip()
        for item in connections.get("broken", [])
        if isinstance(item, dict) and item.get("import")
    ]
    unique_imports = sorted({*imports_from, *broken_imports})

    connections_in = [str(x) for x in connections.get("imported_by", []) if x]
    connections_out = unique_imports.copy()
    context_exports = [str(x) for x in connections.get("exports_to", []) if x]
    unique_exports = sorted({*exports, *context_exports})

    locks = getattr(context, "locks", []) if context is not None else []
    lock_reason = None
    if locks and isinstance(locks, list):
        first_lock = locks[0]
        if isinstance(first_lock, dict):
            lock_reason = str(first_lock.get("reason") or first_lock.get("message") or "")

    payload = {
        "path": file_path,
        "status": status,
        "loc": int(node_data.get("loc", 0) or 0),
        "export_count": int(node_data.get("exportCount", len(unique_exports)) or 0),
        "building_height": float(node_data.get("buildingHeight", 3.0) or 3.0),
        "footprint": float(node_data.get("footprint", 2.0) or 2.0),
        "imports": unique_imports,
        "exports": unique_exports,
        "rooms": [r.to_dict() for r in rooms],
        "connections_in": connections_in,
        "connections_out": connections_out,
        "lock_state": lock_reason or None,
        "locked": bool(lock_reason),
        "centrality": float(node_data.get("centrality", 0.0) or 0.0),
        "in_cycle": bool(node_data.get("inCycle", False)),
        "health_errors": health_errors or node_errors,
    }
    return validate_building_panel(payload)


def select_room_entry(panel: BuildingPanel) -> Optional[Dict[str, Any]]:
    """Select a room-level handoff target for broken/combat workflows."""
    if not panel.rooms:
        return None

    broken_room = next((room for room in panel.rooms if room.status == "broken"), None)
    if broken_room:
        trigger = "broken_room_click"
        selected = broken_room
    elif panel.status == "combat":
        trigger = "combat_room_focus"
        selected = panel.rooms[0]
    elif panel.status == "broken":
        trigger = "broken_file_fallback"
        selected = panel.rooms[0]
    else:
        return None

    return {
        "trigger": trigger,
        "name": selected.name,
        "room_type": selected.room_type,
        "line_start": selected.line_start,
        "line_end": selected.line_end,
        "status": selected.status,
        "errors": list(selected.errors),
    }


def build_code_city_context_payload(
    node_data: Dict[str, Any],
    *,
    project_root: Path,
    context: Optional[Any],
) -> Dict[str, Any]:
    """Build normalized context payload consumed by Summon/Collabor8 and Sitting Room."""
    panel = build_building_panel_for_node(
        node_data,
        project_root=project_root,
        context=context,
    )
    room_entry = select_room_entry(panel)
    file_path = str(node_data.get("path", ""))
    context_scope = derive_context_scope(file_path)

    sitting_room = None
    if room_entry is not None:
        sitting_room = {
            "mode": "sitting_room",
            "entry_trigger": room_entry["trigger"],
            "file_path": file_path,
            "room": room_entry,
            "return_mode": "city",
        }

    return {
        "path": file_path,
        "status": panel.status,
        "context_scope": context_scope,
        "building_panel": panel.to_dict(),
        "room_entry": room_entry,
        "sitting_room": sitting_room,
    }

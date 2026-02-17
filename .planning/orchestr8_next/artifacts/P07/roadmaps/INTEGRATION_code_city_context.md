# Integration Roadmap: code_city_context.py → a_codex_plan

**Target:** `a_codex_plan`  
**Source:** `/home/bozertron/Orchestr8_jr/IP/features/maestro/code_city_context.py`  
**Version:** Orchestr8 v3.0  
**Date:** 2026-02-16

---

## Executive Summary

This roadmap defines the integration strategy for `code_city_context.py` into the `a_codex_plan` system. The module assembles context payloads from Code City node clicks for handoff to downstream systems including Summon, Collabor8, and Sitting Room. The DENSE + GAP pattern establishes four critical integration layers: type contracts, state boundaries, bridge definitions, and integration logic.

The module operates as a context assembly layer that transforms raw node data from Code City clicks into structured payloads containing building panel data, room entries, and Sitting Room activation triggers. It depends on `IP/contracts/building_panel.py` for type contracts and integrates with `06_maestro.py` for node click handling.

---

## GAP 1: Type Contracts

### Current Contract Structure

The module relies on `IP/contracts/building_panel.py` for its core type contracts. These are implemented as `@dataclass` rather than `TypedDict`:

| Contract | Location | Type | Description |
|----------|----------|------|-------------|
| `BuildingRoom` | `IP/contracts/building_panel.py:14` | `@dataclass` | Function or class inside a source file |
| `BuildingPanel` | `IP/contracts/building_panel.py:29` | `@dataclass` | Complete building inspection panel data |
| `BuildingStatus` | `IP/contracts/building_panel.py:10` | `Literal` | Status values: working, broken, combat |

### Required TypedDict Definitions

The current implementation lacks explicit TypedDict variants. For stricter typing in the a_codex_plan integration, the following TypedDict definitions should be considered:

```python
from typing import TypedDict, Literal, NotRequired

class ContextPayload(TypedDict):
    """Complete context payload for Code City node handoff."""
    path: str
    status: str
    context_scope: str
    building_panel: dict
    room_entry: NotRequired[dict | None]
    sitting_room: NotRequired[dict | None]


class RoomEntry(TypedDict):
    """Room-level handoff target for broken/combat workflows."""
    trigger: str
    name: str
    room_type: str
    line_start: int
    line_end: int
    status: str
    errors: list[str]


class SittingRoomHandoff(TypedDict):
    """Sitting Room activation payload."""
    mode: Literal["sitting_room"]
    entry_trigger: str
    file_path: str
    room: RoomEntry
    return_mode: Literal["city"]


class ContextScopeKey(TypedDict):
    """Context scope key derived from file path."""
    scope: str
```

### Literal Type Definitions

```python
from typing import Literal

TriggerType = Literal["broken_room_click", "combat_room_focus", "broken_file_fallback"]
RoomType = Literal["function", "class", "method"]

ERROR_LINE_PATTERNS: tuple = (
    re.compile(r":(?P<line>\d+)\b"),
    re.compile(r"\bline\s+(?P<line>\d+)\b", re.IGNORECASE),
)
```

---

## GAP 2: State Boundary

### Component State Structure

The module is designed for stateless operation. Each function call accepts all required parameters and produces output without maintaining internal state. However, the calling context in `06_maestro.py` uses Marimo state management:

```python
# From IP/plugins/06_maestro.py
get_code_city_context, set_code_city_context = mo.state({})
```

### Context Attribute Access Pattern

The module accesses context attributes dynamically rather than through a formal interface:

```python
# Current pattern (lines 182-210)
health = _safe_dict(getattr(context, "health", {}))
connections = _safe_dict(getattr(context, "connections", {}))
locks = getattr(context, "locks", []) if context is not None else []
```

This dynamic attribute access creates a loose coupling that could benefit from formalization:

### Recommended State Boundary

For a_codex_plan integration, consider a formal context protocol:

```python
from typing import Protocol, Optional

class CodeCityContextProtocol(Protocol):
    """Protocol for Code City node click context."""
    
    @property
    def health(self) -> dict:
        """Health signals for the node."""
        ...
    
    @property
    def connections(self) -> dict:
        """Connection signals for the node."""
        ...
    
    @property
    def locks(self) -> list:
        """Lock state for the node."""
        ...


# Component state for wrapper layer
_component_state: dict = {
    "_last_node": None,           # Last clicked node data
    "_last_context": None,         # Last context signals
    "_last_payload": None,        # Cached context payload
    "_context_scope": None,        # Derived context scope
    "_room_entry": None,          # Selected room entry
}
```

---

## GAP 3: Bridge Requirements

### Current Bridge Structure

The module provides three primary entry points for payload assembly:

```
IP/features/maestro/code_city_context.py
    |
    +-- derive_context_scope() --> context scope key
    +-- build_building_panel_for_node() --> BuildingPanel
    +-- select_room_entry() --> RoomEntry | None
    +-- build_code_city_context_payload() --> ContextPayload
```

### Bridge Payloads

#### BuildingPanel Bridge

The `build_building_panel_for_node()` function produces a `BuildingPanel` dataclass with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `path` | `str` | File path of the building |
| `status` | `BuildingStatus` | Node status (working/broken/combat) |
| `loc` | `int` | Lines of code |
| `export_count` | `int` | Number of exports |
| `building_height` | `float` | Visual height in Code City |
| `footprint` | `float` | Visual footprint in Code City |
| `imports` | `List[str]` | Import dependencies |
| `exports` | `List[str]` | Export symbols |
| `rooms` | `List[BuildingRoom]` | Functions/classes in file |
| `connections_in` | `List[str]` | Files importing this file |
| `connections_out` | `List[str]` | Files this file imports |
| `lock_state` | `Optional[str]` | Lock reason if locked |
| `locked` | `bool` | Lock state |
| `centrality` | `float` | Graph centrality score |
| `in_cycle` | `bool` | Circular dependency flag |
| `health_errors` | `List[str]` | Combined health errors |

#### ContextPayload Bridge

The `build_code_city_context_payload()` function produces the complete handoff payload:

```python
{
    "path": str,                          # File path
    "status": str,                         # Node status
    "context_scope": str,                  # Derived scope key
    "building_panel": dict,                # BuildingPanel.to_dict()
    "room_entry": dict | None,             # Selected room for handoff
    "sitting_room": dict | None,           # Sitting Room activation payload
}
```

#### SittingRoom Handoff Bridge

When room entry is selected, the `sitting_room` field activates:

```python
{
    "mode": "sitting_room",
    "entry_trigger": "broken_room_click",  # Trigger type
    "file_path": "IP/sample.py",
    "room": {
        "name": "bad_function",
        "room_type": "function",
        "line_start": 10,
        "line_end": 15,
        "status": "broken",
        "errors": ["NameError: name 'nope' is not defined"],
    },
    "return_mode": "city",
}
```

### Gap Analysis

| Bridge | Current | Status | Gap |
|--------|---------|--------|-----|
| `BuildingPanel` | `@dataclass` | ✅ Stable | No TypedDict variant |
| `ContextPayload` | `dict` | ✅ Stable | No formal TypedDict |
| `SittingRoomHandoff` | `dict` | ✅ Stable | No formal TypedDict |
| `RoomEntry` | `dict` | ✅ Stable | No formal TypedDict |

---

## GAP 4: Integration Logic

### Entry Points

| Entry Point | Purpose | Callers |
|-------------|---------|---------|
| `derive_context_scope()` | Derive scope key from file path | `build_code_city_context_payload()` |
| `build_building_panel_for_node()` | Build BuildingPanel from node data | `build_code_city_context_payload()` |
| `select_room_entry()` | Select room for broken/combat handoff | `build_code_city_context_payload()` |
| `build_code_city_context_payload()` | Complete payload assembly | `06_maestro.py`, tests |

### Integration Flow

The context assembly follows this flow:

```
Node Click Event (Code City)
    |
    v
06_maestro.py: on_click handler
    |
    v
build_code_city_context_payload(node_data, project_root, context)
    |
    +-- derive_context_scope(file_path)
    |       |
    |       v
    |   context_scope string
    |
    +-- build_building_panel_for_node(node_data, project_root, context)
    |       |
    |       +-- _extract_python_rooms() or _extract_generic_rooms()
    |       +-- _coerce_error_messages()
    |       +-- _extract_error_line_map()
    |       +-- _mark_room_statuses()
    |       |
    |       v
    |   BuildingPanel (validated)
    |
    +-- select_room_entry(building_panel)
    |       |
    |       v
    |   RoomEntry (if broken/combat)
    |
    v
ContextPayload {
    path,
    status,
    context_scope,
    building_panel,
    room_entry,
    sitting_room (if room_entry exists)
}
    |
    v
set_code_city_context(payload) --> mo.state({})
    |
    v
Shell/UI consumes building_panel, room_entry, sitting_room
```

### Downstream Consumers

| Consumer | Integration Point | Payload Fields Used |
|----------|-------------------|---------------------|
| `06_maestro.py` | `set_code_city_context()` | All fields |
| `shell.py` | `get_code_city_context()` | `building_panel`, `room_entry`, `context_scope` |
| `Summon` | `building_panel` | Imports, exports, connections |
| `Collabor8` | `building_panel` | File metadata, status |
| `Sitting Room` | `sitting_room` | Full handoff payload |

### Trigger Types

The module defines three trigger types for room-level handoff:

| Trigger | Condition | Use Case |
|---------|-----------|----------|
| `broken_room_click` | Room has error status | Direct user to broken function |
| `combat_room_focus` | File has combat status | Focus on first room |
| `broken_file_fallback` | File broken but no broken room | Focus on first room as fallback |

---

## Integration Recommendations

### Recommended Integration Pattern

```python
from pathlib import Path
from IP.features.maestro.code_city_context import (
    build_code_city_context_payload,
    derive_context_scope,
)

# Node click handler
def on_node_click(node_data: dict, project_root: Path, context) -> dict:
    payload = build_code_city_context_payload(
        node_data,
        project_root=project_root,
        context=context,
    )
    
    # Activate Sitting Room if room entry exists
    if payload.get("sitting_room"):
        activate_sitting_room(payload["sitting_room"])
    
    return payload
```

### Context Protocol Implementation

For stricter integration:

```python
from typing import Protocol

class ContextSignalProvider(Protocol):
    """Provides context signals for Code City node clicks."""
    
    def get_health(self, file_path: str) -> dict:
        """Return health signals for file."""
        ...
    
    def get_connections(self, file_path: str) -> dict:
        """Return connection signals for file."""
        ...
    
    def get_locks(self, file_path: str) -> list[dict]:
        """Return lock records for file."""
        ...


def build_context_from_provider(
    node_data: dict,
    project_root: Path,
    provider: ContextSignalProvider,
) -> dict:
    """Build context payload using a provider protocol."""
    file_path = node_data.get("path", "")
    
    context = SimpleNamespace(
        health=provider.get_health(file_path),
        connections=provider.get_connections(file_path),
        locks=provider.get_locks(file_path),
    )
    
    return build_code_city_context_payload(
        node_data,
        project_root=project_root,
        context=context,
    )
```

---

## Dependencies

### Internal Dependencies

| Module | Purpose |
|--------|---------|
| `IP/contracts/building_panel.py` | Type contracts (BuildingPanel, BuildingRoom) |
| `IP/plugins/06_maestro.py` | Primary caller, manages mo.state |
| `IP/features/maestro/views/shell.py` | Consumes building_panel and room_entry |

### Standard Library

| Module | Usage |
|--------|-------|
| `ast` | Python source code parsing for room extraction |
| `re` | Error line pattern matching |
| `pathlib` | File path manipulation |
| `typing` | Type hints |

### No External Dependencies

The module has no third-party dependencies beyond the standard library.

---

## Testing Coverage

The module includes comprehensive tests in `IP/features/maestro/tests/test_code_city_context.py`:

| Test | Coverage |
|------|----------|
| `test_derive_context_scope_for_file_and_dir` | Scope derivation |
| `test_build_building_panel_marks_broken_room` | Error mapping to rooms |
| `test_select_room_entry_prefers_broken_room` | Room selection logic |
| `test_build_code_city_context_payload_includes_sitting_room` | Full payload with Sitting Room |

---

## Summary

| GAP | Current State | Gap | Recommendation |
|-----|---------------|-----|----------------|
| **Type Contracts** | `@dataclass` in `building_panel.py` | No TypedDict variants | Add TypedDict for JSON serialization |
| **State Boundary** | Stateless, uses `getattr()` | No formal context protocol | Define `CodeCityContextProtocol` |
| **Bridge** | Dict-based payloads | No formal contract | Add TypedDict for ContextPayload |
| **Integration Logic** | Entry points stable | Context attribute access loose | Use protocol-based provider |

The module is well-structured for integration with clear entry points and stable output contracts. The primary gaps are formal type definitions and a protocol-based context provider for stricter coupling.

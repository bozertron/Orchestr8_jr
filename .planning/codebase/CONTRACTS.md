# Contracts Module Analysis

**Analysis Date:** 2026-02-16  
**Source:** `/home/bozertron/Orchestr8_jr/IP/contracts/`  
**Target:** `a_codex_plan` integration

---

## Executive Summary

The contracts module (`IP/contracts/`) serves as the foundational **blind integration safety layer** for Orchestr8, providing strongly-typed schemas for all integration boundaries where Code City, the Settlement System, and the Marimo runtime intersect. The module enforces deterministic behavior at all surfaces where components meet.

---

## 1. What Contracts Exist?

The contracts module exports **9 primary schema files** covering building panels, camera state, node events, connection actions, lock overlays, marimo bridges, settlement surveys, status merge policies, and town square classifications.

### 1.1 Contract Summary Table

| Contract File | Primary Types | Literal Types | Validation Functions |
|---------------|---------------|---------------|---------------------|
| `building_panel.py` | `BuildingPanel`, `BuildingRoom` | `BuildingStatus` | `validate_building_panel()` |
| `camera_state.py` | `CameraState` | `CameraMode` | Helper constructors |
| `code_city_node_event.py` | `CodeCityNodeEvent` | `CodeCityStatus` | `validate_code_city_node_event()` |
| `connection_action_event.py` | `ConnectionActionEvent`, `ConnectionEdge` | `ConnectionAction` | `validate_connection_action_event()` |
| `lock_overlay.py` | `LockOverlay` | `LockType`, `DisplayZone` | `LockOverlay.validate()` |
| `marimo_bridge.py` | Runtime helpers | None | None |
| `settlement_survey.py` | `SettlementSurvey`, `FiefdomData`, `BoundaryContract`, `WiringConnection` | None | `parse_settlement_survey()` |
| `status_merge_policy.py` | Functions only | `StatusType` | None |
| `town_square_classification.py` | `TownSquareClassification` | `Classification`, `DisplayZone` | `TownSquareClassification.validate()` |

---

## 2. What Schemas Are Validated?

### 2.1 BuildingPanel Contract (`building_panel.py`)

**Purpose:** Data contract for the Code City building inspection panel — displays when a user clicks a building (file) in Code City.

```python
@dataclass
class BuildingRoom:
    name: str
    line_start: int
    line_end: int
    room_type: Literal["function", "class", "method"]
    status: BuildingStatus = "working"
    errors: List[str] = field(default_factory=list)

@dataclass
class BuildingPanel:
    path: str
    status: BuildingStatus
    loc: int
    export_count: int = 0
    building_height: float = 3.0
    footprint: float = 2.0
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    rooms: List[BuildingRoom] = field(default_factory=list)
    connections_in: List[str] = field(default_factory=list)
    connections_out: List[str] = field(default_factory=list)
    lock_state: Optional[str] = None
    locked: bool = False
    centrality: float = 0.0
    in_cycle: bool = False
    health_errors: List[str] = field(default_factory=list)
```

**Validation:** `validate_building_panel()` enforces required fields (`path`, `status`, `loc`) and validates status values.

### 2.2 CameraState Contract (`camera_state.py`)

**Purpose:** Camera position and animation state for Code City navigation.

```python
@dataclass
class CameraState:
    mode: CameraMode  # overview | neighborhood | building | room | sitting_room | focus
    position: Tuple[float, float, float]
    target: Tuple[float, float, float]
    zoom: float
    return_stack: List[Dict[str, Any]] = field(default_factory=list)
    transition_ms: int = 1000
    easing: str = "easeInOutCubic"
    navigation_context: Dict[str, Any] = field(default_factory=dict)
```

**Factory Functions:**
- `get_default_camera_state()` — Overview for full city visibility
- `get_neighborhood_camera_state(center_x, center_y, radius)` — Neighborhood cluster view
- `get_building_camera_state(building_x, building_y, height)` — Single building inspection
- `get_focus_camera_state(node_x, node_y, path)` — Quick dive with keyboard shortcuts

### 2.3 CodeCityNodeEvent Contract (`code_city_node_event.py`)

**Purpose:** Bridge schema between JavaScript click events and Python handlers.

```python
@dataclass
class CodeCityNodeEvent:
    path: str
    status: CodeCityStatus  # "working" | "broken" | "combat"
    loc: int
    errors: List[str] = field(default_factory=list)
    nodeType: Optional[str] = None
    centrality: Optional[float] = None
    inCycle: Optional[bool] = None
    incomingCount: Optional[int] = None
    outgoingCount: Optional[int] = None
```

**Validation:** `validate_code_city_node_event()` enforces required fields and validates status values.

### 2.4 ConnectionActionEvent Contract (`connection_action_event.py`)

**Purpose:** Bridge for Code City edge panel actions (rewiring connections).

```python
@dataclass
class ConnectionEdge:
    source: str
    target: str
    resolved: bool = True
    lineNumber: int = 0
    edgeType: str = "import"

@dataclass
class ConnectionActionEvent:
    action: ConnectionAction  # "dry_run_rewire" | "apply_rewire"
    connection: ConnectionEdge
    proposedTarget: Optional[str] = None
    actorRole: Optional[str] = None
    signalNodes: List[str] = field(default_factory=list)
    signalEdges: List[str] = field(default_factory=list)
```

**Validation:** `validate_connection_action_event()` enforces action types and connection requirements.

### 2.5 LockOverlay Contract (`lock_overlay.py`)

**Purpose:** Visual rules for locked nodes/ports and Louis lock reasons in Code City.

```python
@dataclass
class LockOverlay:
    path: str
    lock_type: LockType  # "louis" | "readonly" | "system"
    reason: str = ""
    locked_by: str = "unknown"
    locked_at: str = ""
    visual_opacity: float = 0.4
    show_lock_icon: bool = True
    allow_inspection: bool = True
```

**Validation:** `LockOverlay.validate()` checks lock types and opacity range (0.0-1.0).

### 2.6 SettlementSurvey Contract (`settlement_survey.py`)

**Purpose:** Typed structures for Settlement System integration.

```python
class WiringStatus(Enum):
    WORKING = "working"
    BROKEN = "broken"
    COMBAT = "combat"

@dataclass
class FiefdomData:
    name: str
    files: List[str]
    entry_points: List[str]
    exports: List[str]
    internal_coupling: float
    external_coupling: float

@dataclass
class BoundaryContract:
    from_fiefdom: str
    to_fiefdom: str
    allowed_types: List[str]
    forbidden_crossings: List[str]
    contract_status: str  # "defined" | "draft" | "missing"

@dataclass
class WiringConnection:
    source: str
    target: str
    status: WiringStatus
    agents_active: bool = False

@dataclass
class SettlementSurvey:
    metadata: Dict[str, Any]
    fiefdoms: Dict[str, FiefdomData]
    boundary_contracts: List[BoundaryContract]
    wiring_state: List[WiringConnection]
```

**Validation:** `parse_settlement_survey()` validates required keys and enums.

### 2.7 StatusMergePolicy Contract (`status_merge_policy.py`)

**Purpose:** Canonical status merge policy — combat > broken > working.

```python
StatusType = Literal["working", "broken", "combat"]

STATUS_PRIORITY = {
    "combat": 3,
    "broken": 2,
    "working": 1,
}
```

**Functions:**
- `merge_status(*statuses)` — Returns highest priority status
- `get_status_color(status)` — Returns hex color (`#D4AF37` gold, `#1fbdea` teal, `#9D4EDD` purple)

### 2.8 TownSquareClassification Contract (`town_square_classification.py`)

**Purpose:** Rules for infrastructure files excluded from building rendering.

```python
Classification = Literal["infrastructure", "config", "build", "test", "docs", "asset"]
DisplayZone = Literal["town_square", "hidden", "minimap_only"]

@dataclass
class TownSquareClassification:
    path: str
    classification: Classification
    display_zone: DisplayZone = "town_square"
    reason: str = ""
    icon: str = ""
    group: str = ""
```

**Validation:** `TownSquareClassification.validate()` checks classification and display zone values.

### 2.9 MarimoBridge Contract (`marimo_bridge.py`)

**Purpose:** Shared marimo DOM bridge helpers for JS/Python event channels.

**Function:** `build_marimo_bridge_runtime_js(namespace)` — Returns JavaScript runtime helpers for resolving marimo bridge inputs and writing payloads.

---

## 3. Which Components Use These Contracts?

### 3.1 Consumer Components

| Component | File Path | Contracts Used |
|-----------|-----------|-----------------|
| Woven Maps (Core) | `IP/woven_maps.py` | `status_merge_policy`, `town_square_classification` |
| Graph Builder | `IP/features/code_city/graph_builder.py` | `status_merge_policy`, `settlement_survey` |
| Render Pipeline | `IP/features/code_city/render.py` | `camera_state` |
| Code City Context | `IP/features/maestro/code_city_context.py` | `building_panel` |
| Maestro Plugin | `IP/plugins/06_maestro.py` | `code_city_node_event`, `connection_action_event`, `marimo_bridge` |

### 3.2 Test Coverage

All contracts have corresponding test files in `IP/contracts/tests/`:

- `test_building_panel.py`
- `test_camera_state.py`
- `test_code_city_node_event.py`
- `test_connection_action_event.py`
- `test_lock_overlay.py`
- `test_settlement_survey.py`
- `test_status_merge_policy.py`
- `test_town_square_classification.py`

---

## 4. Integration into a_codex_plan

### 4.1 Integration Strategy

The contracts module integrates with `a_codex_plan` through several layers:

1. **Type Contracts Layer** — Direct import of dataclass schemas
2. **State Boundaries Layer** — Validation functions for JSON communication surfaces
3. **Bridge Definitions Layer** — `marimo_bridge.py` for JS/Python event channels
4. **Integration Logic Layer** — Consumer components in `a_codex_plan`

### 4.2 Recommended Integration Points

#### 4.2.1 Type Definitions (GAP 1)

For stricter static typing in `a_codex_plan`, implement TypedDict variants:

```python
# Example: BuildingPanel TypedDict for JSON surfaces
from typing import TypedDict, NotRequired

class BuildingPanelDict(TypedDict):
    path: str
    status: str  # "working" | "broken" | "combat"
    loc: int
    export_count: NotRequired[int]
    building_height: NotRequired[float]
    footprint: NotRequired[float]
    imports: NotRequired[list[str]]
    exports: NotRequired[list[str]]
    rooms: NotRequired[list[dict]]
    connections_in: NotRequired[list[str]]
    connections_out: NotRequired[list[str]]
    lock_state: NotRequired[str | None]
    locked: NotRequired[bool]
    centrality: NotRequired[float]
    in_cycle: NotRequired[bool]
    health_errors: NotRequired[list[str]]
```

#### 4.2.2 State Boundaries (GAP 2)

Implement validation wrapper for incoming data:

```python
def validate_incoming_payload(payload: dict, contract_name: str) -> bool:
    """Validate incoming payload against contract."""
    validators = {
        "BuildingPanel": validate_building_panel,
        "CodeCityNodeEvent": validate_code_city_node_event,
        "ConnectionActionEvent": validate_connection_action_event,
        "SettlementSurvey": parse_settlement_survey,
    }
    validator = validators.get(contract_name)
    if not validator:
        raise ValueError(f"Unknown contract: {contract_name}")
    return validator(payload)
```

#### 4.2.3 Bridge Integration (GAP 3)

Integrate `build_marimo_bridge_runtime_js()` into `a_codex_plan` frontend initialization:

```python
# In a_codex_plan UI setup
from IP.contracts.marimo_bridge import build_marimo_bridge_runtime_js

bridge_js = build_marimo_bridge_runtime_js("__aCodexPlanBridge")
# Inject into page <head>
```

#### 4.2.4 Consumer Component Migration (GAP 4)

| Component | Source | Target in a_codex_plan |
|-----------|--------|------------------------|
| BuildingPanel | `IP/features/maestro/code_city_context.py` | `a_codex_plan/features/code_city/context.py` |
| CameraState | `IP/features/code_city/render.py` | `a_codex_plan/features/code_city/camera.py` |
| NodeEvents | `IP/plugins/06_maestro.py` | `a_codex_plan/plugins/maestro.py` |
| SettlementSurvey | `IP/features/code_city/graph_builder.py` | `a_codex_plan/features/settlement/graph.py` |

### 4.3 Status Merge Policy Integration

The status merge policy should be the **single source of truth** for all status operations in `a_codex_plan`:

```python
from IP.contracts.status_merge_policy import merge_status, get_status_color, STATUS_PRIORITY

# Use in any component that aggregates status
final_status = merge_status(status_a, status_b, status_c)
color = get_status_color(final_status)
```

### 4.4 Pre-Integration Checklist

Before integrating the contracts module with `a_codex_plan`, verify:

- [ ] All contracts have passing tests in `IP/contracts/tests/`
- [ ] Dataclass serialization (`to_dict()`) works for all contracts
- [ ] Factory functions return valid instances
- [ ] Validation functions raise appropriate errors on malformed input
- [ ] Example payloads in each contract file are valid

---

## 5. Key Design Patterns

### 5.1 Dataclass + Validation

Each contract uses `@dataclass` with:
- `to_dict()` method for serialization
- Separate validation function or `.validate()` method
- Example payload as dictionary for testing

### 5.2 Literal Types for Enums

All enums use `Literal` type hints for strict type checking:
- `CodeCityStatus = Literal["working", "broken", "combat"]`
- `CameraMode = Literal["overview", "neighborhood", "building", "room", "sitting_room", "focus"]`

### 5.3 Factory Methods

Complex contracts include factory methods:
- `CameraState` has factory functions for each mode
- `LockOverlay.from_dict()` for dict parsing
- `TownSquareClassification.from_dict()` for dict parsing

---

## 6. File Locations Reference

| File | Purpose |
|------|---------|
| `IP/contracts/__init__.py` | Module exports and color system documentation |
| `IP/contracts/building_panel.py` | Building inspection panel schema |
| `IP/contracts/camera_state.py` | Camera navigation state |
| `IP/contracts/code_city_node_event.py` | JS→Python node click events |
| `IP/contracts/connection_action_event.py` | Connection rewire actions |
| `IP/contracts/lock_overlay.py` | Locked file visualization rules |
| `IP/contracts/marimo_bridge.py` | JS/Python DOM bridge helpers |
| `IP/contracts/settlement_survey.py` | Settlement System data structures |
| `IP/contracts/status_merge_policy.py` | Status precedence (gold > teal > purple) |
| `IP/contracts/town_square_classification.py` | Infrastructure file classification |

---

*Contract analysis: 2026-02-16*

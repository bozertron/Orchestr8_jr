# Integration Roadmap: contracts module → a_codex_plan

**Target:** `a_codex_plan`  
**Source:** `/home/bozertron/Orchestr8_jr/IP/contracts/`  
**Version:** Orchestr8 v3.0  
**Date:** 2026-02-16

---

## Executive Summary

This roadmap defines the integration strategy for the `IP/contracts/` module into the `a_codex_plan` system. The contracts module serves as the foundational type safety layer for Orchestr8, providing strongly-typed schemas for all integration boundaries where Code City, the Settlement System, and the Marimo runtime intersect. The DENSE + GAP pattern establishes four critical integration layers: type contracts, state boundaries, bridge definitions, and integration logic.

The module operates as the blind integration safety layer, enforcing deterministic behavior at all surfaces where components meet. Each contract defines the exact shape of data flowing between systems, ensuring that any future agent can wire components without recovering prior context. The contracts module exports 9 primary schema files covering building panels, camera state, node events, connection actions, lock overlays, marimo bridges, settlement surveys, status merge policies, and town square classifications.

---

## GAP 1: Type Contracts

### Current Contract Structure Overview

The contracts module implements comprehensive type contracts using `@dataclass` decorators with validation methods. These provide runtime type safety and serialization capabilities. The following table summarizes all contracts across the 9 schema files:

| Contract File | Primary Types | Literal Types | Validation Functions |
|---------------|---------------|---------------|----------------------|
| `building_panel.py` | `BuildingPanel`, `BuildingRoom` | `BuildingStatus` | `validate_building_panel()` |
| `camera_state.py` | `CameraState` | `CameraMode` | Helper constructors |
| `code_city_node_event.py` | `CodeCityNodeEvent` | `CodeCityStatus` | `validate_code_city_node_event()` |
| `connection_action_event.py` | `ConnectionActionEvent`, `ConnectionEdge` | `ConnectionAction` | `validate_connection_action_event()` |
| `lock_overlay.py` | `LockOverlay` | `LockType`, `DisplayZone` | `LockOverlay.validate()` |
| `marimo_bridge.py` | Runtime helpers | None | None |
| `settlement_survey.py` | `SettlementSurvey`, `FiefdomData`, `BoundaryContract`, `WiringConnection` | None | `parse_settlement_survey()` |
| `status_merge_policy.py` | Functions only | `StatusType` | None |
| `town_square_classification.py` | `TownSquareClassification` | `Classification`, `DisplayZone` | `TownSquareClassification.validate()` |

### BuildingPanel Contract Details

The `building_panel.py` file defines the primary contract for Code City building inspection panels:

```python
@dataclass
class BuildingRoom:
    """A function or class inside a source file (a 'room' in the building)."""
    name: str
    line_start: int
    line_end: int
    room_type: Literal["function", "class", "method"]
    status: BuildingStatus = "working"
    errors: List[str] = field(default_factory=list)

@dataclass
class BuildingPanel:
    """Data contract for the Code City building inspection panel."""
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

The validation function `validate_building_panel()` enforces required fields and type constraints. This contract is critical for the building inspection panel displayed when users click on buildings in Code City. It provides complete file metadata including imports, exports, function/class rooms, and connection references.

### CameraState Contract Details

The `camera_state.py` file defines the camera position and animation state contract:

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

The module provides factory functions for creating camera states at different zoom levels: `get_default_camera_state()` for overview, `get_neighborhood_camera_state()` for neighborhood view, `get_building_camera_state()` for building inspection, and `get_focus_camera_state()` for quick keyboard-driven navigation. Each factory function presets appropriate position, target, zoom, and transition parameters.

### CodeCityNodeEvent Contract Details

The `code_city_node_event.py` file provides the bridge schema between JavaScript click events and Python handlers:

```python
@dataclass
class CodeCityNodeEvent:
    path: str
    status: CodeCityStatus  # working | broken | combat
    loc: int
    errors: List[str] = field(default_factory=list)
    nodeType: Optional[str] = None
    centrality: Optional[float] = None
    inCycle: Optional[bool] = None
    incomingCount: Optional[int] = None
    outgoingCount: Optional[int] = None
```

This contract handles the initial event payload when a user clicks a node in the Code City visualization. The `validate_code_city_node_event()` function ensures all required fields are present and validates status values.

### ConnectionActionEvent Contract Details

The `connection_action_event.py` file defines the schema for edge panel actions:

```python
@dataclass
class ConnectionEdge:
    """Connection edge payload from Woven Maps selection state."""
    source: str
    target: str
    resolved: bool = True
    lineNumber: int = 0
    edgeType: str = "import"

@dataclass
class ConnectionActionEvent:
    """Action payload emitted from connection panel controls."""
    action: ConnectionAction  # dry_run_rewire | apply_rewire
    connection: ConnectionEdge
    proposedTarget: Optional[str] = None
    actorRole: Optional[str] = None
    signalNodes: List[str] = field(default_factory=list)
    signalEdges: List[str] = field(default_factory=list)
```

This contract supports both dry-run and apply operations for connection rewiring. The validation function `validate_connection_action_event()` enforces required fields and validates action types.

### LockOverlay Contract Details

The `lock_overlay.py` file defines visual rules for locked nodes:

```python
@dataclass
class LockOverlay:
    """Visual rules for locked nodes/ports and Louis lock reasons in Code City."""
    path: str
    lock_type: LockType  # louis | readonly | system
    reason: str = ""
    locked_by: str = "unknown"
    locked_at: str = ""
    visual_opacity: float = 0.4
    show_lock_icon: bool = True
    allow_inspection: bool = True
```

The contract includes a `validate()` method that enforces lock type constraints and opacity ranges. The factory method `from_dict()` provides validated construction from dictionary data.

### SettlementSurvey Contract Details

The `settlement_survey.py` file provides the Settlement System integration schema:

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
    contract_status: str  # defined | draft | missing

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

This contract provides the complete data structure for Settlement System integration, including fiefdom definitions, boundary contracts between fiefdoms, and wiring connection state.

### StatusMergePolicy Contract Details

The `status_merge_policy.py` file defines the canonical status precedence rules:

```python
StatusType = Literal["working", "broken", "combat"]

STATUS_PRIORITY = {
    "combat": 3,
    "broken": 2,
    "working": 1,
}

def merge_status(*statuses: StatusType) -> StatusType:
    """Merge multiple status values using canonical precedence.
    Rule: combat > broken > working
    Returns 'working' for empty input or all-None input.
    Raises ValueError for unknown status values.
    """

def get_status_color(status: StatusType) -> str:
    """Get canonical hex color for a status value."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
    }
```

This is a pure function module with no data classes. It provides the canonical status merge logic used throughout Orchestr8 for combining multiple status values with the precedence rule: combat outranks broken, which outranks working.

### TownSquareClassification Contract Details

The `town_square_classification.py` file defines rules for infrastructure files:

```python
@dataclass
class TownSquareClassification:
    """Rules for infrastructure files excluded from building rendering."""
    path: str
    classification: Classification  # infrastructure | config | build | test | docs | asset
    display_zone: DisplayZone = "town_square"  # town_square | hidden | minimap_only
    reason: str = ""
    icon: str = ""
    group: str = ""
```

The contract validates classification and display zone values, providing factory construction through `from_dict()` with validation.

### Required TypedDict Definitions

The current implementation uses `@dataclass` which provides runtime validation but lacks explicit TypedDict variants for stricter static typing. For a_codex_plan integration, the following TypedDict definitions are recommended for JSON communication surfaces:

```python
from typing import TypedDict, Literal, NotRequired

class BuildingPanelDict(TypedDict):
    """Serialized BuildingPanel for JSON communication."""
    path: str
    status: Literal["working", "broken", "combat"]
    loc: int
    export_count: int
    building_height: float
    footprint: float
    imports: list[str]
    exports: list[str]
    rooms: list[dict]
    connections_in: list[str]
    connections_out: list[str]
    lock_state: str | None
    locked: bool
    centrality: float
    in_cycle: bool
    health_errors: list[str]

class CameraStateDict(TypedDict):
    """Serialized CameraState for JSON communication."""
    mode: Literal["overview", "neighborhood", "building", "room", "sitting_room", "focus"]
    position: tuple[float, float, float]
    target: tuple[float, float, float]
    zoom: float
    return_stack: list[dict]
    transition_ms: int
    easing: str
    navigation_context: dict

class SettlementSurveyDict(TypedDict):
    """Serialized SettlementSurvey for JSON communication."""
    metadata: dict
    fiefdoms: dict
    boundary_contracts: list[dict]
    wiring_state: list[dict]
```

---

## GAP 2: State Boundary

### Stateless Design Pattern

The contracts module is designed for stateless operation. All contract classes are pure data containers with serialization methods, and all validation functions are pure functions that transform input data into validated output without side effects. This stateless design ensures predictable behavior across all integration boundaries.

### BuildingPanel State Boundary

The `BuildingPanel` contract serves as a snapshot of building state at the moment of inspection. It does not maintain references to live objects or dynamic state. The contract captures the following state boundaries:

The import and export lists represent static analysis results computed at scan time, not live import resolution. The rooms list represents functions and classes detected at analysis time. The connection lists represent the graph state at analysis time. The lock state represents the Louis protection status at the moment of panel creation.

When integrating with a_codex_plan, treat `BuildingPanel` instances as immutable snapshots. Do not attempt to mutate fields after construction; instead, construct new instances with updated values.

### CameraState State Boundary

The `CameraState` contract represents the current camera position and animation parameters. While the dataclass itself is mutable, the integration boundary treats camera state as a value object. Key state boundaries include:

The `return_stack` field maintains navigation history for round-trip drilling into nodes and back. The stack is managed through `push_return_state()`, `pop_return_state()`, and `clear_return_stack()` methods. These methods mutate the internal list but should be treated as a stack data structure rather than persistent state.

The `navigation_context` dictionary carries metadata about how the user arrived at the current view. This context is preserved across transitions but does not affect camera positioning directly.

When integrating with the 3D visualization layer, always transmit complete `CameraState` objects rather than delta updates to ensure synchronization.

### SettlementSurvey State Boundary

The `SettlementSurvey` contract represents the complete state of the Settlement System at a point in time. The state boundaries are:

The `metadata` field contains survey metadata including project name, timestamp, and survey version. The `fiefdoms` dictionary maps fiefdom names to their complete definition including files, entry points, exports, and coupling metrics. The `boundary_contracts` list defines explicit contracts between fiefdoms. The `wiring_state` list captures the current state of all wiring connections.

When integrating with a_codex_plan, the survey should be treated as a snapshot. New surveys replace old ones rather than being merged incrementally.

### State Management Recommendations

For a_codex_plan integration, implement the following state management patterns:

First, prefer value semantics for contract instances. Pass complete objects rather than deltas across component boundaries. Second, treat contracts as immutable after construction. Use factory functions to create modified copies. Third, serialize state snapshots for persistence. Use the `to_dict()` methods for storage and reconstruction. Fourth, validate on deserialization. Always run validation functions when reconstructing contract instances from stored or transmitted data.

---

## GAP 3: Bridge Definitions

### Marimo Bridge Runtime

The `marimo_bridge.py` file provides JavaScript runtime helpers for resolving marimo bridge inputs. This is the only bridge-related file in the contracts module:

```python
def build_marimo_bridge_runtime_js(namespace: str = "__orchimo_bridge") -> str:
    """Return JS runtime helpers for marimo bridge input resolution."""
```

The function generates an immediately-invoked function expression that establishes a global namespace with two helper functions:

The `resolveBridgeInput(bridgeId)` function queries the DOM for marimo UI elements with the specified object ID and returns the associated input or textarea element. It handles both direct querySelector matches and shadow DOM traversal.

The `writePayloadToBridge(bridgeId, payload, label)` function serializes a payload to JSON, writes it to the bridge input value, and dispatches an input event to trigger marimo reactivity.

### Bridge Usage Pattern

The marimo bridge pattern works as follows: Python renders a hidden input element with a known object ID. JavaScript writes JSON payloads to this input. Marimo detects the input change and triggers the associated Python callback.

This pattern enables bidirectional communication between the JavaScript 3D visualization and Python handlers. The contracts module provides the schema for payloads, while the bridge handles the transport mechanism.

### Bridge Integration Points

The following contracts flow through the marimo bridge:

The `CodeCityNodeEvent` flows from JavaScript click handlers to Python `on_click` handlers in `06_maestro.py`. The `ConnectionActionEvent` flows from connection panel controls to Python handlers. The `CameraState` flows bidirectionally: from Python to JavaScript for initial positioning, and from JavaScript to Python for user-driven navigation.

### Bridge Security Considerations

When integrating the marimo bridge with a_codex_plan, implement the following security measures:

Validate all incoming payloads using the validation functions before processing. Sanitize string inputs to prevent injection attacks. Limit payload size to prevent denial-of-service attacks. Implement authentication for sensitive actions like connection rewiring.

---

## GAP 4: Integration Logic

### Integration Architecture

The contracts module integrates with a_codex_plan through several layers. The primary integration points are:

The visualization layer (`woven_maps.py`, `woven_maps_3d.js`) consumes `CameraState` for camera positioning and emits `CodeCityNodeEvent` for node clicks. The inspection layer (`code_city_context.py`) consumes `BuildingPanel` for building details and `CodeCityNodeEvent` for click handling. The connection layer (`connection_actions.py`) consumes `ConnectionActionEvent` for edge rewire operations. The protection layer (`louis_core.py`) consumes `LockOverlay` for locked node rendering. The classification layer consumes `TownSquareClassification` for infrastructure file handling. The settlement layer (`settlement_survey.py`) provides `SettlementSurvey` for fiefdom management.

### BuildingPanel Integration Logic

Integration with the building panel contract follows this flow:

First, the connection verifier analyzes import relationships and produces connection data. Second, the health watcher analyzes file health and produces error data. Third, the woven maps renderer computes building geometry from file metrics. Fourth, when a user clicks a building, the click handler collects all relevant data and constructs a `BuildingPanel` instance using `validate_building_panel()`. Fifth, the panel is rendered in the inspection UI.

For a_codex_plan integration, implement a factory function that orchestrates the data collection:

```python
def create_building_panel(file_path: str, project_root: str) -> BuildingPanel:
    """Factory function to create BuildingPanel from file analysis."""
    # 1. Get connection data
    # 2. Get health data  
    # 3. Compute geometry
    # 4. Get lock state
    # 5. Construct and validate panel
```

### CameraState Integration Logic

Camera state integration follows a bidirectional flow:

Python initializes camera state using factory functions like `get_default_camera_state()` or `get_building_camera_state()`. The state is serialized to JSON and transmitted to the JavaScript visualization layer via marimo output. JavaScript maintains the camera state and animates transitions. On user navigation, JavaScript emits the new state, which Python receives and validates.

For a_codex_plan integration, implement state synchronization:

```python
def sync_camera_state(js_state: dict) -> CameraState:
    """Reconstruct CameraState from JavaScript state."""
    # Validate required fields
    # Apply defaults for missing fields
    # Return validated CameraState

def serialize_camera_state(state: CameraState) -> dict:
    """Serialize CameraState for JavaScript consumption."""
    return state.to_dict()
```

### ConnectionActionEvent Integration Logic

Connection action events flow from the connection panel UI to Python handlers:

The user selects an edge in the visualization. The connection panel displays edge details and action buttons. The user clicks an action button (dry_run_rewire or apply_rewire). The JavaScript handler constructs a `ConnectionActionEvent` payload. The payload is written to the marimo bridge. Python validates the payload using `validate_connection_action_event()`. Python executes the action and returns results.

For a_codex_plan integration, implement action handlers:

```python
def handle_connection_action(event: ConnectionActionEvent) -> dict:
    """Handle connection action from panel."""
    if event.action == "dry_run_rewire":
        return dry_run_rewire(event)
    elif event.action == "apply_rewire":
        return apply_rewire(event)
    else:
        raise ValueError(f"Unknown action: {event.action}")
```

### SettlementSurvey Integration Logic

Settlement survey integration operates at the system level:

The survey is generated by the Settlement System analysis. The survey data is stored in the contracts module format. Downstream consumers query the survey for fiefdom definitions, boundary contracts, and wiring state.

For a_codex_plan integration, implement survey storage and retrieval:

```python
def store_survey(survey: SettlementSurvey) -> None:
    """Store settlement survey for later retrieval."""
    # Serialize to JSON
    # Store in persistence layer

def load_survey() -> SettlementSurvey:
    """Load current settlement survey."""
    # Load from persistence layer
    # Parse using parse_settlement_survey()
```

### StatusMergePolicy Integration Logic

The status merge policy is a pure function that integrates at multiple points:

When merging status from multiple files in a fiefdom, use `merge_status()`. When determining node color in visualization, use `get_status_color()`. When validating status values in other contracts, reference `STATUS_PRIORITY` for comparison.

For a_codex_plan integration, the status merge policy should be the single source of truth for all status operations:

```python
def compute_fiefdom_status(files: list[FileStatus]) -> str:
    """Compute fiefdom status from constituent file statuses."""
    return merge_status(*[f.status for f in files])
```

### Testing Strategy

For each contract, implement tests covering:

Validation of valid payloads returns correct instances. Validation of invalid payloads raises appropriate exceptions. Serialization and deserialization preserves data. Factory functions produce correct instances. Edge cases like empty lists, None values, and boundary values.

Example test patterns:

```python
def test_building_panel_validation_valid():
    """Valid payload produces correct BuildingPanel."""
    payload = EXAMPLE_BUILDING_PANEL
    panel = validate_building_panel(payload)
    assert panel.path == payload["path"]
    assert panel.status == payload["status"]

def test_building_panel_validation_missing_field():
    """Missing required field raises ValueError."""
    payload = {"status": "working", "loc": 100}  # missing path
    with pytest.raises(ValueError, match="Missing required field"):
        validate_building_panel(payload)
```

### Migration Path

For existing code using contracts, implement the following migration steps:

First, audit current usage of contract classes and validate where validation functions are called. Second, add validation function calls where they are missing. Third, replace mutable operations with immutable factory patterns. Fourth, add TypedDict variants for new JSON communication surfaces. Fifth, update tests to cover validation behavior.

---

## Dependencies

### Internal Dependencies

The contracts module has minimal internal dependencies:

| Module | Purpose |
|--------|---------|
| `IP/connection_verifier.py` | Provides connection data for BuildingPanel |
| `IP/health_watcher.py` | Provides health data for BuildingPanel |
| `IP/woven_maps.py` | Consumes CameraState for visualization |
| `IP/plugins/06_maestro.py` | Consumes events and panels |
| `IP/features/maestro/code_city_context.py` | Consumes BuildingPanel |

### External Dependencies

The contracts module has no external dependencies beyond the Python standard library:

| Module | Usage |
|--------|-------|
| `dataclasses` | Decorator for contract classes |
| `typing` | Type hints for contracts |
| `enum` | Enum definitions in settlement_survey |
| `asdict` | Serialization helper |

This zero-dependency design ensures the contracts module can be imported and used in any Python environment without additional package installation.

---

## Integration Checklist

Before integrating the contracts module with a_codex_plan, verify the following items:

Ensure all validation functions are called on incoming data from external sources. Implement factory functions for creating contract instances from analysis results. Add TypedDict variants for JSON communication surfaces. Implement proper serialization and deserialization for persistence. Write comprehensive tests covering validation, serialization, and edge cases. Document the status merge precedence rule in user-facing interfaces. Ensure camera state synchronization between Python and JavaScript. Implement proper error handling for invalid payloads across all integration points.

---

## File Manifest

| File | Lines | Primary Exports |
|------|-------|-----------------|
| `building_panel.py` | 135 | `BuildingPanel`, `BuildingRoom`, `validate_building_panel()` |
| `camera_state.py` | 130 | `CameraState`, factory functions |
| `code_city_node_event.py` | 62 | `CodeCityNodeEvent`, `validate_code_city_node_event()` |
| `connection_action_event.py` | 108 | `ConnectionActionEvent`, `validate_connection_action_event()` |
| `lock_overlay.py` | 76 | `LockOverlay` |
| `marimo_bridge.py` | 52 | `build_marimo_bridge_runtime_js()` |
| `settlement_survey.py` | 94 | `SettlementSurvey`, `parse_settlement_survey()` |
| `status_merge_policy.py` | 44 | `merge_status()`, `get_status_color()`, `STATUS_PRIORITY` |
| `town_square_classification.py` | 82 | `TownSquareClassification` |
| `__init__.py` | 69 | Public API exports |

Total: 842 lines of core contract definitions plus comprehensive examples and documentation.

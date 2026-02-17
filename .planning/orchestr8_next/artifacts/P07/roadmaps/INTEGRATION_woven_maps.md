# Integration Roadmap: woven_maps.py → a_codex_plan

**Target:** `a_codex_plan`  
**Source:** `/home/bozertron/Orchestr8_jr/IP/woven_maps.py`  
**Version:** Orchestr8 v3.0  
**Date:** 2026-02-16

---

## Executive Summary

This roadmap defines the integration strategy for `woven_maps.py` (Woven Maps Code City Visualization) into the `a_codex_plan` system. The module renders interactive 3D city visualizations of codebases using the Barradeau particle technique. The DENSE + GAP pattern establishes four critical integration layers: type contracts, state boundaries, bridge definitions, and integration logic.

The module operates as the primary visualization engine for Orchestr8, transforming codebase metrics into immersive 3D cityscapes where buildings represent files, height reflects exports, and color indicates status (Gold=working, Teal=broken, Purple=combat). It integrates with `IP/features/code_city/render.py` for Marimo rendering and `IP/static/woven_maps_3d.js` for Three.js visualization.

---

## GAP 1: Type Contracts

### Current Contract Structure

The module implements comprehensive type contracts using `@dataclass` decorators. These define the data structures for nodes, edges, configuration, and neighborhoods:

| Contract | Location | Type | Description |
|----------|----------|------|-------------|
| `CodeNode` | `woven_maps.py:93` | `@dataclass` | Represents a file in the codebase |
| `EdgeData` | `woven_maps.py:143` | `@dataclass` | Import relationship between files |
| `ColorScheme` | `woven_maps.py:179` | `@dataclass` | Color configuration for visualization |
| `GraphConfig` | `woven_maps.py:205` | `@dataclass` | Visualization configuration |
| `Neighborhood` | `woven_maps.py:273` | `@dataclass` | Neighborhood/fiefdom boundary region |
| `GraphData` | `woven_maps.py:303` | `@dataclass` | Complete visualization data package |

### CodeNode Contract Details

The `CodeNode` dataclass is the primary node representation:

```python
@dataclass
class CodeNode:
    path: str
    status: str = "working"  # working | broken | combat
    loc: int = 0
    errors: List[str] = field(default_factory=list)
    health_errors: List[Any] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    node_type: str = "file"  # file|component|store|entry|test|route|api|config|type
    centrality: float = 0.0  # PageRank score (0-1)
    in_cycle: bool = False
    depth: int = 0
    incoming_count: int = 0
    outgoing_count: int = 0
    export_count: int = 0
    building_height: float = BUILDING_HEIGHT_BASE
    footprint: float = BUILDING_FOOTPRINT_BASE
    is_locked: bool = False
    display_zone: str = "city"  # city | town_square | hidden | minimap_only
```

### Required TypedDict Definitions

The current implementation uses `@dataclass` which provides runtime validation but lacks explicit TypedDict variants for stricter static typing. For a_codex_plan integration, the following TypedDict definitions are recommended:

```python
from typing import TypedDict, Literal, NotRequired

class CodeNodeDict(TypedDict):
    """Serialized CodeNode for JSON communication."""
    id: str
    path: str
    status: Literal["working", "broken", "combat"]
    x: float
    y: float
    loc: int
    errors: list[str]
    healthErrors: list[Any]
    nodeType: Literal["file", "component", "store", "entry", "test", "route", "api", "config", "type"]
    centrality: float
    inCycle: bool
    depth: int
    incomingCount: int
    outgoingCount: int
    exportCount: int
    buildingHeight: float
    footprint: float
    isLocked: bool
    displayZone: Literal["city", "town_square", "hidden", "minimap_only"]


class EdgeDataDict(TypedDict):
    """Serialized EdgeData for JSON communication."""
    source: str
    target: str
    resolved: bool
    bidirectional: bool
    lineNumber: int
    fromFiefdom: str
    toFiefdom: str
    isBoundary: bool
    allowedTypes: list[str]
    forbiddenCrossings: list[str]
    contractStatus: Literal["defined", "draft", "missing", ""]


class GraphConfigDict(TypedDict):
    """Serialized GraphConfig for JSON communication."""
    width: int
    height: int
    maxHeight: int
    wireCount: int
    showParticles: bool
    showTooltip: bool
    emergenceDuration: float
    performance: dict
    colors: dict


class NeighborhoodDict(TypedDict):
    """Serialized Neighborhood for JSON communication."""
    name: str
    nodes: list[str]
    centerX: float
    centerY: float
    boundaryPoints: list[dict[str, float]]
    integrationCount: int
    neighbors: list[dict[str, Any]]
    status: Literal["working", "broken", "mixed"]
```

### Color System Contracts

The module defines locked color constants that must not change:

```python
COLORS = {
    "gold_metallic": "#D4AF37",   # Working code
    "blue_dominant": "#1fbdea",   # Broken code / Teal during scan
    "purple_combat": "#9D4EDD",   # Combat (LLM active)
    "bg_primary": "#0A0A0B",      # The Void
    "bg_elevated": "#121214",     # Elevated surfaces
    "gold_dark": "#B8860B",       # Secondary gold
    "gold_saffron": "#F4C430",    # Bright highlights
}

JS_COLORS = {
    "void": "#0A0A0B",
    "working": "#D4AF37",
    "broken": "#1fbdea",
    "combat": "#9D4EDD",
    "wireframe": "#333333",
    "teal": "#1fbdea",
    "gold": "#D4AF37",
    "cycle": "#ff4444",
    "edge": "#333333",
    "edge_broken": "#ff6b6b",
}
```

### Building Geometry Contracts

Locked formulas from canon that govern visual representation:

```python
BUILDING_HEIGHT_BASE = 3.0
BUILDING_HEIGHT_EXPORT_SCALE = 0.8
BUILDING_FOOTPRINT_BASE = 2.0
BUILDING_FOOTPRINT_LOC_SCALE = 0.008

# height = 3 + (exports * 0.8)
# footprint = 2 + (lines * 0.008)
```

---

## GAP 2: State Boundary

### Current State Structure

The `woven_maps.py` module operates as a stateless computation layer. Each public function accepts parameters and produces output without maintaining internal state. However, for reactive integration with Marimo and the broader Orchestr8 system, a component state wrapper is needed:

```python
# Proposed component state structure for wrapper layer
_component_state: dict = {
    "_last_root": None,              # Last scanned project root
    "_last_graph_data": None,       # Cached GraphData
    "_last_render": None,           # Cached Marimo HTML output
    "_health_results": None,        # Current health results
    "_camera_state": None,          # Current camera position
    "_stream_config": None,         # Streaming configuration
    "_selected_node": None,          # Currently selected node
    "_filter_zone": None,            # Current display zone filter
}
```

### State Management Integration

The module currently delegates state management to the calling context in `IP/features/code_city/render.py`:

```python
# From IP/features/code_city/render.py
def create_code_city(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
    health_results: Optional[Dict[str, Any]] = None,
) -> Any:
    # Graph data is computed fresh on each call
    graph_data = build_from_connection_graph(root, ...)
    
    # Health results are merged if provided
    if health_results:
        graph_data.nodes = build_from_health_results(graph_data.nodes, health_results)
    
    # Template substitution for iframe rendering
    iframe_html = load_woven_maps_template().replace("__GRAPH_DATA__", graph_data.to_json())
    
    return mo.Html(f'<iframe srcdoc="{html.escape(iframe_html)}"...')
```

### State Boundary Protocol

For stricter integration with a_codex_plan, a formal state protocol is recommended:

```python
from typing import Protocol, Optional
from pathlib import Path

class WovenMapsStateProtocol(Protocol):
    """Protocol for Woven Maps component state."""
    
    @property
    def graph_data(self) -> GraphData:
        """Current graph data for visualization."""
        ...
    
    @property
    def health_results(self) -> Optional[dict]:
        """Current health results merged into visualization."""
        ...
    
    @property
    def camera_state(self) -> dict:
        """Current camera position and target."""
        ...
    
    @property
    def selected_node(self) -> Optional[str]:
        """Currently selected node path."""
        ...


# Component state initialization
def init_woven_maps_state(
    root: Path,
    health_results: Optional[dict] = None,
) -> dict:
    """Initialize component state for Woven Maps."""
    return {
        "_root": str(root),
        "_graph_data": None,
        "_health_results": health_results,
        "_camera_state": {
            "mode": "overview",
            "position": {"x": 0, "y": 60, "z": 60},
            "target": {"x": 0, "y": 5, "z": 0},
            "zoom": 1.0,
            "return_stack": [],
            "transition_ms": 2000,
            "easing": "cubic",
        },
        "_stream_config": {
            "bps": 5_000_000,
            "inline_building_data": False,
        },
        "_selected_node": None,
        "_filter_zone": "city",
    }
```

---

## GAP 3: Bridge Requirements

### Current Bridge Structure

The module uses an iframe-based bridge for JavaScript communication. The bridge operates through template substitution in `IP/features/code_city/render.py`:

```
woven_maps.py
    |
    +-- build_graph_data() --> GraphData
    +-- create_3d_code_city() --> building_data dict
    |
    v
IP/features/code_city/render.py
    |
    +-- load_woven_maps_template() --> HTML template
    +-- Replace __GRAPH_DATA__, __BUILDING_DATA__, __CAMERA_STATE__
    +-- Inject Three.js, Delaunay, woven_maps_3d.js
    |
    v
mo.Html(<iframe srcdoc=...>)
    |
    v
IP/static/woven_maps_3d.js (CodeCityScene class)
    |
    +-- postMessage communication for node clicks
    +-- Camera state synchronization
    +-- Building selection events
```

### Bridge Payloads

#### GraphData Bridge

The `build_graph_data()` and `build_from_connection_graph()` functions produce a `GraphData` object that serializes to JSON:

| Field | Type | Description |
|-------|------|-------------|
| `nodes` | `List[CodeNodeDict]` | Files in the codebase |
| `edges` | `List[EdgeDataDict]` | Import relationships |
| `config` | `GraphConfigDict` | Visualization settings |
| `neighborhoods` | `List[NeighborhoodDict]` | Fiefdom boundaries |

#### BuildingData Bridge

The `create_3d_code_city()` function produces building geometry data:

```python
{
    "buildings": [
        {
            "path": "IP/woven_maps.py",
            "position": {"x": 0.0, "z": 0.0},
            "height": 10.0,
            "footprint": 3.5,
            "status": "working",
            "color": "#D4AF37",
            "isLocked": False,
        },
        # ... more buildings
    ],
    "metadata": {
        "total_buildings": 150,
        "layout_scale": 10.0,
        "generated_at": "2026-02-16T12:00:00",
    }
}
```

#### CameraState Bridge

Camera state is communicated via `IP/contracts/camera_state.py`:

```python
{
    "mode": "overview",  # overview | street | focus | orbit
    "position": {"x": 0, "y": 60, "z": 60},
    "target": {"x": 0, "y": 5, "z": 0},
    "zoom": 1.0,
    "return_stack": [],
    "transition_ms": 2000,
    "easing": "cubic",
}
```

### postMessage Communication

The JavaScript layer (`IP/static/woven_maps_3d.js`) communicates back to Python via postMessage:

```javascript
// From IP/static/woven_maps_3d.js
class CodeCityScene {
    // Node click event
    onBuildingClick(building) {
        window.parent.postMessage({
            type: "code_city_node_click",
            path: building.path,
            status: building.status,
            position: { x: building.x, z: building.z },
        }, "*");
    }
    
    // Camera state sync
    onCameraChange(camera) {
        window.parent.postMessage({
            type: "code_city_camera_update",
            mode: this.currentMode,
            position: camera.position,
            target: camera.target,
        }, "*");
    }
}
```

### Gap Analysis

| Bridge | Current | Status | Gap |
|--------|---------|--------|-----|
| `GraphData` | `@dataclass` with `to_dict()` | ✅ Stable | No TypedDict variant for JSON schema |
| `BuildingData` | Dict from `create_3d_code_city()` | ✅ Stable | No formal TypedDict |
| `CameraState` | Dict from `get_default_camera_state()` | ✅ Stable | Defined in separate module |
| `postMessage` | Event-based in JS | ⚠️ Partial | No Python handler in current scope |

---

## GAP 4: Integration Logic

### Entry Points

The module provides multiple entry points for different use cases:

| Entry Point | Purpose | Callers |
|-------------|---------|---------|
| `create_code_city()` | Full Marimo rendering | `06_maestro.py` |
| `build_graph_data()` | Basic graph without connection data | Tests, CLI |
| `build_from_connection_graph()` | Full graph with import edges | `render.py` |
| `build_from_health_results()` | Merge health signals into nodes | `render.py` |
| `create_3d_code_city()` | 3D building geometry data | `render.py` (when inlined) |
| `scan_codebase()` | Raw file scanning | `graph_builder.py` |
| `calculate_layout()` | 2D node positioning | `graph_builder.py` |
| `compute_neighborhoods()` | Fiefdom boundary computation | `graph_builder.py` |

### Integration Flow

The primary integration flow for Marimo rendering:

```
User selects project root (06_maestro.py)
    |
    v
create_code_city(root, width, height, max_height, wire_count, health_results)
    |
    +-- build_from_connection_graph(root, ...)
    |       |
    |       +-- scan_codebase(root) --> List[CodeNode]
    |       +-- analyze_file(filepath) --> CodeNode with metrics
    |       +-- calculate_layout(nodes) --> positions
    |       +-- compute_neighborhoods(nodes, edges)
    |       |
    |       v
    |   GraphData with nodes, edges, neighborhoods
    |
    +-- build_from_health_results(nodes, health_results)
    |       |
    |       v
    |   Nodes enriched with health errors
    |
    v
load_woven_maps_template()
    |
    +-- Substitute __GRAPH_DATA__ --> graph_data.to_json()
    +-- Substitute __BUILDING_DATA__ --> building_data_json
    +-- Substitute __CAMERA_STATE__ --> camera_state_json
    +-- Inject JS libraries (Three.js, Delaunay, woven_maps_3d.js)
    |
    v
mo.Html(<iframe srcdoc="{escaped}">)
    |
    v
Browser renders CodeCityScene with Three.js
    |
    v
User clicks building --> postMessage --> Python handler
```

### Configuration Entry Points

The module respects environment variables for runtime configuration:

| Environment Variable | Default | Purpose |
|----------------------|---------|---------|
| `ORCHESTR8_CODE_CITY_MAX_BYTES` | 9,000,000 | Payload size guard |
| `ORCHESTR8_CODE_CITY_STREAM_BPS` | 5,000,000 | 3D building stream rate |
| `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` | false | Legacy inline mode |
| `ORCHESTR8_PATCHBAY_APPLY` | false | Enable patchbay integration |

### Downstream Consumers

| Consumer | Integration Point | Data Used |
|----------|------------------|-----------|
| `06_maestro.py` | `create_code_city()` | Full GraphData |
| `shell.py` | Node click events | Selected node path |
| `code_city_context.py` | Node data | Building panel assembly |
| Health Watcher | `build_from_health_results()` | Health error merging |
| Connection Verifier | `build_from_connection_graph()` | Import edge computation |

### Trigger Types

The visualization supports multiple camera modes triggered by user interaction:

| Trigger | Condition | Use Case |
|---------|-----------|----------|
| `overview` | Default state | City-wide view |
| `street` | Double-click building | Street-level inspection |
| `focus` | Node selection | Focused building view |
| `orbit` | Toggle auto-rotate | Cinematic exploration |

---

## Integration Recommendations

### Recommended Integration Pattern

```python
from pathlib import Path
from IP.woven_maps import (
    create_code_city,
    build_from_connection_graph,
    create_3d_code_city,
)
from IP.contracts.camera_state import get_default_camera_state

# Full rendering integration
def render_code_city(
    project_root: Path,
    health_results: Optional[dict] = None,
    width: int = 800,
    height: int = 600,
) -> Any:
    """Render Woven Maps Code City for Marimo."""
    return create_code_city(
        root=str(project_root),
        width=width,
        height=height,
        max_height=250,
        wire_count=15,
        health_results=health_results,
    )


# Data-only integration for external processing
def get_graph_data(project_root: Path) -> GraphData:
    """Get graph data without rendering."""
    return build_from_connection_graph(
        project_root=str(project_root),
        width=800,
        height=600,
        max_height=250,
        wire_count=15,
    )


# 3D building data for custom rendering
def get_building_geometry(project_root: Path) -> dict:
    """Get 3D building geometry for custom visualization."""
    graph_data = build_from_connection_graph(str(project_root))
    return create_3d_code_city(graph_data, layout_scale=10.0)
```

### Component State Wrapper

For reactive state management:

```python
import marimo as mo

# State management for Woven Maps
get_woven_maps_state, set_woven_maps_state = mo.state({
    "graph_data": None,
    "health_results": None,
    "selected_node": None,
    "camera_mode": "overview",
    "render_config": {
        "width": 800,
        "height": 600,
        "max_height": 250,
        "wire_count": 15,
    },
})


def update_woven_maps(
    project_root: str,
    health_results: Optional[dict] = None,
) -> dict:
    """Update Woven Maps state and return render."""
    graph_data = build_from_connection_graph(project_root)
    
    if health_results:
        graph_data.nodes = build_from_health_results(
            graph_data.nodes, 
            health_results
        )
    
    current_state = get_woven_maps_state()
    new_state = {
        **current_state,
        "graph_data": graph_data,
        "health_results": health_results,
    }
    set_woven_maps_state(new_state)
    
    return create_code_city(
        root=project_root,
        health_results=health_results,
    )
```

---

## Dependencies

### Internal Dependencies

| Module | Purpose |
|--------|---------|
| `IP/features/code_city/render.py` | Marimo rendering assembly |
| `IP/features/code_city/graph_builder.py` | Graph computation |
| `IP/features/code_city/assets.py` | Template loading |
| `IP/contracts/camera_state.py` | Camera state contract |
| `IP/contracts/status_merge_policy.py` | Health status merging |
| `IP/contracts/town_square_classification.py` | File classification (optional) |
| `IP/audio/config.py` | Audio FFT configuration |
| `IP/static/woven_maps_3d.js` | Three.js visualization |
| `Barradeau/woven_map/delaunay.js` | Delaunay triangulation |
| `Barradeau/FBO-master/vendor/three.min.js` | Three.js core |
| `Barradeau/FBO-master/vendor/OrbitControls.js` | Camera controls |

### External Dependencies

| Package | Purpose |
|---------|---------|
| `marimo` | Reactive notebook runtime |
| `pandas` | Data manipulation |
| `networkx` | Graph algorithms |
| `jinja2` | Template processing |

### Standard Library

| Module | Usage |
|--------|-------|
| `json` | Serialization |
| `html` | HTML escaping |
| `math` | Layout calculations |
| `os` | Path operations |
| `re` | Pattern matching |
| `ast` | Python source parsing |
| `fnmatch` | File pattern matching |
| `pathlib` | Path manipulation |
| `datetime` | Timestamps |

---

## Testing Coverage

The module includes tests in `IP/features/code_city/tests/`:

| Test | Coverage |
|------|----------|
| `test_health_flow` | Health result merging |
| `test_code_city_context` | Context assembly (integration) |

### Manual Testing Checklist

- [ ] Scan a Python project and verify node count
- [ ] Verify building heights match export counts
- [ ] Verify building footprints match line counts
- [ ] Test color coding: gold (working), teal (broken), purple (combat)
- [ ] Verify emergence animation plays on load
- [ ] Test camera transitions between modes
- [ ] Test node click produces postMessage
- [ ] Verify large codebase performance (payload guard)
- [ ] Test town square zone classification
- [ ] Verify health errors merge correctly

---

## Summary

| GAP | Current State | Gap | Recommendation |
|-----|---------------|-----|----------------|
| **Type Contracts** | `@dataclass` in `woven_maps.py` | No TypedDict variants | Add TypedDict for JSON schema clarity |
| **State Boundary** | Stateless, delegated to caller | No formal component state | Define `_component_state` wrapper |
| **Bridge** | Iframe template substitution | postMessage handler not in module scope | Document Python handler contract |
| **Integration Logic** | Entry points stable and well-defined | Environment variable coupling | Formalize config injection |

The module is well-structured for integration with canonical type contracts, stable entry points, and clear separation between data computation and rendering. The primary gaps are formal TypedDict definitions for JSON communication and a component state wrapper for reactive Marimo integration. The bridge is partially implemented through iframe template substitution; the missing piece is the Python-side postMessage handler for node click events.

---

## Visual Contract Reference

The visualization follows the Orchestr8 visual contract from the SOT.md:

- **Gold (#D4AF37)**: Working code - buildings glow with metallic gold
- **Teal (#1fbdea)**: During scan - buildings pulse teal before emergence
- **Purple (#9D4EDD)**: Combat - LLM-active files glow purple
- **Void (#0A0A0B)**: Background - buildings emerge from darkness
- **Emergence**: Particles coalesce from chaos, buildings materialize from particles
- **No breathing**: Static geometry after emergence (no pulsing animations)

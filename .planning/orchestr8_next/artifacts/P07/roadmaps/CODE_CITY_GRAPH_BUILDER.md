# Code City Graph Builder — Deep Analysis

**Source:** `IP/features/code_city/graph_builder.py`  
**Target:** `a_codex_plan`  
**Purpose:** Builds the node/edge data structure for Code City visualization  
**Date:** 2026-02-16

---

## 1. Overview

The GraphBuilder module (`graph_builder.py`) is the central transformer that converts raw codebase analysis into the graph data structure consumed by WovenMaps for 3D Code City visualization. It serves as the orchestration layer that:

1. **Aggregates** inputs from multiple analyzers (ConnectionVerifier, CombatTracker, LouisWarden, HealthChecker)
2. **Transforms** raw file analysis into visual primitives (nodes with geometry, edges with contracts)
3. **Computes** neighborhood boundaries from directory structure
4. **Emits** a complete `GraphData` object ready for WovenMaps rendering

---

## 2. Input Sources

The GraphBuilder integrates data from four primary sources:

### 2.1 ConnectionVerifier (`IP.connection_verifier`)

**Function:** `build_connection_graph(project_root) -> ConnectionGraph`

| Input Field | Type | Description |
|-------------|------|-------------|
| `nodes[].filePath` | string | Relative path to source file |
| `nodes[].type` | NodeType enum | File classification (file, component, store, route, etc.) |
| `nodes[].status` | string | "error" flag for broken imports |
| `nodes[].metrics` | ConnectionMetrics | Centrality, in_cycle, depth, issueCount, incomingCount, outgoingCount |
| `edges[].source` | string | Importing file path |
| `edges[].target` | string | Imported file path |
| `edges[].resolved` | boolean | Whether import resolves to real file |
| `edges[].bidirectional` | boolean | Mutual import flag |
| `edges[].lineNumber` | int | Source line of import statement |

**Status Derivation:** If `node_data.get("status") == "error"` OR `metrics.get("issueCount", 0) > 0`, node is marked as "broken".

### 2.2 CombatTracker (`IP.combat_tracker`)

**Function:** `CombatTracker(root).get_combat_files() -> Set[str]`

| Input Field | Type | Description |
|-------------|------|-------------|
| `combat_files` | Set[str] | File paths currently under LLM editing |

**Effect:** Any node whose `path` is in `combat_files` gets its status overridden to "combat" (highest precedence).

### 2.3 LouisWarden (`IP.louis_core`)

**Function:** `LouisWarden(config).is_locked(file_path) -> bool`

| Input Field | Type | Description |
|-------------|------|-------------|
| `is_locked` | boolean | Whether file is protected/locked by Louis |

**Effect:** Sets `node.is_locked = True` for protected files. These render with a special visual indicator in the Code City.

### 2.4 HealthChecker Results (`IP.health_checker`)

**Function:** `build_from_health_results(nodes, health_results)`

| Input Field | Type | Description |
|-------------|------|-------------|
| `health_results` | Dict[str, Any] | Mapping of file paths to health check results |
| `result.status` | string | Health status (working, broken, etc.) |
| `result.errors` | List | Structured error list |

**Merge Behavior:** Uses `merge_status(node.status, health_status)` to combine existing status with health check status, applying canonical precedence.

### 2.5 Settlement Survey (Boundary Contracts)

**Function:** `parse_settlement_survey(survey_data)`

| Input Field | Type | Description |
|-------------|------|-------------|
| `boundary_contracts[].from_fiefdom` | string | Source fiefdom |
| `boundary_contracts[].to_fiefdom` | string | Target fiefdom |
| `boundary_contracts[].allowed_types` | List[str] | e.g., ["imports", "calls"] |
| `boundary_contracts[].forbidden_crossings` | List[str] | e.g., ["cyclic_imports"] |
| `boundary_contracts[].contract_status` | string | "defined", "draft", "missing" |

**Search Paths:** 
- `.settlement/survey.json`
- `.planning/survey.json`
- `settlement_survey.json`

---

## 3. Node Generation

### 3.1 Building Height Formula

```
height = 3.0 + (export_count * 0.8)
```

| Parameter | Value | Source |
|-----------|-------|--------|
| `BUILDING_HEIGHT_BASE` | 3.0 | Minimum building height |
| `BUILDING_HEIGHT_EXPORT_SCALE` | 0.8 | Scaling factor per export |

**Rationale:** Exports (public functions/classes) indicate module complexity. More exports = taller building = more surface area for the 3D mesh.

### 3.2 Footprint Formula

```
footprint = 2.0 + (lines_of_code * 0.008)
```

| Parameter | Value | Source |
|-----------|-------|--------|
| `BUILDING_FOOTPRINT_BASE` | 2.0 | Minimum footprint |
| `BUILDING_FOOTPRINT_LOC_SCALE` | 0.008 | Scaling factor per LOC |

**Rationale:** File size correlates with visual weight. Small files cluster tightly; large files spread out.

### 3.3 Export Counting Strategies

| Language | Detection Pattern |
|----------|-------------------|
| Python | `ast.FunctionDef`, `ast.AsyncFunctionDef`, `ast.ClassDef` (excludes `_` prefix) |
| JS/TS/Vue | `export ...`, `module.exports =`, `exports.X =` |
| Other | Returns 0 exports |

### 3.4 Display Zone Classification

Files route to different visual zones:

| Zone | Description | Examples |
|------|-------------|----------|
| `city` | Main Code City (default) | Source files |
| `town_square` | Infrastructure/config | `pyproject.toml`, `Dockerfile`, README |
| `hidden` | Excluded from view | `.env`, `*.pyc`, `node_modules` |
| `minimap_only` | Minimap only | `*.md`, `*.svg`, static assets |

### 3.5 Node Data Structure

```python
@dataclass
class CodeNode:
    path: str                           # File path
    status: str = "working"             # working | broken | combat
    loc: int = 0                        # Lines of code
    errors: List[str] = []              # Parsing/TODO/FIXME errors
    health_errors: List[Dict] = []      # Structured health check errors
    x: float = 0.0                      # 2D layout X position
    y: float = 0.0                      # 2D layout Y position
    node_type: str = "file"             # file|component|store|entry|test|route|api|config|type
    centrality: float = 0.0             # PageRank score (0-1)
    in_cycle: bool = False              # Circular dependency flag
    depth: int = 0                      # Distance from entry points
    incoming_count: int = 0             # Files importing this
    outgoing_count: int = 0             # Files this imports
    export_count: int = 0               # Public symbol count
    building_height: float = 3.0        # Computed height
    footprint: float = 2.0              # Computed footprint
    is_locked: bool = False             # Louis lock status
    display_zone: str = "city"          # Rendering zone
```

---

## 4. Edge Generation

### 4.1 Fiefdom Boundary Detection

```python
def _extract_fiefdom(file_path: str) -> str:
    """Extract fiefdom name (first directory component)."""
    parts = Path(file_path).parts
    if len(parts) >= 2:
        return parts[0]
    return ""
```

**Boundary Crossing:** An edge crosses a fiefdom boundary if:
- `from_fiefdom` != `to_fiefdom`
- Both fiefdoms are non-empty

### 4.2 Edge Data Structure

```python
@dataclass
class EdgeData:
    source: str                         # Importer file path
    target: str                         # Imported file path
    resolved: bool = True               # Import resolves?
    bidirectional: bool = False        # Mutual import?
    line_number: int = 0               # Source line
    from_fiefdom: str = ""              # Source fiefdom
    to_fiefdom: str = ""                # Target fiefdom
    is_boundary: bool = False           # Crosses fiefdom?
    allowed_types: List[str] = []       # Contract-allowed types
    forbidden_crossings: List[str] = [] # Contract-forbidden patterns
    contract_status: str = ""            # "defined" | "draft" | "missing"
```

### 4.3 Contract Resolution

For boundary edges, the GraphBuilder looks up the corresponding contract in `boundary_contracts_map`:

```python
if is_boundary:
    contract = boundary_contracts_map.get((from_fiefdom, to_fiefdom))
    if contract:
        allowed_types = contract["allowed_types"]
        forbidden_crossings = contract["forbidden_crossings"]
        contract_status = contract["contract_status"]
    else:
        contract_status = "missing"
```

This enables visualization of:
- **Valid crossings** (gold wires)
- **Contract violations** (warning indicators)
- **Undefined boundaries** (missing contracts highlighted)

---

## 5. Status Precedence

### 5.1 Canonical Merge Policy

The system uses **priority-based merging** with this exact precedence:

| Priority | Status | Numeric Value | Meaning |
|----------|--------|---------------|---------|
| 3 (highest) | `combat` | 3 | LLM actively editing |
| 2 | `broken` | 2 | Import errors, health failures |
| 1 (lowest) | `working` | 1 | All checks pass |

### 5.2 Merge Function

```python
STATUS_PRIORITY = {
    "combat": 3,
    "broken": 2,
    "working": 1,
}

def merge_status(*statuses) -> StatusType:
    """combat > broken > working"""
    if not statuses:
        return "working"
    valid = [s for s in statuses if s is not None]
    if not valid:
        return "working"
    return max(valid, key=lambda s: STATUS_PRIORITY[s])
```

### 5.3 Visual Color Mapping

| Status | Hex Color | Description |
|--------|-----------|--------------|
| `working` | `#D4AF37` (Gold) | All imports resolve |
| `broken` | `#1fbdea` (Teal/Blue) | Has errors |
| `combat` | `#9D4EDD` (Purple) | LLM deployed |

### 5.4 Neighborhood Status Aggregation

Neighborhoods (directories) aggregate node statuses:

```python
status_counts = {"working": 0, "broken": 0, "combat": 0}
for node in dir_nodes:
    if node.status in status_counts:
        status_counts[node.status] += 1

# Combat dominates, then broken, else working
if status_counts["combat"] > 0:
    status = "broken"  # Note: combat nodes are marked broken in neighborhoods
elif status_counts["broken"] > status_counts["working"]:
    status = "broken"
else:
    status = "working"
```

**Note:** The CLAUDE.md specifies combat should take precedence, but the current neighborhood aggregation marks combat neighborhoods as "broken" (not carrying the purple status). This may be an inconsistency worth addressing.

---

## 6. Output Format for WovenMaps

### 6.1 GraphData Structure

```python
@dataclass
class GraphData:
    nodes: List[CodeNode]           # All file nodes
    edges: List[EdgeData]           # All import edges
    config: GraphConfig             # Rendering configuration
    neighborhoods: List[Neighborhood] # Directory boundaries

@dataclass
class GraphConfig:
    width: int = 800                # Canvas width
    height: int = 600               # Canvas height
    max_height: int = 250           # Building height cap
    wire_count: int = 15            # Wireframe layers
    show_particles: bool = True     # Emergence particles
    show_tooltip: bool = True       # Hover tooltips
    emergence_duration: float = 2.5 # Animation duration
    # Performance tuning
    particle_cpu_cap: int = 180000
    particle_gpu_target_cap: int = 1_000_000
    emergence_frame_spawn_cap: int = 700
    error_frame_spawn_cap: int = 280
    mesh_layer_cap: int = 18
    mesh_gradient_height_cap: int = 340
    edge_stride: int = 1
    audio_fft_size: int = 256
    audio_smoothing: float = 0.8
    colors: ColorScheme

@dataclass
class Neighborhood:
    name: str                       # Directory path
    nodes: List[str]                # File paths in this neighborhood
    center_x: float                 # Centroid X
    center_y: float                 # Centroid Y
    boundary_points: List[Dict]    # Polygon vertices
    integration_count: int          # Edges crossing to other neighborhoods
    neighbors: List[Dict]           # Neighbor directory + crossing count
    status: str                     # aggregated status
```

### 6.2 Serialization

GraphData serializes to JSON for frontend consumption:

```python
def to_json(self) -> str:
    return json.dumps({
        "nodes": [n.to_dict() for n in self.nodes],
        "edges": [e.to_dict() for e in self.edges],
        "config": self.config.to_dict(),
        "neighborhoods": [n.to_dict() for n in self.neighborhoods],
    })
```

### 6.3 3D Building Generation

The WovenMaps module transforms GraphData into 3D buildings via `generate_barradeau_buildings()`:

```python
def generate_barradeau_buildings(graph_data, layout_scale=10.0):
    buildings = []
    for node in graph_data.nodes:
        position = {"x": node.x * layout_scale, "z": node.y * layout_scale}
        building = BarradeauBuilding(
            path=node.path,
            line_count=node.loc,
            export_count=node.export_count,
            status=node.status,
            position=position,
            is_locked=node.is_locked,
        )
        buildings.append(building.get_building_data())
    return buildings
```

---

## 7. Layout Algorithm

### 7.1 Directory-Based Grid Layout

1. **Group by directory:** Nodes are grouped by parent directory
2. **Grid cells:** Each directory gets a grid cell based on `sqrt(dir_count)`
3. **Radial distribution:** Within each directory, files are distributed in a circle:
   - Angle = `(index / total) * 2 * PI - PI/2`
   - Radius scales with `footprint` (larger files push outward)
   - Jitter added to prevent overlap: `±10px`

### 7.2 Position Clamping

All coordinates are clamped to canvas bounds:
```python
node.x = max(padding, min(width - padding, node.x))
node.y = max(padding, min(height - padding, node.y))
```

---

## 8. Integration Points

### 8.1 Primary Entry Points

| Function | Purpose |
|----------|---------|
| `build_graph_data()` | Simple standalone graph (no ConnectionGraph) |
| `build_from_connection_graph()` | Full graph with import relationships |
| `build_from_health_results()` | Merge health check results into existing nodes |

### 8.2 Compatibility Wrappers

The `woven_maps.py` module re-exports GraphBuilder functions as compatibility wrappers:

```python
# woven_maps.py
def build_from_connection_graph(...):
    from IP.features.code_city.graph_builder import (
        build_from_connection_graph as _build_from_connection_graph,
    )
    return _build_from_connection_graph(...)
```

This allows both import paths to work:
- `from IP.woven_maps import build_from_connection_graph`
- `from IP.features.code_city.graph_builder import build_from_connection_graph`

---

## 9. Key Observations

### 9.1 Strengths

1. **Multi-source aggregation:** Clean integration of four independent analyzers
2. **Canonical status system:** Clear precedence rules with `merge_status()`
3. **Contract-aware edges:** Boundary contracts enable violation detection
4. **Fiefdom extraction:** First-directory-component is a simple but effective fiefdom strategy

### 9.2 Potential Issues

1. **Neighborhood status anomaly:** Combat nodes in neighborhoods are aggregated to "broken" rather than "combat" - this may mask active LLM work in directory-level views
2. **Fiefdom boundary fragility:** Using only first directory component (`parts[0]`) may miss nested fiefdoms (e.g., `IP/features/code_city` collapses to just `IP`)
3. **Health result matching:** The path matching uses substring/infix matching which could cause false positives:
   ```python
   if path in node.path or node.path.startswith(path.rstrip("/"))
   ```
4. **Missing edge pruning:** The `build_from_connection_graph` function doesn't limit edge count, which could cause performance issues on large codebases

### 9.3 Performance Considerations

- `wire_count` parameter (default 15) controls wireframe layers but edges are not currently filtered
- `max_height` (default 250) caps building height but doesn't reduce vertex count
- The layout algorithm is O(n) but includes hash-based jitter calculations

---

## 10. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     ConnectionVerifier                          │
│                 build_connection_graph(root)                     │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────────┐                        │
│              │   ConnectionGraph        │                        │
│              │   - nodes[] (w/ metrics) │                        │
│              │   - edges[]              │                        │
│              └─────────────────────────┘                        │
│                         │                                        │
│            ┌────────────┼────────────┐                           │
│            ▼            ▼            ▼                           │
│     ┌───────────┐ ┌───────────┐ ┌────────────┐                   │
│     │CombatTrack│ │LouisWarden│ │Settlement  │                   │
│     │-combat_   │ │-is_locked │ │-contracts  │                   │
│     │  files   │ │           │ │            │                   │
│     └───────────┘ └───────────┘ └────────────┘                   │
│            │            │            │                           │
│            └────────────┼────────────┘                           │
│                         ▼                                        │
│              ┌─────────────────────────┐                        │
│              │    GraphBuilder         │                        │
│              │  build_from_connection  │                        │
│              │       _graph()          │                        │
│              └─────────────────────────┘                        │
│                         │                                        │
│            ┌────────────┼────────────┐                           │
│            ▼            ▼            ▼                           │
│     ┌───────────┐ ┌───────────┐ ┌────────────┐                   │
│     │ CodeNodes │ │ EdgeData │ │Neighborhood│                   │
│     │ -status  │ │ -fiefdom │ │  -boundary │                   │
│     │ -geometry│ │ -contract│ │    -status │                   │
│     └───────────┘ └───────────┘ └────────────┘                   │
│            │            │            │                           │
│            └────────────┼────────────┘                           │
│                         ▼                                        │
│              ┌─────────────────────────┐                        │
│              │      GraphData          │                        │
│              │  (nodes + edges +       │                        │
│              │   config + neighborhoods│                        │
│              └─────────────────────────┘                        │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────────┐                        │
│              │      WovenMaps          │                        │
│              │  - 3D buildings         │                        │
│              │  - Emergence particles  │                        │
│              │  - Wireframe layers     │                        │
│              └─────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Dependencies Summary

| Module | Purpose |
|--------|---------|
| `IP.contracts.status_merge_policy` | `merge_status()` for precedence |
| `IP.connection_verifier` | `build_connection_graph()` for import analysis |
| `IP.combat_tracker` | `CombatTracker` for LLM deployment status |
| `IP.louis_core` | `LouisWarden` for file locking |
| `IP.contracts.settlement_survey` | `parse_settlement_survey()` for boundary contracts |
| `IP.woven_maps` | Output data structures (`CodeNode`, `EdgeData`, `GraphData`, `GraphConfig`, `Neighborhood`) |
| `pathlib.Path` | Path manipulation |
| `json` | Serialization |

---

## 12. Related Artifacts

| Document | Relationship |
|----------|--------------|
| `INTEGRATION_connection_verifier.md` | Input source for import graph |
| `INTEGRATION_combat_tracker.md` | Input source for combat status |
| `INTEGRATION_louis_core.md` | Input source for file locking |
| `INTEGRATION_health_checker.md` | Optional health result injection |
| `INTEGRATION_contracts.md` | Boundary contract schema |
| `INTEGRATION_woven_maps.md` | Rendering consumer of GraphData |

---

*Analysis complete. GraphBuilder is the central transformer that unifies multi-source analysis into WovenMaps-consumable graph data.*

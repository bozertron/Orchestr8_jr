# ANALYSIS: Woven Maps Config

**Source:** `/home/bozertron/Orchestr8_jr/IP/woven_maps.py`
**Analysis Date:** 2026-02-16
**Agent:** A-6 (Analysis Agent)

---

## 1. What Configuration Does This Provide?

### 1.1 Color System (Visual State Tokens)

The configuration defines a **three-state color system** aligned with Orchestr8's visual language:

| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| Working | Gold Metallic | `#D4AF37` | All imports resolve, code is healthy |
| Broken | Blue Dominant | `#1fbdea` | Has errors / Teal during scan |
| Combat | Purple Combat | `#9D4EDD` | LLM deployed / active |

Additional palette:
- `bg_primary` / `void`: `#0A0A0B` - The Void (ground state)
- `bg_elevated` / `surface`: `#121214` - Elevated surfaces
- `gold_dark`: `#B8860B` - Secondary gold
- `gold_saffron`: `#F4C430` - Bright highlights

### 1.2 Building Geometry Formulas (Locked)

Canonical formulas from lines 79-85:
```
height = 3 + (exports × 0.8)
footprint = 2 + (lines × 0.008)
```

- **Height base:** 3.0 units
- **Export scale:** 0.8 per export
- **Footprint base:** 2.0 units  
- **LOC scale:** 0.008 per line

### 1.3 Graph Visualization Config

`GraphConfig` dataclass (lines 205-269):
- Canvas dimensions: `width` × `height`
- `max_height`: 250 (cityscape silhouette)
- `wire_count`: 15 layers for richness
- `emergence_duration`: 2.5s animation

### 1.4 Performance Tuning (Hardware-Specific)

Performance profile for Dell Precision 7710 + Quadro M5000M:
- `particle_cpu_cap`: 180,000 particles
- `particle_gpu_target_cap`: 1,000,000 particles
- `emergence_frame_spawn_cap`: 700/frame
- `error_frame_spawn_cap`: 280/frame
- `mesh_layer_cap`: 18 layers
- `mesh_gradient_height_cap`: 340

### 1.5 Audio Configuration

Imports from `IP.audio.config`:
- `DEFAULT_FFT_SIZE`: FFT window size
- `DEFAULT_SMOOTHING`: Audio smoothing factor
- `get_all_bands()`: Frequency band definitions

### 1.6 Display Zone Classification

Files are routed to zones based on pattern matching (lines 384-475):

| Zone | Files | Examples |
|------|-------|----------|
| `city` | Default | Source code files |
| `town_square` | Infrastructure | configs, build files, README |
| `hidden` | Secrets | .env*, *.pyc, node_modules |
| `minimap_only` | Assets | *.md, *.svg, static/** |

---

## 2. Data Structures Defined

### 2.1 CodeNode (lines 92-140)

Represents a single file in the codebase:

```python
@dataclass
class CodeNode:
    path: str                          # File path
    status: str                        # "working" | "broken" | "combat"
    loc: int                           # Lines of code
    errors: List[str]                  # Error messages
    health_errors: List[Any]           # Structured health check errors
    x: float                           # 2D canvas X position
    y: float                           # 2D canvas Y position
    node_type: str                     # file|component|store|entry|test|route|api|config|type
    centrality: float                  # PageRank score (0-1)
    in_cycle: bool                     # Circular dependency flag
    depth: int                         # Distance from entry points
    incoming_count: int               # Files importing this
    outgoing_count: int               # Files this imports
    export_count: int                  # Public/exported symbols
    building_height: float             # Computed height
    footprint: float                  # Computed footprint
    is_locked: bool                    # Louis lock status
    display_zone: str                  # city|town_square|hidden|minimap_only
```

### 2.2 EdgeData (lines 142-176)

Represents import relationships:

```python
@dataclass
class EdgeData:
    source: str                        # Importer file path
    target: str                        # Imported file path
    resolved: bool                     # Import resolution status
    bidirectional: bool                # Mutual import flag
    line_number: int                   # Source line of import
    from_fiefdom: str                  # Source fiefdom
    to_fiefdom: str                    # Target fiefdom
    is_boundary: bool                  # Crosses fiefdom boundary
    allowed_types: List[str]           # e.g., ["imports", "calls"]
    forbidden_crossings: List[str]     # e.g., ["cyclic_imports"]
    contract_status: str               # "defined"|"draft"|"missing"
```

### 2.3 ColorScheme (lines 178-202)

Maps status to visual tokens:

```python
@dataclass
class ColorScheme:
    working: str                      # Gold
    broken: str                        # Blue/Teal
    combat: str                        # Purple
    void: str                          # Background
    surface: str                      # Elevated surfaces
    frame_scanning: str                # Teal (during scan)
    frame_complete: str                # Gold (when complete)
```

### 2.4 GraphConfig (lines 204-269)

Visualization parameters with validation:

```python
@dataclass
class GraphConfig:
    width: int
    height: int
    max_height: int                    # 250
    wire_count: int                    # 15
    show_particles: bool
    show_tooltip: bool
    emergence_duration: float          # 2.5s
    # Performance caps (CPU/GPU)
    particle_cpu_cap: int              # 180000
    particle_gpu_target_cap: int       # 1000000
    emergence_frame_spawn_cap: int     # 700
    error_frame_spawn_cap: int         # 280
    mesh_layer_cap: int                # 18
    mesh_gradient_height_cap: int      # 340
    edge_stride: int
    audio_fft_size: int                # Power of 2, 64-4096
    audio_smoothing: float              # 0.0-1.0
    colors: ColorScheme
```

### 2.5 Neighborhood (lines 272-299)

Represents fiefdom boundaries:

```python
@dataclass
class Neighborhood:
    name: str                          # Directory path
    nodes: List[str]                   # File paths in neighborhood
    center_x: float
    center_y: float
    boundary_points: List[Dict]        # 2D canvas polygon
    integration_count: int             # Edges to other neighborhoods
    neighbors: List[Dict]              # Neighbor neighborhoods
    status: str                        # "working"|"broken"|"mixed"
```

### 2.6 GraphData (lines 302-321)

Complete visualization package:

```python
@dataclass
class GraphData:
    nodes: List[CodeNode]
    edges: List[EdgeData]
    config: GraphConfig
    neighborhoods: List[Neighborhood]
```

---

## 3. How Does It Connect to Visual Tokens?

### 3.1 Status → Color Mapping

The three-state system flows through the entire visualization:

1. **CodeNode.status** drives building color
2. **ColorScheme** provides the hex values
3. **JS_COLORS** provides JavaScript-compatible names for frontend

```
CodeNode("working") → gold_metallic (#D4AF37)
CodeNode("broken")  → blue_dominant (#1fbdea)
CodeNode("combat")  → purple_combat  (#9D4EDD)
```

### 3.2 Frame Color Transition

Special animation state (lines 188-190):
- `frame_scanning`: Teal (`#1fbdea`) during Code City scan
- `frame_complete`: Gold (`#D4AF37`) when scan completes

This creates the Teal → Gold frame transition mentioned in the docstring.

### 3.3 Building Geometry → 3D Rendering

The `compute_building_geometry()` function (lines 534-540):
- Takes `lines` (LOC) and `exports` (public symbols)
- Returns `(height, footprint)` tuple
- Used by `generate_barradeau_buildings()` for 3D building generation

### 3.4 Display Zone → File Routing

`get_display_zone()` (lines 478-504) determines:
- Which files appear in main city
- Which go to "town square" (infrastructure)
- Which are hidden (secrets/build artifacts)
- Which appear only in minimap

### 3.5 Fiefdom Boundaries → Edge Styling

`EdgeData.is_boundary` and `contract_status` enable:
- Visual differentiation of cross-fiefdom imports
- Contract-aware edge rendering (defined/draft/missing)

---

## 4. Integration into a_codex_plan

### 4.1 Data Flow Architecture

```
a_codex_plan
    ↓ (code analysis)
IP/woven_maps.py (config + structures)
    ↓ (GraphData)
IP/features/code_city/graph_builder.py
    ↓ (JSON)
IP/static/woven_maps_3d.js
    ↓ (render)
Code City Visualization
```

### 4.2 Key Entry Points for Integration

1. **scan_codebase()** (lines 606-644)
   - Scans directory tree
   - Returns `List[CodeNode]`
   - Skips: node_modules, .git, __pycache__, etc.

2. **build_graph_data()** (lines 774-792)
   - Compatibility wrapper
   - Returns complete `GraphData`

3. **build_from_connection_graph()** (lines 795-813)
   - Uses ConnectionGraph integration
   - Includes fiefdom metadata

4. **create_3d_code_city()** (lines 871-894)
   - Generates 3D building data
   - Returns package for frontend

### 4.3 Required Dependencies

- `IP.contracts.status_merge_policy.merge_status`
- `IP.features.code_city.assets.load_woven_maps_template`
- `IP.audio.config.*`
- `IP.contracts.town_square_classification` (optional)

### 4.4 Extending for a_codex_plan

To integrate with a_codex_plan's temporal state:

1. **Add temporal fields to CodeNode:**
   ```python
   last_analyzed: datetime
   change_frequency: float
   stability_score: float
   ```

2. **Add temporal edge data:**
   ```python
   last_import_change: datetime
   import_trend: str  # increasing|decreasing|stable
   ```

3. **Visual token extensions:**
   - Add `aging` status for stale files
   - Add `volatile` token for frequently-changing code

---

## 5. Summary

**Woven Maps Config provides:**

| Category | Elements |
|----------|----------|
| **Colors** | 3-state system (gold/blue/purple) + Void palette |
| **Geometry** | Locked formulas for building height/footprint |
| **Zones** | 4-tier display routing (city/town_square/hidden/minimap) |
| **Performance** | Hardware-tuned particle/mesh caps |
| **Audio** | FFT configuration for reactive visualization |
| **Data Structures** | CodeNode, EdgeData, GraphConfig, Neighborhood, GraphData |

**Visual token connection:**
- Status field drives all color choices
- Export count + LOC drives building geometry
- Fiefdom metadata drives edge styling
- Display zone drives file placement

**a_codex_plan integration point:**
- Primary: `GraphData` as the data contract
- Entry: `build_from_connection_graph()` for fiefdom-aware analysis
- Extension point: Add temporal fields to CodeNode/EdgeData for time-series visualization

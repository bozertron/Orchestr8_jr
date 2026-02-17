# ANALYSIS: Code City Render

**Source:** `/home/bozertron/Orchestr8_jr/IP/features/code_city/render.py`
**Date:** 2026-02-16
**Agent:** A-5 (Analysis Agent)

---

## 1. Function Overview

### Primary Function: `create_code_city()`

**Location:** `IP/features/code_city/render.py:23-161`

**Purpose:** Creates a Woven Maps Code City visualization embedded in a Marimo HTML iframe.

**Signature:**
```python
def create_code_city(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
    health_results: Optional[Dict[str, Any]] = None,
) -> Any
```

**Returns:** `mo.Html` (Marimo HTML component)

### Data Flow Pipeline

```
root directory
    ↓
build_from_connection_graph() / build_graph_data()
    ↓ (GraphData with nodes, edges, neighborhoods)
build_from_health_results() [optional]
    ↓
create_3d_code_city() [conditional]
    ↓
load_woven_maps_template() → inject graph_data, building_data
    ↓
mo.Html(<iframe srcdoc=...>)
```

---

## 2. Marimo Integration

### Entry Point Chain

| File | Function | Role |
|------|----------|------|
| `orchestr8.py` | Entry point | Loads `06_maestro.py` |
| `IP/plugins/06_maestro.py:1175` | `create_code_city()` | Called from Maestro render |
| `IP/woven_maps.py:911` | `create_code_city()` | Compatibility wrapper |
| `IP/features/code_city/render.py:23` | `create_code_city()` | **Implementation** |

### State Dependencies

The function is called within `06_maestro.py` `render()` function and requires:
- `root` - Project root path from `STATE_MANAGERS["root"]`
- `health_results` - Health check results from `STATE_MANAGERS["health"]`

### Payload Size Guard

**Location:** `06_maestro.py:1178-1212`

The Maestro plugin implements a critical guard:
1. Measures rendered payload bytes via `_payload_size_bytes(result)`
2. Default limit: `9,000,000` bytes (configurable via `ORCHESTR8_CODE_CITY_MAX_BYTES`)
3. Fallback: If root payload too large, retries with `IP/` subroot
4. Final fallback: Displays warning panel if still oversized

---

## 3. 2D/3D Connections

### Dual Rendering Mode

The system supports two rendering modes controlled by environment variable:

| Mode | Env Var | Behavior |
|------|---------|----------|
| **2D (Default)** | `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` not set | Buildings generated client-side from graph nodes |
| **3D (Legacy)** | `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA=1` | Full 3D data pre-computed and inlined |

### 2D Path (Current Default)

```
IP/features/code_city/render.py
    ↓
graph_data.to_json() → __GRAPH_DATA__ placeholder
    ↓
building_data_json = "null" (no pre-computed 3D)
    ↓
IP/static/woven_maps_3d.js
    ↓
CodeCityScene class generates buildings client-side
    ↓
Stream budget: ORCHESTR8_CODE_CITY_STREAM_BPS (default: 5,000,000 bps)
```

### 3D Path (Legacy)

```
IP/features/code_city/render.py:74-80
    ↓
if inline_building_data:
    building_data = wm.create_3d_code_city(graph_data, layout_scale=10.0)
    building_data_json = json.dumps(building_data)
    ↓
Full 3D building arrays inlined into iframe srcdoc
```

### Stream Budget Control

**Environment Variable:** `ORCHESTR8_CODE_CITY_STREAM_BPS`
- **Default:** `5,000,000` bytes/sec
- **Minimum:** `100,000` bytes/sec
- **Purpose:** Controls progressive 3D building streaming to prevent overwhelming the browser

---

## 4. Wiring & Integration

### External Dependencies

| Dependency | Source | Purpose |
|------------|--------|---------|
| **marimo** | `import marimo as mo` | UI framework |
| **graph_builder** | `IP.features.code_city.graph_builder` | Graph data construction |
| **woven_maps** | `IP.woven_maps` | 3D city generation, CodeNode, EdgeData |
| **assets** | `IP.features.code_city.assets` | Template loading, script tags |
| **camera_state** | `IP.contracts.camera_state` | Default camera configuration |
| **connection_verifier** | `IP.connection_verifier` | Import graph building |

### Static Assets Loaded

| Asset | Path | Fallback CDN |
|-------|------|--------------|
| `woven_maps_3d.js` | `IP/static/woven_maps_3d.js` | N/A (required) |
| `delaunay.js` | `Barradeau/woven_map/delaunay.js` | `d3-delaunay@6` |
| `three.min.js` | `Barradeau/FBO-master/vendor/three.min.js` | `three.js r128` |
| `OrbitControls.js` | `Barradeau/FBO-master/vendor/OrbitControls.js` | `three@0.128.0` |

### Health Integration

**Function:** `build_from_health_results()` in `graph_builder.py:334-376`

Merges HealthChecker output into CodeNode objects:
- `node.status` - Updated via `merge_status()` policy
- `node.health_errors` - Up to 10 structured errors per file

### Combat Tracker Integration

**Location:** `graph_builder.py:229-238`

Sets node status to "combat" if file is actively deployed by an LLM agent.

### Louis (File Protection) Integration

**Location:** `graph_builder.py:240-249`

Sets `node.is_locked = True` for protected files.

---

## 5. Ambiguities & Concerns

### 1. Dual Entry Point for Code City

**Issue:** There are two `create_code_city()` functions:
- `IP/features/code_city/render.py:23` - Primary implementation
- `IP/woven_maps.py:911` - Wrapper that imports and calls the primary

**Ambiguity:** Which should be imported where? Currently:
- `06_maestro.py` imports from `IP.woven_maps` (wrapper path)
- Direct usage may import from either location

### 2. Import Fallback in graph_builder.py

**Location:** `graph_builder.py:181-182`

```python
try:
    from IP.connection_verifier import build_connection_graph
except ImportError:
    from connection_verifier import build_connection_graph  # ← Fallback
```

**Ambiguity:** The fallback assumes `connection_verifier` is in Python path. This works in some contexts but is fragile.

### 3. Boundary Contract Loading

**Location:** `graph_builder.py:252-277`

The code searches for survey.json in multiple locations:
```python
survey_paths = [
    Path(project_root) / ".settlement" / "survey.json",
    Path(project_root) / ".planning" / "survey.json",
    Path(project_root) / "settlement_survey.json",
]
```

**Ambiguity:** Which location is canonical? The code breaks after finding the first one.

### 4. Environment Variable Naming Inconsistency

| Variable | Purpose |
|----------|---------|
| `ORCHESTR8_CODE_CITY_STREAM_BPS` | Streaming rate |
| `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` | 3D mode toggle |
| `ORCHESTR8_CODE_CITY_MAX_BYTES` | Payload guard |
| `ORCHESTR8_PATCHBAY_APPLY` | Patchbay feature flag |

**Concern:** All start with `ORCHESTR8_` but the patchbay variable is scoped differently.

### 5. Three.js Version Pinning

**Location:** `render.py:118`

```python
"https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
```

**Concern:** r128 is ~2.5 years old. Newer Three.js features not available.

### 6. Silent Failure Modes

The function returns `mo.md()` for errors rather than raising:
- Invalid root → "Set a valid project root"
- No code files → "No code files found"

**Ambiguity:** These are informational but may mask configuration issues.

### 7. Camera State Serialization

**Location:** `render.py:82-95`

```python
camera_state = get_default_camera_state()
camera_state_json = json.dumps({
    "mode": camera_state.mode,
    "position": camera_state.position,
    ...
})
```

**Concern:** Custom `CameraState` object from `IP.contracts.camera_state` is serialized manually. If fields change, serialization breaks silently.

---

## 6. Key Data Structures

### CodeNode (from woven_maps.py:92-139)

| Field | Type | Purpose |
|-------|------|---------|
| `path` | str | File path |
| `status` | str | "working" / "broken" / "combat" |
| `loc` | int | Lines of code |
| `x`, `y` | float | 2D layout position |
| `building_height` | float | 3D building height |
| `footprint` | float | 3D building footprint |
| `is_locked` | bool | Louis protection status |
| `display_zone` | str | "city" / "town_square" / "hidden" |

### EdgeData (from woven_maps.py:142-)

| Field | Type | Purpose |
|-------|------|---------|
| `source` | str | Importing file |
| `target` | str | Imported file |
| `from_fiefdom` | str | Source directory |
| `to_fiefdom` | str | Target directory |
| `is_boundary` | bool | Cross-fiefdom connection |
| `contract_status` | str | "valid" / "missing" / "violated" |

### Neighborhood (from woven_maps.py)

| Field | Type | Purpose |
|-------|------|---------|
| `name` | str | Directory path |
| `center_x`, `center_y` | float | Centroid |
| `boundary_points` | List[dict] | Bounding box |
| `integration_count` | int | Cross-neighborhood edges |
| `status` | str | Aggregated status |

---

## 7. CSS/Visual Contract

**Background:** `#0A0AB` (The Void)
**Border Radius:** 8px
**Height:** `clamp(360px, 78vh, 1200px)`

**Iframe sandbox:** `allow-scripts`
**Iframe allow:** `microphone` (unusual - potential security concern)

---

## 8. Recommendations

1. **Consolidate entry points** - Single canonical `create_code_city()` import path
2. **Remove fallback imports** - Use absolute imports consistently
3. **Canonical survey location** - Pick one path for boundary contracts
4. **Upgrade Three.js** - Consider r152+ for better WebGPU support
5. **Document camera_state fields** - Explicit serialization schema
6. **Audit microphone permission** - Verify it's actually needed

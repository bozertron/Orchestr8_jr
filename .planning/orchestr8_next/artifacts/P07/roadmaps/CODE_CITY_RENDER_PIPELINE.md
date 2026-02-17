# Code City Render Pipeline

**Source**: `/home/bozertron/Orchestr8_jr/IP/features/code_city/render.py`
**Target**: `a_codex_plan`
**Rationale**: Marimo assembly of Code City visualization
**Date**: 2026-02-16

---

## Overview

The render pipeline in `render.py` serves as the final assembly layer that transforms Code City graph data into an interactive HTML iframe visualization embedded in Marimo. It bridges the gap between Python-side data preparation (graph structures, file metrics, health status) and JavaScript-side rendering (Woven Maps canvas, particle effects, 3D buildings).

---

## 1. Iframe Creation Mechanism

### Entry Point

The `create_code_city()` function (lines 23-161) is the primary entry point for rendering the Code City visualization. It performs the following high-level operations:

1. **Validation**: Ensures the project root directory exists
2. **Data Pipeline**: Builds graph data from the codebase using either connection graph or fallback scanning
3. **Health Merge**: Injects health check results into node status
4. **Configuration**: Reads environment variables for streaming and inline building data
5. **Template Assembly**: Loads the HTML template and substitutes all placeholders
6. **HTML Wrapping**: Embeds the assembled HTML into a Marimo `mo.Html()` component with an iframe

### HTML Structure

The final iframe is created with the following characteristics:

```python
mo.Html(f"""
<div style="background: #0A0A0B; border-radius: 8px; overflow: hidden; ...">
    <iframe
        srcdoc="{escaped}"
        width="100%"
        height="100%"
        style="border: none; display: block; ..."
        sandbox="allow-scripts"
        allow="microphone"
    ></iframe>
</div>
""")
```

Key attributes:
- **`srcdoc`**: Contains the complete inline HTML document, avoiding external request dependencies
- **`sandbox="allow-scripts"`**: Permits JavaScript execution while restricting other capabilities
- **`allow="microphone"`**: Enables audio-reactive features (Web Audio API)
- **Dynamic sizing**: Uses `clamp(360px, 78vh, 1200px)` for responsive height

---

## 2. Template Substitution Patterns

### Template Loading

The template is loaded from a static file via `assets.py`:

```python
@lru_cache(maxsize=1)
def load_woven_maps_template() -> str:
    template_path = Path(__file__).resolve().parents[2] / "static" / "woven_maps_template.html"
    return template_path.read_text(encoding="utf-8")
```

The `@lru_cache` ensures the template is read only once per process.

### Placeholder Replacements

The template uses a double-underscore naming convention for placeholders that are replaced via string `.replace()` calls (lines 125-138):

| Placeholder | Source | Purpose |
|-------------|--------|---------|
| `__GRAPH_DATA__` | `graph_data.to_json()` | Complete graph structure (nodes, edges, config, neighborhoods) |
| `__BUILDING_DATA__` | `json.dumps(building_data)` or `"null"` | 3D building geometry for WebGL rendering (client-side generation) |
| `__BUILDING_STREAM_BPS__` | Environment variable | Streaming rate for progressive 3D building data |
| `__CAMERA_STATE__` | `json.dumps(camera_dict)` | Initial camera position, zoom, and navigation state |
| `__PATCHBAY_APPLY_ENABLED__` | Environment variable | Boolean flag for re-wiring feature availability |
| `__DELAUNAY_LIB_TAG__` | `script_tag()` helper | D3 Delaunay library (inline or CDN fallback) |
| `__THREE_CORE_TAG__` | `script_tag()` helper | Three.js core (inline or CDN fallback) |
| `__THREE_ORBIT_TAG__` | `script_tag()` helper | OrbitControls for 3D navigation |
| `__WOVEN_MAPS_3D_JS__` | File content | Custom Woven Maps 3D rendering logic |

### Script Tag Pattern

The `script_tag()` helper (assets.py, lines 21-25) implements a local-first strategy with CDN fallback:

```python
def script_tag(local_source: str, fallback_src: str) -> str:
    if local_source.strip():
        return f"<script>{script_safe(local_source)}</script>"
    return f'<script src="{fallback_src}"></script>'
```

This ensures the visualization works even if local asset files are missing.

### HTML Escaping

Before embedding in the iframe, the assembled HTML is escaped:

```python
escaped = html.escape(iframe_html)
```

This prevents XSS issues when the template contains user-derived content.

---

## 3. State Management

### Camera State

Camera state is defined in `IP/contracts/camera_state.py` as a `CameraState` dataclass with the following structure:

```python
@dataclass
class CameraState:
    mode: CameraMode  # "overview" | "neighborhood" | "building" | "room" | "sitting_room" | "focus"
    position: Tuple[float, float, float]  # (x, y, z) camera position
    target: Tuple[float, float, float]    # Look-at target
    zoom: float
    return_stack: List[Dict[str, Any]]    # Navigation history for round-trip
    transition_ms: int = 1000
    easing: str = "easeInOutCubic"
```

The default camera provides a distant overview for rapid hotspot triage:

```python
def get_default_camera_state() -> CameraState:
    return CameraState(
        mode="overview",
        position=(0.0, 800.0, 1200.0),
        target=(0.0, 0.0, 0.0),
        zoom=0.5,
        ...
    )
```

### Health Results Injection

Health check results are merged into nodes via `build_from_health_results()`:

```python
if health_results:
    graph_data.nodes = build_from_health_results(graph_data.nodes, health_results)
```

This function (graph_builder.py, lines 332-371) updates node status and populates `health_errors` for display in tooltips.

### Environment-Driven Configuration

Three environment variables control rendering behavior:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ORCHESTR8_CODE_CITY_STREAM_BPS` | `5,000,000` | Bytes per second for progressive 3D building streaming |
| `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` | `""` (off) | Whether to inline full 3D building arrays vs. client-side generation |
| `ORCHESTR8_PATCHBAY_APPLY` | `""` (off) | Enable the re-wiring panel and apply functionality |
| `ORCHESTR8_CODE_CITY_MAX_BYTES` | `9,000,000` | Payload size guardrail for oversized repositories |

---

## 4. Integration with woven_maps.py

### Data Structure Dependencies

`render.py` imports core data structures from `woven_maps.py`:

```python
from IP.woven_maps import (
    CodeNode,      # File representation with metrics
    EdgeData,      # Import relationship between files
    GraphConfig,   # Visualization configuration
    GraphData,     # Complete graph package
    Neighborhood,  # Directory cluster with boundary
)
```

These structures are defined in `woven_maps.py` (lines 93-320) with `to_dict()` and `to_json()` serialization methods.

### Graph Building Pipeline

The render pipeline delegates graph construction to `graph_builder.py`:

1. **Primary Path**: `build_from_connection_graph()` uses the `ConnectionGraph` from `connection_verifier.py` to build nodes and edges with real import relationships
2. **Fallback Path**: `build_graph_data()` scans the filesystem directly when connection graph is unavailable
3. **Health Merge**: `build_from_health_results()` injects health check output

### 3D Building Generation

When inline building data is enabled, `render.py` calls:

```python
from IP import woven_maps as wm
building_data = wm.create_3d_code_city(graph_data, layout_scale=10.0)
```

This function (woven_maps.py, lines 871-894) delegates to `barradeau_builder.py` to generate 3D geometry:

```python
def create_3d_code_city(graph_data, layout_scale=10.0):
    buildings = generate_barradeau_buildings(graph_data, layout_scale)
    return {"buildings": buildings, "metadata": {...}}
```

### Compatibility Wrappers

`woven_maps.py` provides wrapper functions that delegate back to the feature-sliced modules:

```python
def create_code_city(root, ...):
    from IP.features.code_city.render import create_code_city as _create_code_city
    return _create_code_city(...)
```

This allows downstream code to import from `woven_maps.py` without knowing the internal module structure.

---

## 5. Payload Size Guardrail

The render pipeline includes an oversized payload protection mechanism (06_maestro.py, lines 1178-1212):

1. **Measurement**: `_payload_size_bytes(result)` calculates serialized output size
2. **Retry Strategy**: If root payload exceeds `ORCHESTR8_CODE_CITY_MAX_BYTES`, retries with `IP/` subroot
3. **Fallback**: If still oversized, displays a warning panel with configuration guidance

This protects against repository roots that produce visualization payloads exceeding Marimo's output limits.

---

## 6. Data Flow Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Marimo Cell (06_maestro.py)                  │
│  create_code_city(root, health_results)                             │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    render.py: create_code_city()                    │
│                                                                      │
│  ┌──────────────────┐    ┌─────────────────┐    ┌───────────────┐ │
│  │ root validation  │───▶│ build_from_     │───▶│ build_from_   │ │
│  │                  │    │ connection_graph│    │ health_results│ │
│  └──────────────────┘    └─────────────────┘    └───────────────┘ │
│                                   │                                 │
│                                   ▼                                 │
│  ┌──────────────────┐    ┌─────────────────┐    ┌───────────────┐ │
│  │ camera_state     │    │ load template   │    │ script_tag()  │ │
│  │ get_default()    │    │ load_woven_     │    │ helper        │ │
│  │                  │    │ maps_template() │    │               │ │
│  └──────────────────┘    └─────────────────┘    └───────────────┘ │
│                                   │                                 │
│                                   ▼                                 │
│                    ┌────────────────────────────────┐               │
│                    │  Template substitution         │               │
│                    │  .replace("__GRAPH_DATA__",    │               │
│                    │  .replace("__CAMERA_STATE__",  │               │
│                    │  ...                           │               │
│                    └────────────────────────────────┘               │
│                                   │                                 │
│                                   ▼                                 │
│                    ┌────────────────────────────────┐               │
│                    │  HTML escape + iframe wrap     │               │
│                    │  mo.Html(srcdoc="{escaped}")  │               │
│                    └────────────────────────────────┘               │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Browser Runtime                               │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Template    │  │ GRAPH_DATA  │  │ CAMERA_STATE│  │ BUILDING  │ │
│  │ HTML shell  │  │ nodes/edges │  │ navigation  │  │ DATA      │ │
│  │             │  │ neighborhoods│ │ mode/zoom   │  │ (3D opt)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘ │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │              Woven Maps Canvas Rendering                       ││
│  │  - Delaunay triangulation for building placement               ││
│  │  - Emergence particle system                                    ││
│  │  - Audio-reactive visualization                                 ││
│  │  - Navigation (warpDive, returnFromDive)                       ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Key Files and Locations

| File | Purpose |
|------|---------|
| `IP/features/code_city/render.py` | Primary render pipeline entry point |
| `IP/features/code_city/assets.py` | Template loading and script tag helpers |
| `IP/features/code_city/graph_builder.py` | Graph data construction from codebase |
| `IP/woven_maps.py` | Data structures and compatibility wrappers |
| `IP/static/woven_maps_template.html` | HTML template for iframe content |
| `IP/contracts/camera_state.py` | Camera state schema and defaults |
| `IP/plugins/06_maestro.py` | Caller site with payload guardrail |

---

## 8. Findings and Implications

### Strengths

1. **Single render path**: The `create_code_city()` function is the canonical entry point, avoiding UI drift from multiple render paths
2. **Graceful degradation**: CDN fallbacks ensure visualization works without local assets
3. **Payload protection**: Guardrail prevents oversized renders from breaking Marimo
4. **Clean separation**: Feature-sliced modules (`render.py`, `graph_builder.py`) isolate concerns
5. **Environment-driven**: Configuration via env vars enables tuning without code changes

### Areas for Potential Enhancement

1. **Template substitution**: Current `.replace()` chain could be refactored to use a dictionary-based substitution pattern for maintainability
2. **Streaming architecture**: The current streaming mechanism relies on environment variables; a more explicit configuration API could improve usability
3. **Error boundaries**: The render pipeline lacks explicit error handling for malformed graph data
4. **State hydration**: Camera state is read-only at render time; bidirectional state sync (postMessage from iframe to Python) is not fully utilized
5. **Testability**: The render function mixes data fetching, template assembly, and HTML construction; dependency injection could improve test coverage

---

*End of Pipeline Analysis*

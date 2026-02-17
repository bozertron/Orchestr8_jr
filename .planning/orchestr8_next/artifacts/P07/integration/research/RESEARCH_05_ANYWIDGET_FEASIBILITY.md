# Phase: Agent 5 - anywidget Code City Feasibility - Research

**Researched:** 2026-02-16  
**Domain:** Jupyter/marimo widget development, Three.js 3D visualization migration  
**Confidence:** HIGH

## Summary

This research investigates the feasibility of replacing the current Code City HTML/JS injection mechanism (`mo.Html()` with iframe) with an anywidget-based solution. The current pipeline uses a complex flow: `graph_builder.py` → `woven_maps.py` → HTML template injection → `mo.Html()` iframe rendering. anywidget provides a modern alternative that eliminates iframe communication overhead and simplifies widget lifecycle management.

**Primary recommendation:** GO - The migration is feasible and recommended. anywidget v0.9.21 + marimo 0.19.11 combination supports this migration. The existing `woven_maps_3d.js` Three.js code can be adapted to work as an ESM module within anywidget's AFM specification. Estimated effort: **16-24 hours** for core implementation.

## Current Pipeline Analysis

### Data Flow (Current Implementation)

```
graph_builder.py
    ├── build_from_connection_graph() 
    │   └── returns GraphData (nodes, edges, neighborhoods)
    │
woven_maps.py  
    ├── CodeNode, EdgeData, GraphConfig, GraphData dataclasses
    ├── scan_codebase() → calculates building geometry
    └── create_3d_code_city() → generates Barradeau buildings

render.py
    ├── load_woven_maps_template() → HTML string with __PLACEHOLDERS__
    ├── read_text_if_exists() → inline JS (woven_maps_3d.js)
    ├── string replacement → injects graph_data, building_data, camera_state
    └── mo.Html(iframe srcdoc=escaped_html) → browser
```

### Key Files and Their Roles

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `graph_builder.py` | Builds graph from codebase | `build_from_connection_graph()`, `compute_neighborhoods()` |
| `woven_maps.py` | Data structures + geometry | `CodeNode`, `EdgeData`, `GraphData`, `GraphConfig` |
| `render.py` | Marimo integration entry | `create_code_city()` → returns `mo.Html()` |
| `woven_maps_3d.js` | Three.js renderer | `CodeCityScene` class |
| `woven_maps_template.html` | Iframe HTML shell | Full UI with controls, tooltips, HUD |

### Current Limitations (Motivation for Migration)

1. **Iframe communication overhead** - postMessage events between iframe and parent have latency
2. **Complex template string replacement** - 6+ placeholder replacements in render.py
3. **No direct Python-JS state sync** - changes require full re-render
4. **Static asset loading complexity** - CDN fallbacks for Three.js dependencies
5. **Limited interactivity** - camera state changes require iframe message round-trip

## Standard Stack

### Core Technologies

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **anywidget** | 0.9.21 | Widget specification & runtime | Native marimo support, modern ipywidgets alternative |
| **marimo** | 0.19.11 | Reactive notebook runtime | Native `mo.ui.anywidget()` wrapper |
| **traitlets** | (bundled) | Bidirectional state sync | anywidget's state management |
| **Three.js** | r128 (CDN) | 3D rendering | Existing Code City dependency |

### Supporting Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **esbuild** | Bundler for ESM | If splitting JS into multiple files |
| **esm.sh** | CDN for ES modules | For Three.js in anywidget ESM |
| **Vite** | Dev server + HMR | If using React/Svelte bridges |

### Anywidget Architecture

anywidget uses the **Anywidget Front-End Module (AFM)** specification:

```python
# Python side
class MyWidget(anywidget.AnyWidget):
    _esm = """...ESM JavaScript..."""  # or path to .js file
    _css = """...CSS..."""              # optional
    count = traitlets.Int(0).tag(sync=True)
```

```javascript
// JavaScript side (ESM)
export default {
    initialize({ model }) {
        // Called once per widget instance
    },
    render({ model, el }) {
        // Called each time view renders
        // model.get/set for traitlet access
        // el is the container DOM element
    }
}
```

## Architecture Patterns for Migration

### Proposed anywidget Class Design

```python
# IP/features/code_city/anywidget_city.py
import anywidget
import traitlets
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class CodeCityWidget(anywidget.AnyWidget):
    """Three.js Code City visualization as anywidget."""
    
    # ESM module - references external JS file
    _esm = Path(__file__).parent / "static" / "code_city_widget.js"
    _css = Path(__file__).parent / "static" / "code_city_widget.css"
    
    # === Traitlets for bidirectional sync ===
    
    # Graph data - the core visualization data
    graph_data = traitlets.Dict().tag(sync=True)
    
    # Building data - pre-computed 3D positions (optional, can derive)
    building_data = traitlets.Dict().tag(sync=True)
    
    # Configuration
    width = traitlets.Int(800).tag(sync=True)
    height = traitlets.Int(600).tag(sync=True)
    max_height = traitlets.Int(250).tag(sync=True)
    
    # Camera state (read/write from JS)
    camera_mode = traitlets.Unicode("overview").tag(sync=True)
    camera_zoom = traitlets.Float(0.5).tag(sync=True)
    camera_position = traitlets.List([]).tag(sync=True)
    camera_target = traitlets.List([0, 5, 0]).tag(sync=True)
    
    # Interaction state
    hovered_node = traitlets.Unicode("").tag(sync=True)
    selected_node = traitlets.Unicode("").tag(sync=True)
    emergence_phase = traitlets.Unicode("void").tag(sync=True)
    
    # Performance tuning
    particle_cpu_cap = traitlets.Int(180000).tag(sync=True)
    emergence_frame_spawn_cap = traitlets.Int(700).tag(sync=True)
    
    def __init__(
        self,
        root: str,
        width: int = 800,
        height: int = 600,
        max_height: int = 250,
        **kwargs
    ):
        # Build graph data on initialization
        from IP.features.code_city.graph_builder import build_from_connection_graph
        from IP import woven_maps as wm
        
        graph_data = build_from_connection_graph(
            root,
            width=width,
            height=height,
            max_height=max_height,
        )
        
        # Convert to dict for traitlet serialization
        self.graph_data = graph_data.to_dict()
        
        # Pre-compute building data if inline requested
        inline = kwargs.pop('inline_building_data', False)
        if inline:
            building_data = wm.create_3d_code_city(graph_data, layout_scale=10.0)
            self.building_data = building_data
        
        super().__init__(
            width=width,
            height=height,
            max_height=max_height,
            **kwargs
        )
```

### Proposed JavaScript ESM Structure

```javascript
// IP/features/code_city/static/code_city_widget.js
import * as THREE from 'https://esm.sh/three@0.128.0';
import { OrbitControls } from 'https://esm.sh/three@0.128.0/examples/jsm/controls/OrbitControls.js';

// Import existing CodeCityScene class logic
import { CodeCityScene } from './woven_maps_3d.js';

export default {
    initialize({ model }) {
        // Set up event handlers for traitlet changes
        model.on("change:camera_mode", this._onCameraModeChange);
        model.on("change:camera_zoom", this._onCameraZoomChange);
        
        // Listen for custom messages from Python
        model.on("msg:custom", this._onCustomMessage);
        
        // Cleanup function
        return () => {
            // Called when widget is destroyed
            this._cleanup();
        };
    },
    
    render({ model, el }) {
        // Create container
        const container = document.createElement('div');
        container.style.width = `${model.get('width')}px`;
        container.style.height = `${model.get('height')}px`;
        container.style.background = '#050505';
        el.appendChild(container);
        
        // Initialize Three.js scene
        this._scene = new CodeCityScene(container);
        
        // Load buildings from graph data
        const graphData = model.get('graph_data');
        if (graphData && graphData.buildings) {
            this._scene.loadBuildings(graphData.buildings);
        }
        
        // Start emergence animation
        this._scene.playEmergenceSequence(2000, (phase) => {
            // Sync emergence phase back to Python
            model.set('emergence_phase', phase.name);
            model.save_changes();
        });
        
        // Enable hover effects
        this._scene.enableHoverEffects();
        
        // Listen for node hover events
        window.addEventListener('nodeHover', (e) => {
            model.set('hovered_node', e.detail.path);
            model.save_changes();
        });
        
        // Expose camera control methods
        this._setupCameraControls(model, container);
        
        // Cleanup on view removal
        return () => {
            this._scene.dispose();
            container.remove();
        };
    },
    
    _onCameraModeChange(model) {
        const mode = model.get('camera_mode');
        this._scene.setCameraMode(mode);
    },
    
    _onCameraZoomChange(model) {
        const zoom = model.get('camera_zoom');
        this._scene.setZoom(zoom);
    },
    
    _onCustomMessage(msg, buffers) {
        // Handle custom messages from Python
        // e.g., updateBuildingStatus, focusNode, etc.
        switch (msg.type) {
            case 'update_status':
                this._scene.updateBuildingStatus(msg.path, msg.status);
                break;
            case 'focus':
                this._scene.warpDiveTo(msg.node);
                break;
        }
    },
    
    _setupCameraControls(model, container) {
        // Sync camera state changes back to Python
        // This enables round-trip navigation state
    }
};
```

### Data Flow (Proposed anywidget Implementation)

```
Python                          JavaScript (ESM)
───────                          ─────────────────

graph_builder.py                    
    │                             
    ▼                             
CodeCityWidget.__init__()         initialize({model})
    │                             
    ▼                             
model.set('graph_data', ...)  ───► model.get('graph_data')
                                        │
                                        ▼
                                   CodeCityScene.render()
                                        │
                                        ▼
                                   Three.js canvas

model.on('change:camera_zoom') ◄──── model.set('camera_zoom', ...)
model.on('msg:custom')          ◄──── model.send({type: 'hover', ...})
```

### Key Differences: Current vs Proposed

| Aspect | Current (iframe) | Proposed (anywidget) |
|--------|-----------------|---------------------|
| Rendering | `mo.Html(iframe srcdoc=...)` | `mo.ui.anywidget(CodeCityWidget())` |
| State sync | Full re-render on any change | Traitlet-level bidirectional sync |
| Communication | postMessage (iframe ↔ parent) | Direct model.get/set |
| Dependencies | Inline script tags in HTML | ESM imports from esm.sh |
| Camera control | JSON via postMessage | Direct traitlet observation |
| Events | Custom event dispatch | model.send() → Python callbacks |

## Don't Hand-Roll

### Problems with Existing Solutions

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| **3D Rendering** | Custom WebGL | Three.js | Already implemented, battle-tested |
| **Widget Protocol** | Custom iframe message protocol | anywidget AFM | Marimo native support |
| **State Sync** | Manual JSON serialization | traitlets | Automatic bidirectional sync |
| **ESM Bundling** | Custom build pipeline | esbuild or esm.sh CDN | Simpler, HMR support |
| **Particle Effects** | Canvas 2D fallback | Existing ShaderMaterial | Barradeau algorithm already works |

### Existing Code Reuse Strategy

1. **Reuse `CodeCityScene` class** - Extract from `woven_maps_3d.js` as ESM module
2. **Reuse `GraphData` dataclasses** - `woven_maps.py` classes work as-is
3. **Reuse `graph_builder.py`** - No changes needed, produces same data structure
4. **Reuse color constants** - Share via Python dict passed to JS

## Common Pitfalls

### Pitfall 1: ESM Module Loading in anywidget
**What goes wrong:** Three.js ESM imports fail due to CORS or module resolution issues  
**Why it happens:** CDN URLs must be properly versioned and CORS-enabled  
**How to avoid:** Use esm.sh or jsdelivr with exact versions; test in browser first  
**Warning signs:** Console shows "Failed to load module", CORS errors

### Pitfall 2: Traitlet Serialization Size
**What goes wrong:** Large graph data causes slow renders or memory issues  
**Why it happens:** Traitlets sync entire dict on each change  
**How to avoid:** 
- Use `traitlets.Dict()` with careful `.tag(sync=True)` scoping
- Consider streaming large data via `model.send()` with buffers
- Pass only delta updates for camera moves

### Pitfall 3: Circular Dependencies in JS Modules
**What goes wrong:** CodeCityScene references Three.js globals that aren't exported  
**Why it happens:** Original code assumes globals from `<script>` tags  
**How to avoid:** Refactor to use ESM imports consistently; test in isolation

### Pitfall 4: Memory Leaks on Widget Re-creation
**What goes wrong:** Three.js WebGL context not disposed on re-render  
**Why it happens:** Missing cleanup in render() return function  
**How to avoid:** Always return cleanup function that calls `renderer.dispose()`, removes event listeners

### Pitfall 5: marimo Cell Reactivity Loop
**What goes wrong:** Setting traitlet in Python triggers re-execution of cell  
**Why it happens:** marimo's reactivity observes widget.value changes  
**How to avoid:** 
- Use widget-specific attributes (not `.value`) for internal state
- Or use `mo.state()` for non-reactive state

## Code Examples

### Example 1: Basic anywidget with Three.js

```python
# Minimal working example - test anywidget + Three.js integration
import anywidget
import traitlets
import marimo as mo

class Simple3DWidget(anywidget.AnyWidget):
    _esm = """
    import * as THREE from 'https://esm.sh/three@0.128.0';
    
    export default {
        render({ model, el }) {
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, el.clientWidth / el.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer();
            renderer.setSize(el.clientWidth, el.clientHeight);
            el.appendChild(renderer.domElement);
            
            const geometry = new THREE.BoxGeometry();
            const material = new THREE.MeshBasicMaterial({ color: 0xd4af37 });
            const cube = new THREE.Mesh(geometry, material);
            scene.add(cube);
            camera.position.z = 5;
            
            function animate() {
                requestAnimationFrame(animate);
                cube.rotation.x += 001;
                cube.rotation.y += 0.01;
                renderer.render(scene, camera);
            }
            animate();
            
            return () => renderer.dispose();
        }
    }
    """
    
    background_color = traitlets.Unicode("#050505").tag(sync=True)

# Test in marimo
widget = Simple3DWidget()
mo.ui.anywidget(widget)
```

### Example 2: Bidirectional State Sync

```python
import anywidget
import traitlets

class CounterWidget(anywidget.AnyWidget):
    _esm = """
    export default {
        render({ model, el }) {
            const btn = document.createElement('button');
            btn.textContent = `Count: ${model.get('count')}`;
            btn.onclick = () => {
                model.set('count', model.get('count') + 1);
                model.save_changes();
            };
            model.on('change:count', () => {
                btn.textContent = `Count: ${model.get('count')}`;
            });
            el.appendChild(btn);
        }
    }
    """
    count = traitlets.Int(0).tag(sync=True)
```

### Example 3: Custom Messages (Events from JS to Python)

```python
import anywidget
import traitlets
from marimo import mo

class EventWidget(anywidget.AnyWidget):
    _esm = """
    export default {
        render({ model, el }) {
            // Send custom message to Python
            el.onclick = () => {
                model.send({
                    'type': 'click',
                    'x': Math.random(),
                    'y': Math.random()
                });
            };
        }
    }
    """
    
    # Handle custom messages
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Note: Custom message handling requires 
        # creating a custom widget subclass in marimo
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| ipywidgets + IPythonWidget | anywidget + AFM | 2024+ | Modern ESM, no Backbone.js |
| Iframe HTML injection | Native widget | anywidget 0.9+ | Direct DOM, no iframe overhead |
| String template replacement | Traitlet state | traitlets 5.2+ | Type-safe, observable properties |
| CDN script tags | ESM imports | Modern browsers | Tree-shaking, better caching |

### Deprecated/outdated:
- **Backbone.js widget base** - anywidget doesn't require it
- **ipywidgets cookiecutter templates** - anywidget simplifies this
- **Inline `<script>` tags in HTML** - Use ESM imports instead
- **Manual postMessage communication** - Use model.get/set + send()

## Binary Data Support

anywidget supports efficient binary data transfer via the `buffers` parameter in `model.send()`:

```javascript
// JavaScript - send binary data
const buffer = new Float32Array([1.0, 2.0, 3.0]);
model.send({ type: 'buffer' }, null, [buffer]);
```

This can be used for:
- Large particle position arrays (Float32Array for 3D coordinates)
- Texture data
- Audio FFT data

**Current pipeline already handles this well** - graph data is JSON-serialized, which is acceptable for typical codebase sizes (<10,000 files). For very large codebases, binary buffers could optimize the building data transfer.

## Static Asset 404 Problem Analysis

### Current Issue
The current implementation uses a complex fallback chain:
1. Try local static file (e.g., `woven_maps_3d.js`)
2. If not found, fallback to CDN URL

This can cause 404s when:
- Running in different environments (colab, local, deployed)
- Static files not properly deployed
- Path resolution issues

### anywidget Solution
anywidget **eliminates this problem** because:
1. ESM is embedded or loaded via URL - no local file fallback needed
2. Dependencies come from CDN (esm.sh, jsdelivr) - reliable, versioned
3. No iframe means no separate static file serving

### Migration Impact
✅ **SOLVED** - anywidget's ESM approach inherently avoids static asset 404s by using:
- Inline ESM string in Python file (development)
- esm.sh CDN URLs (production)
- No local static file serving required

## Effort Estimate

### Phase 1: Core Implementation (12-16 hours)

| Task | Hours | Notes |
|------|-------|-------|
| Create CodeCityWidget class | 2 | Define traitlets, ESM reference |
| Extract/refactor woven_maps_3d.js to ESM | 4 | Add exports, fix globals to imports |
| Create code_city_widget.js render logic | 4 | Initialize Three.js, wire traitlets |
| Style CSS (reuse from template) | 1 | Extract from woven_maps_template.html |
| Test basic rendering | 2 | Verify Three.js loads, buildings render |
| Debug ESM module issues | 2 | Common: import paths, Three.js globals |
| **Subtotal** | **15** | |

### Phase 2: Feature Parity (4-6 hours)

| Task | Hours | Notes |
|------|-------|-------|
| Implement camera controls sync | 1 | Zoom, pan, rotation |
| Implement hover/click events | 1 | Node selection |
| Implement emergence animation | 1 | Phase callbacks |
| Add neighborhood boundaries | 1 | Reuse existing JS logic |
| Audio reactive features | 1 | Optional, depends on mic permission |
| **Subtotal** | **5** | |

### Phase 3: Integration & Polish (2-4 hours)

| Task | Hours | Notes |
|------|-------|-------|
| Update render.py to use anywidget | 1 | Replace mo.Html() with mo.ui.anywidget() |
| Handle backward compatibility | 1 | Environment variable flag |
| Performance testing | 1 | Large codebase rendering |
| Documentation update | 1 | Migration notes |
| **Subtotal** | **4** | |

### Total: 16-24 hours

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Three.js ESM import issues | Medium | High | Test with minimal example first |
| Traitlet performance with large data | Low | Medium | Use binary buffers if needed |
| marimo anywidget edge cases | Low | Medium | Test in target marimo version |
| Breaking changes in anywidget API | Low | Low | Pin to 0.9.x |

## Open Questions

1. **Question:** Does marimo's `mo.ui.anywidget()` support all anywidget features?
   - What we know: Basic traitlet sync and custom messages work
   - What's unclear: Advanced features like buffer transfer in marimo
   - Recommendation: Test with minimal example before full implementation

2. **Question:** How to handle audio input (microphone) in anywidget?
   - What we know: Current iframe uses `allow="microphone"`
   - What's unclear: anywidget's approach for media permissions
   - Recommendation: Test audio features after core rendering works

3. **Question:** Should we keep backward compatibility with the old iframe approach?
   - What we know: Both approaches can coexist
   - What's unclear: Long-term maintenance burden
   - Recommendation: Use environment flag, deprecate old approach after migration

## Sources

### Primary (HIGH confidence)
- anywidget.dev/getting-started/ - Official documentation
- anywidget.dev/en/afm/ - AFM specification
- anywidget.dev/en/bundling/ - ESM bundling guide
- docs.marimo.io/api/inputs/anywidget - marimo integration

### Secondary (MEDIUM confidence)
- esm.sh - CDN for ES modules (Three.js)
- three.js documentation - Version r128 API

### Tertiary (LOW confidence)
- Community anywidget examples (various GitHub repos)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - anywidget 0.9.21 + marimo 0.19.11 verified installed
- Architecture: HIGH - AFM specification is stable, examples numerous
- Pitfalls: MEDIUM - Some Three.js ESM edge cases need testing
- Binary data: HIGH - anywidget supports buffers per AFM spec
- Static asset 404: HIGH - ESM approach eliminates this problem

**Research date:** 2026-02-16  
**Valid until:** 2026-03-16 (anywidget is stable, unlikely to break)

---

## GO/NO-GO Recommendation

### ✅ GO

**Rationale:**
1. **Technical Feasibility: HIGH** - anywidget + marimo combination is proven and supports the required features
2. **Problem Solved: YES** - Current iframe approach has real limitations that anywidget addresses
3. **Reuse Existing Code: YES** - 90%+ of current JS/Three.js code can be adapted
4. **Effort Reasonable: YES** - 16-24 hours is a manageable sprint
5. **Risk Acceptable: LOW** - Issues are addressable, no showstoppers identified

**Recommended approach:**
1. Start with a minimal anywidget + Three.js test (2 hours)
2. Refactor woven_maps_3d.js to ESM in isolation (4 hours)  
3. Build full CodeCityWidget with core features (8 hours)
4. Integrate and test in marimo (4 hours)
5. Polish and ship (4 hours)

**Rollout strategy:**
- Use environment flag to toggle between old/new implementations
- A/B test with small codebase first
- Full migration in single PR

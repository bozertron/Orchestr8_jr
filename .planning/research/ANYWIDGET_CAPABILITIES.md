# Research: anywidget for Custom Visualization

**Project:** Orchestr8 - Code City Visualization  
**Researched:** 2026-02-13  
**Confidence:** HIGH - Verified with Context7, GitHub, and existing implementations

## Executive Summary

**Verdict: anywidget CAN replace custom WebGPU canvas for Code City rendering.**

anywidget is a mature, well-supported library (852 GitHub stars, 1.5k+ dependents) that provides bidirectional Python-JavaScript communication with support for:
- Binary data (TypedArrays) via `traitlets.Bytes()`
- WebGL/Three.js rendering (proven by existing packages like ipyniivue, threey, lonboard)
- Real-time updates via the Comm protocol
- Native marimo integration via `mo.ui.anywidget()`

The architecture is suitable for Code City visualization. However, there are tradeoffs around **real-time animation performance** that require careful consideration.

---

## 1. anywidget Architecture

### Data Flow

anywidget uses a **traitlets-based state synchronization** model:

```
Python (traitlets) <--Comm Protocol--> JavaScript (model.get/set)
```

**Python Side:**
```python
import anywidget
import traitlets

class CodeCityWidget(anywidget.AnyWidget):
    _esm = """... JavaScript code ..."""
    buildings = traitlets.List().tag(sync=True)  # Full JSON sync
    edges = traitlets.List().tag(sync=True)
```

**JavaScript Side (AFM):**
```javascript
export default {
  render({ model, el }) {
    // model.get("buildings") - read synced data
    // model.on("change:buildings", callback) - react to changes
    // model.set("selected", id); model.save_changes() - write back to Python
  }
}
```

### Serialization Overhead

| Data Type | Mechanism | Overhead |
|-----------|-----------|----------|
| JSON properties | `traitlets.*.tag(sync=True)` | Full serialization via Comm |
| Binary data | `traitlets.Bytes().tag(sync=True)` | Zero-copy buffer transfer |
| Custom messages | `model.send(content, callbacks, buffers)` | Direct binary buffers |

**Key Finding:** For large datasets (>10K points), use `traitlets.Bytes()` to avoid JSON serialization overhead.

---

## 2. Performance Characteristics

### Latency

Based on marimo's implementation and anywidget's Comm protocol:

| Operation | Expected Latency | Notes |
|-----------|-----------------|-------|
| Property sync (JSON) | 10-50ms | Depends on data size |
| Binary buffer transfer | 1-10ms | Near-zero overhead |
| Custom message round-trip | 5-20ms | Async, not blocking |

**Real-time animation consideration:** The Comm protocol is **not designed for 60fps data streaming**. Each property change triggers a full sync cycle. For Code City:

- **Static/interactive visualization:** ✅ Works well
- **60fps particle animation:** ⚠️ May struggle - need to test

### 10K+ Data Points

**Verified support exists:**
- `lonboard` handles large geospatial datasets with WebGL
- `ipyniivue` renders millions of voxels
- Binary transfer via `traitlets.Bytes()` avoids JSON overhead

**Recommendation:** Use binary buffers for building/edge data if >1K items.

### Binary Data Support (TypedArrays)

**Verified in marimo tests** (`test_anywidget.py` line 299-318):

```python
class BufferWidget(anywidget.AnyWidget):
    _esm = ""
    array = traitlets.Bytes().tag(sync=True)

data = bytes([1, 2, 3, 4])
wrapped = anywidget(BufferWidget(array=data))
```

The frontend receives `ArrayBuffer` directly - no base64 encoding.

---

## 3. 3D/Canvas Rendering

### Can anywidget embed Three.js/WebGL canvases?

**YES - Proven by existing packages:**

| Package | Stars | Technology | Use Case |
|---------|-------|------------|----------|
| [ipyniivue](https://github.com/niivue/ipyniivue) | 45 | WebGL | 3D medical imaging |
| [threey](https://github.com/kelreeeeey/threey) | 11 | Three.js | 3D seismic data |
| [ipymolstar](https://github.com/molstar/ipymolstar) | 50 | Mol* (WebGL) | Molecular visualization |
| [lonboard](https://github.com/developmentseed/lonboard) | 907 | deck.gl/WebGL | Geospatial mapping |
| [mapwidget](https://github.com/opengeos/mapwidget) | 250 | Cesium/Mapbox | 2D/3D maps |

### Code Example: Three.js Integration

```python
import anywidget
import traitlets

class ThreeJSWidget(anywidget.AnyWidget):
    _esm = """
    import * as THREE from "https://esm.sh/three@0.160.0";
    
    function render({ model, el }) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, el.clientWidth / el.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(el.clientWidth, el.clientHeight);
        el.appendChild(renderer.domElement);
        
        // Read building data from Python
        const buildings = model.get("buildings");
        // ... create 3D meshes
        
        // Animation loop (runs client-side, no Python overhead)
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
        
        // React to data changes
        model.on("change:buildings", () => {
            // Update meshes
        });
    }
    export default { render };
    """
    
    buildings = traitlets.List().tag(sync=True)
    
widget = ThreeJSWidget(buildings=[...])
```

### Known Limitations

1. **No direct GPU buffer sharing** - Data still goes through Comm (unlike your current WebGPU approach)
2. **Animation must run client-side** - The render loop runs in browser; Python updates trigger re-renders
3. **Bundle size** - Large JS dependencies increase load time (use CDN imports for prototyping)

---

## 4. Integration with marimo

### Native Support

marimo has **first-class anywidget support**:

```python
import marimo as mo
import anywidget

class MyWidget(anywidget.AnyWidget):
    _esm = "..."
    
widget = MyWidget()
wrapped = mo.ui.anywidget(widget)  # ✅ Native integration
```

**Verified in marimo tests** - `mo.ui.anywidget()` wraps anywidget instances.

### marimo-Specific Considerations

1. **Frontend implementation:** marimo uses a custom model implementation (no Backbone dependency)
2. **HMR support:** Available via `ANYWIDGET_HMR=1` environment variable
3. **Installation:** Requires `pip install anywidget` (already in project)

### Installation/Usage Pattern

```bash
pip install anywidget traitlets
```

```python
# In orchestr8.py or plugin
from IP.plugins.my_code_city import CodeCityWidget

widget = CodeCityWidget(buildings=data, edges=connections)
code_city_ui = mo.ui.anywidget(widget)
```

---

## 5. Comparison: Current WebGPU vs anywidget

| Aspect | Current WebGPU | anywidget |
|--------|---------------|------------|
| Rendering | Direct WebGPU compute shaders | WebGL via Three.js |
| Data transfer | GPU buffer sharing | Comm protocol (JSON/buffer) |
| Animation | GPGPU (full GPU) | Client-side requestAnimationFrame |
| 60fps streaming | ✅ Native | ⚠️ Via Comm (potential bottleneck) |
| Code City complexity | Custom GLSL | Three.js primitives |
| Dependencies | None (raw WebGPU) | anywidget + Three.js |
| Debugging | Complex | Standard browser devtools |

---

## 6. Recommendations for Code City

### When anywidget is the RIGHT choice:

1. **Interactive exploration** - Clicking buildings, hovering for tooltips
2. **Python-driven updates** - When data changes from Python, widget updates
3. **Standard visualizations** - Buildings, edges, basic animations
4. **Ecosystem integration** - Leverages existing Three.js ecosystem

### When to KEEP current WebGPU:

1. **High-frequency particle animation** - If you need 60fps physics simulation
2. **Massive datasets** - If GPU buffer sharing is critical for performance
3. **Custom compute** - If you're doing non-visual GPGPU work

### Hybrid Approach

Consider using anywidget for the **structure** (buildings, edges, interactive elements) while keeping WebGPU for **particle effects** that don't need Python coordination:

```python
class HybridCodeCity(anywidget.AnyWidget):
    _esm = """
    // Three.js for buildings/interaction
    // WebGPU canvas overlay for particles
    // Communication via model.get/set
    """
    buildings = traitlets.List().tag(sync=True)
    selected = traitlets.Unicode().tag(sync=True)
```

---

## 7. Version Considerations

- **anywidget:** Current version 0.9.21 (November 2025)
- **traitlets:** Required dependency, ships with anywidget
- **marimo:** Has native anywidget integration (verified in tests)
- **Node.js:** ESM imports require modern browser (Chrome 89+, Firefox 90+, Safari 15+)

---

## Sources

- [anywidget.dev Documentation](https://anywidget.dev/) - Primary source
- [anywidget GitHub](https://github.com/manzt/anywidget) - 852 stars, 62 forks
- [AFM Specification](https://anywidget.dev/en/afm/) - Architecture details
- [marimo anywidget tests](marimo/tests/_plugins/ui/_impl/test_anywidget.py) - Integration verification
- [lonboard](https://github.com/developmentseed/lonboard) - WebGL example (907 stars)
- [ipyniivue](https://github.com/niivue/ipyniivue) - WebGL example (45 stars)
- [threey](https://github.com/kelreeeeey/threey) - Three.js example (11 stars)

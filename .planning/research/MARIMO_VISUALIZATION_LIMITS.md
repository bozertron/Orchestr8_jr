# Marimo Visualization Limits Research

**Project:** Orchestr8  
**Researched:** 2026-02-13  
**Confidence:** HIGH

## Executive Summary

Marimo provides rich native visualization capabilities through built-in integrations with Altair, Plotly, and Matplotlib. However, **3D rendering is not natively supported** - it requires custom solutions via anywidget or HTML/iframe embedding. The platform has practical data limits: ~20,000 rows for Altair (expandable to 400K with CSV transformer), ~5MB message size soft limit for outputs. Custom JavaScript/Canvas is fully supported through `mo.Html()`, `mo.iframe()`, and anywidget.

---

## 1. Native Output Types

### 1.1 Built-in Charting Libraries

| Library | Support | Reactive | Notes |
|---------|---------|----------|-------|
| **Altair** | `mo.ui.altair_chart()` | Yes | Auto-selection, data transformers |
| **Plotly** | `mo.ui.plotly()` | Partial | Scatter, bar, heatmap, treemap, sunburst only |
| **Matplotlib** | `mo.mpl.interactive()` | No | Pan/zoom viewer only |
| **Seaborn** | Via matplotlib | No | Renders as static image |

**Source:** [marimo plotting API](https://docs.marimo.io/api/plotting.html)

### 1.2 3D Content

**Verdict: NOT natively supported**

Marimo has no built-in 3D visualization components. Options:
1. **anywidget** - Custom JS widgets with Three.js
2. **iframe embedding** - Render 3D in separate document
3. **mo.Html()** - Inline HTML with canvas elements

### 1.3 Media Types

| Type | Component | Notes |
|------|-----------|-------|
| Images | `mo.ui.image()` | URL or base64 |
| Audio | `mo.ui.audio()` | Various formats |
| Video | `mo.ui.video()` | Various formats |
| PDFs | `mo.ui.pdf()` | Embed viewer |

---

## 2. Performance Benchmarks

### 2.1 Data Size Limits

| Library | Default Limit | Configurable | Notes |
|---------|---------------|--------------|-------|
| Altair | 20,000 rows | Yes | Uses `marimo_csv` transformer for 400K+ |
| Plotly | No explicit limit | No | Browser-dependent |
| Matplotlib | N/A | N/A | Static output |
| Generic HTML | ~5MB soft limit | Environment var | WebSocket message size |

**Altair Performance:**
- Default: 20,000 rows (marimo patches default of 5,000)
- With `alt.data_transformers.enable('marimo_csv')`: 400,000+ rows
- CSV transformer is automatic with `mo.ui.altair_chart()`

**Source:** [marimo plotting performance](https://docs.marimo.io/api/plotting.html#performance-and-data-transformers)

### 2.2 Render Time Estimates

| Output Type | Estimated Time | Notes |
|-------------|----------------|-------|
| Altair chart (1K rows) | <100ms | JSON serialization dominant |
| Altair chart (20K rows) | 200-500ms | With CSV transformer |
| Plotly scatter (10K points) | 100-300ms | Client-side rendering |
| Matplotlib figure | 50-200ms | Static SVG/PNG |
| Custom HTML iframe | Depends on content | Out of marimo scope |

### 2.3 Interactivity Limits

| Library | Selection | Zoom/Pan | Animations |
|---------|-----------|----------|------------|
| Altair | Yes (point/interval) | Yes | Limited |
| Plotly | Yes (subset) | Yes | Yes |
| Matplotlib | No | Yes (viewer) | No |
| Custom (anywidget) | Full control | Full control | Full control |

---

## 3. HTML/Canvas in Marimo

### 3.1 Embedding Mechanisms

#### mo.Html() - Direct HTML
```python
mo.Html("<canvas id='mycanvas'></canvas>")
```
- Renders raw HTML in output
- Scripts NOT executed by default (security)
- CSS isolation not provided

#### mo.iframe() - Sandboxed iframe
```python
mo.iframe("<canvas id='mycanvas'></canvas>", height="600px")
```
- Executes scripts (unlike mo.Html)
- Sandboxed: `allow-scripts`, no same-origin
- Recommended for 3D/Canvas content

#### mo.as_html() - Object conversion
```python
mo.as_html(matplotlib_figure)
```
- Converts objects to HTML representation
- Used for embedding in markdown

### 3.2 Custom JavaScript

**Two approaches:**

1. **anywidget** (recommended for reactive):
```python
import anywidget
import traitlets

class CanvasWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        const canvas = document.createElement('canvas');
        // Three.js or custom rendering
        el.appendChild(canvas);
    }
    export default { render };
    """
    data = traitlets.Dict().tag(sync=True)

widget = mo.ui.anywidget(CanvasWidget())
```

2. **Inline via iframe** (Orchestr8 approach):
```python
html = """
<canvas id='c'></canvas>
<script>
// Full Three.js setup
</script>
"""
mo.iframe(html)
```

### 3.3 Performance Penalties

| Method | Overhead | Data Transfer |
|--------|----------|---------------|
| mo.Html() | Minimal | Full payload per update |
| mo.iframe() | ~10-50ms | Isolated, smaller delta |
| anywidget | Minimal | Trait sync only |

**Orchestr8's approach** uses iframe with streaming to avoid marimo message size limits.

---

## 4. Third-Party Visualization Integration

### 4.1 Compatible Libraries

| Library | Integration | Reactive | Notes |
|---------|-------------|----------|-------|
| **Three.js** | anywidget/iframe | Yes | Full 3D support |
| **Leafmap** | Built-in | No | Map visualization |
| **PyDeck** | Plotly deck.gl | No | Deck.gl via Plotly |
| **VisPy** | Indirect | No | GPU via anywidget |
| **PyVista** | Indirect | No | 3D via anywidget |

### 4.2 anywidget Compatibility

**Verified working:**
- drawdata ( ScatterWidget)
- quak (earthquake visualization)
- wigglystuff widgets

**Requirements:**
- Python anywidget package
- ESM/JavaScript frontend code
- Traitlets for state sync

### 4.3 Three.js Integration

Three.js works via:
1. **anywidget** - Direct integration with Python state
2. **iframe** - Full isolation (current Orchestr8 approach)

**Pros/Cons:**
| Approach | Pros | Cons |
|----------|------|------|
| anywidget | Reactive, stateful | More setup, traitlets |
| iframe | Simpler, full JS freedom | No direct Python state |

---

## 5. Known Limitations & Pitfalls

### 5.1 Critical Limits

1. **Output Size**
   - Soft limit: ~5MB per message (WebSocket)
   - Hard limit: Not publicly documented but enforced
   - **Orchestr8 observed:** 9MB triggers guard

2. **No Native 3D**
   - Must use custom solutions
   - iframe or anywidget required

3. **Plotly Reactive Limitations**
   - Only scatter, bar, heatmap, treemap, sunburst support selection
   - Other chart types render but aren't reactive

### 5.2 Performance Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Large DataFrame in Altair | Slow render, possible crash | Use CSV transformer |
| Frequent cell updates | UI lag | Use lazy execution |
| Large HTML payloads | WebSocket errors | Chunk/stream (Orchestr8 solution) |
| Inline scripts in mo.Html | Not executed | Use mo.iframe() |

---

## 6. Recommendations for Orchestr8

### Current Approach (Verified Working)

The Orchestr8 project uses iframe embedding with streaming:
- `mo.iframe()` for Code City 3D visualization
- Payload size guard at ~9MB
- Streaming for large 3D data (5MB/sec)
- Client-side Three.js generation

This approach is correct for:
- Large visualizations exceeding marimo limits
- 3D content requiring WebGL
- Interactive content with complex state

### Alternative: anywidget

For new custom visualizations, consider anywidget:
- Native reactive integration
- Smaller payload (just trait changes)
- Better for interactive tools

**Choose anywidget when:**
- Visualization is interactive but not 3D
- State needs to sync with Python
- Data fits within message limits

---

## 7. Sources

- [marimo Plotting API](https://docs.marimo.io/api/plotting.html) - HIGH confidence
- [marimo Inputs/AnyWidget](https://docs.marimo.io/api/inputs/anywidget.html) - HIGH confidence
- [marimo HTML API](https://docs.marimo.io/api/html.html) - HIGH confidence
- [marimo Outputs API](https://docs.marimo.io/api/outputs.html) - HIGH confidence
- [Altair Data Transformers](https://altair-viz.github.io/user_guide/data_transformers.html) - MEDIUM confidence (external)
- Orchestr8 implementation patterns - HIGH confidence (direct observation)

---

## Research Flags

| Flag | Area | Action |
|------|------|--------|
| 3D visualization | Native limits | Verify anywidget + Three.js works for complex cases |
| Message size hard limit | Performance | Test actual limits with Code City payload |
| anywidget + Three.js | Integration | Consider for future visualization features |


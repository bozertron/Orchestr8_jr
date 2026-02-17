# Rendering Tradeoffs Analysis: Custom Canvas vs Native Alternatives

**Project:** Orchestr8  
**Researched:** 2026-02-13  
**Confidence:** HIGH

## Executive Summary

**The custom WebGPU/Three.js canvas in Orchestr8 is justified for the Code City 3D visualization but likely over-engineered for the 2D wiring diagram use case.**

The current implementation provides:
- Full 3D rendering with particle emergence animations
- Up to 1M GPU particles / 180K CPU particles
- Camera controls (orbit, pan, zoom, warp-dive)
- Post-processing (bloom, fog)
- Real-time animations (emergence, status transitions)

**However**, for the "wired connections" visualization specifically (the edge/import graph), alternatives exist that could reduce complexity significantly while maintaining interactivity.

---

## 1. Current Implementation Analysis

### 1.1 What the Custom Canvas Renders

| Feature | Implementation | Complexity |
|---------|---------------|------------|
| **Buildings** | Three.js particle systems (Barradeau technique) | Very High |
| **Particles** | WebGPU compute shaders / CPU canvas fallback | High |
| **Edges/Wiring** | Three.js LineSegments with custom shaders | High |
| **Camera** | OrbitControls with keyframe transitions | Medium |
| **Post-processing** | UnrealBloomPass, fog | Medium |
| **Interactivity** | Raycasting for hover/click, warp-dive | High |

**Source:** `IP/static/woven_maps_3d.js` (1200+ lines)

### 1.2 Computational Costs

| Metric | CPU Mode | GPU Mode | Source |
|--------|----------|----------|--------|
| **Particle cap** | 180,000 | 1,000,000 | `IP/woven_maps.py:216-217` |
| **Frame spawn rate** | 280/frame | 700/frame | `IP/woven_maps.py:218-219` |
| **Mesh layers** | 18 | 18 | `IP/woven_maps.py:220` |
| **Pixel ratio cap** | N/A | 2x | Compatibility doc |
| **Stream bandwidth** | N/A | 5MB/sec default | `ORCHESTR8_CODE_CITY_STREAM_BPS` |

**Memory estimate:**
- 100 files × ~2000 particles/file = 200K particles
- Each particle: 3 floats (position) + 1 float (opacity) + 1 float (size) = 20 bytes
- 200K × 20 bytes = ~4MB GPU memory for particles alone

### 1.3 Interactivity Capabilities

| Interaction | Supported | Implementation |
|-------------|-----------|----------------|
| Hover (tooltip) | ✅ | Raycasting + HTML overlay |
| Click (select) | ✅ | Raycasting + state callback |
| Pan | ✅ | OrbitControls |
| Zoom | ✅ | OrbitControls |
| Warp dive | ✅ | Custom camera animation |
| Multi-select | ❌ | Not implemented |
| Drag nodes | ❌ | Not implemented |

---

## 2. Marimo Native Alternatives

### 2.1 What's Available Natively

| Component | 3D Support | Interactive | Performance |
|-----------|------------|-------------|-------------|
| `mo.ui.altair_chart()` | ❌ 2D only | Partial | 20K rows default |
| `mo.ui.plotly()` | ❌ 2D only | Yes | 10K points |
| `mo.mpl.interactive()` | ❌ 2D only | Limited | Static render |
| `mo.ui.dataframe()` | N/A | Yes | 100K rows |
| `mo.ui.table()` | N/A | Yes | Pagination |

**Source:** [marimo Plotting API](https://docs.marimo.io/api/plotting.html) - HIGH confidence

### 2.2 Can Native Components Handle 3D/Flexible Layout?

**Verdict: NO.**

Marimo has **no native 3D support**. The documentation explicitly states this requires custom solutions via anywidget or iframe embedding.

For 2D network graphs specifically:
- Altair: Limited to scatter plots with custom encoding
- Plotly: Has network graph support but not fully reactive in marimo
- Neither provides the "Code City" 3D metaphor

### 2.3 Performance Ceiling for Native Outputs

| Output Type | Practical Limit | Over Limit Behavior |
|-------------|-----------------|---------------------|
| Altair | 20K rows (400K with CSV) | Slow render / crash |
| Plotly scatter | ~10K points | Browser-dependent |
| Generic HTML | ~5MB message | WebSocket error |
| Custom iframe | Unlimited (chunked) | Works with streaming |

**Source:** Existing research in `.planning/research/MARIMO_VISUALIZATION_LIMITS.md` - HIGH confidence

---

## 3. anywidget Alternatives

### 3.1 Can anywidget Replace Canvas Rendering?

**Yes, but with caveats.**

anywidget provides:
- Python ↔ JavaScript state sync via traitlets
- Full Three.js/WebGL access
- Reactive updates (state changes propagate automatically)

**Architecture comparison:**

| Aspect | Current iframe | anywidget |
|--------|---------------|-----------|
| State sync | Manual (postMessage) | Automatic (traitlets) |
| Initial load | Large payload | Smaller, incremental |
| Real-time animation | Full control | Full control |
| Python callbacks | Indirect | Direct |
| Complexity | Higher | Lower |

### 3.2 Data Transfer Overhead

| Scenario | Current iframe | anywidget |
|----------|----------------|-----------|
| Initial render | Full JSON (~1MB) | Full JSON |
| Update (hover) | postMessage (~1KB) | Trait sync (~500B) |
| Update (click) | postMessage + cell re-run | Trait sync only |

**Estimated reduction:** 60-80% fewer bytes for interactive updates

### 3.3 Can it Handle Real-Time Particle Animations?

**Yes**, anywidget can run Three.js just like the current iframe approach. The difference is architectural, not capability.

```python
# Example: anywidget with Three.js
class ThreeWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        // Full Three.js setup here
        const scene = new THREE.Scene();
        // ... particles, buildings, etc.
    }
    """
    buildings = traitlets.Dict().tag(sync=True)
```

**Source:** [anywidget.dev](https://anywidget.dev/) - HIGH confidence

---

## 4. Feature-Specific Analysis

### 4.1 Buildings (Code City Visualization)

| Approach | Capability | Cost | Recommendation |
|---------|-----------|------|----------------|
| **Current (Three.js)** | Full 3D, particles, emergence | Very High | ✅ Keep |
| anywidget + Three.js | Identical | High | ✅ Alternative |
| Native marimo | ❌ Not possible | N/A | ❌ Reject |

**Verdict: KEEP** - The 3D building visualization requires custom rendering. The emergence animation (particles coalescing) is a signature feature that cannot be replicated with native tools.

### 4.2 Particles (Emergence Animation)

| Approach | Capability | Cost | Recommendation |
|---------|-----------|------|----------------|
| **Current (WebGPU)** | 1M particles, curl noise | Very High | ✅ Keep |
| Current (CPU fallback) | 180K particles | High | ✅ Keep |
| anywidget + Three.js | Identical | High | ✅ Alternative |
| Plotly | ~10K points max | Medium | ❌ Reject |

**Verdict: KEEP** - The emergence animation is central to Orchestr8's aesthetic. However, consider migrating to anywidget for better Python integration.

### 4.3 Connections/Wiring (Import Graph)

| Approach | Capability | Cost | Recommendation |
|---------|-----------|------|----------------|
| **Current (Three.js)** | 3D lines, hover, click | High | ⚠️ Overkill |
| **NetworkX + Pyvis** | 2D interactive graph | Low | ✅ Consider |
| **D3 via anywidget** | 2D/2.5D force-directed | Medium | ✅ Consider |
| **Plotly network** | Basic 2D graph | Low | ⚠️ Limited |

**Analysis:**

The current implementation renders edges as 3D line segments with:
- Custom shaders for glow effects
- Raycasting for hover detection
- Color coding (working/broken/combat)

**However**, this is essentially a 2D graph rendered in 3D space. For the import graph:

| Requirement | Current | Pyvis | D3 |
|-------------|---------|-------|-----|
| Node positioning | 3D grid | Force-directed | Force-directed |
| Edge rendering | 3D lines | 2D arrows | 2D/curved |
| Hover tooltips | ✅ | ✅ | ✅ |
| Click navigation | ✅ | ✅ | ✅ |
| Zoom/pan | ✅ | ✅ | ✅ |
| Status colors | ✅ | ✅ | ✅ |
| Real-time updates | Manual | Manual | Manual |

**Recommendation: Consider Pyvis or D3 for wiring diagram**

Pyvis generates interactive HTML that works in iframe:
```python
from pyvis.network import Network
net = Network()
net.from_nx(graph)
net.save_graph("graph.html")
```

**Source:** [Pyvis docs](https://pyvis.readthedocs.io/) - MEDIUM confidence

---

## 5. Alternative Approaches Ranked

### For 3D Code City (Buildings + Particles)

| Rank | Approach | Capability | Cost | Notes |
|------|----------|------------|------|-------|
| 1 | **Current iframe** | Full 3D, particles, emergence | High | Already implemented, working |
| 2 | anywidget + Three.js | Identical | High | Better Python integration, simpler state |
| 3 | Native marimo | ❌ | N/A | Not possible |

### For 2D Wiring Diagram (Edges/Connections)

| Rank | Approach | Capability | Cost | Notes |
|------|----------|------------|------|-------|
| 1 | **Pyvis** | Interactive 2D | Low | Simple, HTML output |
| 2 | D3 via anywidget | Interactive 2D/2.5D | Medium | Full customization |
| 3 | **Current Three.js** | 3D lines | High | Over-engineered for 2D data |
| 4 | Plotly network | Basic 2D | Low | Limited interactivity |

---

## 6. Specific Recommendations

### 6.1 For Buildings (Keep Current)

**Recommendation: Keep current implementation OR migrate to anywidget**

```python
# Option A: Keep as-is (current iframe approach)
# Pros: Working, proven
# Cons: Manual state management

# Option B: Migrate to anywidget
# Pros: Better Python integration, automatic state sync
# Cons: Requires rewrite
```

### 6.2 For Particles (Keep Current)

**Recommendation: Keep current implementation**

The emergence animation is Orchestr8's signature visual. No native alternative can replicate it.

### 6.3 For Connections (Consider Alternative)

**Recommendation: Consider Pyvis or D3 for wiring diagram**

If the goal is simply to visualize import relationships:

```python
# Pyvis approach (simple, proven)
from pyvis.network import Network
import networkx as nx

G = nx.DiGraph()
# Add nodes (files) and edges (imports)
for node in nodes:
    G.add_node(node.path, color=status_color)
for edge in edges:
    G.add_edge(edge.source, edge.target)

net = Network()
net.from_nx(G)
net.save_graph("wiring.html")

# Display in marimo
mo.iframe("wiring.html", height="600px")
```

**Benefits:**
- 80%+ code reduction (no custom WebGL)
- Native hover tooltips
- Built-in zoom/pan
- Force-directed layout (better for finding clusters)
- Easier maintenance

**Tradeoffs:**
- Loses 3D positioning (could be mitigated with 3D→2D projection)
- No warp-dive animation
- Different aesthetic

---

## 7. Verdict: Is the Custom Canvas Worth It?

### For Code City (3D Buildings + Particles)

**YES** — The custom canvas is justified.

**Rationale:**
1. **No native alternative exists** for 3D particle-based visualization
2. The emergence animation is a **signature feature** of Orchestr8
3. Performance is acceptable (1M GPU / 180K CPU particles)
4. The implementation is working and battle-tested

**However**, consider migrating to anywidget for:
- Simpler Python ↔ JS state management
- Better reactivity
- Smaller update payloads

### For Wiring Diagram (2D Edges)

**NO** — Over-engineered.

**Rationale:**
1. Edges are essentially 2D data (import relationships)
2. Rendering them in 3D adds complexity without value
3. Pyvis/D3 can achieve 90% of functionality at 20% of cost
4. The 3D line rendering is essentially visual flourish

**Recommendation:** Create a separate 2D wiring view using Pyvis, keep the 3D Code City as-is.

---

## 8. Migration Path (Optional)

If deciding to migrate to anywidget for better integration:

### Phase 1: Anywidget Wrapper
- Wrap current Three.js in anywidget class
- Keep all existing rendering logic
- Add traitlets for state sync

### Phase 2: Wiring Diagram Replacement
- Create separate Pyvis/D3 component for edges
- Keep 3D Code City for buildings

### Phase 3: Deprecate iframe
- Once anywidget is stable, remove iframe path
- Simplify codebase

---

## 9. Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Current implementation analysis | HIGH | Direct code inspection |
| Computational costs | HIGH | Config values from source |
| Marimo native alternatives | HIGH | Verified against official docs |
| anywidget capabilities | HIGH | Official docs + existing research |
| Pyvis/D3 alternatives | MEDIUM | External library, not tested in Orchestr8 |
| Recommendations | MEDIUM | Tradeoff analysis, opinionated |

---

## 10. Sources

### Primary Sources (HIGH Confidence)
- `IP/woven_maps.py` - Configuration and Python logic
- `IP/static/woven_maps_3d.js` - Three.js rendering (1200+ lines)
- [marimo Plotting API](https://docs.marimo.io/api/plotting.html)
- [marimo AnyWidget](https://docs.marimo.io/api/inputs/anywidget.html)
- `.planning/research/MARIMO_VISUALIZATION_LIMITS.md` - Existing research

### Secondary Sources (MEDIUM Confidence)
- [Pyvis Documentation](https://pyvis.readthedocs.io/)
- [NetworkX Gallery](https://networkx.org/documentation/stable/auto_examples/index.html)
- [anywidget.dev](https://anywidget.dev/)

---

## 11. Open Questions

1. **Warp-dive requirement**: Does the wiring diagram need warp-dive animation, or is click-to-navigate sufficient?
2. **3D positioning**: Are the 3D positions of buildings (x, z based on directory structure) important for understanding, or could 2D work?
3. **Performance tolerance**: If Pyvis shows 1000 nodes with lag, is that acceptable, or is 60fps required?

These answers would refine the recommendations above.

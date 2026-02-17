# Visual & Rendering Research: Complete Synthesis

**Generated:** 2026-02-16  
**Sources:** 12 research files, 1 canonical token lock  
**Confidence:** HIGH

---

## Executive Summary

This document synthesizes all visual and rendering research for the Orchestr8 project. The system uses a **dual-layer visual architecture**: CSS tokens for UI chrome and custom WebGPU/Three.js for Code City 3D visualization. The visual token system is locked and canonical (VISUAL_TOKEN_LOCK.md), while the rendering pipeline has been battle-tested but carries technical debt in the wiring diagram layer.

### Key Findings

1. **Visual Tokens are Canonical** — All colors, typography, and dimensions are locked in `SOT/VISUAL_TOKEN_LOCK.md` and implemented in `IP/styles/orchestr8.css`
2. **3D Code City is Justified** — No native alternative can replicate the emergence animation; custom WebGPU/Three.js is required
3. **Wiring Diagram is Over-Engineered** — 2D import relationships rendered as 3D lines; Pyvis/D3 could reduce complexity by 80%
4. **Health→Color Pipeline Has Gaps** — Warnings not propagated, neighborhood combat status bug exists
5. **Node Click Integration Works** — Full payload pipeline from JS→Python exists, but no Summon handoff

---

## Part I: Visual Token System

### 1.1 Canonical Source of Truth

**VISUAL_TOKEN_LOCK.md** is the immutable registry for all visual design tokens. Changes require Founder approval.

| Token Category | Location | Status |
|----------------|----------|--------|
| Color Tokens | `SOT/VISUAL_TOKEN_LOCK.md:12-40` | LOCKED |
| Typography Tokens | `SOT/VISUAL_TOKEN_LOCK.md:42-70` | LOCKED |
| Spacing Tokens | `SOT/VISUAL_TOKEN_LOCK.md:72-81` | LOCKED |
| Dimension Tokens | `SOT/VISUAL_TOKEN_LOCK.md:83-100` | LOCKED |
| Effect Tokens | `SOT/VISUAL_TOKEN_LOCK.md:102-109` | LOCKED |
| Animation Tokens | `SOT/VISUAL_TOKEN_LOCK.md:111-118` | LOCKED |

**Implementation Files:**
| File | Purpose |
|------|---------|
| `IP/styles/orchestr8.css` | CSS variable definitions (MUST match tokens) |
| `IP/styles/font_profiles.py` | Font injection based on `ui.general.font_profile` setting |
| `IP/plugins/06_maestro.py` | Main render, reads tokens and applies them |

### 1.2 Color Token Definitions

#### Primary Palette (LOCKED)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `--bg-obsidian` | #050505 | 5,5,5 | Background base |
| `--gold-dark` | #C5A028 | 197,160,40 | Primary accent, borders |
| `--gold-light` | #F4C430 | 244,196,48 | Highlight accent, hover |
| `--teal` | #00E5E5 | 0,229,229 | Secondary accent, text |
| `--text-grey` | #CCC | 204,204,204 | Standard text |

#### State Colors (LOCKED)

| State | Token | Hex | Visualization |
|-------|-------|-----|---------------|
| Working | `--state-working` | #D4AF37 | Gold buildings |
| Broken | `--state-broken` | #1fbdea | Blue buildings |
| Combat | `--state-combat` | #9D4EDD | Purple buildings |

### 1.3 Typography Token Definitions (LOCKED)

| Token | Value | Weight | Usage |
|-------|-------|--------|-------|
| `--font-header` | 'Marcellus SC', serif | 400 | Major headers, top buttons |
| `--font-ui` | 'Poiret One', cursive | 400 | UI labels, mini buttons |
| `--font-data` | 'VT323', monospace | 400 | Data, status, terminal |

### 1.4 Dimension Token Definitions (LOCKED)

| Token | Value | Usage |
|-------|-------|-------|
| `--header-height` | 80px | Header section |
| `--top-btn-height` | 50px | Top navigation buttons |
| `--top-btn-min-width` | 160px | Top button minimum width |
| `--btn-mini-height` | 22px | Footer mini buttons |
| `--btn-mini-min-width` | 60px | Mini button minimum width |
| `--btn-maestro-height` | 36px | MAESTRO button |

### 1.5 Token Verification Flow

```
orchestr8.py (Entry Point)
    ↓
Loads SOT/VISUAL_TOKEN_LOCK.md at startup
    ↓
Parses IP/styles/orchestr8.css variables
    ↓
verify_token_alignment() checks CSS matches canonical
    ↓
Initializes button I/O provisioning
    ↓
Renders IP/plugins/06_maestro.py
```

---

## Part II: Rendering Pipeline

### 2.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RENDERING LAYERS                             │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 1: CSS Tokens (orchestr8.css)                               │
│  → UI chrome, buttons, layout, typography                          │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 2: Three.js Canvas (woven_maps_3d.js)                      │
│  → 3D Code City, particles, edges                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 3: Data Bridge (JavaScript ↔ Python)                       │
│  → postMessage, state sync, node clicks                           │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Three.js Rendering Details

**Source:** `IP/static/woven_maps_3d.js` (1200+ lines)

| Feature | Implementation | Complexity |
|---------|---------------|------------|
| Buildings | Three.js particle systems (Barradeau technique) | Very High |
| Particles | WebGPU compute shaders / CPU canvas fallback | High |
| Edges/Wiring | Three.js LineSegments with custom shaders | High |
| Camera | OrbitControls with keyframe transitions | Medium |
| Post-processing | UnrealBloomPass, fog | Medium |
| Interactivity | Raycasting for hover/click, warp-dive | High |

### 2.3 Performance Specifications

| Metric | CPU Mode | GPU Mode | Config Variable |
|--------|----------|----------|-----------------|
| Particle cap | 180,000 | 1,000,000 | — |
| Frame spawn rate | 280/frame | 700/frame | — |
| Mesh layers | 18 | 18 | — |
| Pixel ratio cap | N/A | 2x | Compatibility |
| Stream bandwidth | N/A | 5MB/sec | `ORCHESTR8_CODE_CITY_STREAM_BPS` |

**Payload Guard:** Code City output has oversized payload guard at ~9MB (`ORCHESTR8_CODE_CITY_MAX_BYTES`)

### 2.4 GPU-First with CPU Fallback

From `IP/woven_maps.py`:
```python
initParticleBackend() checks navigator.gpu
    → Uses WebGPU when available
    → Falls back to CPU canvas on failure
```

---

## Part III: Health Check to Color Pipeline

### 3.1 Transformation Chain

```
HealthChecker (static analysis)
    ↓
HealthCheckResult {status, errors, warnings, ...}
    ↓
build_from_health_results() merges into CodeNode
    ↓
CodeNode.status determines color via get_status_color()
    ↓
Woven Maps renders colored buildings
```

### 3.2 Color Mapping

From `IP/contracts/status_merge_policy.py:36-43`:

| Status | Hex Color | Name | Source |
|--------|-----------|------|--------|
| working | #D4AF37 | Gold | No errors detected |
| broken | #1fbdea | Teal/Blue | Errors detected |
| combat | #9D4EDD | Purple | LLM actively deployed |

### 3.3 Priority Chain (merge_status)

```python
STATUS_PRIORITY = {
    "combat": 3,   # Highest - LLM active overrides all
    "broken": 2,   # Second - errors present
    "working": 1,  # Lowest - clean code
}
```

### 3.4 Identified Gaps

| Gap | Severity | Description |
|-----|----------|-------------|
| **Warnings Not Propagated** | HIGH | `HealthCheckResult.warnings` is never merged into CodeNode |
| **Neighborhood Combat Bug** | HIGH | Line 69-70: `if status_counts["combat"] > 0: status = "broken"` — should be "combat" |
| **Missing Metadata** | MEDIUM | Column, error_code, severity not passed to frontend |

---

## Part IV: Node Click Integration

### 4.1 JavaScript → Python Payload

From `woven_maps_template.html`:
```javascript
window.parent.postMessage({
    type: 'WOVEN_MAPS_NODE_CLICK',
    node: {
        path: string,
        status: "working" | "broken" | "combat",
        loc: number,
        errors: string[],
        nodeType: string,
        centrality: number,
        inCycle: boolean,
        // ... more fields
    }
}, '*')
```

### 4.2 Python Processing Pipeline

```
on_node_click_bridge_change(payload_json)
    ↓
process_node_click(payload)
    ↓
validate_code_city_node_event() → CodeCityNodeEvent contract
    ↓
handle_node_click(node_data)
    ↓
carl.gather_context(scope) → FiefdomContext
    ↓
build_code_city_context_payload() → Full context dict
    ↓
set_code_city_context() → State storage
```

### 4.3 Panel Selection by Status

| Status | Panel Shown | Location |
|--------|-------------|----------|
| broken | DeployPanel | 06_maestro.py:448-509 |
| combat | Status message | 06_maestro.py:511-518 |
| working | Building info | 06_maestro.py:520-522 |

### 4.4 Context Payload Structure

```python
{
    "path": str,
    "status": str,
    "context_scope": str,
    "building_panel": { /* Full building inspection */ },
    "room_entry": { /* Selected room */ } | None,
    "sitting_room": { /* Sitting room handoff */ } | None
}
```

### 4.5 Integration Gaps

| Gap | Description | Impact |
|-----|-------------|--------|
| **No node→Summon handoff** | Clicking node doesn't prepopulate Summon | Can't use node context in AI search |
| **No Sitting Room auto-entry** | `sitting_room` config exists but not always used | Room-level inspection incomplete |
| **No cross-file context** | Only single file context | Missing broader system understanding |

---

## Part V: anywidget & Native Alternatives

### 5.1 Marimo Visualization Limits

| Output Type | Limit | Behavior Over Limit |
|-------------|-------|---------------------|
| Altair | 20K rows (400K with CSV) | Slow render / crash |
| Plotly scatter | ~10K points | Browser-dependent |
| Generic HTML | ~5MB soft limit | WebSocket error |
| Custom iframe | Unlimited | Works with streaming |

### 5.2 Native Alternatives Comparison

#### For 3D Code City (Buildings + Particles)

| Approach | Capability | Verdict |
|----------|------------|---------|
| Current (Three.js) | Full 3D, particles, emergence | ✅ KEEP |
| anywidget + Three.js | Identical | ✅ Alternative |
| Native marimo | ❌ Not possible | ❌ Reject |

**Verdict:** The emergence animation is Orchestr8's signature. No native alternative exists.

#### For Wiring Diagram (2D Edges)

| Approach | Capability | Cost | Verdict |
|----------|------------|------|---------|
| Current (Three.js) | 3D lines, hover, click | High | ⚠️ Overkill |
| Pyvis | Interactive 2D | Low | ✅ Consider |
| D3 via anywidget | Interactive 2D/2.5D | Medium | ✅ Consider |

**Verdict:** Rendering 2D data as 3D lines is over-engineered. Pyvis could achieve 90% functionality at 20% cost.

### 5.3 anywidget Architecture

anywidget uses traitlets-based state sync:
```
Python (traitlets) <--Comm Protocol--> JavaScript (model.get/set)
```

**Key Finding:** For large datasets (>10K points), use `traitlets.Bytes()` to avoid JSON serialization overhead.

---

## Part VI: Integration Points

### 6.1 Physical Structure (MANDATORY)

```
orchestr8.py                          ← ENTRY POINT (CAN CHANGE)
    └── IP/plugins/06_maestro.py      ← MAIN RENDER (CANNOT CHANGE PATH)
        ├── IP/styles/
        │   ├── orchestr8.css        ← VISUAL TOKENS LIVE HERE
        │   ├── font_profiles.py     ← FONT INJECTION
        ├── IP/static/
        │   ├── woven_maps_3d.js     ← THREE.JS RENDERER
        │   └── woven_maps_template.html
        ├── IP/features/code_city/
        │   ├── graph_builder.py
        │   └── render.py
        └── IP/plugins/components/
            ├── deploy_panel.py
            └── [other panels]
```

### 6.2 Button I/O Mapping

| Button | Handler | Status |
|--------|---------|--------|
| orchestr8 | toggle_orchestr8_panel() | ✅ |
| MAESTRO | cycle_maestro_state() | ✅ |
| collab8 | toggle_collab8_panel() | ✅ |
| JFDI | toggle_jfdi_panel() | ✅ |
| Ticket | toggle_tickets() | ✅ |
| Calendar | toggle_calendar() | ✅ |
| Comms | toggle_comms() | ✅ |
| File | toggle_file_explorer() | ✅ |
| Deploy | toggle_deploy() | ✅ |
| Summon | toggle_summon() | ✅ |
| Settings | toggle_settings() | ✅ |

---

## Part VII: Known Issues & Gaps

### Critical Issues

| Issue | Location | Fix |
|-------|----------|-----|
| Neighborhood combat status bug | graph_builder.py:69-70 | Change `status = "broken"` to `status = "combat"` |
| Warnings not propagated | graph_builder.py:364 | Add `node.health_warnings` field |
| No node→Summon handoff | 06_maestro.py | Add payload passthrough |

### Technical Debt

| Item | Impact | Recommendation |
|------|--------|----------------|
| 3D wiring diagram | Over-engineered | Consider Pyvis for v2 |
| Custom iframe vs anywidget | Manual state management | Consider anywidget migration |
| Large payload streaming | Complex | Acceptable given 3D requirements |

---

## Part VIII: Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Visual tokens | HIGH | Canonical source verified |
| 3D rendering | HIGH | Battle-tested implementation |
| Health→color pipeline | HIGH | Direct code inspection |
| Node click integration | HIGH | Full pipeline traced |
| anywidget alternatives | HIGH | Verified with docs |
| Pyvis recommendation | MEDIUM | External library, not tested in Orchestr8 |

---

## Part IX: Recommendations

### Keep (Confirmed Working)

1. **3D Code City** — Custom WebGPU/Three.js required for emergence animation
2. **Visual tokens** — VISUAL_TOKEN_LOCK.md is canonical
3. **CSS architecture** — File-based, loaded dynamically
4. **Node click pipeline** — Works for broken/working/combat states

### Consider (Tradeoff Analysis)

1. **Pyvis for wiring diagram** — Could reduce code by 80%
2. **anywidget migration** — Better Python integration, requires rewrite
3. **Health pipeline fixes** — Warnings propagation, neighborhood bug

### Don't Change

1. **Physical structure** — Entry points locked
2. **State colors** — Working/broken/combat locked in token system
3. **Font stack** — Marcellus SC, Poiret One, VT323

---

## Sources

### Primary Sources (HIGH Confidence)
- `SOT/VISUAL_TOKEN_LOCK.md` — Canonical token definitions
- `IP/styles/orchestr8.css` — CSS implementation
- `IP/static/woven_maps_3d.js` — Three.js rendering (1200+ lines)
- `IP/woven_maps.py` — Python logic, configuration
- `IP/plugins/06_maestro.py` — Main UI orchestration
- `IP/contracts/status_merge_policy.py` — Color mapping
- `IP/features/code_city/graph_builder.py` — Health merge logic

### Research Files (HIGH Confidence)
- `.planning/research/RENDERING_TRADEOFFS.md`
- `.planning/research/RENDERING_SUMMARY.md`
- `.planning/research/RENDERING_CREATIVE.md`
- `.planning/research/ANYWIDGET_CAPABILITIES.md`
- `.planning/research/MARIMO_VISUALIZATION_LIMITS.md`
- `.planning/orchestr8_next/artifacts/P07/integration/CANONICAL_VISUAL_INTEGRATION_SPEC.md`
- `.planning/orchestr8_next/artifacts/P07/integration/HEALTH_COLOR_PIPELINE.md`
- `.planning/orchestr8_next/artifacts/P07/integration/NODE_CLICK_INTEGRATION.md`

### External Sources (MEDIUM Confidence)
- [marimo Plotting API](https://docs.marimo.io/api/plotting.html)
- [marimo AnyWidget](https://docs.marimo.io/api/inputs/anywidget.html)
- [anywidget.dev](https://anywidget.dev/)
- [Pyvis Documentation](https://pyvis.readthedocs.io/)

---

## Research Flags

| Flag | Phase | Action |
|------|-------|--------|
| Health pipeline fixes | Current | Fix neighborhood combat bug, propagate warnings |
| Wiring diagram simplification | v2 | Evaluate Pyvis for import graph |
| anywidget migration | Future | Prototype if integration pain points emerge |
| Node→Summon handoff | Future | Add payload passthrough for AI context |

---

**Synthesis Complete** — All visual and rendering research from 12+ sources has been consolidated into this document.
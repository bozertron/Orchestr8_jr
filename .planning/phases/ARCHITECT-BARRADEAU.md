# ARCHITECT-BARRADEAU.md
## Settlement System: Barradeau Patterns Integration
## Generated: 2026-02-12
## Status: ARCHITECTURAL PLAN

---

## 1. Patterns to Extract from Reference Files

### From void-phase0-buildings.html (PRIMARY)

| Pattern | Location | Purpose |
|---------|----------|---------|
| **BarradeauBuilding class** | Lines 827-1031 | Core building generator with particle placement |
| **Delaunay.triangulate()** | Lines 727-803 | Footprint mesh generation |
| **Edge length filtering** | Lines 929-940 | Longer edges fade at higher layers |
| **Particle density formula** | Lines 956-959 | `density = 1 + (1 - edge.length/max) * 2` |
| **CONFIG object** | Lines 809-825 | All scaling constants in one place |
| **ShaderMaterial** | Lines 1077-1121 | Soft glow falloff for particles |

### From barradeau-3d.html (SECONDARY)

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Footprint generators** | Lines 338-466 | tower(), cathedral(), skyscraper(), neighborhood() |
| **Config flexibility** | Lines 195-203 | height, layers, particlesPerUnit, taper, densityFalloff |
| **LineSegments geometry** | Lines 319-332 | Edge visualization mesh |

### Core Technique (Barradeau Edge Filter)

```
Delaunay Triangulation → Edge Extraction → Length-Based Filtering → Particle Placement
```

**Key insight**: Shorter edges get more particles. At higher layers, longer edges are filtered out entirely, creating the ethereal fade effect.

---

## 2. Current woven_maps.py State

### Existing Components (KEEP)

| Component | Lines | Status |
|-----------|-------|--------|
| CodeNode dataclass | 54-86 | Aligned with ConnectionGraph |
| EdgeData dataclass | 89-105 | Working |
| ColorScheme | 108-130 | Aligned with canonical colors |
| scan_codebase() | 195-231 | Working |
| calculate_layout() | 272-326 | Working |
| build_from_connection_graph() | 360-451 | Working, provides edges |
| Control panel HTML/CSS | 596-815 | Working |
| Keyframe system | 862-974 | Working |
| Audio reactive | 977-1095 | Working |

### 2D Canvas Renderer (REPLACE with 3D option)

| Component | Lines | Action |
|-----------|-------|--------|
| Canvas setup | 1344-1358 | Keep for 2D fallback |
| WaveField | ~1400+ | Keep for 2D |
| Delaunay (d3-delaunay) | Uses CDN | Replace with custom class |
| Particle system | ~1500+ | Adapt for 3D |

### Gaps

1. **No Three.js integration** - currently 2D canvas only
2. **No 3D building extrusion** - flat node rendering
3. **No Barradeau edge filter** - uses d3-delaunay, not custom
4. **No particle clustering** - single particles per node

---

## 3. Integration Approach

### Strategy: Dual-Mode Rendering

```
┌─────────────────────────────────────────────┐
│              woven_maps.py                  │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │  2D Canvas  │  │   3D Three.js Mode   │  │
│  │  (existing) │  │     (NEW)            │  │
│  └─────────────┘  └──────────────────────┘  │
│         │                   │                │
│         └───────┬───────────┘                │
│                 ▼                            │
│        GraphData (shared)                    │
└─────────────────────────────────────────────┘
```

### Files to Create

| File | Purpose |
|------|---------|
| `IP/barradeau_builder.py` | Python side: building data generation |
| `IP/static/woven_maps_3d.js` | Three.js renderer with Barradeau patterns |
| `IP/static/shaders/barradeau.vert` | Vertex shader for edge filtering |
| `IP/static/shaders/barradeau.frag` | Fragment shader for glow |

### Color Alignment (LOCKED)

```javascript
// FROM void-phase0-buildings.html
COLOR: 0xC9A962  // Reference gold

// TO canonical
COLOR: 0xD4AF37  // Canonical gold-metallic
```

### Building Formula (LOCKED - already correct)

```javascript
footprint_radius = 2 + (lines * 0.008)
height = 3 + (exports * 0.8)
particles_per_unit = 1.2
layer_count = 15
taper = 0.015
```

---

## 4. Modification Order

### Phase 1: Extract Core Patterns (Est: 2 agents, 1 session)

1. Create `IP/barradeau_builder.py`
   - Port `BarradeauBuilding` class logic to Python
   - Port `Delaunay` triangulation
   - Output: BuildingData with particles, edges

2. Create `IP/static/woven_maps_3d.js`
   - Three.js scene setup
   - OrbitControls (from reference)
   - UnrealBloomPass post-processing

### Phase 2: Implement Building Generator (Est: 3 agents, 1 session)

1. Port footprint generation
   - From file metrics → footprint points
   - Complexity based on LOC

2. Port extrusion logic
   - Layer-based particle placement
   - Edge length filtering per layer
   - Taper calculation

3. Create shaders
   - Vertex: size attenuation, opacity from layer
   - Fragment: soft glow falloff (Barradeau style)

### Phase 3: Wire to GraphData (Est: 2 agents, 1 session)

1. Connect to `build_from_connection_graph()`
   - Use export_count from edges for height
   - Use incoming/outgoing counts for additional sizing

2. Implement color state mapping
   - working → 0xD4AF37
   - broken → 0x1fbdea  
   - combat → 0x9D4EDD

### Phase 4: Add 3D Controls (Est: 1 agent, 1 session)

1. Add mode toggle (2D/3D)
2. Add density slider (`densit8`) - controls `particlesPerUnit`
3. Add camera keyframes for 3D

### Phase 5: Emergence Animation (Est: 1 agent, 1 session)

1. Particles start scattered → coalesce to building positions
2. NO breathing - emergence only
3. Frame color: teal during emergence → gold when complete

---

## 5. Agent Estimates

### Universal Scaling Formula

```
effective_tokens = file_tokens × complexity_multiplier × responsibility_multiplier
agents = ceil(effective_tokens / 2500) × 3  (Sentinel Protocol)
```

### Estimates by Phase

| Phase | Files | Est. LOC | Complexity | Responsibility | Agents |
|-------|-------|----------|------------|----------------|--------|
| 1. Extract Core | 2 | 400 | 1.5 | 1.2 | 3 |
| 2. Building Gen | 3 | 600 | 1.8 | 1.3 | 6 |
| 3. Wire GraphData | 1 | 200 | 1.2 | 1.1 | 3 |
| 4. 3D Controls | 1 | 150 | 1.0 | 1.0 | 3 |
| 5. Emergence | 1 | 200 | 1.3 | 1.1 | 3 |

**Total: ~18 agent deployments across 5 phases**

---

## 6. Key Integration Points

### From woven_maps.py

```python
# Line 378-385: ConnectionGraph already provides metrics
metrics = node_data.get("metrics", {})
centrality = metrics.get("centrality", 0.0)  # For sizing boost
incoming_count = metrics.get("incomingCount", 0)  # For height
outgoing_count = metrics.get("outgoingCount", 0)  # For footprint
```

### From void-phase0-buildings.html

```javascript
// Lines 809-825: CONFIG to port
const CONFIG = {
    BASE_FOOTPRINT: 2,
    FOOTPRINT_SCALE: 0.008,
    MIN_HEIGHT: 3,
    HEIGHT_PER_EXPORT: 0.8,
    PARTICLES_PER_UNIT: 1.2,
    LAYER_COUNT: 15,
    TAPER: 0.015,
    COLOR: 0xC9A962  // → Change to 0xD4AF37
};
```

### Emergence Pattern (LOCKED - no breathing)

```javascript
// FROM woven_maps.py emergence system
// Particles coalesce from scattered positions
// NO sin/cos oscillation after emergence
// Single emergence event, not continuous animation
```

---

## 7. Success Criteria

- [ ] Buildings render with Barradeau particle clustering
- [ ] Height formula: `3 + (exports × 0.8)`
- [ ] Footprint formula: `2 + (lines × 0.008)`
- [ ] Three-color system: #D4AF37, #1fbdea, #9D4EDD
- [ ] Emergence animation (no breathing)
- [ ] Density slider adjusts particle visibility
- [ ] 2D fallback mode still works

---

**Document Status:** ARCHITECTURAL PLAN
**Ready for:** Implementation Phase
**Requires Founder Approval:** Yes (per INTEGRATION_QUEUE.md)

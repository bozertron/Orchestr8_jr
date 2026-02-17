# 07-07 WOVEN MAPS 3D - INTEGRATION SPECIFICATION

**Phase:** 07-07 Woven Maps 3D Integration  
**Date:** 2026-01-31  
**Based on:** Comprehensive research from Barradeau source files, roadmaps, and existing code

---

## 1. EXECUTIVE SUMMARY

### What This Phase Delivers

Transform the 2D canvas Code City visualization (`IP/woven_maps.py`) into a 3D Barradeau particle city using Three.js, leveraging the complete reference implementations in `one integration at a time/Barradeau/`.

### Key Deliverables

| Deliverable | Source | Est. Hours |
|------------|--------|------------|
| Three.js hybrid renderer (GPU + Canvas fallback) | `barradeau-3d.html` | 4-6h |
| BarradeauBuilding class (extracted) | `void-phase0-buildings.html` | 8-10h |
| Edge filter shader (GLSL) | Reference patterns | 2-4h |
| Dive-to-building interaction | `woven_maps.py` + concepts | 4-6h |
| Real-time Socket.io updates | Architecture spec | 2-4h |
| New control panel buttons | UI spec | 2-4h |

**Total:** 22-34 hours across 4 implementation phases

### Why Now

- Phase 0-6 complete (core wiring done)
- Barradeau prototypes fully functional (50KB+ of tested code)
- Clear roadmap from MASTER_ROADMAP phases 11-15
- Single source of truth in `one integration at a time/Barradeau/`

---

## 2. CURRENT STATE ANALYSIS

### IP/woven_maps.py (2059 lines)

**What's Working (Keep):**

- Emergence animation with particle coalescence
- Wave field for organic motion
- Audio-reactive visualization (microphone)
- Keyframe system (4 slots, morph between states)
- ConnectionGraph integration (real import edges)
- Node type shapes (7 shapes for file types)
- Centrality-based node sizing
- Cycle detection with red pulsing glow

**What's Missing (Add):**

- Three.js 3D rendering
- Barradeau building structures
- Shader-based edge filtering
- Dive-to-building interaction
- Real-time Socket.io updates
- New control buttons (densit8, orbit8, focus8, pulse8, layer8)

### Barradeau Source Files (CRITICAL REFERENCE)

| File | Lines | Purpose | Extract |
|------|-------|---------|---------|
| `void-phase0-buildings.html` | 1266 | Phase 0 building generator | `BarradeauBuilding` class, `Delaunay` triangulation, file parsing |
| `barradeau-3d.html` | 652 | Three.js adaptation | Scene setup, footprint generators, shader materials |
| `barradeau-buildings.html` | ~600 | 2D reference | Fallback mode patterns |
| `barradeau-builder.html` | ~800 | Building generator | Config patterns |
| `HANDOFF_PROMPT.md` | 257 | Metaphor and working style | Design decisions |

---

## 3. ARCHITECTURE DECISION: HYBRID RENDERER

### GPU Default, CPU Fallback

```
┌─────────────────────────────────────────────────────────┐
│                 Woven Maps Hybrid Renderer              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ Three.js 3D  │ or │  Canvas 2D   │ or │  Text-only │ │
│  │ (GPU, 1M+    │    │ (CPU, 100K   │    │  (fallback)│ │
│  │  particles)  │    │  particles)  │    │            │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│         │                   │                   │        │
│         └───────────────────┴───────────────────┘        │
│                          │                              │
│                  Auto-detect GPU capability             │
│                  Fallback to Canvas 2D                  │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
Python Layer                    JavaScript Layer
─────────────────────────────────────────────────────────
IP/woven_maps.py          →    woven_maps_3d.js
     │                          │
     ├── scan_codebase()   →    data.json
     ├── calculate_layout() →    node positions
     └── build_graph_data() →    edges, health

IP/connection_verifier.py  →    import relationships
IP/health_checker.py       →    status colors
IP/combat_tracker.py       →    combat indicators
```

---

## 4. BARRADEAU BUILDING SPECIFICATION

### Building Size Formula (From void-phase0-buildings.html)

```javascript
// CONFIG from void-phase0 (lines 809-825)
const CONFIG = {
    // Scaling factors
    BASE_FOOTPRINT: 2,           // Minimum building size
    FOOTPRINT_SCALE: 0.008,      // Lines → footprint multiplier
    MIN_HEIGHT: 3,               // Minimum building height
    HEIGHT_PER_EXPORT: 0.8,      // Each export adds this much height
    
    // Particle density
    PARTICLES_PER_UNIT: 1.2,     // Higher = more particles
    
    // Visual
    LAYER_COUNT: 15,             // Vertical layers in extrusion
    TAPER: 0.015,                // How much building narrows at top
    
    // Color (from orchestr8)
    COLOR: 0xD4AF37              // Gold - healthy state
};

// Calculate dimensions
footprintRadius = CONFIG.BASE_FOOTPRINT + (lineCount * CONFIG.FOOTPRINT_SCALE);
height = CONFIG.MIN_HEIGHT + (exportCount * CONFIG.HEIGHT_PER_EXPORT);
```

### Particle Placement (The Barradeau Technique)

From `void-phase0-buildings.html` (lines 897-972):

1. **Generate Footprint** - Irregular polygon based on file size
2. **Triangulate** - Delaunay triangulation of footprint points
3. **Extract Edges** - Unique edges with lengths
4. **Extrude Layers** - For each layer:
   - Scale footprint (taper toward top)
   - Filter edges by length (longer edges filtered first at higher layers)
   - Place particles along remaining edges
   - Shorter edges = more particles (density inversely proportional to length)

```javascript
// Key insight: densityFalloff
const densityMultiplier = 1 + (1 - edge.length / maxEdgeLength) * 2;
// Shorter edges get MORE particles
```

### Three.js Geometry

```javascript
class BarradeauBuilding {
    createMesh(material) {
        const positions = new Float32Array(this.particles.length * 3);
        const colors = new Float32Array(this.particles.length * 3);
        const sizes = new Float32Array(this.particles.length);
        
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            positions[i*3] = p.x;
            positions[i*3+1] = p.y;
            positions[i*3+2] = p.z;
            
            // Color by health state (orchestr8 colors)
            const color = new THREE.Color(HEALTH_COLORS[this.status]);
            colors[i*3] = color.r;
            colors[i*3+1] = color.g;
            colors[i*3+2] = color.b;
            
            sizes[i] = p.size;
        }
        
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        
        return new THREE.Points(geometry, material);
    }
}
```

---

## 5. SHADER SPECIFICATION

### Edge Filter Shader (From reference patterns)

**Vertex Shader:**

```glsl
attribute vec3 neighbor;
uniform float uThreshold;

varying float vAlpha;

void main() {
    float edgeLen = distance(position, neighbor);
    float alpha = 1.0 - smoothstep(uThreshold, uThreshold + 0.5, edgeLen);
    vAlpha = alpha;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

**Fragment Shader:**

```glsl
varying float vAlpha;

void main() {
    // Soft glow falloff (Barradeau style)
    float alpha = pow(vAlpha, 1.5);
    gl_FragColor = vec4(color, alpha * 0.85);
}
```

### Particle Shader (From barradeau-3d.html)

```glsl
// Vertex
attribute float size;
attribute vec3 color;
varying vec3 vColor;

void main() {
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * (120.0 / -mvPosition.z);  // Size attenuation
    gl_Position = projectionMatrix * mvPosition;
}

// Fragment
varying vec3 vColor;

void main() {
    vec2 center = gl_PointCoord - 0.5;
    float dist = length(center);
    if (dist > 0.5) discard;
    
    float alpha = 1.0 - smoothstep(0.0, 0.5, dist);
    alpha = pow(alpha, 1.5);
    
    gl_FragColor = vec4(vColor, alpha * 0.85);
}
```

---

## 6. CONTROL PANEL SPECIFICATION

### New Buttons (Phase 15b)

| Button | Label | Action | Source |
|--------|-------|--------|--------|
| Density | `densit8` | Slider: Barradeau threshold (0.5-3.0) | zsphere.html |
| Dock/Float | `dock8` | Toggle control panel docked/floating | UI spec |
| Overview | `orbit8` | Auto-rotate overview mode | barradeau-3d.html |
| Focus | `focus8` | Dive to selected building | New |
| Pulse | `pulse8` | Toggle breathing animation | barradeau-3d.html |
| Layer | `layer8` | Cycle building layer visibility | void-phase0 |

### Layout (Bottom 5th)

```
┌─────────────────────────────────────────────────────────────────┐
│ [Gold] [Teal] [Purple]  │  [1][2][3][4]  │  [🔊]  │  [densit8 ▽] │
├─────────────────────────────────────────────────────────────────┤
│ [Re-Emerge] [Clear] [dock8] [orbit8] [focus8] [pulse8] [layer8] │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Points

Existing control panel in `IP/woven_maps.py` (lines 596-885):

- Add new buttons after "Clear" button
- Update JavaScript `updateMorph()` function for 3D values
- Add new state variables: `activeDensit8`, `activeOrbit8`, etc.

---

## 7. INTERACTION SPECIFICATIONS

### Dive-to-Building

From MASTER_ROADMAP (lines 480-510):

```javascript
function diveToBuilding(building) {
    const targetPosition = building.position.clone();
    targetPosition.z += building.height * 1.5;
    
    // Smooth camera animation
    gsap.to(camera.position, {
        x: targetPosition.x,
        y: targetPosition.y + 5,
        z: targetPosition.z,
        duration: 1.2,
        ease: "power2.inOut"
    });
    
    controls.target.copy(building.position);
    showBuildingDetails(building.metadata);
}
```

**Raycasting for Selection:**

```javascript
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(scene.children);

if (intersects.length > 0) {
    const selected = intersects[0].object;
    diveToBuilding(selected);
}
```

### Town Square (Conceptual)

High-centrality nodes cluster at center:

```javascript
function calculateTownSquareLayout(nodes) {
    nodes.sort((a, b) => b.centrality - a.centrality);
    
    const centerRadius = 50;
    const peripheryRadius = 400;
    
    nodes.forEach((node, i) => {
        const t = i / nodes.length;
        const radius = centerRadius + (peripheryRadius - centerRadius) * Math.pow(t, 0.5);
        const angle = i * Math.PI * 2 / nodes.length;
        
        node.x = Math.cos(angle) * radius;
        node.y = Math.sin(angle) * radius;
    });
}
```

### Wire Grab (Conceptual)

Drag broken edge → auto-fix import:

```javascript
function setupWireGrab() {
    const brokenEdges = edges.filter(e => !e.resolved);
    
    brokenEdges.forEach(edge => {
        makeDraggable(edge);
        edge.on('dragend', (event) => {
            const target = findNearestNode(event.position);
            if (target) {
                emit('fix_import', { from: edge.source, to: target.path });
            }
        });
    });
}
```

---

## 8. REAL-TIME INTEGRATION

### Socket.io Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Carl Health Monitor                   │
│            (detects file health changes)                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   Socket.io Server                       │
│         (broadcasts to all connected clients)           │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Browser │ │ Browser │ │  CLI    │
    └─────────┘ └─────────┘ └─────────┘
        │           │           │
        ▼           ▼           ▼
    ┌─────────────────────────────────────────────────────────┐
    │               Woven Maps 3D Renderer                     │
    │         (updates building colors in real-time)          │
    └─────────────────────────────────────────────────────────┘
```

### Client Implementation

```javascript
const socket = io('http://localhost:3000');

socket.on('health_change', (data) => {
    const building = buildings.get(data.filePath);
    if (building) {
        // Smooth color transition
        animateColorChange(building, data.status);
    }
});

function animateColorChange(building, newStatus) {
    const startColor = building.mesh.material.color.clone();
    const endColor = new THREE.Color(HEALTH_COLORS[newStatus]);
    
    // GSAP color tween
    gsap.to(startColor, {
        r: endColor.r,
        g: endColor.g,
        b: endColor.b,
        duration: 0.5,
        onUpdate: () => {
            building.mesh.material.color.copy(startColor);
        }
    });
}
```

---

## 9. FILE STRUCTURE

```
IP/
├── woven_maps.py                    # Keep, add 3D toggle
├── woven_maps_3d.js                 # NEW: Three.js renderer
├── barradeau_building.js            # NEW: BarradeauBuilding class
├── delaunay.js                      # NEW: Delaunay triangulation
├── shaders/
│   ├── barradeau.vert              # NEW: Edge filter vertex
│   ├── barradeau.frag              # NEW: Edge filter fragment
│   └── particles.vert              # NEW: Particle vertex
│
one integration at a time/Barradeau/  # REFERENCE ONLY
├── void-phase0-buildings.html       # Extract BarradeauBuilding
├── barradeau-3d.html                # Extract Three.js patterns
└── zsphere.html                     # Extract shader patterns
```

---

## 10. PHASED IMPLEMENTATION

### Phase 1: Three.js Setup (4-6h)

**Goal:** Hybrid renderer with GPU detection

**Tasks:**

1. Create `IP/woven_maps_3d.js` module
2. Set up Three.js scene, camera, renderer
3. Implement GPU capability detection
4. Create Canvas 2D fallback path
5. Migrate 2D nodes to 3D points
6. Migrate 2D edges to 3D lines

**Deliverables:**

- `IP/woven_maps_3d.js` (500+ lines)
- Toggle between 2D/3D in control panel

### Phase 2: Barradeau Buildings (8-10h)

**Goal:** 3D building generation from file metrics

**Tasks:**

1. Extract `BarradeauBuilding` class from void-phase0
2. Extract `Delaunay` triangulation
3. Implement building size formula
4. Create particle placement along edges
5. Implement layer-based filtering
6. Add mesh generation

**Deliverables:**

- `IP/barradeau_building.js` (800+ lines)
- Buildings render with correct size

### Phase 3: Shaders and Controls (6-8h)

**Goal:** Edge filtering and new controls

**Tasks:**

1. Implement edge filter shader
2. Add `densit8` slider
3. Add `orbit8`, `focus8`, `pulse8`, `layer8` buttons
4. Wire keyframes to camera positions
5. Add bloom post-processing

**Deliverables:**

- `IP/shaders/` directory (3 files)
- All control buttons functional

### Phase 4: Interactions and Real-Time (4-6h)

**Goal:** Click interactions and Socket.io

**Tasks:**

1. Implement raycasting for selection
2. Add dive-to-building animation
3. Add building details panel
4. Implement Socket.io client
5. Wire to Carl health monitoring

**Deliverables:**

- Click → dive interaction
- Real-time color updates

---

## 11. RISKS AND MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| Three.js performance with large graphs | High | LOD for distant buildings, instance reuse |
| Shader compatibility across GPUs | Medium | Test on multiple GPUs, fallback to lines |
| Socket.io latency | Medium | Debounce updates, optimistic UI |
| Migration complexity | Low | Incremental approach, test at each step |
| Memory growth from BufferGeometry | Medium | Dispose geometries, limit particle count |

---

## 12. SUCCESS CRITERIA

### Functional

- [ ] 3D Code City renders with Barradeau aesthetic
- [ ] Buildings scale correctly from file metrics (lines, exports)
- [ ] Particle density follows Barradeau technique
- [ ] Health colors update in real-time
- [ ] Click building → camera dives to it
- [ ] Wire grab interaction fixes broken imports

### Technical

- [ ] Three.js GPU mode with Canvas 2D fallback
- [ ] Shader-based edge filtering (densit8 slider works)
- [ ] Socket.io real-time updates (sub-2s latency)
- [ ] No regression in 2D canvas mode
- [ ] All control panel buttons functional

### Performance

- [ ] 60fps with <1000 buildings on GPU
- [ ] Graceful degradation to Canvas 2D
- [ ] Memory stable over time (no leaks)

---

## 13. INTEGRATION CHECKLIST

### Before Phase 1

- [ ] Review `void-phase0-buildings.html` for BarradeauBuilding extraction
- [ ] Review `barradeau-3d.html` for Three.js patterns
- [ ] Verify Three.js r160 CDN availability
- [ ] Set up test environment with GPU

### During Phase 1

- [ ] Create `IP/woven_maps_3d.js` module structure
- [ ] Implement GPU detection
- [ ] Create Canvas 2D fallback
- [ ] Test 2D/3D toggle

### During Phase 2

- [ ] Extract BarradeauBuilding class
- [ ] Extract Delaunay triangulation
- [ ] Implement file parsing (lines, exports)
- [ ] Test building generation with sample files

### During Phase 3

- [ ] Implement shaders
- [ ] Add control panel buttons
- [ ] Test densit8 slider
- [ ] Verify bloom post-processing

### During Phase 4

- [ ] Implement raycasting
- [ ] Add Socket.io client
- [ ] Test real-time updates
- [ ] Verify building details panel

---

**Specification Complete:** 2026-01-31  
**Next:** EXECUTION-PLAN.md with task breakdown

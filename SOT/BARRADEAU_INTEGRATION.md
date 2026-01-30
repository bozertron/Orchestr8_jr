# Barradeau Integration Strategy
## Code City 3D Visualization - Milestone 3

**Created:** 2026-01-30
**Status:** Ready for GSD Handoff
**Dependencies:** Phases 1-5 (Branding, Buttons, Health, Briefing, Calendar)

---

## I. Core Technique: Barradeau Edge Filter

The Barradeau technique transforms code metrics into living particle structures:

```
Code Metrics → Delaunay Triangulation → Edge Filtering → Particle Placement → Animation
```

### Building Size Formula (DEFINITIVE)
```javascript
footprint_radius = 2 + (file_lines * 0.008)
building_height = 3 + (export_count * 0.8)
particles_per_unit = 1.2
layer_count = 15
taper = 0.015
```

### Three-Color System
| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| Working | Gold | #D4AF37 | Healthy, passing tests |
| Broken | Blue | #1fbdea | Failing, needs attention |
| Combat | Purple | #9D4EDD | Active LLM engagement |

---

## II. Architecture Decisions

### GPU Default, CPU Fallback
- **GPU (GPGPU)**: Default mode, 1M+ particle capacity
- **CPU**: Fallback for compatibility, reduced particle count
- **Why**: Density is critical for visually delineating nuances in complex codebases

### Real-Time Health Updates (Socket.io)
```
Carl Health Monitor → Socket.io Broadcast → Code City Color Update
```
- Carl detects file health changes (tests pass/fail)
- Broadcasts to Code City via Socket.io
- Buildings change color in real-time (Gold → Blue → Gold)

### Data Flow
```
Python (woven_maps.py)     →  structure_map.json  →  Three.js Renderer
├── file_lines                                        ├── Building footprint
├── export_count                                      ├── Building height
├── health_status                                     ├── Particle color
└── relationships                                     └── Edge connections
```

---

## III. Key Interactions

### "Dive to Building" (PRIMARY)
User clicks building → camera smoothly zooms to building → shows file details

**Existing Pattern** (woven_maps.py:1891-1912):
```javascript
canvas.addEventListener('click', (e) => {
    // Raycasting to detect node
    type: 'WOVEN_MAPS_NODE_CLICK',
    // Opens file details
});
```

**Enhancement for 3D**:
```javascript
function diveToBuilding(building) {
    const targetPosition = building.position.clone();
    targetPosition.z += building.height * 1.5;  // Camera offset

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

### Keyframe System (EXISTING)
4 camera position slots - click to load, double-click to save:
```javascript
keyframes[slot] = {
    camera: camera.position.clone(),
    target: controls.target.clone(),
    zoom: camera.zoom
};
```

---

## IV. Control Panel Buttons (Bottom 5th)

### Existing Buttons (Keep)
| Button | Action | Pattern |
|--------|--------|---------|
| Gold | `setFrameColor('gold')` | Filter to healthy files |
| Teal | `setFrameColor('teal')` | Filter to broken files |
| Purple | `setFrameColor('combat')` | Filter to combat files |
| KF 1-4 | `loadKeyframe(n)` / `saveKeyframe(n)` | Camera positions |
| Audio | `toggleAudio()` | Sound on/off |
| Re-Emerge | `reEmergence()` | Reset particle positions |
| Clear | `clearParticles()` | Remove all particles |

### New Buttons (Proposed)

| Button | Label | Action | Source |
|--------|-------|--------|--------|
| **Density** | `densit8` | Slider: Barradeau threshold (0.5-3.0) | zsphere.html |
| **Dock/Float** | `dock8` | Toggle control panel docked/floating | GPT5Pats.txt |
| **Overview** | `orbit8` | Auto-rotate overview mode | barradeau-3d.html |
| **Focus** | `focus8` | Dive to selected building | New |
| **Pulse** | `pulse8` | Toggle breathing animation | barradeau-3d.html |
| **Layer** | `layer8` | Cycle building layer visibility | void-phase0 |

### Button Layout (Bottom 5th)
```
┌─────────────────────────────────────────────────────────────────┐
│ [Gold] [Teal] [Purple]  │  [1][2][3][4]  │  [🔊]  │  [densit8] │
├─────────────────────────────────────────────────────────────────┤
│ [Re-Emerge] [Clear] [dock8] [orbit8] [focus8] [pulse8] [layer8] │
└─────────────────────────────────────────────────────────────────┘
```

---

## V. Shader: Barradeau Edge Filter

From zsphere.html - the core visual effect:

```glsl
// Vertex Shader
attribute vec3 neighbor;
uniform float uThreshold;

void main() {
    vec3 pos = position;

    // Edge length determines visibility
    float edgeLen = distance(pos, neighbor);

    // Threshold logic - longer edges fade out
    float alpha = 1.0 - smoothstep(uThreshold, uThreshold + 0.5, edgeLen);

    // Color by distance from center (health state)
    float distFromCenter = length(pos);
    vColor = mix(coreColor, shellColor, distFromCenter);
    vAlpha = alpha;
}
```

### Integration Point
The `densit8` slider controls `uThreshold`:
- Lower = More detail (dense particle field)
- Higher = Sparse structure (performance mode)

---

## VI. Later Roadmap Items

### Audio Reactivity (Post-Milestone 3)
```javascript
// From 2 COMPUTE PASS Update.txt
compute.simMaterial.uniforms.uAudioBass.value = uBass;
compute.simMaterial.uniforms.uAudioTreble.value = uTreble;
```
- LLM conversations drive audio input
- Buildings pulse/breathe with voice

### Canvas Fallback (Post-Milestone 3)
- 2D canvas version for maximum compatibility
- From v4.html - zero-dependency mode

---

## VII. File Structure

```
IP/
├── woven_maps.py          # Enhance with 3D mode
├── woven_maps_3d.js       # NEW: Three.js renderer
├── barradeau_builder.js   # NEW: Building generator
└── shaders/
    ├── barradeau.vert     # NEW: Edge filter vertex
    └── barradeau.frag     # NEW: Edge filter fragment

one integration at a time/Barradeau/
├── void-phase0-buildings.html  # SOURCE: Building generator
├── barradeau-3d.html           # SOURCE: Footprint generators
└── zsphere.html                # SOURCE: Edge filter shader
```

---

## VIII. GSD Handoff: Phase 6 - Code City 3D

### Objective
Transform woven_maps.py's 2D Code City into a 3D Barradeau particle visualization.

### Tasks
1. **Extract BarradeauBuilding class** from void-phase0-buildings.html
2. **Add Three.js renderer** as alternative to 2D canvas
3. **Implement edge filter shader** from zsphere.html
4. **Add density slider** (`densit8`) to control panel
5. **Implement dive-to-building** click handler
6. **Connect Socket.io** for real-time health updates

### Success Criteria
- [ ] Buildings render with correct size formula
- [ ] Three-color system working
- [ ] Density slider adjusts particle visibility
- [ ] Click building → camera dives to it
- [ ] Health changes reflected in real-time

### Key Files to Reference
- `IP/woven_maps.py` (lines 596-811) - Control panel CSS/HTML
- `one integration at a time/Barradeau/void-phase0-buildings.html` - Building generator
- `one integration at a time/Barradeau/zsphere.html` - Edge filter shader

---

## IX. Dependencies

### NPM/CDN
```html
<script type="importmap">
{
    "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
    }
}
</script>
```

### Python
```python
# Already in requirements
import marimo
import networkx
# May need
import json  # For structure_map export
```

---

**Next Phase:** Phase 7 - Panel Completion (Collabor8, Summon)

# Code City 3D Engine Technical Analysis

**Source:** `/home/bozertron/Orchestr8_jr/IP/static/woven_maps_3d.js`  
**Target Integration:** `a_codex_plan`  
**Date:** 2026-02-16

---

## Executive Summary

The Code City 3D engine (`woven_maps_3d.js`) is a pure Three.js rendering solution that visualizes software project structure as volumetric particle-based cityscapes. Unlike traditional mesh-based 3D rendering, this engine employs the **Barradeau particle technique** — representing buildings as dense point clouds rather than solid geometry.

### Key Architectural Characteristics

| Aspect | Implementation |
|--------|---------------|
| **Rendering Paradigm** | Particle-based (not mesh-based) |
| **Building Representation** | Point clouds with custom shaders |
| **Camera System** | OrbitControls + keyframe transitions |
| **Interaction Model** | Stateless renderer (no click/hover in engine) |
| **Communication** | Parent-controlled via method calls |
| **Animation** | Emergence (scatter → coalesce → crystallize) |

---

## 1. Building Geometry Generation

### 1.1 The Barradeau Particle Technique

The engine does not generate traditional 3D mesh geometry (boxes, extrusions). Instead, buildings are rendered as **volumetric point clouds**:

```javascript
// From createBuildingMesh()
const particles = buildingData.particles;
const positions = new Float32Array(particles.length * 3);
const opacities = new Float32Array(particles.length);
const sizes = new Float32Array(particles.length);
```

**Particle Attributes:**
- **Position (x, y, z):** 3D coordinates in world space
- **Opacity:** Per-particle transparency (0.0 - 1.0)
- **Size:** Per-particle size with random variation

### 1.2 Building Data Structure

Buildings are defined by `BuildingData` objects (from Python's `barradeau_builder.py`):

```typescript
interface BuildingData {
    path: string;           // File path (e.g., "IP/plugins/06_maestro.py")
    status: string;         // "working" | "broken" | "combat" | "locked"
    height: number;        // Derived from export count / complexity
    footprint: number;     // Derived from lines of code
    particles: Particle[]; // Array of {x, y, z, opacity, size}
    edges: Edge[];         // Wireframe connections
    isLocked: boolean;     // File protection status
    position?: {x: number, z: number}; // Grid position
}
```

### 1.3 Height and Footprint Formulas

The 3D engine does **not** compute height/footprint — it receives pre-calculated values from Python. However, the Python side derives:

- **Height:** Based on export count and function/class complexity
- **Footprint:** Based on total lines of code (LOC)
- **Particle Distribution:** Dense core with sparse corona effect

### 1.4 Dual-Layer Rendering

Each building renders as two visual layers:

1. **Particle Cloud (Primary):**
   ```javascript
   const mesh = new THREE.Points(geometry, material);
   mesh.userData = {
       path: buildingData.path,
       status: buildingData.status,
       particleCount: particles.length
   };
   ```

2. **Wireframe Edges (Secondary):**
   ```javascript
   const lineMesh = new THREE.LineSegments(geometry, material);
   // Low opacity (0.3) additive blending
   ```

---

## 2. Particle System

### 2.1 Custom ShaderMaterial

The engine uses a custom `ShaderMaterial` for GPU-accelerated particle rendering:

**Vertex Shader:**
```glsl
attribute float size;
attribute float opacity;

varying float vOpacity;
varying float vDistance;

void main() {
    vOpacity = opacity;
    
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    vDistance = -mvPosition.z;
    
    // Size attenuation: closer = larger
    gl_PointSize = size * (300.0 / vDistance);
    gl_PointSize = clamp(gl_PointSize, 1.0, 50.0);
    
    gl_Position = projectionMatrix * mvPosition;
}
```

**Fragment Shader:**
```glsl
varying float vOpacity;
varying float vDistance;

uniform vec3 color;

void main() {
    // Create circular point with soft falloff
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);
    
    // Soft edge falloff (Barradeau style)
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    alpha *= vOpacity;
    
    // Add subtle glow
    float glow = exp(-dist * 3.0) * 0.5;
    
    vec3 finalColor = color + glow * color;
    
    // Discard transparent fragments for performance
    if (alpha < 0.01) discard;
    
    gl_FragColor = vec4(finalColor, alpha);
}
```

### 2.2 Particle Rendering Features

| Feature | Implementation |
|---------|---------------|
| **Shape** | Circular with soft radial falloff |
| **Size Attenuation** | Distance-based (closer = larger) |
| **Blending** | Additive for glow effect |
| **Depth Write** | Disabled for transparency sorting |
| **Fallback** | `PointsMaterial` if shaders unavailable |

### 2.3 Emergence Animation

The signature animation — buildings **EMERGE from the Void** (no breathing/pulsing):

```javascript
// Phase 1: Scatter particles randomly
const scatteredPositions = new Float32Array(count * 3);
for (let i = 0; i < count; i++) {
    scatteredPositions[i3] = (Math.random() - 0.5) * 100;
    scatteredPositions[i3 + 1] = Math.random() * 50;
    scatteredPositions[i3 + 2] = (Math.random() - 0.5) * 100;
}

// Phase 2: Color starts as teal (VOID_EMERGENCE)
const emergenceColor = new THREE.Color(CONFIG_3D.COLOR_BROKEN); // 0x1fbdea

// Phase 3: Animate position + color simultaneously
const positionEased = 1 - Math.pow(1 - t, 3);  // Cubic ease-out
const colorT = Math.pow(t, 1.5);               // Color lags slightly
const currentColor = new THREE.Color().lerpColors(
    emergenceColor,     // Start: teal
    targetColor,        // End: gold/purple
    colorT
);
```

**Animation Parameters:**
- Duration: 1200ms (single building) / 2000ms (all buildings)
- Position easing: Cubic ease-out
- Color easing: Power curve (1.5) — color transition lags position

---

## 3. Camera Controls

### 3.1 OrbitControls Configuration

```javascript
this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
this.controls.enableDamping = true;
this.controls.dampingFactor = 0.05;
this.controls.autoRotate = true;
this.controls.autoRotateSpeed = 0.3;
```

### 3.2 Keyframe System

Predefined camera positions for cinematic navigation:

| Keyframe | Position (x, y, z) | Target (x, y, z) | Auto-Rotate |
|----------|-------------------|------------------|-------------|
| `overview` | (0, 60, 60) | (0, 5, 0) | No |
| `street` | (25, 3, 25) | (0, 2, 0) | No |
| `focus` | (12, 18, 12) | (0, 8, 0) | No |
| `orbit` | (30, 25, 30) | (0, 5, 0) | Yes (0.5 speed) |

### 3.3 Smooth Transitions

```javascript
transitionTo(keyframeName, duration = 2000) {
    // Cubic ease-in-out
    const eased = this._easeInOutCubic(t);
    
    // Interpolate position
    this.camera.position.x = this._lerp(start.x, keyframe.position.x, eased);
    
    // Interpolate orbit target
    this.controls.target.x = this._lerp(startTarget.x, keyframe.target.x, eased);
    
    // Enable auto-rotate after transition completes
    if (t >= 1) {
        this.controls.autoRotate = keyframe.autoRotate;
    }
}
```

### 3.4 Demo Mode

Automatic cycling through all keyframes:
```javascript
startDemoMode(interval = 5000) {
    const keyframes = Object.keys(CONFIG_3D.CAMERA_KEYFRAMES);
    let currentIndex = 0;
    
    const cycleKeyframe = async () => {
        await this.transitionTo(keyframes[currentIndex]);
        currentIndex = (currentIndex + 1) % keyframes.length;
    };
    
    this._demoInterval = setInterval(cycleKeyframe, interval);
}
```

---

## 4. Interaction Handlers

### 4.1 Critical Finding: No Direct 3D Interactions

**The 3D engine (`woven_maps_3d.js`) does NOT implement click or hover handlers.**

There is no:
- `THREE.Raycaster` for raycasting
- `click` event listeners on meshes
- `mousemove` handlers for hover detection
- `userData` click callbacks

### 4.2 Interaction Architecture

The interaction system is split across two rendering contexts:

```
┌─────────────────────────────────────────────────────────────┐
│                    orchestr8.py (Parent)                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 06_maestro.py                                          │ │
│  │   - Listens for postMessage from iframe                │ │
│  │   - Bridges events to Python state                     │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                    postMessage
                            │
┌─────────────────────────────────────────────────────────────┐
│              woven_maps_template.html (2D Canvas)           │
│   - Canvas-based node/edge click detection                  │
│   - postMessage to parent on:                               │
│     * WOVEN_MAPS_NODE_CLICK                                 │
│     * WOVEN_MAPS_CONNECTION_ACTION                          │
│     * WOVEN_MAPS_CAMERA_NAVIGATE                             │
│     * WOVEN_MAPS_CAMERA_RETURN                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 3D Rendering Isolation

The 3D scene (`CodeCityScene`) is a **stateless renderer**:
- Receives building data via `loadBuildings()`
- Receives status updates via `updateBuildingStatus()`
- Receives camera commands via `transitionTo()`
- No direct user input handling

---

## 5. postMessage Communication Protocol

### 5.1 Message Types (2D Canvas → Parent)

| Message Type | Payload | Purpose |
|--------------|---------|---------|
| `WOVEN_MAPS_NODE_CLICK` | `{path, status, loc, errors, nodeType, centrality, ...}` | Node selection |
| `WOVEN_MAPS_CONNECTION_ACTION` | `{source, target, actionType, ...}` | Edge manipulation |
| `WOVEN_MAPS_CAMERA_NAVIGATE` | `{targetNode, position, ...}` | Camera dive |
| `WOVEN_MAPS_CAMERA_RETURN` | `{}` | Camera return |

### 5.2 Message Types (Parent → 2D Canvas)

| Message Type | Payload | Purpose |
|--------------|---------|---------|
| `WOVEN_MAPS_CONNECTION_RESULT` | `{ok, message, ...}` | Action result feedback |

### 5.3 Bridge Implementation (06_maestro.py)

```javascript
// Parent listens for iframe messages
window.addEventListener('message', function(event) {
    if (event.data.type === 'WOVEN_MAPS_NODE_CLICK') {
        // Bridge to Python state
        bridgeRuntime.writePayloadToBridge(bridgeId, event.data.node, 'Node click');
    }
    
    if (event.data.type === 'WOVEN_MAPS_CONNECTION_ACTION') {
        bridgeRuntime.writePayloadToBridge(bridgeId, event.data.payload, 'Connection action');
    }
    
    if (event.data.type === 'WOVEN_MAPS_CAMERA_NAVIGATE') {
        bridgeRuntime.writePayloadToBridge(cameraBridgeId, event.data, 'Camera navigation');
    }
});

// Parent sends results back to iframe
function broadcastToCodeCityIframes(message) {
    const frames = document.querySelectorAll('iframe');
    frames.forEach((frame) => {
        frame.contentWindow.postMessage(message, '*');
    });
}
```

---

## 6. State Synchronization

### 6.1 Internal State Management

The 3D engine maintains local state:

```javascript
class CodeCityScene {
    constructor(container) {
        this.buildings = [];           // Raw building data
        this.buildingMeshes = [];      // THREE.Points + THREE.LineSegments
        this.neighborhoodBoundaries = []; // Boundary overlays
        this.neighborhoodLabels = [];     // Text sprites
        this.isRunning = false;       // Animation loop state
    }
}
```

### 6.2 Building State Updates

```javascript
updateBuildingStatus(path, newStatus) {
    for (const meshGroup of this.buildingMeshes) {
        if (meshGroup.data.path === path) {
            const color = new THREE.Color(this.getStatusColor(newStatus));
            
            // Update ShaderMaterial uniform OR PointsMaterial
            if (meshGroup.particles.userData.useCustomShader) {
                meshGroup.particles.material.uniforms.color.value = color;
            } else {
                meshGroup.particles.material.color = color;
            }
            
            meshGroup.data.status = newStatus;
        }
    }
}
```

### 6.3 Status Color Mapping

```javascript
getStatusColor(status) {
    const colorMap = {
        "working": 0xD4AF37,      // Gold
        "broken": 0x1fbdea,        // Teal
        "combat": 0x9D4EDD,       // Purple
        "needs_work": 0x1fbdea,   // Teal
        "agents_active": 0x9D4EDD // Purple
    };
    return colorMap[status] || 0xD4AF37;
}
```

### 6.4 External State Synchronization

Synchronization flow:
1. **Python** generates/updates `BuildingData`
2. **Python** calls iframe method or reloads data
3. **3D Engine** receives via `loadBuildings()` or `updateBuildingStatus()`
4. **3D Engine** re-renders on next animation frame

---

## 7. Post-Processing Pipeline

### 7.1 Effect Composer Setup

```javascript
_initPostProcessing() {
    if (typeof THREE.EffectComposer === "function") {
        this.composer = new THREE.EffectComposer(this.renderer);
        
        const renderPass = new THREE.RenderPass(this.scene, this.camera);
        this.composer.addPass(renderPass);
        
        this.bloomPass = new THREE.UnrealBloomPass(
            new THREE.Vector2(width, height),
            1.0,   // strength
            0.4,   // radius
            0.15   // threshold
        );
        this.composer.addPass(this.bloomPass);
    }
}
```

### 7.2 Bloom Parameters

| Parameter | Value | Effect |
|-----------|-------|--------|
| Strength | 1.0 | Moderate glow intensity |
| Radius | 0.4 | Wide bloom spread |
| Threshold | 0.15 | Only bright elements bloom |

---

## 8. Neighborhood Boundary System

### 8.1 Boundary Rendering

Neighborhoods (fiefdoms) render as:
1. **Polygon mesh:** Semi-transparent fill (alpha: 0.15)
2. **Edge lines:** Perimeter outline (alpha: 0.4)
3. **Label sprite:** Floating text above boundary
4. **Integration badge:** Purple circle with count

```javascript
addNeighborhoodBoundaries(neighborhoods, scale = 10) {
    for (const neighborhood of neighborhoods) {
        // Create ShapeGeometry from boundary points
        const shape = new THREE.Shape();
        shape.moveTo(points3D[0].x, points3D[0].z);
        
        const geometry = new THREE.ShapeGeometry(shape);
        const material = new THREE.MeshBasicMaterial({
            color: boundaryColor,
            transparent: true,
            opacity: 0.15,
            depthWrite: false
        });
    }
}
```

### 8.2 Lock Indicators

Locked buildings show a 🔒 sprite above them:
```javascript
createLockIndicator(buildingData) {
    const canvas = document.createElement('canvas');
    // Draw lock emoji
    const texture = new THREE.CanvasTexture(canvas);
    const sprite = new THREE.Sprite(material);
    sprite.position.set(x, buildingHeight + 1.5, z);
    return sprite;
}
```

---

## 9. Integration Points for a_codex_plan

### 9.1 Required Extensions

For the 3D engine to support interactive node selection in `a_codex_plan`:

1. **Add Raycaster:**
   ```javascript
   this.raycaster = new THREE.Raycaster();
   this.mouse = new THREE.Vector2();
   ```

2. **Add Click Handler:**
   ```javascript
   _initInteractionHandlers() {
       this.renderer.domElement.addEventListener('click', (e) => {
           // Normalize mouse coordinates
           this.mouse.x = (e.clientX / this.container.clientWidth) * 2 - 1;
           this.mouse.y = -(e.clientY / this.container.clientHeight) * 2 + 1;
           
           // Raycast
           this.raycaster.setFromCamera(this.mouse, this.camera);
           const intersects = this.raycaster.intersectObjects(
               this.buildingMeshes.map(m => m.particles)
           );
           
           if (intersects.length > 0) {
               const path = intersects[0].object.userData.path;
               this._notifyParent('WOVEN_MAPS_NODE_CLICK', { path });
           }
       });
   }
   ```

3. **Add Hover Handler:**
   ```javascript
   _initHoverHighlight() {
       // Add mouse move listener
       // Update cursor style
       // Highlight hovered building
   }
   ```

### 9.2 Communication Bridge

To integrate with the existing message protocol:

```javascript
_notifyParent(type, payload) {
    if (window.parent !== window) {
        window.parent.postMessage({ type, node: payload }, '*');
    }
}
```

### 9.3 State Synchronization Hook

```javascript
// Called from Python via iframe bridge
handleMessage(event) {
    const { type, payload } = event.data;
    
    switch (type) {
        case 'UPDATE_BUILDING_STATUS':
            this.updateBuildingStatus(payload.path, payload.status);
            break;
        case 'LOAD_BUILDINGS':
            this.loadBuildings(payload.buildings);
            break;
        case 'TRANSITION_CAMERA':
            this.transitionTo(payload.keyframe, payload.duration);
            break;
    }
}
```

---

## 10. Performance Considerations

### 10.1 Payload Size Guard

Per CLAUDE.md session notes:
- Default max payload: 9,000,000 bytes
- Falls back to `IP/` root when oversized
- Stream budget for progressive loading: 5,000,000 bytes/sec

### 10.2 Optimization Strategies

| Technique | Implementation |
|-----------|---------------|
| **BufferGeometry** | All particles use typed arrays |
| **Additive Blending** | No depth sorting required |
| **Shader Discard** | Transparent fragments skipped |
| **Resize Handler** | Updates camera aspect + renderer size |
| **RequestAnimationFrame** | Smooth 60fps render loop |

---

## 11. Configuration Reference

```javascript
const CONFIG_3D = {
    // Colors
    COLOR_WORKING: 0xD4AF37,   // Gold
    COLOR_BROKEN: 0x1fbdea,    // Teal
    COLOR_COMBAT: 0x9D4EDD,    // Purple
    COLOR_LOCKED: 0xff6b6b,   // Red
    COLOR_VOID: 0x0A0A0B,      // Background
    
    // Camera
    CAMERA_FOV: 50,
    CAMERA_NEAR: 0.1,
    CAMERA_FAR: 500,
    
    // Controls
    DAMPING_FACTOR: 0.05,
    AUTO_ROTATE_SPEED: 0.3,
    
    // Animation
    KEYFRAME_DURATION: 2000,
    EASE_CUBIC: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    
    // Post-processing
    BLOOM_STRENGTH: 1.0,
    BLOOM_RADIUS: 0.4,
    BLOOM_THRESHOLD: 0.15,
    
    // Fog
    FOG_DENSITY: 0.025,
    
    // Particles
    PARTICLE_MIN_SIZE: 0.3,
    PARTICLE_MAX_SIZE: 0.7,
};
```

---

## 12. Conclusion

The Code City 3D engine is a sophisticated **stateless renderer** that visualizes software architecture as emergent particle cityscapes. Its architecture deliberately separates:

- **Rendering:** Pure Three.js with custom shaders
- **State:** Maintained by parent Python/Marimo
- **Interaction:** Handled by 2D canvas sibling (or must be added)

For `a_codex_plan` integration, the 3D engine requires extension with raycaster-based interaction handlers and message bridge integration to participate in the existing communication protocol.

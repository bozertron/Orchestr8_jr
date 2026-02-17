# static/woven_maps_3d.js Integration Guide

- Source: `IP/static/woven_maps_3d.js`
- Total lines: `~450`
- Role: **Three.js 3D Renderer** — Code City visualization with Barradeau particle technique

## Why This Is Painful

- Three.js scene setup requires proper initialization order
- Post-processing (UnrealBloomPass) must be configured correctly
- Emergence animation must NOT include breathing/pulsing
- Color uniforms must accept three-state system

## Anchor Lines

- `IP/static/woven_maps_3d.js:15` — `CONFIG_3D` — All rendering constants
- `IP/static/woven_maps_3d.js:17-20` — Canonical colors (0xD4AF37, 0x1fbdea, 0x9D4EDD)
- `IP/static/woven_maps_3d.js:51` — `class CodeCityScene` — Main scene manager
- `IP/static/woven_maps_3d.js:62` — `_initScene()` — Renderer with void background
- `IP/static/woven_maps_3d.js:76` — `_initCamera()` — PerspectiveCamera setup
- `IP/static/woven_maps_3d.js:91` — `_initControls()` — OrbitControls with damping
- `IP/static/woven_maps_3d.js:107` — `_initPostProcessing()` — EffectComposer + UnrealBloomPass
- `IP/static/woven_maps_3d.js:149` — `getStatusColor(status)` — Color mapping
- `IP/static/woven_maps_3d.js:161` — `createBuildingMesh()` — Particle mesh from BuildingData
- `IP/static/woven_maps_3d.js:215` — `createBuildingLines()` — Wireframe mesh
- `IP/static/woven_maps_3d.js:285` — `playEmergenceAnimation()` — Particles coalesce from Void

## Integration Use

```javascript
// Initialize
const scene = new CodeCityScene(document.getElementById('container'));
scene.start();

// Load buildings from Python BuildingData
scene.loadBuildings(buildingDataArray);

// Update status
scene.updateBuildingStatus('IP/woven_maps.py', 'broken');

// Play emergence animation
scene.playEmergenceAnimation(2000);

// Cleanup
scene.dispose();
```

## Emergence Pattern (LOCKED)

- Particles start scattered in Void (random positions)
- Coalesce to building positions over duration
- Ease-out cubic curve for smooth finish
- NO sin/cos oscillation after emergence

## Resolved Gaps

- [x] Three.js scene with black background (#0A0A0B)
- [x] OrbitControls with damping and auto-rotate
- [x] UnrealBloomPass for soft particle glow
- [x] Building mesh creation from BuildingData
- [x] Emergence animation (no breathing)

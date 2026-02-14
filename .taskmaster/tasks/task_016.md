# Task ID: 16

**Title:** 3D Code City Frontend Compatibility Checklist

**Status:** pending

**Dependencies:** 15

**Priority:** medium

**Description:** Create and execute compatibility checklist for IP/static/woven_maps_3d.js including Three.js version compatibility, WebGL feature detection, and graceful degradation paths.

**Details:**

1. Create compatibility checklist document:
   - Three.js version requirements (check r150+ for WebGPU support)
   - WebGL 1.0 vs 2.0 feature usage
   - OrbitControls API compatibility
   - EffectComposer/UnrealBloomPass requirements

2. Audit woven_maps_3d.js for:
   - WebGPU usage (navigator.gpu checks)
   - Fallback to CPU canvas per CLAUDE.md
   - Pixel ratio handling for high-DPI
   - ResizeObserver vs window.resize

3. Verify fallback paths:
```javascript
// Check current implementation
function initParticleBackend() {
    if (navigator.gpu) {
        return initWebGPUBackend();
    }
    return initCPUCanvasBackend();
}
```

4. Add feature detection guards:
```javascript
const FEATURES = {
    webgl2: !!document.createElement('canvas').getContext('webgl2'),
    webgpu: !!navigator.gpu,
    bloom: true, // Disable if performance issues
};
```

5. Document mobile/low-power device considerations

6. Create IP/static/woven_maps_3d_compatibility.md checklist

**Test Strategy:**

1. Test with WebGL disabled (browser flag)
2. Test on integrated graphics (if available)
3. Verify graceful degradation shows fallback UI
4. Check console for WebGL/Three.js errors
5. Profile GPU memory usage

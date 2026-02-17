# 3D Code City Frontend Compatibility Checklist

**Generated:** 2026-02-13  
**File:** `IP/static/woven_maps_3d.js`

---

## 1. Three.js Version Requirements

| Item | Status | Details |
|------|--------|---------|
| **Three.js Version** | ✅ PASS | r128 (CDN: cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js) |
| **Release Date** | ⚠️ NOTE | r128 released ~March 2020 - relatively old but stable |
| **Dependencies Loaded** | ✅ PASS | All required modules available at matching version (three@0.128.0) |

**Loaded Dependencies:**
- `three.min.js` (r128)
- `OrbitControls.js`
- `EffectComposer.js`
- `RenderPass.js`
- `UnrealBloomPass.js`
- `CopyShader.js`, `LuminosityHighPassShader.js`

---

## 2. WebGPU Usage Audit

| Item | Status | Details |
|------|--------|---------|
| **WebGPU in woven_maps_3d.js** | ✅ NOT USED | Uses `THREE.WebGLRenderer` only |
| **WebGPU in woven_maps.py (2D)** | ✅ HAS FALLBACK | `ParticleGPUField` class has CPU Canvas fallback |
| **WebGPU Detection** | ✅ PASS | Only in 2D particle system, has graceful fallback |

**WebGPU in 2D Woven Maps (woven_maps.py):**
```javascript
async function initParticleBackend() {
    if (!navigator.gpu) {
        backendState.mode = 'CPU Canvas';  // Fallback works correctly
        return;
    }
    // ... WebGPU initialization with try/catch fallback
}
```

**Conclusion:** The 3D Code City (`woven_maps_3d.js`) does NOT use WebGPU and will work on any browser with WebGL support.

---

## 3. WebGL Version Compatibility

| Feature | WebGL 1.0 | WebGL 2.0 | Notes |
|---------|-----------|-----------|-------|
| `THREE.WebGLRenderer` | ✅ | ✅ | Auto-detects, uses 2.0 if available |
| `BufferGeometry` | ✅ | ✅ | Standard in both versions |
| `ShaderMaterial` | ✅ | ✅ | GLSL 1.0 compatible |
| `gl_PointSize` | ✅ | ✅ | Used in vertex shader |
| `gl_PointCoord` | ✅ | ✅ | Used in fragment shader |
| `smoothstep()` | ✅ | ✅ | Standard GLSL function |
| `additiveBlending` | ✅ | ✅ | Standard blending mode |

**GLSL Version:** Shaders use GLSL 1.0 syntax (compatible with both WebGL 1.0 and 2.0)

---

## 4. Fallback to CPU Canvas

| Item | Status | Details |
|------|--------|---------|
| **CPU Fallback Exists** | ✅ YES | The 2D particle system has CPU Canvas fallback |
| **3D Scene Fallback** | ⚠️ MANUAL | No automatic fallback - requires WebGL |
| **WebGL Check** | ❌ MISSING | No explicit WebGL availability check in 3D code |

**Recommendation:** Add WebGL availability check before initializing `CodeCityScene`:

```javascript
function isWebGLAvailable() {
    try {
        const canvas = document.createElement('canvas');
        return !!(window.WebGLRenderingContext && 
            (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
        return false;
    }
}
```

---

## 5. Pixel Ratio Handling (High-DPI)

| Item | Status | Details |
|------|--------|---------|
| **Pixel Ratio Set** | ✅ PASS | `this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` |
| **Capped at 2x** | ✅ GOOD | Prevents performance issues on high-DPI displays (Retina, 4K) |
| **Composer Sized** | ✅ PASS | `this.composer.setSize(width, height)` called in resize |

**Line 108 in woven_maps_3d.js:**
```javascript
this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

This is good practice - capping at 2x prevents:
- Excessive GPU memory usage
- Slow rendering on very high DPI displays
- Battery drain on mobile devices

---

## 6. ResizeObserver vs window.resize

| Item | Status | Details |
|------|--------|---------|
| **Current Implementation** | ⚠️ BASIC | Uses `window.addEventListener('resize', ...)` |
| **ResizeObserver** | ❌ NOT USED | Could improve performance for embedded iframes |
| **Resize Handler** | ✅ WORKS | Correctly updates camera, renderer, and composer |

**Current Implementation (Line 182-191):**
```javascript
_initResizeHandler() {
    window.addEventListener('resize', () => {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        
        this.renderer.setSize(width, height);
        this.composer.setSize(width, height);
    });
}
```

**Recommendation:** Consider ResizeObserver for better iframe/embedded usage, but current implementation works fine for standalone pages.

---

## 7. Feature Detection Guards Needed

| Feature | Required | Current | Action |
|---------|----------|---------|--------|
| **WebGL 1.0** | Yes | No check | Add guard (optional) |
| **WebGL 2.0** | No | Auto-detect | OK |
| **requestAnimationFrame** | Yes | Assumed | OK |
| **Float32Array** | Yes | Assumed | OK (modern browsers) |
| **ES6 Classes** | Yes | Assumed | OK (modern browsers) |

---

## 8. Browser Compatibility Matrix

| Browser | WebGL 1.0 | WebGL 2.0 | Expected Result |
|---------|-----------|-----------|-----------------|
| Chrome 56+ | ✅ | ✅ | Full support |
| Firefox 51+ | ✅ | ✅ | Full support |
| Safari 15+ | ✅ | ✅ | Full support |
| Edge 79+ | ✅ | ✅ | Full support |
| Chrome Android | ✅ | ✅ | Full support |
| Safari iOS 15+ | ✅ | ✅ | Full support |
| IE 11 | ⚠️ | ❌ | May work (Three.js r128) |

**Minimum Supported:** Chrome 56, Firefox 51 (released 2017)

---

## 9. Summary & Recommendations

### ✅ Already Implemented Correctly
1. Three.js r128 with matching dependency versions
2. WebGL fallback to CPU canvas in 2D particle system
3. Pixel ratio capped at 2x for performance
4. Resize handler updates all components (camera, renderer, composer)
5. GLSL shaders compatible with WebGL 1.0 and 2.0

### ⚠️ Minor Improvements (Optional)
1. **Add WebGL availability check** before initializing 3D scene
2. **Consider ResizeObserver** if embedding in iframes becomes common

### ❌ Not Required
- WebGPU support in 3D scene (uses WebGL)
- Advanced feature detection (standard browsers assumed)

---

## 10. Compatibility Status: APPROVED

The `woven_maps_3d.js` file is compatible with the current codebase and browser requirements. No code changes are strictly required for compatibility.

**Verified Against:**
- CLAUDE.md Section: "Code City 3D payload strategy" (GPU-first + CPU fallback)
- Three.js version loaded in woven_maps.py
- WebGPU detection in particle backend with fallback

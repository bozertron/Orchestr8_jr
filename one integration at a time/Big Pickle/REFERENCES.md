# Orchestr8 Visual References Library

A curated collection of techniques, libraries, and inspiration for the Code City visualization system.

---

## Core Algorithm - Woven Maps

**Author:** Nicolas Barradeau
**Source:** <https://barradeau.com/blog/?p=763>

### The Algorithm

1. Collect points (files in codebase)
2. Delaunay triangulation
3. Compute edge lengths
4. Render gradient layers (translate canvas, fade alpha, draw short edges)
5. Wireframe overlays
6. Optional: color overlay, glow effects

### Key Code Pattern

```javascript
function renderEdges(edges, min) {
    ctx.beginPath();
    for (const edge of edges) {
        if (edge[0] < min) {  // Only draw edges shorter than threshold
            ctx.moveTo(edge[1].x, edge[1].y);
            ctx.lineTo(edge[2].x, edge[2].y);
        }
    }
    ctx.stroke();
}

// The magic: creates 3D cityscape illusion
for (let i = 0; i < maxHeight; i++) {
    ctx.translate(0, 1);
    ctx.globalAlpha = (1 - i / maxHeight) * 0.05;
    renderEdges(edges, i);
}
```

---

## Particle Systems

### FBO Particles (GPU-Accelerated)

**Author:** Nicolas Barradeau
**Tutorial:** <https://barradeau.com/blog/?p=621>
**Implementation:** <https://github.com/marioecg/gpu-party>

**Concept:** Store particle positions/velocities in GPU textures, compute physics via shaders.

**Ping-Pong Pattern:**

```
Frame 1: Read TextureA → Compute → Write TextureB
Frame 2: Read TextureB → Compute → Write TextureA
```

**Capacity:** 100,000+ particles (vs ~1,000 on CPU)

### Volume Distribution

**Repo:** <https://github.com/nicoptere/volume_distribution>

**Technique:** Scatter particles inside arbitrary 3D meshes using raycasting.

- Shoot rays from inflated bounding box
- Count intersections (odd = inside, even = outside)
- Returns position/destination arrays for shader animation

### Curl Noise

**Purpose:** Organic, swirling particle motion

**Vertex Shader Pattern:**

```glsl
vec3 target = position + curl(pos.x * freq, pos.y * freq, pos.z * freq) * amplitude;
float d = length(newpos - target) / maxDistance;
newpos = mix(position, target, pow(d, 4.));  // Smooth ease-out
```

---

## Audio-Reactive Systems

### BPM Detection

**Article:** <https://jmperezperez.com/blog/bpm-detection-javascript/>
**Library:** <https://github.com/chrisguttandin/web-audio-beat-detector>

```javascript
import { guess } from 'web-audio-beat-detector';
const { bpm } = await guess(audioBuffer);
const interval = 60000 / bpm;  // ms between beats
setInterval(() => dispatchEvent({ type: 'beat' }), interval);
```

### Frequency Analysis

```javascript
// Segment frequency spectrum into bands
const lowFreqStart = Math.floor((10 * bufferLength) / sampleRate);
const lowFreqEnd = Math.floor((250 * bufferLength) / sampleRate);
const lowAvg = normalizeValue(calculateAverage(frequencyArray, lowFreqStart, lowFreqEnd));
// Repeat for mid (250-2000Hz) and high (2000-20000Hz)
```

### Audio → Visual Mapping (Coala Pattern)

```javascript
amplitude = 0.8 + mapLinear(frequencyData.high, 0, 0.6, -0.1, 0.2)
offsetGain = frequencyData.mid * 0.6
time += clamp(mapLinear(frequencyData.low, 0.6, 1, 0.2, 0.5), 0.2, 0.5)
```

---

## Animation Libraries

### GSAP (GreenSock)

**Repo:** <https://github.com/greensock/GSAP>
**Purpose:** Industry-standard web animation library

**Key Features:**

- Timeline sequencing
- Advanced easing functions
- ScrollTrigger for scroll-based animations
- MorphSVG for shape morphing

**Pattern:**

```javascript
gsap.to(element, {
    duration: 1,
    x: 100,
    ease: "power2.out",
    onComplete: () => console.log("done")
});
```

---

## GPU Computing / Processing

### PixelFlow (Java/Processing)

**Repo:** <https://github.com/diwi/PixelFlow>

**Capabilities:**

- Optical flow
- Fluid simulation
- Soft-body dynamics
- GPU particles
- Post-processing effects

**Relevance:** Reference for GPU-accelerated visual effects patterns.

### JRubyArt

**Repo:** <https://github.com/ruby-processing/JRubyArt>
**Examples:** <https://github.com/ruby-processing/JRubyArt-examples>

**Purpose:** Creative coding in Ruby (Processing port)

---

## Geographic / Tile-Based

### Cartography

**Repo:** <https://github.com/nicoptere/cartography>

**Capabilities:**

- XYZ tileset rendering in Three.js
- Elevation mapping
- Geographic data visualization

**Relevance:** Tile-based chunking for large codebases, elevation = metrics.

---

## Phase-Based Animation (stereOS Pattern)

From the AwakeningEngine reference:

```typescript
enum Phase {
    VOID,        // Nothing visible
    AWAKENING,   // Initial stirring
    TUNING,      // Calibrating
    COALESCING,  // Coming together
    EMERGENCE,   // Final formation
    TRANSITION,  // Color shift (teal → gold)
    READY        // Complete
}
```

**Wave Field Interference:**

```javascript
const d1 = Math.sqrt((x - sourceLeftX) ** 2 + y ** 2);
const d2 = Math.sqrt((x - sourceRightX) ** 2 + y ** 2);
const wave1 = Math.sin(d1 * freq - elapsed * speed) * amp;
const wave2 = Math.sin(d2 * freq * 0.8 - elapsed * speed * 0.7) * amp * 0.6;
```

---

## Color System (EXACT - NO EXCEPTIONS)

```
Gold (#D4AF37)   - Working code, completion state
Blue (#1fbdea)   - Broken code, scanning state (teal)
Purple (#9D4EDD) - Combat state (LLM deployed)
Void (#0A0A0B)   - Background
Surface (#121214) - Elevated elements
```

---

## Implementation Tiers

### Tier 1: Canvas 2D (Current)

- ✅ Woven Maps algorithm
- ✅ Emergence animations
- ✅ Teal → Gold transitions
- ✅ Curl-like particle approximation
- ✅ Wave field distortion

### Tier 2: Three.js + GSAP (Near-term)

- WebGL rendering
- True 3D camera
- GSAP timeline animations
- Proper curl noise in shaders

### Tier 3: FBO + Audio (Ambitious)

- GPU particle physics
- 100k+ particles
- Audio-reactive via web-audio-beat-detector
- Real-time frequency mapping

---

## Key Principles

1. **Things EMERGE from the void** - No breathing animations
2. **Teal during scan, Gold on completion** - Phase-based color
3. **Low frequency waves** - Smooth landscape morphing, not noise
4. **Distance-based staggering** - Elements further from center emerge later
5. **Exponential decay** - `pow(1 - progress, 2)` for natural fade

---

*Last updated: 2026-01-26*
*For future Claude instances: This document preserves context for the Code City visualization system.*

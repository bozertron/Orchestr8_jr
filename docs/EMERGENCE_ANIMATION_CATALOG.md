# Emergence Animations: Complete Compatibility Catalog

**Purpose:** Every technique for "emerge from void" animations, with compatibility notes for Marimo  
**Created:** 2026-01-26  
**Last Updated:** 2026-01-26  
**Status:** EXPANDED GOLDMINE - DROOL-WORTHY REFERENCE LIBRARY

**NEW SECTIONS ADDED:**
- 9. Nicolas Barradeau Collection (FBO Particles, Woven Maps, Active Contour, 3D Point Distribution)
- 10. Mathematical Landscapes for Morphing (Python)
- 11. Cesium Particle System (GPU Wind Fields)
- 12. Audio-Reactive Enhanced (Frequency Bands, BPM, Curl Noise)

**DESIGNATED TARGETS:**
- **CODE MAP:** Section 9.2 - Woven Maps (Delaunay triangulation cityscapes)
- **MORPHING:** Section 10.1 - landscapes library (rastrigin → ackley → rosenbrock)

---

## Table of Contents

1. [Compatibility Matrix](#compatibility-matrix)
2. [Layer 1: Pure CSS (Fully Compatible)](#layer-1-pure-css-fully-compatible)
3. [Layer 2: CSS + HTML Head Injection](#layer-2-css--html-head-injection)
4. [Layer 3: JavaScript Animation Libraries](#layer-3-javascript-animation-libraries)
5. [Layer 4: WebGL / Three.js](#layer-4-webgl--threejs)
6. [Layer 5: Python-Driven Browser Rendering](#layer-5-python-driven-browser-rendering)
7. [Layer 6: SVG Animations](#layer-6-svg-animations)
8. [Layer 7: Lottie Animations](#layer-7-lottie-animations)
9. [Accessibility: Reduced Motion](#accessibility-reduced-motion)
10. [Code Snippets Library](#code-snippets-library)
11. [EXPANSION: Nicolas Barradeau Collection](#expansion-nicolas-barradeau-collection)
    - [9.1 FBO Particles](#91-fbo-particles-p621---gpu-particle-engine)
    - [9.2 Woven Maps (CODE MAP TARGET)](#92-woven-maps-p1001---target-code-map-visualization)
    - [9.3 Woven Maps Controls Spec](#93-woven-maps-controls---future-development-spec)
    - [9.4 Active Contour Model](#94-active-contour-model-p1032---morphological-snakes)
    - [9.5 Random Points in 3D Mesh](#95-random-points-in-3d-mesh-p1058)
12. [EXPANSION: Mathematical Landscapes](#expansion-mathematical-landscapes-for-morphing)
    - [10.1 landscapes Library](#101-landscapes-library-python)
    - [10.2 spatial-analysis](#102-spatial-analysis-python)
13. [EXPANSION: Cesium Particle System](#expansion-cesium-particle-system)
14. [EXPANSION: Audio-Reactive Details](#expansion-audio-reactive-details)
15. [Updated Compatibility Matrix](#updated-compatibility-matrix)

---

## Compatibility Matrix

| Technique | Marimo Compatible | Integration Method | Performance | Complexity |
|-----------|-------------------|-------------------|-------------|------------|
| **Pure CSS Keyframes** | ✅ Full | Custom CSS file | Excellent | Low |
| **CSS Transitions** | ✅ Full | .style() or mo.Html | Excellent | Low |
| **CSS Particles (no JS)** | ✅ Full | Custom CSS + mo.Html | Good | Medium |
| **GSAP** | ✅ Via mo.iframe | HTML head / iframe | Excellent | Medium |
| **Anime.js** | ✅ Via mo.iframe | HTML head / iframe | Excellent | Medium |
| **Lottie** | ✅ Via mo.iframe | HTML head / iframe | Excellent | Low |
| **Three.js/WebGL** | ⚠️ Partial | mo.iframe only | GPU-accelerated | High |
| **p5.js** | ✅ Via widget | p5-widget package | Good | Medium |
| **Bokeh WebGL** | ✅ Native | output_backend="webgl" | GPU-accelerated | Low |
| **pythreejs** | ❓ Untested | anywidget wrapper? | GPU-accelerated | High |
| **SVG SMIL** | ⚠️ Limited | mo.Html inline | Good | Medium |
| **SVG CSS** | ✅ Full | Custom CSS + mo.Html | Excellent | Medium |
| **PyScript/Pyodide WebGL** | ❓ Experimental | iframe | GPU-accelerated | Very High |

**Legend:**
- ✅ Full = Works directly in Marimo cells
- ⚠️ Partial = Works with limitations
- ❓ Untested = Theoretically possible, needs testing

---

## Layer 1: Pure CSS (Fully Compatible)

### 1.1 Keyframe Animations

**Integration:** Via `custom_css` in pyproject.toml or inline in mo.Html

```css
/* Emerge from void - fade + scale */
@keyframes emerge-void {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Emerge from direction */
@keyframes emerge-right {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes emerge-down {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes emerge-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Pop with slight overshoot */
@keyframes emerge-pop {
    0% { opacity: 0; transform: scale(0.8); }
    70% { transform: scale(1.02); }
    100% { opacity: 1; transform: scale(1); }
}
```

### 1.2 Pure CSS Particles (No JavaScript)

**Source:** [CSS Only Particles](https://dev.to/code_mystery/css-only-animated-background-particles-effects-52d)

```html
<!-- HTML Structure -->
<div class="particle purple"></div>
<div class="particle blue"></div>
<div class="particle gold"></div>
```

```scss
// SCSS with random positioning
$colors: (
    purple: #9D4EDD,
    blue: #1fbdea,
    gold: #D4AF37
);

@function random-num($min, $max) {
    @return floor(random() * ($max - $min) + $min);
}

@each $name, $hex in $colors {
    $size: random-num(5, 20);
    $x1: random-num(0, 100);
    $y1: random-num(0, 100);
    $x2: random-num(0, 100);
    $y2: random-num(0, 100);
    
    .particle.#{$name} {
        position: absolute;
        width: #{$size}px;
        height: #{$size}px;
        background: $hex;
        border-radius: 50%;
        left: #{$x1}vw;
        top: #{$y1}vh;
        animation: float-#{$name} 10s ease-in-out infinite;
        opacity: 0.6;
    }
    
    @keyframes float-#{$name} {
        50% { transform: translate(#{$x2 - $x1}vw, #{$y2 - $y1}vh); }
        100% { transform: translate(0, 0); }
    }
}
```

**Pure CSS Version (No SCSS):**

```css
/* Pure CSS Floating Particles */
.particles-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    z-index: -1;
}

.particle {
    position: absolute;
    border-radius: 50%;
    animation: float 15s ease-in-out infinite;
}

.particle:nth-child(1) {
    width: 10px; height: 10px;
    background: #D4AF37;
    left: 10%; top: 20%;
    animation-delay: 0s;
}

.particle:nth-child(2) {
    width: 15px; height: 15px;
    background: #1fbdea;
    left: 30%; top: 40%;
    animation-delay: -2s;
}

.particle:nth-child(3) {
    width: 8px; height: 8px;
    background: #9D4EDD;
    left: 70%; top: 60%;
    animation-delay: -4s;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    25% { transform: translate(20px, -30px) rotate(90deg); }
    50% { transform: translate(-20px, 20px) rotate(180deg); }
    75% { transform: translate(30px, 10px) rotate(270deg); }
}
```

### 1.3 Staggered Emergence

```css
/* Stagger children emergence */
.stagger-container > * {
    opacity: 0;
    animation: emerge-void 0.3s ease-out forwards;
}

.stagger-container > *:nth-child(1) { animation-delay: 0.0s; }
.stagger-container > *:nth-child(2) { animation-delay: 0.1s; }
.stagger-container > *:nth-child(3) { animation-delay: 0.2s; }
.stagger-container > *:nth-child(4) { animation-delay: 0.3s; }
.stagger-container > *:nth-child(5) { animation-delay: 0.4s; }
/* ... continue as needed */
```

---

## Layer 2: CSS + HTML Head Injection

### 2.1 Loading External Fonts with Animation

**File:** `head.html`

```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Global animation styles -->
<style>
    /* Ensure fonts are loaded before showing text */
    .font-loaded {
        animation: emerge-void 0.3s ease-out forwards;
    }
    
    @keyframes emerge-void {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
</style>
```

**Configuration:**

```python
# In Marimo notebook
app = marimo.App(html_head_file="head.html")
```

---

## Layer 3: JavaScript Animation Libraries

### 3.1 GSAP (GreenSock)

**CDN:** `https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js`

**Integration via mo.iframe:**

```python
@app.cell
def _():
    gsap_animation = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js"></script>
        <style>
            body { margin: 0; background: #0A0A0B; overflow: hidden; }
            .box {
                width: 100px;
                height: 100px;
                background: #D4AF37;
                border-radius: 4px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }
        </style>
    </head>
    <body>
        <div class="box"></div>
        <script>
            // Emerge animation
            gsap.from(".box", {
                duration: 0.6,
                scale: 0,
                opacity: 0,
                ease: "back.out(1.7)"
            });
            
            // Continuous subtle float
            gsap.to(".box", {
                y: "+=10",
                duration: 2,
                ease: "sine.inOut",
                yoyo: true,
                repeat: -1
            });
        </script>
    </body>
    </html>
    """
    mo.iframe(gsap_animation, width="100%", height="300px")
```

**GSAP Features:**
- `gsap.to()` / `gsap.from()` / `gsap.fromTo()` - Basic tweens
- `gsap.timeline()` - Sequence animations
- `ScrollTrigger` - Scroll-based animations
- `stagger` - Built-in stagger support
- Easing: `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"power2.inOut"`

### 3.2 Anime.js

**CDN:** `https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js`  
**CDN v4:** `https://cdn.jsdelivr.net/npm/animejs@4.0.1/lib/anime.iife.min.js`

**Key Features (from official docs):**
- Per property parameters
- Flexible keyframes system
- Built-in easings
- Individual CSS Transforms
- Function based values
- Scroll Observer (sync animations with scroll)
- Advanced staggering (time, values, timeline positions)
- SVG morphing, line drawing, motion path
- Draggable API with springs
- Timeline orchestration
- Responsive animations (media queries)
- **Bundle size:** 24.50KB (modular - import only what you need)

**Code Examples from Anime.js:**

```javascript
// Basic emerge
animate('.square', {
    rotate: 90,
    scale: [0, 1],
    opacity: [0, 1],
    duration: 600,
    ease: 'inOutExpo',
});

// Random positions with blending
animate('.shape', {
    x: random(-100, 100),
    y: random(-100, 100),
    rotate: random(-180, 180),
    duration: random(500, 1000),
    composition: 'blend',
});

// SVG motion path + line drawing
animate('.car', {
    ...createMotionPath('.circuit'),
});

animate(createDrawable('.circuit'), {
    draw: '0 1',
});

// SVG morphing
animate('.circuit-a', {
    d: morphTo('.circuit-b'),
});

// Staggered grid animation
const options = {
    grid: [13, 13],
    from: 'center',
};

createTimeline()
    .add('.dot', {
        scale: stagger([1.1, .75], options),
        ease: 'inOutQuad',
    }, stagger(200, options));

// Scroll-synced drawing
animate(createDrawable('path'), {
    draw: ['0 0', '0 1', '1 1'],
    delay: stagger(40),
    ease: 'inOut(3)',
    autoplay: onScroll({ sync: true }),
});

// Spring physics draggable
createDraggable('.circle', {
    releaseEase: createSpring({
        stiffness: 120,
        damping: 6,
    })
});
```

### 3.3 Integration Pattern for Both

```python
@app.cell
def _():
    def create_animated_iframe(html_content: str, height: str = "400px") -> mo.Html:
        """Wrap HTML with animation library in iframe for isolation."""
        return mo.iframe(html_content, width="100%", height=height)
    return create_animated_iframe
```

---

## Layer 4: WebGL / Three.js

### 4.1 Three.js Audio-Reactive Particles

**Source:** [Codrops Tutorial](https://tympanus.net/codrops/2023/12/19/creating-audio-reactive-visuals-with-dynamic-particles-in-three-js/)  
**GitHub:** [tgcnzn/Interactive-Particles-Music-Visualizer](https://github.com/tgcnzn/interactive-particles-music-visualizer)

**Key Components:**

```javascript
// Scene initialization (after user click for audio autoplay)
export default class App {
    constructor() {
        this.onClickBinder = () => this.init()
        document.addEventListener('click', this.onClickBinder)
    }

    init() {
        document.removeEventListener('click', this.onClickBinder)
        this.renderer = new THREE.WebGLRenderer()
        this.camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 10000)
        this.scene = new THREE.Scene()
    }
}

// Audio frequency analysis
this.lowFrequency = 10;
this.frequencyArray = this.audioAnalyser.getFrequencyData();
const lowFreqRangeStart = Math.floor((this.lowFrequency * this.bufferLength) / this.audioContext.sampleRate)
const lowFreqRangeEnd = Math.floor((this.midFrequency * this.bufferLength) / this.audioContext.sampleRate)
const lowAvg = this.normalizeValue(this.calculateAverage(this.frequencyArray, lowFreqRangeStart, lowFreqRangeEnd));

// BPM detection with web-audio-beat-detector
const { bpm } = await guess(audioBuffer);
this.interval = 60000 / bpm;
this.intervalId = setInterval(() => {
    this.dispatchEvent({ type: 'beat' })
}, this.interval);

// Procedural geometry
const geometry = new THREE.BoxGeometry(1, 1, 1, widthSeg, heightSeg, depthSeg)
const material = new THREE.ShaderMaterial({
    side: THREE.DoubleSide,
    vertexShader: vertex,
    fragmentShader: fragment,
    transparent: true,
    uniforms: {
        size: { value: 2 },
    },
})
const pointsMesh = new THREE.Points(geometry, material)

// Vertex shader with curl noise
vec3 newpos = position;
vec3 target = position + (normal * .1) + curl(newpos.x * frequency, newpos.y * frequency, newpos.z * frequency) * amplitude;
float d = length(newpos - target) / maxDistance;
newpos = mix(position, target, pow(d, 4.));
newpos.z += sin(time) * (.1 * offsetGain);
gl_PointSize = size + (pow(d,3.) * offsetSize) * (1./-mvPosition.z);

// Fragment shader with color interpolation
vec3 circ = vec3(circle(uv,1.));
vec3 color = mix(startColor,endColor,vDistance);
gl_FragColor=vec4(color,circ.r * vDistance);

// Audio-reactive updates
update() {
    this.material.uniforms.amplitude.value = 0.8 + THREE.MathUtils.mapLinear(App.audioManager.frequencyData.high, 0, 0.6, -0.1, 0.2)
    this.material.uniforms.offsetGain.value = App.audioManager.frequencyData.mid * 0.6
    const t = THREE.MathUtils.mapLinear(App.audioManager.frequencyData.low, 0.6, 1, 0.2, 0.5)
    this.time += THREE.MathUtils.clamp(t, 0.2, 0.5)
    this.material.uniforms.time.value = this.time
}
```

**Dependencies:**
- three.js
- GSAP
- web-audio-beat-detector
- WebGL Noise (Ashima)

### 4.2 Marimo + Three.js via iframe

```python
@app.cell
def _():
    threejs_scene = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
        <style>
            body { margin: 0; background: #0A0A0B; }
            canvas { display: block; }
        </style>
    </head>
    <body>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor(0x0A0A0B);
            document.body.appendChild(renderer.domElement);
            
            // Create particles
            const geometry = new THREE.BufferGeometry();
            const vertices = [];
            for (let i = 0; i < 1000; i++) {
                vertices.push(
                    (Math.random() - 0.5) * 10,
                    (Math.random() - 0.5) * 10,
                    (Math.random() - 0.5) * 10
                );
            }
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
            
            const material = new THREE.PointsMaterial({
                color: 0xD4AF37,
                size: 0.05
            });
            
            const particles = new THREE.Points(geometry, material);
            scene.add(particles);
            camera.position.z = 5;
            
            // Emerge animation
            particles.scale.set(0, 0, 0);
            const emergeSpeed = 0.02;
            
            function animate() {
                requestAnimationFrame(animate);
                
                // Emerge effect
                if (particles.scale.x < 1) {
                    particles.scale.x += emergeSpeed;
                    particles.scale.y += emergeSpeed;
                    particles.scale.z += emergeSpeed;
                }
                
                particles.rotation.y += 0.001;
                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    """
    mo.iframe(threejs_scene, width="100%", height="400px")
```

---

## Layer 5: Python-Driven Browser Rendering

### 5.1 Bokeh WebGL (Native Marimo Support)

```python
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show

# Enable WebGL for large datasets
p = figure(
    title="10,000 Particles",
    output_backend="webgl",  # GPU acceleration!
    tools="pan,wheel_zoom,box_zoom,reset"
)

# Generate particles
N = 10000
x = np.random.normal(0, np.pi, N)
y = np.sin(x) + np.random.normal(0, 0.2, N)

# Scatter with status colors
colors = np.random.choice(['#D4AF37', '#1fbdea', '#9D4EDD'], N)
p.scatter(x, y, color=colors, alpha=0.6, size=4)

show(p)
```

**WebGL-Supported Glyphs:**
- circle(), scatter()
- line(), multi_line(), step()
- hbar(), vbar()
- rect(), quad(), block()
- annular_wedge(), annulus(), wedge()
- hex_tile()
- image(), image_rgba(), image_stack()

**NOT Supported:** image_url(), heatmaps (Rect glyph)

### 5.2 p5-widget for Marimo

**Installation:** `pip install p5widget`

```python
import marimo as mo
from p5widget import P5Widget

# p5.js sketch in "instance mode"
sketch = """
let particles = [];

p.setup = function() {
    p.createCanvas(400, 300);
    p.background(10, 10, 11);
    
    for (let i = 0; i < 50; i++) {
        particles.push({
            x: p.random(p.width),
            y: p.random(p.height),
            size: p.random(2, 8),
            color: p.random(['#D4AF37', '#1fbdea', '#9D4EDD']),
            vx: p.random(-0.5, 0.5),
            vy: p.random(-0.5, 0.5)
        });
    }
};

p.draw = function() {
    p.background(10, 10, 11, 20);
    
    for (let particle of particles) {
        p.fill(particle.color);
        p.noStroke();
        p.circle(particle.x, particle.y, particle.size);
        
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        if (particle.x < 0 || particle.x > p.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > p.height) particle.vy *= -1;
    }
};
"""

widget = P5Widget(sketch)
mo.ui.anywidget(widget)
```

### 5.3 PyScript/Pyodide WebGL (Experimental)

**Reference:** [Łukasz Langa - Intro to WebGL with Python](https://www.youtube.com/watch?v=CYAspBOPszg)

PyScript allows Python to call browser WebGL APIs directly:

```python
# This runs IN THE BROWSER via Pyodide
from js import document, window
from pyodide.ffi import create_proxy

# Get WebGL context
canvas = document.getElementById('glcanvas')
gl = canvas.getContext('webgl')

# Set clear color (The Void)
gl.clearColor(0.039, 0.039, 0.043, 1.0)  # #0A0A0B
gl.clear(gl.COLOR_BUFFER_BIT)
```

**PyScript Examples Available:**
- WebGL Icosahedron (three.js)
- Numpy Fractals (canvas)
- D3 Visualization
- New York Taxi Panel (WebGL + Panel)

---

## Layer 6: SVG Animations

### 6.1 CSS-Based SVG Animation

```css
/* Line drawing effect */
.draw-line {
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    animation: draw 2s ease-out forwards;
}

@keyframes draw {
    to { stroke-dashoffset: 0; }
}

/* SVG emerge */
.svg-emerge {
    opacity: 0;
    transform: scale(0.8);
    animation: emerge-svg 0.5s ease-out forwards;
}

@keyframes emerge-svg {
    to {
        opacity: 1;
        transform: scale(1);
    }
}
```

### 6.2 SMIL Animation (Limited Browser Support)

```xml
<svg width="200" height="200">
    <circle cx="100" cy="100" r="50" fill="#D4AF37">
        <!-- Emerge animation -->
        <animate
            attributeName="r"
            from="0"
            to="50"
            dur="0.5s"
            fill="freeze"
        />
        <animate
            attributeName="opacity"
            from="0"
            to="1"
            dur="0.5s"
            fill="freeze"
        />
    </circle>
</svg>
```

**Note:** SMIL is deprecated in some browsers. Prefer CSS or JavaScript animations.

### 6.3 SVG Path Morphing (via JavaScript)

```javascript
// Using Anime.js
animate('.circuit-a', {
    d: morphTo('.circuit-b'),
    duration: 1000,
    ease: 'inOutQuad'
});

// Using GSAP MorphSVG plugin
gsap.to("#shape1", {
    morphSVG: "#shape2",
    duration: 1
});
```

---

## Layer 7: Lottie Animations

### 7.1 Lottie Integration

**CDN:** `https://cdn.jsdelivr.net/npm/bodymovin/build/lottie.js`

```html
<script src="https://cdn.jsdelivr.net/npm/bodymovin/build/lottie.js"></script>

<div id="lottie-container"></div>

<script>
    var animationContainer = document.getElementById('lottie-container');
    var anim = lottie.loadAnimation({
        container: animationContainer,
        renderer: 'svg',  // or 'canvas', 'html'
        loop: true,
        autoplay: true,
        path: 'path/to/animation.json'
    });
</script>
```

### 7.2 Lottie in Marimo via iframe

```python
@app.cell
def _():
    lottie_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/lottie-web@5.12.2/build/player/lottie.min.js"></script>
        <style>
            body { margin: 0; background: #0A0A0B; display: flex; justify-content: center; align-items: center; height: 100vh; }
            #lottie { width: 200px; height: 200px; }
        </style>
    </head>
    <body>
        <div id="lottie"></div>
        <script>
            lottie.loadAnimation({
                container: document.getElementById('lottie'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                // Replace with your Lottie JSON URL
                path: 'https://assets5.lottiefiles.com/packages/lf20_uwR49r.json'
            });
        </script>
    </body>
    </html>
    """
    mo.iframe(lottie_html, width="100%", height="250px")
```

### 7.3 Lottie Sources

- **LottieFiles:** https://lottiefiles.com/ (800,000+ free animations)
- **Lottielab:** https://lottielab.com/ (create your own)
- **After Effects Export:** Via Bodymovin plugin

---

## Accessibility: Reduced Motion

### 8.1 CSS prefers-reduced-motion

```css
/* Default: animations enabled */
.emerge {
    animation: emerge-void 0.3s ease-out forwards;
}

/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
    .emerge {
        animation: none;
        opacity: 1;
        transform: none;
    }
    
    /* Disable ALL animations and transitions */
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

### 8.2 JavaScript Detection

```javascript
// Check user preference
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
    // Skip animations or use instant transitions
    element.style.opacity = 1;
} else {
    // Play full animation
    gsap.from(element, { opacity: 0, duration: 0.5 });
}

// Listen for changes
window.matchMedia('(prefers-reduced-motion: reduce)')
    .addEventListener('change', (e) => {
        if (e.matches) {
            // User enabled reduced motion
        }
    });
```

### 8.3 No-Motion-First Approach

```css
/* Start with no motion (accessible default) */
.box {
    opacity: 1;
    transform: none;
}

/* Only add motion if user hasn't disabled it */
@media (prefers-reduced-motion: no-preference) {
    .box {
        animation: emerge-void 0.3s ease-out;
    }
}
```

---

## Code Snippets Library

### Complete Orchestr8 Animation CSS

```css
/* ======================================
   ORCHESTR8 EMERGENCE ANIMATIONS
   MaestroView.vue Compatible
   ====================================== */

:root {
    --gold-metallic: #D4AF37;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
    --emerge-duration: 0.3s;
    --emerge-easing: ease-out;
}

/* ---- KEYFRAME DEFINITIONS ---- */

@keyframes emerge-void {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes emerge-right {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes emerge-left {
    from { opacity: 0; transform: translateX(-100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes emerge-down {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes emerge-up {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes emerge-pop {
    0% { opacity: 0; transform: scale(0.7); }
    70% { transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}

/* ---- APPLICATION CLASSES ---- */

.emerge-void { animation: emerge-void var(--emerge-duration) var(--emerge-easing) forwards; }
.emerge-right { animation: emerge-right var(--emerge-duration) var(--emerge-easing) forwards; }
.emerge-left { animation: emerge-left var(--emerge-duration) var(--emerge-easing) forwards; }
.emerge-down { animation: emerge-down var(--emerge-duration) var(--emerge-easing) forwards; }
.emerge-up { animation: emerge-up var(--emerge-duration) var(--emerge-easing) forwards; }
.emerge-pop { animation: emerge-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }

/* ---- STAGGER DELAYS ---- */

.emerge-stagger > *:nth-child(1) { animation-delay: 0.00s; opacity: 0; }
.emerge-stagger > *:nth-child(2) { animation-delay: 0.05s; opacity: 0; }
.emerge-stagger > *:nth-child(3) { animation-delay: 0.10s; opacity: 0; }
.emerge-stagger > *:nth-child(4) { animation-delay: 0.15s; opacity: 0; }
.emerge-stagger > *:nth-child(5) { animation-delay: 0.20s; opacity: 0; }
.emerge-stagger > *:nth-child(6) { animation-delay: 0.25s; opacity: 0; }
.emerge-stagger > *:nth-child(7) { animation-delay: 0.30s; opacity: 0; }
.emerge-stagger > *:nth-child(8) { animation-delay: 0.35s; opacity: 0; }
.emerge-stagger > *:nth-child(9) { animation-delay: 0.40s; opacity: 0; }
.emerge-stagger > *:nth-child(10) { animation-delay: 0.45s; opacity: 0; }

/* ---- CELL-SPECIFIC ---- */

[data-cell-name='mermaid_graph'] [data-cell-role='output'] {
    animation: emerge-void 0.4s var(--emerge-easing) forwards;
}

[data-cell-name='fiefdom_list'] [data-cell-role='output'] {
    animation: emerge-void 0.3s var(--emerge-easing) 0.1s forwards;
    opacity: 0;
}

[data-cell-name='tickets_panel'] [data-cell-role='output'] {
    animation: emerge-right 0.3s var(--emerge-easing) forwards;
}

[data-cell-name='agents_panel'] [data-cell-role='output'] {
    animation: emerge-down 0.3s var(--emerge-easing) forwards;
}

/* Overton Anchor - NO ANIMATION */
[data-cell-name='command_bar'] [data-cell-role='output'] {
    animation: none !important;
    opacity: 1 !important;
}

/* ---- ACCESSIBILITY ---- */

@media (prefers-reduced-motion: reduce) {
    .emerge-void, .emerge-right, .emerge-left,
    .emerge-down, .emerge-up, .emerge-pop,
    .emerge-stagger > * {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
    }
}

/* ---- PANEL TRANSITIONS ---- */

.panel-slide-right {
    position: fixed;
    right: 0;
    top: 60px;
    bottom: 80px;
    width: 400px;
    background: var(--bg-elevated);
    border-left: 1px solid var(--gold-metallic);
    animation: emerge-right 0.3s var(--emerge-easing) forwards;
    z-index: 100;
}

.panel-slide-down {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    height: 300px;
    background: var(--bg-elevated);
    border-bottom: 1px solid var(--gold-metallic);
    animation: emerge-down 0.3s var(--emerge-easing) forwards;
    z-index: 100;
}
```

---

## Summary: Recommended Approach for Orchestr8

### Tier 1: Primary (Use These)
1. **Pure CSS Animations** - Custom CSS file with keyframes
2. **Cell-Specific CSS** - Target named cells via `[data-cell-name]`
3. **mo.Html() with inline styles** - For dynamic/conditional animations

### Tier 2: Enhanced (When Needed)
4. **Bokeh WebGL** - For large data visualizations (10k+ points)
5. **GSAP via mo.iframe()** - For complex sequenced animations
6. **Lottie via mo.iframe()** - For pre-made decorative animations

### Tier 3: Advanced (Future Exploration)
7. **p5-widget** - Creative coding, generative art
8. **Three.js via mo.iframe()** - 3D scenes, particle systems
9. **Anime.js** - SVG morphing, complex timelines

### Not Recommended for Orchestr8
- SMIL (deprecated, poor support)
- PyScript WebGL (too experimental)
- pythreejs (Jupyter-focused, untested in Marimo)

---

## EXPANSION: Nicolas Barradeau Collection

### 9.1 FBO Particles (p=621) - GPU Particle Engine

**Source:** [barradeau.com/blog/?p=621](https://barradeau.com/blog/?p=621)

Frame Buffer Object particles - the gold standard for high-performance GPU particle systems.

**Architecture:**
1. **Simulation Pass** - Updates particle positions using Data Texture → writes to RenderTarget
2. **Render Pass** - Uses RenderTarget to display particles on screen

**Why FBO?**
- Millions of particles at 60fps
- All computation happens on GPU
- Position data stored as RGBA texture (x,y,z,w in r,g,b,a)
- Each pixel = one particle's state

**Key Code Pattern:**
```javascript
// FBO requires WebGL extensions
const extensions = [
    'OES_texture_float',
    'OES_texture_float_linear'  // for smooth interpolation
];

// Data texture: each pixel stores particle position
const dataTexture = new THREE.DataTexture(
    positionData,  // Float32Array
    width,         // sqrt of particle count
    height,
    THREE.RGBAFormat,
    THREE.FloatType
);

// Simulation shader reads from texture A, writes to texture B (ping-pong)
const simulationMaterial = new THREE.ShaderMaterial({
    uniforms: {
        positions: { value: dataTextureA },
        time: { value: 0 },
        delta: { value: 0 }
    },
    vertexShader: passThruVert,
    fragmentShader: simulationFrag
});

// Render particles using positions from simulation
const particleMaterial = new THREE.ShaderMaterial({
    uniforms: {
        positions: { value: renderTarget.texture }
    },
    vertexShader: particleVert,
    fragmentShader: particleFrag
});
```

**GitHub Reference:** ES6 port available - search "FBO particles three.js"

**Marimo Integration:** Via mo.iframe only (requires WebGL context)

---

### 9.2 Woven Maps (p=1001) - TARGET: CODE MAP VISUALIZATION

**Source:** [barradeau.com/blog/?p=1001](https://barradeau.com/blog/?p=1001)  
**Demo:** [barradeau.com/2017/wovenmaps](https://www.barradeau.com/2017/wovenmaps/index.html)

**DESIGNATED TARGET FOR "CODE MAP" - Abstract cityscapes representing code metropolis where LLM colleagues live**

**Algorithm Steps:**
1. Collect set of points
2. Delaunay triangulation on the set
3. Compute triangle edge lengths
4. Draw gradient (translate canvas + opacity per height level)
5. Render wireframes at specific intervals
6. Overlay additive color image
7. Render white wireframes with glow

**Core Code - Process Function:**
```javascript
function process(points) {
    // Not enough points: bail out
    if (points.length < 3) return;
    
    // Remove duplicates (create point SET)
    points = cleanup(points);
    
    // Delaunay triangulation
    var tris = delaunay.compute(points);
    
    // Compute edge lengths + store endpoints
    edges = [];
    for (var i = 0; i < tris.length; i += 3) {
        var p0 = points[tris[i]];
        var p1 = points[tris[i+1]];
        var p2 = points[tris[i+2]];
        edges.push(
            [distance(p0, p1), p0, p1],
            [distance(p1, p2), p1, p2],
            [distance(p2, p0), p2, p0]
        );
    }
    render();
}
```

**Core Code - Render Function:**
```javascript
function render() {
    // Reset canvas
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.fillStyle = "#FFF";
    ctx.fillRect(0, 0, w, h);
    
    // Draw gradient (stacked translucent layers)
    ctx.save();
    var max = config.height;
    for (i = 0; i < max; i++) {
        ctx.translate(0, 1);  // Move down 1px each iteration
        ctx.globalAlpha = (1 - i / max) * 0.05;  // Fade out
        renderEdges(edges, i);  // Only draw edges shorter than i
    }
    ctx.restore();
    
    // Render wireframe layers
    if (config.wireframe) {
        var m = config.wireCount;
        for (i = 0; i < m; i++) {
            var t = (i / m);
            ctx.save();
            ctx.translate(0, max * (1 - t));
            ctx.globalAlpha = .05 + .15 * t;
            renderEdges(edges, (i * 10));
            ctx.restore();
        }
    }
    
    // Color overlay (screen blend mode)
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "screen";
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, cw, ch);
    ctx.restore();
    
    // White glow wireframe
    if (config.glow) {
        ctx.globalCompositeOperation = "source-over";
        ctx.strokeStyle = "#FFF";
        ctx.globalAlpha = .2;
        renderEdges(edges, config.glowSize / 2);
        
        // Blur glow
        ctx.globalCompositeOperation = "screen";
        ctx.globalAlpha = 1;
        ctx.filter = "blur(6px)";
        renderEdges(edges, config.glowSize);
    }
}

function renderEdges(edges, min) {
    if (edges.length == 0) return;
    ctx.beginPath();
    
    for (var i = 0; i < edges.length; i++) {
        var edge = edges[i];
        // Only draw if edge length < threshold
        if (edge[0] < min) {
            ctx.moveTo(edge[1].x, edge[1].y);
            ctx.lineTo(edge[2].x, edge[2].y);
        }
    }
    ctx.stroke();
}
```

**ORCHESTR8 CODE MAP APPLICATION:**
- Points = file/function locations in codebase
- Edge density = coupling/dependencies
- Color overlay = file type (gold=working, blue=broken, purple=combat)
- Abstract "city blocks" = modules/packages
- Keep it "fuzzy" like original - not too detailed

**Marimo Integration:** Canvas API works in mo.iframe or could use p5.js

---

### 9.3 WOVEN MAPS CONTROLS - FUTURE DEVELOPMENT SPEC

**Source:** [barradeau.com/2017/wovenmaps](https://www.barradeau.com/2017/wovenmaps/index.html)

**Required Controls to Implement:**
```javascript
// Configuration object structure
const config = {
    height: 200,        // Gradient depth (px)
    wireframe: true,    // Show wireframe overlays
    wireCount: 10,      // Number of wireframe layers
    glow: true,         // Enable white glow effect
    glowSize: 20        // Glow edge threshold
};
```

**UI Controls Specification:**
| Control | Type | Range | Default | Purpose |
|---------|------|-------|---------|---------|
| Height | Slider | 50-500 | 200 | Gradient depth (3D effect intensity) |
| Wireframe | Toggle | on/off | on | Show wireframe overlays |
| Wire Count | Slider | 1-20 | 10 | Number of wireframe layers |
| Glow | Toggle | on/off | on | White glow effect |
| Glow Size | Slider | 5-50 | 20 | Glow edge threshold |
| Color Image | File Input | image | - | Overlay color source |

**Integration with Marimo:**
```python
import marimo as mo

# Control panel
height = mo.ui.slider(50, 500, value=200, label="Height")
wireframe = mo.ui.switch(value=True, label="Wireframe")
wire_count = mo.ui.slider(1, 20, value=10, label="Wire Count")
glow = mo.ui.switch(value=True, label="Glow")
glow_size = mo.ui.slider(5, 50, value=20, label="Glow Size")

# Reactive config
config = {
    "height": height.value,
    "wireframe": wireframe.value,
    "wireCount": wire_count.value,
    "glow": glow.value,
    "glowSize": glow_size.value
}
```

---

### 9.4 Active Contour Model (p=1032) - Morphological Snakes

**Source:** [barradeau.com/blog/?p=1032](https://barradeau.com/blog/?p=1032)

**Algorithm: Morphological Snakes**
- Snake = polyline that expands/shrinks following gradient descent
- Points "roll downhill" toward edges in image
- Self-organizing shape detection

**Process:**
1. Threshold image → binary (black/white)
2. Compute gradient flow fields (forward/backward convolution)
3. Snake points follow flow until reaching minima

**Core Code - Snake Movement:**
```javascript
var scope = this;
this.snake.forEach(function(p) {
    if (p[0] <= 0 || p[0] >= scope.w - 1 || p[1] <= 0 || p[1] >= scope.h - 1) return;
    
    var vx = (.5 - scope.flowX[~~(p[0])][~~(p[1])]) * 2;
    var vy = (.5 - scope.flowY[~~(p[0])][~~(p[1])]) * 2;
    
    p[0] += vx * 100;
    p[1] += vy * 100;
});
```

**Differential Growth (Edge Subdivision):**
```javascript
var tmp = [];
for (var i = 0; i < this.snake.length; i++) {
    var prev = this.snake[(i - 1 < 0 ? this.snake.length - 1 : (i - 1))];
    var cur = this.snake[i];
    var next = this.snake[(i + 1) % this.snake.length];
    
    var dist = distance(prev, cur) + distance(cur, next);
    
    // 1. Destroy edge if too short (don't store)
    if (dist > this.minlen) {
        // 2. Store if within bounds
        if (dist < this.maxlen) {
            tmp.push(cur);
        } else {
            // 3. Subdivide if too long
            var pp = [lerp(.5, prev[0], cur[0]), lerp(.5, prev[1], cur[1])];
            var np = [lerp(.5, cur[0], next[0]), lerp(.5, cur[1], next[1])];
            tmp.push(pp, np);
        }
    }
}
this.snake = tmp;

function lerp(t, a, b) {
    return a + t * (b - a);
}
```

**ORCHESTR8 APPLICATION:**
- Could visualize dependency boundaries
- "Snakes" wrapping around module clusters
- Organic growth animations for code structure

---

### 9.5 Random Points in 3D Mesh (p=1058)

**Source:** [barradeau.com/blog/?p=1058](https://barradeau.com/blog/?p=1058)

**Problem:** Distribute random 3D points uniformly within an arbitrary mesh volume

**Key Insight:** Mesh triangles have different areas - need weighted random selection to avoid clustering on small triangles

**Algorithm:**
1. Calculate area of each triangle in mesh
2. Build cumulative distribution function (CDF)
3. Random selection weighted by area
4. Random point within selected triangle (barycentric coords)

**Marimo Application:** Could populate particles inside custom 3D shapes

---

## EXPANSION: Mathematical Landscapes for Morphing

### 10.1 landscapes Library (Python)

**Source:** [github.com/nathanrooy/landscapes](https://github.com/nathanrooy/landscapes)  
**Install:** `pip install landscapes`

**Dependency-free pure Python optimization test functions - PERFECT FOR MORPHING**

**Available Functions (50+):**
| Function | Dimensions | Visual Character |
|----------|------------|------------------|
| `rastrigin()` | n | Wavy egg-crate pattern |
| `ackley()` | 2 | Deep well with ripples |
| `rosenbrock()` | n | Curved valley (banana) |
| `sphere()` | n | Simple bowl |
| `eggholder()` | 2 | Complex multi-modal |
| `himmelblau()` | 2 | Four local minima |
| `schwefel()` | n | Deceptive deep valleys |
| `griewank()` | n | Many local optima |
| `styblinski_tang()` | n | Asymmetric valleys |
| `holder_table()` | 2 | Four deep corners |
| `cross_in_tray()` | 2 | Cross pattern |
| `drop_wave()` | 2 | Concentric ripples |

**Usage:**
```python
from landscapes.single_objective import rastrigin, ackley, rosenbrock
import numpy as np

# Generate surface for visualization
x = np.linspace(-5.12, 5.12, 100)
y = np.linspace(-5.12, 5.12, 100)
X, Y = np.meshgrid(x, y)

# Evaluate function at each point
Z_rastrigin = np.array([[rastrigin([xi, yi]) for xi, yi in zip(row_x, row_y)] 
                         for row_x, row_y in zip(X, Y)])

Z_ackley = np.array([[ackley([xi, yi]) for xi, yi in zip(row_x, row_y)] 
                      for row_x, row_y in zip(X, Y)])
```

**ORCHESTR8 MORPHING CONCEPT:**
1. Start with simple `sphere()` surface
2. Morph to `rastrigin()` (complexity emerging)
3. Transition through `ackley()` (focus/goal)
4. Land on `rosenbrock()` (optimization path)

**Visualization in Marimo:**
```python
import plotly.graph_objects as go
from landscapes.single_objective import rastrigin
import numpy as np

x = np.linspace(-5.12, 5.12, 50)
y = np.linspace(-5.12, 5.12, 50)
X, Y = np.meshgrid(x, y)
Z = np.array([[rastrigin([xi, yi]) for xi, yi in zip(row_x, row_y)] 
               for row_x, row_y in zip(X, Y)])

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
fig.update_layout(
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        bgcolor='#0A0A0B'
    ),
    paper_bgcolor='#0A0A0B',
    margin=dict(l=0, r=0, t=0, b=0)
)
fig
```

---

### 10.2 spatial-analysis (Python)

**Source:** [github.com/nathanrooy/spatial-analysis](https://github.com/nathanrooy/spatial-analysis)  
**Install:** `pip install git+https://github.com/nathanrooy/spatial-analysis`

**Precise geospatial distance calculations:**
- `haversine()` - Great-circle distance
- `vincenty_inverse()` - Ellipsoid distance (more accurate)

**Could be used for:** Mapping code elements to geographic metaphor

---

## EXPANSION: Cesium Particle System

### 11.1 cesium-particle (Wind Field GPU Particles)

**Source:** [github.com/hongfaqiu/cesium-particle](https://github.com/hongfaqiu/cesium-particle)  
**Install:** `npm install cesium-particle`

**GPU-accelerated particle system for geospatial visualization**

**Key Configuration:**
```javascript
const systemOptions = {
    maxParticles: 64 * 64,      // Will be squared
    particleHeight: 1000.0,     // Altitude
    fadeOpacity: 0.996,         // Trail fade
    dropRate: 0.003,            // Particle reset rate
    dropRateBump: 0.01,         // Speed-based reset increase
    speedFactor: 1.0,           // Velocity multiplier
    lineWidth: 4.0,             // Particle stroke width
    dynamic: true               // Enable animation
};

// Color gradient based on speed or height
const colorTable = [
    [0.015686, 0.054902, 0.847059],  // Low values
    [0.125490, 0.313725, 1.000000]   // High values
];

const particleObj = new Particle3D(viewer, {
    input: ncFile,
    fields: { U: 'water_u', V: 'water_v' },
    userInput: systemOptions,
    colorTable: colorTable,
    colour: 'speed'  // or 'height'
});

await particleObj.init();
particleObj.show();
```

**Vortex Model (Procedural):**
```javascript
// Create vortex without data file
const parameter = [
    [120, 30, 100],  // [lon, lat, lev] center
    5,               // radiusX
    5,               // radiusY
    2000,            // height
    0.1,             // dx resolution
    0.1,             // dy resolution
    2000             // dz resolution
];
const vortexData = new Vortex(...parameter).getData();
```

**ORCHESTR8 APPLICATION:**
- Flow visualization for data pipelines
- Wind/current metaphor for task dependencies
- GPU-accelerated for large particle counts

---

## EXPANSION: Audio-Reactive Details

### 12.1 Enhanced Audio Analysis

**Source:** [Codrops Tutorial](https://tympanus.net/codrops/2023/12/19/creating-audio-reactive-visuals-with-dynamic-particles-in-three-js/)

**Frequency Band Separation:**
```javascript
// Define frequency boundaries
this.lowFrequency = 10;     // Bass starts here
this.midFrequency = 200;    // Mids start here
this.highFrequency = 2000;  // Highs start here

// Calculate range indices
const bufferLength = this.audioAnalyser.frequencyBinCount;
const sampleRate = this.audioContext.sampleRate;

const lowStart = Math.floor((this.lowFrequency * bufferLength) / sampleRate);
const lowEnd = Math.floor((this.midFrequency * bufferLength) / sampleRate);
const midEnd = Math.floor((this.highFrequency * bufferLength) / sampleRate);

// Get normalized averages (0-1)
const frequencyData = this.audioAnalyser.getFrequencyData();
const lowAvg = this.normalizeValue(this.calculateAverage(frequencyData, lowStart, lowEnd));
const midAvg = this.normalizeValue(this.calculateAverage(frequencyData, lowEnd, midEnd));
const highAvg = this.normalizeValue(this.calculateAverage(frequencyData, midEnd, bufferLength));
```

**BPM Detection (web-audio-beat-detector):**
```javascript
import { guess } from 'web-audio-beat-detector';

// Detect BPM from audio buffer
const { bpm } = await guess(audioBuffer);

// Convert to interval (ms between beats)
this.interval = 60000 / bpm;

// Dispatch beat events
this.intervalId = setInterval(() => {
    this.dispatchEvent({ type: 'beat' });
}, this.interval);
```

**Applying to Visuals:**
```javascript
update() {
    // High frequencies → amplitude (particle spread)
    this.material.uniforms.amplitude.value = 
        0.8 + THREE.MathUtils.mapLinear(
            App.audioManager.frequencyData.high, 
            0, 0.6, -0.1, 0.2
        );
    
    // Mid frequencies → offset gain
    this.material.uniforms.offsetGain.value = 
        App.audioManager.frequencyData.mid * 0.6;
    
    // Low frequencies → time progression
    const t = THREE.MathUtils.mapLinear(
        App.audioManager.frequencyData.low, 
        0.6, 1, 0.2, 0.5
    );
    this.time += THREE.MathUtils.clamp(t, 0.2, 0.5);
    this.material.uniforms.time.value = this.time;
}
```

**Curl Noise Integration (Vertex Shader):**
```glsl
// Organic particle movement
vec3 newpos = position;
vec3 target = position 
    + (normal * 0.1) 
    + curl(
        newpos.x * frequency, 
        newpos.y * frequency, 
        newpos.z * frequency
      ) * amplitude;

float d = length(newpos - target) / maxDistance;
newpos = mix(position, target, pow(d, 4.0));

// Wave motion on z-axis
newpos.z += sin(time) * (0.1 * offsetGain);

// Size varies with distance and depth
gl_PointSize = size + (pow(d, 3.0) * offsetSize) * (1.0 / -mvPosition.z);
```

---

## Updated Compatibility Matrix

| Technique | Marimo Compatible | Integration Method | Performance | Complexity |
|-----------|-------------------|-------------------|-------------|------------|
| **Pure CSS Keyframes** | ✅ Full | Custom CSS file | Excellent | Low |
| **CSS Transitions** | ✅ Full | .style() or mo.Html | Excellent | Low |
| **GSAP** | ✅ Via mo.iframe | iframe | Excellent | Medium |
| **Anime.js** | ✅ Via mo.iframe | iframe | Excellent | Medium |
| **Lottie** | ✅ Via mo.iframe | iframe | Excellent | Low |
| **FBO Particles** | ⚠️ Via mo.iframe | iframe + WebGL | GPU-accelerated | High |
| **Woven Maps (Canvas)** | ✅ Via mo.iframe | Canvas 2D | Good | Medium |
| **Three.js/WebGL** | ⚠️ Via mo.iframe | iframe | GPU-accelerated | High |
| **p5.js** | ✅ Via p5-widget | anywidget | Good | Medium |
| **Bokeh WebGL** | ✅ Native | output_backend="webgl" | GPU-accelerated | Low |
| **landscapes (Python)** | ✅ Native | Plotly/Matplotlib | Good | Low |
| **Active Contour/Snakes** | ✅ Via mo.iframe | Canvas 2D | Good | Medium |
| **Audio-Reactive** | ⚠️ Via mo.iframe | iframe + Web Audio | GPU-accelerated | High |
| **cesium-particle** | ⚠️ Complex | Cesium.js iframe | GPU-accelerated | Very High |

---

**END CATALOG**

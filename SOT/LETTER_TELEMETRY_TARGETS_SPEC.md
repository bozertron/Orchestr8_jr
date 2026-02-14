# Letter Telemetry Targets Spec

**Concept:** Letters as particle targets - text that emerges from cursor and attracts particles
**Created:** 2026-02-13
**Status:** DRAFT - Ready for prototyping
**Author:** Founder + Claude

---

## 1. The Vision

### 1.1 Core Concept

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   THE VOID                                                  │
│                                                             │
│                    ╭──────────────╮                         │
│            ───────►│   BUILDING   │◄──── particles          │
│           ✨       │     NAME     │     flowing to target   │
│          ✨ ✨     ╰──────────────╯                          │
│         ✨   ✨           ▲                                   │
│        ✨     ✨          │                                   │
│       ✨       ✨    cursor position                         │
│      ✨    ✨    ✨      when letter                          │
│     ✨  ✨        ✨    emerges                                │
│                                                             │
│   Particle streams create visible pathways to text targets  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Key Behaviors

| Behavior | Description |
|----------|-------------|
| **Cursor Emergence** | Letters morph out from cursor position |
| **Thick Readable** | Chunky text like Claude Code's UI font |
| **Particle Attraction** | Particles flow toward letter outlines |
| **Pathway Creation** | Streams show visual "telemetry" paths |
| **Solid + Emergent** | Text is readable but has emergence animation |

---

## 2. Technical Architecture

### 2.1 Layer Stack

```
┌─────────────────────────────────────────┐
│  CURSOR TRACKER                         │  ← Mouse position
├─────────────────────────────────────────┤
│  TEXT EMERGER                           │  ← Letters morph from cursor
├─────────────────────────────────────────┤
│  PARTICLE ENGINE                        │  ← FBO or Canvas 2D
├─────────────────────────────────────────┤
│  ATTRACTION FIELD                       │  ← Letter outlines as targets
├─────────────────────────────────────────┤
│  RENDERER                               │  ← WebGL or Canvas
└─────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

#### Cursor Tracker
```javascript
// Track cursor position for emergence origin
const cursor = { x: 0, y: 0 };
document.addEventListener('mousemove', (e) => {
    cursor.x = e.clientX;
    cursor.y = e.clientY;
});
```

#### Text Emerger
```javascript
// Letter emergence from cursor
class TextEmerger {
    constructor(text, originX, originY) {
        this.text = text;
        this.origin = { x: originX, y: originY };
        this.letters = [];
        this.emergeLetter(0); // Start emergence cascade
    }
    
    emergeLetter(index) {
        if (index >= this.text.length) return;
        
        const letter = {
            char: this.text[index],
            // Start at cursor, animate to final position
            x: this.origin.x,
            y: this.origin.y,
            targetX: this.origin.x + (index * LETTER_WIDTH),
            targetY: this.origin.y,
            scale: 0,
            opacity: 0,
            emergeProgress: 0
        };
        
        this.letters.push(letter);
        this.animateEmergence(letter, () => {
            // Cascade to next letter
            setTimeout(() => this.emergeLetter(index + 1), 50);
        });
    }
    
    animateEmergence(letter, onComplete) {
        // Morph from cursor: scale 0→1, opacity 0→1, position cursor→target
        gsap.to(letter, {
            x: letter.targetX,
            y: letter.targetY,
            scale: 1,
            opacity: 1,
            duration: 0.4,
            ease: "back.out(1.7)",
            onComplete
        });
    }
}
```

#### Attraction Field
```javascript
// Convert letter outlines to particle targets
class AttractionField {
    constructor() {
        this.targets = []; // Points that attract particles
    }
    
    addTextTarget(text, x, y, fontSize, fontFamily) {
        // Render text to offscreen canvas
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        ctx.font = `${fontSize}px ${fontFamily}`;
        ctx.fillText(text, 0, fontSize);
        
        // Sample outline points
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const outline = this.extractOutline(imageData);
        
        // Add each outline point as attraction target
        for (const point of outline) {
            this.targets.push({
                x: x + point.x,
                y: y + point.y,
                strength: 1.0,
                type: 'outline'
            });
        }
    }
    
    extractOutline(imageData) {
        // Edge detection on text pixels
        const points = [];
        const data = imageData.data;
        const w = imageData.width;
        const h = imageData.height;
        
        for (let y = 1; y < h - 1; y++) {
            for (let x = 1; x < w - 1; x++) {
                const i = (y * w + x) * 4;
                const alpha = data[i + 3];
                
                // If pixel has alpha and neighbor doesn't = outline
                if (alpha > 128) {
                    const neighbors = [
                        data[((y-1) * w + x) * 4 + 3],
                        data[((y+1) * w + x) * 4 + 3],
                        data[(y * w + x-1) * 4 + 3],
                        data[(y * w + x+1) * 4 + 3]
                    ];
                    
                    const hasEmptyNeighbor = neighbors.some(n => n < 128);
                    if (hasEmptyNeighbor) {
                        points.push({ x, y });
                    }
                }
            }
        }
        
        return this.decimate(points, SAMPLE_RATE); // Reduce point count
    }
    
    getAttraction(particleX, particleY) {
        // Sum attraction vectors from all targets
        let fx = 0, fy = 0;
        
        for (const target of this.targets) {
            const dx = target.x - particleX;
            const dy = target.y - particleY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < ATTRACTION_RADIUS && dist > 0) {
                const force = target.strength / (dist * dist);
                fx += (dx / dist) * force;
                fy += (dy / dist) * force;
            }
        }
        
        return { fx, fy };
    }
}
```

#### Particle Engine
```javascript
// Particles that flow toward text targets
class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.life = 1.0;
        this.color = ORCHESTR8_COLORS.gold;
    }
    
    update(attractionField) {
        // Get attraction toward nearest text outline
        const { fx, fy } = attractionField.getAttraction(this.x, this.y);
        
        // Apply attraction force
        this.vx += fx * ATTRACTION_STRENGTH;
        this.vy += fy * ATTRACTION_STRENGTH;
        
        // Apply velocity with damping
        this.x += this.vx;
        this.y += this.vy;
        this.vx *= 0.98;
        this.vy *= 0.98;
        
        // Fade out over time
        this.life -= 0.002;
    }
}
```

---

## 3. Visual Design

### 3.1 Typography

**Reference:** Claude Code's thick, readable UI text

```css
.letter-target {
    font-family: 'Orchestr8 HardCompn', 'Cal Sans', sans-serif;
    font-weight: 600;
    font-size: 32px;
    letter-spacing: 0.05em;
    
    /* Thick, solid appearance */
    -webkit-text-stroke: 1px rgba(212, 175, 55, 0.3);
    paint-order: stroke fill;
    
    /* Emergence animation */
    animation: letter-emerge 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes letter-emerge {
    0% {
        opacity: 0;
        transform: scale(0.5) translateY(10px);
        filter: blur(4px);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
        filter: blur(0);
    }
}
```

### 3.2 Color System (Canonical)

| State | Color | Usage |
|-------|-------|-------|
| **Working** | `#D4AF37` | Default letter/particle color |
| **Broken** | `#1fbdea` | Error state letters |
| **Combat** | `#9D4EDD` | Active agent targets |
| **Void** | `#0A0A0B` | Background |

### 3.3 Particle Appearance

```javascript
const PARTICLE_CONFIG = {
    size: { min: 2, max: 6 },
    speed: { min: 0.5, max: 2.0 },
    lifetime: { min: 2000, max: 5000 },  // ms
    emissionRate: 50,  // particles per second per target
    attractionRadius: 200,  // pixels
    attractionStrength: 0.1,
    trail: {
        enabled: true,
        length: 20,
        opacity: 0.3
    }
};
```

---

## 4. Interaction Patterns

### 4.1 Cursor-Triggered Emergence

```
CURSOR MOVES TO LOCATION
        │
        ▼
USER PRESSES KEY / CLICKS
        │
        ▼
TEXT EMERGES FROM CURSOR
        │
        ├──► Letter 1 morphs out (0ms)
        ├──► Letter 2 morphs out (50ms)
        ├──► Letter 3 morphs out (100ms)
        └──► ... cascade complete
        │
        ▼
ATTRACTION FIELD ACTIVATES
        │
        ▼
PARTICLES BEGIN FLOW
```

### 4.2 Particle Behaviors

| Behavior | Trigger | Visual |
|----------|---------|--------|
| **Attract** | Particle within radius | Curved path toward letter |
| **Orbit** | Particle very close | Circular motion around outline |
| **Dissolve** | Particle reaches outline | Fade into letter color |
| **Stream** | Continuous emission | Visible pathway/telemetry |

### 4.3 User Interactions

```javascript
const INTERACTIONS = {
    // Hover over letter → particles intensify
    hover: {
        particleRate: 2.0,  // 2x emission
        glowIntensity: 1.5
    },
    
    // Click letter → burst effect
    click: {
        burstCount: 50,
        burstRadius: 100,
        burstSpeed: 5.0
    },
    
    // Drag letter → particles follow
    drag: {
        trailEnabled: true,
        trailLength: 50
    }
};
```

---

## 5. Integration with Orchestr8

### 5.1 Code City Application

```
┌─────────────────────────────────────────────────────────────┐
│  CODE CITY                                                  │
│                                                             │
│     ╭──────────╮                                            │
│     │ main.py  │ ← Building label as target                │
│     ╰──────────╯                                            │
│         ▲                                                    │
│         │ particles showing import flow                     │
│         │                                                    │
│     ╭──────────╮     ╭──────────╮                          │
│     │ utils.py │◄────│ config.py│                          │
│     ╰──────────╯     ╰──────────╯                          │
│                                                             │
│  Labels = Particle targets                                  │
│  Particles = Data flow visualization                        │
│  Pathways = Import relationships                            │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Use Cases in Orchestr8

| Use Case | Text Target | Particle Meaning |
|----------|-------------|------------------|
| **Building Labels** | File names | Import flow |
| **Status Indicators** | "BROKEN" / "WORKING" | Error particles |
| **Agent Status** | "DIRECTOR" / "PROFESSOR" | Activity level |
| **Notifications** | Alert messages | Attention stream |
| **Search Results** | Matching files | Relevance flow |

### 5.3 Integration Points

```python
# In IP/plugins/06_maestro.py

def create_letter_target(text: str, x: int, y: int, status: str = "working"):
    """Create a letter telemetry target in Code City."""
    
    color = {
        "working": "#D4AF37",
        "broken": "#1fbdea", 
        "combat": "#9D4EDD"
    }[status]
    
    return mo.Html(f"""
    <div class="letter-target" 
         style="left: {x}px; top: {y}px; color: {color};"
         data-text="{text}"
         data-status="{status}">
        {text}
    </div>
    <canvas class="particle-layer" 
            style="position: absolute; left: 0; top: 0; pointer-events: none;">
    </canvas>
    """)
```

---

## 6. Implementation Phases

### Phase 1: Core Emergence (Week 1)

**Goal:** Letters emerge from cursor position

- [ ] Cursor position tracker
- [ ] Single letter emergence animation
- [ ] Multi-letter cascade
- [ ] CSS emergence keyframes

**Deliverable:** Click anywhere → text emerges from cursor

### Phase 2: Attraction Field (Week 2)

**Goal:** Particles attracted to letter outlines

- [ ] Text-to-outline extraction
- [ ] Attraction force calculation
- [ ] Basic particle engine (Canvas 2D)
- [ ] Particle-to-target flow

**Deliverable:** Particles flow toward emerged letters

### Phase 3: Visual Polish (Week 3)

**Goal:** Production-quality appearance

- [ ] Particle trails
- [ ] Glow effects on letters
- [ ] Smooth emergence curves
- [ ] Color transitions by state

**Deliverable:** Visually polished demo

### Phase 4: Orchestr8 Integration (Week 4)

**Goal:** Working in Code City

- [ ] Building label targets
- [ ] Import flow particles
- [ ] Status-based coloring
- [ ] Performance optimization

**Deliverable:** Integrated feature in main app

---

## 7. Technical Options

### 7.1 Rendering Backend

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **Canvas 2D** | Simple, no WebGL | Limited particles | Phase 1-2 |
| **WebGL** | High performance | Complex setup | Phase 3+ |
| **FBO Particles** | Millions of particles | Very complex | Future |

### 7.2 Animation Library

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **CSS Only** | No dependencies | Limited control | Emergence |
| **GSAP** | Powerful, reliable | 45KB | Recommended |
| **Anime.js** | SVG morphing | Smaller ecosystem | Alternative |
| **Custom** | Full control | More work | If needed |

### 7.3 Text Rendering

| Option | Description | Use Case |
|--------|-------------|----------|
| **DOM + CSS** | Standard HTML text | Simple labels |
| **Canvas fillText** | Drawn to canvas | Integrated with particles |
| **SVG Text** | Vector, scalable | High-quality rendering |
| **Signed Distance Fields** | GPU-friendly | WebGL path |

---

## 8. Code Templates

### 8.1 Minimal Prototype

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #0A0A0B;
            overflow: hidden;
            font-family: 'Courier New', monospace;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
        }
        .letter {
            position: absolute;
            color: #D4AF37;
            font-size: 32px;
            font-weight: bold;
            pointer-events: none;
            opacity: 0;
            transform: scale(0.5);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .letter.visible {
            opacity: 1;
            transform: scale(1);
        }
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    <div id="letters"></div>
    
    <script>
        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        const lettersDiv = document.getElementById('letters');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // State
        const cursor = { x: 0, y: 0 };
        const particles = [];
        const targets = [];
        
        // Track cursor
        document.addEventListener('mousemove', (e) => {
            cursor.x = e.clientX;
            cursor.y = e.clientY;
        });
        
        // Click to create letter target
        document.addEventListener('click', () => {
            emergeText('TARGET', cursor.x, cursor.y);
        });
        
        // Emergence animation
        function emergeText(text, x, y) {
            const letters = text.split('');
            
            letters.forEach((char, i) => {
                setTimeout(() => {
                    const letter = document.createElement('div');
                    letter.className = 'letter';
                    letter.textContent = char;
                    letter.style.left = x + 'px';
                    letter.style.top = y + 'px';
                    lettersDiv.appendChild(letter);
                    
                    // Trigger emergence
                    requestAnimationFrame(() => {
                        letter.classList.add('visible');
                        letter.style.left = (x + i * 24) + 'px';
                    });
                    
                    // Add outline points as targets
                    setTimeout(() => {
                        const rect = letter.getBoundingClientRect();
                        addOutlineTargets(rect);
                    }, 400);
                    
                }, i * 50);
            });
        }
        
        // Add letter outline as particle targets
        function addOutlineTargets(rect) {
            const step = 4;
            for (let x = rect.left; x < rect.right; x += step) {
                targets.push({ x, y: rect.top, type: 'top' });
                targets.push({ x, y: rect.bottom, type: 'bottom' });
            }
            for (let y = rect.top; y < rect.bottom; y += step) {
                targets.push({ x: rect.left, y, type: 'left' });
                targets.push({ x: rect.right, y, type: 'right' });
            }
        }
        
        // Spawn particles
        function spawnParticle() {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: 0,
                vy: 0,
                life: 1.0
            });
        }
        
        // Animation loop
        function animate() {
            ctx.fillStyle = 'rgba(10, 10, 11, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Spawn new particles
            if (targets.length > 0 && Math.random() < 0.3) {
                spawnParticle();
            }
            
            // Update and draw particles
            ctx.fillStyle = '#D4AF37';
            
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                
                // Attract toward targets
                for (const t of targets) {
                    const dx = t.x - p.x;
                    const dy = t.y - p.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < 200 && dist > 0) {
                        const force = 0.5 / dist;
                        p.vx += dx * force;
                        p.vy += dy * force;
                    }
                }
                
                // Apply velocity
                p.x += p.vx * 0.1;
                p.y += p.vy * 0.1;
                p.vx *= 0.99;
                p.vy *= 0.99;
                p.life -= 0.001;
                
                // Draw
                if (p.life > 0) {
                    ctx.globalAlpha = p.life;
                    ctx.fillRect(p.x, p.y, 3, 3);
                } else {
                    particles.splice(i, 1);
                }
            }
            
            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }
        
        animate();
    </script>
</body>
</html>
```

### 8.2 Orchestr8 Integration Template

```python
# IP/components/letter_telemetry.py

import marimo as mo
from typing import Optional
from dataclasses import dataclass

@dataclass
class LetterTarget:
    text: str
    x: int
    y: int
    status: str = "working"  # working, broken, combat
    
    @property
    def color(self) -> str:
        return {
            "working": "#D4AF37",
            "broken": "#1fbdea",
            "combat": "#9D4EDD"
        }[self.status]


def render_letter_telemetry(targets: list[LetterTarget]) -> mo.Html:
    """Render letter targets with particle telemetry."""
    
    targets_json = [
        {"text": t.text, "x": t.x, "y": t.y, "color": t.color}
        for t in targets
    ]
    
    return mo.Html(f"""
    <div class="letter-telemetry-container" style="position: relative;">
        <canvas id="telemetry-particles" 
                style="position: absolute; top: 0; left: 0; pointer-events: none;">
        </canvas>
        <div id="telemetry-targets"></div>
    </div>
    
    <script>
    (function() {{
        const targets = {targets_json};
        const canvas = document.getElementById('telemetry-particles');
        const ctx = canvas.getContext('2d');
        const container = document.querySelector('.letter-telemetry-container');
        const targetsDiv = document.getElementById('telemetry-targets');
        
        // Initialize
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
        
        // Create letter elements
        targets.forEach((t, i) => {{
            const el = document.createElement('div');
            el.className = 'telemetry-letter';
            el.style.cssText = `
                position: absolute;
                left: ${{t.x}}px;
                top: ${{t.y}}px;
                color: ${{t.color}};
                font-family: 'Orchestr8 HardCompn', sans-serif;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.05em;
                opacity: 0;
                transform: scale(0.5) translateY(10px);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            `;
            el.textContent = t.text;
            targetsDiv.appendChild(el);
            
            // Trigger emergence with cascade
            setTimeout(() => {{
                el.style.opacity = '1';
                el.style.transform = 'scale(1) translateY(0)';
            }}, i * 100);
        }});
        
        // Particle system
        const particles = [];
        const outlineTargets = [];
        
        // Extract outlines after emergence
        setTimeout(() => {{
            document.querySelectorAll('.telemetry-letter').forEach(el => {{
                const rect = el.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                
                // Add outline points
                for (let x = 0; x < rect.width; x += 4) {{
                    outlineTargets.push({{
                        x: rect.left - containerRect.left + x,
                        y: rect.top - containerRect.top
                    }});
                    outlineTargets.push({{
                        x: rect.left - containerRect.left + x,
                        y: rect.bottom - containerRect.top
                    }});
                }}
            }});
        }}, 500);
        
        // Animation loop
        function animate() {{
            ctx.fillStyle = 'rgba(10, 10, 11, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Spawn particles toward targets
            if (outlineTargets.length > 0 && Math.random() < 0.2) {{
                particles.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: 0, vy: 0, life: 1.0
                }});
            }}
            
            ctx.fillStyle = '#D4AF37';
            
            for (let i = particles.length - 1; i >= 0; i--) {{
                const p = particles[i];
                
                // Attract to nearest target
                let nearestDist = Infinity;
                let nearestTarget = null;
                
                for (const t of outlineTargets) {{
                    const dx = t.x - p.x;
                    const dy = t.y - p.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < nearestDist) {{
                        nearestDist = dist;
                        nearestTarget = t;
                    }}
                }}
                
                if (nearestTarget && nearestDist > 5) {{
                    const dx = nearestTarget.x - p.x;
                    const dy = nearestTarget.y - p.y;
                    const force = 2 / Math.max(nearestDist, 10);
                    p.vx += dx * force;
                    p.vy += dy * force;
                }}
                
                p.x += p.vx * 0.05;
                p.y += p.vy * 0.05;
                p.vx *= 0.98;
                p.vy *= 0.98;
                p.life -= 0.002;
                
                if (p.life > 0) {{
                    ctx.globalAlpha = p.life * 0.7;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
                    ctx.fill();
                }} else {{
                    particles.splice(i, 1);
                }}
            }}
            
            requestAnimationFrame(animate);
        }}
        
        animate();
    }})();
    </script>
    """)
```

---

## 9. Success Criteria

### Phase 1 Complete When:
- [ ] Click produces letter emergence from cursor
- [ ] Multi-letter cascade animation works
- [ ] Emergence timing matches canon (400ms, cubic-bezier)

### Phase 2 Complete When:
- [ ] Particles attracted to letter outlines
- [ ] Visible particle streams toward targets
- [ ] Performance stable at 60fps with 500 particles

### Phase 3 Complete When:
- [ ] Particle trails visible
- [ ] Letters have subtle glow
- [ ] Color transitions by status

### Phase 4 Complete When:
- [ ] Integrated in Code City
- [ ] Building labels as targets
- [ ] Import flow visualization works

---

## 10. References

### 10.1 Internal
- `one integration at a time/docs/EMERGENCE_ANIMATION_CATALOG.md` - Full technique catalog
- `IP/styles/orchestr8.css` - Canonical emergence animations
- `IP/woven_maps.py` - Existing particle system

### 10.2 External
- [particles.js](https://github.com/VincentGarreau/particles.js/) - Particle library
- [Barradeau FBO Particles](https://barradeau.com/blog/?p=621) - GPU particles
- [Anime.js SVG Morphing](https://animejs.com/) - Text morphing
- [GSAP Text Plugin](https://greensock.com/docs/v3/Plugins/TextPlugin) - Text animation

### 10.3 Related Concepts
- **Active Contour Model** - Snakes wrapping around shapes (Section 9.4 of catalog)
- **Curl Noise** - Organic particle movement
- **Signed Distance Fields** - GPU text rendering

---

**END SPEC**

**Status:** ✅ READY FOR PROTOTYPING
**Next Step:** Create minimal prototype (Section 8.1)

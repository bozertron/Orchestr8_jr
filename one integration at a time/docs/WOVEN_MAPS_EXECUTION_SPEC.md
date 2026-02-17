# WOVEN MAPS CODE CITY: COMPLETE EXECUTION SPECIFICATION

**Document Version:** 1.0.0
**Created:** 2026-01-26
**Purpose:** Enable ANY Claude instance to implement the Code City visualization without prior context
**Status:** READY FOR EXECUTION

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Project Context](#2-project-context)
3. [The Vision](#3-the-vision)
4. [Technical Architecture](#4-technical-architecture)
5. [Woven Maps Algorithm](#5-woven-maps-algorithm-complete)
6. [Marimo Integration](#6-marimo-integration)
7. [Complete Implementation Code](#7-complete-implementation-code)
8. [Data Structures](#8-data-structures)
9. [Color System](#9-color-system)
10. [Animation Specifications](#10-animation-specifications)
11. [Testing Procedures](#11-testing-procedures)
12. [Three.js Graduation Path](#12-threejs-graduation-path)
13. [Troubleshooting Guide](#13-troubleshooting-guide)
14. [File Locations Reference](#14-file-locations-reference)

---

## 1. EXECUTIVE SUMMARY

### What We're Building

A "Code City" visualization that displays a codebase as an abstract cityscape. Files become buildings, directories become neighborhoods, and code health is shown through color:

- **Gold (#D4AF37)**: Working code - all imports resolve, no errors
- **Blue (#1fbdea)**: Broken code - has errors, needs attention
- **Purple (#9D4EDD)**: Combat - LLM "General" is actively debugging

### Why Woven Maps

Nicolas Barradeau's "Woven Maps" algorithm creates beautiful abstract cityscapes using Delaunay triangulation. It's:

- **Lightweight**: Canvas 2D, no WebGL required
- **Fast**: Can render 1000+ points at 60fps
- **Beautiful**: Creates organic, architectural forms
- **Perfect for Marimo**: Works in iframe or direct HTML injection

### The Immediate Goal

Implement Woven Maps in `IP/plugins/06_maestro.py` (The Void plugin) so that when the user opens Orchestr8, they see their codebase as a living, breathing city.

---

## 2. PROJECT CONTEXT

### What is Orchestr8?

Orchestr8 is a developer tool that enables a human "Emperor" to coordinate multiple Claude Code instances ("Generals") across a complex codebase. It is NOT part of stereOS - it's the tool used to BUILD stereOS.

### The Application Stack

```
┌─────────────────────────────────────────┐
│           Marimo Runtime                │  ← Reactive Python notebook
├─────────────────────────────────────────┤
│         IP/orchestr8_app.py             │  ← Main application entry
├─────────────────────────────────────────┤
│           Plugin System                 │  ← Dynamic plugin loading
│  ┌─────────────────────────────────┐    │
│  │ 00_welcome.py                   │    │
│  │ 01_generator.py                 │    │
│  │ 02_explorer.py                  │    │
│  │ 03_gatekeeper.py                │    │
│  │ 04_connie_ui.py                 │    │
│  │ 05_universal_bridge.py          │    │
│  │ 06_maestro.py  ← THE VOID       │    │  ← THIS IS WHERE WE IMPLEMENT
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│         STATE_MANAGERS                  │  ← Reactive state injection
│  {                                      │
│    "root": (get_root, set_root),        │
│    "files": (get_files, set_files),     │
│    "selected": (get_selected, ...),     │
│    "logs": (get_logs, set_logs)         │
│  }                                      │
└─────────────────────────────────────────┘
```

### Plugin Protocol

Every plugin MUST have:

```python
PLUGIN_NAME = "Display Name"  # Shown in tab
PLUGIN_ORDER = 6              # Lower = appears first

def render(STATE_MANAGERS: dict) -> Any:
    """Return mo.Html, mo.md, or mo.vstack layout"""
    get_root, set_root = STATE_MANAGERS["root"]
    # ... build UI ...
    return mo.vstack([...])
```

### Current State of 06_maestro.py

The plugin currently has:

- ✅ Correct color constants (including PURPLE_COMBAT)
- ✅ Control surface with buttons
- ✅ Chat-style void (messages emerge)
- ❌ NO graph visualization
- ❌ NO Woven Maps implementation
- ❌ NO codebase topology display

---

## 3. THE VISION

### UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ TOP ROW (z-index: 50)                                           │
│ [stereOS]              [Collabor8] [JFDI] [Summon]              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                        THE VOID                                 │
│                                                                 │
│    ┌─────────────────────────────────────────────────────┐     │
│    │                                                     │     │
│    │           WOVEN MAPS CODE CITY                      │     │
│    │                                                     │     │
│    │    Gold buildings = working code                    │     │
│    │    Blue buildings = broken code                     │     │
│    │    Purple buildings = combat (LLM active)           │     │
│    │                                                     │     │
│    │    Errors float up like pollution                   │     │
│    │    Click blue spot → zoom to neighborhood           │     │
│    │                                                     │     │
│    └─────────────────────────────────────────────────────┘     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ BOTTOM FIFTH (z-index: 20) - The Overton Anchor                │
│ [Chat Input                                                   ] │
│ [Apps][Matrix][Files]    (maestro)    [Search][Phreak>][Send]   │
└─────────────────────────────────────────────────────────────────┘
```

### The "Errors Float Up Like Pollution" Concept

When a file has errors:

1. The building glows blue
2. Small particles rise from it like smoke/pollution
3. The particle count = error count
4. Clicking the building zooms camera into that "neighborhood"
5. A panel drops showing error details + "House a Digital Native?" provider selection

### The "Camera Sucks Into Neighborhood" Concept

When user clicks a blue (broken) building:

1. The camera smoothly animates toward that area
2. The scale increases (zoom in)
3. A synchronized panel drops from top
4. The panel shows the "Digital Native Housing" interface

---

## 4. TECHNICAL ARCHITECTURE

### Rendering Approach

We use **Canvas 2D in an iframe** for several reasons:

1. **Isolation**: JavaScript runs in iframe sandbox
2. **Performance**: No conflict with Marimo's reactivity
3. **Flexibility**: Full Canvas API available
4. **Compatibility**: Works in all browsers

### Data Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Codebase Scan  │────▶│  Build Graph     │────▶│  Woven Maps     │
│  (Python)       │     │  (Python)        │     │  (JavaScript)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                       │                        │
        ▼                       ▼                        ▼
   files_df              edges_df +              Canvas rendering
   (DataFrame)           node positions          with animations
```

### Communication Pattern

```python
# Python side: Build data and inject into iframe
graph_data = {
    "nodes": [...],  # {id, path, status, x, y, loc, errors}
    "edges": [...],  # {source, target, weight}
    "config": {...}  # {width, height, colors}
}

# Inject as JSON into iframe HTML
iframe_html = f"""
<script>
const GRAPH_DATA = {json.dumps(graph_data)};
// ... Canvas rendering code ...
</script>
"""

# Marimo renders iframe
mo.Html(f'<iframe srcdoc="{html.escape(iframe_html)}" ...></iframe>')
```

---

## 5. WOVEN MAPS ALGORITHM (COMPLETE)

### Original Source

- **Author**: Nicolas Barradeau
- **Blog Post**: <https://barradeau.com/blog/?p=1001>
- **Live Demo**: <https://www.barradeau.com/2017/wovenmaps/index.html>

### Algorithm Steps

#### Step 1: Collect Points

```javascript
// Each file becomes a point
// Position based on directory structure
const points = files.map(file => ({
    x: calculateX(file.path),
    y: calculateY(file.path),
    id: file.path,
    status: file.status,  // 'working' | 'broken' | 'combat'
    errors: file.errors
}));
```

#### Step 2: Delaunay Triangulation

```javascript
// Use d3-delaunay or delaunator library
import { Delaunay } from 'd3-delaunay';

const delaunay = Delaunay.from(points.map(p => [p.x, p.y]));
const triangles = delaunay.triangles;  // Flat array of point indices
```

#### Step 3: Compute Edge Lengths

```javascript
function distance(p0, p1) {
    const dx = p1.x - p0.x;
    const dy = p1.y - p0.y;
    return Math.sqrt(dx * dx + dy * dy);
}

const edges = [];
for (let i = 0; i < triangles.length; i += 3) {
    const p0 = points[triangles[i]];
    const p1 = points[triangles[i + 1]];
    const p2 = points[triangles[i + 2]];

    edges.push(
        { length: distance(p0, p1), p0, p1 },
        { length: distance(p1, p2), p1, p2: p2 },
        { length: distance(p2, p0), p2: p2, p0 }
    );
}
```

#### Step 4: Draw Gradient Layers (The Magic)

```javascript
function render(ctx, edges, config) {
    const { width, height, maxHeight, colors } = config;

    // Clear canvas
    ctx.fillStyle = colors.void;
    ctx.fillRect(0, 0, width, height);

    // Draw gradient (stacked translucent layers)
    ctx.save();
    ctx.strokeStyle = colors.gold;  // Default to gold
    ctx.lineWidth = 1;

    for (let i = 0; i < maxHeight; i++) {
        ctx.translate(0, 1);  // Move down 1px each iteration
        ctx.globalAlpha = (1 - i / maxHeight) * 0.05;  // Fade out

        // Only draw edges shorter than threshold
        renderEdges(ctx, edges, i);
    }
    ctx.restore();
}

function renderEdges(ctx, edges, minLength) {
    ctx.beginPath();
    for (const edge of edges) {
        if (edge.length < minLength) {
            ctx.moveTo(edge.p0.x, edge.p0.y);
            ctx.lineTo(edge.p1.x, edge.p1.y);
        }
    }
    ctx.stroke();
}
```

#### Step 5: Wireframe Overlays

```javascript
function renderWireframes(ctx, edges, config) {
    const { maxHeight, wireCount } = config;

    for (let i = 0; i < wireCount; i++) {
        const t = i / wireCount;
        ctx.save();
        ctx.translate(0, maxHeight * (1 - t));
        ctx.globalAlpha = 0.05 + 0.15 * t;
        renderEdges(ctx, edges, i * 10);
        ctx.restore();
    }
}
```

#### Step 6: Color Overlay (Status Colors)

```javascript
function applyStatusColors(ctx, points, config) {
    const { colors } = config;

    for (const point of points) {
        const color = colors[point.status];
        const radius = point.status === 'broken' ? 8 : 5;

        // Glow effect for broken
        if (point.status === 'broken') {
            ctx.save();
            ctx.globalAlpha = 0.3;
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(point.x, point.y, radius * 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }

        // Core dot
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
        ctx.fill();
    }
}
```

#### Step 7: Error Particles (Pollution)

```javascript
class ErrorParticle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vy = -0.5 - Math.random() * 0.5;  // Rise speed
        this.vx = (Math.random() - 0.5) * 0.3;  // Drift
        this.size = 2 + Math.random() * 3;
        this.alpha = 0.6 + Math.random() * 0.4;
        this.color = color;
        this.life = 100 + Math.random() * 100;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life--;
        this.alpha = Math.max(0, this.alpha - 0.005);
    }

    draw(ctx) {
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }

    isDead() {
        return this.life <= 0 || this.alpha <= 0;
    }
}

// Particle system
const particles = [];

function spawnErrorParticles(point) {
    const count = Math.min(point.errors.length * 2, 20);
    for (let i = 0; i < count; i++) {
        particles.push(new ErrorParticle(
            point.x + (Math.random() - 0.5) * 10,
            point.y,
            COLORS.broken
        ));
    }
}

function updateParticles(ctx) {
    for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw(ctx);
        if (particles[i].isDead()) {
            particles.splice(i, 1);
        }
    }
}
```

### Complete Woven Maps Render Function

```javascript
function renderWovenCity(ctx, data, config) {
    const { nodes, edges } = data;
    const { width, height, maxHeight, wireCount, colors } = config;

    // 1. Clear to void
    ctx.fillStyle = colors.void;
    ctx.fillRect(0, 0, width, height);

    // 2. Compute Delaunay triangulation
    const delaunay = Delaunay.from(nodes.map(n => [n.x, n.y]));
    const triangles = delaunay.triangles;

    // 3. Build edges with lengths
    const triEdges = [];
    for (let i = 0; i < triangles.length; i += 3) {
        const p0 = nodes[triangles[i]];
        const p1 = nodes[triangles[i + 1]];
        const p2 = nodes[triangles[i + 2]];

        triEdges.push(
            { length: distance(p0, p1), p0, p1 },
            { length: distance(p1, p2), p1, p2 },
            { length: distance(p2, p0), p2, p0: p0 }
        );
    }

    // 4. Draw gradient layers (the cityscape effect)
    ctx.save();
    ctx.strokeStyle = colors.gold;
    ctx.lineWidth = 1;

    for (let i = 0; i < maxHeight; i++) {
        ctx.translate(0, 1);
        ctx.globalAlpha = (1 - i / maxHeight) * 0.05;

        ctx.beginPath();
        for (const edge of triEdges) {
            if (edge.length < i) {
                ctx.moveTo(edge.p0.x, edge.p0.y);
                ctx.lineTo(edge.p1.x, edge.p1.y);
            }
        }
        ctx.stroke();
    }
    ctx.restore();

    // 5. Wireframe overlays
    for (let i = 0; i < wireCount; i++) {
        const t = i / wireCount;
        ctx.save();
        ctx.translate(0, maxHeight * (1 - t));
        ctx.globalAlpha = 0.05 + 0.15 * t;
        ctx.strokeStyle = colors.gold;

        ctx.beginPath();
        for (const edge of triEdges) {
            if (edge.length < i * 10) {
                ctx.moveTo(edge.p0.x, edge.p0.y);
                ctx.lineTo(edge.p1.x, edge.p1.y);
            }
        }
        ctx.stroke();
        ctx.restore();
    }

    // 6. Apply status colors (nodes)
    ctx.globalAlpha = 1;
    for (const node of nodes) {
        const color = colors[node.status];
        const radius = node.status === 'broken' ? 8 : 5;

        // Glow for broken
        if (node.status === 'broken') {
            ctx.save();
            ctx.globalAlpha = 0.3;
            ctx.shadowColor = color;
            ctx.shadowBlur = 15;
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius * 1.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }

        // Purple glow for combat
        if (node.status === 'combat') {
            ctx.save();
            ctx.globalAlpha = 0.5;
            ctx.shadowColor = color;
            ctx.shadowBlur = 20;
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius * 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }

        // Core dot
        ctx.globalAlpha = 1;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
        ctx.fill();
    }

    // 7. Update and draw error particles
    updateParticles(ctx);

    // 8. Spawn new particles for broken nodes
    for (const node of nodes) {
        if (node.status === 'broken' && Math.random() < 0.1) {
            spawnErrorParticles(node);
        }
    }
}
```

---

## 6. MARIMO INTEGRATION

### Iframe Approach

```python
import marimo as mo
import json
import html

def create_woven_map_iframe(graph_data: dict, width: int = 800, height: int = 600) -> mo.Html:
    """Create an iframe containing the Woven Maps visualization."""

    iframe_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/d3-delaunay@6"></script>
        <style>
            body {{ margin: 0; overflow: hidden; background: #0A0A0B; }}
            canvas {{ display: block; }}
        </style>
    </head>
    <body>
        <canvas id="city"></canvas>
        <script>
            const GRAPH_DATA = {json.dumps(graph_data)};
            const COLORS = {{
                void: '#0A0A0B',
                working: '#D4AF37',
                broken: '#1fbdea',
                combat: '#9D4EDD'
            }};

            // ... full rendering code here ...
        </script>
    </body>
    </html>
    '''

    # Escape for srcdoc attribute
    escaped = html.escape(iframe_html)

    return mo.Html(f'''
        <iframe
            srcdoc="{escaped}"
            width="{width}"
            height="{height}"
            style="border: none; border-radius: 8px;"
        ></iframe>
    ''')
```

### Building Graph Data from Codebase

```python
import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any
import math

@dataclass
class CodeNode:
    path: str
    status: str  # 'working' | 'broken' | 'combat'
    loc: int     # Lines of code
    errors: List[str]
    x: float = 0.0
    y: float = 0.0

def scan_codebase(root: str) -> List[CodeNode]:
    """Scan codebase and return list of CodeNodes."""
    nodes = []
    skip_dirs = {'node_modules', '.git', '__pycache__', 'dist', 'build', '.venv', 'venv'}
    code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.cpp', '.c', '.h'}

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            ext = Path(filename).suffix
            if ext not in code_extensions:
                continue

            filepath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(filepath, root)

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    loc = len(lines)

                    # Detect potential errors (simplified)
                    errors = []
                    if 'TODO' in content or 'FIXME' in content:
                        errors.append('Contains TODO/FIXME')
                    if re.search(r'(console\.log|print\s*\(.*debug)', content, re.I):
                        errors.append('Debug statements present')

                    status = 'broken' if errors else 'working'

                    nodes.append(CodeNode(
                        path=relpath,
                        status=status,
                        loc=loc,
                        errors=errors
                    ))
            except Exception as e:
                nodes.append(CodeNode(
                    path=relpath,
                    status='broken',
                    loc=0,
                    errors=[str(e)]
                ))

    return nodes

def calculate_layout(nodes: List[CodeNode], width: int, height: int) -> List[CodeNode]:
    """Position nodes based on directory structure."""
    # Group by directory
    dirs: Dict[str, List[CodeNode]] = {}
    for node in nodes:
        dir_path = str(Path(node.path).parent)
        if dir_path not in dirs:
            dirs[dir_path] = []
        dirs[dir_path].append(node)

    # Layout directories in a grid
    dir_list = list(dirs.keys())
    cols = max(1, int(math.sqrt(len(dir_list))))

    padding = 50
    usable_width = width - padding * 2
    usable_height = height - padding * 2

    for i, dir_path in enumerate(dir_list):
        dir_x = (i % cols) / max(1, cols) * usable_width + padding
        dir_y = (i // cols) / max(1, len(dir_list) // cols + 1) * usable_height + padding

        # Position files within directory
        dir_nodes = dirs[dir_path]
        for j, node in enumerate(dir_nodes):
            angle = (j / len(dir_nodes)) * 2 * math.pi
            radius = 30 + (node.loc / 100) * 20  # Larger files = further from center
            node.x = dir_x + math.cos(angle) * radius + (hash(node.path) % 20 - 10)
            node.y = dir_y + math.sin(angle) * radius + (hash(node.path) % 20 - 10)

    return nodes

def build_graph_data(root: str, width: int = 800, height: int = 600) -> dict:
    """Build complete graph data for visualization."""
    nodes = scan_codebase(root)
    nodes = calculate_layout(nodes, width, height)

    return {
        "nodes": [
            {
                "id": node.path,
                "path": node.path,
                "status": node.status,
                "x": node.x,
                "y": node.y,
                "loc": node.loc,
                "errors": node.errors
            }
            for node in nodes
        ],
        "config": {
            "width": width,
            "height": height,
            "maxHeight": 200,
            "wireCount": 10
        }
    }
```

---

## 7. COMPLETE IMPLEMENTATION CODE

### Full Iframe HTML Template

```python
WOVEN_MAPS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/d3-delaunay@6"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0A0A0B;
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
        }
        canvas { display: block; }
        #tooltip {
            position: absolute;
            background: #121214;
            border: 1px solid #D4AF37;
            border-radius: 4px;
            padding: 8px 12px;
            color: #fff;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            max-width: 300px;
            z-index: 100;
        }
        #tooltip.visible { opacity: 1; }
        #tooltip .path { color: #D4AF37; font-weight: bold; }
        #tooltip .status { margin-top: 4px; }
        #tooltip .status.working { color: #D4AF37; }
        #tooltip .status.broken { color: #1fbdea; }
        #tooltip .status.combat { color: #9D4EDD; }
        #tooltip .errors { margin-top: 4px; color: #1fbdea; font-size: 11px; }
    </style>
</head>
<body>
    <canvas id="city"></canvas>
    <div id="tooltip"></div>

    <script>
        // ============================================================
        // DATA INJECTION (replaced by Python)
        // ============================================================
        const GRAPH_DATA = __GRAPH_DATA__;

        // ============================================================
        // CONSTANTS
        // ============================================================
        const COLORS = {
            void: '#0A0A0B',
            working: '#D4AF37',
            broken: '#1fbdea',
            combat: '#9D4EDD',
            wireframe: '#333333'
        };

        // ============================================================
        // CANVAS SETUP
        // ============================================================
        const canvas = document.getElementById('city');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');

        const { nodes, config } = GRAPH_DATA;
        const { width, height, maxHeight, wireCount } = config;

        canvas.width = width;
        canvas.height = height;

        // ============================================================
        // PARTICLE SYSTEM
        // ============================================================
        const particles = [];

        class Particle {
            constructor(x, y, color) {
                this.x = x;
                this.y = y;
                this.vy = -0.3 - Math.random() * 0.5;
                this.vx = (Math.random() - 0.5) * 0.2;
                this.size = 1.5 + Math.random() * 2.5;
                this.alpha = 0.4 + Math.random() * 0.4;
                this.color = color;
                this.life = 150 + Math.random() * 100;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life--;
                this.alpha = Math.max(0, this.alpha - 0.003);
                this.size = Math.max(0.5, this.size - 0.01);
            }

            draw(ctx) {
                ctx.globalAlpha = this.alpha;
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }

            isDead() {
                return this.life <= 0 || this.alpha <= 0;
            }
        }

        function spawnParticles(node) {
            if (node.status !== 'broken') return;
            const count = Math.min(node.errors.length + 1, 5);
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(
                    node.x + (Math.random() - 0.5) * 15,
                    node.y + (Math.random() - 0.5) * 5,
                    COLORS.broken
                ));
            }
        }

        function updateParticles() {
            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].update();
                particles[i].draw(ctx);
                if (particles[i].isDead()) {
                    particles.splice(i, 1);
                }
            }
        }

        // ============================================================
        // DELAUNAY TRIANGULATION
        // ============================================================
        function distance(p0, p1) {
            const dx = p1.x - p0.x;
            const dy = p1.y - p0.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        // Build triangulation
        const points = nodes.map(n => [n.x, n.y]);
        const delaunay = d3.Delaunay.from(points);
        const triangles = delaunay.triangles;

        // Build edges
        const edges = [];
        for (let i = 0; i < triangles.length; i += 3) {
            const i0 = triangles[i];
            const i1 = triangles[i + 1];
            const i2 = triangles[i + 2];

            const p0 = nodes[i0];
            const p1 = nodes[i1];
            const p2 = nodes[i2];

            edges.push(
                { length: distance(p0, p1), p0, p1 },
                { length: distance(p1, p2), p0: p1, p1: p2 },
                { length: distance(p2, p0), p0: p2, p1: p0 }
            );
        }

        // ============================================================
        // RENDERING
        // ============================================================
        function renderEdges(minLength, color, alpha) {
            ctx.globalAlpha = alpha;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
            ctx.beginPath();

            for (const edge of edges) {
                if (edge.length < minLength) {
                    ctx.moveTo(edge.p0.x, edge.p0.y);
                    ctx.lineTo(edge.p1.x, edge.p1.y);
                }
            }
            ctx.stroke();
        }

        function render() {
            // Clear
            ctx.fillStyle = COLORS.void;
            ctx.fillRect(0, 0, width, height);

            // Draw gradient layers (the cityscape magic)
            ctx.save();
            for (let i = 0; i < maxHeight; i++) {
                ctx.translate(0, 0.5);
                const alpha = (1 - i / maxHeight) * 0.04;
                renderEdges(i * 0.5, COLORS.working, alpha);
            }
            ctx.restore();

            // Wireframe overlays
            for (let i = 0; i < wireCount; i++) {
                const t = i / wireCount;
                ctx.save();
                ctx.translate(0, maxHeight * (1 - t) * 0.3);
                renderEdges(i * 15, COLORS.working, 0.03 + 0.1 * t);
                ctx.restore();
            }

            // Draw import edges (connections)
            ctx.globalAlpha = 0.15;
            ctx.strokeStyle = COLORS.wireframe;
            ctx.lineWidth = 0.5;
            // (Would draw actual import connections here if we had that data)

            // Draw nodes
            ctx.globalAlpha = 1;
            for (const node of nodes) {
                const color = COLORS[node.status];
                const baseRadius = 3 + Math.min(node.loc / 50, 8);

                // Glow for non-working
                if (node.status === 'broken' || node.status === 'combat') {
                    ctx.save();
                    ctx.globalAlpha = 0.3;
                    ctx.shadowColor = color;
                    ctx.shadowBlur = 20;
                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, baseRadius * 2, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }

                // Core
                ctx.globalAlpha = 0.9;
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(node.x, node.y, baseRadius, 0, Math.PI * 2);
                ctx.fill();

                // Inner highlight
                ctx.globalAlpha = 0.5;
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(node.x - baseRadius * 0.3, node.y - baseRadius * 0.3, baseRadius * 0.3, 0, Math.PI * 2);
                ctx.fill();
            }

            // Update particles
            updateParticles();

            // Spawn new particles (randomly for broken nodes)
            for (const node of nodes) {
                if (node.status === 'broken' && Math.random() < 0.05) {
                    spawnParticles(node);
                }
            }

            requestAnimationFrame(render);
        }

        // ============================================================
        // INTERACTION
        // ============================================================
        function findNodeAt(x, y) {
            for (const node of nodes) {
                const dx = node.x - x;
                const dy = node.y - y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const radius = 3 + Math.min(node.loc / 50, 8);
                if (dist < radius + 5) {
                    return node;
                }
            }
            return null;
        }

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const node = findNodeAt(x, y);

            if (node) {
                tooltip.innerHTML = `
                    <div class="path">${node.path}</div>
                    <div class="status ${node.status}">${node.status.toUpperCase()} | ${node.loc} LOC</div>
                    ${node.errors.length ? `<div class="errors">${node.errors.join('<br>')}</div>` : ''}
                `;
                tooltip.style.left = (e.clientX + 10) + 'px';
                tooltip.style.top = (e.clientY + 10) + 'px';
                tooltip.classList.add('visible');
                canvas.style.cursor = 'pointer';
            } else {
                tooltip.classList.remove('visible');
                canvas.style.cursor = 'default';
            }
        });

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const node = findNodeAt(x, y);

            if (node) {
                // Send message to parent (Marimo)
                window.parent.postMessage({
                    type: 'NODE_CLICKED',
                    node: {
                        path: node.path,
                        status: node.status,
                        errors: node.errors
                    }
                }, '*');
            }
        });

        // ============================================================
        // START
        // ============================================================
        render();
    </script>
</body>
</html>
'''
```

### Integration Function for 06_maestro.py

```python
def create_code_city(STATE_MANAGERS: dict, width: int = 800, height: int = 600) -> Any:
    """Create the Woven Maps Code City visualization."""
    import marimo as mo
    import json
    import html

    get_root, _ = STATE_MANAGERS["root"]
    root = get_root()

    if not root or not os.path.isdir(root):
        return mo.md("*Set a valid project root to visualize the codebase.*")

    # Build graph data
    graph_data = build_graph_data(root, width, height)

    if not graph_data["nodes"]:
        return mo.md("*No code files found in project.*")

    # Inject data into template
    iframe_html = WOVEN_MAPS_TEMPLATE.replace(
        '__GRAPH_DATA__',
        json.dumps(graph_data)
    )

    # Escape for srcdoc
    escaped = html.escape(iframe_html)

    return mo.Html(f'''
        <div style="
            background: #0A0A0B;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(212, 175, 55, 0.2);
        ">
            <iframe
                srcdoc="{escaped}"
                width="{width}"
                height="{height}"
                style="border: none; display: block;"
            ></iframe>
        </div>
    ''')
```

---

## 8. DATA STRUCTURES

### CodeNode

```python
@dataclass
class CodeNode:
    path: str           # Relative path from root
    status: str         # 'working' | 'broken' | 'combat'
    loc: int            # Lines of code
    errors: List[str]   # Error messages
    x: float = 0.0      # Canvas X position
    y: float = 0.0      # Canvas Y position
```

### Graph Data (JSON)

```json
{
    "nodes": [
        {
            "id": "src/main.py",
            "path": "src/main.py",
            "status": "working",
            "x": 150.5,
            "y": 200.3,
            "loc": 342,
            "errors": []
        },
        {
            "id": "src/utils.py",
            "path": "src/utils.py",
            "status": "broken",
            "x": 180.2,
            "y": 220.1,
            "loc": 89,
            "errors": ["Contains TODO", "Debug statements present"]
        }
    ],
    "config": {
        "width": 800,
        "height": 600,
        "maxHeight": 200,
        "wireCount": 10
    }
}
```

### Edge (JavaScript)

```javascript
{
    length: 45.2,       // Euclidean distance
    p0: { x, y, ... },  // Source node reference
    p1: { x, y, ... }   // Target node reference
}
```

---

## 9. COLOR SYSTEM

### Exact Hex Values (NO EXCEPTIONS)

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| `--gold-metallic` | `#D4AF37` | rgb(212, 175, 55) | Working code, UI highlights |
| `--blue-dominant` | `#1fbdea` | rgb(31, 189, 234) | Broken code, UI default |
| `--purple-combat` | `#9D4EDD` | rgb(157, 78, 221) | Combat state, active debugging |
| `--bg-primary` | `#0A0A0B` | rgb(10, 10, 11) | The Void background |
| `--bg-elevated` | `#121214` | rgb(18, 18, 20) | Elevated surfaces |
| `--gold-dark` | `#B8860B` | rgb(184, 134, 11) | Secondary gold |
| `--gold-saffron` | `#F4C430` | rgb(244, 196, 48) | Bright highlights |

### Three-State System

```
┌─────────────────────────────────────────────────────────────┐
│                     CODE STATUS                             │
├─────────────────────────────────────────────────────────────┤
│  GOLD (#D4AF37)    │  Working                               │
│                    │  - All imports resolve                 │
│                    │  - No errors or warnings               │
│                    │  - TypeScript/lint passes              │
├─────────────────────────────────────────────────────────────┤
│  BLUE (#1fbdea)    │  Broken                                │
│                    │  - Has errors                          │
│                    │  - Unresolved imports                  │
│                    │  - Needs attention                     │
├─────────────────────────────────────────────────────────────┤
│  PURPLE (#9D4EDD)  │  Combat                                │
│                    │  - LLM General actively deployed       │
│                    │  - Being debugged/fixed                │
│                    │  - Human + AI collaboration active     │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. ANIMATION SPECIFICATIONS

### Emergence Animation (CSS)

```css
@keyframes emerge-void {
    from {
        opacity: 0;
        transform: scale(0.95);
        filter: blur(4px);
    }
    to {
        opacity: 1;
        transform: scale(1);
        filter: blur(0);
    }
}

.emerge {
    animation: emerge-void 0.3s ease-out forwards;
}
```

### Particle Animation (JavaScript)

```javascript
// Particles rise and fade
class Particle {
    update() {
        this.y += this.vy;      // Rise (vy is negative)
        this.x += this.vx;      // Drift
        this.alpha -= 0.003;    // Fade
        this.size -= 0.01;      // Shrink
        this.life--;
    }
}
```

### Camera Zoom (Future - Three.js)

```javascript
// Smooth camera animation to target
function zoomToNode(node, camera, controls) {
    const target = new THREE.Vector3(node.x, 0, node.y);
    const duration = 1000;
    const start = camera.position.clone();
    const startTime = Date.now();

    function animate() {
        const elapsed = Date.now() - startTime;
        const t = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - t, 3);  // Ease out cubic

        camera.position.lerpVectors(start, target.clone().add(new THREE.Vector3(0, 30, 30)), eased);
        controls.target.lerp(target, eased);

        if (t < 1) requestAnimationFrame(animate);
    }
    animate();
}
```

---

## 11. TESTING PROCEDURES

### Unit Test: Graph Data Generation

```python
def test_build_graph_data():
    """Test that graph data is correctly generated."""
    import tempfile
    import os

    # Create temp directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        os.makedirs(os.path.join(tmpdir, 'src'))

        with open(os.path.join(tmpdir, 'src', 'main.py'), 'w') as f:
            f.write('print("hello")\n' * 100)

        with open(os.path.join(tmpdir, 'src', 'broken.py'), 'w') as f:
            f.write('# TODO: fix this\nprint("broken")')

        # Generate graph data
        data = build_graph_data(tmpdir, 800, 600)

        # Assertions
        assert len(data['nodes']) == 2
        assert any(n['status'] == 'working' for n in data['nodes'])
        assert any(n['status'] == 'broken' for n in data['nodes'])
        assert all(0 <= n['x'] <= 800 for n in data['nodes'])
        assert all(0 <= n['y'] <= 600 for n in data['nodes'])

test_build_graph_data()
print("✓ Graph data generation test passed")
```

### Integration Test: Iframe Renders

```python
def test_iframe_renders():
    """Test that iframe HTML is valid."""
    import json

    test_data = {
        "nodes": [
            {"id": "test.py", "path": "test.py", "status": "working", "x": 100, "y": 100, "loc": 50, "errors": []}
        ],
        "config": {"width": 400, "height": 300, "maxHeight": 100, "wireCount": 5}
    }

    html = WOVEN_MAPS_TEMPLATE.replace('__GRAPH_DATA__', json.dumps(test_data))

    # Check for required elements
    assert '<canvas id="city">' in html
    assert 'd3-delaunay' in html
    assert '#D4AF37' in html  # Gold color
    assert '#1fbdea' in html  # Blue color
    assert '#9D4EDD' in html  # Purple color

    print("✓ Iframe rendering test passed")

test_iframe_renders()
```

### Visual Test: Run in Marimo

```bash
# Start Marimo in edit mode
cd /home/user/Orchestr8_jr
marimo edit IP/orchestr8_app.py

# Navigate to "The Void" tab
# Set project root to a codebase
# Verify:
# 1. Canvas renders with cityscape
# 2. Gold dots for working files
# 3. Blue dots for files with TODO/FIXME
# 4. Particles rise from blue dots
# 5. Tooltip appears on hover
# 6. Click triggers console message
```

---

## 12. THREE.JS GRADUATION PATH

When ready to upgrade from Canvas 2D to Three.js WebGL:

### Step 1: Add Three.js to iframe

```html
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
```

### Step 2: Replace Canvas with Three.js Scene

```javascript
// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0A0A0B);

const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
camera.position.set(0, 100, 100);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(width, height);
document.body.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
```

### Step 3: Convert Nodes to 3D Buildings

```javascript
function createBuilding(node) {
    const height = Math.max(5, node.loc / 10);
    const geometry = new THREE.BoxGeometry(5, height, 5);
    const material = new THREE.MeshLambertMaterial({
        color: COLORS[node.status],
        emissive: node.status === 'broken' ? COLORS.broken : 0x000000,
        emissiveIntensity: node.status === 'broken' ? 0.3 : 0
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(node.x - width/2, height/2, node.y - height/2);
    mesh.userData = node;

    return mesh;
}
```

### Step 4: Add Low-Poly Assets

Download from:

- Kenney: <https://kenney.nl/assets/city-kit-commercial>
- Quaternius: <https://quaternius.com/packs/ultimatetexturedbuildings.html>

Load with GLTFLoader:

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const loader = new GLTFLoader();
loader.load('assets/building_small.glb', (gltf) => {
    const model = gltf.scene;
    model.scale.set(0.1, 0.1, 0.1);
    scene.add(model);
});
```

### Step 5: VS Code Fork (Ultimate Goal)

See `Big Pickle/CLAUDE_EXECUTION_PROMPT.md` for full VS Code fork instructions.

---

## 13. TROUBLESHOOTING GUIDE

### Issue: Canvas is blank

**Cause:** Graph data not injected correctly
**Fix:** Check that `__GRAPH_DATA__` is replaced with valid JSON

```python
# Debug: Print graph data
print(json.dumps(graph_data, indent=2))
```

### Issue: Delaunay fails with "fewer than 3 points"

**Cause:** Not enough files scanned
**Fix:** Ensure root directory has code files, check extension filter

```python
code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs'}
```

### Issue: Particles not appearing

**Cause:** No broken files detected
**Fix:** Add a file with `TODO` or `FIXME` to test

### Issue: iframe security error

**Cause:** Cross-origin restriction
**Fix:** Use `srcdoc` attribute instead of `src`

```python
mo.Html(f'<iframe srcdoc="{escaped_html}" ...>')
```

### Issue: Colors look wrong

**Cause:** Hex values not exact
**Fix:** Use EXACT values:

- Gold: `#D4AF37` (NOT `#d4af37` or `gold`)
- Blue: `#1fbdea` (NOT `#1FBDEA` or `cyan`)
- Purple: `#9D4EDD` (NOT `purple`)

---

## 14. FILE LOCATIONS REFERENCE

### Key Files

| File | Purpose |
|------|---------|
| `IP/orchestr8_app.py` | Main Marimo application |
| `IP/plugins/06_maestro.py` | The Void plugin (implement here) |
| `Big Pickle/WOVEN_MAPS_EXECUTION_SPEC.md` | This document |
| `Big Pickle/CLAUDE_EXECUTION_PROMPT.md` | VS Code fork spec |
| `Big Pickle/EMERGENCE_ANIMATION_CATALOG.md` | Animation reference |
| `Big Pickle/UI_ARCHITECTURE_SPEC.md` | UI layout spec |
| `style/MAESTROVIEW_REFERENCE.md` | Authoritative style guide |

### Directory Structure

```
Orchestr8_jr/
├── IP/
│   ├── orchestr8_app.py          # Main app
│   ├── plugins/
│   │   ├── 00_welcome.py
│   │   ├── 01_generator.py
│   │   ├── 02_explorer.py
│   │   ├── 03_gatekeeper.py
│   │   ├── 04_connie_ui.py
│   │   ├── 05_universal_bridge.py
│   │   └── 06_maestro.py         # ← IMPLEMENT HERE
│   ├── mermaid_generator.py      # (stub)
│   ├── terminal_spawner.py       # (stub)
│   ├── health_checker.py         # (stub)
│   └── briefing_generator.py     # (stub)
├── Big Pickle/
│   ├── WOVEN_MAPS_EXECUTION_SPEC.md  # ← THIS FILE
│   ├── CLAUDE_EXECUTION_PROMPT.md
│   ├── EMERGENCE_ANIMATION_CATALOG.md
│   └── UI_ARCHITECTURE_SPEC.md
├── style/
│   └── MAESTROVIEW_REFERENCE.md
└── docs/
    └── UI_PRESSURE_TEST_REPORT.md
```

---

## EXECUTION CHECKLIST

### Pre-Implementation

- [ ] Read this entire document
- [ ] Verify file locations exist
- [ ] Check Marimo is installed (`pip install marimo`)
- [ ] Understand the STATE_MANAGERS pattern

### Implementation Steps

- [ ] Read current `06_maestro.py`
- [ ] Add `build_graph_data()` function
- [ ] Add `scan_codebase()` function
- [ ] Add `calculate_layout()` function
- [ ] Add `WOVEN_MAPS_TEMPLATE` constant
- [ ] Add `create_code_city()` function
- [ ] Integrate into `render()` function
- [ ] Test with `marimo edit IP/orchestr8_app.py`

### Verification

- [ ] Canvas renders cityscape
- [ ] Gold/Blue/Purple colors correct
- [ ] Particles rise from broken nodes
- [ ] Tooltip shows on hover
- [ ] Click logs node info

### Commit

- [ ] All tests pass
- [ ] `git add IP/plugins/06_maestro.py`
- [ ] Commit with descriptive message
- [ ] Push to branch

---

## FINAL NOTES

This document is designed to be **completely self-contained**. Any Claude instance should be able to:

1. Read this document
2. Understand the full context
3. Implement the Woven Maps visualization
4. Without any prior conversation history

**Key principles:**

- NO BREATHING ANIMATIONS (things EMERGE, not breathe)
- Colors are EXACT (no approximations)
- The Void is THE central metaphor
- Errors float up like pollution
- The Emperor must see everything

**When in doubt:**

- Check `style/MAESTROVIEW_REFERENCE.md` for styling
- Check `Big Pickle/CLAUDE_EXECUTION_PROMPT.md` for broader vision
- Check `Big Pickle/EMERGENCE_ANIMATION_CATALOG.md` for animation options

---

**END OF SPECIFICATION**

*This document is the single source of truth for Woven Maps implementation.*
*Total length: ~1500 lines | Last updated: 2026-01-26*

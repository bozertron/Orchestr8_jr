"""
Woven Maps Code City Visualization - Enhanced Edition
======================================================

Enhanced with:
- Emergence animation (particles coalesce from chaos)
- Teal → Gold frame transition (scan progress → complete)
- Organic curl-like particle motion
- Phase-based initialization (tuning → coalescing → emergence)

Based on Nicolas Barradeau's "Woven Maps" algorithm
Aligned with stereOS Maestro vision (M14.jpg reference)
"""

from __future__ import annotations

import json
import html
import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional

# =============================================================================
# COLOR CONSTANTS - EXACT, NO EXCEPTIONS
# =============================================================================

COLORS = {
    "gold_metallic": "#D4AF37",   # Working code
    "blue_dominant": "#1fbdea",   # Broken code / Teal during scan
    "purple_combat": "#9D4EDD",   # Combat (LLM active)
    "bg_primary": "#0A0A0B",      # The Void
    "bg_elevated": "#121214",     # Elevated surfaces
    "gold_dark": "#B8860B",       # Secondary gold
    "gold_saffron": "#F4C430",    # Bright highlights
}

JS_COLORS = {
    "void": "#0A0A0B",
    "working": "#D4AF37",
    "broken": "#1fbdea",
    "combat": "#9D4EDD",
    "wireframe": "#333333",
    "teal": "#1fbdea",
    "gold": "#D4AF37",
}

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CodeNode:
    """Represents a file in the codebase."""
    path: str
    status: str = "working"
    loc: int = 0
    errors: List[str] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.path,
            "path": self.path,
            "status": self.status,
            "x": self.x,
            "y": self.y,
            "loc": self.loc,
            "errors": self.errors,
        }


@dataclass
class GraphConfig:
    """Configuration for the visualization."""
    width: int = 800
    height: int = 600
    max_height: int = 250       # Taller cityscape silhouette
    wire_count: int = 15        # More wireframe layers for richness
    show_particles: bool = True
    show_tooltip: bool = True
    emergence_duration: float = 2.5  # Slightly longer for drama

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "maxHeight": self.max_height,
            "wireCount": self.wire_count,
            "showParticles": self.show_particles,
            "showTooltip": self.show_tooltip,
            "emergenceDuration": self.emergence_duration,
        }


@dataclass
class GraphData:
    """Complete data structure for visualization."""
    nodes: List[CodeNode] = field(default_factory=list)
    config: GraphConfig = field(default_factory=GraphConfig)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "config": self.config.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


# =============================================================================
# CODEBASE SCANNING
# =============================================================================

SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'dist', 'build',
    '.venv', 'venv', 'env', '.env', '.tox', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'coverage', '.coverage',
    'htmlcov', '.idea', '.vscode', 'target', 'out', 'bin',
}

CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.mjs', '.cjs',
    '.java', '.go', '.rs', '.cpp', '.c', '.h', '.hpp',
    '.cs', '.rb', '.php', '.swift', '.kt', '.scala',
    '.vue', '.svelte', '.astro',
}


def scan_codebase(
    root: str,
    skip_dirs: Optional[set] = None,
    extensions: Optional[set] = None,
) -> List[CodeNode]:
    """Scan a codebase and return a list of CodeNodes."""
    skip = skip_dirs or SKIP_DIRS
    exts = extensions or CODE_EXTENSIONS
    nodes = []

    root_path = Path(root).resolve()
    if not root_path.exists():
        return nodes

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith('.')]

        for filename in filenames:
            ext = Path(filename).suffix.lower()
            if ext not in exts:
                continue

            filepath = Path(dirpath) / filename
            relpath = str(filepath.relative_to(root_path))

            try:
                node = analyze_file(filepath, relpath)
                nodes.append(node)
            except Exception as e:
                nodes.append(CodeNode(
                    path=relpath,
                    status="broken",
                    loc=0,
                    errors=[f"Read error: {str(e)}"],
                ))

    return nodes


def analyze_file(filepath: Path, relpath: str) -> CodeNode:
    """Analyze a single file for status and metrics."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return CodeNode(path=relpath, status="broken", errors=[str(e)])

    lines = content.split('\n')
    loc = len(lines)
    errors = []

    # TODO/FIXME detection
    todo_pattern = re.compile(r'\b(TODO|FIXME|XXX|HACK|BUG)\b', re.IGNORECASE)
    for i, line in enumerate(lines[:500], 1):
        if todo_pattern.search(line):
            match = todo_pattern.search(line)
            errors.append(f"Line {i}: {match.group(0)} found")
            if len(errors) >= 5:
                errors.append("... and more")
                break

    # Debug statement detection
    debug_patterns = [
        (r'console\.(log|debug|info)\s*\(', 'console.log'),
        (r'print\s*\([^)]*debug', 'debug print'),
        (r'debugger\s*;?', 'debugger statement'),
        (r'pdb\.set_trace\(\)', 'pdb breakpoint'),
        (r'breakpoint\(\)', 'breakpoint'),
    ]

    for pattern, name in debug_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"{name} detected")

    status = "broken" if errors else "working"
    return CodeNode(path=relpath, status=status, loc=loc, errors=errors[:10])


def calculate_layout(
    nodes: List[CodeNode],
    width: int,
    height: int,
    padding: int = 60,
) -> List[CodeNode]:
    """Calculate 2D positions for nodes based on directory structure."""
    if not nodes:
        return nodes

    dirs: Dict[str, List[CodeNode]] = {}
    for node in nodes:
        dir_path = str(Path(node.path).parent)
        if dir_path == '.':
            dir_path = 'root'
        if dir_path not in dirs:
            dirs[dir_path] = []
        dirs[dir_path].append(node)

    dir_count = len(dirs)
    cols = max(1, int(math.ceil(math.sqrt(dir_count))))
    rows = max(1, int(math.ceil(dir_count / cols)))

    usable_width = width - padding * 2
    usable_height = height - padding * 2
    cell_width = usable_width / cols
    cell_height = usable_height / rows

    for i, (dir_path, dir_nodes) in enumerate(dirs.items()):
        col = i % cols
        row = i // cols
        center_x = padding + col * cell_width + cell_width / 2
        center_y = padding + row * cell_height + cell_height / 2

        file_count = len(dir_nodes)
        max_radius = min(cell_width, cell_height) / 2 - 20

        for j, node in enumerate(dir_nodes):
            if file_count == 1:
                node.x = center_x
                node.y = center_y
            else:
                angle = (j / file_count) * 2 * math.pi - math.pi / 2
                size_factor = min(1.0, node.loc / 500)
                radius = 20 + size_factor * (max_radius - 20)
                jitter_x = (hash(node.path) % 21 - 10)
                jitter_y = (hash(node.path + 'y') % 21 - 10)
                node.x = center_x + math.cos(angle) * radius + jitter_x
                node.y = center_y + math.sin(angle) * radius + jitter_y

        for node in dir_nodes:
            node.x = max(padding, min(width - padding, node.x))
            node.y = max(padding, min(height - padding, node.y))

    return nodes


def build_graph_data(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
) -> GraphData:
    """Build complete graph data from a codebase root."""
    nodes = scan_codebase(root)
    nodes = calculate_layout(nodes, width, height)
    config = GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )
    return GraphData(nodes=nodes, config=config)


# =============================================================================
# ENHANCED IFRAME TEMPLATE - With Emergence Animations
# =============================================================================

WOVEN_MAPS_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/d3-delaunay@6"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0A0A0B;
            overflow: hidden;
            font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
        }

        /* Canvas with animated border */
        #canvas-container {
            position: relative;
            border: 1px solid #1fbdea;
            border-radius: 4px;
            transition: border-color 1.5s ease;
        }
        #canvas-container.emerged {
            border-color: #D4AF37;
        }

        canvas { display: block; cursor: crosshair; }

        /* Phase indicator */
        #phase {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 9px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #1fbdea;
            transition: color 1s ease;
            opacity: 0.7;
        }
        #phase.emerged { color: #D4AF37; }

        /* Tooltip */
        #tooltip {
            position: absolute;
            background: #121214;
            border: 1px solid #D4AF37;
            border-radius: 4px;
            padding: 8px 12px;
            color: #fff;
            font-size: 11px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.15s ease;
            max-width: 320px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        #tooltip.visible { opacity: 1; }
        #tooltip .path { color: #D4AF37; font-weight: 600; word-break: break-all; margin-bottom: 4px; }
        #tooltip .meta { display: flex; gap: 12px; margin-bottom: 4px; }
        #tooltip .status { padding: 2px 6px; border-radius: 3px; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
        #tooltip .status.working { background: rgba(212, 175, 55, 0.2); color: #D4AF37; }
        #tooltip .status.broken { background: rgba(31, 189, 234, 0.2); color: #1fbdea; }
        #tooltip .status.combat { background: rgba(157, 78, 221, 0.2); color: #9D4EDD; }
        #tooltip .loc { color: #888; }
        #tooltip .errors { margin-top: 6px; padding-top: 6px; border-top: 1px solid #333; color: #1fbdea; font-size: 10px; line-height: 1.4; }
        #tooltip .error-item { margin: 2px 0; }

        /* Stats */
        #stats {
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: #666;
            font-size: 10px;
            letter-spacing: 0.05em;
        }
        #stats span { margin-right: 12px; }
        #stats .working { color: #D4AF37; }
        #stats .broken { color: #1fbdea; }
        #stats .combat { color: #9D4EDD; }
    </style>
</head>
<body>
    <div id="canvas-container">
        <canvas id="city"></canvas>
        <div id="phase">tuning...</div>
    </div>
    <div id="tooltip"></div>
    <div id="stats"></div>

    <script>
        // ================================================================
        // DATA & CONFIG
        // ================================================================
        const GRAPH_DATA = __GRAPH_DATA__;
        const { nodes, config } = GRAPH_DATA;
        const { width, height, maxHeight, wireCount, emergenceDuration = 2.0 } = config;

        const COLORS = {
            void: '#0A0A0B',
            working: '#D4AF37',
            broken: '#1fbdea',
            combat: '#9D4EDD',
            wireframe: '#2a2a2a',
            teal: '#1fbdea',
            gold: '#D4AF37'
        };

        // ================================================================
        // SETUP
        // ================================================================
        const container = document.getElementById('canvas-container');
        const canvas = document.getElementById('city');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const stats = document.getElementById('stats');
        const phaseEl = document.getElementById('phase');

        canvas.width = width;
        canvas.height = height;

        // Stats
        const workingCount = nodes.filter(n => n.status === 'working').length;
        const brokenCount = nodes.filter(n => n.status === 'broken').length;
        const combatCount = nodes.filter(n => n.status === 'combat').length;
        stats.innerHTML = `
            <span class="working">${workingCount} working</span>
            <span class="broken">${brokenCount} broken</span>
            ${combatCount ? `<span class="combat">${combatCount} combat</span>` : ''}
            <span>${nodes.length} files</span>
        `;

        // ================================================================
        // WAVE FIELD CONFIG - Smooth landscape morphing (LOW frequency)
        // ================================================================
        const waveField = {
            sourceLeftX: width * 0.2,    // Left wave source
            sourceRightX: width * 0.8,   // Right wave source
            ampBase: 20,                  // Higher amplitude for visible flow
            speedBase: 0.0008,            // SLOW wave speed for smoothness
            frequency: 0.004              // LOW frequency for landscape morphing
        };

        // ================================================================
        // EMERGENCE STATE
        // ================================================================
        let emergenceProgress = 0;  // 0 to 1
        let emerged = false;
        const emergenceStartTime = performance.now();
        const emergenceDurationMs = emergenceDuration * 1000;

        // Store original positions, start from chaos
        const nodeStates = nodes.map(n => ({
            targetX: n.x,
            targetY: n.y,
            // Start positions: scattered from center with chaos
            currentX: width / 2 + (Math.random() - 0.5) * width * 0.8,
            currentY: height / 2 + (Math.random() - 0.5) * height * 0.8,
            currentAlpha: 0,
            targetAlpha: 1,
            // Emergence timing: stagger based on distance from center
            delay: Math.sqrt(Math.pow(n.x - width/2, 2) + Math.pow(n.y - height/2, 2)) / (width/2) * 0.3,
            // Entry offset for wave field
            entryOffset: Math.random() * 4
        }));

        // Wave field calculation - smooth mathematical landscape morphing
        function calcWaveDisplacement(x, y, elapsed) {
            // Use LOW frequency for smooth, flowing landscape effect
            const freq = waveField.frequency;

            // Distance-based waves from two sources (interference pattern)
            const d1 = Math.sqrt(Math.pow(x - waveField.sourceLeftX, 2) + Math.pow(y - height/2, 2));
            const d2 = Math.sqrt(Math.pow(x - waveField.sourceRightX, 2) + Math.pow(y - height/2, 2));

            // Smooth, slow-moving waves
            const wave1 = Math.sin(d1 * freq - elapsed * waveField.speedBase) * waveField.ampBase;
            const wave2 = Math.sin(d2 * freq * 0.8 - elapsed * waveField.speedBase * 0.7) * waveField.ampBase * 0.6;

            // Gentle diagonal flow for landscape feel
            const wave3 = Math.sin((x * 0.003 + y * 0.003) + elapsed * waveField.speedBase * 0.4) * waveField.ampBase * 0.3;

            // Combine for X and Y displacement
            const dx = (wave1 + wave2) * 0.4;
            const dy = wave3;

            return { dx, dy };
        }

        // ================================================================
        // ENHANCED PARTICLE SYSTEM - Curl-like Motion
        // ================================================================
        const particles = [];
        const emergenceParticles = [];  // Special particles during emergence

        class Particle {
            constructor(x, y, color, type = 'error') {
                this.x = x;
                this.y = y;
                this.type = type;
                this.color = color;

                if (type === 'emergence') {
                    // Emergence particles: swirl toward target
                    this.vx = (Math.random() - 0.5) * 2;
                    this.vy = (Math.random() - 0.5) * 2;
                    this.size = 1 + Math.random() * 1.5;
                    this.alpha = 0.5 + Math.random() * 0.3;
                    this.life = 60 + Math.random() * 40;
                    this.friction = 0.98;
                } else {
                    // Error particles: rise like pollution with curl
                    this.vy = -0.15 - Math.random() * 0.25;
                    this.vx = (Math.random() - 0.5) * 0.1;
                    this.size = 1 + Math.random() * 2;
                    this.alpha = 0.3 + Math.random() * 0.4;
                    this.life = 200 + Math.random() * 150;
                    this.curlPhase = Math.random() * Math.PI * 2;
                    this.curlSpeed = 0.02 + Math.random() * 0.02;
                    this.curlAmplitude = 0.3 + Math.random() * 0.3;
                }
            }

            update(time) {
                if (this.type === 'emergence') {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.vx *= this.friction;
                    this.vy *= this.friction;
                    this.life--;
                    this.alpha = Math.max(0, this.alpha - 0.008);
                } else {
                    // Curl noise approximation for organic motion
                    this.curlPhase += this.curlSpeed;
                    this.vx = Math.sin(this.curlPhase) * this.curlAmplitude;
                    this.x += this.vx;
                    this.y += this.vy;
                    this.life--;
                    this.alpha = Math.max(0, this.alpha - 0.002);
                    this.size = Math.max(0.3, this.size - 0.003);
                }
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

        function spawnEmergenceParticles(x, y, count = 5) {
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(
                    x + (Math.random() - 0.5) * 20,
                    y + (Math.random() - 0.5) * 20,
                    COLORS.teal,
                    'emergence'
                ));
            }
        }

        function spawnErrorParticles(node) {
            if (node.status !== 'broken') return;
            const count = Math.min(Math.max(1, node.errors.length), 4);
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(
                    node.x + (Math.random() - 0.5) * 12,
                    node.y + (Math.random() - 0.5) * 4,
                    COLORS.broken,
                    'error'
                ));
            }
        }

        // ================================================================
        // DELAUNAY TRIANGULATION
        // ================================================================
        function distance(p0, p1) {
            return Math.sqrt(Math.pow(p1.x - p0.x, 2) + Math.pow(p1.y - p0.y, 2));
        }

        let edges = [];
        if (nodes.length >= 3) {
            const points = nodes.map(n => [n.x, n.y]);
            const delaunay = d3.Delaunay.from(points);
            const triangles = delaunay.triangles;

            for (let i = 0; i < triangles.length; i += 3) {
                const [i0, i1, i2] = [triangles[i], triangles[i+1], triangles[i+2]];
                const [p0, p1, p2] = [nodes[i0], nodes[i1], nodes[i2]];
                if (p0 && p1 && p2) {
                    edges.push(
                        { length: distance(p0, p1), i0, i1 },
                        { length: distance(p1, p2), i0: i1, i1: i2 },
                        { length: distance(p2, p0), i0: i2, i1: i0 }
                    );
                }
            }
        }

        // ================================================================
        // RENDERING
        // ================================================================
        function easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        }

        function easeOutElastic(t) {
            const c4 = (2 * Math.PI) / 3;
            return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
        }

        function renderEdges(minLength, color, alpha, useCurrentPositions = false) {
            if (edges.length === 0) return;
            ctx.globalAlpha = alpha * emergenceProgress;
            ctx.strokeStyle = color;
            ctx.lineWidth = 0.5;
            ctx.beginPath();

            for (const edge of edges) {
                if (edge.length < minLength) {
                    const p0 = useCurrentPositions ? nodeStates[edge.i0] : nodes[edge.i0];
                    const p1 = useCurrentPositions ? nodeStates[edge.i1] : nodes[edge.i1];
                    const x0 = useCurrentPositions ? p0.currentX : p0.x;
                    const y0 = useCurrentPositions ? p0.currentY : p0.y;
                    const x1 = useCurrentPositions ? p1.currentX : p1.x;
                    const y1 = useCurrentPositions ? p1.currentY : p1.y;
                    ctx.moveTo(x0, y0);
                    ctx.lineTo(x1, y1);
                }
            }
            ctx.stroke();
        }

        function render(time) {
            // Update emergence progress
            const elapsed = time - emergenceStartTime;
            emergenceProgress = Math.min(1, elapsed / emergenceDurationMs);
            const easedProgress = easeOutCubic(emergenceProgress);

            // Update phase indicator
            if (emergenceProgress >= 1 && !emerged) {
                emerged = true;
                container.classList.add('emerged');
                phaseEl.classList.add('emerged');
                phaseEl.textContent = 'emerged';
            } else if (!emerged) {
                if (emergenceProgress < 0.3) {
                    phaseEl.textContent = 'tuning...';
                } else if (emergenceProgress < 0.7) {
                    phaseEl.textContent = 'coalescing...';
                } else {
                    phaseEl.textContent = 'emerging...';
                }
            }

            // Update node positions during emergence with wave field distortion
            for (let i = 0; i < nodeStates.length; i++) {
                const state = nodeStates[i];
                const adjustedProgress = Math.max(0, Math.min(1, (easedProgress - state.delay) / (1 - state.delay)));

                // Wave distortion STRONGEST at beginning, fades as nodes settle
                // Smooth exponential decay for landscape morphing effect
                const waveStrength = Math.pow(1 - adjustedProgress, 2); // Strong early, gentle fade
                const wave = calcWaveDisplacement(state.targetX, state.targetY, elapsed);

                // Lerp from chaos to target with wave distortion
                const targetX = state.targetX + wave.dx * waveStrength;
                const targetY = state.targetY + wave.dy * waveStrength;

                state.currentX = state.currentX + (targetX - state.currentX) * adjustedProgress * 0.1;
                state.currentY = state.currentY + (targetY - state.currentY) * adjustedProgress * 0.1;
                state.currentAlpha = adjustedProgress;

                // Spawn emergence particles during coalescing (more during peak wave)
                if (!emerged && adjustedProgress > 0.1 && adjustedProgress < 0.9) {
                    const spawnChance = 0.02 + waveStrength * 0.03;
                    if (Math.random() < spawnChance) {
                        spawnEmergenceParticles(state.currentX, state.currentY, 2);
                    }
                }
            }

            // Clear
            ctx.fillStyle = COLORS.void;
            ctx.fillRect(0, 0, width, height);

            // ============================================================
            // GORGEOUS MESH RENDERING - Like the Paris cityscapes
            // ============================================================
            if (edges.length > 0) {
                const frameColor = emerged ? COLORS.gold : COLORS.teal;

                // Layer 1: Dense gradient base (the "city" silhouette)
                ctx.save();
                for (let i = 0; i < maxHeight; i++) {
                    ctx.translate(0, 0.5);  // Slightly larger steps for depth
                    // Exponential falloff for more realistic depth
                    const alpha = Math.pow(1 - i / maxHeight, 1.5) * 0.04;
                    // Edge threshold grows slower at bottom (denser base)
                    const threshold = Math.pow(i / maxHeight, 0.7) * maxHeight * 0.8;
                    renderEdges(threshold, frameColor, alpha, !emerged);
                }
                ctx.restore();

                // Layer 2: Mid-tone wireframe layers
                for (let i = 0; i < wireCount; i++) {
                    const t = i / wireCount;
                    ctx.save();
                    ctx.translate(0, maxHeight * (1 - t) * 0.3);
                    ctx.globalAlpha = 0.03 + 0.1 * t;
                    ctx.strokeStyle = frameColor;
                    ctx.lineWidth = 0.5;
                    renderEdges(15 + i * 15, frameColor, 0.03 + 0.1 * t, !emerged);
                    ctx.restore();
                }

                // Layer 3: Color gradient overlay (screen blend)
                ctx.save();
                ctx.globalCompositeOperation = 'screen';
                const gradient = ctx.createLinearGradient(0, height, 0, 0);
                if (emerged) {
                    gradient.addColorStop(0, 'rgba(212, 175, 55, 0.15)');  // Gold at bottom
                    gradient.addColorStop(0.5, 'rgba(184, 134, 11, 0.08)');
                    gradient.addColorStop(1, 'rgba(244, 196, 48, 0.03)');  // Saffron at top
                } else {
                    gradient.addColorStop(0, 'rgba(31, 189, 234, 0.15)');  // Teal at bottom
                    gradient.addColorStop(0.5, 'rgba(31, 189, 234, 0.06)');
                    gradient.addColorStop(1, 'rgba(157, 78, 221, 0.02)');  // Hint of purple at top
                }
                ctx.fillStyle = gradient;
                ctx.fillRect(0, 0, width, height);
                ctx.restore();

                // Layer 4: Bright wireframe highlights (the "glow")
                ctx.save();
                ctx.globalCompositeOperation = 'screen';
                ctx.strokeStyle = emerged ? '#fff' : COLORS.teal;
                ctx.lineWidth = 0.8;
                ctx.globalAlpha = 0.12;
                renderEdges(40, ctx.strokeStyle, 0.12, !emerged);

                // Layer 5: Soft glow blur
                ctx.filter = 'blur(3px)';
                ctx.globalAlpha = 0.15;
                ctx.strokeStyle = frameColor;
                ctx.lineWidth = 1.5;
                renderEdges(60, ctx.strokeStyle, 0.15, !emerged);
                ctx.filter = 'none';
                ctx.restore();
            }

            // Draw nodes
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const state = nodeStates[i];
                const color = COLORS[node.status];
                const baseRadius = 2 + Math.min(node.loc / 80, 6);

                // After emergence: subtle energy field displacement (NOT breathing)
                let x, y;
                if (emerged) {
                    const ambientWave = calcWaveDisplacement(node.x, node.y, elapsed);
                    x = node.x + ambientWave.dx * 0.15;  // Very subtle
                    y = node.y + ambientWave.dy * 0.15;
                } else {
                    x = state.currentX;
                    y = state.currentY;
                }
                const alpha = state.currentAlpha;

                // Outer glow for non-working
                if ((node.status === 'broken' || node.status === 'combat') && alpha > 0.5) {
                    ctx.save();
                    ctx.globalAlpha = 0.25 * alpha;
                    ctx.shadowColor = color;
                    ctx.shadowBlur = 15;
                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(x, y, baseRadius * 1.8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }

                // Core dot
                ctx.globalAlpha = 0.85 * alpha;
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(x, y, baseRadius, 0, Math.PI * 2);
                ctx.fill();

                // Inner highlight
                if (alpha > 0.7) {
                    ctx.globalAlpha = 0.4 * alpha;
                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(x - baseRadius * 0.25, y - baseRadius * 0.25, baseRadius * 0.25, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            // Update and draw particles
            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].update(time);
                particles[i].draw(ctx);
                if (particles[i].isDead()) {
                    particles.splice(i, 1);
                }
            }

            // Spawn error particles (only after emerged)
            if (emerged) {
                for (const node of nodes) {
                    if (node.status === 'broken' && Math.random() < 0.025) {
                        spawnErrorParticles(node);
                    }
                }
            }

            requestAnimationFrame(render);
        }

        // ================================================================
        // INTERACTION
        // ================================================================
        function findNodeAt(x, y) {
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const state = nodeStates[i];
                const nx = emerged ? node.x : state.currentX;
                const ny = emerged ? node.y : state.currentY;
                const dist = Math.sqrt(Math.pow(nx - x, 2) + Math.pow(ny - y, 2));
                const radius = 2 + Math.min(node.loc / 80, 6);
                if (dist < radius + 8) {
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
                const errorsHtml = node.errors.length
                    ? `<div class="errors">${node.errors.map(e => `<div class="error-item">• ${e}</div>`).join('')}</div>`
                    : '';

                tooltip.innerHTML = `
                    <div class="path">${node.path}</div>
                    <div class="meta">
                        <span class="status ${node.status}">${node.status}</span>
                        <span class="loc">${node.loc} lines</span>
                    </div>
                    ${errorsHtml}
                `;

                let tx = e.clientX + 15;
                let ty = e.clientY + 15;
                if (tx + 320 > window.innerWidth) tx = e.clientX - 325;
                if (ty + 200 > window.innerHeight) ty = e.clientY - 100;

                tooltip.style.left = tx + 'px';
                tooltip.style.top = ty + 'px';
                tooltip.classList.add('visible');
                canvas.style.cursor = 'pointer';
            } else {
                tooltip.classList.remove('visible');
                canvas.style.cursor = 'crosshair';
            }
        });

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const node = findNodeAt(x, y);

            if (node) {
                window.parent.postMessage({
                    type: 'WOVEN_MAPS_NODE_CLICK',
                    node: { path: node.path, status: node.status, loc: node.loc, errors: node.errors }
                }, '*');
                console.log('Node clicked:', node.path);
            }
        });

        canvas.addEventListener('mouseleave', () => {
            tooltip.classList.remove('visible');
        });

        // ================================================================
        // START
        // ================================================================
        requestAnimationFrame(render);
        console.log('Woven Maps Enhanced initialized:', nodes.length, 'nodes');
    </script>
</body>
</html>'''


# =============================================================================
# MARIMO INTEGRATION
# =============================================================================

def create_code_city(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
) -> Any:
    """Create a Woven Maps Code City visualization for Marimo."""
    try:
        import marimo as mo
    except ImportError:
        raise ImportError("marimo is required. Install with: pip install marimo")

    if not root or not os.path.isdir(root):
        return mo.md(f"**Set a valid project root to visualize the codebase.**\n\nCurrent: `{root or 'None'}`")

    graph_data = build_graph_data(root, width, height, max_height, wire_count)

    if not graph_data.nodes:
        return mo.md(f"**No code files found in project.**\n\nScanned: `{root}`")

    iframe_html = WOVEN_MAPS_TEMPLATE.replace('__GRAPH_DATA__', graph_data.to_json())
    escaped = html.escape(iframe_html)

    return mo.Html(f'''
        <div style="
            background: #0A0A0B;
            border-radius: 8px;
            overflow: hidden;
        ">
            <iframe
                srcdoc="{escaped}"
                width="{width}"
                height="{height}"
                style="border: none; display: block;"
                sandbox="allow-scripts"
            ></iframe>
        </div>
    ''')


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python woven_maps.py <directory>")
        sys.exit(1)

    data = build_graph_data(sys.argv[1])
    print(f"Scanned {len(data.nodes)} files")
    print(f"Working: {sum(1 for n in data.nodes if n.status == 'working')}")
    print(f"Broken: {sum(1 for n in data.nodes if n.status == 'broken')}")

"""
Woven Maps Code City Visualization
===================================

A complete implementation of Nicolas Barradeau's "Woven Maps" algorithm
adapted for codebase visualization in Marimo.

Usage:
    from IP.woven_maps import create_code_city, build_graph_data

    # In a Marimo plugin:
    def render(STATE_MANAGERS):
        get_root, _ = STATE_MANAGERS["root"]
        return create_code_city(get_root(), width=800, height=600)

Source: https://barradeau.com/blog/?p=1001
Colors: MaestroView.vue (stereOS)
"""

from __future__ import annotations

import json
import html
import math
import os
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# =============================================================================
# COLOR CONSTANTS - EXACT, NO EXCEPTIONS
# =============================================================================

COLORS = {
    "gold_metallic": "#D4AF37",   # Working code
    "blue_dominant": "#1fbdea",   # Broken code
    "purple_combat": "#9D4EDD",   # Combat (LLM active)
    "bg_primary": "#0A0A0B",      # The Void
    "bg_elevated": "#121214",     # Elevated surfaces
    "gold_dark": "#B8860B",       # Secondary gold
    "gold_saffron": "#F4C430",    # Bright highlights
}

# JavaScript-friendly color map
JS_COLORS = {
    "void": "#0A0A0B",
    "working": "#D4AF37",
    "broken": "#1fbdea",
    "combat": "#9D4EDD",
    "wireframe": "#333333",
}

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CodeNode:
    """Represents a file in the codebase."""
    path: str
    status: str = "working"  # 'working' | 'broken' | 'combat'
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
    max_height: int = 200
    wire_count: int = 10
    show_particles: bool = True
    show_tooltip: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "maxHeight": self.max_height,
            "wireCount": self.wire_count,
            "showParticles": self.show_particles,
            "showTooltip": self.show_tooltip,
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

# Directories to skip during scanning
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'dist', 'build',
    '.venv', 'venv', 'env', '.env', '.tox', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'coverage', '.coverage',
    'htmlcov', '.idea', '.vscode', 'target', 'out', 'bin',
}

# File extensions to include
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
    """
    Scan a codebase and return a list of CodeNodes.

    Args:
        root: Root directory to scan
        skip_dirs: Directories to skip (defaults to SKIP_DIRS)
        extensions: File extensions to include (defaults to CODE_EXTENSIONS)

    Returns:
        List of CodeNode objects
    """
    skip = skip_dirs or SKIP_DIRS
    exts = extensions or CODE_EXTENSIONS
    nodes = []

    root_path = Path(root).resolve()

    if not root_path.exists():
        return nodes

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out skip directories
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
                # File couldn't be read - mark as broken
                nodes.append(CodeNode(
                    path=relpath,
                    status="broken",
                    loc=0,
                    errors=[f"Read error: {str(e)}"],
                ))

    return nodes


def analyze_file(filepath: Path, relpath: str) -> CodeNode:
    """
    Analyze a single file for status and metrics.

    Args:
        filepath: Absolute path to file
        relpath: Relative path for display

    Returns:
        CodeNode with analysis results
    """
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return CodeNode(
            path=relpath,
            status="broken",
            errors=[str(e)],
        )

    lines = content.split('\n')
    loc = len(lines)

    # Detect potential issues
    errors = []

    # TODO/FIXME detection
    todo_pattern = re.compile(r'\b(TODO|FIXME|XXX|HACK|BUG)\b', re.IGNORECASE)
    for i, line in enumerate(lines[:500], 1):  # Check first 500 lines
        if todo_pattern.search(line):
            match = todo_pattern.search(line)
            errors.append(f"Line {i}: {match.group(0)} found")
            if len(errors) >= 5:  # Limit errors per file
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

    # Determine status
    status = "broken" if errors else "working"

    return CodeNode(
        path=relpath,
        status=status,
        loc=loc,
        errors=errors[:10],  # Limit to 10 errors
    )


# =============================================================================
# LAYOUT CALCULATION
# =============================================================================

def calculate_layout(
    nodes: List[CodeNode],
    width: int,
    height: int,
    padding: int = 60,
) -> List[CodeNode]:
    """
    Calculate 2D positions for nodes based on directory structure.

    Uses a radial layout where:
    - Directories are arranged in a grid
    - Files within a directory are arranged radially
    - Larger files are positioned further from center

    Args:
        nodes: List of CodeNodes to position
        width: Canvas width
        height: Canvas height
        padding: Edge padding

    Returns:
        Same nodes with x, y coordinates set
    """
    if not nodes:
        return nodes

    # Group nodes by directory
    dirs: Dict[str, List[CodeNode]] = {}
    for node in nodes:
        dir_path = str(Path(node.path).parent)
        if dir_path == '.':
            dir_path = 'root'
        if dir_path not in dirs:
            dirs[dir_path] = []
        dirs[dir_path].append(node)

    # Calculate grid dimensions
    dir_count = len(dirs)
    cols = max(1, int(math.ceil(math.sqrt(dir_count))))
    rows = max(1, int(math.ceil(dir_count / cols)))

    # Usable area
    usable_width = width - padding * 2
    usable_height = height - padding * 2

    # Cell dimensions
    cell_width = usable_width / cols
    cell_height = usable_height / rows

    # Position each directory's files
    for i, (dir_path, dir_nodes) in enumerate(dirs.items()):
        # Grid position
        col = i % cols
        row = i // cols

        # Center of this cell
        center_x = padding + col * cell_width + cell_width / 2
        center_y = padding + row * cell_height + cell_height / 2

        # Position files radially within cell
        file_count = len(dir_nodes)
        max_radius = min(cell_width, cell_height) / 2 - 20

        for j, node in enumerate(dir_nodes):
            if file_count == 1:
                # Single file - place at center
                node.x = center_x
                node.y = center_y
            else:
                # Multiple files - arrange radially
                angle = (j / file_count) * 2 * math.pi - math.pi / 2

                # Radius based on file size (larger files further out)
                size_factor = min(1.0, node.loc / 500)  # Normalize by 500 LOC
                radius = 20 + size_factor * (max_radius - 20)

                # Add some jitter for visual interest
                jitter_x = (hash(node.path) % 21 - 10)
                jitter_y = (hash(node.path + 'y') % 21 - 10)

                node.x = center_x + math.cos(angle) * radius + jitter_x
                node.y = center_y + math.sin(angle) * radius + jitter_y

        # Ensure nodes stay within bounds
        for node in dir_nodes:
            node.x = max(padding, min(width - padding, node.x))
            node.y = max(padding, min(height - padding, node.y))

    return nodes


# =============================================================================
# GRAPH DATA BUILDER
# =============================================================================

def build_graph_data(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
) -> GraphData:
    """
    Build complete graph data from a codebase root.

    Args:
        root: Root directory to scan
        width: Canvas width
        height: Canvas height
        max_height: Max gradient height (cityscape effect)
        wire_count: Number of wireframe layers

    Returns:
        GraphData ready for visualization
    """
    # Scan codebase
    nodes = scan_codebase(root)

    # Calculate layout
    nodes = calculate_layout(nodes, width, height)

    # Build config
    config = GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )

    return GraphData(nodes=nodes, config=config)


# =============================================================================
# IFRAME TEMPLATE
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
        canvas { display: block; cursor: crosshair; }
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
        #tooltip .path {
            color: #D4AF37;
            font-weight: 600;
            word-break: break-all;
            margin-bottom: 4px;
        }
        #tooltip .meta {
            display: flex;
            gap: 12px;
            margin-bottom: 4px;
        }
        #tooltip .status {
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        #tooltip .status.working { background: rgba(212, 175, 55, 0.2); color: #D4AF37; }
        #tooltip .status.broken { background: rgba(31, 189, 234, 0.2); color: #1fbdea; }
        #tooltip .status.combat { background: rgba(157, 78, 221, 0.2); color: #9D4EDD; }
        #tooltip .loc { color: #888; }
        #tooltip .errors {
            margin-top: 6px;
            padding-top: 6px;
            border-top: 1px solid #333;
            color: #1fbdea;
            font-size: 10px;
            line-height: 1.4;
        }
        #tooltip .error-item { margin: 2px 0; }
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
    <canvas id="city"></canvas>
    <div id="tooltip"></div>
    <div id="stats"></div>

    <script>
        // ================================================================
        // DATA INJECTION
        // ================================================================
        const GRAPH_DATA = __GRAPH_DATA__;

        // ================================================================
        // CONSTANTS
        // ================================================================
        const COLORS = {
            void: '#0A0A0B',
            working: '#D4AF37',
            broken: '#1fbdea',
            combat: '#9D4EDD',
            wireframe: '#2a2a2a'
        };

        // ================================================================
        // SETUP
        // ================================================================
        const canvas = document.getElementById('city');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const stats = document.getElementById('stats');

        const { nodes, config } = GRAPH_DATA;
        const { width, height, maxHeight, wireCount } = config;

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
            <span>${nodes.length} total files</span>
        `;

        // ================================================================
        // PARTICLE SYSTEM
        // ================================================================
        const particles = [];

        class Particle {
            constructor(x, y, color) {
                this.x = x;
                this.y = y;
                this.vy = -0.2 - Math.random() * 0.4;
                this.vx = (Math.random() - 0.5) * 0.15;
                this.size = 1 + Math.random() * 2;
                this.alpha = 0.3 + Math.random() * 0.4;
                this.color = color;
                this.life = 200 + Math.random() * 150;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life--;
                this.alpha = Math.max(0, this.alpha - 0.002);
                this.size = Math.max(0.3, this.size - 0.005);
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
            const count = Math.min(Math.max(1, node.errors.length), 4);
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(
                    node.x + (Math.random() - 0.5) * 12,
                    node.y + (Math.random() - 0.5) * 4,
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

        // ================================================================
        // DELAUNAY TRIANGULATION
        // ================================================================
        function distance(p0, p1) {
            const dx = p1.x - p0.x;
            const dy = p1.y - p0.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        // Build triangulation (only if we have enough points)
        let edges = [];
        if (nodes.length >= 3) {
            const points = nodes.map(n => [n.x, n.y]);
            const delaunay = d3.Delaunay.from(points);
            const triangles = delaunay.triangles;

            for (let i = 0; i < triangles.length; i += 3) {
                const i0 = triangles[i];
                const i1 = triangles[i + 1];
                const i2 = triangles[i + 2];

                const p0 = nodes[i0];
                const p1 = nodes[i1];
                const p2 = nodes[i2];

                if (p0 && p1 && p2) {
                    edges.push(
                        { length: distance(p0, p1), p0, p1 },
                        { length: distance(p1, p2), p0: p1, p1: p2 },
                        { length: distance(p2, p0), p0: p2, p1: p0 }
                    );
                }
            }
        }

        // ================================================================
        // RENDERING
        // ================================================================
        function renderEdges(minLength, color, alpha) {
            if (edges.length === 0) return;

            ctx.globalAlpha = alpha;
            ctx.strokeStyle = color;
            ctx.lineWidth = 0.5;
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
            // Clear to void
            ctx.fillStyle = COLORS.void;
            ctx.fillRect(0, 0, width, height);

            // Draw gradient layers (the cityscape magic)
            if (edges.length > 0) {
                ctx.save();
                for (let i = 0; i < maxHeight; i++) {
                    ctx.translate(0, 0.4);
                    const alpha = (1 - i / maxHeight) * 0.03;
                    renderEdges(i * 0.6, COLORS.working, alpha);
                }
                ctx.restore();

                // Wireframe overlays
                for (let i = 0; i < wireCount; i++) {
                    const t = i / wireCount;
                    ctx.save();
                    ctx.translate(0, maxHeight * (1 - t) * 0.25);
                    renderEdges(i * 18, COLORS.working, 0.02 + 0.08 * t);
                    ctx.restore();
                }
            }

            // Draw nodes
            ctx.globalAlpha = 1;
            for (const node of nodes) {
                const color = COLORS[node.status];
                const baseRadius = 2 + Math.min(node.loc / 80, 6);

                // Outer glow for non-working
                if (node.status === 'broken' || node.status === 'combat') {
                    ctx.save();
                    ctx.globalAlpha = 0.25;
                    ctx.shadowColor = color;
                    ctx.shadowBlur = 15;
                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, baseRadius * 1.8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }

                // Core dot
                ctx.globalAlpha = 0.85;
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(node.x, node.y, baseRadius, 0, Math.PI * 2);
                ctx.fill();

                // Inner highlight
                ctx.globalAlpha = 0.4;
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(
                    node.x - baseRadius * 0.25,
                    node.y - baseRadius * 0.25,
                    baseRadius * 0.25,
                    0, Math.PI * 2
                );
                ctx.fill();
            }

            // Particles
            updateParticles();

            // Spawn new particles (randomly for broken nodes)
            for (const node of nodes) {
                if (node.status === 'broken' && Math.random() < 0.03) {
                    spawnParticles(node);
                }
            }

            requestAnimationFrame(render);
        }

        // ================================================================
        // INTERACTION
        // ================================================================
        function findNodeAt(x, y) {
            for (const node of nodes) {
                const dx = node.x - x;
                const dy = node.y - y;
                const dist = Math.sqrt(dx * dx + dy * dy);
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

                // Position tooltip
                let tx = e.clientX + 15;
                let ty = e.clientY + 15;

                // Keep on screen
                const tooltipRect = tooltip.getBoundingClientRect();
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
                // Send message to parent window (Marimo)
                window.parent.postMessage({
                    type: 'WOVEN_MAPS_NODE_CLICK',
                    node: {
                        path: node.path,
                        status: node.status,
                        loc: node.loc,
                        errors: node.errors
                    }
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
        render();
        console.log('Woven Maps initialized:', nodes.length, 'nodes');
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
    """
    Create a Woven Maps Code City visualization for Marimo.

    Args:
        root: Root directory of the codebase to visualize
        width: Canvas width in pixels
        height: Canvas height in pixels
        max_height: Maximum gradient height (affects cityscape depth)
        wire_count: Number of wireframe overlay layers

    Returns:
        mo.Html element containing the visualization iframe

    Example:
        >>> import marimo as mo
        >>> from IP.woven_maps import create_code_city
        >>>
        >>> @app.cell
        >>> def city_view():
        >>>     return create_code_city("/path/to/project", width=900, height=600)
    """
    try:
        import marimo as mo
    except ImportError:
        raise ImportError("marimo is required. Install with: pip install marimo")

    # Validate root
    if not root or not os.path.isdir(root):
        return mo.md(f"""
        **Set a valid project root to visualize the codebase.**

        Current value: `{root or 'None'}`
        """)

    # Build graph data
    graph_data = build_graph_data(root, width, height, max_height, wire_count)

    if not graph_data.nodes:
        return mo.md(f"""
        **No code files found in project.**

        Scanned: `{root}`

        Supported extensions: {', '.join(sorted(CODE_EXTENSIONS))}
        """)

    # Inject data into template
    iframe_html = WOVEN_MAPS_TEMPLATE.replace(
        '__GRAPH_DATA__',
        graph_data.to_json()
    )

    # Escape for srcdoc attribute
    escaped = html.escape(iframe_html)

    # Stats for header
    working = sum(1 for n in graph_data.nodes if n.status == 'working')
    broken = sum(1 for n in graph_data.nodes if n.status == 'broken')
    combat = sum(1 for n in graph_data.nodes if n.status == 'combat')

    return mo.Html(f'''
        <div style="
            background: #0A0A0B;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(212, 175, 55, 0.15);
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


def create_code_city_with_controls(STATE_MANAGERS: dict) -> Any:
    """
    Create Code City with Marimo UI controls.

    Integrates with STATE_MANAGERS pattern for plugin compatibility.

    Args:
        STATE_MANAGERS: Dict of (getter, setter) tuples

    Returns:
        mo.vstack with controls and visualization
    """
    try:
        import marimo as mo
    except ImportError:
        raise ImportError("marimo required")

    get_root, set_root = STATE_MANAGERS.get("root", (lambda: None, lambda x: None))
    root = get_root()

    # Controls
    width_slider = mo.ui.slider(400, 1200, value=800, step=50, label="Width")
    height_slider = mo.ui.slider(300, 800, value=600, step=50, label="Height")
    refresh_btn = mo.ui.button(label="Refresh", on_change=lambda _: None)

    controls = mo.hstack([
        width_slider,
        height_slider,
        refresh_btn,
    ], gap="1rem")

    # Visualization
    city = create_code_city(
        root,
        width=width_slider.value,
        height=height_slider.value,
    )

    return mo.vstack([controls, city], gap="1rem")


# =============================================================================
# CLI FOR TESTING
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python woven_maps.py <directory>")
        print("\nGenerates graph data JSON for the given directory.")
        sys.exit(1)

    root = sys.argv[1]
    data = build_graph_data(root)

    print(f"Scanned {len(data.nodes)} files")
    print(f"Working: {sum(1 for n in data.nodes if n.status == 'working')}")
    print(f"Broken: {sum(1 for n in data.nodes if n.status == 'broken')}")
    print()
    print("JSON output:")
    print(data.to_json())

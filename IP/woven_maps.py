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
    status: str = "working"   # working | broken | combat
    loc: int = 0
    errors: List[str] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    # Extended fields for ConnectionGraph integration
    node_type: str = "file"   # file|component|store|entry|test|route|api|config|type
    centrality: float = 0.0   # PageRank score (0-1) for sizing
    in_cycle: bool = False    # Part of circular dependency
    depth: int = 0            # Distance from entry points
    incoming_count: int = 0   # Files that import this
    outgoing_count: int = 0   # Files this imports

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.path,
            "path": self.path,
            "status": self.status,
            "x": self.x,
            "y": self.y,
            "loc": self.loc,
            "errors": self.errors,
            "nodeType": self.node_type,
            "centrality": self.centrality,
            "inCycle": self.in_cycle,
            "depth": self.depth,
            "incomingCount": self.incoming_count,
            "outgoingCount": self.outgoing_count,
        }


@dataclass
class EdgeData:
    """Represents an import relationship between files."""
    source: str              # Source file path (importer)
    target: str              # Target file path (imported)
    resolved: bool = True    # Whether the import resolves
    bidirectional: bool = False  # Mutual imports
    line_number: int = 0     # Source line of import

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "resolved": self.resolved,
            "bidirectional": self.bidirectional,
            "lineNumber": self.line_number,
        }


@dataclass
class ColorScheme:
    """Color configuration for Woven Maps - matches stereOS three-state system."""
    working: str = "#D4AF37"    # Gold - all imports resolve
    broken: str = "#1fbdea"     # Blue/Teal - has errors
    combat: str = "#9D4EDD"     # Purple - LLM deployed
    void: str = "#0A0A0B"       # Background
    surface: str = "#121214"    # Elevated surfaces

    # Frame colors (teal during scan, gold when complete)
    frame_scanning: str = "#1fbdea"
    frame_complete: str = "#D4AF37"

    def to_dict(self) -> Dict[str, str]:
        return {
            "working": self.working,
            "broken": self.broken,
            "combat": self.combat,
            "void": self.void,
            "surface": self.surface,
            "frameScanning": self.frame_scanning,
            "frameComplete": self.frame_complete,
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
    colors: ColorScheme = field(default_factory=ColorScheme)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "maxHeight": self.max_height,
            "wireCount": self.wire_count,
            "showParticles": self.show_particles,
            "showTooltip": self.show_tooltip,
            "emergenceDuration": self.emergence_duration,
            "colors": self.colors.to_dict(),
        }


@dataclass
class GraphData:
    """Complete data structure for visualization."""
    nodes: List[CodeNode] = field(default_factory=list)
    edges: List[EdgeData] = field(default_factory=list)
    config: GraphConfig = field(default_factory=GraphConfig)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
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

    # Check combat status - files with active LLM deployments get purple
    try:
        from IP.combat_tracker import CombatTracker
        tracker = CombatTracker(root)
        combat_files = tracker.get_combat_files()
        for node in nodes:
            if node.path in combat_files:
                node.status = "combat"  # Purple in visualization
    except ImportError:
        pass  # CombatTracker not available

    config = GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )
    return GraphData(nodes=nodes, config=config)


def build_from_connection_graph(
    project_root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 250,
    wire_count: int = 15,
) -> GraphData:
    """
    Build GraphData from ConnectionGraph with real import relationships.

    This provides:
    - Real import edges (not just Delaunay triangulation)
    - Node types (component, store, entry, test, etc.)
    - Centrality-based sizing
    - Cycle detection
    - Depth from entry points
    """
    # Import here to avoid circular dependency
    try:
        from IP.connection_verifier import build_connection_graph
    except ImportError:
        # Fallback for standalone use
        from connection_verifier import build_connection_graph

    # Build the full connection graph with all analysis
    conn_graph = build_connection_graph(project_root)
    graph_dict = conn_graph.to_dict()

    # Convert ConnectionGraph nodes to CodeNodes
    nodes = []
    node_lookup = {}

    for node_data in graph_dict["nodes"]:
        metrics = node_data.get("metrics", {})

        # Map status: error → broken, normal → working
        status = "working"
        if node_data.get("status") == "error":
            status = "broken"
        elif metrics.get("issueCount", 0) > 0:
            status = "broken"

        code_node = CodeNode(
            path=node_data["filePath"],
            status=status,
            loc=100,  # Will be calculated during layout
            errors=[],  # Could extract from connection graph
            node_type=node_data.get("type", "file"),
            centrality=metrics.get("centrality", 0.0),
            in_cycle=metrics.get("inCycle", False),
            depth=metrics.get("depth", 0),
            incoming_count=metrics.get("incomingCount", 0),
            outgoing_count=metrics.get("outgoingCount", 0),
        )
        nodes.append(code_node)
        node_lookup[code_node.path] = code_node

    # Apply layout
    nodes = calculate_layout(nodes, width, height)

    # Check combat status - files with active LLM deployments get purple
    try:
        from IP.combat_tracker import CombatTracker
        tracker = CombatTracker(project_root)
        combat_files = tracker.get_combat_files()
        for node in nodes:
            if node.path in combat_files:
                node.status = "combat"  # Purple in visualization
    except ImportError:
        pass  # CombatTracker not available

    # Convert edges
    edges = []
    for edge_data in graph_dict["edges"]:
        # Only include edges where both source and target exist in our nodes
        if edge_data["source"] in node_lookup and edge_data["target"] in node_lookup:
            edges.append(EdgeData(
                source=edge_data["source"],
                target=edge_data["target"],
                resolved=edge_data.get("resolved", True),
                bidirectional=edge_data.get("bidirectional", False),
                line_number=edge_data.get("lineNumber", 0),
            ))

    config = GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )

    return GraphData(nodes=nodes, edges=edges, config=config)


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

        /* Control Panel */
        #controls {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(18, 18, 20, 0.9);
            border: 1px solid rgba(31, 189, 234, 0.3);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 10px;
            color: #888;
            max-width: 180px;
            transition: opacity 0.2s, border-color 0.3s;
        }
        #controls:hover { border-color: rgba(212, 175, 55, 0.5); }
        #controls.collapsed { padding: 6px 10px; }
        #controls.collapsed .ctrl-body { display: none; }

        .ctrl-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            cursor: pointer;
        }
        .ctrl-title {
            color: #D4AF37;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .ctrl-toggle {
            color: #666;
            font-size: 12px;
        }

        .ctrl-section {
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .ctrl-section:last-child { border-bottom: none; margin-bottom: 0; }

        .ctrl-label {
            display: block;
            margin-bottom: 4px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .ctrl-row {
            display: flex;
            gap: 4px;
            margin-bottom: 6px;
        }

        .ctrl-btn {
            flex: 1;
            padding: 5px 8px;
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 3px;
            color: #888;
            font-family: inherit;
            font-size: 9px;
            cursor: pointer;
            transition: all 0.15s;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .ctrl-btn:hover { border-color: rgba(255,255,255,0.4); color: #fff; }
        .ctrl-btn.active { border-color: #D4AF37; color: #D4AF37; background: rgba(212,175,55,0.1); }
        .ctrl-btn.gold { border-color: #D4AF37; color: #D4AF37; }
        .ctrl-btn.gold.active { background: rgba(212,175,55,0.2); }
        .ctrl-btn.blue { border-color: #1fbdea; color: #1fbdea; }
        .ctrl-btn.blue.active { background: rgba(31,189,234,0.2); }
        .ctrl-btn.purple { border-color: #9D4EDD; color: #9D4EDD; }
        .ctrl-btn.purple.active { background: rgba(157,78,221,0.2); }

        .ctrl-slider {
            width: 100%;
            height: 4px;
            -webkit-appearance: none;
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
            outline: none;
        }
        .ctrl-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 12px;
            height: 12px;
            background: #D4AF37;
            border-radius: 50%;
            cursor: pointer;
        }

        .ctrl-value {
            display: inline-block;
            min-width: 30px;
            text-align: right;
            color: #D4AF37;
            font-family: monospace;
        }

        /* Keyframe buttons */
        .ctrl-btn.kf {
            width: 28px;
            height: 28px;
            padding: 0;
            font-weight: 600;
            font-size: 11px;
            transition: all 0.2s;
        }
        .ctrl-btn.kf.saved {
            border-color: #D4AF37;
            color: #D4AF37;
            box-shadow: 0 0 6px rgba(212, 175, 55, 0.3);
        }
        .ctrl-btn.kf.active {
            background: rgba(212, 175, 55, 0.3);
            transform: scale(1.1);
        }
        .ctrl-btn.kf.morphing {
            animation: kf-pulse 0.5s ease-in-out infinite;
        }
        @keyframes kf-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Audio Controls */
        .audio-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            width: 100%;
            padding: 6px;
            border: 1px solid rgba(157, 78, 221, 0.4);
            background: transparent;
            border-radius: 4px;
            color: #9D4EDD;
            cursor: pointer;
            transition: all 0.2s;
        }
        .audio-btn:hover {
            border-color: #9D4EDD;
            background: rgba(157, 78, 221, 0.1);
        }
        .audio-btn.active {
            border-color: #D4AF37;
            color: #D4AF37;
            background: rgba(212, 175, 55, 0.15);
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
        }
        .audio-btn.active::before {
            content: '';
            width: 8px;
            height: 8px;
            background: #D4AF37;
            border-radius: 50%;
            animation: audio-pulse 1s ease-in-out infinite;
        }
        @keyframes audio-pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.8); }
        }

        /* Frequency Bars */
        .freq-display {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            height: 24px;
            margin-top: 6px;
            padding: 0 2px;
            background: rgba(0,0,0,0.3);
            border-radius: 3px;
        }
        .freq-bar {
            width: 18%;
            min-height: 2px;
            background: linear-gradient(to top, #1fbdea, #9D4EDD);
            border-radius: 1px;
            transition: height 0.05s ease-out;
        }
        .freq-bar.low { background: linear-gradient(to top, #1fbdea, #1fbdea); }
        .freq-bar.mid { background: linear-gradient(to top, #9D4EDD, #9D4EDD); }
        .freq-bar.high { background: linear-gradient(to top, #D4AF37, #D4AF37); }
    </style>
</head>
<body>
    <div id="canvas-container">
        <canvas id="city"></canvas>
        <div id="phase">tuning...</div>
    </div>
    <div id="tooltip"></div>
    <div id="stats"></div>

    <!-- Control Panel -->
    <div id="controls">
        <div class="ctrl-header" onclick="toggleControls()">
            <span class="ctrl-title">Controls</span>
            <span class="ctrl-toggle">▼</span>
        </div>
        <div class="ctrl-body">
            <!-- Color Mode -->
            <div class="ctrl-section">
                <span class="ctrl-label">Frame Color</span>
                <div class="ctrl-row">
                    <button class="ctrl-btn gold active" onclick="setFrameColor('gold')">Gold</button>
                    <button class="ctrl-btn blue" onclick="setFrameColor('teal')">Teal</button>
                    <button class="ctrl-btn purple" onclick="setFrameColor('combat')">Purple</button>
                </div>
            </div>

            <!-- Wave Controls -->
            <div class="ctrl-section">
                <span class="ctrl-label">Wave Amplitude</span>
                <input type="range" class="ctrl-slider" id="waveAmp" min="0" max="50" value="20" oninput="updateWave()">
                <span class="ctrl-label">Wave Speed</span>
                <input type="range" class="ctrl-slider" id="waveSpeed" min="0" max="20" value="8" oninput="updateWave()">
            </div>

            <!-- Particles -->
            <div class="ctrl-section">
                <span class="ctrl-label">Particle Density</span>
                <input type="range" class="ctrl-slider" id="particleDensity" min="0" max="100" value="25" oninput="updateParticles()">
            </div>

            <!-- Keyframes -->
            <div class="ctrl-section">
                <span class="ctrl-label">Keyframes</span>
                <div class="ctrl-row">
                    <button class="ctrl-btn kf" id="kf1" onclick="loadKeyframe(0)" ondblclick="saveKeyframe(0)">1</button>
                    <button class="ctrl-btn kf" id="kf2" onclick="loadKeyframe(1)" ondblclick="saveKeyframe(1)">2</button>
                    <button class="ctrl-btn kf" id="kf3" onclick="loadKeyframe(2)" ondblclick="saveKeyframe(2)">3</button>
                    <button class="ctrl-btn kf" id="kf4" onclick="loadKeyframe(3)" ondblclick="saveKeyframe(3)">4</button>
                </div>
                <div class="ctrl-row" style="margin-top: 4px;">
                    <span style="font-size: 8px; color: #555;">click=load, dblclick=save</span>
                </div>
            </div>

            <!-- Morph Speed -->
            <div class="ctrl-section">
                <span class="ctrl-label">Morph Speed</span>
                <input type="range" class="ctrl-slider" id="morphSpeed" min="1" max="50" value="20">
            </div>

            <!-- Audio Reactive -->
            <div class="ctrl-section">
                <span class="ctrl-label">Audio Reactive</span>
                <button class="audio-btn" id="audioToggle" onclick="toggleAudio()">
                    <span>Enable Microphone</span>
                </button>
                <div class="freq-display" id="freqDisplay">
                    <div class="freq-bar low" id="freqLow"></div>
                    <div class="freq-bar low" id="freqLow2"></div>
                    <div class="freq-bar mid" id="freqMid"></div>
                    <div class="freq-bar mid" id="freqMid2"></div>
                    <div class="freq-bar high" id="freqHigh"></div>
                </div>
                <span class="ctrl-label" style="margin-top: 8px;">Sensitivity</span>
                <input type="range" class="ctrl-slider" id="audioSensitivity" min="1" max="100" value="50">
            </div>

            <!-- Actions -->
            <div class="ctrl-section">
                <div class="ctrl-row">
                    <button class="ctrl-btn" onclick="reEmergence()">Re-Emerge</button>
                    <button class="ctrl-btn" onclick="clearParticles()">Clear</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ================================================================
        // DATA & CONFIG
        // ================================================================
        const GRAPH_DATA = __GRAPH_DATA__;
        const { nodes, edges = [], config } = GRAPH_DATA;
        const { width, height, maxHeight, wireCount, emergenceDuration = 2.0 } = config;

        const COLORS = {
            void: '#0A0A0B',
            working: '#D4AF37',
            broken: '#1fbdea',
            combat: '#9D4EDD',
            wireframe: '#2a2a2a',
            teal: '#1fbdea',
            gold: '#D4AF37',
            cycle: '#ff4444',       // Red for cycle highlighting
            edge: '#333333',        // Default edge color
            edgeBroken: '#ff6b6b'   // Broken import edge
        };

        // Node type shape definitions
        const NODE_SHAPES = {
            file: 'circle',
            component: 'diamond',
            store: 'hexagon',
            entry: 'star',
            test: 'triangle',
            route: 'pentagon',
            api: 'triangle',
            config: 'square',
            type: 'circle'
        };

        // Build node lookup for edge rendering
        const nodeById = {};
        nodes.forEach(n => { nodeById[n.id] = n; });

        // ================================================================
        // CONTROL PANEL STATE
        // ================================================================
        let activeFrameColor = 'gold';  // 'gold' | 'teal' | 'combat'
        let particleDensityMultiplier = 1.0;

        // ================================================================
        // KEYFRAME SYSTEM
        // ================================================================
        const keyframes = [null, null, null, null];  // 4 slots
        let currentKeyframe = -1;
        let morphTarget = null;
        let morphProgress = 0;
        let morphStartState = null;

        function captureState() {
            return {
                frameColor: activeFrameColor,
                waveAmp: parseFloat(document.getElementById('waveAmp').value),
                waveSpeed: parseFloat(document.getElementById('waveSpeed').value),
                particleDensity: parseFloat(document.getElementById('particleDensity').value),
                // Store RGB values for smooth morphing
                frameColorRGB: hexToRgb(getFrameColor())
            };
        }

        function hexToRgb(hex) {
            const result = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : { r: 212, g: 175, b: 55 };
        }

        function rgbToHex(r, g, b) {
            return '#' + [r, g, b].map(x => {
                const hex = Math.round(x).toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }).join('');
        }

        function lerpValue(a, b, t) {
            return a + (b - a) * t;
        }

        function saveKeyframe(slot) {
            keyframes[slot] = captureState();
            document.getElementById('kf' + (slot + 1)).classList.add('saved');
            console.log('Saved keyframe', slot + 1, keyframes[slot]);
        }

        function loadKeyframe(slot) {
            if (!keyframes[slot]) return;

            const morphSpeed = parseFloat(document.getElementById('morphSpeed').value) / 100;

            // Start morphing
            morphStartState = captureState();
            morphTarget = keyframes[slot];
            morphProgress = 0;
            currentKeyframe = slot;

            // Update UI
            document.querySelectorAll('.ctrl-btn.kf').forEach((btn, i) => {
                btn.classList.remove('active', 'morphing');
                if (i === slot) btn.classList.add('morphing');
            });
        }

        function updateMorph() {
            if (!morphTarget || morphProgress >= 1) {
                if (morphTarget && morphProgress >= 1) {
                    // Morphing complete
                    document.querySelectorAll('.ctrl-btn.kf').forEach((btn, i) => {
                        btn.classList.remove('morphing');
                        if (i === currentKeyframe) btn.classList.add('active');
                    });
                    morphTarget = null;
                }
                return;
            }

            const morphSpeed = parseFloat(document.getElementById('morphSpeed').value) / 500;
            morphProgress = Math.min(1, morphProgress + morphSpeed);

            // Ease function (smooth)
            const t = 1 - Math.pow(1 - morphProgress, 3);

            // Interpolate all values
            const amp = lerpValue(morphStartState.waveAmp, morphTarget.waveAmp, t);
            const speed = lerpValue(morphStartState.waveSpeed, morphTarget.waveSpeed, t);
            const density = lerpValue(morphStartState.particleDensity, morphTarget.particleDensity, t);

            // Update sliders
            document.getElementById('waveAmp').value = amp;
            document.getElementById('waveSpeed').value = speed;
            document.getElementById('particleDensity').value = density;

            // Update actual values
            waveField.ampBase = amp;
            waveField.speedBase = speed / 10000;
            particleDensityMultiplier = density / 25;

            // Interpolate colors
            const r = lerpValue(morphStartState.frameColorRGB.r, morphTarget.frameColorRGB.r, t);
            const g = lerpValue(morphStartState.frameColorRGB.g, morphTarget.frameColorRGB.g, t);
            const b = lerpValue(morphStartState.frameColorRGB.b, morphTarget.frameColorRGB.b, t);
            const morphedColor = rgbToHex(r, g, b);

            // Apply morphed color to frame
            container.style.borderColor = morphedColor;
            phaseEl.style.color = morphedColor;

            // Update frame color state at end
            if (morphProgress >= 1) {
                activeFrameColor = morphTarget.frameColor;
                setFrameColor(activeFrameColor);
            }
        }

        // ================================================================
        // AUDIO-REACTIVE SYSTEM
        // ================================================================
        let audioContext = null;
        let analyser = null;
        let audioSource = null;
        let audioEnabled = false;
        let frequencyData = { low: 0, mid: 0, high: 0 };

        async function toggleAudio() {
            const btn = document.getElementById('audioToggle');

            if (!audioEnabled) {
                try {
                    // Request microphone access
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                    // Setup audio context
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    analyser = audioContext.createAnalyser();
                    analyser.fftSize = 256;
                    analyser.smoothingTimeConstant = 0.8;

                    audioSource = audioContext.createMediaStreamSource(stream);
                    audioSource.connect(analyser);

                    audioEnabled = true;
                    btn.classList.add('active');
                    btn.innerHTML = '<span>Listening...</span>';
                    console.log('Audio-reactive mode enabled');

                } catch (err) {
                    console.error('Microphone access denied:', err);
                    alert('Microphone access needed for audio-reactive mode!');
                }
            } else {
                // Disable audio
                if (audioSource) {
                    audioSource.disconnect();
                }
                if (audioContext) {
                    audioContext.close();
                }
                audioEnabled = false;
                audioContext = null;
                analyser = null;
                audioSource = null;
                frequencyData = { low: 0, mid: 0, high: 0 };

                btn.classList.remove('active');
                btn.innerHTML = '<span>Enable Microphone</span>';

                // Reset frequency bars
                document.getElementById('freqLow').style.height = '2px';
                document.getElementById('freqLow2').style.height = '2px';
                document.getElementById('freqMid').style.height = '2px';
                document.getElementById('freqMid2').style.height = '2px';
                document.getElementById('freqHigh').style.height = '2px';
            }
        }

        function updateAudioReactive() {
            if (!audioEnabled || !analyser) return;

            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyser.getByteFrequencyData(dataArray);

            const sensitivity = parseFloat(document.getElementById('audioSensitivity').value) / 50;

            // Calculate frequency bands (low: bass, mid: mids, high: treble)
            const lowEnd = Math.floor(bufferLength * 0.1);   // 0-10% = bass
            const midStart = Math.floor(bufferLength * 0.1);
            const midEnd = Math.floor(bufferLength * 0.5);   // 10-50% = mids
            const highStart = Math.floor(bufferLength * 0.5);

            // Average each band
            let lowSum = 0, midSum = 0, highSum = 0;
            for (let i = 0; i < lowEnd; i++) lowSum += dataArray[i];
            for (let i = midStart; i < midEnd; i++) midSum += dataArray[i];
            for (let i = highStart; i < bufferLength; i++) highSum += dataArray[i];

            // Guard against division by zero (unlikely but possible with small FFT sizes)
            const low = lowEnd > 0 ? (lowSum / lowEnd / 255) * sensitivity : 0;
            const mid = (midEnd - midStart) > 0 ? (midSum / (midEnd - midStart) / 255) * sensitivity : 0;
            const high = (bufferLength - highStart) > 0 ? (highSum / (bufferLength - highStart) / 255) * sensitivity : 0;

            // Smooth transitions
            frequencyData.low = frequencyData.low * 0.7 + low * 0.3;
            frequencyData.mid = frequencyData.mid * 0.7 + mid * 0.3;
            frequencyData.high = frequencyData.high * 0.7 + high * 0.3;

            // Update frequency display bars
            document.getElementById('freqLow').style.height = Math.max(2, frequencyData.low * 22) + 'px';
            document.getElementById('freqLow2').style.height = Math.max(2, frequencyData.low * 18) + 'px';
            document.getElementById('freqMid').style.height = Math.max(2, frequencyData.mid * 22) + 'px';
            document.getElementById('freqMid2').style.height = Math.max(2, frequencyData.mid * 18) + 'px';
            document.getElementById('freqHigh').style.height = Math.max(2, frequencyData.high * 22) + 'px';

            // === MAP AUDIO TO VISUAL PARAMETERS ===

            // Low (bass) → Wave amplitude (landscape rumble)
            const baseAmp = parseFloat(document.getElementById('waveAmp').value);
            waveField.ampBase = baseAmp + frequencyData.low * 30;

            // Mid → Particle density boost
            const baseDensity = parseFloat(document.getElementById('particleDensity').value) / 25;
            particleDensityMultiplier = baseDensity + frequencyData.mid * 2;

            // High (treble) → Wave speed boost
            const baseSpeed = parseFloat(document.getElementById('waveSpeed').value) / 10000;
            waveField.speedBase = baseSpeed + frequencyData.high * 0.002;

            // Strong beats: trigger particle bursts
            if (frequencyData.low > 0.7) {
                const burstX = width * (0.2 + Math.random() * 0.6);
                const burstY = height * (0.2 + Math.random() * 0.6);
                spawnEmergenceParticles(burstX, burstY, Math.floor(frequencyData.low * 8));
            }
        }

        // Control panel functions
        function toggleControls() {
            const panel = document.getElementById('controls');
            const toggle = panel.querySelector('.ctrl-toggle');
            panel.classList.toggle('collapsed');
            toggle.textContent = panel.classList.contains('collapsed') ? '▶' : '▼';
        }

        function setFrameColor(color) {
            activeFrameColor = color;
            // Update button states
            document.querySelectorAll('.ctrl-btn.gold, .ctrl-btn.blue, .ctrl-btn.purple').forEach(btn => {
                btn.classList.remove('active');
            });
            const colorClass = color === 'teal' ? 'blue' : color === 'combat' ? 'purple' : 'gold';
            document.querySelector(`.ctrl-btn.${colorClass}`).classList.add('active');

            // Update container border
            const borderColor = color === 'gold' ? COLORS.gold : color === 'combat' ? COLORS.combat : COLORS.teal;
            container.style.borderColor = borderColor;
            phaseEl.style.color = borderColor;
        }

        function updateWave() {
            const amp = parseFloat(document.getElementById('waveAmp').value);
            const speed = parseFloat(document.getElementById('waveSpeed').value);
            waveField.ampBase = amp;
            waveField.speedBase = speed / 10000;  // Scale to reasonable range
        }

        function updateParticles() {
            const density = parseFloat(document.getElementById('particleDensity').value);
            particleDensityMultiplier = density / 25;  // Normalize around default
        }

        function reEmergence() {
            // Reset emergence state
            emerged = false;
            emergenceProgress = 0;
            emergenceStartTime = performance.now();
            container.classList.remove('emerged');
            phaseEl.classList.remove('emerged');

            // Re-scatter nodes
            for (let i = 0; i < nodeStates.length; i++) {
                nodeStates[i].currentX = width / 2 + (Math.random() - 0.5) * width * 0.8;
                nodeStates[i].currentY = height / 2 + (Math.random() - 0.5) * height * 0.8;
                nodeStates[i].currentAlpha = 0;
            }
        }

        function clearParticles() {
            particles.length = 0;
        }

        function getFrameColor() {
            if (activeFrameColor === 'combat') return COLORS.combat;
            if (activeFrameColor === 'teal') return COLORS.teal;
            return emerged ? COLORS.gold : COLORS.teal;
        }

        // ================================================================
        // NODE TYPE SHAPE DRAWING
        // ================================================================
        function drawNodeShape(ctx, x, y, radius, nodeType, color, alpha) {
            ctx.globalAlpha = alpha;
            ctx.fillStyle = color;
            ctx.beginPath();

            const shape = NODE_SHAPES[nodeType] || 'circle';

            switch (shape) {
                case 'diamond':
                    // Component - rotated square
                    ctx.moveTo(x, y - radius * 1.2);
                    ctx.lineTo(x + radius, y);
                    ctx.lineTo(x, y + radius * 1.2);
                    ctx.lineTo(x - radius, y);
                    ctx.closePath();
                    break;

                case 'hexagon':
                    // Store - hexagon
                    for (let i = 0; i < 6; i++) {
                        const angle = (i * Math.PI / 3) - Math.PI / 2;
                        const px = x + radius * Math.cos(angle);
                        const py = y + radius * Math.sin(angle);
                        if (i === 0) ctx.moveTo(px, py);
                        else ctx.lineTo(px, py);
                    }
                    ctx.closePath();
                    break;

                case 'star':
                    // Entry point - 5-pointed star
                    for (let i = 0; i < 10; i++) {
                        const r = i % 2 === 0 ? radius * 1.2 : radius * 0.5;
                        const angle = (i * Math.PI / 5) - Math.PI / 2;
                        const px = x + r * Math.cos(angle);
                        const py = y + r * Math.sin(angle);
                        if (i === 0) ctx.moveTo(px, py);
                        else ctx.lineTo(px, py);
                    }
                    ctx.closePath();
                    break;

                case 'triangle':
                    // Test/API - triangle
                    ctx.moveTo(x, y - radius);
                    ctx.lineTo(x + radius * 0.87, y + radius * 0.5);
                    ctx.lineTo(x - radius * 0.87, y + radius * 0.5);
                    ctx.closePath();
                    break;

                case 'pentagon':
                    // Route - pentagon
                    for (let i = 0; i < 5; i++) {
                        const angle = (i * 2 * Math.PI / 5) - Math.PI / 2;
                        const px = x + radius * Math.cos(angle);
                        const py = y + radius * Math.sin(angle);
                        if (i === 0) ctx.moveTo(px, py);
                        else ctx.lineTo(px, py);
                    }
                    ctx.closePath();
                    break;

                case 'square':
                    // Config - square
                    ctx.rect(x - radius, y - radius, radius * 2, radius * 2);
                    break;

                default:
                    // Default circle
                    ctx.arc(x, y, radius, 0, Math.PI * 2);
            }

            ctx.fill();
        }

        // ================================================================
        // EDGE RENDERING - Real import connections
        // ================================================================
        function drawImportEdges(ctx, time) {
            if (!edges || edges.length === 0) return;

            const elapsed = time - emergenceStartTime;

            for (const edge of edges) {
                const sourceNode = nodeById[edge.source];
                const targetNode = nodeById[edge.target];
                if (!sourceNode || !targetNode) continue;

                const sourceIdx = nodes.indexOf(sourceNode);
                const targetIdx = nodes.indexOf(targetNode);
                if (sourceIdx < 0 || targetIdx < 0) continue;

                const sourceState = nodeStates[sourceIdx];
                const targetState = nodeStates[targetIdx];

                // Use current positions during emergence
                const x1 = emerged ? sourceNode.x : sourceState.currentX;
                const y1 = emerged ? sourceNode.y : sourceState.currentY;
                const x2 = emerged ? targetNode.x : targetState.currentX;
                const y2 = emerged ? targetNode.y : targetState.currentY;

                // Edge alpha based on emergence progress
                const edgeAlpha = Math.min(sourceState.currentAlpha, targetState.currentAlpha) * 0.4;
                if (edgeAlpha < 0.05) continue;

                ctx.globalAlpha = edgeAlpha;

                // Color based on resolved status
                if (!edge.resolved) {
                    ctx.strokeStyle = COLORS.edgeBroken;
                    ctx.setLineDash([4, 4]);  // Dashed for broken
                } else if (edge.bidirectional) {
                    ctx.strokeStyle = COLORS.cycle;  // Red for mutual imports
                    ctx.setLineDash([]);
                } else {
                    ctx.strokeStyle = COLORS.edge;
                    ctx.setLineDash([]);
                }

                ctx.lineWidth = edge.bidirectional ? 1.5 : 0.8;

                // Draw curved edge (quadratic bezier)
                const midX = (x1 + x2) / 2;
                const midY = (y1 + y2) / 2;
                const dx = x2 - x1;
                const dy = y2 - y1;
                const dist = Math.sqrt(dx * dx + dy * dy);

                // Curve outward perpendicular to the line
                const curveOffset = Math.min(dist * 0.15, 30);
                const perpX = -dy / dist * curveOffset;
                const perpY = dx / dist * curveOffset;

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.quadraticCurveTo(midX + perpX, midY + perpY, x2, y2);
                ctx.stroke();

                // Draw arrowhead
                if (emerged && edgeAlpha > 0.2) {
                    const arrowSize = 4;
                    const angle = Math.atan2(y2 - (midY + perpY), x2 - (midX + perpX));
                    ctx.beginPath();
                    ctx.moveTo(x2, y2);
                    ctx.lineTo(
                        x2 - arrowSize * Math.cos(angle - Math.PI / 6),
                        y2 - arrowSize * Math.sin(angle - Math.PI / 6)
                    );
                    ctx.lineTo(
                        x2 - arrowSize * Math.cos(angle + Math.PI / 6),
                        y2 - arrowSize * Math.sin(angle + Math.PI / 6)
                    );
                    ctx.closePath();
                    ctx.fill();
                }
            }

            ctx.setLineDash([]);  // Reset
        }

        // ================================================================
        // CYCLE HIGHLIGHTING - Pulsing glow for circular dependencies
        // ================================================================
        function drawCycleGlow(ctx, node, x, y, radius, time) {
            if (!node.inCycle) return;

            // Pulsing animation
            const pulse = 0.5 + 0.5 * Math.sin(time * 0.003);
            const glowRadius = radius * (2 + pulse);

            ctx.save();
            ctx.globalAlpha = 0.3 * pulse;
            ctx.shadowColor = COLORS.cycle;
            ctx.shadowBlur = 20 + pulse * 10;
            ctx.fillStyle = COLORS.cycle;
            ctx.beginPath();
            ctx.arc(x, y, glowRadius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }

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
        const cycleCount = nodes.filter(n => n.inCycle).length;
        const edgeCount = edges ? edges.length : 0;
        stats.innerHTML = `
            <span class="working">${workingCount} working</span>
            <span class="broken">${brokenCount} broken</span>
            ${combatCount ? `<span class="combat">${combatCount} combat</span>` : ''}
            ${cycleCount ? `<span style="color: #ff4444;">${cycleCount} in cycles</span>` : ''}
            <span>${nodes.length} files</span>
            ${edgeCount ? `<span style="color: #666;">${edgeCount} imports</span>` : ''}
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
        let emergenceStartTime = performance.now();
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
        // DELAUNAY TRIANGULATION (for mesh background)
        // ================================================================
        function distance(p0, p1) {
            return Math.sqrt(Math.pow(p1.x - p0.x, 2) + Math.pow(p1.y - p0.y, 2));
        }

        let delaunayEdges = [];
        if (nodes.length >= 3) {
            const points = nodes.map(n => [n.x, n.y]);
            const delaunay = d3.Delaunay.from(points);
            const triangles = delaunay.triangles;

            for (let i = 0; i < triangles.length; i += 3) {
                const [i0, i1, i2] = [triangles[i], triangles[i+1], triangles[i+2]];
                const [p0, p1, p2] = [nodes[i0], nodes[i1], nodes[i2]];
                if (p0 && p1 && p2) {
                    delaunayEdges.push(
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

        function renderDelaunayEdges(minLength, color, alpha, useCurrentPositions = false) {
            if (delaunayEdges.length === 0) return;
            ctx.globalAlpha = alpha * emergenceProgress;
            ctx.strokeStyle = color;
            ctx.lineWidth = 0.5;
            ctx.beginPath();

            for (const edge of delaunayEdges) {
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
            // Update keyframe morphing
            updateMorph();

            // Update audio-reactive values
            updateAudioReactive();

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
                    const spawnChance = (0.02 + waveStrength * 0.03) * particleDensityMultiplier;
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
            if (delaunayEdges.length > 0) {
                const frameColor = getFrameColor();

                // Layer 1: Dense gradient base (the "city" silhouette)
                ctx.save();
                for (let i = 0; i < maxHeight; i++) {
                    ctx.translate(0, 0.5);  // Slightly larger steps for depth
                    // Exponential falloff for more realistic depth
                    const alpha = Math.pow(1 - i / maxHeight, 1.5) * 0.04;
                    // Edge threshold grows slower at bottom (denser base)
                    const threshold = Math.pow(i / maxHeight, 0.7) * maxHeight * 0.8;
                    renderDelaunayEdges(threshold, frameColor, alpha, !emerged);
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
                    renderDelaunayEdges(15 + i * 15, frameColor, 0.03 + 0.1 * t, !emerged);
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
                renderDelaunayEdges(40, ctx.strokeStyle, 0.12, !emerged);

                // Layer 5: Soft glow blur
                ctx.filter = 'blur(3px)';
                ctx.globalAlpha = 0.15;
                ctx.strokeStyle = frameColor;
                ctx.lineWidth = 1.5;
                renderDelaunayEdges(60, ctx.strokeStyle, 0.15, !emerged);
                ctx.filter = 'none';
                ctx.restore();
            }

            // ============================================================
            // IMPORT EDGES - Real connections from ConnectionGraph
            // ============================================================
            drawImportEdges(ctx, time);

            // Draw nodes with type shapes and centrality sizing
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const state = nodeStates[i];
                const color = COLORS[node.status];

                // Size based on centrality (if available) + LOC
                // centrality ranges 0-1, boost important nodes
                const centralityBoost = (node.centrality || 0) * 8;
                const baseRadius = 2 + Math.min(node.loc / 80, 6) + centralityBoost;

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

                // CYCLE HIGHLIGHTING - Red pulsing glow
                if (node.inCycle && alpha > 0.3) {
                    drawCycleGlow(ctx, node, x, y, baseRadius, time);
                }

                // Outer glow for non-working or cycle nodes
                if ((node.status === 'broken' || node.status === 'combat' || node.inCycle) && alpha > 0.5) {
                    ctx.save();
                    ctx.globalAlpha = 0.25 * alpha;
                    ctx.shadowColor = node.inCycle ? COLORS.cycle : color;
                    ctx.shadowBlur = 15;
                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(x, y, baseRadius * 1.8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }

                // Draw node with type-specific shape
                const nodeType = node.nodeType || 'file';
                drawNodeShape(ctx, x, y, baseRadius, nodeType, color, 0.85 * alpha);

                // Inner highlight for larger nodes
                if (alpha > 0.7 && baseRadius > 4) {
                    ctx.globalAlpha = 0.4 * alpha;
                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(x - baseRadius * 0.25, y - baseRadius * 0.25, baseRadius * 0.2, 0, Math.PI * 2);
                    ctx.fill();
                }

                // Entry point special glow (stars get extra treatment)
                if (nodeType === 'entry' && emerged && alpha > 0.8) {
                    ctx.save();
                    ctx.globalAlpha = 0.15 + 0.1 * Math.sin(time * 0.002);
                    ctx.shadowColor = COLORS.gold;
                    ctx.shadowBlur = 20;
                    ctx.fillStyle = COLORS.gold;
                    ctx.beginPath();
                    ctx.arc(x, y, baseRadius * 0.5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
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
                    if (node.status === 'broken' && Math.random() < 0.025 * particleDensityMultiplier) {
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

                // Node type badge
                const nodeType = node.nodeType || 'file';
                const typeColors = {
                    entry: '#D4AF37',
                    component: '#9D4EDD',
                    store: '#1fbdea',
                    test: '#888',
                    route: '#F4C430',
                    api: '#1fbdea'
                };
                const typeColor = typeColors[nodeType] || '#666';

                // Connection info
                const incoming = node.incomingCount || 0;
                const outgoing = node.outgoingCount || 0;
                const connectionInfo = incoming || outgoing
                    ? `<div style="color: #666; margin-top: 4px; font-size: 10px;">↓${incoming} imports this · ↑${outgoing} imports</div>`
                    : '';

                // Cycle warning
                const cycleWarning = node.inCycle
                    ? `<div style="color: #ff4444; margin-top: 4px; font-size: 10px;">CYCLE: Part of circular dependency</div>`
                    : '';

                // Centrality indicator
                const centrality = node.centrality || 0;
                const centralityInfo = centrality > 0.01
                    ? `<div style="color: #888; font-size: 10px;">Centrality: ${(centrality * 100).toFixed(1)}%</div>`
                    : '';

                tooltip.innerHTML = `
                    <div class="path">${node.path}</div>
                    <div class="meta">
                        <span class="status ${node.status}">${node.status}</span>
                        <span style="color: ${typeColor}; font-size: 10px; text-transform: uppercase;">${nodeType}</span>
                        <span class="loc">${node.loc} lines</span>
                    </div>
                    ${connectionInfo}
                    ${centralityInfo}
                    ${cycleWarning}
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
                    node: {
                        path: node.path,
                        status: node.status,
                        loc: node.loc,
                        errors: node.errors,
                        nodeType: node.nodeType,
                        centrality: node.centrality,
                        inCycle: node.inCycle,
                        incomingCount: node.incomingCount,
                        outgoingCount: node.outgoingCount
                    }
                }, '*');
                console.log('Node clicked:', node.path, node.nodeType);
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
                sandbox="allow-scripts allow-same-origin"
                allow="microphone"
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

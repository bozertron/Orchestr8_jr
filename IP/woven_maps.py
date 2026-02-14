"""
Woven Maps Code City Visualization - Enhanced Edition
======================================================

Enhanced with:
- Emergence animation (particles coalesce from chaos)
- Teal → Gold frame transition (scan progress → complete)
- Organic curl-like particle motion
- Phase-based initialization (tuning → coalescing → emergence)

Based on Nicolas Barradeau's "Woven Maps" algorithm
Aligned with Maestro vision (M14.jpg reference)
"""

from __future__ import annotations

import json
import html
import math
import os
import re
import ast
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from IP.contracts.status_merge_policy import merge_status

# =============================================================================
# COLOR CONSTANTS - EXACT, NO EXCEPTIONS
# =============================================================================

COLORS = {
    "gold_metallic": "#D4AF37",  # Working code
    "blue_dominant": "#1fbdea",  # Broken code / Teal during scan
    "purple_combat": "#9D4EDD",  # Combat (LLM active)
    "bg_primary": "#0A0A0B",  # The Void
    "bg_elevated": "#121214",  # Elevated surfaces
    "gold_dark": "#B8860B",  # Secondary gold
    "gold_saffron": "#F4C430",  # Bright highlights
}

JS_COLORS = {
    "void": "#0A0A0B",
    "working": "#D4AF37",
    "broken": "#1fbdea",
    "combat": "#9D4EDD",
    "wireframe": "#333333",
    "teal": "#1fbdea",
    "gold": "#D4AF37",
    "cycle": "#ff4444",
    "edge": "#333333",
    "edge_broken": "#ff6b6b",
}

# Locked building geometry formulas from canon:
# height = 3 + (exports * 0.8)
# footprint = 2 + (lines * 0.008)
BUILDING_HEIGHT_BASE = 3.0
BUILDING_HEIGHT_EXPORT_SCALE = 0.8
BUILDING_FOOTPRINT_BASE = 2.0
BUILDING_FOOTPRINT_LOC_SCALE = 0.008

# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class CodeNode:
    """Represents a file in the codebase."""

    path: str
    status: str = "working"  # working | broken | combat
    loc: int = 0
    errors: List[str] = field(default_factory=list)
    health_errors: List[Any] = field(
        default_factory=list
    )  # Structured health check errors
    x: float = 0.0
    y: float = 0.0
    # Extended fields for ConnectionGraph integration
    node_type: str = "file"  # file|component|store|entry|test|route|api|config|type
    centrality: float = 0.0  # PageRank score (0-1) for sizing
    in_cycle: bool = False  # Part of circular dependency
    depth: int = 0  # Distance from entry points
    incoming_count: int = 0  # Files that import this
    outgoing_count: int = 0  # Files this imports
    export_count: int = 0  # Public/exported symbols used by geometry contract
    building_height: float = BUILDING_HEIGHT_BASE
    footprint: float = BUILDING_FOOTPRINT_BASE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.path,
            "path": self.path,
            "status": self.status,
            "x": self.x,
            "y": self.y,
            "loc": self.loc,
            "errors": self.errors,
            "healthErrors": self.health_errors,
            "nodeType": self.node_type,
            "centrality": self.centrality,
            "inCycle": self.in_cycle,
            "depth": self.depth,
            "incomingCount": self.incoming_count,
            "outgoingCount": self.outgoing_count,
            "exportCount": self.export_count,
            "buildingHeight": self.building_height,
            "footprint": self.footprint,
        }


@dataclass
class EdgeData:
    """Represents an import relationship between files."""

    source: str  # Source file path (importer)
    target: str  # Target file path (imported)
    resolved: bool = True  # Whether the import resolves
    bidirectional: bool = False  # Mutual imports
    line_number: int = 0  # Source line of import

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
    """Color configuration for Woven Maps - matches orchestr8 three-state system."""

    working: str = COLORS["gold_metallic"]  # Gold - all imports resolve
    broken: str = COLORS["blue_dominant"]  # Blue/Teal - has errors
    combat: str = COLORS["purple_combat"]  # Purple - LLM deployed
    void: str = COLORS["bg_primary"]  # Background
    surface: str = COLORS["bg_elevated"]  # Elevated surfaces

    # Frame colors (teal during scan, gold when complete)
    frame_scanning: str = COLORS["blue_dominant"]
    frame_complete: str = COLORS["gold_metallic"]

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
    max_height: int = 250  # Taller cityscape silhouette
    wire_count: int = 15  # More wireframe layers for richness
    show_particles: bool = True
    show_tooltip: bool = True
    emergence_duration: float = 2.5  # Slightly longer for drama
    # Performance profile tuned for Dell Precision 7710 + Quadro M5000M demo
    particle_cpu_cap: int = 180000
    particle_gpu_target_cap: int = 1_000_000
    emergence_frame_spawn_cap: int = 700
    error_frame_spawn_cap: int = 280
    mesh_layer_cap: int = 18
    mesh_gradient_height_cap: int = 340
    edge_stride: int = 1
    audio_fft_size: int = 256
    audio_smoothing: float = 0.82
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
            "performance": {
                "particleCpuCap": self.particle_cpu_cap,
                "particleGpuTargetCap": self.particle_gpu_target_cap,
                "emergenceFrameSpawnCap": self.emergence_frame_spawn_cap,
                "errorFrameSpawnCap": self.error_frame_spawn_cap,
                "meshLayerCap": self.mesh_layer_cap,
                "meshGradientHeightCap": self.mesh_gradient_height_cap,
                "edgeStride": self.edge_stride,
                "audioFftSize": self.audio_fft_size,
                "audioSmoothing": self.audio_smoothing,
            },
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
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    ".venv",
    "venv",
    "env",
    ".env",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
    ".coverage",
    "htmlcov",
    ".idea",
    ".vscode",
    "target",
    "out",
    "bin",
}

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".mjs",
    ".cjs",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".scala",
    ".vue",
    ".svelte",
    ".astro",
}


def compute_building_geometry(lines: int, exports: int) -> tuple[float, float]:
    """Compute canonical building geometry using locked formulas."""
    safe_lines = max(0, int(lines))
    safe_exports = max(0, int(exports))
    height = BUILDING_HEIGHT_BASE + (safe_exports * BUILDING_HEIGHT_EXPORT_SCALE)
    footprint = BUILDING_FOOTPRINT_BASE + (safe_lines * BUILDING_FOOTPRINT_LOC_SCALE)
    return height, footprint


def _count_python_exports(content: str) -> int:
    """Count top-level Python definitions as export proxies."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return 0

    count = 0
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Exclude underscore-prefixed internals from "public export" count.
            if not node.name.startswith("_"):
                count += 1
    return count


def _count_js_like_exports(content: str) -> int:
    """Count JS/TS/Vue/Svelte style exports."""
    export_patterns = [
        r"\bexport\s+(default\s+)?(async\s+)?(function|class|const|let|var|interface|type|enum)\b",
        r"\bexport\s*\{[^}]+\}",
        r"\bmodule\.exports\s*=",
        r"\bexports\.[A-Za-z_]\w*\s*=",
    ]
    count = 0
    for pattern in export_patterns:
        count += len(re.findall(pattern, content))
    return count


def estimate_export_count(filepath: Path, content: str) -> int:
    """Estimate exported/public symbol count for geometry sizing."""
    ext = filepath.suffix.lower()
    if ext == ".py":
        return _count_python_exports(content)
    if ext in {
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".mjs",
        ".cjs",
        ".vue",
        ".svelte",
        ".astro",
    }:
        return _count_js_like_exports(content)
    return 0


def get_file_metrics(root: Path, relpath: str) -> tuple[int, int]:
    """Return (loc, export_count) for a file relative to project root."""
    filepath = root / relpath
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 0, 0

    loc = len(content.splitlines())
    export_count = estimate_export_count(filepath, content)
    return loc, export_count


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
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]

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
                nodes.append(
                    CodeNode(
                        path=relpath,
                        status="broken",
                        loc=0,
                        errors=[f"Read error: {str(e)}"],
                    )
                )

    return nodes


def analyze_file(filepath: Path, relpath: str) -> CodeNode:
    """Analyze a single file for status and metrics."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return CodeNode(path=relpath, status="broken", errors=[str(e)])

    lines = content.split("\n")
    loc = len(lines)
    export_count = estimate_export_count(filepath, content)
    building_height, footprint = compute_building_geometry(loc, export_count)
    errors = []

    # TODO/FIXME detection
    todo_pattern = re.compile(r"\b(TODO|FIXME|XXX|HACK|BUG)\b", re.IGNORECASE)
    for i, line in enumerate(lines[:500], 1):
        if todo_pattern.search(line):
            match = todo_pattern.search(line)
            errors.append(f"Line {i}: {match.group(0)} found")
            if len(errors) >= 5:
                errors.append("... and more")
                break

    # Debug statement detection
    debug_patterns = [
        (r"console\.(log|debug|info)\s*\(", "console.log"),
        (r"print\s*\([^)]*debug", "debug print"),
        (r"debugger\s*;?", "debugger statement"),
        (r"pdb\.set_trace\(\)", "pdb breakpoint"),
        (r"breakpoint\(\)", "breakpoint"),
    ]

    for pattern, name in debug_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"{name} detected")

    status = "broken" if errors else "working"
    return CodeNode(
        path=relpath,
        status=status,
        loc=loc,
        errors=errors[:10],
        export_count=export_count,
        building_height=building_height,
        footprint=footprint,
    )


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
        if dir_path == ".":
            dir_path = "root"
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
                size_factor = min(
                    1.0,
                    max(0.0, (node.footprint - BUILDING_FOOTPRINT_BASE) / 8.0),
                )
                radius = 20 + size_factor * (max_radius - 20)
                jitter_x = hash(node.path) % 21 - 10
                jitter_y = hash(node.path + "y") % 21 - 10
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
    root_path = Path(project_root).resolve()
    metrics_cache: Dict[str, tuple[int, int]] = {}

    for node_data in graph_dict["nodes"]:
        metrics = node_data.get("metrics", {})

        # Map status: error → broken, normal → working
        status = "working"
        if node_data.get("status") == "error":
            status = "broken"
        elif metrics.get("issueCount", 0) > 0:
            status = "broken"

        file_path = node_data["filePath"]
        if file_path not in metrics_cache:
            metrics_cache[file_path] = get_file_metrics(root_path, file_path)
        loc, export_count = metrics_cache[file_path]
        building_height, footprint = compute_building_geometry(loc, export_count)

        code_node = CodeNode(
            path=file_path,
            status=status,
            loc=loc,
            errors=[],  # Could extract from connection graph
            node_type=node_data.get("type", "file"),
            centrality=metrics.get("centrality", 0.0),
            in_cycle=metrics.get("inCycle", False),
            depth=metrics.get("depth", 0),
            incoming_count=metrics.get("incomingCount", 0),
            outgoing_count=metrics.get("outgoingCount", 0),
            export_count=export_count,
            building_height=building_height,
            footprint=footprint,
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
            edges.append(
                EdgeData(
                    source=edge_data["source"],
                    target=edge_data["target"],
                    resolved=edge_data.get("resolved", True),
                    bidirectional=edge_data.get("bidirectional", False),
                    line_number=edge_data.get("lineNumber", 0),
                )
            )

    config = GraphConfig(
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )

    return GraphData(nodes=nodes, edges=edges, config=config)


def build_from_health_results(
    nodes: List[CodeNode], health_results: Dict[str, Any]
) -> List[CodeNode]:
    """
    Merge HealthChecker output into CodeNode objects.

    Updates node status to 'broken' if health check fails,
    and populates health_errors for tooltip display.

    Args:
        nodes: List of CodeNode objects to update
        health_results: Dict mapping file paths to HealthCheckResult

    Returns:
        Updated list of CodeNode objects
    """
    for node in nodes:
        for path, result in health_results.items():
            if path in node.path or node.path.startswith(path.rstrip("/")):
                # Use canonical merge_status — combat > broken > working
                node.status = merge_status(node.status, result.status)

                if hasattr(result, "errors") and result.errors:
                    node.health_errors = [
                        {"file": e.file, "line": e.line, "message": e.message}
                        for e in result.errors[:10]
                    ]
                break

    return nodes


# =============================================================================
# BARRADEAU 3D BUILDING GENERATION
# =============================================================================


def generate_barradeau_buildings(
    graph_data: "GraphData",
    layout_scale: float = 10.0,
) -> List[Dict[str, Any]]:
    """
    Generate Barradeau-style 3D buildings from GraphData.

    Args:
        graph_data: GraphData with nodes and layout
        layout_scale: Scale factor for positioning buildings in 3D space

    Returns:
        List of BuildingData dicts ready for JSON serialization
    """
    try:
        from IP.barradeau_builder import BarradeauBuilding
    except ImportError:
        from barradeau_builder import BarradeauBuilding

    buildings = []

    for node in graph_data.nodes:
        position = {"x": node.x * layout_scale, "z": node.y * layout_scale}

        building = BarradeauBuilding(
            path=node.path,
            line_count=node.loc,
            export_count=node.export_count,
            status=node.status,
            position=position,
        )

        building_data = building.get_building_data().to_json()
        buildings.append(building_data)

    return buildings


def create_3d_code_city(
    graph_data: "GraphData",
    layout_scale: float = 10.0,
) -> Dict[str, Any]:
    """
    Create complete 3D Code City data package for frontend.

    Args:
        graph_data: GraphData with nodes and edges
        layout_scale: Scale factor for 3D positioning

    Returns:
        Dict with buildings array and metadata
    """
    buildings = generate_barradeau_buildings(graph_data, layout_scale)

    return {
        "buildings": buildings,
        "metadata": {
            "total_buildings": len(buildings),
            "layout_scale": layout_scale,
            "generated_at": datetime.now().isoformat(),
        },
    }


# =============================================================================
# ENHANCED IFRAME TEMPLATE - With Emergence Animations
# =============================================================================

WOVEN_MAPS_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/d3-delaunay@6"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0A0A0B;
            overflow: hidden;
            font-family: 'Orchestr8 Mini Pixel', 'Courier New', monospace;
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
        #city-gpu {
            position: absolute;
            inset: 0;
            display: none;
            pointer-events: none;
        }

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
        #tooltip .health-errors { margin-top: 8px; padding-top: 8px; border-top: 1px solid #1fbdea; }
        #tooltip .health-error-item { color: #1fbdea; font-size: 10px; line-height: 1.4; margin: 2px 0; }
        #tooltip .health-error-loc { color: #666; font-family: monospace; }

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

        /* Connection Panel */
        #connection-panel {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 340px;
            max-height: 280px;
            overflow: auto;
            background: rgba(18, 18, 20, 0.94);
            border: 1px solid rgba(212, 175, 55, 0.45);
            border-radius: 6px;
            padding: 10px 12px;
            color: #cfcfcf;
            font-size: 10px;
            z-index: 900;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.45);
        }
        #connection-panel.hidden {
            display: none;
        }
        #connection-panel .title {
            color: #D4AF37;
            font-size: 10px;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-weight: 600;
        }
        #connection-panel .row {
            margin: 2px 0;
            color: #9c9c9c;
            word-break: break-all;
        }
        #connection-panel .row strong {
            color: #cfcfcf;
            margin-right: 4px;
        }
        #connection-panel .path-list {
            margin-top: 8px;
            padding-top: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #d7d7d7;
        }
        #connection-panel .path-list div {
            margin: 2px 0;
            word-break: break-all;
        }
        #connection-panel .meta {
            margin-top: 7px;
            color: #777;
        }
        #connection-panel .actions {
            display: flex;
            gap: 6px;
            margin-top: 10px;
            align-items: center;
        }
        #connection-panel .rewire-input {
            width: 100%;
            margin-top: 8px;
            background: rgba(10, 10, 11, 0.95);
            border: 1px solid rgba(31, 189, 234, 0.35);
            color: #d7d7d7;
            border-radius: 4px;
            padding: 4px 6px;
            font-size: 10px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            box-sizing: border-box;
        }
        #connection-panel .rewire-input:focus {
            outline: none;
            border-color: rgba(212, 175, 55, 0.65);
        }
        #connection-panel .action-btn {
            background: rgba(10, 10, 11, 0.95);
            border: 1px solid rgba(212, 175, 55, 0.45);
            color: #D4AF37;
            border-radius: 4px;
            font-size: 10px;
            padding: 3px 7px;
            cursor: pointer;
            letter-spacing: 0.03em;
        }
        #connection-panel .action-btn:hover {
            border-color: rgba(31, 189, 234, 0.6);
            color: #f0d47a;
        }
        #connection-panel .action-btn.apply {
            border-color: rgba(31, 189, 234, 0.55);
            color: #1fbdea;
        }
        #connection-panel .action-btn.apply:hover {
            border-color: rgba(157, 78, 221, 0.75);
            color: #9D4EDD;
        }
        #connection-panel .action-btn.disabled,
        #connection-panel .action-btn:disabled {
            opacity: 0.45;
            cursor: not-allowed;
            border-color: rgba(120, 120, 120, 0.5);
            color: #8a8a8a;
        }
        #connection-panel .action-result {
            margin-top: 8px;
            padding-top: 7px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }
        #connection-panel .action-result .title {
            margin-bottom: 4px;
        }
        #connection-panel .action-result.ok .title {
            color: #D4AF37;
        }
        #connection-panel .action-result.blocked .title {
            color: #1fbdea;
        }
        #connection-panel .action-result .msg {
            color: #bbb;
            margin-bottom: 3px;
        }
        #connection-panel .action-result .issue {
            color: #1fbdea;
            margin: 2px 0;
        }
        #connection-panel .action-result .warn {
            color: #9D4EDD;
            margin: 2px 0;
        }
        #connection-panel .action-history {
            margin-top: 8px;
            padding-top: 7px;
            border-top: 1px dashed rgba(255, 255, 255, 0.14);
        }
        #connection-panel .action-history .title {
            color: #b8b8b8;
            margin-bottom: 4px;
        }
        #connection-panel .action-history .entry {
            margin: 3px 0;
            color: #9f9f9f;
            font-size: 9px;
            line-height: 1.35;
        }
        #connection-panel .action-history .entry.ok {
            color: #D4AF37;
        }
        #connection-panel .action-history .entry.blocked {
            color: #1fbdea;
        }

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
        #controls.docked-bottom {
            top: auto;
            bottom: 10px;
            left: 10px;
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
        <div id="city-gpu"></div>
        <div id="phase">tuning...</div>
    </div>
    <div id="tooltip"></div>
    <div id="stats"></div>
    <div id="connection-panel" class="hidden"></div>

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

            <!-- View Mode -->
            <div class="ctrl-section">
                <span class="ctrl-label">View Mode</span>
                <div class="ctrl-row">
                    <button class="ctrl-btn gold active" id="view2dBtn" onclick="setViewMode('2d')">2D</button>
                    <button class="ctrl-btn blue" id="view3dBtn" onclick="setViewMode('3d')">3D</button>
                </div>
            </div>

            <!-- Particles -->
            <div class="ctrl-section">
                <span class="ctrl-label">densit8</span>
                <input type="range" class="ctrl-slider" id="particleDensity" min="1" max="10" value="5" oninput="updateDensit8()">
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
                <div class="ctrl-row">
                    <button class="ctrl-btn" onclick="toggleDock8()">dock8</button>
                    <button class="ctrl-btn" onclick="toggleOrbit8()">orbit8</button>
                </div>
                <div class="ctrl-row">
                    <button class="ctrl-btn" onclick="focus8()">focus8</button>
                    <button class="ctrl-btn" onclick="cycleLayer8()">layer8</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ================================================================
        // DATA & CONFIG
        // ================================================================
        const GRAPH_DATA = __GRAPH_DATA__;
        window.BUILDING_DATA = __BUILDING_DATA__;
        const BUILDING_STREAM_BPS = __BUILDING_STREAM_BPS__;
        const { nodes, edges = [], config } = GRAPH_DATA;
        const { width, height, maxHeight, wireCount, emergenceDuration = 2.0 } = config;
        const PATCHBAY_APPLY_ENABLED = __PATCHBAY_APPLY_ENABLED__;
        const perfCfg = config.performance || {};
        const PERF = {
            // CPU-safe cap for this canvas path (GPU target tracked separately)
            particleCpuCap: perfCfg.particleCpuCap || 180000,
            particleGpuTargetCap: perfCfg.particleGpuTargetCap || 1000000,
            emergenceFrameSpawnCap: perfCfg.emergenceFrameSpawnCap || 700,
            errorFrameSpawnCap: perfCfg.errorFrameSpawnCap || 280,
            meshLayerCap: perfCfg.meshLayerCap || 18,
            meshGradientHeightCap: perfCfg.meshGradientHeightCap || 340,
            edgeStride: perfCfg.edgeStride || 1,
            audioFftSize: perfCfg.audioFftSize || 256,
            audioSmoothing: perfCfg.audioSmoothing || 0.82
        };

        // ================================================================
        // CAMERA STATE
        // ================================================================
        const CAMERA_STATE = __CAMERA_STATE__;
        let cameraMode = CAMERA_STATE.mode;
        let cameraZoom = CAMERA_STATE.zoom;
        let cameraPanX = 0;
        let cameraPanY = 0;
        let cameraReturnStack = [];

        // Camera animation state
        let cameraAnimating = false;
        let cameraAnimStart = 0;
        let cameraAnimDuration = CAMERA_STATE.transition_ms;
        let cameraStartZoom = cameraZoom;
        let cameraTargetZoom = cameraZoom;
        let cameraStartPanX = 0;
        let cameraStartPanY = 0;
        let cameraTargetPanX = 0;
        let cameraTargetPanY = 0;

        function clamp01(v) {
            return Math.max(0, Math.min(1, v));
        }

        // Easing function for smooth camera transitions
        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }

        // Warp dive to a specific node
        function warpDiveTo(node) {
            if (!node) return;

            // Save current state to return stack
            cameraReturnStack.push({
                mode: cameraMode,
                zoom: cameraZoom,
                panX: cameraPanX,
                panY: cameraPanY,
            });

            // Calculate target pan to center on node
            const targetPanX = width / 2 - node.x;
            const targetPanY = height / 2 - node.y;
            const targetZoom = 3.0; // Zoom in 3x

            // Start animation
            cameraAnimating = true;
            cameraAnimStart = performance.now();
            cameraAnimDuration = CAMERA_STATE.transition_ms;
            cameraStartZoom = cameraZoom;
            cameraTargetZoom = targetZoom;
            cameraStartPanX = cameraPanX;
            cameraStartPanY = cameraPanY;
            cameraTargetPanX = targetPanX;
            cameraTargetPanY = targetPanY;

            cameraMode = 'focus';
        }

        // Return from dive to previous camera state
        function returnFromDive() {
            if (cameraReturnStack.length === 0) return;

            const prevState = cameraReturnStack.pop();

            // Start animation back
            cameraAnimating = true;
            cameraAnimStart = performance.now();
            cameraAnimDuration = CAMERA_STATE.transition_ms;
            cameraStartZoom = cameraZoom;
            cameraTargetZoom = prevState.zoom;
            cameraStartPanX = cameraPanX;
            cameraStartPanY = cameraPanY;
            cameraTargetPanX = prevState.panX;
            cameraTargetPanY = prevState.panY;

            cameraMode = prevState.mode;
        }

        // Update camera animation
        function updateCamera(time) {
            if (!cameraAnimating) return;

            const elapsed = time - cameraAnimStart;
            const progress = Math.min(1, elapsed / cameraAnimDuration);
            const eased = easeInOutCubic(progress);

            cameraZoom = cameraStartZoom + (cameraTargetZoom - cameraStartZoom) * eased;
            cameraPanX = cameraStartPanX + (cameraTargetPanX - cameraStartPanX) * eased;
            cameraPanY = cameraStartPanY + (cameraTargetPanY - cameraStartPanY) * eased;

            // Spawn warp particles during dive transitions (middle 60% of animation)
            if (progress > 0.2 && progress < 0.8 && Math.random() < 0.3) {
                const warpColor = cameraMode === 'focus' ? COLORS.broken : COLORS.gold;
                // Spawn particles from edges toward center
                const edge = Math.floor(Math.random() * 4);
                let px, py, vx, vy;
                if (edge === 0) { // left
                    px = 0;
                    py = Math.random() * height;
                    vx = 8 + Math.random() * 4;
                    vy = (Math.random() - 0.5) * 2;
                } else if (edge === 1) { // right
                    px = width;
                    py = Math.random() * height;
                    vx = -8 - Math.random() * 4;
                    vy = (Math.random() - 0.5) * 2;
                } else if (edge === 2) { // top
                    px = Math.random() * width;
                    py = 0;
                    vx = (Math.random() - 0.5) * 2;
                    vy = 8 + Math.random() * 4;
                } else { // bottom
                    px = Math.random() * width;
                    py = height;
                    vx = (Math.random() - 0.5) * 2;
                    vy = -8 - Math.random() * 4;
                }
                particles.push(new Particle(px, py, warpColor, 'emergence'));
            }

            if (progress >= 1) {
                cameraAnimating = false;
            }
        }

        // Apply camera transform to canvas context
        function applyCameraTransform(ctx) {
            ctx.save();
            ctx.translate(cameraPanX, cameraPanY);
            ctx.scale(cameraZoom, cameraZoom);
        }

        // Restore camera transform
        function restoreCameraTransform(ctx) {
            ctx.restore();
        }

        function hexToVec4(hex) {
            const raw = (hex || '#D4AF37').replace('#', '');
            const value = raw.length === 3
                ? raw.split('').map(c => c + c).join('')
                : raw.padEnd(6, '0').slice(0, 6);
            const r = parseInt(value.slice(0, 2), 16) / 255;
            const g = parseInt(value.slice(2, 4), 16) / 255;
            const b = parseInt(value.slice(4, 6), 16) / 255;
            return [r, g, b, 1.0];
        }

        class ParticleGPUField {
            constructor(canvas, width, height, perf) {
                this.canvas = canvas;
                this.width = width;
                this.height = height;
                this.perf = perf;
                this.device = null;
                this.adapter = null;
                this.context = null;
                this.format = null;
                this.computePipeline = null;
                this.renderPipeline = null;
                this.bindGroup = null;
                this.particleBuffer = null;
                this.uniformBuffer = null;
                this.activeCount = 0;
                this.maxParticles = 0;
                this.lastTime = null;
                this.initialized = false;
                this.uniformArrayBuffer = new ArrayBuffer(32 * 4);
                this.uniformF32 = new Float32Array(this.uniformArrayBuffer);
                this.uniformU32 = new Uint32Array(this.uniformArrayBuffer);
                this.params = {
                    density: 0.25,
                    orbit: 0.0,
                    layer: 1.0,
                    audioLow: 0.0,
                    audioMid: 0.0,
                    audioHigh: 0.0,
                    focusX: width * 0.5,
                    focusY: height * 0.5,
                    focusStrength: 0.0,
                    seed: 1.0,
                    frameColor: hexToVec4('#D4AF37'),
                };
            }

            async init() {
                if (!navigator.gpu) {
                    throw new Error('WebGPU not available in this browser');
                }

                this.adapter = await navigator.gpu.requestAdapter();
                if (!this.adapter) {
                    throw new Error('No WebGPU adapter available');
                }

                this.device = await this.adapter.requestDevice();
                this.context = this.canvas.getContext('webgpu');
                if (!this.context) {
                    throw new Error('Unable to acquire WebGPU context');
                }

                this.format = navigator.gpu.getPreferredCanvasFormat();
                const dpr = window.devicePixelRatio || 1;
                this.canvas.width = Math.floor(this.width * dpr);
                this.canvas.height = Math.floor(this.height * dpr);
                this.canvas.style.width = this.width + 'px';
                this.canvas.style.height = this.height + 'px';
                this.context.configure({
                    device: this.device,
                    format: this.format,
                    alphaMode: 'premultiplied',
                });

                this.maxParticles = Math.max(
                    65536,
                    Math.min(this.perf.particleGpuTargetCap || 1000000, 1000000)
                );

                const strideFloats = 8; // pos.xy vel.xy life status phase pad
                const initial = new Float32Array(this.maxParticles * strideFloats);
                for (let i = 0; i < this.maxParticles; i++) {
                    const base = i * strideFloats;
                    const r0 = fract(Math.sin((i + 1) * 12.9898) * 43758.5453);
                    const r1 = fract(Math.sin((i + 1) * 78.233) * 24634.6345);
                    const r2 = fract(Math.sin((i + 1) * 35.719) * 13579.2468);
                    const r3 = fract(Math.sin((i + 1) * 92.157) * 98765.4321);
                    const r4 = fract(Math.sin((i + 1) * 14.313) * 54231.1111);

                    initial[base + 0] = r0 * this.width;
                    initial[base + 1] = r1 * this.height;
                    initial[base + 2] = (r2 - 0.5) * 0.7;
                    initial[base + 3] = (r3 - 0.5) * 0.7;
                    initial[base + 4] = 0.2 + r4 * 0.8;
                    initial[base + 5] = i % 3; // 0=working 1=broken 2=combat
                    initial[base + 6] = r3 * 6.2831853;
                    initial[base + 7] = 0.0;
                }

                this.particleBuffer = this.device.createBuffer({
                    size: initial.byteLength,
                    usage: GPUBufferUsage.STORAGE | GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
                });
                this.device.queue.writeBuffer(this.particleBuffer, 0, initial);

                this.uniformBuffer = this.device.createBuffer({
                    size: this.uniformArrayBuffer.byteLength,
                    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
                });

                const shader = this.device.createShaderModule({
                    code: /* wgsl */`
struct Particle {
    pos: vec2<f32>,
    vel: vec2<f32>,
    life: f32,
    status: f32,
    phase: f32,
    pad: f32,
};

struct Params {
    time: f32,
    dt: f32,
    width: f32,
    height: f32,
    density: f32,
    orbit: f32,
    layer: f32,
    audioLow: f32,
    audioMid: f32,
    audioHigh: f32,
    focusX: f32,
    focusY: f32,
    focusStrength: f32,
    seed: f32,
    activeCount: u32,
    pad0: u32,
    pad1: u32,
    pad2: u32,
    frameColor: vec4<f32>,
};

struct VSOut {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
};

@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> u: Params;

fn hash(x: f32) -> f32 {
    return fract(sin(x * 12.9898 + u.seed * 78.233) * 43758.5453);
}

@compute @workgroup_size(256)
fn cs_main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let i = gid.x;
    if (i >= u.activeCount) { return; }

    var p = particles[i];
    let center = vec2<f32>(u.width * 0.5, u.height * 0.5);
    let toCenter = center - p.pos;
    let dist = max(length(toCenter), 0.001);
    let dir = toCenter / dist;
    let tangent = vec2<f32>(-dir.y, dir.x);

    var accel = dir * (0.012 + u.audioLow * 0.02) * u.layer;
    accel = accel + tangent * (0.008 + u.orbit * 0.03);

    let focus = vec2<f32>(u.focusX, u.focusY);
    let toFocus = focus - p.pos;
    let dFocus = max(length(toFocus), 0.001);
    accel = accel + normalize(toFocus) * (u.focusStrength * 0.08 / max(dFocus * 0.02, 1.0));

    p.phase = p.phase + (0.008 + u.audioHigh * 0.01);
    let swirl = vec2<f32>(cos(p.phase), sin(p.phase)) * (0.002 + u.audioMid * 0.004);

    p.vel = (p.vel + accel + swirl) * 0.992;
    p.pos = p.pos + p.vel * (1.0 + u.audioMid * 1.6);

    if (p.pos.x < 0.0) { p.pos.x = 0.0; p.vel.x = abs(p.vel.x); }
    if (p.pos.x > u.width) { p.pos.x = u.width; p.vel.x = -abs(p.vel.x); }
    if (p.pos.y < 0.0) { p.pos.y = 0.0; p.vel.y = abs(p.vel.y); }
    if (p.pos.y > u.height) { p.pos.y = u.height; p.vel.y = -abs(p.vel.y); }

    p.life = p.life - (0.0009 + u.audioHigh * 0.0015 + (1.0 - u.density) * 0.0005);
    if (p.life <= 0.0) {
        let fi = f32(i);
        p.pos = vec2<f32>(hash(fi + 1.1) * u.width, hash(fi + 2.7) * u.height);
        p.vel = vec2<f32>((hash(fi + 3.3) - 0.5) * 0.5, (hash(fi + 4.9) - 0.5) * 0.5);
        p.life = 0.2 + hash(fi + 5.5) * 0.8;
        p.status = f32(i % 3u);
        p.phase = hash(fi + 8.8) * 6.2831853;
    }

    particles[i] = p;
}

@vertex
fn vs_main(
    @location(0) pos: vec2<f32>,
    @location(1) life: f32,
    @location(2) status: f32
) -> VSOut {
    var out: VSOut;
    let px = (pos.x / u.width) * 2.0 - 1.0;
    let py = 1.0 - (pos.y / u.height) * 2.0;
    out.position = vec4<f32>(px, py, 0.0, 1.0);

    var statusColor = vec3<f32>(0.83, 0.69, 0.22);
    if (status > 1.5) {
        statusColor = vec3<f32>(0.62, 0.31, 0.87);
    } else if (status > 0.5) {
        statusColor = vec3<f32>(0.12, 0.74, 0.92);
    }

    let mixed = mix(statusColor, u.frameColor.xyz, 0.38);
    let alpha = clamp(life * (0.35 + u.density * 0.85), 0.05, 0.95);
    out.color = vec4<f32>(mixed, alpha);
    return out;
}

@fragment
fn fs_main(in: VSOut) -> @location(0) vec4<f32> {
    return in.color;
}
                    `,
                });

                this.computePipeline = this.device.createComputePipeline({
                    layout: 'auto',
                    compute: {
                        module: shader,
                        entryPoint: 'cs_main',
                    },
                });

                this.renderPipeline = this.device.createRenderPipeline({
                    layout: 'auto',
                    vertex: {
                        module: shader,
                        entryPoint: 'vs_main',
                        buffers: [
                            {
                                arrayStride: 8 * 4,
                                attributes: [
                                    { shaderLocation: 0, offset: 0, format: 'float32x2' },
                                    { shaderLocation: 1, offset: 4 * 4, format: 'float32' },
                                    { shaderLocation: 2, offset: 5 * 4, format: 'float32' },
                                ],
                            },
                        ],
                    },
                    fragment: {
                        module: shader,
                        entryPoint: 'fs_main',
                        targets: [
                            {
                                format: this.format,
                                blend: {
                                    color: {
                                        srcFactor: 'src-alpha',
                                        dstFactor: 'one-minus-src-alpha',
                                        operation: 'add',
                                    },
                                    alpha: {
                                        srcFactor: 'one',
                                        dstFactor: 'one-minus-src-alpha',
                                        operation: 'add',
                                    },
                                },
                            },
                        ],
                    },
                    primitive: {
                        topology: 'point-list',
                    },
                });

                this.bindGroup = this.device.createBindGroup({
                    layout: this.computePipeline.getBindGroupLayout(0),
                    entries: [
                        { binding: 0, resource: { buffer: this.particleBuffer } },
                        { binding: 1, resource: { buffer: this.uniformBuffer } },
                    ],
                });

                this.setDensityFromSlider(25);
                this.initialized = true;
            }

            setDensityFromSlider(sliderValue) {
                const normalized = clamp01((sliderValue || 0) / 100);
                this.params.density = Math.max(0.001, normalized);
                this.activeCount = Math.max(
                    4096,
                    Math.min(this.maxParticles, Math.floor(this.maxParticles * this.params.density))
                );
            }

            setOrbit(active) {
                this.params.orbit = active ? 1.0 : 0.0;
            }

            setLayer(multiplier) {
                this.params.layer = Math.max(0.4, Math.min(2.0, multiplier || 1.0));
            }

            setAudio(low, mid, high) {
                this.params.audioLow = Math.max(0, low || 0);
                this.params.audioMid = Math.max(0, mid || 0);
                this.params.audioHigh = Math.max(0, high || 0);
            }

            setFrameColorMode(mode, isReady) {
                let hex = '#D4AF37';
                if (mode === 'combat') hex = '#9D4EDD';
                else if (mode === 'teal') hex = '#1fbdea';
                else if (!isReady) hex = '#1fbdea';
                this.params.frameColor = hexToVec4(hex);
            }

            setFocus(x, y, strength = 0.0) {
                this.params.focusX = x;
                this.params.focusY = y;
                this.params.focusStrength = Math.max(0.0, Math.min(1.0, strength));
            }

            clearFocus() {
                this.params.focusStrength = 0.0;
            }

            reseed() {
                this.params.seed += 1.0;
            }

            clear() {
                this.activeCount = 0;
            }

            writeUniforms(time, dt) {
                this.uniformF32[0] = time * 0.001;
                this.uniformF32[1] = dt;
                this.uniformF32[2] = this.width;
                this.uniformF32[3] = this.height;
                this.uniformF32[4] = this.params.density;
                this.uniformF32[5] = this.params.orbit;
                this.uniformF32[6] = this.params.layer;
                this.uniformF32[7] = this.params.audioLow;
                this.uniformF32[8] = this.params.audioMid;
                this.uniformF32[9] = this.params.audioHigh;
                this.uniformF32[10] = this.params.focusX;
                this.uniformF32[11] = this.params.focusY;
                this.uniformF32[12] = this.params.focusStrength;
                this.uniformF32[13] = this.params.seed;
                this.uniformU32[14] = this.activeCount >>> 0;
                this.uniformU32[15] = 0;
                this.uniformU32[16] = 0;
                this.uniformU32[17] = 0;
                this.uniformF32[18] = this.params.frameColor[0];
                this.uniformF32[19] = this.params.frameColor[1];
                this.uniformF32[20] = this.params.frameColor[2];
                this.uniformF32[21] = this.params.frameColor[3];

                this.device.queue.writeBuffer(this.uniformBuffer, 0, this.uniformArrayBuffer);
            }

            step(time) {
                if (!this.initialized || !this.device || !this.context) return;
                const dt = this.lastTime == null
                    ? 0.016
                    : Math.min(0.05, Math.max(0.001, (time - this.lastTime) / 1000));
                this.lastTime = time;
                this.writeUniforms(time, dt);

                const encoder = this.device.createCommandEncoder();

                if (this.activeCount > 0) {
                    const computePass = encoder.beginComputePass();
                    computePass.setPipeline(this.computePipeline);
                    computePass.setBindGroup(0, this.bindGroup);
                    computePass.dispatchWorkgroups(Math.ceil(this.activeCount / 256));
                    computePass.end();
                }

                const colorView = this.context.getCurrentTexture().createView();
                const renderPass = encoder.beginRenderPass({
                    colorAttachments: [
                        {
                            view: colorView,
                            loadOp: 'clear',
                            storeOp: 'store',
                            clearValue: { r: 0, g: 0, b: 0, a: 0 },
                        },
                    ],
                });
                renderPass.setPipeline(this.renderPipeline);
                renderPass.setBindGroup(0, this.bindGroup);
                renderPass.setVertexBuffer(0, this.particleBuffer);
                if (this.activeCount > 0) {
                    renderPass.draw(this.activeCount, 1, 0, 0);
                }
                renderPass.end();

                this.device.queue.submit([encoder.finish()]);
            }
        }

        function fract(v) {
            return v - Math.floor(v);
        }

        const COLORS = {
            void: '#0A0A0B',
            working: '#D4AF37',
            broken: '#1fbdea',
            combat: '#9D4EDD',
            wireframe: '#333333',
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
        const nodeIndexById = {};
        nodes.forEach((n, idx) => {
            nodeById[n.id] = n;
            nodeIndexById[n.id] = idx;
        });
        const outgoingNeighbors = {};
        const incomingNeighbors = {};
        edges.forEach((edge) => {
            if (!outgoingNeighbors[edge.source]) outgoingNeighbors[edge.source] = [];
            if (!incomingNeighbors[edge.target]) incomingNeighbors[edge.target] = [];
            outgoingNeighbors[edge.source].push(edge.target);
            incomingNeighbors[edge.target].push(edge.source);
        });

        function edgeKey(edge) {
            return `${edge.source}->${edge.target}:${edge.lineNumber || 0}`;
        }

        // ================================================================
        // CONTROL PANEL STATE
        // ================================================================
        let activeFrameColor = 'gold';  // 'gold' | 'teal' | 'combat'
        let viewMode = '2d';  // '2d' | '3d'
        let particlesPerUnit = 5;  // densit8: 1-10, default 5
        let particleDensityMultiplier = 1.0;
        let barradeauThreshold = 1.0;
        let activeDock8 = false;
        let activeOrbit8 = false;
        let activeLayerIndex = 1;
        const layerLevels = [0.7, 1.0, 1.35];
        let focusedNodeId = null;
        let selectedConnection = null;
        let selectedConnectionKey = null;
        let highlightedNodeIds = new Set();
        let highlightedEdgeKeys = new Set();
        let lastConnectionActionResult = null;
        let connectionActionHistory = [];

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
                barradeauThreshold: barradeauThreshold,
                layerIndex: activeLayerIndex,
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
            const threshold = lerpValue(
                morphStartState.barradeauThreshold || 1.0,
                morphTarget.barradeauThreshold || 1.0,
                t
            );

            // Update sliders
            document.getElementById('waveAmp').value = amp;
            document.getElementById('waveSpeed').value = speed;
            document.getElementById('particleDensity').value = density;

            // Update actual values
            waveField.ampBase = amp;
            waveField.speedBase = speed / 10000;
            particleDensityMultiplier = Math.min(4, density / 5);
            barradeauThreshold = threshold;

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
                activeLayerIndex = morphTarget.layerIndex || activeLayerIndex;
            }
        }

        // ================================================================
        // AUDIO-REACTIVE SYSTEM
        // ================================================================
        let audioContext = null;
        let analyser = null;
        let audioSource = null;
        let audioDataArray = null;
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
                    analyser.fftSize = PERF.audioFftSize;
                    analyser.smoothingTimeConstant = PERF.audioSmoothing;
                    audioDataArray = new Uint8Array(analyser.frequencyBinCount);

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
                audioDataArray = null;
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
            if (!audioDataArray || audioDataArray.length !== bufferLength) {
                audioDataArray = new Uint8Array(bufferLength);
            }
            analyser.getByteFrequencyData(audioDataArray);

            const sensitivity = parseFloat(document.getElementById('audioSensitivity').value) / 50;

            // Calculate frequency bands (low: bass, mid: mids, high: treble)
            const lowEnd = Math.floor(bufferLength * 0.1);   // 0-10% = bass
            const midStart = Math.floor(bufferLength * 0.1);
            const midEnd = Math.floor(bufferLength * 0.5);   // 10-50% = mids
            const highStart = Math.floor(bufferLength * 0.5);

            // Average each band
            let lowSum = 0, midSum = 0, highSum = 0;
            for (let i = 0; i < lowEnd; i++) lowSum += audioDataArray[i];
            for (let i = midStart; i < midEnd; i++) midSum += audioDataArray[i];
            for (let i = highStart; i < bufferLength; i++) highSum += audioDataArray[i];

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
            const baseDensity = parseFloat(document.getElementById('particleDensity').value) / 5;
            particleDensityMultiplier = Math.min(4, baseDensity + frequencyData.mid * 2);

            // High (treble) → Wave speed boost
            const baseSpeed = parseFloat(document.getElementById('waveSpeed').value) / 10000;
            waveField.speedBase = Math.min(0.006, baseSpeed + frequencyData.high * 0.002);

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
            toggle.textContent = panel.classList.contains('collapsed') ? '>' : 'v';
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
            if (backendState.gpuEnabled && backendState.gpuField) {
                backendState.gpuField.setFrameColorMode(activeFrameColor, currentPhase === PHASES.READY);
            }
        }

        function updateWave() {
            const amp = parseFloat(document.getElementById('waveAmp').value);
            const speed = parseFloat(document.getElementById('waveSpeed').value);
            waveField.ampBase = amp;
            waveField.speedBase = speed / 10000;  // Scale to reasonable range
        }

        function updateDensit8() {
            const density = parseFloat(document.getElementById('particleDensity').value);
            particlesPerUnit = density;  // 1-10 range
            particleDensityMultiplier = Math.min(4, density / 5);  // Normalize: default 5 = 1.0
            // Map density slider to edge filter threshold (Barradeau-style)
            barradeauThreshold = 0.5 + (density / 10) * 2.0;
            if (backendState.gpuEnabled && backendState.gpuField) {
                backendState.gpuField.setDensityFromSlider(density);
            }
        }

        function generate3DBuildingData() {
            const buildings = [];
            const scale = 0.05;
            
            for (const node of nodes) {
                const particles = [];
                const edges = [];
                
                const footprint = Math.max(1, (node.footprint || 2) * scale);
                const height = Math.max(1, (node.buildingHeight || 5) * scale);
                const centerX = (node.x - config.width / 2) * scale;
                const centerZ = (node.y - config.height / 2) * scale;
                
                const layers = 8;
                const particlesPerLayer = Math.max(4, Math.floor(footprint * 8));
                
                for (let layer = 0; layer < layers; layer++) {
                    const y = (layer / layers) * height;
                    const layerRadius = footprint * (1 - layer * 0.03);
                    const layerOpacity = 0.5 + (layer / layers) * 0.5;
                    
                    for (let i = 0; i < particlesPerLayer; i++) {
                        const angle = (i / particlesPerLayer) * Math.PI * 2;
                        const variance = 0.85 + Math.random() * 0.3;
                        const r = layerRadius * variance;
                        
                        particles.push({
                            x: centerX + Math.cos(angle) * r,
                            y: y,
                            z: centerZ + Math.sin(angle) * r,
                            opacity: layerOpacity,
                            size: 0.3 + Math.random() * 0.2
                        });
                    }
                    
                    if (layer < layers - 1) {
                        const nextY = ((layer + 1) / layers) * height;
                        const nextRadius = footprint * (1 - (layer + 1) * 0.03);
                        
                        for (let i = 0; i < 4; i++) {
                            const angle = (i / 4) * Math.PI * 2;
                            const r1 = layerRadius * 0.9;
                            const r2 = nextRadius * 0.9;
                            
                            edges.push({
                                a: { x: centerX + Math.cos(angle) * r1, y: y, z: centerZ + Math.sin(angle) * r1 },
                                b: { x: centerX + Math.cos(angle) * r2, y: nextY, z: centerZ + Math.sin(angle) * r2 }
                            });
                        }
                    }
                }
                
                buildings.push({
                    path: node.path,
                    status: node.status,
                    particles: particles,
                    edges: edges
                });
            }
            
            return buildings;
        }

        function normalizeBuildingArray(payload) {
            if (Array.isArray(payload)) return payload;
            if (payload && Array.isArray(payload.buildings)) return payload.buildings;
            return [];
        }

        function estimateObjectBytes(value) {
            try {
                return new TextEncoder().encode(JSON.stringify(value)).length;
            } catch (e) {
                const fallback = JSON.stringify(value);
                return fallback ? fallback.length : 0;
            }
        }

        async function streamLoad3DBuildings(scene, buildings, bytesPerSecond) {
            if (!scene || !Array.isArray(buildings)) return;

            scene.clearBuildings();
            const safeRate = Math.max(100000, Number(bytesPerSecond) || 5000000);
            let loaded = 0;
            let budget = 0;
            let lastTick = performance.now();

            while (loaded < buildings.length) {
                const now = performance.now();
                const deltaSeconds = Math.max(0, (now - lastTick) / 1000);
                lastTick = now;
                budget += safeRate * deltaSeconds;

                // Ensure forward progress even on very small/slow frame deltas.
                if (budget < 1) budget = 1;

                let addedThisFrame = 0;
                while (loaded < buildings.length) {
                    const building = buildings[loaded];
                    const estimatedBytes = Math.max(1, estimateObjectBytes(building));
                    if (estimatedBytes > budget && addedThisFrame > 0) break;
                    if (estimatedBytes > budget && addedThisFrame === 0) {
                        // Permit one oversized item for liveness.
                        budget = 0;
                    } else {
                        budget -= estimatedBytes;
                    }
                    scene.addBuilding(building, true);
                    loaded += 1;
                    addedThisFrame += 1;
                }

                phaseEl.textContent = `3D emergence ${loaded}/${buildings.length}`;
                await new Promise((resolve) => requestAnimationFrame(resolve));
            }

            phaseEl.textContent = '3D ready';
        }

        function setViewMode(mode) {
            console.log('[setViewMode] Switching to:', mode);
            viewMode = mode;
            document.getElementById('view2dBtn').classList.toggle('active', mode === '2d');
            document.getElementById('view3dBtn').classList.toggle('active', mode === '3d');
            
            const city2d = document.getElementById('city');
            const city3d = document.getElementById('city-gpu');
            
            if (mode === '3d') {
                city2d.style.display = 'none';
                city3d.style.display = 'block';
                city3d.style.pointerEvents = 'auto';
                phaseEl.textContent = '3D mode';
                
                if (!window.codeCity3D) {
                    try {
                        console.log('[3D] Initializing CodeCityScene...');
                        const container = document.getElementById('city-gpu');
                        
                        if (typeof CodeCityScene === 'undefined') {
                            throw new Error('CodeCityScene class not loaded - check script loading');
                        }

                        window.codeCity3D = new CodeCityScene(container);
                        console.log('[3D] CodeCityScene created successfully');

                        let buildingArray = normalizeBuildingArray(window.BUILDING_DATA);
                        if (!buildingArray.length) {
                            buildingArray = generate3DBuildingData();
                            window.BUILDING_DATA = {
                                buildings: buildingArray,
                                metadata: {
                                    source: 'client-generated',
                                    generatedAt: new Date().toISOString()
                                }
                            };
                        }

                        console.log('[3D] Streaming building data:', buildingArray.length, 'buildings @', BUILDING_STREAM_BPS, 'bytes/sec');
                        window.codeCity3D.start();
                        streamLoad3DBuildings(window.codeCity3D, buildingArray, BUILDING_STREAM_BPS)
                            .catch((streamError) => {
                                console.error('[3D] Stream load error:', streamError);
                            });
                        
                        const densitySlider = document.getElementById('particleDensity');
                        if (densitySlider && window.codeCity3D.setParticleDensity) {
                            window.codeCity3D.setParticleDensity(densitySlider.value / 5);
                        }
                        
                        console.log('[3D] 3D mode initialized successfully');
                    } catch (error) {
                        console.error('[3D] Failed to initialize 3D mode:', error);
                        alert('3D mode failed: ' + error.message);
                    }
                }
            } else {
                city2d.style.display = 'block';
                city3d.style.display = 'none';
                city3d.style.pointerEvents = 'none';
                phaseEl.textContent = currentPhase === PHASES.READY ? 'ready' : 'tuning...';
            }
        }

        function toggleDock8() {
            const panel = document.getElementById('controls');
            activeDock8 = !activeDock8;
            panel.classList.toggle('docked-bottom', activeDock8);
        }

        function toggleOrbit8() {
            activeOrbit8 = !activeOrbit8;
            phaseEl.textContent = activeOrbit8 ? 'orbit8 active' : (currentPhase === PHASES.READY ? 'ready' : phaseEl.textContent);
        }

        function focus8() {
            if (!focusedNodeId) return;
            const node = nodeById[focusedNodeId];
            if (!node) return;

            // Emphasize selected node and seed a local emergence burst
            spawnEmergenceParticles(node.x, node.y, 20);
            setFrameColor(node.status === 'broken' ? 'teal' : (node.status === 'combat' ? 'combat' : 'gold'));
            if (backendState.gpuEnabled && backendState.gpuField) {
                backendState.gpuField.setFocus(node.x, node.y, 1.0);
            }
            phaseEl.textContent = 'focus8 ' + node.path.split('/').pop();
        }

        function cycleLayer8() {
            activeLayerIndex = (activeLayerIndex + 1) % layerLevels.length;
            const level = layerLevels[activeLayerIndex];
            phaseEl.textContent = 'layer8 x' + level.toFixed(2);
        }

        function getNodeRenderPosition(nodeId) {
            const node = nodeById[nodeId];
            const idx = nodeIndexById[nodeId];
            const state = (idx !== undefined) ? nodeStates[idx] : null;
            if (!node) return null;
            if (currentPhase === PHASES.READY || !state) {
                return { x: node.x, y: node.y };
            }
            return { x: state.currentX, y: state.currentY };
        }

        function distanceToSegment(px, py, x1, y1, x2, y2) {
            const vx = x2 - x1;
            const vy = y2 - y1;
            const wx = px - x1;
            const wy = py - y1;
            const lenSq = vx * vx + vy * vy;
            if (lenSq <= 0.000001) {
                const dx = px - x1;
                const dy = py - y1;
                return Math.sqrt(dx * dx + dy * dy);
            }
            let t = (wx * vx + wy * vy) / lenSq;
            t = Math.max(0, Math.min(1, t));
            const projX = x1 + t * vx;
            const projY = y1 + t * vy;
            const dx = px - projX;
            const dy = py - projY;
            return Math.sqrt(dx * dx + dy * dy);
        }

        function quadraticPoint(t, x1, y1, cx, cy, x2, y2) {
            const omt = 1 - t;
            const x = omt * omt * x1 + 2 * omt * t * cx + t * t * x2;
            const y = omt * omt * y1 + 2 * omt * t * cy + t * t * y2;
            return { x, y };
        }

        function distanceToQuadraticCurve(px, py, x1, y1, cx, cy, x2, y2) {
            let minDist = Number.POSITIVE_INFINITY;
            let prev = { x: x1, y: y1 };
            const steps = 20;
            for (let i = 1; i <= steps; i++) {
                const t = i / steps;
                const next = quadraticPoint(t, x1, y1, cx, cy, x2, y2);
                const d = distanceToSegment(px, py, prev.x, prev.y, next.x, next.y);
                if (d < minDist) minDist = d;
                prev = next;
            }
            return minDist;
        }

        function bfsReach(startNodeId, adjacencyMap, maxDepth = 6) {
            const reached = new Set([startNodeId]);
            const queue = [{ id: startNodeId, depth: 0 }];

            while (queue.length > 0) {
                const current = queue.shift();
                if (!current || current.depth >= maxDepth) continue;

                const neighbors = adjacencyMap[current.id] || [];
                for (const nextId of neighbors) {
                    if (!reached.has(nextId) && nodeById[nextId]) {
                        reached.add(nextId);
                        queue.push({ id: nextId, depth: current.depth + 1 });
                    }
                }
            }
            return reached;
        }

        function computeSignalPath(edge) {
            const forward = bfsReach(edge.source, outgoingNeighbors, 6);
            const backward = bfsReach(edge.target, incomingNeighbors, 6);

            const signalNodes = new Set([edge.source, edge.target]);
            forward.forEach((id) => {
                if (backward.has(id)) signalNodes.add(id);
            });

            const signalEdges = new Set();
            for (const e of edges) {
                if (forward.has(e.source) && backward.has(e.target) &&
                    signalNodes.has(e.source) && signalNodes.has(e.target)) {
                    signalEdges.add(edgeKey(e));
                }
            }
            signalEdges.add(edgeKey(edge));

            return { signalNodes, signalEdges };
        }

        function escapeHtml(value) {
            const text = value == null ? '' : String(value);
            return text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function renderConnectionActionResult(edge) {
            if (!lastConnectionActionResult) return '';

            const r = lastConnectionActionResult;
            if (r.source && r.source !== edge.source) return '';
            if (r.target && r.target !== edge.target) return '';

            const statusClass = r.ok ? 'ok' : 'blocked';
            const label = r.action === 'apply_rewire' ? 'Patchbay Apply' : 'Patchbay Dry-Run';
            const msg = escapeHtml(r.message || (r.ok ? 'Completed.' : 'Blocked.'));

            const issues = Array.isArray(r.issues) ? r.issues : [];
            const warnings = Array.isArray(r.warnings) ? r.warnings : [];
            const issueRows = issues.slice(0, 3).map((item) => `<div class="issue">• ${escapeHtml(item)}</div>`).join('');
            const warnRows = warnings.slice(0, 3).map((item) => `<div class="warn">• ${escapeHtml(item)}</div>`).join('');

            return `
                <div class="action-result ${statusClass}">
                    <div class="title">${escapeHtml(label)}</div>
                    <div class="msg">${msg}</div>
                    ${issueRows}
                    ${warnRows}
                </div>
            `;
        }

        function formatHistoryTime(ts) {
            if (!ts) return '--:--:--';
            const d = new Date(ts);
            if (Number.isNaN(d.getTime())) return '--:--:--';
            return d.toLocaleTimeString([], { hour12: false });
        }

        function renderConnectionActionHistory(edge) {
            const history = connectionActionHistory
                .filter((entry) => {
                    if (!entry || !entry.source || !entry.target) return false;
                    return entry.source === edge.source && entry.target === edge.target;
                })
                .slice(0, 5);

            if (!history.length) return '';

            const rows = history.map((entry) => {
                const cls = entry.ok ? 'ok' : 'blocked';
                const action = entry.action === 'apply_rewire' ? 'apply' : 'dry-run';
                const role = entry.actorRole ? ` · ${escapeHtml(entry.actorRole)}` : '';
                const stamp = formatHistoryTime(entry.timestamp);
                const msg = escapeHtml(entry.message || (entry.ok ? 'ok' : 'blocked'));
                return `<div class="entry ${cls}">${stamp} · ${action}${role} · ${msg}</div>`;
            }).join('');

            return `
                <div class="action-history">
                    <div class="title">Recent Patchbay Actions</div>
                    ${rows}
                </div>
            `;
        }

        function getCurrentActorRole() {
            const fromGlobal = (typeof window !== 'undefined' && window.ORCHESTR8_ACTOR_ROLE)
                ? String(window.ORCHESTR8_ACTOR_ROLE)
                : '';
            let fromStorage = '';
            try {
                fromStorage = window.localStorage
                    ? String(window.localStorage.getItem('orchestr8_actor_role') || '')
                    : '';
            } catch (_) {
                fromStorage = '';
            }
            const role = (fromGlobal || fromStorage || 'operator').trim().toLowerCase();
            return role || 'operator';
        }

        function updateConnectionPanel() {
            const panel = document.getElementById('connection-panel');
            if (!selectedConnection) {
                panel.classList.add('hidden');
                panel.innerHTML = '';
                return;
            }

            const orderedNodes = Array.from(highlightedNodeIds).sort((a, b) => a.localeCompare(b));
            const displayNodes = orderedNodes.slice(0, 16);
            const moreCount = Math.max(0, orderedNodes.length - displayNodes.length);

            const status = selectedConnection.resolved ? 'resolved' : 'unresolved';
            const statusColor = selectedConnection.resolved ? '#D4AF37' : '#1fbdea';
            const line = selectedConnection.lineNumber || 0;

            // Extract basenames for cleaner display
            const sourceName = selectedConnection.source.split('/').pop();
            const targetName = selectedConnection.target.split('/').pop();
            const pathRows = displayNodes.map((id) => `<div>• ${id.split('/').pop()}</div>`).join('');
            const suggestedTarget = selectedConnection.target;
            const actionResultHtml = renderConnectionActionResult(selectedConnection);
            const actionHistoryHtml = renderConnectionActionHistory(selectedConnection);
            const applyButtonHtml = PATCHBAY_APPLY_ENABLED
                ? `<button class="action-btn apply" onclick="emitConnectionAction('apply_rewire')">Apply Rewire</button>`
                : `<button class="action-btn apply disabled" disabled title="Set ORCHESTR8_PATCHBAY_APPLY=1 to enable apply">Apply Disabled</button>`;

            panel.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div class="title">Connection Path</div>
                    <button onclick="clearSelectedConnection()" style="background: none; border: none; color: #777; font-size: 16px; cursor: pointer; padding: 0; line-height: 1;">&times;</button>
                </div>
                <div class="row"><strong>from:</strong> ${sourceName}</div>
                <div class="row"><strong>to:</strong> ${targetName}</div>
                <div class="row"><strong>line:</strong> ${line}</div>
                <div class="row"><strong>status:</strong> <span style="color: ${statusColor};">${status}</span></div>
                <div class="path-list">
                    <div><strong>Signal Path Files (${highlightedNodeIds.size})</strong></div>
                    ${pathRows}
                    ${moreCount > 0 ? `<div>... +${moreCount} more</div>` : ''}
                </div>
                <input
                    id="rewire-target-input"
                    class="rewire-input"
                    type="text"
                    placeholder="proposed target path (e.g. IP/contracts/status_merge_policy.py)"
                    value="${suggestedTarget}"
                />
                <div class="actions">
                    <button class="action-btn" onclick="emitConnectionAction('dry_run_rewire')">
                        Patchbay Dry-Run
                    </button>
                    ${applyButtonHtml}
                </div>
                ${actionResultHtml}
                ${actionHistoryHtml}
                <div class="meta">Click empty canvas or press Esc to clear selection.</div>
            `;
            panel.classList.remove('hidden');
        }

        function emitConnectionAction(action) {
            if (!selectedConnection) return;

            if (action === 'apply_rewire' && !PATCHBAY_APPLY_ENABLED) {
                lastConnectionActionResult = {
                    action: 'apply_rewire',
                    ok: false,
                    source: selectedConnection.source,
                    target: selectedConnection.target,
                    actorRole: getCurrentActorRole(),
                    message: 'Apply is disabled. Set ORCHESTR8_PATCHBAY_APPLY=1.',
                    issues: ['Apply is disabled for this session.'],
                    warnings: [],
                    timestamp: new Date().toISOString(),
                };
                connectionActionHistory = [lastConnectionActionResult, ...connectionActionHistory].slice(0, 40);
                updateConnectionPanel();
                phaseEl.textContent = 'patchbay apply disabled';
                return;
            }

            if (action === 'apply_rewire') {
                const confirmed = window.confirm(
                    'Apply patchbay rewire now? This edits the source import line.'
                );
                if (!confirmed) return;
            }

            const targetInput = document.getElementById('rewire-target-input');
            const proposedTarget = targetInput ? targetInput.value.trim() : '';
            const payload = {
                action,
                connection: {
                    source: selectedConnection.source,
                    target: selectedConnection.target,
                    resolved: !!selectedConnection.resolved,
                    lineNumber: selectedConnection.lineNumber || 0,
                    edgeType: selectedConnection.type || 'import',
                },
                proposedTarget: proposedTarget || null,
                actorRole: getCurrentActorRole(),
                signalNodes: Array.from(highlightedNodeIds),
                signalEdges: Array.from(highlightedEdgeKeys),
            };

            window.parent.postMessage(
                {
                    type: 'WOVEN_MAPS_CONNECTION_ACTION',
                    payload,
                },
                '*'
            );

            phaseEl.textContent = action === 'dry_run_rewire'
                ? 'patchbay dry-run requested'
                : 'connection action sent';
        }

        function setSelectedConnection(edge) {
            selectedConnection = edge;
            selectedConnectionKey = edgeKey(edge);
            const signal = computeSignalPath(edge);
            highlightedNodeIds = signal.signalNodes;
            highlightedEdgeKeys = signal.signalEdges;
            updateConnectionPanel();
        }

        function clearSelectedConnection() {
            selectedConnection = null;
            selectedConnectionKey = null;
            highlightedNodeIds = new Set();
            highlightedEdgeKeys = new Set();
            updateConnectionPanel();
        }

        function findEdgeAt(x, y) {
            let best = null;
            let bestDistance = Number.POSITIVE_INFINITY;

            for (const edge of edges) {
                const sourcePos = getNodeRenderPosition(edge.source);
                const targetPos = getNodeRenderPosition(edge.target);
                if (!sourcePos || !targetPos) continue;

                const x1 = sourcePos.x;
                const y1 = sourcePos.y;
                const x2 = targetPos.x;
                const y2 = targetPos.y;
                const dx = x2 - x1;
                const dy = y2 - y1;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 0.0001) continue;

                const curveOffset = Math.min(dist * 0.15, 30);
                const perpX = (-dy / dist) * curveOffset;
                const perpY = (dx / dist) * curveOffset;
                const cx = ((x1 + x2) / 2) + perpX;
                const cy = ((y1 + y2) / 2) + perpY;
                const d = distanceToQuadraticCurve(x, y, x1, y1, cx, cy, x2, y2);

                if (d < bestDistance) {
                    bestDistance = d;
                    best = edge;
                }
            }

            if (best && bestDistance <= 8) return best;
            return null;
        }

        function reEmergence() {
            // Reset emergence state
            currentPhase = PHASES.VOID;
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
            if (backendState.gpuEnabled && backendState.gpuField) {
                backendState.gpuField.reseed();
                backendState.gpuField.setDensityFromSlider(parseFloat(document.getElementById('particleDensity').value));
            }
        }

        function clearParticles() {
            particles.length = 0;
            if (backendState.gpuEnabled && backendState.gpuField) {
                backendState.gpuField.clear();
            }
        }

        function getFrameColor() {
            if (activeFrameColor === 'combat') return COLORS.combat;
            if (activeFrameColor === 'teal') return COLORS.teal;
            // During TRANSITION phase, blend from teal to gold; READY is pure gold
            if (currentPhase === PHASES.READY) return COLORS.gold;
            if (currentPhase === PHASES.TRANSITION) {
                // Blend from teal to gold during transition phase
                const elapsed = performance.now() - emergenceStartTime;
                const transitionStart = PHASE_TIMINGS[PHASES.TRANSITION];
                const transitionEnd = PHASE_TIMINGS[PHASES.READY];
                const t = Math.min(1, (elapsed - transitionStart) / (transitionEnd - transitionStart));
                // Simple blend (could be more sophisticated)
                return COLORS.gold; // For now, just use gold during transition
            }
            return COLORS.teal;
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

        function getNodeVisualRadius(node) {
            const footprint = Number.isFinite(node.footprint)
                ? node.footprint
                : (2 + (Math.max(0, node.loc || 0) * 0.008));
            const centralityBoost = (node.centrality || 0) * 8;
            const footprintRadius = Math.max(2, Math.min(16, footprint * 1.2));
            return footprintRadius + centralityBoost;
        }

        // ================================================================
        // EDGE RENDERING - Real import connections
        // ================================================================
        function drawImportEdges(ctx, time) {
            if (!edges || edges.length === 0) return;

            const elapsed = time - emergenceStartTime;
            const hasSelection = selectedConnectionKey !== null;

            for (const edge of edges) {
                const sourceNode = nodeById[edge.source];
                const targetNode = nodeById[edge.target];
                if (!sourceNode || !targetNode) continue;

                const sourceIdx = nodeIndexById[edge.source];
                const targetIdx = nodeIndexById[edge.target];
                if (sourceIdx === undefined || targetIdx === undefined) continue;

                const sourceState = nodeStates[sourceIdx];
                const targetState = nodeStates[targetIdx];

                // Use current positions during emergence
                const x1 = currentPhase === PHASES.READY ? sourceNode.x : sourceState.currentX;
                const y1 = currentPhase === PHASES.READY ? sourceNode.y : sourceState.currentY;
                const x2 = currentPhase === PHASES.READY ? targetNode.x : targetState.currentX;
                const y2 = currentPhase === PHASES.READY ? targetNode.y : targetState.currentY;

                // Edge alpha based on emergence progress
                const key = edgeKey(edge);
                const isSelected = hasSelection && key === selectedConnectionKey;
                const isInSignalPath = hasSelection && highlightedEdgeKeys.has(key);

                let edgeAlpha = Math.min(sourceState.currentAlpha, targetState.currentAlpha) * 0.4;
                if (hasSelection) {
                    if (isInSignalPath) {
                        edgeAlpha = Math.max(edgeAlpha, isSelected ? 0.95 : 0.72);
                    } else {
                        edgeAlpha *= 0.18;
                    }
                }
                if (edgeAlpha < 0.05) continue;

                ctx.globalAlpha = edgeAlpha;

                // Highlight path in one visual family (no rainbow edge coloring).
                if (hasSelection) {
                    if (isSelected) {
                        ctx.strokeStyle = COLORS.gold;
                        ctx.lineWidth = 2.8;
                    } else if (isInSignalPath) {
                        ctx.strokeStyle = '#F4C430';
                        ctx.lineWidth = 1.9;
                    } else {
                        ctx.strokeStyle = COLORS.edge;
                        ctx.lineWidth = 0.7;
                    }
                    ctx.setLineDash(edge.resolved ? [] : [5, 4]);
                } else {
                    // Canonical color scheme: Gold for resolved, Teal for unresolved
                    if (!edge.resolved) {
                        ctx.strokeStyle = COLORS.teal;  // Teal for broken imports
                        ctx.setLineDash([4, 4]);  // Dashed for broken
                        ctx.lineWidth = 1.0;
                    } else if (edge.bidirectional) {
                        ctx.strokeStyle = COLORS.cycle;  // Red for mutual imports (cycle)
                        ctx.setLineDash([]);
                        ctx.lineWidth = 1.5;
                    } else {
                        ctx.strokeStyle = COLORS.gold;  // Gold for working imports
                        ctx.setLineDash([]);
                        ctx.lineWidth = 0.8;
                    }
                }
                ctx.fillStyle = ctx.strokeStyle;

                // Draw curved edge (quadratic bezier)
                const midX = (x1 + x2) / 2;
                const midY = (y1 + y2) / 2;
                const dx = x2 - x1;
                const dy = y2 - y1;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 0.001) continue;

                // Curve outward perpendicular to the line
                const curveOffset = Math.min(dist * 0.15, 30);
                const perpX = -dy / dist * curveOffset;
                const perpY = dx / dist * curveOffset;

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.quadraticCurveTo(midX + perpX, midY + perpY, x2, y2);
                ctx.stroke();

                // Draw arrowhead
                if (currentPhase === PHASES.READY && edgeAlpha > 0.2) {
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
        const gpuCanvas = document.getElementById('city-gpu');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const stats = document.getElementById('stats');
        const phaseEl = document.getElementById('phase');

        canvas.width = width;
        canvas.height = height;
        gpuCanvas.width = width;
        gpuCanvas.height = height;

        const backendState = {
            mode: 'CPU Canvas',
            gpuEnabled: false,
            gpuField: null,
        };

        async function initParticleBackend() {
            if (!navigator.gpu) {
                backendState.mode = 'CPU Canvas';
                return;
            }
            try {
                const gpuField = new ParticleGPUField(gpuCanvas, width, height, PERF);
                await gpuField.init();
                backendState.gpuField = gpuField;
                backendState.gpuEnabled = true;
                backendState.mode = 'WebGPU';
                gpuCanvas.style.display = 'block';
                canvas.style.opacity = '0.04'; // Keep events on canvas while GPU drives visuals
                console.log('[woven_maps] WebGPU backend enabled');
            } catch (err) {
                backendState.mode = 'CPU Canvas';
                backendState.gpuEnabled = false;
                backendState.gpuField = null;
                gpuCanvas.style.display = 'none';
                console.warn('[woven_maps] WebGPU init failed, using CPU canvas fallback:', err);
            }
        }

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
            <span style="color: #555;">CPU cap ${PERF.particleCpuCap.toLocaleString()}</span>
            <span style="color: #444;">GPU target ${PERF.particleGpuTargetCap.toLocaleString()}</span>
            <span id="backendMode" style="color:#888;">CPU Canvas</span>
            <span id="backendParticles" style="color:#666;">0 particles</span>
        `;
        const backendModeEl = document.getElementById('backendMode');
        const backendParticlesEl = document.getElementById('backendParticles');

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
        // EMERGENCE STATE - PHASE STATE MACHINE
        // ================================================================
        const PHASES = {
            VOID: 'void',              // Black screen, no particles
            AWAKENING: 'awakening',    // First particles appear, scattered
            TUNING: 'tuning',          // Particles begin seeking positions
            COALESCING: 'coalescing',  // Particles converging on targets
            EMERGENCE: 'emergence',    // Final convergence, shape visible
            TRANSITION: 'transition',  // Teal frame → gold frame color shift
            READY: 'ready'             // Fully emerged, stable, interactive
        };

        let currentPhase = PHASES.VOID;
        let emergenceProgress = 0;  // 0 to 1
        let emergenceStartTime = performance.now();
        const emergenceDurationMs = emergenceDuration * 1000;

        // Phase timing configuration (milliseconds from start)
        const PHASE_TIMINGS = {
            [PHASES.VOID]: 0,
            [PHASES.AWAKENING]: 500,
            [PHASES.TUNING]: 2000,
            [PHASES.COALESCING]: 4000,
            [PHASES.EMERGENCE]: 6000,
            [PHASES.TRANSITION]: 7500,
            [PHASES.READY]: 8500
        };

        // Derived emerged state for backward compatibility
        const emerged = () => currentPhase === PHASES.READY;

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
        let frameEmergenceSpawnBudget = PERF.emergenceFrameSpawnCap;
        let frameErrorSpawnBudget = PERF.errorFrameSpawnCap;
        let runtimeEdgeStride = Math.max(1, PERF.edgeStride);

        function refreshSpawnBudgets() {
            frameEmergenceSpawnBudget = PERF.emergenceFrameSpawnCap;
            frameErrorSpawnBudget = PERF.errorFrameSpawnCap;
        }

        function getParticlePressure() {
            return Math.max(0, (particles.length - PERF.particleCpuCap) / PERF.particleCpuCap);
        }

        function allocateSpawn(requested, channel = 'emergence') {
            if (requested <= 0 || particles.length >= PERF.particleCpuCap) return 0;

            const budgetRef = channel === 'error' ? frameErrorSpawnBudget : frameEmergenceSpawnBudget;
            if (budgetRef <= 0) return 0;

            const pressure = getParticlePressure();
            const pressureScale = Math.max(0.05, 1 - pressure * 0.8);
            const capLeft = Math.max(0, PERF.particleCpuCap - particles.length);
            const allowance = Math.max(
                0,
                Math.floor(Math.min(requested, budgetRef, capLeft) * pressureScale)
            );

            if (channel === 'error') {
                frameErrorSpawnBudget -= allowance;
            } else {
                frameEmergenceSpawnBudget -= allowance;
            }

            return allowance;
        }

        class Particle {
            constructor(x, y, color, type = 'error', severity = 'normal') {
                this.x = x;
                this.y = y;
                this.type = type;
                this.color = color;
                this.severity = severity;

                if (type === 'emergence') {
                    // Emergence particles: swirl toward target
                    this.vx = (Math.random() - 0.5) * 2;
                    this.vy = (Math.random() - 0.5) * 2;
                    this.size = 1 + Math.random() * 1.5;
                    this.alpha = 0.5 + Math.random() * 0.3;
                    this.life = 60 + Math.random() * 40;
                    this.friction = 0.98;
                } else {
                    // Error particles: RISE ONLY, fade linearly — no horizontal motion, no breathing
                    // Severity affects speed and height
                    if (severity === 'critical' || severity === 'error') {
                        this.vy = -0.3 - Math.random() * 0.3;  // Faster rise
                        this.size = 1.5 + Math.random() * 2.5;  // Larger
                        this.life = 250 + Math.random() * 150;  // Live longer (rise higher)
                    } else if (severity === 'warning') {
                        this.vy = -0.1 - Math.random() * 0.15;  // Slower rise
                        this.size = 0.8 + Math.random() * 1.2;  // Smaller
                        this.life = 150 + Math.random() * 100;  // Shorter lifetime
                    } else {
                        // Normal/default severity
                        this.vy = -0.15 - Math.random() * 0.25;
                        this.size = 1 + Math.random() * 2;
                        this.life = 200 + Math.random() * 150;
                    }

                    // Small horizontal spread at spawn only — no ongoing oscillation
                    this.vx = (Math.random() - 0.5) * 0.08;
                    this.vxDecay = 0.95;  // Horizontal motion dies quickly

                    this.alpha = 0.4 + Math.random() * 0.4;
                    this.initialAlpha = this.alpha;
                    this.initialLife = this.life;
                }

                // Track source node for per-node particle cap
                this.nodeId = null;
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
                    // RISE/FADE ONLY — no curl, no breathing, no horizontal oscillation
                    // Decay horizontal velocity to zero
                    this.vx *= this.vxDecay;

                    this.x += this.vx;
                    this.y += this.vy;  // Only vertical movement persists

                    this.life--;

                    // Linear fade based on remaining life
                    const lifeFraction = this.life / this.initialLife;
                    this.alpha = this.initialAlpha * lifeFraction;

                    // Size shrinks slightly as particle rises
                    this.size = Math.max(0.3, this.size - 0.002);
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
            const allowance = allocateSpawn(count, 'emergence');
            for (let i = 0; i < allowance; i++) {
                particles.push(new Particle(
                    x + (Math.random() - 0.5) * 20,
                    y + (Math.random() - 0.5) * 20,
                    COLORS.teal,
                    'emergence'
                ));
            }
        }

        // Per-node particle count tracking (max 50 error particles per node)
        const nodeParticleCounts = new Map();

        function getNodeParticleCount(nodeId) {
            if (!nodeParticleCounts.has(nodeId)) {
                nodeParticleCounts.set(nodeId, 0);
            }
            return nodeParticleCounts.get(nodeId);
        }

        function incrementNodeParticles(nodeId) {
            const current = getNodeParticleCount(nodeId);
            nodeParticleCounts.set(nodeId, current + 1);
        }

        function decrementNodeParticles(nodeId) {
            const current = getNodeParticleCount(nodeId);
            if (current > 0) {
                nodeParticleCounts.set(nodeId, current - 1);
            }
        }

        function spawnErrorParticles(node) {
            // Allow both broken and combat nodes to spawn error particles
            if (node.status !== 'broken' && node.status !== 'combat') return;

            // Check per-node particle cap (50 particles max per node)
            const nodeId = node.path || node.id || `${node.x},${node.y}`;
            if (getNodeParticleCount(nodeId) >= 50) return;

            // Calculate emission intensity based on error count
            const errorCount = (node.errors?.length || 0) + (node.healthErrors?.length || 0);
            const baseRate = 1;
            const intensityMultiplier = Math.min(5, errorCount || 1);
            const requested = Math.min(Math.ceil(baseRate * intensityMultiplier), 8);

            const allowance = allocateSpawn(requested, 'error');
            if (allowance <= 0) return;

            // Color based on node status
            const particleColor = node.status === 'combat' ? COLORS.combat : COLORS.broken;

            // Spawn particles with severity-based variation
            for (let i = 0; i < allowance; i++) {
                // Determine severity from healthErrors if available
                let severity = 'normal';
                if (node.healthErrors && node.healthErrors.length > 0) {
                    const randomError = node.healthErrors[Math.floor(Math.random() * node.healthErrors.length)];
                    severity = randomError.severity || 'normal';
                }

                const particle = new Particle(
                    node.x + (Math.random() - 0.5) * 12,
                    node.y + (Math.random() - 0.5) * 4,
                    particleColor,
                    'error',
                    severity
                );
                particle.nodeId = nodeId;
                particles.push(particle);
                incrementNodeParticles(nodeId);
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

            for (let idx = 0; idx < delaunayEdges.length; idx += runtimeEdgeStride) {
                const edge = delaunayEdges[idx];
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
            // Update camera animation
            updateCamera(time);

            // Update keyframe morphing
            updateMorph();

            // Update audio-reactive values
            updateAudioReactive();
            refreshSpawnBudgets();
            const particlePressure = getParticlePressure();
            runtimeEdgeStride = Math.max(
                1,
                PERF.edgeStride + Math.min(3, Math.floor(particlePressure * 3))
            );

            // Update emergence progress
            const elapsed = time - emergenceStartTime;
            emergenceProgress = Math.min(1, elapsed / emergenceDurationMs);
            const easedProgress = easeOutCubic(emergenceProgress);
            const layerMultiplier = layerLevels[activeLayerIndex];

            // Update phase based on elapsed time
            if (currentPhase !== PHASES.READY) {
                if (elapsed >= PHASE_TIMINGS[PHASES.READY]) {
                    currentPhase = PHASES.READY;
                    container.classList.add('emerged');
                    phaseEl.classList.add('emerged');
                    phaseEl.textContent = 'ready';
                } else if (elapsed >= PHASE_TIMINGS[PHASES.TRANSITION]) {
                    currentPhase = PHASES.TRANSITION;
                    phaseEl.textContent = 'transition';
                } else if (elapsed >= PHASE_TIMINGS[PHASES.EMERGENCE]) {
                    currentPhase = PHASES.EMERGENCE;
                    phaseEl.textContent = 'emergence';
                } else if (elapsed >= PHASE_TIMINGS[PHASES.COALESCING]) {
                    currentPhase = PHASES.COALESCING;
                    phaseEl.textContent = 'coalescing';
                } else if (elapsed >= PHASE_TIMINGS[PHASES.TUNING]) {
                    currentPhase = PHASES.TUNING;
                    phaseEl.textContent = 'tuning';
                } else if (elapsed >= PHASE_TIMINGS[PHASES.AWAKENING]) {
                    currentPhase = PHASES.AWAKENING;
                    phaseEl.textContent = 'awakening';
                }
            }

            // orbit8 overview mode perturbs wave sources for panoramic motion
            if (activeOrbit8) {
                const orbit = time * 0.00025;
                waveField.sourceLeftX = width * 0.2 + Math.cos(orbit) * width * 0.12;
                waveField.sourceRightX = width * 0.8 + Math.sin(orbit) * width * 0.12;
            } else {
                waveField.sourceLeftX = width * 0.2;
                waveField.sourceRightX = width * 0.8;
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
                if (currentPhase !== PHASES.READY && adjustedProgress > 0.1 && adjustedProgress < 0.9) {
                    const spawnChance = (0.02 + waveStrength * 0.03) * particleDensityMultiplier * Math.max(0.15, 1 - particlePressure * 0.7);
                    if (Math.random() < spawnChance) {
                        spawnEmergenceParticles(state.currentX, state.currentY, 2);
                    }
                }
            }

            if (backendState.gpuEnabled && backendState.gpuField) {
                const gpu = backendState.gpuField;
                gpu.setDensityFromSlider(parseFloat(document.getElementById('particleDensity').value));
                gpu.setOrbit(activeOrbit8);
                gpu.setLayer(layerLevels[activeLayerIndex]);
                gpu.setAudio(frequencyData.low, frequencyData.mid, frequencyData.high);
                gpu.setFrameColorMode(activeFrameColor, currentPhase === PHASES.READY);

                if (focusedNodeId && nodeById[focusedNodeId]) {
                    const focusNode = nodeById[focusedNodeId];
                    const focusIdx = nodeIndexById[focusNode.id];
                    const focusState = (focusIdx !== undefined) ? nodeStates[focusIdx] : null;
                    const focusX = currentPhase === PHASES.READY || !focusState ? focusNode.x : focusState.currentX;
                    const focusY = currentPhase === PHASES.READY || !focusState ? focusNode.y : focusState.currentY;
                    gpu.setFocus(focusX, focusY, 1.0);
                } else {
                    gpu.clearFocus();
                }

                gpu.step(time);

                if (backendModeEl) backendModeEl.textContent = backendState.mode;
                if (backendParticlesEl) {
                    backendParticlesEl.textContent = (gpu.activeCount || 0).toLocaleString() + ' gpu particles';
                }

                requestAnimationFrame(render);
                return;
            }

            // Clear
            ctx.fillStyle = COLORS.void;
            ctx.fillRect(0, 0, width, height);

            // Apply camera transform for all subsequent drawing
            applyCameraTransform(ctx);

            // ============================================================
            // GORGEOUS MESH RENDERING - Like the Paris cityscapes
            // ============================================================
            if (delaunayEdges.length > 0) {
                const frameColor = getFrameColor();
                const layeredHeight = Math.min(
                    PERF.meshGradientHeightCap,
                    Math.max(30, Math.floor(maxHeight * layerMultiplier))
                );
                const layeredWireCount = Math.min(
                    PERF.meshLayerCap,
                    Math.max(4, Math.floor(wireCount * layerMultiplier))
                );

                // Layer 1: Dense gradient base (the "city" silhouette)
                ctx.save();
                for (let i = 0; i < layeredHeight; i++) {
                    ctx.translate(0, 0.5);  // Slightly larger steps for depth
                    // Exponential falloff for more realistic depth
                    const alpha = Math.pow(1 - i / layeredHeight, 1.5) * 0.04;
                    // Edge threshold grows slower at bottom (denser base)
                    const threshold = Math.pow(i / layeredHeight, 0.7) * layeredHeight * 0.8 * barradeauThreshold;
                    renderDelaunayEdges(threshold, frameColor, alpha, currentPhase !== PHASES.READY);
                }
                ctx.restore();

                // Layer 2: Mid-tone wireframe layers
                for (let i = 0; i < layeredWireCount; i++) {
                    const t = i / layeredWireCount;
                    ctx.save();
                    ctx.translate(0, layeredHeight * (1 - t) * 0.3);
                    ctx.globalAlpha = 0.03 + 0.1 * t;
                    ctx.strokeStyle = frameColor;
                    ctx.lineWidth = 0.5;
                    renderDelaunayEdges((15 + i * 15) * barradeauThreshold, frameColor, 0.03 + 0.1 * t, currentPhase !== PHASES.READY);
                    ctx.restore();
                }

                // Layer 3: Color gradient overlay (screen blend)
                ctx.save();
                ctx.globalCompositeOperation = 'screen';
                const gradient = ctx.createLinearGradient(0, height, 0, 0);
                if (currentPhase === PHASES.READY) {
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
                ctx.strokeStyle = currentPhase === PHASES.READY ? '#fff' : COLORS.teal;
                ctx.lineWidth = 0.8;
                ctx.globalAlpha = 0.12;
                renderDelaunayEdges(40 * barradeauThreshold, ctx.strokeStyle, 0.12, currentPhase !== PHASES.READY);

                // Layer 5: Soft glow blur
                ctx.filter = 'blur(3px)';
                ctx.globalAlpha = 0.15;
                ctx.strokeStyle = frameColor;
                ctx.lineWidth = 1.5;
                renderDelaunayEdges(60 * barradeauThreshold, ctx.strokeStyle, 0.15, currentPhase !== PHASES.READY);
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

                // Size based on locked footprint formula + centrality boost.
                const baseRadius = getNodeVisualRadius(node);

                // After emergence: subtle energy field displacement (NOT breathing)
                let x, y;
                if (currentPhase === PHASES.READY) {
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
                if (nodeType === 'entry' && currentPhase === PHASES.READY && alpha > 0.8) {
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

                // Connection-path selection ring
                if (selectedConnectionKey && highlightedNodeIds.has(node.id)) {
                    ctx.save();
                    ctx.globalAlpha = 0.55;
                    ctx.strokeStyle = '#F4C430';
                    ctx.lineWidth = 1.1;
                    ctx.beginPath();
                    ctx.arc(x, y, baseRadius + 4, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.restore();
                }

                // focus8 selection ring
                if (focusedNodeId === node.id) {
                    ctx.save();
                    ctx.globalAlpha = 0.9;
                    ctx.strokeStyle = COLORS.gold;
                    ctx.lineWidth = 1.2;
                    ctx.beginPath();
                    ctx.arc(x, y, baseRadius + 6, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.restore();
                }
            }

            // Update and draw particles
            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].update(time);
                particles[i].draw(ctx);
                if (particles[i].isDead()) {
                    // Decrement per-node counter for error particles
                    if (particles[i].type === 'error' && particles[i].nodeId) {
                        decrementNodeParticles(particles[i].nodeId);
                    }
                    particles.splice(i, 1);
                }
            }

            // Spawn error particles (only after emerged)
            if (currentPhase === PHASES.READY) {
                for (const node of nodes) {
                    const isBrokenOrCombat = node.status === 'broken' || node.status === 'combat';
                    if (isBrokenOrCombat && Math.random() < 0.025 * particleDensityMultiplier * Math.max(0.2, 1 - particlePressure * 0.6)) {
                        spawnErrorParticles(node);
                    }
                }
            }

            // Restore camera transform after all drawing is complete
            restoreCameraTransform(ctx);

            if (backendModeEl) backendModeEl.textContent = backendState.mode;
            if (backendParticlesEl) {
                backendParticlesEl.textContent = particles.length.toLocaleString() + ' cpu particles';
            }

            requestAnimationFrame(render);
        }

        // ================================================================
        // INTERACTION
        // ================================================================
        function findNodeAt(screenX, screenY) {
            // Transform screen coordinates to world coordinates
            const worldX = (screenX - cameraPanX) / cameraZoom;
            const worldY = (screenY - cameraPanY) / cameraZoom;

            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const state = nodeStates[i];
                const nx = currentPhase === PHASES.READY ? node.x : state.currentX;
                const ny = currentPhase === PHASES.READY ? node.y : state.currentY;
                const dist = Math.sqrt(Math.pow(nx - worldX, 2) + Math.pow(ny - worldY, 2));
                const radius = getNodeVisualRadius(node);
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
            const edge = node ? null : findEdgeAt(x, y);

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

                // Health errors section
                let healthErrorsHtml = '';
                if (node.healthErrors && node.healthErrors.length > 0) {
                    const displayErrors = node.healthErrors.slice(0, 5);
                    let healthHtml = '<div class="health-errors">';
                    displayErrors.forEach(e => {
                        healthHtml += '<div class="health-error-item">';
                        healthHtml += '<span class="health-error-loc">' + (e.file || node.path) + ':' + (e.line || 0) + '</span> ';
                        healthHtml += (e.message || 'Unknown error');
                        healthHtml += '</div>';
                    });
                    if (node.healthErrors.length > 5) {
                        healthHtml += '<div class="health-error-item" style="color:#666">... and ' + (node.healthErrors.length - 5) + ' more</div>';
                    }
                    healthHtml += '</div>';
                    healthErrorsHtml = healthHtml;
                }

                const cameraModeIndicator = cameraMode !== 'overview'
                    ? `<div style="margin-top:4px; color:#D4AF37; font-size: 10px;">CAMERA: ${cameraMode} | zoom ${cameraZoom.toFixed(2)}x | ESC to return</div>`
                    : '';

                tooltip.innerHTML = `
                    <div class="path">${node.path}</div>
                    <div class="meta">
                        <span class="status ${node.status}">${node.status}</span>
                        <span style="color: ${typeColor}; font-size: 10px; text-transform: uppercase;">${nodeType}</span>
                        <span class="loc">${node.loc} lines</span>
                        <span class="loc">${node.exportCount || 0} exports</span>
                        <span class="loc">h ${((node.buildingHeight || 3)).toFixed(1)}</span>
                    </div>
                    ${cameraModeIndicator}
                    ${connectionInfo}
                    ${centralityInfo}
                    ${cycleWarning}
                    ${errorsHtml}
                    ${healthErrorsHtml}
                `;

                let tx = e.clientX + 15;
                let ty = e.clientY + 15;
                if (tx + 320 > window.innerWidth) tx = e.clientX - 325;
                if (ty + 200 > window.innerHeight) ty = e.clientY - 100;

                tooltip.style.left = tx + 'px';
                tooltip.style.top = ty + 'px';
                tooltip.classList.add('visible');
                canvas.style.cursor = 'pointer';
            } else if (edge) {
                const resolved = edge.resolved ? 'resolved' : 'unresolved';
                const line = edge.lineNumber || 0;
                tooltip.innerHTML = `
                    <div class="path">${edge.source}</div>
                    <div style="color:#888; margin: 2px 0;">→ ${edge.target}</div>
                    <div class="meta">
                        <span class="status ${edge.resolved ? 'working' : 'broken'}">${resolved}</span>
                        <span class="loc">line ${line}</span>
                    </div>
                    <div style="margin-top:6px; color:#666;">Click to highlight full signal path.</div>
                `;
                let tx = e.clientX + 15;
                let ty = e.clientY + 15;
                if (tx + 320 > window.innerWidth) tx = e.clientX - 325;
                if (ty + 140 > window.innerHeight) ty = e.clientY - 120;
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
                clearSelectedConnection();
                focusedNodeId = node.id;

                // Warp dive to broken nodes
                if (node.status === 'broken' && currentPhase === PHASES.READY) {
                    warpDiveTo(node);
                }

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
                        outgoingCount: node.outgoingCount,
                        exportCount: node.exportCount,
                        buildingHeight: node.buildingHeight,
                        footprint: node.footprint
                    }
                }, '*');
                console.log('Node clicked:', node.path, node.nodeType);
                return;
            }

            const edge = findEdgeAt(x, y);
            if (edge) {
                setSelectedConnection(edge);
                phaseEl.textContent = 'path ' + edge.source.split('/').pop() + ' -> ' + edge.target.split('/').pop();
                return;
            }

            clearSelectedConnection();
        });

        canvas.addEventListener('mouseleave', () => {
            tooltip.classList.remove('visible');
        });

        window.addEventListener('message', (event) => {
            if (!event.data || event.data.type !== 'WOVEN_MAPS_CONNECTION_RESULT') return;
            const payload = event.data.payload || null;
            if (!payload) return;

            lastConnectionActionResult = payload;
            connectionActionHistory = [payload, ...connectionActionHistory].slice(0, 40);
            if (selectedConnection) {
                updateConnectionPanel();
            }

            phaseEl.textContent = payload.ok
                ? 'patchbay action complete'
                : 'patchbay action blocked';
        });

        window.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                // Return from camera dive if available, otherwise clear selection
                if (cameraReturnStack.length > 0) {
                    returnFromDive();
                } else {
                    clearSelectedConnection();
                }
            }
        });

        // ================================================================
        // START
        // ================================================================
        updateWave();
        updateDensit8();
        updateConnectionPanel();
        initParticleBackend();
        requestAnimationFrame(render);
        console.log('Woven Maps Enhanced initialized:', nodes.length, 'nodes');
    </script>

    <!-- Three.js for 3D Code City -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <!-- Three.js addons for 3D Code City -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>

    <!-- Barradeau 3D Code City Renderer (embedded inline) -->
    <script>__WOVEN_MAPS_3D_JS__</script>
</body>
</html>"""


# =============================================================================
# MARIMO INTEGRATION
# =============================================================================


def create_code_city(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
    health_results: Optional[Dict[str, Any]] = None,
) -> Any:
    """Create a Woven Maps Code City visualization for Marimo.

    Args:
        root: Project root directory path.
        width: Visualization width in pixels.
        height: Visualization height in pixels.
        max_height: Maximum building height.
        wire_count: Number of Delaunay wires.
        health_results: Optional dict mapping file/fiefdom paths to
            HealthCheckResult objects. When provided, node statuses are
            merged using the canonical combat > broken > working policy.
    """
    try:
        import marimo as mo
    except ImportError:
        raise ImportError("marimo is required. Install with: pip install marimo")

    if not root or not os.path.isdir(root):
        return mo.md(
            f"**Set a valid project root to visualize the codebase.**\n\nCurrent: `{root or 'None'}`"
        )

    # Prefer ConnectionVerifier graph path so import edges are present for
    # connection panel + full signal-path highlighting. Fall back to baseline
    # scan-only graph if dependency analysis fails.
    try:
        graph_data = build_from_connection_graph(
            root,
            width=width,
            height=height,
            max_height=max_height,
            wire_count=wire_count,
        )
    except Exception:
        graph_data = build_graph_data(root, width, height, max_height, wire_count)

    if not graph_data.nodes:
        return mo.md(f"**No code files found in project.**\n\nScanned: `{root}`")

    # Merge health check results into node statuses (combat > broken > working)
    if health_results:
        graph_data.nodes = build_from_health_results(graph_data.nodes, health_results)

    stream_bps_raw = os.getenv("ORCHESTR8_CODE_CITY_STREAM_BPS", "5000000").strip()
    try:
        stream_bps = max(100_000, int(stream_bps_raw))
    except ValueError:
        stream_bps = 5_000_000

    inline_building_data = os.getenv(
        "ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA", ""
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    # Keep payload lean by default: let the browser generate 3D meshes from
    # graph nodes and stream them into the scene at a controlled rate.
    if inline_building_data:
        building_data = create_3d_code_city(graph_data, layout_scale=10.0)
        building_data_json = json.dumps(building_data)
    else:
        building_data_json = "null"

    # Get default camera state and inject into template
    from IP.contracts.camera_state import get_default_camera_state

    camera_state = get_default_camera_state()
    camera_state_json = json.dumps(
        {
            "mode": camera_state.mode,
            "position": camera_state.position,
            "target": camera_state.target,
            "zoom": camera_state.zoom,
            "return_stack": camera_state.return_stack,
            "transition_ms": camera_state.transition_ms,
            "easing": camera_state.easing,
        }
    )
    patchbay_apply_enabled = os.getenv(
        "ORCHESTR8_PATCHBAY_APPLY", ""
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    js_3d_path = Path(__file__).parent / "static" / "woven_maps_3d.js"
    js_3d_content = (
        js_3d_path.read_text(encoding="utf-8") if js_3d_path.exists() else ""
    )

    iframe_html = (
        WOVEN_MAPS_TEMPLATE.replace("__GRAPH_DATA__", graph_data.to_json())
        .replace("__BUILDING_DATA__", building_data_json)
        .replace("__BUILDING_STREAM_BPS__", str(stream_bps))
        .replace("__CAMERA_STATE__", camera_state_json)
        .replace(
            "__PATCHBAY_APPLY_ENABLED__", "true" if patchbay_apply_enabled else "false"
        )
        .replace("__WOVEN_MAPS_3D_JS__", js_3d_content)
    )
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

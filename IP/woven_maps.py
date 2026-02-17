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
import fnmatch
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from IP.contracts.status_merge_policy import merge_status
from IP.features.code_city.assets import (
    load_woven_maps_template,
    read_text_if_exists,
    script_tag,
)

# Audio configuration - single source of truth for audio-reactive settings
from IP.audio.config import (
    DEFAULT_FFT_SIZE,
    DEFAULT_SMOOTHING,
    get_all_bands,
)

# Try importing TownSquareClassification (may not exist in all installations)
try:
    from IP.contracts.town_square_classification import TownSquareClassification

    TOWN_SQUARE_AVAILABLE = True
except ImportError:
    TOWN_SQUARE_AVAILABLE = False
    TownSquareClassification = None

# =============================================================================
# COLOR CONSTANTS - EXACT, NO EXCEPTIONS
# =============================================================================

COLORS = {
    "gold_metallic": "#D4AF37",  # Working code
    "blue_dominant": "#1fbdea",  # Broken code / Teal during scan
    "purple_combat": "#9D4EDD",  # Combat (LLM active)
    "bg_primary": "#050505",  # The Void - obsidian
    "bg_elevated": "#121214",  # Elevated surfaces
    "gold_dark": "#B8860B",  # Secondary gold
    "gold_saffron": "#F4C430",  # Bright highlights
}

JS_COLORS = {
    "void": "#050505",
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
    is_locked: bool = False  # Louis lock status - file is read-only
    display_zone: str = "city"  # city | town_square | hidden | minimap_only

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
            "isLocked": self.is_locked,
            "displayZone": self.display_zone,
        }


@dataclass
class EdgeData:
    """Represents an import relationship between files."""

    source: str  # Source file path (importer)
    target: str  # Target file path (imported)
    resolved: bool = True  # Whether the import resolves
    bidirectional: bool = False  # Mutual imports
    line_number: int = 0  # Source line of import
    # Fiefdom boundary crossing metadata
    from_fiefdom: str = ""  # Fiefdom of source file
    to_fiefdom: str = ""  # Fiefdom of target file
    is_boundary: bool = False  # True if edge crosses fiefdom boundary
    # Boundary contract metadata
    allowed_types: List[str] = field(default_factory=list)  # e.g., ["imports", "calls"]
    forbidden_crossings: List[str] = field(
        default_factory=list
    )  # e.g., ["cyclic_imports"]
    contract_status: str = ""  # "defined" | "draft" | "missing"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "resolved": self.resolved,
            "bidirectional": self.bidirectional,
            "lineNumber": self.line_number,
            "fromFiefdom": self.from_fiefdom,
            "toFiefdom": self.to_fiefdom,
            "isBoundary": self.is_boundary,
            "allowedTypes": self.allowed_types,
            "forbiddenCrossings": self.forbidden_crossings,
            "contractStatus": self.contract_status,
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
    audio_fft_size: int = DEFAULT_FFT_SIZE
    audio_smoothing: float = DEFAULT_SMOOTHING
    colors: ColorScheme = field(default_factory=ColorScheme)

    def __post_init__(self):
        """Validate audio configuration after initialization."""
        # Validate FFT size is power of 2
        if self.audio_fft_size < 64 or self.audio_fft_size > 4096:
            raise ValueError(
                f"audio_fft_size must be between 64 and 4096, got {self.audio_fft_size}"
            )
        if self.audio_fft_size & (self.audio_fft_size - 1) != 0:
            raise ValueError(
                f"audio_fft_size must be a power of 2, got {self.audio_fft_size}"
            )
        # Validate smoothing
        if not 0.0 <= self.audio_smoothing <= 1.0:
            raise ValueError(
                f"audio_smoothing must be between 0.0 and 1.0, got {self.audio_smoothing}"
            )

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
                "audioFrequencyBands": [
                    {"name": band.name, "lowHz": band.low_hz, "highHz": band.high_hz}
                    for band in get_all_bands()
                ],
            },
            "colors": self.colors.to_dict(),
        }


@dataclass
class Neighborhood:
    """Represents a neighborhood/fiefdom boundary region."""

    name: str  # Directory path as neighborhood name
    nodes: List[str] = field(default_factory=list)  # File paths in this neighborhood
    center_x: float = 0.0
    center_y: float = 0.0
    # Boundary polygon points (2D canvas coordinates)
    boundary_points: List[Dict[str, float]] = field(default_factory=list)
    # Integration crossing count - edges to other neighborhoods
    integration_count: int = 0
    # List of neighbor neighborhoods for badge display
    neighbors: List[Dict[str, Any]] = field(default_factory=list)
    # Status: working | broken | mixed
    status: str = "working"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "nodes": self.nodes,
            "centerX": self.center_x,
            "centerY": self.center_y,
            "boundaryPoints": self.boundary_points,
            "integrationCount": self.integration_count,
            "neighbors": self.neighbors,
            "status": self.status,
        }


@dataclass
class GraphData:
    """Complete data structure for visualization."""

    nodes: List[CodeNode] = field(default_factory=list)
    edges: List[EdgeData] = field(default_factory=list)
    config: GraphConfig = field(default_factory=GraphConfig)
    neighborhoods: List[Neighborhood] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "config": self.config.to_dict(),
            "neighborhoods": [n.to_dict() for n in self.neighborhoods],
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


# =============================================================================
# TOWN SQUARE CLASSIFICATION - Infrastructure File Detection
# =============================================================================

# Common infrastructure file patterns mapping to (classification, display_zone)
# These files are routed to the "town square" zone instead of main city
INFRA_PATTERNS: Dict[str, tuple[str, str]] = {
    # Build configuration files
    "pyproject.toml": ("config", "town_square"),
    "setup.py": ("config", "town_square"),
    "setup.cfg": ("config", "town_square"),
    "requirements*.txt": ("config", "town_square"),
    "Pipfile": ("config", "town_square"),
    "poetry.lock": ("config", "town_square"),
    "package.json": ("config", "town_square"),
    "package-lock.json": ("config", "town_square"),
    "yarn.lock": ("config", "town_square"),
    "pnpm-lock.yaml": ("config", "town_square"),
    "bun.lockb": ("config", "town_square"),
    # Version control & IDE
    ".gitignore": ("config", "town_square"),
    ".gitattributes": ("config", "town_square"),
    ".editorconfig": ("config", "town_square"),
    ".prettierrc*": ("config", "town_square"),
    ".eslintrc*": ("config", "town_square"),
    ".eslintignore": ("config", "town_square"),
    ".prettierignore": ("config", "town_square"),
    "tsconfig*.json": ("config", "town_square"),
    "jsconfig.json": ("config", "town_square"),
    ".vscode/**": ("config", "town_square"),
    ".idea/**": ("config", "town_square"),
    # Build scripts & tools
    "Makefile": ("infrastructure", "town_square"),
    "makefile": ("infrastructure", "town_square"),
    "CMakeLists.txt": ("infrastructure", "town_square"),
    "Dockerfile*": ("infrastructure", "town_square"),
    "docker-compose*.yml": ("infrastructure", "town_square"),
    "docker-compose*.yaml": ("infrastructure", "town_square"),
    ".dockerignore": ("config", "town_square"),
    # Generic config files in root
    "*.yaml": ("config", "town_square"),
    "*.yml": ("config", "town_square"),
    "*.json": ("config", "town_square"),
    "package.json": ("config", "town_square"),  # Explicitly include (not hidden)
    # CI/CD
    ".github/**": ("config", "town_square"),
    ".gitlab-ci.yml": ("config", "town_square"),
    "azure-pipelines.yml": ("config", "town_square"),
    "Jenkinsfile": ("config", "town_square"),
    # Environment & secrets
    ".env*": ("config", "hidden"),  # Secrets - hidden by default
    ".env": ("config", "hidden"),
    ".env.local": ("config", "hidden"),
    ".env.*.local": ("config", "hidden"),
    # Documentation (can be toggled)
    "README*": ("docs", "town_square"),
    "CHANGELOG*": ("docs", "town_square"),
    "LICENSE*": ("docs", "town_square"),
    "CONTRIBUTING*": ("docs", "town_square"),
    "*.md": ("docs", "minimap_only"),  # MD files in minimap only
    # Test configuration (infrastructure, not test code)
    "pytest.ini": ("config", "town_square"),
    "setup.cfg": ("config", "town_square"),
    "tox.ini": ("config", "town_square"),
    ".coveragerc": ("config", "town_square"),
    "conftest.py": ("config", "town_square"),  # pytest shared fixtures
    # Type stubs & type config
    "*.d.ts": ("asset", "minimap_only"),
    "types/**": ("asset", "minimap_only"),
    # Assets
    "*.ico": ("asset", "hidden"),
    "*.svg": ("asset", "minimap_only"),
    "*.png": ("asset", "hidden"),
    "*.jpg": ("asset", "hidden"),
    "*.jpeg": ("asset", "hidden"),
    "*.gif": ("asset", "hidden"),
    "*.webp": ("asset", "hidden"),
    "*.woff": ("asset", "hidden"),
    "*.woff2": ("asset", "hidden"),
    "*.ttf": ("asset", "hidden"),
    "*.eot": ("asset", "hidden"),
    "fonts/**": ("asset", "hidden"),
    "static/**": ("asset", "minimap_only"),
    "public/**": ("asset", "minimap_only"),
    "assets/**": ("asset", "minimap_only"),
    # Compiled/output (hidden)
    "*.pyc": ("build", "hidden"),
    "__pycache__/**": ("build", "hidden"),
    "node_modules/**": ("build", "hidden"),
    "dist/**": ("build", "hidden"),
    "build/**": ("build", "hidden"),
    "target/**": ("build", "hidden"),
    "out/**": ("build", "hidden"),
    "*.class": ("build", "hidden"),
    "*.o": ("build", "hidden"),
    "*.so": ("build", "hidden"),
    "*.dll": ("build", "hidden"),
}


def get_display_zone(path: str) -> str:
    """
    Determine the display zone for a file based on its path.

    Args:
        path: Relative path to the file

    Returns:
        Display zone: 'city' (default), 'town_square', 'hidden', or 'minimap_only'
    """
    # Get the basename for pattern matching
    basename = os.path.basename(path)

    # Check exact basename matches first
    if basename in INFRA_PATTERNS:
        return INFRA_PATTERNS[basename][1]

    # Check pattern matches (supports wildcards)
    for pattern, (_, zone) in INFRA_PATTERNS.items():
        if fnmatch.fnmatch(basename, pattern):
            return zone
        # Also check if path matches (for directory patterns like .github/**)
        if fnmatch.fnmatch(path, pattern):
            return zone

    # Default to main city
    return "city"


def classify_infrastructure(path: str) -> tuple[str, str]:
    """
    Classify an infrastructure file.

    Args:
        path: Relative path to the file

    Returns:
        Tuple of (classification, display_zone)
    """
    basename = os.path.basename(path)

    # Check exact basename matches first
    if basename in INFRA_PATTERNS:
        return INFRA_PATTERNS[basename]

    # Check pattern matches
    for pattern, (classification, zone) in INFRA_PATTERNS.items():
        if fnmatch.fnmatch(basename, pattern):
            return classification, zone
        if fnmatch.fnmatch(path, pattern):
            return classification, zone

    # Not an infrastructure file
    return ("", "city")


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

    # Detect display zone for Town Square classification
    display_zone = get_display_zone(relpath)

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
        display_zone=display_zone,
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


def compute_neighborhoods(
    nodes: List[CodeNode],
    edges: List[EdgeData],
    width: int,
    height: int,
    padding: int = 40,
) -> List[Neighborhood]:
    """Compatibility wrapper for feature-sliced neighborhood computation."""
    from IP.features.code_city.graph_builder import (
        compute_neighborhoods as _compute_neighborhoods,
    )

    return _compute_neighborhoods(nodes, edges, width, height, padding)


def build_graph_data(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
) -> GraphData:
    """Compatibility wrapper for feature-sliced graph builder."""
    from IP.features.code_city.graph_builder import (
        build_graph_data as _build_graph_data,
    )

    return _build_graph_data(
        root=root,
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )


def build_from_connection_graph(
    project_root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 250,
    wire_count: int = 15,
) -> GraphData:
    """Compatibility wrapper for feature-sliced connection graph builder."""
    from IP.features.code_city.graph_builder import (
        build_from_connection_graph as _build_from_connection_graph,
    )

    return _build_from_connection_graph(
        project_root=project_root,
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
    )


def build_from_health_results(
    nodes: List[CodeNode], health_results: Dict[str, Any]
) -> List[CodeNode]:
    """Compatibility wrapper for feature-sliced health merge logic."""
    from IP.features.code_city.graph_builder import (
        build_from_health_results as _build_from_health_results,
    )

    return _build_from_health_results(nodes, health_results)


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
            is_locked=getattr(node, "is_locked", False),
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

# Canonical template source moved to static asset for maintainability.
# Keep constant name stable for downstream compatibility.
WOVEN_MAPS_TEMPLATE = load_woven_maps_template()


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
    """Compatibility wrapper for feature-sliced Code City rendering."""
    from IP.features.code_city.render import create_code_city as _create_code_city

    return _create_code_city(
        root=root,
        width=width,
        height=height,
        max_height=max_height,
        wire_count=wire_count,
        health_results=health_results,
    )


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

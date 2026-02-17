"""
Barradeau Building Generator for Code City

Extracts patterns from Barradeau particle technique for 3D building visualization.
Buildings EMERGE from the Void - no breathing/pulsing animations.

Reference: Barradeau/void-phase0-buildings.html
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional
import math
import random


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG - All scaling constants (LOCKED per CONTEXT.md)
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG = {
    # Scaling factors
    "BASE_FOOTPRINT": 2,  # Minimum building size
    "FOOTPRINT_SCALE": 0.008,  # Lines → footprint multiplier
    "MIN_HEIGHT": 3,  # Minimum building height
    "HEIGHT_PER_EXPORT": 0.8,  # Each export adds this much height
    # Particle density
    "PARTICLES_PER_UNIT": 1.2,  # Higher = more particles
    # Visual
    "LAYER_COUNT": 15,  # Vertical layers in extrusion
    "TAPER": 0.015,  # How much building narrows at top
    # Colors - CANONICAL per VISUAL_TOKEN_LOCK
    "COLOR_WORKING": 0xD4AF37,  # Gold-metallic (#D4AF37)
    "COLOR_BROKEN": 0x1FBDEA,  # Teal/Blue (#1fbdea)
    "COLOR_COMBAT": 0x9D4EDD,  # Purple (#9D4EDD)
    "COLOR_VOID": 0x050505,  # The Void - obsidian background (#050505)
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class Point2D:
    """2D point for footprint triangulation."""

    x: float
    y: float

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10

    def __hash__(self):
        return hash((round(self.x, 10), round(self.y, 10)))


@dataclass
class Point3D:
    """3D point for particle placement."""

    x: float
    y: float
    z: float
    opacity: float = 1.0
    size: float = 0.3


@dataclass
class Edge2D:
    """2D edge with length for footprint."""

    a: Point2D
    b: Point2D
    length: float


@dataclass
class Edge3D:
    """3D edge for wireframe rendering."""

    a: Dict[str, float]
    b: Dict[str, float]


@dataclass
class Triangle:
    """Triangle for Delaunay triangulation."""

    p1: Point2D
    p2: Point2D
    p3: Point2D


@dataclass
class BuildingData:
    """
    Output dataclass for a generated building.
    Contains particles and edges ready for Three.js rendering.
    """

    path: str  # File path this building represents
    status: str  # "working" | "broken" | "combat"
    position: Dict[str, float]  # {x, z} position in scene
    footprint_radius: float  # Calculated footprint
    height: float  # Calculated height
    particles: List[Dict[str, float]]  # All particles with x, y, z, opacity, size
    edges: List[Dict[str, Any]]  # All edges with a, b points
    line_count: int  # Source file lines
    export_count: int  # Source file exports
    is_locked: bool = False  # Louis lock status

    def to_json(self) -> Dict[str, Any]:
        """Serialize for JavaScript consumption."""
        return {
            "path": self.path,
            "status": self.status,
            "isLocked": self.is_locked,
            "position": self.position,
            "footprintRadius": self.footprint_radius,
            "height": self.height,
            "particles": self.particles,
            "edges": self.edges,
            "lineCount": self.line_count,
            "exportCount": self.export_count,
            "particleCount": len(self.particles),
            "edgeCount": len(self.edges),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# DELAUNAY TRIANGULATION
# ═══════════════════════════════════════════════════════════════════════════════


class Delaunay:
    """
    Delaunay triangulation using Bowyer-Watson algorithm.

    Ported from Barradeau/void-phase0-buildings.html lines 727-803
    """

    @staticmethod
    def triangulate(points: List[Point2D]) -> List[Triangle]:
        """
        Generate Delaunay triangulation from a set of 2D points.

        Args:
            points: List of Point2D objects

        Returns:
            List of Triangle objects
        """
        if len(points) < 3:
            return []

        # Find bounding box
        min_x = min(p.x for p in points)
        min_y = min(p.y for p in points)
        max_x = max(p.x for p in points)
        max_y = max(p.y for p in points)

        dx = max_x - min_x
        dy = max_y - min_y
        delta_max = max(dx, dy) * 2

        # Create super-triangle that contains all points
        p1 = Point2D(min_x - delta_max, min_y - delta_max)
        p2 = Point2D(min_x + delta_max * 2, min_y - delta_max)
        p3 = Point2D(min_x + dx / 2, max_y + delta_max)

        triangles = [Triangle(p1, p2, p3)]

        # Add each point
        for point in points:
            bad_triangles = []

            # Find triangles whose circumcircle contains this point
            for tri in triangles:
                if Delaunay._in_circumcircle(point, tri):
                    bad_triangles.append(tri)

            # Find polygon hole
            polygon = []
            for tri in bad_triangles:
                edges = [(tri.p1, tri.p2), (tri.p2, tri.p3), (tri.p3, tri.p1)]

                for edge in edges:
                    shared = False
                    for other in bad_triangles:
                        if other is tri:
                            continue
                        if Delaunay._has_edge(edge, other):
                            shared = True
                            break
                    if not shared:
                        polygon.append(edge)

            # Remove bad triangles
            triangles = [t for t in triangles if t not in bad_triangles]

            # Create new triangles from polygon edges to the point
            for edge in polygon:
                triangles.append(Triangle(edge[0], edge[1], point))

        # Remove triangles that share vertices with super-triangle
        return [
            tri
            for tri in triangles
            if tri.p1 != p1
            and tri.p1 != p2
            and tri.p1 != p3
            and tri.p2 != p1
            and tri.p2 != p2
            and tri.p2 != p3
            and tri.p3 != p1
            and tri.p3 != p2
            and tri.p3 != p3
        ]

    @staticmethod
    def _in_circumcircle(p: Point2D, tri: Triangle) -> bool:
        """Check if point is inside triangle's circumcircle."""
        ax = tri.p1.x - p.x
        ay = tri.p1.y - p.y
        bx = tri.p2.x - p.x
        by = tri.p2.y - p.y
        cx = tri.p3.x - p.x
        cy = tri.p3.y - p.y

        return (
            (ax * ax + ay * ay) * (bx * cy - cx * by)
            - (bx * bx + by * by) * (ax * cy - cx * ay)
            + (cx * cx + cy * cy) * (ax * by - bx * ay)
        ) > 0

    @staticmethod
    def _has_edge(edge: Tuple[Point2D, Point2D], tri: Triangle) -> bool:
        """Check if triangle has this edge."""
        tri_edges = [(tri.p1, tri.p2), (tri.p2, tri.p3), (tri.p3, tri.p1)]
        for e in tri_edges:
            if (e[0] == edge[0] and e[1] == edge[1]) or (
                e[0] == edge[1] and e[1] == edge[0]
            ):
                return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# BARRADEAU BUILDING GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════


class BarradeauBuilding:
    """
    Generates a Code City building using Barradeau particle technique.

    Buildings have:
    - Footprint based on line count: 2 + (lines × 0.008)
    - Height based on export count: 3 + (exports × 0.8)
    - 15 layers with taper for ethereal fade effect
    - Particle density inversely proportional to edge length

    NO BREATHING - buildings EMERGE from the Void.
    """

    def __init__(
        self,
        path: str,
        line_count: int,
        export_count: int,
        status: str = "working",
        position: Optional[Dict[str, float]] = None,
        is_locked: bool = False,
    ):
        """
        Initialize building generator.

        Args:
            path: File path this building represents
            line_count: Lines of code in file
            export_count: Number of exports from file
            status: "working" | "broken" | "combat"
            position: {x, z} position in scene (default: origin)
            is_locked: Louis lock status (default: False)
        """
        self.path = path
        self.line_count = line_count
        self.export_count = export_count
        self.status = status
        self.position = position or {"x": 0, "z": 0}
        self.is_locked = is_locked

        self.particles: List[Point3D] = []
        self.edges: List[Edge3D] = []
        self.footprint_radius: float = 0
        self.height: float = 0
        self.footprint_points: List[Point2D] = []

        self._calculate_dimensions()
        self._generate_footprint()
        self._extrude_building()

    def _calculate_dimensions(self) -> None:
        """Calculate building footprint and height from file metrics."""
        # Footprint radius based on file size (LOCKED formula)
        self.footprint_radius = CONFIG["BASE_FOOTPRINT"] + (
            self.line_count * CONFIG["FOOTPRINT_SCALE"]
        )

        # Height based on exports (LOCKED formula)
        self.height = CONFIG["MIN_HEIGHT"] + (
            self.export_count * CONFIG["HEIGHT_PER_EXPORT"]
        )

    def _generate_footprint(self) -> None:
        """Generate 2D footprint points for triangulation."""
        # Complexity based on file size (more lines = more detail)
        complexity = min(12, 6 + self.line_count // 100)
        points = []

        # Main perimeter (slightly irregular for organic feel)
        for i in range(complexity):
            angle = (i / complexity) * math.pi * 2
            variance = 0.85 + random.random() * 0.3
            r = self.footprint_radius * variance
            points.append(Point2D(x=math.cos(angle) * r, y=math.sin(angle) * r))

        # Inner structure points (creates more triangulation detail)
        inner_rings = int(self.footprint_radius / 1.5)
        for ring in range(1, inner_rings + 1):
            ring_radius = (ring / (inner_rings + 1)) * self.footprint_radius * 0.8
            ring_points = max(4, complexity - ring * 2)

            for i in range(ring_points):
                angle = (i / ring_points) * math.pi * 2 + (ring * 0.3)
                points.append(
                    Point2D(
                        x=math.cos(angle) * ring_radius + (random.random() - 0.5) * 0.3,
                        y=math.sin(angle) * ring_radius + (random.random() - 0.5) * 0.3,
                    )
                )

        # Center point
        points.append(Point2D(0, 0))

        self.footprint_points = points

    def _extrude_building(self) -> None:
        """
        Extrude footprint into 3D particles using Barradeau technique.

        Key patterns:
        - Delaunay triangulation of footprint
        - Edge length filtering at higher layers (ethereal fade)
        - Particle density inversely proportional to edge length
        - Taper at higher layers
        """
        # Triangulate footprint
        triangles = Delaunay.triangulate(self.footprint_points)

        # Extract unique edges with lengths
        edge_map: Dict[str, Edge2D] = {}
        for tri in triangles:
            tri_edges = [(tri.p1, tri.p2), (tri.p2, tri.p3), (tri.p3, tri.p1)]

            for a, b in tri_edges:
                # Create consistent key for edge
                if a.x < b.x or (a.x == b.x and a.y < b.y):
                    key = f"{a.x:.4f},{a.y:.4f}-{b.x:.4f},{b.y:.4f}"
                else:
                    key = f"{b.x:.4f},{b.y:.4f}-{a.x:.4f},{a.y:.4f}"

                if key not in edge_map:
                    length = math.hypot(b.x - a.x, b.y - a.y)
                    edge_map[key] = Edge2D(a=a, b=b, length=length)

        edges_2d = list(edge_map.values())
        max_edge_length = max(e.length for e in edges_2d) if edges_2d else 1

        self.particles = []
        self.edges = []

        # For each layer, extrude and place particles
        layer_count = CONFIG["LAYER_COUNT"]
        taper = CONFIG["TAPER"]
        particles_per_unit = CONFIG["PARTICLES_PER_UNIT"]

        for layer in range(layer_count):
            t = layer / layer_count
            y = t * self.height
            scale = 1 - (layer * taper)
            layer_opacity = 1 - t * 0.5

            # Barradeau technique: filter edges by length at higher layers
            # Longer edges are filtered out, creating the ethereal fade effect
            length_threshold = max_edge_length * (1 - t * 0.5)

            for edge in edges_2d:
                # Skip longer edges at higher layers
                if edge.length > length_threshold:
                    continue

                # Transform 2D edge to 3D
                a_3d = {
                    "x": edge.a.x * scale + self.position["x"],
                    "y": y,
                    "z": edge.a.y * scale + self.position["z"],
                }
                b_3d = {
                    "x": edge.b.x * scale + self.position["x"],
                    "y": y,
                    "z": edge.b.y * scale + self.position["z"],
                }

                self.edges.append(Edge3D(a=a_3d, b=b_3d))

                # Particle density inversely proportional to edge length
                # Shorter edges get MORE particles (more detail in complex areas)
                density_multiplier = 1 + (1 - edge.length / max_edge_length) * 2
                num_particles = max(
                    2, int(edge.length * particles_per_unit * density_multiplier)
                )

                for i in range(num_particles + 1):
                    pt = i / num_particles
                    self.particles.append(
                        Point3D(
                            x=a_3d["x"]
                            + (b_3d["x"] - a_3d["x"]) * pt
                            + (random.random() - 0.5) * 0.08,
                            y=a_3d["y"] + (random.random() - 0.5) * 0.08,
                            z=a_3d["z"]
                            + (b_3d["z"] - a_3d["z"]) * pt
                            + (random.random() - 0.5) * 0.08,
                            opacity=layer_opacity,
                            size=0.3 + layer_opacity * 0.4,
                        )
                    )

    def get_building_data(self) -> BuildingData:
        """Get BuildingData for JavaScript consumption."""
        return BuildingData(
            path=self.path,
            status=self.status,
            position=self.position,
            footprint_radius=self.footprint_radius,
            height=self.height,
            particles=[
                {"x": p.x, "y": p.y, "z": p.z, "opacity": p.opacity, "size": p.size}
                for p in self.particles
            ],
            edges=[{"a": e.a, "b": e.b} for e in self.edges],
            line_count=self.line_count,
            export_count=self.export_count,
            is_locked=self.is_locked,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def get_status_color_hex(status: str) -> str:
    """
    Get hex color string for status.

    Args:
        status: "working" | "broken" | "combat"

    Returns:
        Hex color string (e.g., "#D4AF37")
    """
    colors = {
        "working": CONFIG["COLOR_WORKING"],
        "broken": CONFIG["COLOR_BROKEN"],
        "combat": CONFIG["COLOR_COMBAT"],
    }
    color_int = colors.get(status, CONFIG["COLOR_WORKING"])
    return f"#{color_int:06X}"


def get_status_color_int(status: str) -> int:
    """
    Get integer color for Three.js.

    Args:
        status: "working" | "broken" | "combat"

    Returns:
        Integer color value (e.g., 0xD4AF37)
    """
    colors = {
        "working": CONFIG["COLOR_WORKING"],
        "broken": CONFIG["COLOR_BROKEN"],
        "combat": CONFIG["COLOR_COMBAT"],
    }
    return colors.get(status, CONFIG["COLOR_WORKING"])


# ═══════════════════════════════════════════════════════════════════════════════
# TEST / DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Create a test building
    building = BarradeauBuilding(
        path="IP/woven_maps.py",
        line_count=2804,
        export_count=12,
        status="working",
        position={"x": 0, "z": 0},
    )

    data = building.get_building_data()
    print(f"Building: {data.path}")
    print(f"  Footprint: {data.footprint_radius:.2f}")
    print(f"  Height: {data.height:.2f}")
    print(f"  Particles: {len(data.particles)}")
    print(f"  Edges: {len(data.edges)}")
    print(f"  Color: {get_status_color_hex(data.status)}")

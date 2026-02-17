"""CameraState schema — Code City camera position and animation state."""

from typing import Literal, Tuple, List, Dict, Any, Optional
from dataclasses import dataclass, field

CameraMode = Literal["overview", "neighborhood", "building", "room", "sitting_room", "focus"]


@dataclass
class CameraState:
    mode: CameraMode
    position: Tuple[float, float, float]
    target: Tuple[float, float, float]
    zoom: float
    return_stack: List[Dict[str, Any]] = field(default_factory=list)
    transition_ms: int = 1000
    easing: str = "easeInOutCubic"
    # Navigation context for round-trip navigation
    navigation_context: Dict[str, Any] = field(default_factory=dict)

    def clamp_zoom(self, min_zoom: float = 0.1, max_zoom: float = 10.0):
        """Clamp zoom to safe range."""
        self.zoom = max(min_zoom, min(max_zoom, self.zoom))

    def normalize_position(self, bounds: Tuple[float, float, float]):
        """Clamp position within scene bounds."""
        x, y, z = self.position
        bx, by, bz = bounds
        self.position = (
            max(-bx, min(bx, x)),
            max(-by, min(by, y)),
            max(-bz, min(bz, z)),
        )

    def push_return_state(self, node_path: Optional[str] = None, 
                          node_status: Optional[str] = None,
                          zoom_level: Optional[float] = None) -> None:
        """Push current state onto return stack for round-trip navigation."""
        state = {
            "mode": self.mode,
            "position": self.position,
            "target": self.target,
            "zoom": zoom_level if zoom_level is not None else self.zoom,
            "node_path": node_path,
            "node_status": node_status,
        }
        self.return_stack.append(state)

    def pop_return_state(self) -> Optional[Dict[str, Any]]:
        """Pop and return previous state from return stack."""
        if self.return_stack:
            return self.return_stack.pop()
        return None

    def clear_return_stack(self) -> None:
        """Clear the return stack."""
        self.return_stack.clear()


def get_default_camera_state() -> CameraState:
    """Return default overview camera perspective for rapid hotspot triage.
    
    Distant overview position allows seeing the entire Code City at once,
    making it easy to spot broken (teal) areas that need attention.
    """
    return CameraState(
        mode="overview",
        position=(0.0, 800.0, 1200.0),  # Distant overview for full city visibility
        target=(0.0, 0.0, 0.0),
        zoom=0.5,  # Zoomed out to see entire city
        return_stack=[],
        transition_ms=1500,
        easing="easeInOutCubic",
        navigation_context={"entry_point": "overview", "hotspot_triage": True},
    )


def get_neighborhood_camera_state(center_x: float, center_y: float, 
                                   radius: float = 200.0) -> CameraState:
    """Return camera state for neighborhood-level view.
    
    Positioned to see a neighborhood cluster with surrounding context.
    """
    return CameraState(
        mode="neighborhood",
        position=(center_x, 400.0, center_y + 600.0),
        target=(center_x, 0.0, center_y),
        zoom=1.2,
        return_stack=[],
        transition_ms=1200,
        easing="easeInOutCubic",
        navigation_context={"level": "neighborhood", "center": (center_x, center_y), "radius": radius},
    )


def get_building_camera_state(building_x: float, building_y: float,
                               building_height: float = 10.0) -> CameraState:
    """Return camera state for building-level view.
    
    Positioned for close inspection of a single building/file.
    """
    return CameraState(
        mode="building",
        position=(building_x, 200.0, building_y + 300.0),
        target=(building_x, building_height / 2, building_y),
        zoom=2.5,
        return_stack=[],
        transition_ms=1000,
        easing="easeInOutCubic",
        navigation_context={"level": "building", "position": (building_x, building_y)},
    )


def get_focus_camera_state(node_x: float, node_y: float,
                            node_path: str = "") -> CameraState:
    """Return camera state for focus8 dive to a specific node.
    
    Quick dive with keyboard shortcut support for rapid navigation.
    """
    return CameraState(
        mode="focus",
        position=(node_x, 150.0, node_y + 250.0),
        target=(node_x, 0.0, node_y),
        zoom=3.0,
        return_stack=[],
        transition_ms=800,
        easing="easeOutQuad",
        navigation_context={"level": "focus", "node_path": node_path, "shortcut_triggered": True},
    )

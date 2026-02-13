"""CameraState schema — Code City camera position and animation state."""

from typing import Literal, Tuple, List, Dict, Any
from dataclasses import dataclass, field

CameraMode = Literal["overview", "dive", "focus", "room", "sitting_room"]


@dataclass
class CameraState:
    mode: CameraMode
    position: Tuple[float, float, float]
    target: Tuple[float, float, float]
    zoom: float
    return_stack: List[Dict[str, Any]] = field(default_factory=list)
    transition_ms: int = 1000
    easing: str = "easeInOutCubic"

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


def get_default_camera_state() -> CameraState:
    """Return default overview camera perspective."""
    return CameraState(
        mode="overview",
        position=(0.0, 500.0, 800.0),
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
        return_stack=[],
        transition_ms=1500,
        easing="easeInOutCubic",
    )

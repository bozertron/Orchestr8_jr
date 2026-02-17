# Task ID: 3

**Title:** Implement CameraState schema

**Status:** done

**Dependencies:** 1 ✓

**Priority:** medium

**Description:** Create schema for Code City camera position and animation state with defaults

**Details:**

Create IP/contracts/camera_state.py with dataclass for camera state management.

Implementation:
```python
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
        """Normalize position within scene bounds."""
        x, y, z = self.position
        bx, by, bz = bounds
        self.position = (
            max(-bx, min(bx, x)),
            max(-by, min(by, y)),
            max(-bz, min(bz, z))
        )

def get_default_camera_state() -> CameraState:
    """Return default overview camera perspective."""
    return CameraState(
        mode="overview",
        position=(0.0, 500.0, 800.0),  # Bird's eye view
        target=(0.0, 0.0, 0.0),         # Looking at origin
        zoom=1.0,
        return_stack=[],
        transition_ms=1500,
        easing="easeInOutCubic"
    )
```

**Test Strategy:**

Test get_default_camera_state() returns valid state. Test clamp_zoom() and normalize_position() edge cases. Verify all camera modes are valid Literal values.

## Subtasks

### 3.1. Create IP/contracts directory and camera_state.py file skeleton

**Status:** pending  
**Dependencies:** None  

Create the contracts directory structure and initialize camera_state.py with imports and type definitions

**Details:**

Create IP/contracts/ directory with __init__.py. Create camera_state.py with imports: typing (Literal, Tuple, List, Dict, Any), dataclasses (dataclass, field). Define CameraMode type alias as Literal["overview", "dive", "focus", "room", "sitting_room"].

### 3.2. Implement CameraState dataclass with core fields

**Status:** pending  
**Dependencies:** 3.1  

Define the CameraState dataclass with all required fields and default values

**Details:**

Create @dataclass CameraState with fields: mode (CameraMode), position (Tuple[float, float, float]), target (Tuple[float, float, float]), zoom (float), return_stack (List[Dict[str, Any]] with field(default_factory=list)), transition_ms (int = 1000), easing (str = "easeInOutCubic").

### 3.3. Implement clamp_zoom utility method

**Status:** pending  
**Dependencies:** 3.2  

Add clamp_zoom method to CameraState for constraining zoom values to safe ranges

**Details:**

Add method clamp_zoom(self, min_zoom: float = 0.1, max_zoom: float = 10.0) that sets self.zoom = max(min_zoom, min(max_zoom, self.zoom)). This ensures zoom stays within valid bounds for rendering.

### 3.4. Implement normalize_position utility method

**Status:** pending  
**Dependencies:** 3.2  

Add normalize_position method to CameraState for constraining camera position within scene bounds

**Details:**

Add method normalize_position(self, bounds: Tuple[float, float, float]) that clamps each position coordinate to [-bound, bound] range. For each axis (x,y,z), apply: max(-bx, min(bx, x)). Updates self.position in place.

### 3.5. Implement get_default_camera_state factory function

**Status:** pending  
**Dependencies:** 3.2  

Create factory function returning default overview camera state for Code City initialization

**Details:**

Implement get_default_camera_state() -> CameraState returning CameraState with: mode="overview", position=(0.0, 500.0, 800.0) for bird's eye view, target=(0.0, 0.0, 0.0) at origin, zoom=1.0, empty return_stack, transition_ms=1500, easing="easeInOutCubic".

from typing import List, Dict, Any, Optional, Protocol, Callable
from dataclasses import dataclass, field
import uuid

@dataclass
class TourStep:
    """
    Represents a single step in a guided city tour.
    Ref: C3-01 MaestroWizard.
    """
    id: str
    title: str
    content: str
    # 3D Coordinates for Camera Flight
    target_camera_pos: Optional[Dict[str, float]] = None 
    # Logic hooks (clean-room decoupled from UI)
    actions: List[str] = field(default_factory=list) 

class TourService:
    """
    State machine for City Onboarding / Guided Tours.
    """
    def __init__(self, temporal_service: Optional[Any] = None):
        self._steps: List[TourStep] = []
        self._current_index: int = -1
        self._active: bool = False
        self._temporal = temporal_service
    
    def load_tour(self, steps: List[TourStep]) -> None:
        self._steps = steps
        self._reset()

    def start_tour(self) -> Optional[TourStep]:
        if not self._steps: return None
        self._active = True
        self._current_index = 0
        step = self._steps[0]
        if self._temporal:
            self._temporal.record_quantum("tour_start", "tour_service", {
                "step_id": step.id,
                "title": step.title
            })
        return step
        
    def next_step(self) -> Optional[TourStep]:
        if not self._active: return None
        
        if self._current_index < len(self._steps) - 1:
            self._current_index += 1
            step = self._steps[self._current_index]
            if self._temporal:
                self._temporal.record_quantum("tour_next", "tour_service", {
                    "step_id": step.id,
                    "title": step.title
                })
            return step
        else:
            self._active = False
            return None

    def previous_step(self) -> Optional[TourStep]:
        if not self._active: return None
        
        if self._current_index > 0:
            self._current_index -= 1
            step = self._steps[self._current_index]
            if self._temporal:
                self._temporal.record_quantum("tour_prev", "tour_service", {
                    "step_id": step.id,
                    "title": step.title
                })
            return step
        return None

    def get_current_step(self) -> Optional[TourStep]:
        if self._active and 0 <= self._current_index < len(self._steps):
            return self._steps[self._current_index]
        return None

    def is_active(self) -> bool:
        return self._active

    def _reset(self):
        self._current_index = -1
        self._active = False

"""LockOverlay schema — visual rules for locked nodes/ports and Louis lock reasons in Code City."""

from typing import Literal
from dataclasses import dataclass, asdict

LockType = Literal["louis", "readonly", "system"]
DisplayZone = Literal["town_square", "hidden", "minimap_only"]


@dataclass
class LockOverlay:
    """Visual rules for locked nodes/ports and Louis lock reasons in Code City.

    Defines how locked files appear in the Code City visualization and what
    interaction constraints apply to them.
    """

    path: str
    lock_type: LockType
    reason: str = ""
    locked_by: str = "unknown"
    locked_at: str = ""
    visual_opacity: float = 0.4
    show_lock_icon: bool = True
    allow_inspection: bool = True

    def validate(self):
        """Validate lock overlay constraints.

        Raises ValueError if validation fails.
        """
        valid_lock_types = ("louis", "readonly", "system")
        if self.lock_type not in valid_lock_types:
            raise ValueError(
                f"Invalid lock_type: {self.lock_type}. Must be one of {valid_lock_types}"
            )

        if not (0.0 <= self.visual_opacity <= 1.0):
            raise ValueError(
                f"Invalid visual_opacity: {self.visual_opacity}. Must be between 0.0 and 1.0"
            )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LockOverlay":
        """Factory method to create LockOverlay from dictionary.

        Validates the created instance before returning.
        """
        lock = cls(
            path=str(data["path"]),
            lock_type=data["lock_type"],
            reason=str(data.get("reason", "")),
            locked_by=str(data.get("locked_by", "unknown")),
            locked_at=str(data.get("locked_at", "")),
            visual_opacity=float(data.get("visual_opacity", 0.4)),
            show_lock_icon=bool(data.get("show_lock_icon", True)),
            allow_inspection=bool(data.get("allow_inspection", True)),
        )
        lock.validate()
        return lock


EXAMPLE_LOCK_OVERLAY = {
    "path": "IP/louis_core.py",
    "lock_type": "louis",
    "reason": "Protected by Louis: Core module",
    "locked_by": "louis_core",
    "locked_at": "2026-02-13T03:00:00Z",
    "visual_opacity": 0.4,
    "show_lock_icon": True,
    "allow_inspection": True,
}

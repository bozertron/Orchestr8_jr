"""
Director models - shared dataclasses to avoid circular imports.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any
import time
import uuid


@dataclass
class Suggestion:
    """
    Represents a contextual suggestion from the AI Director.
    """
    id: str
    type: str  # "workflow", "tool", "productivity", "learning"
    title: str
    description: str
    action_data: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    priority: int  # 1 (low) to 5 (high)
    created_at: int
    expires_at: Optional[int] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = int(time.time() * 1000)

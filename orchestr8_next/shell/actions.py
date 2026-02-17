import uuid
from datetime import datetime, timezone
from typing import Generic, TypeVar, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from orchestr8_next.shell.contracts import ActionType

T = TypeVar('T')

class UIAction(BaseModel, Generic[T]):
    """
    Standard envelope for all UI-driven actions dispatched to the Store.
    Ensures traceability and type safety across the Action Bus.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: ActionType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Optional[T] = None

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

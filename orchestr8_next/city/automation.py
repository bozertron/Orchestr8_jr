from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass
class AutomationTask:
    id: str
    target_id: str
    description: str
    status: str = "pending"
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())

class QueueService:
    """
    Manages batch job execution for City Automation.
    Ref: P07-C2-01 AutoRun.
    """
    def __init__(self):
        self._queue: List[AutomationTask] = []
        self._history: List[AutomationTask] = []

    def enqueue(self, target_id: str, description: str) -> str:
        task_id = str(uuid.uuid4())
        task = AutomationTask(id=task_id, target_id=target_id, description=description)
        self._queue.append(task)
        return task_id

    def next_task(self) -> Optional[AutomationTask]:
        if not self._queue:
            return None
        task = self._queue.pop(0)
        task.status = "processing"
        self._history.append(task)
        return task

    def get_pending_count(self) -> int:
        return len(self._queue)

class UndoRedoService:
    """
    Manages undo/redo snapshots for city state.
    Ref: P07-C2-01 useAutoRunUndo.
    """
    def __init__(self):
        self._snapshots: List[Any] = []
        self._pointer: int = -1

    def capture_snapshot(self, state: Any) -> None:
        # Truncate redo history if we are in the middle
        if self._pointer < len(self._snapshots) - 1:
            self._snapshots = self._snapshots[:self._pointer + 1]
            
        self._snapshots.append(state)
        self._pointer += 1

    def undo(self) -> Optional[Any]:
        if self._pointer > 0:
            self._pointer -= 1
            return self._snapshots[self._pointer]
        return None

    def redo(self) -> Optional[Any]:
        if self._pointer < len(self._snapshots) - 1:
            self._pointer += 1
            return self._snapshots[self._pointer]
        return None
    
    def can_undo(self) -> bool:
        return self._pointer > 0

    def can_redo(self) -> bool:
        return self._pointer < len(self._snapshots) - 1

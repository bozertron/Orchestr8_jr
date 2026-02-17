from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import time
import uuid
import json

@dataclass
class Epoch:
    """
    Represents a major project phase or timeline segment.
    Ref: MSL-MOD-03.
    """
    id: str
    name: str # e.g. "P07"
    start_time: float
    end_time: Optional[float] = None
    status: str = "active" # active, completed, archived
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Quantum:
    """Atomic event in the city timeline."""
    id: str
    timestamp: float
    type: str # e.g. "commit", "obs", "artifact"
    source_id: str # Agent or System ID
    payload: Dict[str, Any] = field(default_factory=dict)
    epoch_id: Optional[str] = None

@dataclass
class Snapshot:
    """
    Immutable state capture at a specific point in time.
    Ref: MSL-MOD-03.
    """
    id: str
    timestamp: float
    epoch_id: str
    artifact_refs: List[str] # List of file paths or hashes
    description: str

class TemporalStateService:
    """
    Core service for managing Code City timeline and history.
    """
    def __init__(self):
        self._epochs: Dict[str, Epoch] = {}
        self._timeline: List[Quantum] = []
        self._snapshots: Dict[str, Snapshot] = {}
        self._active_epoch_id: Optional[str] = None

    def start_epoch(self, name: str, meta: Dict = None) -> str:
        # Close active if any
        if self._active_epoch_id:
            self.end_epoch(self._active_epoch_id)
            
        eid = f"epoch-{uuid.uuid4()}"
        epoch = Epoch(
            id=eid,
            name=name,
            start_time=time.time(),
            metadata=meta or {}
        )
        self._epochs[eid] = epoch
        self._active_epoch_id = eid
        return eid

    def end_epoch(self, epoch_id: str) -> bool:
        if epoch_id in self._epochs:
            self._epochs[epoch_id].end_time = time.time()
            self._epochs[epoch_id].status = "completed"
            if self._active_epoch_id == epoch_id:
                self._active_epoch_id = None
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for persistence."""
        return {
            "epochs": {eid: e.__dict__ for eid, e in self._epochs.items()},
            "timeline": [q.__dict__ for q in self._timeline],
            "snapshots": {sid: s.__dict__ for sid, s in self._snapshots.items()},
            "active_epoch_id": self._active_epoch_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TemporalStateService':
        """Reconstruct service from serialized state."""
        service = cls()
        for eid, edata in data.get("epochs", {}).items():
            service._epochs[eid] = Epoch(**edata)
        for qdata in data.get("timeline", []):
            service._timeline.append(Quantum(**qdata))
        for sid, sdata in data.get("snapshots", {}).items():
            service._snapshots[sid] = Snapshot(**sdata)
        service._active_epoch_id = data.get("active_epoch_id")
        return service

    def record_quantum(self, event_type: str, source_id: str, payload: Dict[str, Any], timestamp: Optional[float] = None) -> str:
        """Record an atomic city event."""
        qid = f"q-{int(time.time() * 1000)}"
        quantum = Quantum(
            id=qid,
            timestamp=timestamp or time.time(),
            type=event_type,
            source_id=source_id,
            payload=payload,
            epoch_id=self._active_epoch_id
        )
        self._timeline.append(quantum)
        return qid

    def advance_quantum(self, trigger_event: str, payload: Dict = None) -> int:
        """
        Advance the atomic timeline progression.
        Ref: MSL-04 3.1.
        """
        qid_num = len(self._timeline) + 1
        qid = f"{qid_num}" # Monotonic increment
        quantum = Quantum(
            id=qid,
            timestamp=time.time(),
            type=trigger_event,
            source_id="system",
            payload=payload or {}
        )
        self._timeline.append(quantum)
        return qid_num

    def get_snapshot_by_quantum(self, quantum_id: int) -> Optional[Snapshot]:
        """
        Retrieve historical snapshot based on quantum ID.
        Ref: MSL-04 3.2.
        """
        # Simplification: find a snapshot roughly at that quantum's timestamp
        # or map snapshots to quantum IDs directly.
        # For MVP, we'll look for a direct match in metadata if available.
        for snap in self._snapshots.values():
            if snap.id == str(quantum_id):
                return snap
        return None

    def get_bucketed_activity(self, start_time: float, end_time: float, bucket_count: int = 24) -> List[Dict[str, Any]]:
        """
        Bucketize activity events over time.
        Ref: P07-C5-01 SessionActivityGraph.
        """
        if end_time <= start_time:
            return []
            
        bucket_size = (end_time - start_time) / bucket_count
        buckets = []
        
        for i in range(bucket_count):
            b_start = start_time + i * bucket_size
            b_end = b_start + bucket_size
            
            # Count events in this bucket
            count = sum(1 for q in self._timeline if b_start <= q.timestamp < b_end)
            
            buckets.append({
                "start": b_start,
                "end": b_end,
                "count": count
            })
            
        return buckets

    def search_history(self, query: Optional[str] = None, type_filter: Optional[str] = None, limit: int = 100) -> List[Quantum]:
        """
        Search and filter historical events.
        Ref: P07-C5-02 HistoryPanel.
        """
        results = self._timeline
        
        if type_filter:
            results = [q for q in results if q.type == type_filter]
            
        if query:
            query = query.lower()
            results = [
                q for q in results 
                if query in q.type.lower() or query in q.source_id.lower() or query in json.dumps(q.payload).lower()
            ]
            
        return results[-limit:]

    def create_snapshot(self, description: str, artifacts: List[str]) -> Optional[str]:
        """Immutable state capture."""
        if not self._active_epoch_id: 
            return None
            
        sid = f"snap-{uuid.uuid4()}"
        snapshot = Snapshot(
            id=sid,
            timestamp=time.time(),
            epoch_id=self._active_epoch_id,
            artifact_refs=artifacts,
            description=description
        )
        self._snapshots[sid] = snapshot
        return sid

    def get_timeline(self, start_ts: float = 0, end_ts: float = float('inf')) -> List[Quantum]:
        return [q for q in self._timeline if start_ts <= q.timestamp <= end_ts]

    def get_active_epoch(self) -> Optional[Epoch]:
        if self._active_epoch_id:
            return self._epochs[self._active_epoch_id]
        return None

    def export_persistence(self, file_path: str):
        """Save state to disk."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def import_persistence(cls, file_path: str) -> 'TemporalStateService':
        """Load state from disk."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

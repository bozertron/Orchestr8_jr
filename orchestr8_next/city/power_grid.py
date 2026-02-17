from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import time

@dataclass
class GridEntity:
    """
    Standardized Process Node for City Power Grid.
    Ref: P07-C2-02 ProcessMonitor.
    """
    id: str
    pid: int
    name: str = "unknown"
    cpu_usage: float = 0.0
    memory_usage: int = 0
    status: str = "active"
    children: List['GridEntity'] = field(default_factory=list)

class ProcessService:
    """
    Manages active system processes for Power Grid visualization.
    """
    def __init__(self):
        self._mock_processes: Dict[int, GridEntity] = {}

    def fetch_active_processes(self) -> List[GridEntity]:
        """
        Polls system or mock data.
        Returns flat list.
        """
        # In real impl, return psutil data
        # For P07 integration, return current known state
        return list(self._mock_processes.values())

    def build_grid_topology(self, processes: List[Dict[str, Any]]) -> List[GridEntity]:
        """
        Constructs hierarchical grid from flat process list.
        Expects keys: pid, ppid, name, cpu.
        """
        # 1. Create Nodes
        entities: Dict[int, GridEntity] = {}
        for p in processes:
            pid = p.get('pid')
            if not pid: continue
            
            entity = GridEntity(
                id=str(pid),
                pid=pid,
                name=p.get('name', f"process-{pid}"),
                cpu_usage=p.get('cpu', 0.0),
                memory_usage=p.get('memory', 0),
                status=p.get('status', 'running')
            )
            entities[pid] = entity

        # 2. Link Parent/Child (Power Lines)
        roots: List[GridEntity] = []
        for p in processes:
            pid = p.get('pid')
            ppid = p.get('ppid')
            
            if not pid or pid not in entities: continue
            
            node = entities[pid]
            
            if ppid and ppid in entities:
                parent = entities[ppid]
                parent.children.append(node)
            else:
                # Top-level (Power Station)
                roots.append(node)
                
        return roots

    def kill_process_entity(self, pid: int) -> bool:
        """
        Emergency Shutoff Logic.
        """
        if pid in self._mock_processes:
            del self._mock_processes[pid]
            return True
        return False

"""BuildingPanel schema — building inspection panel data contract.

Shows when a user clicks a building (file) in Code City.
Displays imports, exports, routines/rooms, connection references, and lock state.
"""

from typing import List, Optional, Literal
from dataclasses import dataclass, field, asdict

BuildingStatus = Literal["working", "broken", "combat"]


@dataclass
class BuildingRoom:
    """A function or class inside a source file (a 'room' in the building)."""

    name: str
    line_start: int
    line_end: int
    room_type: Literal["function", "class", "method"]
    status: BuildingStatus = "working"
    errors: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class BuildingPanel:
    """Data contract for the Code City building inspection panel.

    Shows when a user clicks a building (file) in Code City.
    Displays imports, exports, routines/rooms, connection references, and lock state.
    """

    path: str
    status: BuildingStatus
    loc: int
    export_count: int = 0
    building_height: float = 3.0
    footprint: float = 2.0
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    rooms: List[BuildingRoom] = field(default_factory=list)
    connections_in: List[str] = field(default_factory=list)
    connections_out: List[str] = field(default_factory=list)
    lock_state: Optional[str] = None
    locked: bool = False
    centrality: float = 0.0
    in_cycle: bool = False
    health_errors: List[str] = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        # Convert rooms to dicts
        d["rooms"] = [r.to_dict() if hasattr(r, "to_dict") else r for r in self.rooms]
        return d


def validate_building_panel(payload: dict) -> BuildingPanel:
    """Validate and parse a building panel payload.

    Raises ValueError on malformed payload.
    """
    required = ["path", "status", "loc"]
    for key in required:
        if key not in payload:
            raise ValueError(f"Missing required field: {key}")

    if payload["status"] not in ("working", "broken", "combat"):
        raise ValueError(f"Invalid status: {payload['status']}")

    # Parse rooms
    rooms = []
    for r in payload.get("rooms", []):
        if isinstance(r, dict):
            rooms.append(BuildingRoom(**r))
        else:
            rooms.append(r)

    return BuildingPanel(
        path=str(payload["path"]),
        status=payload["status"],
        loc=int(payload["loc"]),
        export_count=int(payload.get("export_count", 0)),
        building_height=float(payload.get("building_height", 3.0)),
        footprint=float(payload.get("footprint", 2.0)),
        imports=list(payload.get("imports", [])),
        exports=list(payload.get("exports", [])),
        rooms=rooms,
        connections_in=list(payload.get("connections_in", [])),
        connections_out=list(payload.get("connections_out", [])),
        lock_state=payload.get("lock_state"),
        locked=bool(payload.get("locked", False)),
        centrality=float(payload.get("centrality", 0.0)),
        in_cycle=bool(payload.get("in_cycle", False)),
        health_errors=list(payload.get("health_errors", [])),
    )


EXAMPLE_BUILDING_PANEL = {
    "path": "IP/woven_maps.py",
    "status": "working",
    "loc": 2940,
    "export_count": 8,
    "building_height": 9.4,
    "footprint": 25.52,
    "imports": ["IP/contracts/status_merge_policy.py", "IP/connection_verifier.py"],
    "exports": ["create_code_city", "build_graph_data", "CodeNode", "EdgeData"],
    "rooms": [
        {
            "name": "create_code_city",
            "line_start": 2922,
            "line_end": 2940,
            "room_type": "function",
            "status": "working",
            "errors": [],
        },
        {
            "name": "build_graph_data",
            "line_start": 500,
            "line_end": 530,
            "room_type": "function",
            "status": "working",
            "errors": [],
        },
    ],
    "connections_in": ["IP/plugins/06_maestro.py", "orchestr8.py"],
    "connections_out": ["IP/contracts/status_merge_policy.py"],
    "locked": False,
    "centrality": 0.85,
    "in_cycle": False,
    "health_errors": [],
}

"""CodeCityNodeEvent schema — bridge between JS click events and Python handlers."""

from typing import Literal, Optional, List
from dataclasses import dataclass, field, asdict

CodeCityStatus = Literal["working", "broken", "combat"]


@dataclass
class CodeCityNodeEvent:
    path: str
    status: CodeCityStatus
    loc: int
    errors: List[str] = field(default_factory=list)
    nodeType: Optional[str] = None
    centrality: Optional[float] = None
    inCycle: Optional[bool] = None
    incomingCount: Optional[int] = None
    outgoingCount: Optional[int] = None

    def to_dict(self):
        return asdict(self)


def validate_code_city_node_event(payload: dict) -> CodeCityNodeEvent:
    """Validate and parse a node click payload into CodeCityNodeEvent.

    Raises ValueError on malformed payload.
    """
    required = ["path", "status", "loc"]
    for key in required:
        if key not in payload:
            raise ValueError(f"Missing required field: {key}")

    if payload["status"] not in ("working", "broken", "combat"):
        raise ValueError(f"Invalid status: {payload['status']}")

    return CodeCityNodeEvent(
        path=str(payload["path"]),
        status=payload["status"],
        loc=int(payload["loc"]),
        errors=list(payload.get("errors") or []),
        nodeType=payload.get("nodeType"),
        centrality=payload.get("centrality"),
        inCycle=payload.get("inCycle"),
        incomingCount=payload.get("incomingCount"),
        outgoingCount=payload.get("outgoingCount"),
    )


EXAMPLE_NODE_EVENT = {
    "path": "IP/woven_maps.py",
    "status": "broken",
    "loc": 2847,
    "errors": ["TypeError on line 42"],
    "nodeType": "file",
    "centrality": 0.85,
    "inCycle": False,
    "incomingCount": 12,
    "outgoingCount": 8,
}

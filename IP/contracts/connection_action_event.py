"""ConnectionActionEvent schema — bridge for Code City edge panel actions."""

from typing import Any, Dict, List, Optional, Literal
from dataclasses import dataclass, field, asdict

ConnectionAction = Literal["dry_run_rewire", "apply_rewire"]


@dataclass
class ConnectionEdge:
    """Connection edge payload from Woven Maps selection state."""

    source: str
    target: str
    resolved: bool = True
    lineNumber: int = 0
    edgeType: str = "import"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConnectionActionEvent:
    """Action payload emitted from connection panel controls."""

    action: ConnectionAction
    connection: ConnectionEdge
    proposedTarget: Optional[str] = None
    actorRole: Optional[str] = None
    signalNodes: List[str] = field(default_factory=list)
    signalEdges: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["connection"] = self.connection.to_dict()
        return payload


def validate_connection_action_event(payload: Dict[str, Any]) -> ConnectionActionEvent:
    """Validate and parse a connection panel action payload."""
    if not isinstance(payload, dict):
        raise ValueError("Connection action payload must be a dictionary.")

    if "action" not in payload:
        raise ValueError("Missing required field: action")
    if payload["action"] not in ("dry_run_rewire", "apply_rewire"):
        raise ValueError(f"Invalid action: {payload['action']}")

    connection = payload.get("connection")
    if not isinstance(connection, dict):
        raise ValueError("Missing required field: connection")

    source = connection.get("source")
    target = connection.get("target")
    if not source:
        raise ValueError("Missing required field: connection.source")
    if not target:
        raise ValueError("Missing required field: connection.target")

    edge = ConnectionEdge(
        source=str(source),
        target=str(target),
        resolved=bool(connection.get("resolved", True)),
        lineNumber=int(connection.get("lineNumber", 0)),
        edgeType=str(connection.get("edgeType", "import")),
    )

    proposed_target = payload.get("proposedTarget")
    if proposed_target is not None:
        proposed_target = str(proposed_target).strip() or None

    actor_role = payload.get("actorRole")
    if actor_role is not None:
        actor_role = str(actor_role).strip().lower() or None

    signal_nodes = payload.get("signalNodes") or []
    signal_edges = payload.get("signalEdges") or []
    if not isinstance(signal_nodes, list):
        raise ValueError("signalNodes must be a list")
    if not isinstance(signal_edges, list):
        raise ValueError("signalEdges must be a list")

    return ConnectionActionEvent(
        action=payload["action"],
        connection=edge,
        proposedTarget=proposed_target,
        actorRole=actor_role,
        signalNodes=[str(x) for x in signal_nodes],
        signalEdges=[str(x) for x in signal_edges],
    )


EXAMPLE_CONNECTION_ACTION = {
    "action": "dry_run_rewire",
    "connection": {
        "source": "IP/plugins/06_maestro.py",
        "target": "IP/woven_maps.py",
        "resolved": True,
        "lineNumber": 98,
        "edgeType": "import",
    },
    "proposedTarget": "IP/woven_maps_gpu.py",
    "actorRole": "operator",
    "signalNodes": ["IP/plugins/06_maestro.py", "IP/woven_maps.py"],
    "signalEdges": ["IP/plugins/06_maestro.py->IP/woven_maps.py:98"],
}

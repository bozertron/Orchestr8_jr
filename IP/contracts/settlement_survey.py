"""SettlementSurvey schema — typed structures for Settlement System integration."""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum


class WiringStatus(Enum):
    WORKING = "working"
    BROKEN = "broken"
    COMBAT = "combat"


@dataclass
class FiefdomData:
    name: str
    files: List[str]
    entry_points: List[str]
    exports: List[str]
    internal_coupling: float
    external_coupling: float


@dataclass
class BoundaryContract:
    from_fiefdom: str
    to_fiefdom: str
    allowed_types: List[str]
    forbidden_crossings: List[str]
    contract_status: str  # "defined" | "draft" | "missing"


@dataclass
class WiringConnection:
    source: str
    target: str
    status: WiringStatus
    agents_active: bool = False


@dataclass
class SettlementSurvey:
    metadata: Dict[str, Any]
    fiefdoms: Dict[str, FiefdomData]
    boundary_contracts: List[BoundaryContract]
    wiring_state: List[WiringConnection]


def parse_settlement_survey(data: Dict[str, Any]) -> SettlementSurvey:
    """Parse and validate settlement survey JSON.

    Raises ValueError for missing required top-level keys.
    """
    required = ["metadata", "fiefdoms", "boundary_contracts", "wiring_state"]
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required survey field: {key}")

    fiefdoms = {}
    for name, fief_data in data["fiefdoms"].items():
        fiefdoms[name] = FiefdomData(**fief_data)

    contracts = [BoundaryContract(**bc) for bc in data["boundary_contracts"]]

    wiring = []
    for wire in data["wiring_state"]:
        w = dict(wire)
        w["status"] = WiringStatus(w["status"])
        wiring.append(WiringConnection(**w))

    return SettlementSurvey(
        metadata=data["metadata"],
        fiefdoms=fiefdoms,
        boundary_contracts=contracts,
        wiring_state=wiring,
    )


EXAMPLE_SURVEY = {
    "metadata": {"project": "Orchestr8", "timestamp": "2026-02-13"},
    "fiefdoms": {
        "core": {
            "name": "core",
            "files": ["orchestr8.py"],
            "entry_points": ["orchestr8.py"],
            "exports": ["STATE_MANAGERS"],
            "internal_coupling": 0.9,
            "external_coupling": 0.3,
        }
    },
    "boundary_contracts": [],
    "wiring_state": [],
}

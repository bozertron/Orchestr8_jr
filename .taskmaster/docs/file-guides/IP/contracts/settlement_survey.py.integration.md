# contracts/settlement_survey.py Integration Guide

- Source: `IP/contracts/settlement_survey.py`
- Total lines: `93`
- SHA256: `f52283dbe0954bf433ee90b431e4b716295ba5081af95467cd78d0ec31dfe574`
- Role: **Settlement System Survey Schema** — Fiefdom data, boundary contracts, and wiring state

## Why This Is Painful

- Nested dataclasses require careful parsing from JSON/dict
- WiringStatus enum must match status_merge_policy statuses
- Fiefdom coupling values must be 0-1 floats

## Anchor Lines

- `IP/contracts/settlement_survey.py:4` — `class WiringStatus(Enum)` — WORKING/BROKEN/COMBAT enum
- `IP/contracts/settlement_survey.py:9` — `@dataclass class FiefdomData` — Fiefdom metadata
- `IP/contracts/settlement_survey.py:17` — `@dataclass class BoundaryContract` — Inter-fiefdom contract
- `IP/contracts/settlement_survey.py:25` — `@dataclass class WiringConnection` — Import/export wiring
- `IP/contracts/settlement_survey.py:32` — `@dataclass class SettlementSurvey` — Top-level survey
- `IP/contracts/settlement_survey.py:39` — `def parse_settlement_survey(data)` — Parser with validation

## Integration Use

- **Health integration**: Survey data enriches Code City visualization with fiefdom context
- **Boundary enforcement**: BoundaryContract defines allowed/forbidden crossings
- **Wiring visualization**: WiringConnection maps to edge colors in Code City

## Nested Dataclass Structure

```
SettlementSurvey
├── metadata: Dict[str, Any]
├── fiefdoms: Dict[str, FiefdomData]
│   ├── name: str
│   ├── files: List[str]
│   ├── entry_points: List[str]
│   ├── exports: List[str]
│   ├── internal_coupling: float (0-1)
│   └── external_coupling: float (0-1)
├── boundary_contracts: List[BoundaryContract]
│   ├── from_fiefdom: str
│   ├── to_fiefdom: str
│   ├── allowed_types: List[str]
│   ├── forbidden_crossings: List[str]
│   └── contract_status: str ("defined"|"draft"|"missing")
└── wiring_state: List[WiringConnection]
    ├── source: str
    ├── target: str
    ├── status: WiringStatus
    └── agents_active: bool
```

## Resolved Gaps

- [x] All nested dataclasses implemented with correct field types
- [x] WiringStatus enum matches status_merge_policy values
- [x] parse_settlement_survey() validates required top-level keys
- [x] EXAMPLE_SURVEY provides test fixture

# Task ID: 4

**Title:** Implement SettlementSurvey schema

**Status:** done

**Dependencies:** 1 ✓

**Priority:** medium

**Description:** Create schema for Settlement System survey data with typed fiefdom and boundary structures

**Details:**

Create IP/contracts/settlement_survey.py with comprehensive schema for Settlement System integration.

Implementation:
```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class WiringStatus(Enum):
    WORKING = "working"    # Gold - #D4AF37
    BROKEN = "broken"      # Teal - #1fbdea
    COMBAT = "combat"      # Purple - #9D4EDD

@dataclass
class FiefdomData:
    name: str
    files: List[str]
    entry_points: List[str]
    exports: List[str]
    internal_coupling: float  # 0-1
    external_coupling: float  # 0-1
    
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
    """Parse and validate settlement survey JSON."""
    # Validate required top-level keys
    required = ['metadata', 'fiefdoms', 'boundary_contracts', 'wiring_state']
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required survey field: {key}")
    
    # Parse fiefdoms
    fiefdoms = {}
    for name, fief_data in data['fiefdoms'].items():
        fiefdoms[name] = FiefdomData(**fief_data)
    
    # Parse boundary contracts
    contracts = [BoundaryContract(**bc) for bc in data['boundary_contracts']]
    
    # Parse wiring state
    wiring = []
    for wire in data['wiring_state']:
        wire['status'] = WiringStatus(wire['status'])
        wiring.append(WiringConnection(**wire))
    
    return SettlementSurvey(
        metadata=data['metadata'],
        fiefdoms=fiefdoms,
        boundary_contracts=contracts,
        wiring_state=wiring
    )

# Example fixture for testing
EXAMPLE_SURVEY = {
    "metadata": {"project": "Orchestr8", "timestamp": "2026-02-13"},
    "fiefdoms": {
        "core": {
            "name": "core",
            "files": ["orchestr8.py"],
            "entry_points": ["orchestr8.py"],
            "exports": ["STATE_MANAGERS"],
            "internal_coupling": 0.9,
            "external_coupling": 0.3
        }
    },
    "boundary_contracts": [],
    "wiring_state": []
}
```

**Test Strategy:**

Test parse_settlement_survey(EXAMPLE_SURVEY) succeeds. Test with missing fields raises ValueError. Verify WiringStatus enum maps to correct color values.

## Subtasks

### 4.1. Create contracts directory and base file structure

**Status:** pending  
**Dependencies:** None  

Create the IP/contracts directory and settlement_survey.py file with required imports

**Details:**

Create IP/contracts/ directory if it doesn't exist, then create settlement_survey.py with imports: typing (Dict, List, Any, Optional), dataclasses (dataclass, field), and enum (Enum). Add an empty __init__.py to make it a proper Python package.

### 4.2. Implement WiringStatus enum and FiefdomData dataclass

**Status:** pending  
**Dependencies:** 4.1  

Create the WiringStatus enum with three states and the FiefdomData dataclass for fiefdom information

**Details:**

Implement WiringStatus enum with WORKING='working' (#D4AF37 Gold), BROKEN='broken' (#1fbdea Teal), COMBAT='combat' (#9D4EDD Purple). Then implement FiefdomData dataclass with fields: name (str), files (List[str]), entry_points (List[str]), exports (List[str]), internal_coupling (float 0-1), external_coupling (float 0-1).

### 4.3. Implement BoundaryContract and WiringConnection dataclasses

**Status:** pending  
**Dependencies:** 4.2  

Create the BoundaryContract and WiringConnection dataclasses for inter-fiefdom relationships

**Details:**

Implement BoundaryContract dataclass with fields: from_fiefdom (str), to_fiefdom (str), allowed_types (List[str]), forbidden_crossings (List[str]), contract_status (str - 'defined'|'draft'|'missing'). Implement WiringConnection dataclass with fields: source (str), target (str), status (WiringStatus), agents_active (bool, default=False).

### 4.4. Implement SettlementSurvey dataclass and parse function

**Status:** pending  
**Dependencies:** 4.3  

Create the main SettlementSurvey dataclass and parse_settlement_survey validation function

**Details:**

Implement SettlementSurvey dataclass with fields: metadata (Dict[str, Any]), fiefdoms (Dict[str, FiefdomData]), boundary_contracts (List[BoundaryContract]), wiring_state (List[WiringConnection]). Implement parse_settlement_survey(data: Dict[str, Any]) -> SettlementSurvey that validates required keys, parses fiefdoms dict to FiefdomData, converts boundary_contracts list to BoundaryContract objects, and converts wiring_state with WiringStatus enum conversion.

### 4.5. Add EXAMPLE_SURVEY fixture and export module API

**Status:** pending  
**Dependencies:** 4.4  

Add the example survey fixture for testing and configure module exports in __init__.py

**Details:**

Add EXAMPLE_SURVEY dict constant with metadata (project, timestamp), fiefdoms ('core' with all FiefdomData fields), empty boundary_contracts list, and empty wiring_state list. Update IP/contracts/__init__.py to export: WiringStatus, FiefdomData, BoundaryContract, WiringConnection, SettlementSurvey, parse_settlement_survey, EXAMPLE_SURVEY.

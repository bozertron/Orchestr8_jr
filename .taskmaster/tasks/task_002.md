# Task ID: 2

**Title:** Implement CodeCityNodeEvent schema

**Status:** done

**Dependencies:** 1 ✓

**Priority:** high

**Description:** Create strongly-typed schema for Code City node click events with validation

**Details:**

Create IP/contracts/code_city_node_event.py with TypedDict or dataclass schema matching the JS event payload from woven_maps.py.

Implementation:
```python
from typing import Literal, Optional, TypedDict, List
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
    """Validate and parse node click payload into CodeCityNodeEvent.
    
    Raises ValueError on malformed payload.
    """
    required = ['path', 'status', 'loc']
    for key in required:
        if key not in payload:
            raise ValueError(f"Missing required field: {key}")
    
    if payload['status'] not in ('working', 'broken', 'combat'):
        raise ValueError(f"Invalid status: {payload['status']}")
    
    return CodeCityNodeEvent(
        path=payload['path'],
        status=payload['status'],
        loc=int(payload['loc']),
        errors=payload.get('errors', []),
        nodeType=payload.get('nodeType'),
        centrality=payload.get('centrality'),
        inCycle=payload.get('inCycle'),
        incomingCount=payload.get('incomingCount'),
        outgoingCount=payload.get('outgoingCount')
    )

# Example payload for testing
EXAMPLE_NODE_EVENT = {
    'path': 'IP/woven_maps.py',
    'status': 'broken',
    'loc': 2847,
    'errors': ['TypeError on line 42'],
    'nodeType': 'file',
    'centrality': 0.85,
    'inCycle': False,
    'incomingCount': 12,
    'outgoingCount': 8
}
```

**Test Strategy:**

Unit test validation function with valid/invalid payloads. Test that validate_code_city_node_event(EXAMPLE_NODE_EVENT) succeeds and malformed payloads raise ValueError.

## Subtasks

### 2.1. Create IP/contracts directory and __init__.py module

**Status:** pending  
**Dependencies:** None  

Initialize the contracts package directory structure with proper Python module setup

**Details:**

Create the IP/contracts/ directory and add an __init__.py file that will export the CodeCityNodeEvent schema and validate_code_city_node_event function. The __init__.py should include: `from .code_city_node_event import CodeCityNodeEvent, CodeCityStatus, validate_code_city_node_event, EXAMPLE_NODE_EVENT`

### 2.2. Implement CodeCityStatus type alias and CodeCityNodeEvent dataclass

**Status:** pending  
**Dependencies:** 2.1  

Create the core dataclass schema matching the JS event payload structure from woven_maps.py CodeNode

**Details:**

Create IP/contracts/code_city_node_event.py with: (1) CodeCityStatus = Literal['working', 'broken', 'combat'] type alias, (2) CodeCityNodeEvent dataclass with required fields (path: str, status: CodeCityStatus, loc: int) and optional fields (errors: List[str], nodeType: Optional[str], centrality: Optional[float], inCycle: Optional[bool], incomingCount: Optional[int], outgoingCount: Optional[int]), (3) to_dict() method using dataclasses.asdict(). Field naming must use camelCase to match JS payload (nodeType not node_type) unlike Python-side CodeNode which uses snake_case.

### 2.3. Implement validate_code_city_node_event validation function

**Status:** pending  
**Dependencies:** 2.2  

Create the validation function that parses dict payloads into typed CodeCityNodeEvent instances

**Details:**

Add validate_code_city_node_event(payload: dict) -> CodeCityNodeEvent function that: (1) Checks required fields ['path', 'status', 'loc'] exist, raising ValueError with specific field name if missing, (2) Validates status is one of ('working', 'broken', 'combat'), raising ValueError if invalid, (3) Coerces loc to int for robustness, (4) Extracts optional fields with .get() defaulting to None or [], (5) Returns constructed CodeCityNodeEvent instance. Function should be defensive but not overly strict on optional fields.

### 2.4. Add EXAMPLE_NODE_EVENT fixture and docstrings

**Status:** pending  
**Dependencies:** 2.2  

Create the example payload constant for testing and documentation purposes

**Details:**

Add EXAMPLE_NODE_EVENT dict constant matching the specification: {'path': 'IP/woven_maps.py', 'status': 'broken', 'loc': 2847, 'errors': ['TypeError on line 42'], 'nodeType': 'file', 'centrality': 0.85, 'inCycle': False, 'incomingCount': 12, 'outgoingCount': 8}. Add comprehensive docstrings to the dataclass and validation function explaining the schema's purpose as the bridge between JS Code City events and Python handlers.

### 2.5. Write unit tests for CodeCityNodeEvent schema and validation

**Status:** pending  
**Dependencies:** 2.3, 2.4  

Create comprehensive test coverage for the schema validation edge cases

**Details:**

Create test file (location TBD based on project test structure) with tests: (1) test_valid_minimal_payload - only required fields, (2) test_valid_full_payload - all fields including EXAMPLE_NODE_EVENT, (3) test_missing_required_field_path/status/loc - each raises ValueError with field name, (4) test_invalid_status_value - non-enum value raises ValueError, (5) test_loc_coercion - string '100' coerces to int 100, (6) test_to_dict_roundtrip - to_dict() output can be re-validated, (7) test_optional_fields_default_none - unspecified optionals are None

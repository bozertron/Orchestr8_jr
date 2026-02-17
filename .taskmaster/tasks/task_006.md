# Task ID: 6

**Title:** Add unit tests for contract schemas

**Status:** done

**Dependencies:** 2 ✓, 3 ✓, 4 ✓, 5 ✓

**Priority:** medium

**Description:** Create comprehensive unit tests for all four schema modules

**Details:**

Create tests/ directory and test files for each schema module.

Files to create:
- tests/__init__.py
- tests/test_code_city_node_event.py
- tests/test_camera_state.py
- tests/test_settlement_survey.py
- tests/test_status_merge_policy.py

Each test file should:
1. Test valid payloads succeed
2. Test invalid payloads raise appropriate errors
3. Test edge cases (empty lists, None values, out-of-range numbers)
4. Test serialization/deserialization roundtrips
5. Use pytest fixtures for reusable test data

Example test structure:
```python
import pytest
from IP.contracts.code_city_node_event import validate_code_city_node_event, EXAMPLE_NODE_EVENT

def test_valid_node_event():
    result = validate_code_city_node_event(EXAMPLE_NODE_EVENT)
    assert result.path == 'IP/woven_maps.py'
    assert result.status == 'broken'

def test_missing_required_field():
    invalid = {'status': 'broken', 'loc': 100}  # Missing 'path'
    with pytest.raises(ValueError, match="Missing required field: path"):
        validate_code_city_node_event(invalid)

def test_invalid_status():
    invalid = {**EXAMPLE_NODE_EVENT, 'status': 'unknown'}
    with pytest.raises(ValueError, match="Invalid status"):
        validate_code_city_node_event(invalid)
```

Run tests with: pytest tests/ -v

**Test Strategy:**

All tests pass with pytest. Coverage > 90% for each schema module. Edge cases handled correctly without crashes.

## Subtasks

### 6.1. Create tests directory structure and __init__.py

**Status:** pending  
**Dependencies:** None  

Initialize the tests/ directory with proper package structure for pytest discovery

**Details:**

Create the tests/ directory at the project root level alongside IP/. Add tests/__init__.py as an empty file to make it a proper Python package. Verify pytest can discover the test directory by running 'pytest tests/ --collect-only'. This establishes the foundation for all subsequent test files.

### 6.2. Write test_code_city_node_event.py with comprehensive test coverage

**Status:** pending  
**Dependencies:** 6.1  

Create unit tests for CodeCityNodeEvent schema covering valid payloads, invalid payloads, and edge cases

**Details:**

Create tests/test_code_city_node_event.py with pytest fixtures for reusable test data. Test cases must include: (1) test_valid_node_event - validates EXAMPLE_NODE_EVENT succeeds and fields match, (2) test_missing_required_field - missing 'path' raises ValueError, (3) test_invalid_status - status not in ['working','broken','combat'] raises ValueError, (4) test_invalid_loc_type - non-integer loc raises error, (5) test_empty_errors_list - empty list is valid, (6) test_none_optional_fields - nodeType=None is valid, (7) test_serialization_roundtrip - asdict() and reconstruction preserves data. Use @pytest.fixture for valid_event_data and invalid_event_variants.

### 6.3. Write test_camera_state.py testing defaults and utility methods

**Status:** pending  
**Dependencies:** 6.1  

Create unit tests for CameraState schema including default factory, clamp_zoom, and normalize_position utilities

**Details:**

Create tests/test_camera_state.py with comprehensive tests: (1) test_get_default_camera_state - returns valid CameraState with expected defaults (mode='overview', zoom in range), (2) test_all_camera_modes_valid - iterate CameraMode literals and verify each works, (3) test_clamp_zoom_lower_bound - values below min clamped correctly, (4) test_clamp_zoom_upper_bound - values above max clamped correctly, (5) test_clamp_zoom_within_range - valid values unchanged, (6) test_normalize_position_tuple - 3-tuple floats work, (7) test_invalid_position_length - wrong tuple size raises error, (8) test_return_stack_default_empty - default factory creates empty list, (9) test_serialization_roundtrip - asdict() reconstruction preserves all fields. Use fixtures for default and custom camera states.

### 6.4. Write test_settlement_survey.py and test_status_merge_policy.py

**Status:** pending  
**Dependencies:** 6.1  

Create unit tests for nested SettlementSurvey structure and StatusMergePolicy precedence rules with color mapping

**Details:**

Create tests/test_settlement_survey.py: (1) test_valid_settlement_survey - EXAMPLE passes validation, (2) test_nested_room_structure - rooms within files validate correctly, (3) test_empty_rooms_list - files can have empty rooms, (4) test_invalid_fiefdom_id - non-string ID raises error, (5) test_missing_required_nested_field - missing room.name raises error, (6) test_serialization_roundtrip - nested structures survive asdict/reconstruction. Create tests/test_status_merge_policy.py: (1) test_combat_takes_precedence - combat > broken > working, (2) test_broken_over_working - broken beats working, (3) test_same_status_merge - identical statuses return same, (4) test_color_mapping_working - returns '#D4AF37' (Gold), (5) test_color_mapping_broken - returns '#1fbdea' (Blue), (6) test_color_mapping_combat - returns '#9D4EDD' (Purple), (7) test_invalid_status_color - unknown status raises error. Use fixtures for survey structures and status pairs.

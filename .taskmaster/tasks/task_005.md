# Task ID: 5

**Title:** Implement status merge policy

**Status:** done

**Dependencies:** 1 ✓

**Priority:** high

**Description:** Create canonical status merge function following combat > broken > working precedence

**Details:**

Create IP/contracts/status_merge_policy.py implementing the three-state color system merge logic.

Implementation:
```python
from typing import Literal, Iterable, Optional

StatusType = Literal["working", "broken", "combat"]

# Canonical precedence: combat > broken > working
STATUS_PRIORITY = {
    "combat": 3,
    "broken": 2,
    "working": 1
}

def merge_status(*statuses: StatusType) -> StatusType:
    """Merge multiple status values using canonical precedence.
    
    Rule: combat > broken > working
    
    Args:
        *statuses: Variable number of status strings
        
    Returns:
        The highest-priority status
        
    Raises:
        ValueError: If any status is unknown/invalid
    
    Examples:
        >>> merge_status("working", "broken")
        "broken"
        >>> merge_status("working", "working", "combat")
        "combat"
        >>> merge_status("broken", "broken")
        "broken"
    """
    if not statuses:
        return "working"  # Default to working
    
    # Filter out None/null values
    valid_statuses = [s for s in statuses if s is not None]
    
    if not valid_statuses:
        return "working"
    
    # Validate all statuses
    for status in valid_statuses:
        if status not in STATUS_PRIORITY:
            raise ValueError(f"Unknown status value: {status}")
    
    # Return highest priority
    return max(valid_statuses, key=lambda s: STATUS_PRIORITY[s])

def get_status_color(status: StatusType) -> str:
    """Get hex color for status.
    
    Returns:
        Hex color string matching canonical color system
    """
    colors = {
        "working": "#D4AF37",  # Gold
        "broken": "#1fbdea",   # Blue/Teal
        "combat": "#9D4EDD"    # Purple
    }
    return colors.get(status, "#D4AF37")  # Default to gold
```

**Test Strategy:**

Unit tests: merge_status('working', 'broken') == 'broken', merge_status('combat', 'working', 'broken') == 'combat', merge_status() == 'working', merge_status('invalid') raises ValueError, get_status_color('combat') == '#9D4EDD'

## Subtasks

### 5.1. Create IP/contracts directory and status_merge_policy.py module

**Status:** pending  
**Dependencies:** None  

Create the contracts directory structure and initialize the status_merge_policy.py file with module docstring and imports

**Details:**

Create IP/contracts/ directory if not exists. Create __init__.py for package. Create status_merge_policy.py with typing imports (Literal, Iterable, Optional) and module-level docstring explaining the three-state color system merge logic.

### 5.2. Define StatusType literal and STATUS_PRIORITY constant

**Status:** pending  
**Dependencies:** 5.1  

Create the StatusType type alias and STATUS_PRIORITY dict establishing combat > broken > working precedence

**Details:**

Define StatusType = Literal['working', 'broken', 'combat'] for type safety. Define STATUS_PRIORITY dict mapping each status to integer priority (combat=3, broken=2, working=1). Add inline comments explaining the canonical precedence rule.

### 5.3. Implement merge_status function with validation

**Status:** pending  
**Dependencies:** 5.2  

Create the merge_status(*statuses) function implementing priority-based merge with input validation

**Details:**

Implement merge_status using max() with STATUS_PRIORITY key lookup. Handle empty input (return 'working'). Filter None values. Validate all inputs against STATUS_PRIORITY keys, raising ValueError for unknown statuses. Include comprehensive docstring with examples.

### 5.4. Implement get_status_color helper function

**Status:** pending  
**Dependencies:** 5.2  

Create get_status_color(status) function returning canonical hex colors for each status

**Details:**

Implement simple dict lookup for status colors: working=#D4AF37 (Gold), broken=#1fbdea (Blue/Teal), combat=#9D4EDD (Purple). Default to gold for unknown status. Add docstring documenting return type and color mapping.

### 5.5. Export public API in __init__.py and add type exports

**Status:** pending  
**Dependencies:** 5.3, 5.4  

Update IP/contracts/__init__.py to export merge_status, get_status_color, StatusType, and STATUS_PRIORITY

**Details:**

Add from .status_merge_policy import merge_status, get_status_color, StatusType, STATUS_PRIORITY to __init__.py. Define __all__ list for explicit public API. Verify imports work from IP.contracts namespace.

# Task ID: 9

**Title:** Update woven_maps.py to use status merge policy

**Status:** done

**Dependencies:** 5 ✓, 7 ✓

**Priority:** medium

**Description:** Integrate status_merge_policy into build_from_health_results function

**Details:**

Update IP/woven_maps.py to use the canonical merge_status function when combining health check results with existing node status.

Modify build_from_health_results() function (around line 527):
```python
from IP.contracts.status_merge_policy import merge_status

def build_from_health_results(
    nodes: List[CodeNode], health_results: Dict[str, Any]
) -> List[CodeNode]:
    """Merge HealthChecker output into CodeNode objects.
    
    Uses canonical status merge policy: combat > broken > working
    """
    for node in nodes:
        for path, result in health_results.items():
            if path in node.path or node.path.startswith(path.rstrip("/")):
                # Use canonical merge instead of manual override
                health_status = "broken" if result.status == "broken" else "working"
                node.status = merge_status(node.status, health_status)
                
                if hasattr(result, "errors") and result.errors:
                    node.health_errors = [
                        {"file": e.file, "line": e.line, "message": e.message}
                        for e in result.errors[:10]
                    ]
                break
    
    return nodes
```

This ensures:
- Combat status is never overridden by health results
- Merge logic is consistent across the codebase
- Status precedence is enforced via contract

**Test Strategy:**

Unit test: node with status='combat' + health='broken' → final status='combat'. Node with status='working' + health='broken' → final status='broken'. Verify merge_status is called correctly.

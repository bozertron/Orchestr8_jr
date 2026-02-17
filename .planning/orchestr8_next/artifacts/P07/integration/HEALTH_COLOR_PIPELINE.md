# Health Check to Code City Color Mapping Pipeline

**Research Date:** 2026-02-16  
**Focus:** Understanding the data flow from HealthChecker through GraphBuilder to WovenMaps visualization  
**Status:** Analysis Complete

---

## Executive Summary

This document analyzes the pipeline that maps static analysis health check results (errors/warnings) to Code City node colors (gold/teal/purple). The pipeline is functional but has gaps in field propagation.

---

## 1. How Health Status Becomes Node Color

### The Transformation Chain

```
HealthChecker (static analysis)
    ↓
HealthCheckResult {status, errors, warnings, ...}
    ↓
build_from_health_results() merges into CodeNode
    ↓
CodeNode.status determines color via get_status_color()
    ↓
Woven Maps renders colored buildings
```

### Color Mapping (from `IP/contracts/status_merge_policy.py`)

| Status    | Hex Color  | Name       | Source                      |
|-----------|------------|------------|-----------------------------|
| working   | `#D4AF37`  | Gold       | No errors detected          |
| broken    | `#1fbdea`  | Teal/Blue  | Errors detected             |
| combat    | `#9D4EDD`  | Purple     | LLM actively deployed      |

### Code References

**Status to Color mapping** (`IP/contracts/status_merge_policy.py:36-43`):
```python
def get_status_color(status: StatusType) -> str:
    """Get canonical hex color for a status value."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
    }
    return colors.get(status, "#D4AF37")
```

---

## 2. The merge_status Logic

### Priority Chain

The `merge_status()` function in `IP/contracts/status_merge_policy.py` implements a strict precedence hierarchy:

```python
STATUS_PRIORITY = {
    "combat": 3,   # Highest priority - LLM active overrides all
    "broken": 2,   # Second priority - errors present
    "working": 1,  # Lowest priority - clean code
}
```

### Merge Rules

1. **Combat dominates everything** - If any source status is "combat", result is "combat"
2. **Broken dominates working** - "broken" + "working" = "broken"
3. **Working only wins if all inputs are working**
4. **Empty/None input defaults to "working"**

### Test Examples (from `IP/contracts/tests/test_status_merge_policy.py`)

```python
assert merge_status("combat", "broken", "working") == "combat"  # Combat wins
assert merge_status("broken", "working") == "broken"           # Broken wins
assert merge_status("working", "working") == "working"         # All working
assert merge_status() == "working"                             # Empty = working
```

### Where merge_status is Used

1. **`IP/features/code_city/graph_builder.py:364`** - Merges health check status into CodeNode:
   ```python
   node.status = merge_status(node.status, status)
   ```

2. **`IP/features/code_city/graph_builder.py:64-74`** - Neighborhood status aggregation:
   ```python
   status_counts = {"working": 0, "broken": 0, "combat": 0}
   for node in dir_nodes:
       if node.status in status_counts:
           status_counts[node.status] += 1
   
   if status_counts["combat"] > 0:
       status = "broken"  # Note: This appears to be a bug - should be "combat"
   elif status_counts["broken"] > status_counts["working"]:
       status = "broken"
   else:
       status = "working"
   ```

---

## 3. Data Flow Pipeline

### Complete Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          HEALTH CHECK PIPELINE                               │
└─────────────────────────────────────────────────────────────────────────────┘

1. HEALTH CHECKER
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/health_checker.py                                                   │
   │  HealthChecker.check_fiefdom(fiefdom_path)                              │
   │       ↓                                                                 │
   │  ┌──────────────────────────────────────────────────────────────────┐   │
   │  │ Runs: mypy, ruff, py_compile, typescript (npm run typecheck)   │   │
   │  └──────────────────────────────────────────────────────────────────┘   │
   │       ↓                                                                 │
   │  Returns: HealthCheckResult                                           │
   │  {                                                                       │
   │    status: "working" | "broken",                                       │
   │    errors: [ParsedError...],                                           │
   │    warnings: [ParsedError...],  ← NOT USED IN MERGE                  │
   │    last_check: "ISO timestamp",                                        │
   │    checker_used: "mypy, ruff, ..."                                    │
   │  }                                                                       │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
2. STATE MANAGEMENT (Marimo)
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/plugins/06_maestro.py                                              │
   │                                                                            │
   │  get_health(), set_health() = mo.state({})                            │
   │                                                                            │
   │  refresh_health():                                                      │
   │    health_checker = HealthChecker(str(project_root_path))              │
   │    result = health_checker.check_fiefdom("IP")                        │
   │    set_health({"IP": result})                                          │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
3. REAL-TIME WATCHER (optional)
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/health_watcher.py                                                   │
   │                                                                            │
   │  HealthWatcher - watches file changes, debounces 100ms                  │
   │  HealthWatcherManager - Marimo-integrated, debounces 300ms             │
   │                                                                            │
   │  File Change → Debounce → HealthChecker → callback → set_health()     │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
4. CODE CITY RENDER
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/features/code_city/render.py                                        │
   │                                                                            │
   │  create_code_city(root, health_results=health_data or None)           │
   │       ↓                                                                 │
   │  graph_data = build_from_connection_graph(root, ...)                  │
   │       ↓                                                                 │
   │  if health_results:                                                    │
   │      graph_data.nodes = build_from_health_results(nodes, health_results)
   │       ↓                                                                 │
   │  graph_data.to_json() → embedded in iframe srcdoc                    │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
5. GRAPH BUILDER MERGE
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/features/code_city/graph_builder.py                                │
   │                                                                            │
   │  build_from_health_results(nodes, health_results):                    │
   │       ↓                                                                 │
   │  for each node:                                                         │
   │    for each path, result in health_results:                            │
   │      if path matches node.path:                                        │
   │        status = result.status  ("working" | "broken")                │
   │        node.status = merge_status(node.status, status)                │
   │        node.health_errors = [error.dict for error in result.errors]   │
   │                                                                            │
   │  NOTE: warnings are NOT merged into nodes!                             │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
6. NEIGHBORHOOD AGGREGATION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/features/code_city/graph_builder.py                                │
   │                                                                            │
   │  compute_neighborhoods(nodes, edges, width, height):                  │
   │       ↓                                                                 │
   │  For each directory (neighborhood):                                     │
   │    Count node statuses: {working, broken, combat}                      │
   │    Aggregate status = merge of all node statuses                       │
   │    neighborhood.status = aggregated status                             │
   │                                                                            │
   │  NOTE: Doesn't directly use HealthCheckResult - only node.status      │
   └─────────────────────────────────────────────────────────────────────────┘
                                    ↓
7. FRONTEND RENDERING
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  IP/static/woven_maps_3d.js / Woven Maps template                      │
   │                                                                            │
   │  Reads: node.status from graph_data JSON                                │
   │  Maps to CSS/Three.js colors:                                           │
   │    "working" → #D4AF37 (gold)                                           │
   │    "broken"  → #1fbdea (teal)                                           │
   │    "combat"  → #9D4EDD (purple)                                         │
   └─────────────────────────────────────────────────────────────────────────┘
```

### Key Code Paths

| Step | File | Function | Purpose |
|------|------|----------|---------|
| 1 | `IP/health_checker.py` | `HealthChecker.check_fiefdom()` | Run static analysis |
| 2 | `IP/plugins/06_maestro.py` | `refresh_health()` | Store results in state |
| 3 | `IP/features/code_city/render.py` | `create_code_city()` | Entry point for rendering |
| 4 | `IP/features/code_city/graph_builder.py` | `build_from_health_results()` | Merge health into nodes |
| 5 | `IP/features/code_city/graph_builder.py` | `compute_neighborhoods()` | Aggregate neighborhood status |
| 6 | `IP/woven_maps.py` | `CodeNode.to_dict()` | Serialize for frontend |

---

## 4. Fields Produced vs Fields Used

### HealthCheckResult Full Output

```python
@dataclass
class HealthCheckResult:
    status: str                           # ✓ USED in merge
    errors: List[ParsedError]            # ✓ USED in merge (health_errors)
    warnings: List[ParsedError]          # ✗ NOT USED
    last_check: str                      # ✗ NOT USED
    checker_used: str                     # ✗ NOT USED
    raw_output: str                      # ✗ NOT USED
```

### ParsedError Structure

```python
@dataclass
class ParsedError:
    file: str                            # Used
    line: int                           # Used
    column: int = 0                     # NOT EXTRACTED in merge
    error_code: str = ""                 # NOT EXTRACTED in merge  
    message: str = ""                   # Used
    severity: str = "error"              # NOT USED (would enable warning color)
```

### CodeNode After Merge

```python
@dataclass
class CodeNode:
    path: str
    status: str                          # ✓ Updated via merge_status()
    errors: List[str]                    # Original scan errors (TODO/FIXME detection)
    health_errors: List[Any]             # ✓ Health check errors merged here
    # ... other fields
```

---

## 5. Identified Gaps and Issues

### Gap 1: Warnings Not Propagated

**Problem:** `HealthCheckResult.warnings` is never merged into CodeNode.

**Impact:** 
- Linters like ruff report warnings (e.g., W503 line break before binary operator)
- These are stored but discarded before visualization
- Users cannot see warning count in Code City

**Current behavior:** Only errors trigger "broken" status. Warnings have no visual representation.

### Gap 2: Neighborhood Status Logic Bug

**Location:** `IP/features/code_city/graph_builder.py:69-70`

```python
if status_counts["combat"] > 0:
    status = "broken"  # BUG: Should be "combat"
```

**Problem:** When a neighborhood has combat nodes, the aggregated status is set to "broken" instead of "combat", losing the combat designation.

**Expected behavior:** Combat should propagate up (like it does for individual nodes).

### Gap 3: Missing Warning Color

**Problem:** No visual distinction for files with warnings only (no errors).

**Potential enhancement:** Introduce a fourth status or warning indicator:
- Current: working (gold), broken (teal), combat (purple)
- Possible: Add warning count to tooltip, or subtle color shift

### Gap 4: HealthWatcherManager Not Fully Integrated

**Location:** `IP/health_watcher.py:280-304`

**Problem:** `HealthWatcherManager.start()` attempts to use Marimo's `FileWatcherManager` but falls back to polling. The fallback path may not trigger reactive state updates properly.

---

## 6. Recommendations

### Priority 1: Fix Neighborhood Combat Status

```python
# Current (buggy):
if status_counts["combat"] > 0:
    status = "broken"  # Wrong!

# Should be:
if status_counts["combat"] > 0:
    status = "combat"
```

### Priority 2: Propagate Warnings

Option A: Add warning field to CodeNode and display in tooltip
```python
@dataclass
class CodeNode:
    # ... existing fields
    health_warnings: List[Any] = field(default_factory=list)
```

Option B: Add warning count to neighborhood status calculation
```python
if status_counts["combat"] > 0:
    status = "combat"
elif status_counts["broken"] > 0:
    status = "broken"
elif status_counts["working"] > 0:
    status = "working"
# Add warning indicator
```

### Priority 3: Extract Full ParsedError Data

In `build_from_health_results()`, extract all fields:
```python
def _to_error_dict(error: Any) -> Dict[str, Any]:
    if isinstance(error, dict):
        return {
            "file": str(error.get("file", "")),
            "line": int(error.get("line", 0) or 0),
            "column": int(error.get("column", 0) or 0),  # ADD
            "error_code": str(error.get("error_code", "")),  # ADD
            "message": str(error.get("message", "")),
            "severity": str(error.get("severity", "error")),  # ADD
        }
```

---

## 7. Test Coverage

Existing tests in `IP/features/code_city/tests/test_health_flow.py`:

| Test | Purpose |
|------|---------|
| `test_health_watcher_debounced_check_invokes_callback` | Watcher → callback flow |
| `test_health_results_merge_promotes_working_to_broken` | Status override |
| `test_health_results_merge_preserves_combat_precedence` | Combat priority |
| `test_health_results_merge_accepts_dict_payloads` | Dict input support |
| `test_compute_neighborhoods_groups_nodes_by_parent_directory` | Neighborhood grouping |

Missing tests:
- Warning propagation
- Neighborhood combat aggregation
- Full ParsedError field extraction

---

## 8. Source Files Reference

| File | Lines | Purpose |
|------|-------|---------|
| `IP/health_checker.py` | 624 | Static analysis runner |
| `IP/health_watcher.py` | 350 | File change detection |
| `IP/contracts/status_merge_policy.py` | 44 | Status precedence logic |
| `IP/features/code_city/graph_builder.py` | 372 | Graph assembly + health merge |
| `IP/features/code_city/render.py` | 163 | Code City iframe assembly |
| `IP/woven_maps.py` | 947 | Core data structures + scan |
| `IP/plugins/06_maestro.py` | ~1200 | UI orchestration |

---

## Conclusion

The health → color pipeline is functional for the basic case (errors → teal nodes). However, there are notable gaps:

1. **Warnings are discarded** - No visual representation of linting warnings
2. **Neighborhood combat bug** - Combat status doesn't propagate to neighborhoods
3. **Missing metadata** - Column, error_code, severity not passed to frontend

The pipeline architecture is sound, but needs the above fixes to fully realize the health visualization contract.

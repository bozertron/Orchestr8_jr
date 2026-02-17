# ARCHITECT-HEALTHCHECKER.md
## Settlement System Architecture Plan
## Generated: 2026-02-12
## Status: READY FOR WORK ORDER COMPILER

---

## 1. Current State Analysis

### health_checker.py (602 lines)
| Aspect | Status | Notes |
|--------|--------|-------|
| Core Logic | COMPLETE | Multi-language (TS, Python mypy/ruff/py_compile) |
| Output Structure | COMPLETE | `ParsedError`, `HealthCheckResult` dataclasses |
| Integration | MISSING | Standalone - no reactive wiring |
| State Management | MISSING | No STATE_MANAGERS connection |

**Key Methods:**
- `check_fiefdom(path)` → `HealthCheckResult`
- `check_all_fiefdoms(paths)` → `Dict[str, HealthCheckResult]`
- `get_errors_for_file(path)` → `List[ParsedError]`

### woven_maps.py (1358+ lines)
| Aspect | Status | Notes |
|--------|--------|-------|
| Visualization | COMPLETE | Emergence animations, particle system |
| CodeNode.status | EXISTS | working/broken/combat - NOT populated from HealthChecker |
| Health Integration | MISSING | `analyze_file()` only does TODO/FIXME detection |
| Combat Integration | COMPLETE | Uses CombatTracker for purple status |

**Gap:** `analyze_file()` at L234-269 does lightweight scan, ignores HealthChecker.

### 06_maestro.py (1298 lines)
| Aspect | Status | Notes |
|--------|--------|-------|
| HealthChecker Import | EXISTS | L77 - imported but unused |
| STATE_MANAGERS | EXISTS | root, selected, logs - NO health state |
| Code City Render | EXISTS | `build_code_city()` calls `create_code_city()` |
| Node Click Handler | EXISTS | `handle_node_click()` for deploy panel |

**Gap:** No health state in STATE_MANAGERS, no reactive health updates.

---

## 2. Approach: PRESERVE / REFACTOR / CREATE

### PRESERVE (No Changes)
- `health_checker.py` core logic - solid, don't touch
- `woven_maps.py` visualization engine - works
- `06_maestro.py` UI structure - stable

### REFACTOR (Modify Existing)
| File | Change |
|------|--------|
| `woven_maps.py` | Add `build_from_health_results()` to merge HealthChecker output |
| `woven_maps.py` | Modify `analyze_file()` to accept optional `HealthCheckResult` |
| `06_maestro.py` | Add `health` to STATE_MANAGERS |
| `06_maestro.py` | Wire HealthChecker in `build_code_city()` |

### CREATE (New Files)
| File | Purpose | LOC Est. |
|------|---------|----------|
| `IP/health_watcher.py` | File watcher + reactive health updates | ~150 |

---

## 3. Wave-by-Wave Modification Order

### Wave 1: State Infrastructure (Foundation)
**Target:** `06_maestro.py`
**Changes:**
1. Add `get_health, set_health` to STATE_MANAGERS
2. Initialize health state as `Dict[str, HealthCheckResult]`
3. Create `refresh_health()` function

**Tokens:** ~800 | **Complexity:** 1.2 | **Agents:** 3

### Wave 2: HealthWatcher Module (New)
**Target:** `IP/health_watcher.py` (NEW)
**Components:**
1. `HealthWatcher` class wrapping watchdog + HealthChecker
2. `start_watching(project_root, callback)` method
3. Debounce logic (100ms) for rapid file changes
4. Integration with Marimo's reactivity via callback

**Tokens:** ~1500 | **Complexity:** 1.5 | **Agents:** 3

### Wave 3: woven_maps Integration (Bridge)
**Target:** `IP/woven_maps.py`
**Changes:**
1. Add `build_from_health_results(nodes, health_results)` function
2. Modify `CodeNode` to store `health_errors: List[ParsedError]`
3. Update `scan_codebase()` to accept optional `HealthChecker` instance
4. Wire status: `broken` if health_result.errors exists

**Tokens:** ~1200 | **Complexity:** 1.3 | **Agents:** 3

### Wave 4: Maestro Health Wiring (Connect)
**Target:** `IP/plugins/06_maestro.py`
**Changes:**
1. Instantiate `HealthWatcher` in `render()`
2. Call `health_watcher.start_watching(root, on_health_change)`
3. `on_health_change()` updates `set_health(new_results)`
4. `build_code_city()` passes health state to visualization
5. Ensure cleanup on unmount

**Tokens:** ~1000 | **Complexity:** 1.4 | **Agents:** 3

### Wave 5: Room-Level Error Display (Visualization)
**Target:** `IP/woven_maps.py` (JS template)
**Changes:**
1. Tooltip shows specific errors per file (not just "has errors")
2. Error lines highlight in tooltip with line numbers
3. Prepare for future "Sitting Room" click-to-enter feature

**Tokens:** ~600 | **Complexity:** 1.2 | **Agents:** 3

---

## 4. Border Impact Assessment

### Borders TOUCHED by this work:

| Border | Direction | Contract Change |
|--------|-----------|-----------------|
| `health_checker.py` → `woven_maps.py` | OUT | Add `HealthCheckResult` → `CodeNode.status` mapping |
| `health_watcher.py` → `health_checker.py` | IN | Calls `check_fiefdom()`, no changes needed |
| `health_watcher.py` → `06_maestro.py` | OUT | Callback receives `Dict[str, HealthCheckResult]` |
| `06_maestro.py` → `STATE_MANAGERS` | OUT | New `health` key in state dict |
| `woven_maps.py` → `06_maestro.py` | IN | Accepts optional health results |

### Borders UNCHANGED (Explicit):
- `louis_core.py` - LOCKED per CONTEXT.md
- `combat_tracker.py` - Already integrated, no changes
- `connection_verifier.py` - Separate concern

---

## 5. Agent Estimates

Formula: `agents = ceil(tokens × complexity_multiplier / 2500) × 3`

| Wave | Tokens | Complexity | Calculation | Agents |
|------|--------|------------|-------------|--------|
| Wave 1 | 800 | 1.2 | ceil(960/2500) × 3 | **3** |
| Wave 2 | 1500 | 1.5 | ceil(2250/2500) × 3 | **3** |
| Wave 3 | 1200 | 1.3 | ceil(1560/2500) × 3 | **3** |
| Wave 4 | 1000 | 1.4 | ceil(1400/2500) × 3 | **3** |
| Wave 5 | 600 | 1.2 | ceil(720/2500) × 3 | **3** |

**Total Agents:** 15 (3 per wave × 5 waves)
**Sentinel Protocol:** Each wave has 1 primary + 2 sentinels

---

## 6. Data Flow (Post-Implementation)

```
File Change (disk)
    ↓
watchdog observer (health_watcher.py)
    ↓
HealthWatcher._on_file_change() [debounced 100ms]
    ↓
HealthChecker.check_fiefdom(changed_path)
    ↓
HealthCheckResult {status, errors, ...}
    ↓
callback(results_dict) → 06_maestro.py
    ↓
set_health(results_dict) → STATE_MANAGERS["health"]
    ↓
Marimo reactivity triggers re-render
    ↓
build_code_city() reads get_health()
    ↓
woven_maps.build_from_health_results(nodes, health)
    ↓
CodeNode.status = "broken" if errors else "working"
    ↓
Canvas renders: TEAL for broken, GOLD for working
```

---

## 7. Constraints Checklist

| Constraint | Compliance |
|------------|------------|
| NO polling - file watcher only | ✅ Using watchdog |
| Building TEAL for broken | ✅ Existing color system |
| NO breathing animations | ✅ Preserved |
| Three states only | ✅ working/broken/combat |
| NO red for errors | ✅ Teal (#1fbdea) |
| Data flow per CONTEXT.md | ✅ File→Watcher→Checker→STATE→City |

---

## 8. Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| watchdog | REQUIRED | `pip install watchdog` |
| Marimo FileWatcherManager | OPTIONAL | May use native Marimo instead |
| mypy/ruff | OPTIONAL | HealthChecker gracefully degrades if missing |

---

## 9. Success Criteria

1. ✅ Code City buildings turn TEAL when file has errors
2. ✅ Errors appear in tooltip on hover
3. ✅ Real-time updates within 100ms of file save
4. ✅ No polling - event-driven via file watcher
5. ✅ STATE_MANAGERS contains health state
6. ✅ HealthChecker core logic unchanged

---

**Document Status:** READY
**Next Step:** Work Order Compiler generates WAVE-1-HEALTHCHECKER-STATE.md
**Estimated Total LOC:** ~900 new/modified
**Estimated Duration:** 5 waves × 2-3 hours = 10-15 hours

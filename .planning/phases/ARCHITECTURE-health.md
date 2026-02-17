# ARCHITECTURE-health.md — Health Checking & Telemetry Fiefdom
## Generated: 2026-02-12
## Status: PLANNING COMPLETE

---

## 1. Current State Analysis

### What Exists

| Component | File | Lines | Status | Notes |
|-----------|------|-------|--------|-------|
| HealthChecker | `IP/health_checker.py` | 602 | COMPLETE | Multi-language (TS, mypy, ruff, py_compile) |
| Code City | `IP/woven_maps.py` | 1982 | COMPLETE | Emergence visualization, status field exists |
| State Manager | `orchestr8.py` | 240 | PARTIAL | Missing health state |
| Maestro Plugin | `IP/plugins/06_maestro.py` | 1298 | PARTIAL | Uses Code City, no health wiring |

### What's Missing

| Gap | Impact | Priority |
|-----|--------|----------|
| No health state in STATE_MANAGERS | Code City can't react to health changes | HIGH |
| No file watcher integration | Manual refresh only, violates LOCKED spec | HIGH |
| HealthChecker not wired to Code City | Status from simple analysis, not real checking | HIGH |
| No reactive flow | File Change → ... → Code City chain broken | HIGH |

### Current Data Flow (BROKEN)

```
Code City reads files → Simple analysis (TODO/FIXME) → Status
                     ↑
                     └── HealthChecker EXISTS but NOT CONNECTED
```

### LOCKED Data Flow (REQUIRED)

```
File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City
```

---

## 2. Approach Selection: **REFACTOR**

| Option | Rationale | Selected |
|--------|-----------|----------|
| Preserve | HealthChecker is complete, no changes needed to core logic | YES |
| Refactor | Woven Maps needs `apply_health_results()` injection point | YES |
| Restructure | STATE_MANAGERS extension is additive, not destructive | YES |
| Rebuild | Nothing needs complete replacement | NO |

### Why Refactor

1. **HealthChecker is production-ready** — Multi-language, optimized batch checking, proper error parsing
2. **Woven Maps has the plumbing** — `CodeNode.status` field exists, just needs external data source
3. **STATE_MANAGERS is extensible** — Add `health` key without breaking existing plugins
4. **New component required** — FileWatcher/HealthWatcher bridge doesn't exist anywhere

---

## 3. Wave-by-Wave Modification Order

### Wave 1: State Infrastructure [Foundation]
**Target:** `orchestr8.py`
**Dependency:** None (starts the chain)

#### Room: Cell 2 (state_management)
```python
# ADD to existing STATE_MANAGERS
get_health, set_health = mo.state({})  # Dict[str, HealthCheckResult]
get_health_status, set_health_status = mo.state("idle")  # "idle" | "checking" | "complete"

STATE_MANAGERS = {
    "root": (get_root, set_root),
    "files": (get_files, set_files),
    "selected": (get_selected, set_selected),
    "logs": (get_logs, set_logs),
    "health": (get_health, set_health),           # NEW
    "health_status": (get_health_status, set_health_status),  # NEW
}
```

**Files Changed:** 1
**Risk Level:** LOW (additive only)

---

### Wave 2: Health Watcher Bridge [New Component]
**Target:** `IP/health_watcher.py` (NEW FILE)
**Dependency:** Wave 1 (needs STATE_MANAGERS)

#### Room: HealthWatcher Class
```python
class HealthWatcher:
    """Bridges file changes to health checking with debouncing."""
    
    def __init__(self, project_root: str, state_setters: dict):
        self.project_root = Path(project_root)
        self.set_health = state_setters["health"]
        self.set_health_status = state_setters["health_status"]
        self.checker = HealthChecker(str(project_root))
        self._pending: Set[str] = set()
        self._debounce_ms = 300
        
    def on_file_change(self, file_path: str) -> None:
        """Called by file watcher. Debounces rapid changes."""
        self._pending.add(file_path)
        # Debounce logic...
        
    def run_check(self, fiefdom_paths: List[str]) -> Dict[str, HealthCheckResult]:
        """Execute health check and update state."""
        self.set_health_status("checking")
        results = self.checker.check_all_fiefdoms(fiefdom_paths)
        self.set_health(results)
        self.set_health_status("complete")
        return results
```

#### Room: Marimo Integration
```python
def create_health_watcher_cell(mo, STATE_MANAGERS):
    """Marimo cell that creates and manages the health watcher."""
    get_root, set_root = STATE_MANAGERS["root"]
    
    # Create watcher instance
    watcher = HealthWatcher(get_root(), {
        "health": STATE_MANAGERS["health"][1],
        "health_status": STATE_MANAGERS["health_status"][1],
    })
    
    # Initial check on root change
    # Future: Wire to Marimo FileWatcherManager when available
    return watcher
```

**Files Changed:** 1 (new)
**Risk Level:** MEDIUM (new component, integration complexity)

---

### Wave 3: Woven Maps Integration [Data Flow]
**Target:** `IP/woven_maps.py`
**Dependency:** Wave 2 (needs health data)

#### Room: build_graph_data() Modification
```python
def build_graph_data(
    root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 200,
    wire_count: int = 10,
    health_results: Optional[Dict[str, HealthCheckResult]] = None,  # NEW
) -> GraphData:
    """Build complete graph data from a codebase root."""
    nodes = scan_codebase(root)
    nodes = calculate_layout(nodes, width, height)
    
    # NEW: Apply health check results if provided
    if health_results:
        nodes = apply_health_results(nodes, health_results)
    
    # ... rest unchanged
```

#### Room: apply_health_results() Function
```python
def apply_health_results(
    nodes: List[CodeNode],
    health_results: Dict[str, HealthCheckResult]
) -> List[CodeNode]:
    """Apply health check results to CodeNode status."""
    for node in nodes:
        result = health_results.get(node.path)
        if result:
            node.status = result.status  # "working" | "broken"
            node.errors = [str(e) for e in result.errors[:10]]
    return nodes
```

#### Room: build_from_connection_graph() Modification
```python
def build_from_connection_graph(
    project_root: str,
    width: int = 800,
    height: int = 600,
    max_height: int = 250,
    wire_count: int = 15,
    health_results: Optional[Dict[str, HealthCheckResult]] = None,  # NEW
) -> GraphData:
    # ... existing logic ...
    
    # Apply health results after building nodes
    if health_results:
        nodes = apply_health_results(nodes, health_results)
    
    # ... rest unchanged
```

**Files Changed:** 1
**Risk Level:** LOW (optional parameter, graceful fallback)

---

### Wave 4: Maestro Plugin Update [UI Integration]
**Target:** `IP/plugins/06_maestro.py`
**Dependency:** Wave 3 (needs modified woven_maps)

#### Room: build_code_city() Modification
```python
def build_code_city() -> Any:
    """Build the Woven Maps Code City visualization with live health data."""
    root = get_root()
    
    if not root:
        return mo.Html("""...""")
    
    # NEW: Get health data from state
    get_health, _ = STATE_MANAGERS["health"]
    health_results = get_health()
    
    try:
        # Pass health results to Code City
        return create_code_city(
            root,
            width=850,
            height=500,
            health_results=health_results,  # NEW
        )
    except Exception as e:
        # ... error handling
```

#### Room: Health Refresh Trigger
```python
# Add to render() function
def refresh_health() -> None:
    """Trigger a health check refresh."""
    root = get_root()
    if not root:
        return
    
    # Scan for fiefdoms
    nodes = scan_codebase(root)
    fiefdom_paths = list(set(str(Path(n.path).parent) for n in nodes))
    
    # Run health check
    watcher = get_health_watcher()
    watcher.run_check(fiefdom_paths)
    log_action("Health check refreshed")
```

**Files Changed:** 1
**Risk Level:** LOW (uses existing patterns)

---

### Wave 5: File Watcher Integration [Real-Time]
**Target:** `IP/health_watcher.py` (extension)
**Dependency:** Wave 4 (UI needs to handle updates)

#### Room: Watchdog Integration
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

class HealthWatchHandler(FileSystemEventHandler):
    """Watchdog handler that triggers health checks on file changes."""
    
    def __init__(self, watcher: HealthWatcher):
        self.watcher = watcher
        self._debounce_timer = None
        
    def on_modified(self, event: FileModifiedEvent):
        if not event.is_directory and self._is_code_file(event.src_path):
            self.watcher.on_file_change(event.src_path)
            
    def _is_code_file(self, path: str) -> bool:
        return any(path.endswith(ext) for ext in ['.py', '.ts', '.tsx', '.js'])
```

#### Room: Observer Lifecycle
```python
def start_file_watcher(project_root: str, watcher: HealthWatcher) -> Observer:
    """Start the file system observer."""
    handler = HealthWatchHandler(watcher)
    observer = Observer()
    observer.schedule(handler, project_root, recursive=True)
    observer.start()
    return observer
```

**Files Changed:** 1 (extends Wave 2)
**Risk Level:** MEDIUM (async, thread safety)

---

## 4. Border Impact Analysis

### Inbound Borders (What This Fiefdom Receives)

| From | Border Type | Data | Contract |
|------|-------------|------|----------|
| Building Anatomy | IMPORT | `CodeNode.status` field | Status must be "working" \| "broken" \| "combat" |
| Color System | IMPORT | Color constants | Uses `#D4AF37`, `#1fbdea`, `#9D4EDD` |
| State Management | IMPORT | STATE_MANAGERS dict | Read `root`, write `health` |
| Combat Tracker | IMPORT | Active deployments | Combat status overrides health status |

### Outbound Borders (What This Fiefdom Exports)

| To | Border Type | Data | Contract |
|----|-------------|------|----------|
| Code City | EXPORT | `HealthCheckResult` dict | Keyed by file path |
| Carl | EXPORT | Health status aggregation | FiefdomContext.health field |
| Maestro | EXPORT | Health state | Reactive state updates |

### Cross-Fiefdom Dependencies

```
┌─────────────────┐     health results      ┌─────────────────┐
│  Health Checker │ ───────────────────────>│   Code City     │
│  (this fiefdom) │                         │ (Building Anat.)│
└─────────────────┘                         └─────────────────┘
        │                                           │
        │ state update                              │ status display
        ▼                                           ▼
┌─────────────────┐                         ┌─────────────────┐
│ STATE_MANAGERS  │                         │    Maestro      │
│   (orchestr8)   │                         │     Plugin      │
└─────────────────┘                         └─────────────────┘
        │                                           │
        │ context query                             │ UI trigger
        ▼                                           ▼
┌─────────────────┐                         ┌─────────────────┐
│      Carl       │                         │  File Watcher   │
│ (Carl fiefdom)  │                         │  (this fiefdom) │
└─────────────────┘                         └─────────────────┘
```

---

## 5. Agent Estimates

### Universal Scaling Formula
```
effective_tokens = file_tokens × complexity_multiplier × responsibility_multiplier
agents = ceil(effective_tokens / 2500) × 3
```

### Wave 1: State Infrastructure

| File | Tokens | Complexity | Responsibility | Effective | Agents |
|------|--------|------------|----------------|-----------|--------|
| orchestr8.py | 150 | 1.2 (simple) | 1.5 (core) | 270 | 3 |

**Wave 1 Total: 3 agents**

### Wave 2: Health Watcher Bridge

| File | Tokens | Complexity | Responsibility | Effective | Agents |
|------|--------|------------|----------------|-----------|--------|
| health_watcher.py (new) | 500 | 1.5 (moderate) | 1.5 (core) | 1125 | 3 |

**Wave 2 Total: 3 agents**

### Wave 3: Woven Maps Integration

| File | Tokens | Complexity | Responsibility | Effective | Agents |
|------|--------|------------|----------------|-----------|--------|
| woven_maps.py | 300 | 1.3 (moderate) | 1.3 (viz) | 507 | 3 |

**Wave 3 Total: 3 agents**

### Wave 4: Maestro Plugin

| File | Tokens | Complexity | Responsibility | Effective | Agents |
|------|--------|------------|----------------|-----------|--------|
| 06_maestro.py | 200 | 1.2 (simple) | 1.3 (UI) | 312 | 3 |

**Wave 4 Total: 3 agents**

### Wave 5: File Watcher

| File | Tokens | Complexity | Responsibility | Effective | Agents |
|------|--------|------------|----------------|-----------|--------|
| health_watcher.py (ext) | 400 | 1.6 (async) | 1.5 (core) | 960 | 3 |

**Wave 5 Total: 3 agents**

### Total Agent Deployment

| Wave | Agents | Duration (est) | Dependencies |
|------|--------|----------------|--------------|
| Wave 1 | 3 | 30 min | None |
| Wave 2 | 3 | 45 min | Wave 1 |
| Wave 3 | 3 | 30 min | Wave 2 |
| Wave 4 | 3 | 30 min | Wave 3 |
| Wave 5 | 3 | 45 min | Wave 4 |
| **TOTAL** | **15** | **~3 hours** | Sequential |

### Sentinel Protocol Compliance
Each wave includes 1 primary + 2 sentinel agents (×3 multiplier applied).

---

## 6. Implementation Checklist

### Pre-Implementation
- [ ] Verify Marimo version supports reactive state in cells
- [ ] Confirm watchdog is in dependencies
- [ ] Review HealthChecker API stability

### Wave 1: State Infrastructure
- [ ] Add `health` and `health_status` to STATE_MANAGERS
- [ ] Export new state accessors in cell returns
- [ ] Test state isolation (changes don't break other plugins)

### Wave 2: Health Watcher Bridge
- [ ] Create `IP/health_watcher.py`
- [ ] Implement `HealthWatcher` class with debouncing
- [ ] Add Marimo cell for watcher lifecycle
- [ ] Test manual health check trigger

### Wave 3: Woven Maps Integration
- [ ] Add `health_results` parameter to `build_graph_data()`
- [ ] Implement `apply_health_results()` function
- [ ] Update `build_from_connection_graph()` similarly
- [ ] Test fallback when health_results is None

### Wave 4: Maestro Plugin
- [ ] Modify `build_code_city()` to read health state
- [ ] Add refresh trigger button/logic
- [ ] Test reactive updates when health changes
- [ ] Verify Combat Tracker integration still works

### Wave 5: File Watcher
- [ ] Implement `HealthWatchHandler` with watchdog
- [ ] Add observer lifecycle management
- [ ] Test real-time updates on file save
- [ ] Handle edge cases (deleted files, renames)

### Post-Implementation
- [ ] Verify LOCKED data flow works end-to-end
- [ ] Test with TypeScript project
- [ ] Test with Python project
- [ ] Verify three-state color system compliance
- [ ] Document API for Carl integration

---

## 7. Risk Mitigation

### Risk: File Watcher Overwhelm
**Scenario:** Large codebase with many rapid saves triggers too many health checks.
**Mitigation:** Debounce window of 300ms minimum, batch file changes.

### Risk: Health Check Timeout
**Scenario:** mypy/ruff hangs on complex files.
**Mitigation:** Existing 120-180s timeouts in HealthChecker, add progress indicator.

### Risk: State Race Condition
**Scenario:** Multiple plugins read/write health state simultaneously.
**Mitigation:** Marimo's reactive state is single-threaded per cell evaluation.

### Risk: Combat Status Override
**Scenario:** File is both broken AND in combat — which status wins?
**Mitigation:** Combat status takes priority (purple > teal), as per existing pattern in `build_from_connection_graph()`.

---

## 8. Success Criteria (from CONTEXT.md)

| Criterion | How This Plan Addresses |
|-----------|------------------------|
| Code City renders with buildings sized by formula | Unchanged, health doesn't affect sizing |
| Health updates flow from file watcher to visualization in real-time | Waves 2-5 implement full chain |
| Carl provides context to Summon panel | Health state available for Carl to read |
| Three-state color system works consistently | Uses canonical colors, no gradients |
| Things emerge — no breathing animations | No changes to emergence system |
| Clicking connections shows full signal path | Unchanged, orthogonal feature |
| Sitting Room enables collaboration | Unchanged, orthogonal feature |

---

**Document Status:** COMPLETE
**Ready for Implementation:** YES
**Founder Approval Required:** YES (per Integration Policy)

**Next Steps:**
1. Founder review and approval
2. Begin Wave 1 implementation
3. Update INTEGRATION_QUEUE.md with progress

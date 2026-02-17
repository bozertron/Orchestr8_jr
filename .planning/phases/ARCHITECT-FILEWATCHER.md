# ARCHITECT-FILEWATCHER.md
## Settlement Architect Plan: Real-Time File Watching
## Generated: 2026-02-12
## Status: READY FOR IMPLEMENTATION

---

## 1. Current State

### Existing Infrastructure (Marimo)
- **`FileWatcherManager`** at `marimo/_utils/file_watcher.py:161`
  - Manages multiple file watchers with callback sharing
  - Auto-selects: watchdog (preferred) → PollingFileWatcher (fallback)
  - Methods: `add_callback(path, callback)`, `remove_callback(path, callback)`, `stop_all()`

- **`SessionFileWatcherExtension`** at `marimo/_session/file_watcher_integration.py:29`
  - Session-scoped lifecycle management
  - Handles attach/detach/rename events

### Health Checker (IP/health_checker.py)
- `HealthChecker.check_fiefdom(path)` → `HealthCheckResult` (READY)
- `HealthChecker.check_all_fiefdoms(paths)` → `Dict[str, HealthCheckResult]` (READY)
- Already returns structured `ParsedError` with file/line/column/code/message

### Gap
- **NO bridge** between Marimo's FileWatcherManager and Orchestr8's HealthChecker
- **NO integration** with STATE_MANAGERS reactive system

---

## 2. Approach

Create a new `IP/health_watcher.py` that:
1. Wraps Marimo's `FileWatcherManager` for directory watching
2. Implements debouncing (300ms) to batch rapid file changes
3. Calls `HealthChecker.check_fiefdom()` on change
4. Updates `STATE_MANAGERS["health"]` reactively

---

## 3. Where to Instantiate Watcher

### Primary Location: `orchestr8.py` (entry point)

```python
# orchestr8.py - at module level with other state setup
from IP.health_watcher import HealthWatcherManager

# After STATE_MANAGERS initialization
HEALTH_WATCHER = HealthWatcherManager(
    project_root=PROJECT_ROOT,
    state_managers=STATE_MANAGERS,
    watch_paths=["IP/"]  # Configurable fiefdoms
)
```

### Alternative: Lazy init in `06_maestro.py` plugin
- Only start watcher when Code City tab is active
- Trade-off: Slight delay on first view vs. lower idle resource use

**Recommendation:** Primary location (orchestr8.py) for immediate real-time behavior.

---

## 4. Callback Chain Design

```
FILE CHANGE EVENT
       ↓
┌─────────────────────────────────┐
│  HealthWatcherManager           │
│  (IP/health_watcher.py)         │
├─────────────────────────────────┤
│ 1. Debounce (300ms batch)       │
│ 2. Map path → fiefdom           │
│ 3. Call HealthChecker           │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│  HealthChecker                  │
│  (IP/health_checker.py:426)     │
├─────────────────────────────────┤
│ check_fiefdom(fiefdom_path)     │
│ → HealthCheckResult             │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│  STATE_MANAGERS["health"]       │
│  (reactive dict)                │
├─────────────────────────────────┤
│ .set({                          │
│   "IP/": {"status": "broken",   │
│           "errors": [...]},     │
│   ...                           │
│ })                              │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│  Code City (woven_maps.py)      │
├─────────────────────────────────┤
│ Building color update:          │
│   working → gold (#D4AF37)      │
│   broken → teal (#1fbdea)       │
└─────────────────────────────────┘
```

### Key Implementation Details

**Debounce Logic:**
```python
import asyncio
from collections import defaultdict

class HealthWatcherManager:
    DEBOUNCE_MS = 300
    
    def __init__(self, project_root, state_managers, watch_paths):
        self._pending = defaultdict(set)  # fiefdom -> set of changed files
        self._debounce_task = None
        self._health_checker = HealthChecker(project_root)
        self._state = state_managers["health"]
        
    async def _on_file_change(self, path: Path):
        fiefdom = self._map_to_fiefdom(path)
        self._pending[fiefdom].add(path)
        
        if self._debounce_task:
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._debounced_check())
    
    async def _debounced_check(self):
        await asyncio.sleep(self.DEBOUNCE_MS / 1000)
        # Batch check all pending fiefdoms
        for fiefdom in self._pending:
            result = self._health_checker.check_fiefdom(fiefdom)
            self._state.set(fiefdom, result)
        self._pending.clear()
```

**Fiefdom Mapping:**
```python
def _map_to_fiefdom(self, path: Path) -> str:
    # Map file path to its parent fiefdom
    # e.g., "IP/plugins/06_maestro.py" → "IP/"
    parts = path.parts
    if parts[0] == "IP":
        return "IP/"
    return str(path.parent) + "/"
```

---

## 5. Agent Estimates

Using Universal Scaling Formula:
`agents = ceil(effective_tokens / 2500) × 3`

| Component | Est. Tokens | Complexity | Agents |
|-----------|-------------|------------|--------|
| `health_watcher.py` (new) | ~800 | 1.5 (async, debouncing) | 2 |
| `orchestr8.py` integration | ~100 | 1.0 (simple init) | 1 |
| STATE_MANAGERS wiring | ~200 | 1.0 | 1 |
| Testing | ~400 | 1.2 | 2 |
| **TOTAL** | | | **6 agents** |

**Deployment:** Single tier (Tier 4: Wiring)
- 2 primary agents (implementation)
- 4 sentinel agents (testing, review, integration verification)

---

## 6. Dependencies

```toml
# Already in Marimo's dependencies
watchdog = ">=3.0.0"

# Verify in orchestr8
pip install watchdog  # if not present
```

---

## 7. Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `IP/health_watcher.py` | CREATE | HealthWatcherManager class |
| `orchestr8.py` | MODIFY | Instantiate HealthWatcherManager |
| `IP/plugins/06_maestro.py` | MODIFY | Subscribe to STATE_MANAGERS["health"] |

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| High CPU during bulk changes | Debounce + batch processing |
| Watchdog not installed | Fallback to PollingFileWatcher (built into Marimo) |
| Large codebases slow checks | Only check changed fiefdom, not entire project |

---

**Document Status:** READY
**Next Step:** Implement `IP/health_watcher.py`
**Blocked By:** None

# Integration Roadmap: health_watcher.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/health_watcher.py`  
**Target:** `/home/bozertron/a_codex_plan`  
**Pattern:** DENSE + GAP  
**Date:** 2026-02-16

---

## 1. Public API Surface

### 1.1 Classes

| Symbol | Type | Description |
|--------|------|-------------|
| `HealthWatcher` | `class` | Simple watchdog-based file watcher with callback on file changes |
| `HealthWatcherManager` | `class` | Marimo-integrated watcher with reactive state updates via state_managers |

### 1.2 Public Methods - HealthWatcher

| Method | Signature | Description |
|--------|-----------|-------------|
| `HealthWatcher.__init__` | `(project_root: str, callback: Callable[[Dict[str, Any]], None])` | Initialize with project root and callback |
| `HealthWatcher.start_watching` | `() -> None` | Start watching the project for file changes |
| `HealthWatcher.stop_watching` | `() -> None` | Stop watching for file changes |

### 1.3 Public Methods - HealthWatcherManager

| Method | Signature | Description |
|--------|-----------|-------------|
| `HealthWatcherManager.__init__` | `(project_root: Path, state_managers: Dict[str, Any], watch_paths: List[str] = None)` | Initialize with project root and state managers |
| `HealthWatcherManager.start` | `() -> None` | Start watching files using Marimo's FileWatcherManager |
| `HealthWatcherManager.stop` | `() -> None` | Stop watching files and cleanup resources |

### 1.4 Constants

| Symbol | Type | Value | Description |
|--------|------|-------|-------------|
| `HealthWatcher.DEBOUNCE_MS` | `int` | `100` | Debounce period in milliseconds |
| `HealthWatcherManager.DEBOUNCE_MS` | `int` | `300` | Debounce period in milliseconds |
| `HAS_WATCHDOG` | `bool` | `True/False` | Whether watchdog library is installed |

---

## 2. Dependencies

### 2.1 Standard Library

| Module | Usage |
|--------|-------|
| `asyncio` | Async event handling in HealthWatcherManager |
| `threading` | Timer-based debouncing in HealthWatcher |
| `collections.defaultdict` | Pending file changes grouped by fiefdom |
| `pathlib` | File path manipulation |

### 2.2 Typing Imports

| Symbol | Type |
|--------|------|
| `Callable`, `Dict`, `Any`, `Optional`, `List` | Generic type hints |

### 2.3 External Dependencies

| Package | Purpose | Detection |
|---------|---------|-----------|
| `watchdog` | File system event monitoring | Try/except import with `HAS_WATCHDOG` flag |
| `marimo._utils.file_watcher.FileWatcherManager` | Marimo's reactive file watcher | Try/except import in HealthWatcherManager.start() |

### 2.4 Internal Dependencies

| Module | Import | Usage |
|--------|--------|-------|
| `IP.health_checker` | `from IP.health_checker import HealthChecker, HealthCheckResult` | Run health checks on file changes |

---

## 3. Integration Points

### 3.1 Current Consumers

| File | Import | Usage |
|------|--------|-------|
| `IP/plugins/06_maestro.py:79` | `from IP.health_watcher import HealthWatcher` | Instantiate and start watching on Code City render |
| `IP/plugins/06_maestro.py:237` | `HealthWatcher(str(project_root_path), on_health_change)` | Create watcher with health change callback |
| `IP/features/code_city/tests/test_health_flow.py:9` | `from IP.health_watcher import HealthWatcher` | Unit tests |

### 3.2 Data Flow

```
User Edits File
       ↓
FileSystemEvent (watchdog)
       ↓
_on_file_change() - filters by extension (.py, .ts, .tsx, .js, .jsx)
       ↓
Debounce Timer (100ms HealthWatcher / 300ms HealthWatcherManager)
       ↓
_health_checker.check_fiefdom(fiefdom_path)
       ↓
HealthCheckResult (status: "working" | "broken")
       ↓
Callback (HealthWatcher) OR state_managers["health"] (HealthWatcherManager)
       ↓
Code City Status Update (Blue = broken, Gold = working)
```

### 3.3 STATE_MANAGERS Integration

In `06_maestro.py`, health state is accessed via:

```python
get_health, set_health = STATE_MANAGERS["health"]
```

The `HealthWatcherManager` expects `state_managers` dict with:

```python
state_managers = {
    "health": (get_health_fn, set_health_fn),  # Tuple of getter/setter
}
```

---

## 4. DENSE + GAP Analysis

### GAP 1: Type Contracts

**Current State:** No explicit TypedDict for WatchEvent or FileStatus. Uses implicit types via typing module. The callback receives `Dict[str, Any]` which lacks schema enforcement.

**Required Contracts for a_codex_plan:**

```python
from typing import Literal, TypedDict, NotRequired
from pathlib import Path

# GAP 1a: WatchEvent - Represents a file change event
class WatchEvent(TypedDict):
    """Represents a file change event from the watcher."""
    path: str                          # Full path to the changed file
    relative_path: str                 # Path relative to project root
    fiefdom: str                       # Parent fiefdom identifier
    suffix: str                        # File extension (e.g., ".py")
    timestamp: str                     # ISO timestamp of event

# GAP 1b: FileStatus - Represents current file watching status
class FileStatus(TypedDict):
    """Represents the status of file watching for a fiefdom."""
    fiefdom: str
    is_watching: bool
    debounce_ms: int
    pending_files: NotRequired[List[str]]
    last_check: NotRequired[str]
    watcher_type: Literal["watchdog", "marimo_filewatcher", "polling"]

# GAP 1c: WatcherConfig - Configuration for HealthWatcher
class WatcherConfig(TypedDict):
    """Configuration for HealthWatcher initialization."""
    project_root: str
    watch_paths: NotRequired[List[str]]
    debounce_ms: NotRequired[int]
    callback: NotRequired[Callable[[Dict[str, Any]], None]]
    state_managers: NotRequired[Dict[str, Any]]
```

### GAP 2: State Boundary

**Current State:** `HealthWatcherManager` stores state in multiple instance variables:
- `_pending: Dict[str, set]` - Pending file changes grouped by fiefdom
- `_debounce_task` - Debounce task reference
- `_file_watcher` - File watcher reference
- `_health_checker` - Health checker instance

No explicit `_component_state` dict exists for cross-component state transfer.

**Required State Boundary for a_codex_plan:**

```python
class HealthWatcherManager:
    def __init__(
        self,
        project_root: Path,
        state_managers: Dict[str, Any],
        watch_paths: List[str] = None,
    ):
        self.project_root = Path(project_root)
        self._state_managers = state_managers
        self._watch_paths = watch_paths or ["IP/"]
        
        # GAP 2: Explicit component state dict
        self._component_state: Dict[str, Any] = {
            "_component_name": "health_watcher_manager",
            "_component_version": "1.0.0",
            "_component_dependencies": ["watchdog", "asyncio", "IP.health_checker"],
            "project_root": str(project_root),
            "watch_paths": self._watch_paths,
            "is_watching": False,
            "watcher_type": "unknown",  # "watchdog", "marimo_filewatcher", "polling"
            "pending_fiefdoms": [],
            "last_health_update": None,
        }
        
        # Existing state
        self._pending: Dict[str, set] = defaultdict(set)
        self._debounce_task = None
        self._health_checker = HealthChecker(str(self.project_root))
        self._file_watcher = None
        
    def get_component_state(self) -> Dict[str, Any]:
        """Export component state for cross-component transport."""
        return {
            **self._component_state,
            "pending_fiefdoms": list(self._pending.keys()),
            "has_pending_task": self._debounce_task is not None,
        }
    
    def set_component_state(self, state: Dict[str, Any]) -> None:
        """Restore component state from serialized dict."""
        # Only restore non-volatile state
        if "watch_paths" in state:
            self._watch_paths = state["watch_paths"]
        self._component_state.update({k: v for k, v in state.items() 
                                       if k in self._component_state})
```

**Similarly for HealthWatcher:**

```python
class HealthWatcher:
    def __init__(self, project_root: str, callback: Callable[[Dict[str, Any]], None]):
        self.project_root = Path(project_root)
        self.callback = callback
        self.health_checker = HealthChecker(str(self.project_root))
        
        # GAP 2: Explicit component state dict
        self._component_state: Dict[str, Any] = {
            "_component_name": "health_watcher",
            "_component_version": "1.0.0",
            "_component_dependencies": ["watchdog", "threading", "IP.health_checker"],
            "project_root": str(project_root),
            "debounce_ms": self.DEBOUNCE_MS,
            "is_watching": False,
            "watcher_type": "watchdog",
            "last_file": None,
            "last_check_time": None,
        }
        
        # Existing state
        self._observer: Optional[Observer] = None
        self._debounce_timer: Optional[threading.Timer] = None
        self._pending_file: Optional[str] = None
        self._lock = threading.Lock()
```

### GAP 3: Bridge Definitions

**Current State:** No explicit JS<->Python bridge protocol. The HealthWatcher uses callbacks, while HealthWatcherManager uses state_managers. No protocol for frontend file watching status.

**Required Bridge for a_codex_plan:**

```python
# GAP 3a: Bridge protocol for HealthWatcher JS<->Python communication
class HealthWatcherBridge:
    """
    Bridge protocol for HealthWatcher JS<->Python communication.
    Defines the contract between orchestr8 frontend and health_watcher backend.
    """
    
    # Method signatures exposed to JavaScript
    @staticmethod
    def start_watching(
        project_root: str,
        watch_paths: Optional[List[str]] = None,
        state_managers: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Start watching files for changes."""
        root = Path(project_root)
        
        if state_managers:
            manager = HealthWatcherManager(root, state_managers, watch_paths)
        else:
            # Use simple callback-based watcher
            def callback(results):
                pass  # Log or store results
            manager = HealthWatcher(project_root, callback)
        
        manager.start_watching()
        
        return {
            "success": True,
            "project_root": str(root),
            "watch_paths": watch_paths or ["IP/"],
            "watcher_type": "watchdog" if not state_managers else "manager",
        }
    
    @staticmethod
    def stop_watching(watcher_instance) -> Dict[str, Any]:
        """Stop watching files."""
        try:
            watcher_instance.stop_watching()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_status(watcher_instance) -> FileStatus:
        """Get current file watching status."""
        state = watcher_instance.get_component_state() if hasattr(watcher_instance, 'get_component_state') else {}
        
        return FileStatus(
            fiefdom=state.get("project_root", ""),
            is_watching=state.get("is_watching", False),
            debounce_ms=state.get("debounce_ms", 100),
            watcher_type=state.get("watcher_type", "unknown"),
        )

# GAP 3b: Event bridge for real-time file change notifications
FILE_WATCH_EVENTS = {
    "watcher:start": {"project_root": str, "watch_paths": List[str]},
    "watcher:stop": {"project_root": str},
    "file:change": WatchEvent,  # Defined in GAP 1
    "file:pending": {"fiefdom": str, "files": List[str]},
    "file:checked": {"fiefdom": str, "status": str, "error_count": int},
}

# GAP 3c: Protocol for file extension filtering
WATCHED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}

def is_watched_file(path: Path) -> bool:
    """Check if file extension is in the watched set."""
    return path.suffix.lower() in WATCHED_EXTENSIONS
```

### GAP 4: Integration Logic

**Current State:** Direct instantiation by consumers (06_maestro.py). No factory functions or validation. HealthWatcherManager expects specific state_managers structure.

**Required Integration Points for a_codex_plan:**

```python
# GAP 4a: Factory function for creating HealthWatcher with validation
def create_health_watcher(
    project_root: str,
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    validate: bool = True
) -> HealthWatcher:
    """
    Factory function for creating HealthWatcher with validation.
    
    Args:
        project_root: Path to project root
        callback: Callback function for health check results
        validate: If True, verify project root exists
        
    Returns:
        HealthWatcher instance
        
    Raises:
        ValueError: If project_root is invalid
        FileNotFoundError: If project root does not exist
    """
    root_path = Path(project_root)
    
    if validate:
        if not root_path.exists():
            raise FileNotFoundError(f"Project root not found: {project_root}")
        if not root_path.is_dir():
            raise ValueError(f"Project root is not a directory: {project_root}")
    
    if callback is None:
        # Default no-op callback
        callback = lambda r: None
    
    return HealthWatcher(str(root_path), callback)


# GAP 4b: Factory function for HealthWatcherManager with state_managers validation
def create_health_watcher_manager(
    project_root: str,
    state_managers: Dict[str, Any],
    watch_paths: Optional[List[str]] = None,
    validate: bool = True
) -> HealthWatcherManager:
    """
    Factory function for creating HealthWatcherManager with validation.
    
    Args:
        project_root: Path to project root
        state_managers: Dict with "health" state getter/setter
        watch_paths: List of paths to watch (default: ["IP/"])
        validate: If True, verify inputs
        
    Returns:
        HealthWatcherManager instance
        
    Raises:
        ValueError: If state_managers is invalid
        FileNotFoundError: If project root does not exist
    """
    root_path = Path(project_root)
    
    if validate:
        if not root_path.exists():
            raise FileNotFoundError(f"Project root not found: {project_root}")
        
        # Validate state_managers structure
        if "health" not in state_managers:
            raise ValueError("state_managers must contain 'health' key")
        
        health_getters = state_managers["health"]
        if not isinstance(health_getters, (tuple, list)) or len(health_getters) != 2:
            raise ValueError("state_managers['health'] must be a (getter, setter) tuple")
    
    return HealthWatcherManager(root_path, state_managers, watch_paths)


# GAP 4c: Validation middleware for bridge calls
def validate_watcher_input(
    project_root: str,
    watch_paths: Optional[List[str]] = None
) -> Tuple[str, List[str]]:
    """
    Validate inputs for health watcher bridge calls.
    
    Returns:
        Tuple of (validated_project_root, validated_watch_paths)
        
    Raises:
        ValidationError: If inputs are invalid
    """
    errors = []
    
    if not project_root:
        errors.append("project_root is required")
    
    root_path = Path(project_root)
    if project_root and not root_path.exists():
        errors.append(f"Project root does not exist: {project_root}")
    
    validated_paths = watch_paths or ["IP/"]
    for path in validated_paths:
        if ".." in path or path.startswith("/"):
            errors.append(f"Invalid watch path: {path}")
    
    if errors:
        raise ValidationError(f"Health watcher validation failed: {', '.join(errors)}")
    
    return str(root_path.resolve()), validated_paths


# GAP 4d: Integration with 06_maestro.py state_managers pattern
def get_or_create_health_watcher(
    STATE_MANAGERS: Dict[str, Any],
    project_root: Path
) -> HealthWatcher:
    """
    Get existing or create new HealthWatcher for 06_maestro.py integration.
    
    This follows the pattern used in 06_maestro.py where watchers are
    created once and stored in closure scope.
    
    Args:
        STATE_MANAGERS: Marimo state managers dict
        project_root: Path to project root
        
    Returns:
        HealthWatcher instance
    """
    # Check if we have state_managers (Marimo context)
    if "health" in STATE_MANAGERS:
        get_health, set_health = STATE_MANAGERS["health"]
        
        def on_health_change(results: dict) -> None:
            """Callback when health check completes - merges into health state."""
            current = get_health() or {}
            current.update(results)
            set_health(current)
        
        return HealthWatcher(str(project_root), on_health_change)
    else:
        # Fallback to simple watcher without state integration
        return HealthWatcher(str(project_root), lambda r: None)
```

---

## 5. Integration Checklist for a_codex_plan

### 5.1 Pre-Integration (GAP 1-2)

- [ ] Add `typing_extensions` or Python 3.8+ for `TypedDict`, `NotRequired`
- [ ] Define `WatchEvent`, `FileStatus`, `WatcherConfig` TypedDicts
- [ ] Add `_component_state` dict to `HealthWatcher.__init__`
- [ ] Add `_component_state` dict to `HealthWatcherManager.__init__`
- [ ] Implement `get_component_state()` and `set_component_state()` methods for both classes
- [ ] Add `_component_version` tracking for state migration

### 5.2 Bridge Layer (GAP 3)

- [ ] Create `HealthWatcherBridge` class with static methods
- [ ] Define `FILE_WATCH_EVENTS` event schema
- [ ] Define `WATCHED_EXTENSIONS` constant set
- [ ] Implement `is_watched_file()` helper function
- [ ] Register bridge handlers in a_codex_plan plugin system

### 5.3 Entry Points (GAP 4)

- [ ] Implement `create_health_watcher()` factory function
- [ ] Implement `create_health_watcher_manager()` factory function
- [ ] Implement `validate_watcher_input()` validation middleware
- [ ] Implement `get_or_create_health_watcher()` for 06_maestro.py pattern
- [ ] Add error handling for watchdog import failures

### 5.4 Testing

- [ ] Unit test type contract enforcement
- [ ] Unit test state boundary serialization/deserialization
- [ ] Integration test with actual file system events
- [ ] End-to-end test via a_codex_plan UI (start/stop watcher)

### 5.5 Documentation

- [ ] Document the difference between HealthWatcher (callback-based) and HealthWatcherManager (state-based)
- [ ] Document debounce timing differences (100ms vs 300ms)
- [ ] Document file extension filtering behavior

---

## 6. File Location Summary

| Artifact | Path |
|----------|------|
| Source | `/home/bozertron/Orchestr8_jr/IP/health_watcher.py` |
| Target | `/home/bozertron/a_codex_plan` |
| This Roadmap | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/roadmaps/INTEGRATION_health_watcher.md` |

---

## 7. References

- **Current Consumers:** `IP/plugins/06_maestro.py`
- **Dependencies:** `IP/health_checker.py` (HealthChecker), `watchdog` package, `marimo._utils.file_watcher`
- **Data Flow:** File change → debounce → HealthChecker → HealthCheckResult → Code City
- **Color Contract:** "broken" status maps to Blue (#1fbdea), "working" maps to Gold (#D4AF37)
- **Related Files:** `IP/health_checker.py` (health checking), `IP/plugins/06_maestro.py` (integration point)
- **Watched Extensions:** `.py`, `.ts`, `.tsx`, `.js`, `.jsx`

---

## 8. Key Differences from health_checker.py

| Aspect | health_checker.py | health_watcher.py |
|-------|-------------------|-------------------|
| Primary Role | Static analysis runner | Real-time file change detection |
| Trigger | Manual or periodic | File system events |
| Debounce | N/A | 100ms (Watcher) / 300ms (Manager) |
| State Pattern | HealthCheckResult dataclass | _component_state dict |
| Bridge Type | HealthCheckerBridge | HealthWatcherBridge |
| Integration | Called by health_watcher | Called by 06_maestro.py |

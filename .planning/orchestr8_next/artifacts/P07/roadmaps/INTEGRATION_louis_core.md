# Integration Roadmap: louis_core.py

**Target:** `a_codex_plan`  
**Source:** `/home/bozertron/Orchestr8_jr/IP/louis_core.py`  
**Version:** Orchestr8 v3.0  
**Date:** 2026-02-16

---

## Executive Summary

This roadmap defines the integration strategy for `louis_core.py` into the `a_codex_plan` system. The module provides file protection capabilities through the LouisWarden and LouisConfig classes, enabling lock/unlock operations on project files with git hook integration. The DENSE + GAP pattern establishes four critical integration layers: type contracts, state boundaries, bridge definitions, and integration logic.

The file protection system operates at the filesystem level using POSIX permissions (0o444 for locked, 0o644 for unlocked) and maintains protection state in `~/.louis-control/`. Current integration points exist in `03_gatekeeper.py`, `carl_core.py`, and `graph_builder.py` where LouisWarden provides protection status for Code City visualization.

---

## GAP 1: Type Contracts

### Required TypedDict Definitions

The current implementation uses implicit dictionary structures that must be formalized for the a_codex_plan integration. The following TypedDict definitions establish explicit type contracts:

```python
from typing import TypedDict, Literal, NotRequired

class LouisConfigData(TypedDict):
    """Configuration structure for Louis file protection system."""
    project_root: str
    protected_folders: list[str]

class ProtectionStatus(TypedDict):
    """Individual file protection status."""
    locked: bool
    protected: bool

class ProtectionStatusMap(TypedDict):
    """Complete protection status mapping for all tracked files."""
    path: ProtectionStatus

class LockResult(TypedDict):
    """Result of a lock/unlock operation."""
    success: bool
    message: str

class GitHookResult(TypedDict):
    """Result of git hook installation."""
    success: bool
    message: str

class ScanResult(TypedDict):
    """Result of scanning and protecting files."""
    file_count: int
    files: list[str]
```

### Literal Type Definitions

```python
from typing import Literal

FilePermission = Literal["locked", "unlocked"]
PermissionMode = Literal[0o444, 0o644]

LOUIS_PERMISSIONS: dict[FilePermission, PermissionMode] = {
    "locked": 0o444,
    "unlocked": 0o644,
}
```

### Dataclass Contracts for Carl Core Integration

The `FiefdomContext.locks` field expects `List[Dict[str, str]]`, which should be formalized:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class LockRecord:
    """Single file lock record for fiefdom context."""
    file: str
    reason: str
```

---

## GAP 2: State Boundary

### Component State Structure

The current implementation maintains state through file-based storage (`~/.louis-control/`) rather than in-memory state management. For a_codex_plan integration, an explicit state boundary layer is required:

```python
# Louis Component State (in-memory)
_component_state: dict = {
    "_config": None,           # LouisConfig instance
    "_warden": None,           # LouisWarden instance  
    "_project_root": "",       # Current project root path
    "_protection_status": {},  # Cached protection status
    "_selected_files": set(),  # UI selected files for bulk operations
    "_refresh_trigger": 0,    # UI refresh counter
}
```

### State Initialization Pattern

```python
def _init_louis_state(root_path: str) -> None:
    """Initialize Louis component state with validation."""
    if not root_path or not Path(root_path).exists():
        raise ValueError(f"Invalid project root: {root_path}")
    
    _component_state["_project_root"] = root_path
    _component_state["_config"] = LouisConfig(root_path)
    _component_state["_warden"] = LouisWarden(_component_state["_config"])
    _component_state["_protection_status"] = _component_state["_warden"].get_protection_status()
```

### State Accessors

```python
def get_louis_config() -> LouisConfig:
    """Get current LouisConfig instance."""
    if _component_state["_config"] is None:
        raise RuntimeError("Louis state not initialized. Call _init_louis_state first.")
    return _component_state["_config"]

def get_louis_warden() -> LouisWarden:
    """Get current LouisWarden instance."""
    if _component_state["_warden"] is None:
        raise RuntimeError("Louis state not initialized. Call _init_louis_state first.")
    return _component_state["_warden"]

def get_protection_status() -> ProtectionStatusMap:
    """Get cached protection status."""
    return _component_state["_protection_status"]

def refresh_protection_status() -> ProtectionStatusMap:
    """Force refresh of protection status from filesystem."""
    warden = get_louis_warden()
    _component_state["_protection_status"] = warden.get_protection_status()
    return _component_state["_protection_status"]
```

---

## GAP 3: Bridge Definitions

### Python-to-Python Bridge (Internal Integration)

For integration with Carl Core and graph_builder.py:

```python
# Bridge Protocol for Carl Core Integration
class LouisBridgeProtocol:
    """Protocol for Louis file protection bridge operations."""
    
    def get_locks_for_fiefdom(self, fiefdom_path: str) -> list[LockRecord]:
        """
        Get all locks within a specific fiefdom.
        
        Args:
            fiefdom_path: Relative path to fiefdom (e.g., "IP/")
            
        Returns:
            List of LockRecord for files in the fiefdom that are locked
        """
        ...
    
    def is_file_locked(self, rel_path: str) -> bool:
        """Check if a specific file is locked."""
        ...
    
    def get_lock_summary(self) -> dict[str, int]:
        """Get summary statistics of protection status."""
        ...
```

### JS-to-Python Bridge (Future Web UI)

If a_codex_plan requires web-based file protection controls:

```python
# Bridge entry point for web-based Louis UI
def louis_bridge(operation: str, payload: dict) -> dict:
    """
    Main bridge handler for Louis operations.
    
    Operations:
        - status: Get full protection status
        - lock: Lock specific file(s)
        - unlock: Unlock specific file(s)
        - scan: Rescan protected folders
        - add_folder: Add folder to protection list
        - remove_folder: Remove folder from protection list
        - install_hook: Install git pre-commit hook
    """
    warden = get_louis_warden()
    config = get_louis_config()
    
    if operation == "status":
        return {
            "status": warden.get_protection_status(),
            "protected_folders": config.protected_folders,
            "summary": _compute_summary(warden.get_protection_status()),
        }
    
    elif operation == "lock":
        rel_path = payload.get("path")
        success, msg = warden.lock_file(rel_path)
        return {"success": success, "message": msg}
    
    # ... additional operations
```

---

## GAP 4: Integration Logic

### Entry Points with Validation

```python
from typing import Callable, Any

def validate_root_path(root: Any) -> str:
    """Validate and normalize project root path."""
    if root is None:
        raise ValueError("Project root cannot be None")
    
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(f"Project root does not exist: {root}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Project root is not a directory: {root}")
    
    return str(root_path.resolve())

def validate_file_path(rel_path: str) -> str:
    """Validate relative file path."""
    if not rel_path:
        raise ValueError("File path cannot be empty")
    if ".." in rel_path:
        raise ValueError("File path cannot contain '..'")
    return rel_path.strip("/")

# Decorator for validated operations
def with_louis_initialized(func: Callable) -> Callable:
    """Decorator to ensure Louis state is initialized before operation."""
    def wrapper(*args, **kwargs):
        if _component_state["_warden"] is None:
            raise RuntimeError(
                "Louis not initialized. "
                "Call louis_init(project_root) before operations."
            )
        return func(*args, **kwargs)
    return wrapper
```

### Integration with Gatekeeper Plugin

The 03_gatekeeper.py plugin integration pattern:

```python
def gatekeeper_louis_integration(root_path: str) -> dict[str, Any]:
    """
    Integration logic for Gatekeeper plugin.
    
    Returns:
        Dictionary with all UI state needed for Gatekeeper rendering
    """
    # Initialize with validation
    validated_root = validate_root_path(root_path)
    _init_louis_state(validated_root)
    
    warden = get_louis_warden()
    config = get_louis_config()
    
    # Get current state
    protection_status = refresh_protection_status()
    total_protected = len(protection_status)
    locked_count = sum(1 for s in protection_status.values() if s.get("locked"))
    
    return {
        "config": config,
        "warden": warden,
        "protection_status": protection_status,
        "summary": {
            "total": total_protected,
            "locked": locked_count,
            "unlocked": total_protected - locked_count,
        },
        "protected_folders": config.protected_folders,
    }
```

### Integration with Carl Core

The Carl Core integration for fiefdom context gathering:

```python
def get_louis_locks_for_fiefdom(fiefdom_path: str) -> list[LockRecord]:
    """
    Get lock information for a specific fiefdom.
    
    Used by CarlContextualizer.gather_context() to populate
    the FiefdomContext.locks field.
    """
    if _component_state["_warden"] is None:
        return []
    
    protection = _component_state["_warden"].get_protection_status()
    locks = []
    
    for path, status in protection.items():
        if fiefdom_path in path and status.get("locked"):
            locks.append(LockRecord(file=path, reason="Louis protection"))
    
    return locks
```

### Integration with Code City Graph Builder

For Code City visualization showing locked files:

```python
def get_locked_files_for_graph() -> dict[str, bool]:
    """
    Get locked status for all files in protection list.
    
    Used by graph_builder.py to set CodeNode.is_locked flag.
    """
    if _component_state["_warden"] is None:
        return {}
    
    protection = _component_state["_warden"].get_protection_status()
    return {path: status.get("locked", False) for path, status in protection.items()}
```

---

## Public API Reference

### Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `LouisConfig` | Configuration management for Louis protection system | `__init__`, `save`, `log` |
| `LouisWarden` | File protection operations (lock/unlock/scan) | `scan_and_protect`, `is_locked`, `get_protection_status`, `lock_file`, `unlock_file`, `install_git_hook` |

### Public Functions

| Function | Signature | Purpose |
|----------|-----------|---------|
| `validate_root_path` | `(root: Any) -> str` | Validate and normalize project root |
| `validate_file_path` | `(rel_path: str) -> str` | Validate relative file path |
| `_init_louis_state` | `(root_path: str) -> None` | Initialize component state |
| `get_louis_config` | `() -> LouisConfig` | Get current config instance |
| `get_louis_warden` | `() -> LouisWarden` | Get current warden instance |
| `get_protection_status` | `() -> ProtectionStatusMap` | Get cached protection status |
| `refresh_protection_status` | `() -> ProtectionStatusMap` | Force refresh from filesystem |
| `get_louis_locks_for_fiefdom` | `(fiefdom_path: str) -> list[LockRecord]` | Get locks for fiefdom context |

---

## Dependencies

### External Dependencies

The module imports from standard library only:

```python
import os              # File operations, chmod
import stat            # POSIX permission constants
import json            # Configuration serialization
from pathlib import Path  # Path manipulation
from datetime import datetime  # Timestamps for logging
from typing import import List, Tuple  # Type hints
```

### Internal Dependencies

| Module | Import Location | Purpose |
|--------|-----------------|---------|
| None | - | louis_core has no internal dependencies |

### Consumer Dependencies

The following modules depend on louis_core:

| Module | Import Statement | Usage |
|--------|------------------|-------|
| `IP.plugins.03_gatekeeper` | `from IP.louis_core import LouisWarden, LouisConfig` | Full UI integration |
| `IP.carl_core` | `from .louis_core import LouisWarden, LouisConfig` | Lock status in FiefdomContext |
| `IP.features.code_city.graph_builder` | `from IP.louis_core import LouisConfig, LouisWarden` | CodeNode.is_locked flag |

---

## Integration Points

### 1. Gatekeeper Plugin (03_gatekeeper.py)

**Integration Type:** Direct import and instantiation  
**Pattern:** Creates LouisConfig and LouisWarden instances per render call  
**State Management:** Local mo.state() for UI, file-based for persistence

Current usage:
```python
from IP.louis_core import LouisWarden, LouisConfig

def render(STATE_MANAGERS: dict) -> Any:
    config = LouisConfig(root)
    warden = LouisWarden(config)
    protection_status = warden.get_protection_status()
```

### 2. Carl Core (carl_core.py)

**Integration Type:** Conditional import in __init__ with graceful fallback  
**Pattern:** Optional Louis integration for fiefdom context  
**State Management:** Per-instance with try/except wrapper

Current usage:
```python
try:
    louis_config = LouisConfig(str(self.root))
    self.louis_warden = LouisWarden(louis_config)
except Exception:
    self.louis_warden = None

# Later in gather_context():
if self.louis_warden:
    protection = self.louis_warden.get_protection_status()
    # Filter by fiefdom_path
```

### 3. Graph Builder (graph_builder.py)

**Integration Type:** Try/except import with conditional application  
**Pattern:** Sets CodeNode.is_locked during node creation  
**State Management:** Transient per-graph-build

Current usage:
```python
try:
    from IP.louis_core import LouisConfig, LouisWarden
    config = LouisConfig(root_path=root)
    if config.protected_list and config.protected_list.exists():
        warden = LouisWarden(config)
        for node in nodes:
            node.is_locked = warden.is_locked(node.path)
except ImportError:
    pass
```

---

## State Management Approach

### Current Architecture

The module uses a **file-based state** approach:

1. **Configuration Storage:** `~/.louis-control/louis-config.json`
   - Stores project_root and protected_folders list
   - Loaded on LouisConfig instantiation
   
2. **Protection List:** `~/.louis-control/protected-files.txt`
   - One relative path per line
   - Generated by scan_and_protect()
   
3. **Audit Log:** `~/.louis-control/lock-history.log`
   - Append-only timestamped operations

4. **Actual State:** POSIX file permissions (0o444 = locked, 0o644 = unlocked)

### Recommended Approach for a_codex_plan

Implement a **dual-layer state** approach:

1. **Persistent Layer (Unchanged):** File-based configuration in ~/.louis-control/
2. **Transient Layer (New):** In-memory cache via _component_state dict

This provides:
- Fast access to protection status without filesystem I/O
- UI refresh capability via _refresh_trigger
- Selected files tracking for bulk operations
- Integration point for validation and error handling

### State Transitions

```
+-------------------------------------------------------------+
|                    Louis State Machine                       |
+-------------------------------------------------------------+
|                                                              |
|   [Uninitialized]                                           |
|        |                                                    |
|        | _init_louis_state(root_path)                      |
|        v                                                    |
|   [Ready] ------------------------------------------------  |
|        |                                                    |
|        +- scan_and_protect() ----> [Files Scanned]          |
|        |                                                    |
|        +- lock_file() -----------> [File Locked]            |
|        |                              |                      |
|        |                              v                      |
|        |              refresh_protection_status()           |
|        |                              |                      |
|        +- unlock_file() -----------> [File Unlocked]        |
|        |                              |                      |
|        |                              v                      |
|        |              refresh_protection_status()           |
|        |                                                    |
|        +- refresh_protection_status() ---> [Status Cached]  |
|                                                              |
+-------------------------------------------------------------+
```

---

## Migration Checklist

### Phase 1: Type Contracts (Priority: High)

- [ ] Define TypedDict classes for all public interfaces
- [ ] Add Literal types for permission constants
- [ ] Create LockRecord dataclass for Carl Core integration
- [ ] Add type hints to all public methods

### Phase 2: State Boundary (Priority: High)

- [ ] Implement _component_state dictionary
- [ ] Create _init_louis_state() initialization function
- [ ] Implement state accessor functions (get_louis_config, get_louis_warden)
- [ ] Add validation in validate_root_path() and validate_file_path()

### Phase 3: Bridge Definitions (Priority: Medium)

- [ ] Define LouisBridgeProtocol class
- [ ] Implement louis_bridge() for web-based operations
- [ ] Document JS<->Python communication protocol if applicable

### Phase 4: Integration Logic (Priority: Medium)

- [ ] Update 03_gatekeeper.py to use new state management
- [ ] Update carl_core.py to use LouisBridgeProtocol
- [ ] Update graph_builder.py to use get_locked_files_for_graph()
- [ ] Add error handling with descriptive messages

### Phase 5: Testing (Priority: High)

- [ ] Test lock/unlock operations
- [ ] Test git hook installation
- [ ] Test protection status refresh
- [ ] Test fiefdom lock filtering
- [ ] Test error conditions and validation

---

## Notes

- The module intentionally has no internal dependencies, making it highly portable
- Graceful fallback patterns in carl_core.py and graph_builder.py allow optional Louis integration
- The git hook script is embedded as a string and written on-demand
- Permission mode constants (0o444, 0o644) are POSIX-specific and may need adaptation for non-POSIX systems
- The module uses Path.home() for config directory, which assumes POSIX-compatible home directory resolution

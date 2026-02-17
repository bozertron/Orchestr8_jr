# Integration Roadmap: combat_tracker.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/combat_tracker.py`  
**Target:** `a_codex_plan`  
**Date:** 2026-02-16  
**Pattern:** DENSE + GAP

---

## 1. Public API Surface

### 1.1 Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `CombatTracker` | Tracks active LLM General deployments (COMBAT/Purple status) | `deploy()`, `withdraw()`, `is_in_combat()`, `get_active_deployments()`, `get_combat_files()`, `cleanup_stale_deployments()`, `get_deployment_info()` |

### 1.2 Functions/Methods

| Method | Signature | Returns |
|--------|-----------|---------|
| `__init__` | `(project_root: str)` | `None` |
| `_load_state` | `() -> dict` | Combat state dictionary |
| `_save_state` | `(state: dict) -> None` | Persists state to JSON |
| `deploy` | `(file_path: str, terminal_id: str, model: str = "unknown") -> None` | Marks file as COMBAT |
| `withdraw` | `(file_path: str) -> None` | Removes COMBAT status |
| `is_in_combat` | `(file_path: str) -> bool` | Check if file is in COMBAT |
| `get_active_deployments` | `() -> Dict[str, dict]` | All active deployments |
| `get_combat_files` | `() -> List[str]` | Files currently in COMBAT |
| `cleanup_stale_deployments` | `(max_age_hours: int = 24) -> None` | Removes old deployments |
| `get_deployment_info` | `(file_path: str) -> Optional[dict]` | Details for specific file |

### 1.3 State File Schema

**Location:** `.orchestr8/combat_state.json`

```json
{
  "active_deployments": {
    "/path/to/file.py": {
      "deployed_at": "2026-02-16T10:30:00.000000",
      "terminal_id": "terminal-123",
      "model": "claude-3-opus"
    }
  }
}
```

---

## 2. Dependencies

### 2.1 Standard Library

```python
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
```

### 2.2 IP Module Dependencies

| Module | Imported Symbols | Purpose |
|--------|------------------|---------|
| None | - | No internal IP dependencies |

### 2.3 External Dependencies

| Tool/Module | Purpose |
|-------------|---------|
| `pathlib.Path` | File system path handling |
| `json` | State serialization |
| `datetime` | Timestamping deployments |

---

## 3. Integration Points

### 3.1 06_maestro.py (Primary)

```python
# Line 81
from IP.combat_tracker import CombatTracker

# Line 219
combat_tracker = CombatTracker(project_root_path)

# Line 300
combat_tracker.cleanup_stale_deployments(max_age_hours=24)

# Line 513
deployment_info = combat_tracker.get_deployment_info(file_path)

# Line 540, 616, 650, 898
combat_tracker.deploy(...)
```

**Usage Pattern:** Instantiation at plugin init, used for tracking file-level agent deployments across sessions. Called on file selection (deploy) and deselection (withdraw).

### 3.2 CarlCore Integration

```python
# IP/carl_core.py lines 17, 57, 163
from IP.combat_tracker import CombatTracker

self.combat_tracker = CombatTracker(str(self.root))
deployment = self.combat_tracker.get_deployment_info(fiefdom_path)
```

**Usage Pattern:** Provides combat data as part of FiefdomContext aggregation.

### 3.3 Graph Builder Integration

```python
# IP/features/code_city/graph_builder.py lines 128-130, 230-232
from IP.combat_tracker import CombatTracker
tracker = CombatTracker(root)
```

**Usage Pattern:** Used to inject COMBAT/Purple status into Code City visualization.

### 3.4 Standalone Usage

```python
# one integration at a time/orchestr8_standalone.py
from IP.combat_tracker import CombatTracker

combat_tracker = CombatTracker(root)
combat_tracker.deploy(selected, terminal_id, model=selected_model)
combat_tracker.withdraw(selected)
is_in_combat = combat_tracker.is_in_combat(selected)
active_deployments = combat_tracker.get_active_deployments()
```

---

## 4. GAP Analysis & Roadmap

### GAP 1: Type Contracts

**Current State:** Uses raw `dict` and `List[str]` without explicit TypedDict definitions.

**Required Contracts for a_codex_plan:**

| Contract | Type Definition | Notes |
|----------|-----------------|-------|
| `CombatStatus` | `Literal["active", "withdrawn"]` | Deployment lifecycle status |
| `Deployment` | `TypedDict("Deployment", {"deployed_at": str, "terminal_id": str, "model": str})` | Single deployment record |
| `CombatState` | `TypedDict("CombatState", {"active_deployments": Dict[str, Deployment]})` | Full state container |
| `DeploymentInfo` | `TypedDict("DeploymentInfo", {"file_path": str, "deployed_at": str, "terminal_id": str, "model": str, "status": CombatStatus})` | Extended info with status |

**Implementation Priority:** HIGH - Foundation for type-safe integration.

---

### GAP 2: State Boundary

**Current State:** No explicit `_component_state` dict. State is managed through:

- `self.project_root` (Path)
- `self.combat_state_file` (Path)
- File-based JSON persistence via `_load_state()` / `_save_state()`

**Issues Identified:**

1. State loaded/saved on every operation (I/O overhead)
2. No in-memory caching of deployments
3. No history tracking of past deployments (withdrawals not logged)
4. `_load_state()` returns mutable dict - potential state corruption

**Required State Boundary:**

```python
class CombatTracker:
    def __init__(self, project_root: str):
        # Component state - explicit boundary
        self._component_state: Dict[str, Any] = {
            "_initialized": False,
            "_last_load_time": None,
            "_deployments": {},          # In-memory cache of active deployments
            "_history": [],               # Log of all deploy/withdraw events
            "_dirty": False,              # Track if state needs saving
        }
        
        # Configuration (immutable after init)
        self._config = {
            "project_root": Path(project_root),
            "state_file": Path(project_root) / ".orchestr8" / "combat_state.json",
            "max_age_hours": 24,
        }
```

**State Boundary Requirements:**

| Field | Type | Purpose |
|-------|------|---------|
| `_deployments` | `Dict[str, Deployment]` | In-memory cache of active deployments |
| `_history` | `List[DeploymentEvent]` | Historical log of all deploy/withdraw events |
| `_dirty` | `bool` | Track unsaved changes |
| `_last_load_time` | `Optional[datetime]` | Cache invalidation timestamp |

**Implementation Priority:** HIGH - Required for efficient state management and history tracking.

---

### GAP 3: Bridge Definitions

**Current Bridge:** JSON file-based persistence at `.orchestr8/combat_state.json`.

**File→In-Memory Protocol:**

| Field | Type | Description |
|-------|------|-------------|
| `active_deployments` | `Dict[str, Deployment]` | Currently active deployments |

**Python→UI Contract:**

```python
# For Code City integration
{
    "combat_status": {
        "file_path": "IP/components/foo.py",
        "in_combat": true,
        "deployed_at": "2026-02-16T10:30:00.000000",
        "terminal_id": "terminal-123",
        "model": "claude-3-opus"
    }
}

# For bulk deployment status
{
    "combat_files": ["IP/components/foo.py", "IP/utils/bar.py"],
    "deployment_count": 2,
    "active_models": {"claude-3-opus": 1, "claude-3-sonnet": 1}
}
```

**Implementation Priority:** HIGH - Core integration mechanism for Code City visualization.

---

### GAP 4: Integration Logic

**Entry Points for a_codex_plan:**

| Entry Point | Validation Required | Returns |
|-------------|---------------------|---------|
| `CombatTracker.__init__` | `project_root` exists as directory | `CombatTracker` or raises `ValueError` |
| `deploy(file_path, terminal_id, model)` | Valid file_path string, non-empty terminal_id | Updates state, sets dirty flag |
| `withdraw(file_path)` | File in active deployments | Removes deployment, adds to history |
| `is_in_combat(file_path)` | None | Returns bool |
| `get_active_deployments()` | None | Copy of deployments dict |
| `cleanup_stale_deployments(max_age_hours)` | `max_age_hours > 0` | Removes stale, saves if changed |

**Validation Requirements:**

```python
def __init__(self, project_root: str):
    # Validate project_root
    root = Path(project_root)
    if not root.exists():
        raise ValueError(f"project_root does not exist: {project_root}")
    if not root.is_dir():
        raise ValueError(f"project_root is not a directory: {project_root}")
    
    # Initialize state
    self._component_state = {
        "_initialized": True,
        "_last_load_time": datetime.now(),
        "_deployments": {},
        "_history": [],
        "_dirty": False,
    }
```

**Batch Operations (for efficiency):**

```python
def bulk_get_combat_status(self, file_paths: List[str]) -> Dict[str, bool]:
    """Check combat status for multiple files efficiently."""
    return {fp: fp in self._deployments for fp in file_paths}

def get_combat_summary(self) -> Dict[str, Any]:
    """Get aggregated combat statistics."""
    deployments = list(self._deployments.values())
    return {
        "total_active": len(deployments),
        "by_model": self._count_by_model(deployments),
        "oldest_deployment": min((d["deployed_at"] for d in deployments), default=None),
    }
```

**Implementation Priority:** HIGH - Required for production reliability and efficient bulk operations.

---

## 5. Integration Checklist

- [ ] Define TypedDict contracts: `CombatStatus`, `Deployment`, `CombatState`, `DeploymentInfo`
- [ ] Implement `_component_state` boundary with `_deployments`, `_history`, `_dirty`
- [ ] Add in-memory caching to avoid repeated file I/O
- [ ] Add deployment history tracking for audit trail
- [ ] Implement batch operations: `bulk_get_combat_status()`, `get_combat_summary()`
- [ ] Add lazy loading - load state once on first access, not every method call
- [ ] Add `__init__` validation with proper error messages
- [ ] Define Python→UI contracts for Code City integration
- [ ] Add type hints to all public methods
- [ ] Create integration test suite for a_codex_plan

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-------------|
| Concurrent writes corrupt JSON | MEDIUM | HIGH | Add file locking or use atomic writes |
| Stale in-memory cache vs file | MEDIUM | HIGH | Implement `_dirty` flag and explicit save |
| Large history file slows load | LOW | MEDIUM | Paginate history or limit retention |
| Missing state file on first run | LOW | LOW | Handled by mkdir and default state |
| Invalid file_path format | LOW | MEDIUM | Add path validation in deploy() |

---

## 7. Dependencies on Other IP Modules

CombatTracker has **no internal IP dependencies** and can be integrated independently.

However, other modules depend on CombatTracker:

1. **CarlCore** - Uses `CombatTracker.get_deployment_info()` for FiefdomContext
2. **GraphBuilder** - Uses for Code City Purple status injection
3. **Maestro** - Uses for deployment tracking UI

**Recommendation:** CombatTracker can be integrated early due to its simplicity and lack of internal dependencies. It should be available before CarlCore integration completes.

---

## 8. Code City Integration Notes

CombatTracker is critical for the Purple/COMBAT state visualization in Code City:

- **Color:** Purple (#9D4EDD) for active agent deployments
- **Visual:** Files with active deployments show Purple border/glow
- **Data Flow:** 
  1. `combat_tracker.get_combat_files()` → GraphBuilder
  2. GraphBuilder injects Purple status into node metadata
  3. Code City renders Purple buildings/edges

**Required Contract for Code City:**

```python
# Node metadata contract
{
    "id": "IP/components/foo.py",
    "in_combat": true,
    "combat_info": {
        "terminal_id": "terminal-123",
        "model": "claude-3-opus",
        "deployed_at": "2026-02-16T10:30:00.000000"
    }
}
```

---

## 9. Testing Strategy

### Unit Tests

- Test all TypedDict contracts
- Test state boundary initialization
- Test validation in `__init__`
- Test deploy/withdraw lifecycle

### Integration Tests

- Test JSON persistence round-trip
- Test concurrent access scenarios
- Test stale deployment cleanup
- Test Code City metadata contract

### Performance Tests

- Test bulk file status checks
- Test large deployment counts (100+ files)
- Test history size impact on load time

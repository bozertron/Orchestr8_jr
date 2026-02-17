# Integration Roadmap: carl_core.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/carl_core.py`  
**Target:** `a_codex_plan`  
**Date:** 2026-02-16  
**Pattern:** DENSE + GAP

---

## 1. Public API Surface

### 1.1 Classes

| Class | Purpose | Key Methods |
|-------|---------|--------------|
| `CarlContextualizer` | Context Bridge for TypeScript analysis tools | `__init__`, `run_deep_scan()`, `get_file_context()`, `gather_context()`, `gather_context_json()` |
| `FiefdomContext` | Structured context output for fiefdoms (dataclass) | N/A (data container) |

### 1.2 Functions/Methods

| Method | Signature | Returns |
|--------|-----------|---------|
| `__init__` | `(root_path: str, timeout: int = 30, state_managers: Optional[Dict] = None)` | `None` |
| `run_deep_scan` | `() -> Dict[str, Any]` | Analysis results or error dict |
| `get_file_context` | `(rel_path: str) -> str` | XML-wrapped file content |
| `gather_context` | `(fiefdom_path: str) -> FiefdomContext` | Aggregated fiefdom data |
| `gather_context_json` | `(fiefdom_path: str) -> str` | JSON string of context |

### 1.3 Dataclass Fields (FiefdomContext)

| Field | Type | Description |
|-------|------|-------------|
| `fiefdom` | `str` | Fiefdom path (e.g., "IP/") |
| `health` | `Dict[str, Any]` | Health check results |
| `connections` | `Dict[str, Any]` | Import graph data |
| `combat` | `Dict[str, Any]` | Deployment tracking |
| `tickets` | `List[str]` | Active tickets |
| `locks` | `List[Dict[str, str]]` | Louis protection locks |

---

## 2. Dependencies

### 2.1 Standard Library

```python
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
```

### 2.2 IP Module Dependencies

| Module | Imported Symbols | Purpose |
|--------|------------------|---------|
| `IP.health_checker` | `HealthChecker` | File health validation |
| `IP.connection_verifier` | `ConnectionVerifier` | Import graph verification |
| `IP.combat_tracker` | `CombatTracker` | LLM deployment tracking |
| `IP.ticket_manager` | `TicketManager` | Ticket retrieval |
| `IP.louis_core` | `LouisWarden`, `LouisConfig` | File protection system |

### 2.3 External Tools

| Tool | Path | Purpose |
|------|------|---------|
| `npx tsx` | `frontend/tools/unified-context-system.ts` | TypeScript analyzer executor |

---

## 3. Integration Points

### 3.1 06_maestro.py (Primary)

```python
# Line 87
from IP.carl_core import CarlContextualizer

# Line 228
carl = CarlContextualizer(str(project_root_path))
```

**Usage Pattern:** Instantiated once at plugin initialization, used for context aggregation across fiefdoms.

### 3.2 02_explorer.py (Secondary)

```python
# Lines 141-143
from carl_core import CarlContextualizer
carl = CarlContextualizer(root)
context = carl.run_deep_scan()
```

**Usage Pattern:** Triggered on scan action, calls `run_deep_scan()` for deep project analysis.

---

## 4. GAP Analysis & Roadmap

### GAP 1: Type Contracts

**Current State:** Uses `Dict[str, Any]` and `List[Dict[str, str]]` extensively.

**Required Contracts for a_codex_plan:**

| Contract | Type Definition | Notes |
|----------|-----------------|-------|
| `HealthStatus` | `Literal["healthy", "degraded", "broken"]` | Health check result status |
| `HealthError` | `TypedDict("HealthError", {"file": str, "line": int, "message": str})` | Individual error |
| `HealthWarning` | `TypedDict("HealthWarning", {"file": str, "line": int, "message": str})` | Individual warning |
| `HealthData` | `TypedDict("HealthData", {"status": HealthStatus, "errors": List[HealthError], "warnings": List[HealthWarning]})` | Complete health data |
| `ConnectionData` | `TypedDict("ConnectionData", {"imports_from": List[str], "broken": List[Dict[str, Any]]})` | Import graph |
| `CombatData` | `TypedDict("CombatData", {"active": bool, "model": str, "terminal_id": str})` | Deployment info |
| `LockData` | `TypedDict("LockData", {"file": str, "reason": str})` | Protection lock |
| `FiefdomContextType` | `TypedDict("FiefdomContextType", {"fiefdom": str, "health": HealthData, "connections": ConnectionData, "combat": CombatData, "tickets": List[str], "locks": List[LockData]})` | Full context |

**Implementation Priority:** HIGH - Foundation for all downstream integration.

---

### GAP 2: State Boundary

**Current State:** No explicit `_component_state` dict. Uses instance attributes scattered across:

- `self.root`
- `self.timeout`
- `self.ts_tool`
- `self.context_file`
- `self.state_managers` (passed but unused)
- `self.health_checker`
- `self.connection_verifier`
- `self.combat_tracker`
- `self.ticket_manager`
- `self.louis_warden`

**Required State Boundary:**

```python
class CarlContextualizer:
    def __init__(self, root_path: str, timeout: int = 30, state_managers: Optional[Dict] = None):
        # Component state - explicit boundary
        self._component_state: Dict[str, Any] = {
            "_initialized": False,
            "_last_scan_time": None,
            "_scan_in_progress": False,
            "_cache": {},
            "_error_count": 0,
        }
        
        # Configuration (immutable after init)
        self._config = {
            "root": Path(root_path),
            "timeout": timeout,
            "ts_tool": root_path / "frontend/tools/unified-context-system.ts",
            "context_file": root_path / "docs/project-context.json",
        }
        
        # Service references (lazy-loaded)
        self._services: Dict[str, Any] = {}
```

**Implementation Priority:** MEDIUM - Required for reliable state management in a_codex_plan.

---

### GAP 3: Bridge Definitions

**Current Bridge:** `run_deep_scan()` executes TypeScript via subprocess and reads JSON output.

**JS→Python Protocol:**

| Field | Type | Description |
|-------|------|-------------|
| `tool` | `Literal["unified-context-system"]` | Tool identifier |
| `timeout` | `int` | Max execution seconds |
| `output_path` | `str` | JSON result file location |

**Python→JS Response:**

| Field | Type | Description |
|-------|------|-------------|
| `error` | `Optional[str]` | Error message if failed |
| `data` | `Dict[str, Any]` | Parsed JSON from tool |
| `stdout` | `Optional[str]` | Raw output for debugging |
| `stderr` | `Optional[str]` | Error output |

**Python→UI Contract (FiefdomContext):**

```python
# Structured output for Code City integration
{
    "fiefdom": "IP/",
    "health": {...},
    "connections": {...},
    "combat": {...},
    "tickets": [...],
    "locks": [...]
}
```

**Implementation Priority:** HIGH - Core integration mechanism.

---

### GAP 4: Integration Logic

**Entry Points for a_codex_plan:**

| Entry Point | Validation Required | Returns |
|-------------|---------------------|---------|
| `CarlContextualizer.__init__` | `root_path` exists as directory, `timeout > 0` | `CarlContextualizer` or raises `ValueError` |
| `run_deep_scan()` | Tool exists, npx available | `Dict[str, Any]` (always succeeds, errors in dict) |
| `gather_context(fiefdom_path)` | `fiefdom_path` is valid relative path | `FiefdomContext` |
| `gather_context_json(fiefdom_path)` | Same as `gather_context` | JSON string |

**Validation Requirements:**

```python
def __init__(self, root_path: str, timeout: int = 30, state_managers: Optional[Dict] = None):
    # Validate root_path
    root = Path(root_path)
    if not root.exists():
        raise ValueError(f"root_path does not exist: {root_path}")
    if not root.is_dir():
        raise ValueError(f"root_path is not a directory: {root_path}")
    
    # Validate timeout
    if timeout <= 0:
        raise ValueError(f"timeout must be positive, got: {timeout}")
    
    # Validate state_managers type if provided
    if state_managers is not None and not isinstance(state_managers, dict):
        raise ValueError(f"state_managers must be a dict, got: {type(state_managers)}")
```

**Implementation Priority:** HIGH - Required for production reliability.

---

## 5. Integration Checklist

- [ ] Define TypedDict contracts for all `Dict[str, Any]` fields
- [ ] Add `Literal` types for status enums
- [ ] Implement `_component_state` boundary
- [ ] Add `__init__` validation with proper error messages
- [ ] Document JS→Python subprocess protocol
- [ ] Define Python→UI FiefdomContext contract
- [ ] Add type hints to all public methods
- [ ] Create integration test suite for a_codex_plan

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Type inference breaks on refactor | MEDIUM | HIGH | Add runtime validation in GAP 4 |
| Subprocess failure not caught | LOW | MEDIUM | Current implementation already handles errors |
| State leakage between instances | MEDIUM | HIGH | Implement `_component_state` boundary |
| Tool path assumptions break | MEDIUM | MEDIUM | Add validation in `__init__` |

---

## 7. Dependencies on Other IP Modules

To integrate carl_core.py into a_codex_plan, the following must be available:

1. **HealthChecker** - Must be integrated first or mocked
2. **ConnectionVerifier** - Must be integrated first or mocked
3. **CombatTracker** - Must be integrated first or mocked
4. **TicketManager** - Must be integrated first or mocked
5. **LouisWarden** - Graceful fallback already implemented (can be None)

**Recommendation:** These dependencies should be integrated in order before carl_core.py to ensure full functionality.


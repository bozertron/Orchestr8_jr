# Integration Roadmap: health_checker.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/health_checker.py`  
**Target:** `/home/bozertron/a_codex_plan`  
**Pattern:** DENSE + GAP  
**Date:** 2026-02-16

---

## 1. Public API Surface

### 1.1 Enums and Constants

| Symbol | Type | Description |
|--------|------|-------------|
| `CheckerType` | `Enum` | Available checker types: `TYPESCRIPT`, `PYTHON_MYPY`, `PYTHON_RUFF`, `PYTHON_COMPILE` |

### 1.2 Data Classes

| Symbol | Type | Description |
|--------|------|-------------|
| `ParsedError` | `@dataclass` | Structured error with `file`, `line`, `column`, `error_code`, `message`, `severity` |
| `HealthCheckResult` | `@dataclass` | Check result with `status`, `errors`, `warnings`, `last_check`, `raw_output`, `checker_used` |

### 1.3 Main Class

| Symbol | Type | Description |
|--------|------|-------------|
| `HealthChecker` | `class` | Multi-language health checker for TypeScript and Python projects |

### 1.4 Public Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `HealthChecker.__init__` | `(project_root: str)` | Initialize with project root path |
| `HealthChecker.get_available_checkers` | `() -> List[CheckerType]` | Return list of available checkers |
| `HealthChecker.check_typescript` | `(fiefdom_path: Optional[str] = None) -> HealthCheckResult` | Run TypeScript type checking via npm |
| `HealthChecker.check_mypy` | `(target_path: Optional[str] = None) -> HealthCheckResult` | Run mypy type checking |
| `HealthChecker.check_ruff` | `(target_path: Optional[str] = None) -> HealthCheckResult` | Run ruff linting |
| `HealthChecker.check_python_syntax` | `(file_path: str) -> HealthCheckResult` | Check Python file syntax using py_compile |
| `HealthChecker.check_fiefdom` | `(fiefdom_path: str) -> HealthCheckResult` | Run appropriate health check for a fiefdom based on file type |
| `HealthChecker.check_all_fiefdoms` | `(fiefdom_paths: List[str]) -> Dict[str, HealthCheckResult]` | Run health check for multiple fiefdoms |

---

## 2. Dependencies

### 2.1 Standard Library

| Module | Usage |
|--------|-------|
| `subprocess` | Execute external type checkers (npm, mypy, ruff, py_compile) |
| `shutil` | Detect available tools via `which()` |
| `re` | Parse TypeScript, mypy, and ruff output |
| `sys` | Access Python executable path |
| `datetime` | Timestamp check results |
| `pathlib` | File path manipulation |

### 2.2 Typing Imports

| Symbol | Type |
|--------|------|
| `List`, `Dict`, `Optional`, `Tuple` | Generic type hints |
| `Any` | For `to_dict()` return type |

### 2.3 Dataclass/Enum Imports

| Symbol | Source |
|--------|--------|
| `dataclass`, `field` | `dataclasses` |
| `Enum` | `enum` |

### 2.4 External Tool Dependencies

| Tool | Purpose | Detection |
|------|---------|-----------|
| `npm` | Run TypeScript typecheck | `shutil.which("npm")` |
| `mypy` | Python type checking | `shutil.which("mypy")` |
| `ruff` | Python linting | `shutil.which("ruff")` |
| `python` (sys.executable) | Syntax checking | Always available |

---

## 3. Integration Points

### 3.1 Current Consumers

| File | Import | Usage |
|------|--------|-------|
| `IP/plugins/06_maestro.py:78` | `from IP.health_checker import HealthChecker` | Instantiate and run `check_fiefdom("IP")` to update health state |
| `IP/carl_core.py:15,55` | `from .health_checker import HealthChecker` | Instantiate as `self.health_checker` in `CarlContextualizer` |
| `IP/health_watcher.py:30,45` | `from IP.health_checker import HealthChecker, HealthCheckResult` | Instantiate as `self.health_checker` for file change-triggered checks |
| `IP/features/code_city/tests/test_health_flow.py:8` | `from IP.health_checker import HealthCheckResult, ParsedError` | Test assertions |

### 3.2 Data Flow

```
File Change Event (health_watcher.py)
         ↓
    Debounce (100ms)
         ↓
HealthChecker.check_fiefdom()
         ↓
HealthCheckResult (status: "working" | "broken")
         ↓
Code City Status Update (Blue = broken, Gold = working)
```

---

## 4. DENSE + GAP Analysis

### GAP 1: Type Contracts

**Current State:** Uses dataclasses with implicit types. The `severity` and `status` fields use string literals without `Literal` type enforcement.

**Required Contracts for a_codex_plan:**

```python
from typing import Literal, TypedDict

# GAP 1a: Explicit Literal types for status/severity
HealthStatus = Literal["working", "broken"]
SeverityLevel = Literal["error", "warning", "info"]

# GAP 1b: TypedDict for ParsedError serialization
class ParsedErrorDict(TypedDict):
    file: str
    line: int
    column: int
    error_code: str
    message: str
    severity: SeverityLevel

# GAP 1c: TypedDict for HealthCheckResult serialization  
class HealthCheckResultDict(TypedDict):
    status: HealthStatus
    errors: List[ParsedErrorDict]
    warnings: List[ParsedErrorDict]
    error_count: int
    warning_count: int
    last_check: str
    checker_used: str

# GAP 1d: TypedDict for component state boundary
class HealthCheckerState(TypedDict):
    project_root: str
    available_checkers: List[str]
    last_results: Dict[str, HealthCheckResultDict]
    _component_version: str
```

### GAP 2: State Boundary

**Current State:** `HealthChecker` instance stores `_available_checkers` as instance state but has no explicit `_component_state` dict for cross-component state transfer.

**Required State Boundary for a_codex_plan:**

```python
class HealthChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._available_checkers: Dict[CheckerType, bool] = {}
        
        # GAP 2: Explicit component state dict
        self._component_state: Dict[str, Any] = {
            "_component_name": "health_checker",
            "_component_version": "1.0.0",
            "_component_dependencies": ["subprocess", "shutil", "re", "sys"],
            "project_root": str(project_root),
            "available_checkers": [],  # Populated after _detect_available_checkers
            "last_results": {},  # Dict[fiefdom_path, HealthCheckResultDict]
        }
        self._detect_available_checkers()
        
    def get_component_state(self) -> Dict[str, Any]:
        """Export component state for cross-component transport."""
        return {
            **self._component_state,
            "available_checkers": [c.value for c in self.get_available_checkers()],
            "last_results": {
                k: v.to_dict() 
                for k, v in self._component_state.get("last_results", {}).items()
            }
        }
    
    def set_component_state(self, state: Dict[str, Any]) -> None:
        """Restore component state from serialized dict."""
        self._component_state.update(state)
```

### GAP 3: Bridge Definitions

**Current State:** No explicit JS<->Python bridge protocol. Results are Python objects that must be manually serialized.

**Required Bridge for a_codex_plan:**

```python
# GAP 3a: Bridge protocol definition
class HealthCheckerBridge:
    """
    Bridge protocol for HealthChecker JS<->Python communication.
    Defines the contract between orchestr8 frontend and health_checker backend.
    """
    
    # Method signatures exposed to JavaScript
    @staticmethod
    def check(project_root: str, target: str) -> HealthCheckResultDict:
        """Run health check on target path."""
        checker = HealthChecker(project_root)
        result = checker.check_fiefdom(target)
        return result.to_dict()
    
    @staticmethod
    def check_all(project_root: str, fiefdom_paths: List[str]) -> Dict[str, HealthCheckResultDict]:
        """Run health check on multiple fiefdoms."""
        checker = HealthChecker(project_root)
        results = checker.check_all_fiefdoms(fiefdom_paths)
        return {k: v.to_dict() for k, v in results.items()}
    
    @staticmethod
    def get_available(project_root: str) -> List[str]:
        """Get list of available checkers."""
        checker = HealthChecker(project_root)
        return [c.value for c in checker.get_available_checkers()]

# GAP 3b: Event bridge for real-time updates
HEALTH_CHECK_EVENTS = {
    "health:check:start": {"target": str, "checker": Optional[str]},
    "health:check:complete": {"result": HealthCheckResultDict},
    "health:check:error": {"error": str, "target": str},
}
```

### GAP 4: Integration Logic

**Current State:** Direct instantiation by consumers. No validation or entry point abstraction.

**Required Integration Points for a_codex_plan:**

```python
# GAP 4a: Entry point with validation
def create_health_checker(
    project_root: str,
    validate: bool = True
) -> HealthChecker:
    """
    Factory function for creating HealthChecker with validation.
    
    Args:
        project_root: Path to project root
        validate: If True, verify project root exists and is readable
        
    Returns:
        HealthChecker instance
        
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
    
    return HealthChecker(str(root_path))

# GAP 4b: Validation middleware for bridge calls
def validate_health_check_input(
    project_root: str,
    target: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """
    Validate inputs for health check bridge calls.
    
    Returns:
        Tuple of (validated_project_root, validated_target)
        
    Raises:
        ValidationError: If inputs are invalid
    """
    errors = []
    
    if not project_root:
        errors.append("project_root is required")
    
    if target is not None:
        if ".." in target or target.startswith("/"):
            errors.append(f"Invalid target path: {target}")
    
    if errors:
        raise ValidationError(f"Health check validation failed: {', '.join(errors)}")
    
    return str(Path(project_root).resolve()), target
```

---

## 5. Integration Checklist for a_codex_plan

### 5.1 Pre-Integration (GAP 1-2)

- [ ] Add `typing_extensions` or Python 3.8+ for `TypedDict`, `Literal`
- [ ] Define `HealthStatus`, `SeverityLevel` literal types
- [ ] Create `ParsedErrorDict`, `HealthCheckResultDict` TypedDicts
- [ ] Add `_component_state` dict to `HealthChecker.__init__`
- [ ] Implement `get_component_state()` and `set_component_state()` methods

### 5.2 Bridge Layer (GAP 3)

- [ ] Create `HealthCheckerBridge` class with static methods
- [ ] Define `HEALTH_CHECK_EVENTS` event schema
- [ ] Register bridge handlers in a_codex_plan plugin system

### 5.3 Entry Points (GAP 4)

- [ ] Implement `create_health_checker()` factory function
- [ ] Implement `validate_health_check_input()` validation middleware
- [ ] Add error handling for subprocess timeouts and missing tools

### 5.4 Testing

- [ ] Unit test type contract enforcement
- [ ] Unit test state boundary serialization/deserialization
- [ ] Integration test with actual mypy/ruff installations
- [ ] End-to-end test via a_codex_plan UI

---

## 6. File Location Summary

| Artifact | Path |
|----------|------|
| Source | `/home/bozertron/Orchestr8_jr/IP/health_checker.py` |
| Target | `/home/bozertron/a_codex_plan` |
| This Roadmap | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/roadmaps/INTEGRATION_health_checker.md` |

---

## 7. References

- **Current Consumers:** `IP/plugins/06_maestro.py`, `IP/carl_core.py`, `IP/health_watcher.py`
- **Data Flow:** File change → debounce → HealthChecker → HealthCheckResult → Code City
- **Color Contract:** "broken" status maps to Blue (#1fbdea), "working" maps to Gold (#D4AF37)
- **Related Files:** `IP/health_watcher.py` (real-time triggering), `IP/carl_core.py` (context aggregation)

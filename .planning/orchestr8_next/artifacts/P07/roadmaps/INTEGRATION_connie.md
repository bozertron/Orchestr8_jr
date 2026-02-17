# Integration Roadmap: connie.py -> a_codex_plan

**Source**: `/home/bozertron/Orchestr8_jr/IP/connie.py`  
**Target**: `/home/bozertron/a_codex_plan`  
**Date**: 2026-02-16  
**Pattern**: DENSE + GAP

---

## 1. Public API Surface

### 1.1 Classes

| Class | Purpose | Context Manager | Lines |
|-------|---------|-----------------|-------|
| `ConversionEngine` | Headless SQLite database conversion engine | Yes | 26-358 |

**ConversionEngine Methods:**

| Method | Signature | Returns | Notes |
|--------|-----------|---------|-------|
| `__init__` | `(self, db_path: str)` | None | Validates file exists |
| `__enter__` | `(self) -> ConversionEngine` | Self | Opens sqlite3 connection |
| `__exit__` | `(self, exc_type, exc_val, exc_tb) -> None` | None | Closes connection |
| `_ensure_connected` | `(self) -> None` | None | Raises RuntimeError if not in context |
| `list_tables` | `(self) -> pd.DataFrame` | DataFrame | Columns: name, row_count |
| `get_table_schema` | `(self, table_name: str) -> pd.DataFrame` | DataFrame | Columns: column_id, name, type, not_null, default_value, primary_key |
| `get_table_data` | `(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame` | DataFrame | Full table or limited |
| `export_to_json` | `(self, table_name: Optional[str] = None, output_path: str = None) -> str` | str | Path to created file |
| `export_to_csv` | `(self, table_name: str, output_path: str = None) -> str` | str | Path to created file |
| `export_to_markdown` | `(self, table_name: Optional[str] = None, output_path: str = None) -> str` | str | Path to created file |
| `export_to_sql_dump` | `(self, output_path: str = None) -> str` | str | Path to created file |
| `convert_all` | `(self, output_dir: str = ".") -> Dict[str, Any]` | Dict | All formats, returns paths |

### 1.2 Functions

| Function | Signature | Returns | Notes |
|----------|-----------|---------|-------|
| `quick_export` | `(db_path: str, output_format: str = "json", table: str = None) -> str` | str | Convenience wrapper |

### 1.3 Current Type Hints (Implicit)

The current implementation uses implicit types via Python typing module imports:
- `Optional`, `List`, `Dict`, `Any` from `typing`
- `pd.DataFrame` from pandas (duck-typed via import)
- No `TypedDict` or `Literal` types defined
- No explicit state containers

---

## 2. Dependencies

### 2.1 Runtime Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `sqlite3` | stdlib | Database access |
| `pandas` | latest | DataFrame operations, to_markdown, to_csv, to_json |
| `pathlib` | stdlib | Path manipulation |
| `datetime` | stdlib | Timestamps |

### 2.2 Dependency Graph

```
ConversionEngine
├── sqlite3.Connection
├── sqlite3.Cursor  
├── pandas.DataFrame
│   ├── .to_dict()
│   ├── .to_csv()
│   ├── .to_json()
│   └── .to_markdown()
├── pathlib.Path
└── json (stdlib)
```

### 2.3 Import Locations in 04_connie_ui.py

```python
# Line 98: from connie import ConversionEngine
# Line 209: from connie import ConversionEngine  
# Line 282: from connie import ConversionEngine
```

---

## 3. Integration Points

### 3.1 Current Integration: 04_connie_ui.py

The plugin at `/home/bozertron/Orchestr8_jr/IP/plugins/04_connie_ui.py` uses `ConversionEngine` for:

| Feature | Method Used | Line |
|---------|-------------|------|
| Load tables on DB select | `engine.list_tables()` | 101 |
| Export to CSV | `engine.export_to_csv()` | 213 |
| Export to JSON | `engine.export_to_json()` | 215 |
| Export to Markdown | `engine.export_to_markdown()` | 217 |
| Export to SQL | `engine.export_to_sql_dump()` | 219 |
| Batch export | `engine.convert_all()` | 285 |

### 3.2 Fallback Pattern

04_connie_ui.py implements graceful degradation:
1. Try import `ConversionEngine` from connie
2. If ImportError, fall back to raw sqlite3 + pandas
3. Log whether in full-mode or fallback-mode

### 3.3 State Management in 04_connie_ui.py

Local marimo state (lines 56-62):
```python
get_selected_db, set_selected_db = mo.state("")
get_selected_table, set_selected_table = mo.state("")
get_export_format, set_export_format = mo.state("csv")
get_tables, set_tables = mo.state([])
get_preview, set_preview = mo.state(None)
get_export_result, set_export_result = mo.state("")
```

---

## 4. GAP Analysis

### GAP 1: Type Contracts (Explicit TypedDict, Literal Types)

**Current State:** No explicit type contracts defined.

**Required Additions:**

```python
from typing import TypedDict, Literal, NotRequired
from datetime import datetime

# Export format literal type
ExportFormat = Literal["json", "csv", "markdown", "sql"]

# Table info contract
class TableInfo(TypedDict):
    name: str
    row_count: int

# Column schema contract  
class ColumnSchema(TypedDict):
    column_id: int
    name: str
    type: str
    not_null: bool
    default_value: NotRequired[str | None]
    primary_key: bool

# JSON metadata contract
class ExportMetadata(TypedDict):
    database: str
    export_date: str
    table: NotRequired[str]
    row_count: NotRequired[int]
    table_count: NotRequired[int]

# Conversion result contract
class ConversionResult(TypedDict):
    sql: str
    json: str
    markdown: str
    csv: list[str]

# Engine configuration contract
class EngineConfig(TypedDict):
    db_path: str
    output_dir: str
    export_format: ExportFormat
    table_name: NotRequired[str]
```

**GAP 1 Tasks:**
- [ ] Add `ExportFormat` Literal type
- [ ] Define `TableInfo` TypedDict
- [ ] Define `ColumnSchema` TypedDict
- [ ] Define `ExportMetadata` TypedDict
- [ ] Define `ConversionResult` TypedDict
- [ ] Add return type hints to all public methods

---

### GAP 2: State Boundary (Explicit _component_state dict)

**Current State:** No explicit component state container. State lives in marimo mo.state() calls in 04_connie_ui.py.

**Required Additions:**

```python
from typing import TypedDict, NotRequired

class ConnieComponentState(TypedDict):
    """Explicit state boundary for Connie integration."""
    # Database selection
    selected_db: str
    selected_table: str
    
    # UI state
    tables: list[str]
    export_format: str
    
    # Preview/cache
    preview_df: NotRequired[object]  # pd.DataFrame
    
    # Results
    export_result: str
    last_error: NotRequired[str]
    
    # Engine lifecycle
    engine_active: bool
    last_operation: NotRequired[str]
    last_operation_timestamp: NotRequired[str]
```

**GAP 2 Tasks:**
- [ ] Define `ConnieComponentState` TypedDict
- [ ] Add `_component_state: ConnieComponentState` to ConversionEngine
- [ ] Add state initialization in `__enter__`
- [ ] Add state cleanup in `__exit__`
- [ ] Add state mutation methods: `_update_state()`, `_get_state()`
- [ ] Add state validation method: `_validate_state()`

---

### GAP 3: Bridge Definitions (JS<->Python Protocols)

**Current State:** No bridge definitions. 04_connie_ui.py uses direct Python calls via sys.path manipulation.

**Required Additions:**

```python
from typing import Protocol, Callable
from typing_extensions import TypedDict

# Protocol for JS-to-Python bridge
class ConnieBridgeProtocol(Protocol):
    """Protocol for JS<->Python communication."""
    
    def list_tables(self, db_path: str) -> list[TableInfo]: ...
    def get_table_schema(self, db_path: str, table_name: str) -> list[ColumnSchema]: ...
    def get_table_data(self, db_path: str, table_name: str, limit: int | None) -> object: ...
    def export_table(self, db_path: str, table_name: str, format: ExportFormat, output_path: str) -> str: ...
    def export_all(self, db_path: str, output_dir: str) -> ConversionResult: ...

# Bridge message contracts
class BridgeRequest(TypedDict):
    """Incoming request from JS."""
    action: Literal["list_tables", "get_schema", "get_data", "export", "export_all"]
    db_path: str
    table_name: NotRequired[str]
    format: NotRequired[ExportFormat]
    output_path: NotRequired[str]
    limit: NotRequired[int]

class BridgeResponse(TypedDict):
    """Outgoing response to JS."""
    success: bool
    data: NotRequired[object]
    error: NotRequired[str]
    timestamp: str
```

**GAP 3 Tasks:**
- [ ] Define `ConnieBridgeProtocol`
- [ ] Define `BridgeRequest` TypedDict
- [ ] Define `BridgeResponse` TypedDict
- [ ] Implement bridge wrapper class: `ConnieBridge`
- [ ] Add request validation: `validate_request(request: BridgeRequest) -> bool`
- [ ] Add response formatting: `format_response(data: object, error: str | None) -> BridgeResponse`

---

### GAP 4: Integration Logic (Entry Points with Validation)

**Current State:** Direct instantiation in 04_connie_ui.py with try/except import fallback.

**Required Additions:**

```python
from pathlib import Path
from typing import Optional
import logging

class ConnieIntegration:
    """Main integration entry point for a_codex_plan."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._engine: Optional[ConversionEngine] = None
        self._state: ConnieComponentState = {
            "selected_db": "",
            "selected_table": "",
            "tables": [],
            "export_format": "csv",
            "preview_df": None,
            "export_result": "",
            "engine_active": False,
            "last_operation": None,
            "last_operation_timestamp": None
        }
        self._logger = logging.getLogger("connie_integration")
    
    # Entry points with validation
    def connect(self, db_path: str) -> BridgeResponse:
        """Connect to database with validation."""
        # Validate path exists
        full_path = self.project_root / db_path
        if not full_path.exists():
            return {"success": False, "error": f"Database not found: {db_path}", "timestamp": ""}
        
        # Validate extension
        if full_path.suffix not in [".db", ".sqlite", ".sqlite3"]:
            return {"success": False, "error": "Invalid database extension", "timestamp": ""}
        
        try:
            self._engine = ConversionEngine(str(full_path))
            self._engine.__enter__()
            self._state["engine_active"] = True
            self._state["selected_db"] = db_path
            return {"success": True, "data": {"connected": True}, "timestamp": ""}
        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": ""}
    
    def disconnect(self) -> BridgeResponse:
        """Disconnect and cleanup."""
        if self._engine:
            self._engine.__exit__(None, None, None)
            self._engine = None
            self._state["engine_active"] = False
        return {"success": True, "data": {"disconnected": True}, "timestamp": ""}
    
    def list_tables(self) -> BridgeResponse:
        """List tables with state validation."""
        if not self._state["engine_active"]:
            return {"success": False, "error": "Not connected", "timestamp": ""}
        
        try:
            tables = self._engine.list_tables()
            table_list = tables["name"].tolist()
            self._state["tables"] = table_list
            return {"success": True, "data": {"tables": table_list}, "timestamp": ""}
        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": ""}
    
    def export(self, table_name: str, format: ExportFormat, output_dir: str = "exports") -> BridgeResponse:
        """Export with full validation."""
        # Validate connected
        if not self._state["engine_active"]:
            return {"success": False, "error": "Not connected", "timestamp": ""}
        
        # Validate table exists
        if table_name not in self._state["tables"]:
            return {"success": False, "error": f"Table not found: {table_name}", "timestamp": ""}
        
        # Validate format
        if format not in ["json", "csv", "markdown", "sql"]:
            return {"success": False, "error": f"Invalid format: {format}", "timestamp": ""}
        
        # Prepare output directory
        output_path = self.project_root / output_dir
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            if format == "csv":
                result = self._engine.export_to_csv(table_name, str(output_path / f"{table_name}.csv"))
            elif format == "json":
                result = self._engine.export_to_json(table_name, str(output_path / f"{table_name}.json"))
            elif format == "markdown":
                result = self._engine.export_to_markdown(table_name, str(output_path / f"{table_name}.md"))
            elif format == "sql":
                result = self._engine.export_to_sql_dump(str(output_path / f"{self._state['selected_db']}.sql"))
            
            self._state["export_result"] = result
            return {"success": True, "data": {"path": result}, "timestamp": ""}
        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": ""}
    
    def get_state(self) -> ConnieComponentState:
        """Get current component state."""
        return self._state.copy()
```

**GAP 4 Tasks:**
- [ ] Implement `ConnieIntegration` class
- [ ] Add `connect(db_path)` with path validation
- [ ] Add `disconnect()` with cleanup
- [ ] Add `list_tables()` with state update
- [ ] Add `export(table_name, format, output_dir)` with full validation
- [ ] Add `get_state()` accessor
- [ ] Add logging integration
- [ ] Add error recovery logic

---

## 5. Implementation Sequence

### Phase 1: Type Contracts (GAP 1)
1. Add Literal/ TypedDict imports
2. Define all type contracts in new `connie_types.py`
3. Update method signatures with explicit returns
4. Add runtime type checking in debug mode

### Phase 2: State Boundary (GAP 2)
1. Create `_component_state` dict in ConversionEngine
2. Add state initialization/cleanup in context manager
3. Add state accessors
4. Add state validation

### Phase 3: Bridge Definitions (GAP 3)
1. Define bridge protocols
2. Create request/response TypedDicts
3. Implement `ConnieBridge` wrapper
4. Add validation functions

### Phase 4: Integration Logic (GAP 4)
1. Implement `ConnieIntegration` class
2. Add all entry points with validation
3. Add logging
4. Add error recovery
5. Create adapter for a_codex_plan

---

## 6. Acceptance Criteria

- [ ] All public methods have explicit type hints
- [ ] All data structures use TypedDict where applicable
- [ ] Component state is encapsulated in `_component_state`
- [ ] Bridge protocol is defined and documented
- [ ] Integration class provides validated entry points
- [ ] Graceful error handling with informative messages
- [ ] Fallback works when ConversionEngine unavailable
- [ ] Tests verify type contracts at boundaries
- [ ] Documentation for each GAP layer

---

## 7. Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `IP/connie_types.py` | Create | Type contracts (GAP 1) |
| `IP/connie.py` | Modify | Add state, update types (GAP 2) |
| `IP/connie_bridge.py` | Create | Bridge definitions (GAP 3) |
| `IP/connie_integration.py` | Create | Integration logic (GAP 4) |
| `a_codex_plan/orchestr8_next/adapters/connie_adapter.py` | Create | a_codex_plan integration |

---

## 8. References

- Source: `/home/bozertron/Orchestr8_jr/IP/connie.py` (387 lines)
- Integration Point: `/home/bozertron/Orchestr8_jr/IP/plugins/04_connie_ui.py` (319 lines)
- Target: `/home/bozertron/a_codex_plan/orchestr8_next/`

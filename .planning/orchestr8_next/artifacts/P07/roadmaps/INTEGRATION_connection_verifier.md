# Integration Roadmap: connection_verifier.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/connection_verifier.py`  
**Target:** `/home/bozertron/a_codex_plan`  
**Pattern:** DENSE + GAP  
**Date:** 2026-02-16

---

## 1. Public API Surface

### 1.1 Enums and Constants

| Symbol | Type | Description |
|--------|------|-------------|
| `ImportType` | `Enum` | Import source types: `PYTHON`, `JAVASCRIPT`, `TYPESCRIPT`, `UNKNOWN` |
| `IssueSeverity` | `Enum` | Issue severity levels: `CRITICAL`, `ERROR`, `WARNING`, `INFO` with color mapping to Woven Maps system |
| `NodeType` | `Enum` | Graph node types: `FILE`, `COMPONENT`, `STORE`, `ROUTE`, `COMMAND`, `API`, `TYPE`, `ASSET`, `CONFIG`, `TEST`, `ENTRY`, `GROUP` |
| `PYTHON_STDLIB` | `Set[str]` | Common Python standard library modules (70+ modules) |
| `NODE_BUILTINS` | `Set[str]` | Node.js built-in modules (27+ modules) |

### 1.2 Data Classes

| Symbol | Type | Description |
|--------|------|-------------|
| `ImportResult` | `@dataclass` | Single import verification result with `source_file`, `import_statement`, `target_module`, `resolved_path`, `is_resolved`, `is_stdlib`, `is_external`, `line_number` |
| `FileConnectionResult` | `@dataclass` | All import verification results for a file with `file_path`, `total_imports`, `resolved_imports`, `broken_imports`, `external_imports`, `local_imports`, `status` |
| `ConnectionMetrics` | `@dataclass` | Metrics for graph node visualization: `connection_count`, `incoming_count`, `outgoing_count`, `issue_count`, `max_severity`, `centrality`, `in_cycle`, `depth` |
| `GraphNode` | `@dataclass` | A node in the connection graph with `id`, `label`, `file_path`, `node_type`, `status`, `metrics`, `position`, `cluster_id`, and `to_dict()` serialization |
| `GraphEdge` | `@dataclass` | An edge in the connection graph with `source`, `target`, `edge_type`, `resolved`, `line_number`, `weight`, `bidirectional`, and `to_dict()` serialization |
| `PatchbayDryRunResult` | `@dataclass` | Dry-run result for patchbay rewire with `action`, `source_file`, `current_target`, `proposed_target`, `import_type`, `can_apply`, `checks`, `issues`, `warnings`, and camelCase `to_dict()` |

### 1.3 Main Classes

| Symbol | Type | Description |
|--------|------|-------------|
| `ConnectionVerifier` | `class` | Verifies that imports in source files resolve to real files; supports Python, JavaScript, TypeScript |
| `ConnectionGraph` | `class` | Builds and analyzes connection graph from verification results; provides data for Woven Maps Code City |

### 1.4 Public Methods

#### ConnectionVerifier

| Method | Signature | Description |
|--------|-----------|-------------|
| `ConnectionVerifier.__init__` | `(project_root: str, node_modules_path: Optional[str] = None)` | Initialize verifier with project root and optional node_modules path |
| `ConnectionVerifier._detect_file_type` | `(file_path: str) -> ImportType` | Detect source file type from extension |
| `ConnectionVerifier._resolve_python_import` | `(import_path: str, source_file: Path) -> Tuple[Optional[str], bool, bool]` | Resolve Python import; returns `(resolved_path, is_stdlib, is_external)` |
| `ConnectionVerifier._resolve_relative_python_import` | `(import_path: str, source_file: Path) -> Tuple[Optional[str], bool, bool]` | Resolve relative Python imports (from .module import X) |
| `ConnectionVerifier._resolve_js_import` | `(import_path: str, source_file: Path) -> Tuple[Optional[str], bool, bool]` | Resolve JavaScript/TypeScript import |
| `ConnectionVerifier._resolve_relative_js_import` | `(import_path: str, source_file: Path) -> Tuple[Optional[str], bool, bool]` | Resolve relative JS/TS imports |
| `ConnectionVerifier._try_resolve_js_file` | `(target: Path, source_file: Path) -> Tuple[Optional[str], bool, bool]` | Try JS/TS file resolution with various extensions |
| `ConnectionVerifier._extract_imports_with_lines` | `(content: str, patterns: List[re.Pattern]) -> List[Tuple[str, int]]` | Extract imports with line numbers using regex patterns |
| `ConnectionVerifier.verify_file` | `(file_path: str) -> FileConnectionResult` | Verify all imports in a single file |
| `ConnectionVerifier.verify_project` | `(file_paths: Optional[List[str]] = None, extensions: Optional[Set[str]] = None) -> Dict[str, FileConnectionResult]` | Verify imports across project or specific files |
| `ConnectionVerifier.get_broken_imports_summary` | `(results: Dict[str, FileConnectionResult]) -> List[Dict]` | Get summary of all broken imports with suggestions |
| `ConnectionVerifier._suggest_fix` | `(imp: ImportResult) -> str` | Suggest fix for broken import |

#### ConnectionGraph

| Method | Signature | Description |
|--------|-----------|-------------|
| `ConnectionGraph.__init__` | `(verifier: ConnectionVerifier)` | Initialize graph with verifier instance |
| `ConnectionGraph.build_from_results` | `(results: Dict[str, FileConnectionResult]) -> None` | Build graph nodes and edges from verification results |
| `ConnectionGraph.detect_cycles` | `() -> List[List[str]]` | Detect circular dependencies using NetworkX; returns list of cycles |
| `ConnectionGraph.calculate_centrality` | `() -> None` | Calculate PageRank centrality for all nodes |
| `ConnectionGraph.calculate_depth` | `() -> None` | Calculate depth from entry points using BFS |
| `ConnectionGraph.to_dict` | `() -> Dict` | Export graph as dictionary for JSON serialization |
| `ConnectionGraph.to_json` | `() -> str` | Export graph as JSON string |

### 1.5 Top-Level Functions

| Symbol | Signature | Description |
|--------|-----------|-------------|
| `detect_node_type` | `(file_path: str) -> NodeType` | Detect NodeType based on file path patterns |
| `verify_all_connections` | `(project_root: str, files_df) -> Tuple` | Compatibility wrapper for feature-sliced service |
| `build_connection_graph` | `(project_root: str) -> ConnectionGraph` | Compatibility wrapper for feature-sliced service |
| `dry_run_patchbay_rewire` | `(project_root: str, source_file: str, current_target: str, proposed_target: str) -> Dict[str, Any]` | Compatibility wrapper for feature-sliced patchbay |
| `apply_patchbay_rewire` | `(project_root: str, source_file: str, current_target: str, proposed_target: str, auto_rollback: bool = True) -> Dict[str, Any]` | Compatibility wrapper for feature-sliced patchbay |

---

## 2. Dependencies

### 2.1 Standard Library

| Module | Usage |
|--------|-------|
| `os` | File system operations, environment variables |
| `re` | Regex patterns for import extraction |
| `pathlib` | Path manipulation and resolution |
| `dataclasses` | Data class decorators for type contracts |
| `typing` | Type hints (List, Dict, Tuple, Optional, Set, Any) |
| `enum` | Enum definitions |

### 2.2 Optional Dependencies

| Module | Purpose | Detection |
|--------|---------|-----------|
| `networkx` | Graph algorithms (cycle detection, centrality, shortest path) | Falls back gracefully if not installed |

### 2.3 Typing Imports

| Symbol | Type |
|--------|------|
| `Any` | For serialization return types |
| `List`, `Dict`, `Tuple`, `Optional`, `Set` | Generic type hints |

---

## 3. Integration Points

### 3.1 Current Bridge Structure

The module provides compatibility wrappers that delegate to feature-sliced implementations:

```
IP/connection_verifier.py
    |
    +-- verify_all_connections() --> IP/features/connections/service.py
    +-- build_connection_graph() --> IP/features/connections/service.py
    +-- dry_run_patchbay_rewire() --> IP/features/connections/patchbay.py
    +-- apply_patchbay_rewire() --> IP/features/connections/patchbay.py
```

### 3.2 Feature-Sliced Modules

| Module | Purpose |
|--------|---------|
| `IP/features/connections/__init__.py` | Module initialization |
| `IP/features/connections/service.py` | `verify_all_connections()`, `build_connection_graph()` |
| `IP/features/connections/patchbay.py` | `dry_run_patchbay_rewire()`, `apply_patchbay_rewire()` |

---

## 4. GAP Analysis

### 4.1 Type Contracts

**Current State:** Uses `@dataclass` for all type contracts instead of `TypedDict`.

| Contract | Current | Gap | Recommendation |
|----------|---------|-----|----------------|
| `ImportResult` | `@dataclass` | No TypedDict variant exists | Add TypedDict for JSON serialization if needed |
| `FileConnectionResult` | `@dataclass` | No TypedDict variant exists | Add TypedDict for JSON serialization if needed |
| `GraphNode` | `@dataclass` | Has `to_dict()` method | Consider TypedDict for stricter typing |
| `GraphEdge` | `@dataclass` | Has `to_dict()` method | Consider TypedDict for stricter typing |

**Note:** The `@dataclass` approach with `to_dict()` methods provides backward compatibility. TypedDict would be a future enhancement.

### 4.2 State Boundary

**Current State:** No `_component_state` dictionary exists in the module.

| State | Current | Gap | Recommendation |
|-------|---------|-----|----------------|
| `_component_state` | Does not exist | No centralized state management | Create if integrating into stateful UI |
| Instance state | `ConnectionVerifier` stores `project_root`, `node_modules` | Already encapsulated | Maintain as-is for stateless calls |

**Analysis:** The module is designed for stateless operation. Each call to `verify_file()` or `verify_project()` is independent. If integration requires stateful behavior (e.g., caching verification results), consider adding a `_component_state` dict in the wrapper layer rather than modifying this module.

### 4.3 Bridge Requirements

**Current State:** Module provides both direct classes and compatibility wrappers.

| Bridge | Type | Status |
|--------|------|--------|
| `ConnectionVerifier` | Direct class | ✅ Stable API |
| `ConnectionGraph` | Direct class | ✅ Stable API |
| `verify_all_connections()` | Wrapper | ✅ Delegates to feature-sliced |
| `build_connection_graph()` | Wrapper | ✅ Delegates to feature-sliced |
| `dry_run_patchbay_rewire()` | Wrapper | ✅ Delegates to feature-sliced |
| `apply_patchbay_rewire()` | Wrapper | ✅ Delegates to feature-sliced |

**Gap:** No explicit bridge contract defined for UI integration. The module outputs dataclass instances that serialize to dicts.

### 4.4 Integration Logic

**Entry Points:**

| Entry Point | Purpose | Callers |
|-------------|---------|---------|
| `ConnectionVerifier.verify_file()` | Single file import verification | `verify_all_connections()`, direct calls |
| `ConnectionVerifier.verify_project()` | Full project import verification | `build_connection_graph()`, direct calls |
| `ConnectionGraph.build_from_results()` | Graph construction from results | `build_connection_graph()` |
| `detect_node_type()` | Node type detection for visualization | Internal use, graph building |

**Gap:** No explicit entry point for partial graph updates (e.g., re-verify single file after edit).

---

## 5. Integration Recommendations

### 5.1 Recommended Integration Pattern

```python
# Direct usage for full verification
from IP.connection_verifier import ConnectionVerifier, ConnectionGraph

verifier = ConnectionVerifier(project_root="/path/to/project")
results = verifier.verify_project()

graph = ConnectionGraph(verifier)
graph.build_from_results(results)
graph.detect_cycles()
graph.calculate_centrality()
graph.calculate_depth()

# Export for visualization
graph_json = graph.to_json()
```

### 5.2 Patchbay Integration

For import rewire operations:

```python
from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire

# Dry run before applying
dry_result = dry_run_patchbay_rewire(
    project_root="/path/to/project",
    source_file="source.py",
    current_target="old_module",
    proposed_target="new_module"
)

if dry_result["canApply"]:
    apply_result = apply_patchbay_rewire(
        project_root="/path/to/project",
        source_file="source.py",
        current_target="old_module",
        proposed_target="new_module"
    )
```

### 5.3 State Management

If integration requires stateful behavior:

```python
_component_state = {
    "verifier": None,           # ConnectionVerifier instance
    "results_cache": {},       # Dict[str, FileConnectionResult]
    "graph": None,              # ConnectionGraph instance
    "last_scan": None,          # datetime of last scan
    "config": {                 # Configuration overrides
        "max_files": 2500,
        "exclude_dirs": set()
    }
}
```

---

## 6. Color System Alignment

The module integrates with the Woven Maps three-color system:

| IssueSeverity | Color | Meaning |
|---------------|-------|---------|
| `CRITICAL` | Red | File doesn't exist or can't be read |
| `ERROR` | Blue (broken) | Broken imports that block execution |
| `WARNING` | Yellow | Unresolved imports that may be external |
| `INFO` | Gray | Informational (e.g., circular dependency) |

---

## 7. Exclusion Configuration

The module respects environment variables for scan control:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ORCHESTR8_CONN_EXCLUDE_DIRS` | Comma-separated | Additional directories to exclude |
| `ORCHESTR8_CONN_MAX_FILES` | 2500 | Maximum files to scan |

Default exclusions include: `node_modules`, `.git`, `__pycache__`, `.venv`, `venv`, `.env`, `dist`, `build`, `marimo`, `vscode-marimo`, `.taskmaster`, `.planning`, `one integration at a time`, `GSD + Custom Agents`, `SOT`, `Barradeau`, `effects`.

---

## 8. Acceptance Criteria

- [ ] `ConnectionVerifier` can verify imports in Python, JavaScript, and TypeScript files
- [ ] `ConnectionGraph` builds accurate node/edge representation of import relationships
- [ ] Cycle detection works via NetworkX (graceful fallback if not installed)
- [ ] Centrality and depth calculations provide meaningful visualization metrics
- [ ] Patchbay dry-run correctly validates proposed import rewrites
- [ ] Patchbay apply successfully rewires imports with rollback support
- [ ] Output formats (dict, JSON) are compatible with Woven Maps visualization
- [ ] Environment variable configuration is respected
- [ ] Graceful handling of large projects via file count limits

---

## 9. File Location Summary

| Component | File Path |
|-----------|------------|
| Main module | `IP/connection_verifier.py` |
| Feature service | `IP/features/connections/service.py` |
| Patchbay module | `IP/features/connections/patchbay.py` |
| Integration target | `a_codex_plan` (Code City visualization) |

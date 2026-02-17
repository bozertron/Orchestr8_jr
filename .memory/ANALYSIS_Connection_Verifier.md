# ANALYSIS: Connection Verifier

**Source:** `/home/bozertron/Orchestr8_jr/IP/connection_verifier.py`  
**Total Lines:** 975

---

## 1. Function Overview

**Purpose:** Validates that imports in source files actually resolve to real files. Feeds into Blue status (broken) for Woven Maps Code City visualization.

**Supported Languages:**
- Python: `import foo`, `from foo import bar`, `from . import relative`
- JavaScript/TypeScript: `import X from 'path'`, `require('path')`, dynamic `import()`

---

## 2. Key Functions

| Function | Signature | Purpose |
|----------|-----------|---------|
| `ConnectionVerifier.__init__` | `(project_root: str, node_modules_path: Optional[str] = None)` | Initialize verifier with project root |
| `ConnectionVerifier.verify_file` | `(file_path: str) -> FileConnectionResult` | Verify all imports in a single file |
| `ConnectionVerifier.verify_project` | `(file_paths: Optional[List[str]] = None, extensions: Optional[Set[str]] = None) -> Dict[str, FileConnectionResult]` | Verify imports across entire project |
| `ConnectionVerifier.get_broken_imports_summary` | `(results: Dict) -> List[Dict]` | Get summary of broken imports with fix suggestions |
| `ConnectionGraph.build_from_results` | `(results: Dict) -> None` | Build graph from verification results |
| `ConnectionGraph.detect_cycles` | `() -> List[List[str]]` | Detect circular dependencies using NetworkX |
| `ConnectionGraph.calculate_centrality` | `() -> None` | Calculate PageRank centrality scores |
| `ConnectionGraph.calculate_depth` | `() -> None` | Calculate distance from entry points |
| `detect_node_type` | `(file_path: str) -> NodeType` | Detect file type for visual encoding |

### Patchbay Functions (Rewire Workflow)

| Function | Purpose |
|----------|---------|
| `dry_run_patchbay_rewire` | Validate rewire without writing files |
| `apply_patchbay_rewire` | Apply rewire with rollback guardrails |
| `verify_all_connections` | Compatibility wrapper for feature-sliced service |
| `build_connection_graph` | Convenience wrapper for full graph build |

---

## 3. Marimo Mapping

**Entry Points into Orchestr8:**

1. **Direct import via `orchestr8.py`:**
   ```python
   # Not directly imported - uses feature-sliced service layer
   ```

2. **Feature-sliced service layer:** `IP/features/connections/service.py`
   ```python
   from IP.features.connections.service import build_connection_graph
   graph = build_connection_graph(project_root)
   ```

3. **Maestro plugin integration:** `IP/plugins/06_maestro.py`
   ```python
   from IP.connection_verifier import dry_run_patchbay_rewire, apply_patchbay_rewire
   ```

4. **Carl Core integration:** `IP/carl_core.py`
   ```python
   from .connection_verifier import ConnectionVerifier
   self.connection_verifier = ConnectionVerifier(str(self.root))
   ```

**Marimo Cell Dependencies:**
- Connection verification runs as part of the Code City render pipeline
- Graph data feeds into `IP/woven_maps.py` → `build_code_city()`
- Broken imports drive Blue (broken) status coloring in the 3D visualization

---

## 4. Wiring

**Data Flow:**
```
Project Files
    ↓
ConnectionVerifier.verify_project()
    ↓ (returns Dict[file_path → FileConnectionResult])
ConnectionGraph.build_from_results()
    ↓ (creates nodes + edges)
ConnectionGraph.detect_cycles() / calculate_centrality() / calculate_depth()
    ↓ (enriches metrics)
graph.to_dict() → JSON
    ↓
Woven Maps Code City visualization
    ↓ (edges = import relationships, colors = broken/working)
BuildingPanel / Patchbay UI
```

**Key Wire Relationships:**
- `IP/woven_maps.py` → uses `build_connection_graph()` from service
- `IP/features/code_city/graph_builder.py` → imports from `connection_verifier`
- `IP/plugins/06_maestro.py` → patchbay dry-run/apply callbacks
- `IP/carl_core.py` → per-fiefdom connection verification

**Edge Resolution:**
- **Gold edges:** Resolved local imports (working)
- **Blue edges:** Unresolved imports (broken)
- **Gray edges:** External/stdlib imports (not rendered)

---

## 5. Integration into a_codex_plan

**Role in a_codex_plan:** Provides import graph truth source for Code City wiring.

**Contract Points:**

| Consumer | Data Received | Purpose |
|----------|---------------|---------|
| `code_city/graph_builder.py` | `GraphNode`, `GraphEdge` | Build 3D city nodes/edges |
| `woven_maps.py` | Connection results | Color coding (broken = blue) |
| `BuildingPanel` | Broken imports list | Display import issues |
| `Patchbay UI` | `PatchbayDryRunResult` | Rewire validation |

**Configuration:**
```python
# Default exclusions in verify_project()
default_exclusions = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    ".env", "dist", "build", "marimo", "vscode-marimo",
    ".taskmaster", ".planning", "one integration at a time",
    "GSD + Custom Agents", "SOT", "Barradeau", "effects",
}

# Configurable via env var:
# ORCHESTR8_CONN_EXCLUDE_DIRS (comma-separated)
# ORCHESTR8_CONN_MAX_FILES (default: 2500)
```

---

## 6. Ambiguities

### Known Issues

1. **Import Resolution Edge Cases:**
   - Relative imports with complex nested structures may not resolve correctly
   - No support for `__future__` annotations (e.g., `from __future__ import annotations`)
   - Alias detection (`import foo as bar`) is basic

2. **Language Support Gaps:**
   - No support for CSS imports (`@import`)
   - No support for Rust imports
   - JavaScript resolution doesn't check `jsconfig.json` paths

3. **Graph Building Limitations:**
   - NetworkX is optional (falls back silently if not installed)
   - Cycle detection only finds strongly connected components > 1 node
   - No handling of dynamic imports at runtime

4. **Patchbay Limitations:**
   - Rewire assumes single import per line (fails with multi-import statements)
   - No handling of renamed imports in JS (`import { foo as bar }`)
   - Auto-rollback may not handle concurrent file changes

### Configuration Blind Spots

1. **No configurable path aliases:**
   - Hardcoded search in `src`, `lib`, `IP`, `plugins` directories
   - JS alias resolution only checks `@/` and `~/`

2. **Stdlib/Node builtins are hardcoded:**
   - Updates require code changes
   - Not exhaustive (Python: 130 modules, Node: 40 modules)

### Integration Friction Points

1. **Dual import paths:**
   ```python
   # Feature-sliced (preferred)
   from IP.features.connections.service import build_connection_graph
   
   # Direct (legacy)
   from IP.connection_verifier import build_connection_graph
   ```

2. **Wrapper function indirection:**
   - `verify_all_connections()` at line 640 delegates to feature-sliced service
   - `build_connection_graph()` at line 928 delegates similarly
   - Makes debugging stack traces harder

---

## 7. Metrics Summary

| Metric | Value |
|--------|-------|
| Total Lines | 975 |
| Public Classes | 5 (`ImportType`, `IssueSeverity`, `NodeType`, `ConnectionVerifier`, `ConnectionGraph`) |
| Dataclasses | 5 (`ImportResult`, `FileConnectionResult`, `ConnectionMetrics`, `GraphNode`, `GraphEdge`) |
| Stdlib Modules Tracked | 130 |
| Node Builtins Tracked | 40 |
| Max Files Configurable | `ORCHESTR8_CONN_MAX_FILES` (default: 2500) |

---

## 8. Dependencies

| Package | Used For |
|---------|----------|
| `networkx` | Cycle detection, centrality calculation (optional) |
| `os`, `re`, `pathlib` | Core resolution logic |
| Standard library only | No external dependencies |

---

*Analysis generated: 2026-02-16*

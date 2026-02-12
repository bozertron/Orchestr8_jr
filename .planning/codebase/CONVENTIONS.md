# Coding Conventions

**Analysis Date:** 2026-01-30

## Naming Patterns

**Files:**
- Main entry point: `orchestr8.py` (root level)
- Plugin files: Numeric prefix with underscore: `00_welcome.py`, `01_generator.py`, `02_explorer.py` in `IP/plugins/`
- Component files: Descriptive names with underscore separation in `IP/plugins/components/` (e.g., `ticket_panel.py`, `file_explorer_panel.py`)
- Core modules: Descriptive names ending in `_core.py`: `carl_core.py`, `louis_core.py`
- Config files: `pyproject_orchestr8_settings.toml`
- Test files: Prefix naming with `test_` pattern (e.g., `test_adapter.py`, `test_ooda_engine.py`)

**Functions:**
- Use `snake_case` for all function names
- Plugin interface function: Always named `render(STATE_MANAGERS)` - mandatory for plugin protocol
- Helper functions: Prefixed with verb (e.g., `get_file_icon()`, `format_size()`, `scan_directory()`)
- State management: Getter/setter pattern with `get_` and `set_` prefixes (e.g., `get_root()`, `set_root()`)
- Private/internal helpers: Prefixed with underscore (e.g., `_get_context()`, `_get_icon()`)

**Variables:**
- Use `snake_case` for all variables
- State variables: `get_[name], set_[name]` tuple unpacking (e.g., `get_phase, set_phase = mo.state(1)`)
- Constants: ALL_CAPS with underscores (e.g., `DEFAULT_TIMEOUT`, `FILE_ICONS`, `IGNORE_DIRS`)
- Dictionary keys: `snake_case` (e.g., `"project_identity"`, `"technology_stack"`)
- Component states: `get_is_scanning`, `get_refresh_trigger`, `get_selected_files`

**Types:**
- Type hints use standard Python typing: `Dict[str, Any]`, `List[str]`, `Optional[str]`
- Custom types for protocols: Plugin protocol expects `(STATE_MANAGERS)` parameter returning UI element

## Code Style

**Formatting:**
- No explicit formatter configured (not detected: black, isort, autopep8, yapf)
- Consistent with PEP 8 style observed throughout codebase
- Indentation: 4 spaces (Python standard)
- Line length: No strict limit enforced, but most lines stay under 100 characters
- String quotes: Double quotes preferred for docstrings and regular strings

**Linting:**
- No explicit linter configuration found (.pylintrc, .flake8, etc.)
- Code follows PEP 8 implicitly through conventions
- Type hints used throughout for clarity (`Dict[str, Any]`, `Optional[str]`)

## Import Organization

**Order:**
1. Standard library imports (`marimo`, `os`, `sys`, `pathlib`, `json`, `subprocess`, `datetime`)
2. Third-party imports (`pandas`, `networkx`, `pyvis` - for dashboard framework)
3. Local/relative imports (`from IP.plugins.components import ...`)
4. Marimo-specific imports always inside functions when needed (pattern: `import marimo as mo` inside render functions)

**Path Aliases:**
- Relative imports from `IP` module: `from IP.louis_core import LouisWarden`
- Marimo notebook cells reference functions by cell name
- No global import aliases detected - direct imports used

**Pattern Example from `03_gatekeeper.py`:**
```python
from pathlib import Path
from typing import Any
from IP.louis_core import LouisWarden, LouisConfig

import marimo as mo  # Inside render function
```

## Error Handling

**Patterns:**
- Broad try/except blocks for external operations (file I/O, subprocess calls)
- Specific exception handling for expected errors:
  - `subprocess.TimeoutExpired` - for subprocess timeouts
  - `subprocess.CalledProcessError` - for subprocess failures
  - `FileNotFoundError` - for missing files/tools
  - `PermissionError` - for file permission issues
  - `JSONDecodeError` - for JSON parsing failures
  - Generic `Exception` - for fallback/unknown errors

**Error Handling Locations:** `IP/carl_core.py` lines 74-91, `IP/plugins/02_explorer.py` lines 104-105, 147-151

**Convention:** Return error dictionaries from functions that interact with external systems
```python
# From carl_core.py run_deep_scan()
return {
    "error": "Analysis timed out after {self.timeout} seconds",
    "timeout": self.timeout
}
```

**Logging Pattern:**
- No standard logging framework imported
- State-based logging via `get_logs()`/`set_logs()` and appending to logs list
- Log messages prefixed with module name in brackets: `[Plugin Name]` format
- Example from `00_welcome.py`: `set_logs(logs + [f"[Welcome] Tab visited"])`

## Comments

**When to Comment:**
- Module-level docstrings: Always use triple-quoted docstrings for file headers (see `orchestr8.py`, `00_welcome.py`)
- Function docstrings: Use for public API functions (see `CarlContextualizer` class methods)
- Inline comments: Used rarely, only for non-obvious logic or workarounds
- Section markers: Cell comments in Marimo notebooks using `# ============================================================================`

**JSDoc/TSDoc:**
- Python docstrings use standard format with Args/Returns sections
- Example from `carl_core.py`:
```python
def __init__(self, root_path: str, timeout: int = DEFAULT_TIMEOUT):
    """
    Initialize Carl Contextualizer.

    Args:
        root_path: Project root directory
        timeout: Subprocess timeout in seconds (default: 30)
    """
```

## Function Design

**Size:**
- Functions typically range 10-50 lines
- Helper functions kept short (5-20 lines)
- Long functions appear in plugin render logic where UI building is complex

**Parameters:**
- Keep parameter count low (most functions 1-3 parameters)
- Use TYPE_MANAGERS pattern for passing state to plugins: `render(STATE_MANAGERS: dict)`
- Dictionary parameters used for configuration objects (e.g., `LouisConfig`)

**Return Values:**
- Functions return either:
  - Marimo UI elements (mo.md, mo.Html, mo.vstack, etc.) from render functions
  - Dictionaries with 'success' key and data/error info from backend functions
  - State objects or None from state management functions

**Example Pattern:** From `02_explorer.py` scan_directory()
```python
def scan_directory(root_path, max_depth=5):
    """Scan directory and return file list."""
    files = []
    # ... implementation ...
    return files
```

## Module Design

**Exports:**
- Plugin files export exactly 3 module-level variables: `PLUGIN_NAME`, `PLUGIN_ORDER`, and `render` function
- Core modules export classes and utility functions as needed
- No `__all__` lists used, all public names are exported implicitly

**Barrel Files:**
- `IP/plugins/__init__.py` - Empty or minimal (not used for re-exports)
- `IP/__init__.py` - Exports `verify_structure()` and package metadata
- No barrel export patterns used to simplify imports

**Pattern from Plugin System:**
```python
# All plugins follow this exact pattern
PLUGIN_NAME = "Welcome"
PLUGIN_ORDER = 0

def render(STATE_MANAGERS):
    import marimo as mo
    # render implementation
    return mo.vstack([...])
```

## Marimo-Specific Conventions

**Cell Structure:**
- Each Marimo cell decorated with `@app.cell`
- Cell functions return tuples of all local variables to be shared with other cells
- State management uses `mo.state(initial_value)` pattern
- UI building uses `mo.vstack()`, `mo.hstack()`, `mo.md()`, `mo.ui.*` components

**Reactive Pattern:**
- State getters/setters bundled in tuples and passed through STATE_MANAGERS dict
- Plugin render functions are pure functions taking STATE_MANAGERS
- UI elements use `on_change` callbacks for interactivity

## Validation Patterns

**Input Validation:**
- Path validation: `if not root.exists(): return []`
- Permission checks: `try: ... except PermissionError: pass`
- Type validation: Used through type hints, not runtime checks
- JSON validation: Try-catch pattern with fallback to empty dict

**Data Transformation Patterns:**
```python
# From 01_generator.py - CSV parsing helper
def parse_csv(v):
    return [x.strip() for x in v.split(",") if x.strip()]

# From 01_generator.py - JSON parsing helper
def parse_json(v):
    try:
        return json.loads(v) if v.strip() else {}
    except:
        return {}
```

## Marimo Version Compatibility

**Target Version:** Marimo 0.19.6 (specified in generated comment)
- Limited to marimo 0.19.6 API features (no modern progress bars, older UI patterns)
- Workaround example: `mo.Html()` for progress bars since `mo.ui.progress` doesn't exist

---

*Convention analysis: 2026-01-30*

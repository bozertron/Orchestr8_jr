# Architecture

**Analysis Date:** 2026-01-30

## Pattern Overview

**Overall:** Marimo-based plugin system with reactive state management and modular UI layers

**Key Characteristics:**
- Entry point-driven plugin discovery and dynamic loading
- Reactive state management using Marimo's `mo.state()` hooks (tuple-based getter/setter pairs)
- Tab-based UI composition with plugins rendered into tabs
- Modular service layer for domain logic (file protection, health checks, visualization)
- Three-state color system (Gold=working, Blue=broken, Purple=combat) for visual status

## Layers

**Presentation Layer (UI Plugins):**
- Purpose: Render user interfaces and handle user interactions through Marimo components
- Location: `IP/plugins/`
- Contains: Tab plugins (00_welcome through 08_director), component modules (ticket_panel, calendar_panel, etc.)
- Depends on: Marimo, STATE_MANAGERS, service layer modules
- Used by: orchestr8.py main app

**Service/Domain Layer:**
- Purpose: Encapsulate business logic and domain operations (file protection, health checks, visualization, tracking)
- Location: `IP/` (root level files)
- Contains: `louis_core.py` (file protection), `health_checker.py` (code analysis), `woven_maps.py` (visualization), `combat_tracker.py` (LLM deployment tracking), `connection_verifier.py` (import validation), `briefing_generator.py` (context generation), `terminal_spawner.py` (process management), `ticket_manager.py` (issue tracking), `mermaid_generator.py` (diagram generation)
- Depends on: Python stdlib, external packages (anthropic, pandas, networkx, pyvis)
- Used by: Presentation layer plugins

**State Management Layer:**
- Purpose: Centralize reactive state using Marimo's state hooks
- Location: `orchestr8.py` (Cell 2: state_management function)
- Contains: STATE_MANAGERS dict with getter/setter tuples for "root", "files", "selected", "logs"
- Depends on: Marimo `mo.state()`
- Used by: All plugins via STATE_MANAGERS injection

**Application Core:**
- Purpose: Bootstrap the application, load plugins, render UI
- Location: `orchestr8.py` (main entry point)
- Contains: Plugin loader (dynamic import via importlib), tab renderer, main layout (header, controls, tabs)
- Depends on: Presentation layer plugins, State Management layer
- Used by: Marimo runtime

## Data Flow

**Plugin Loading & Initialization:**

1. `orchestr8.py` loads via `marimo run orchestr8.py`
2. Cell 1 imports core dependencies (marimo, pathlib, importlib)
3. Cell 2 initializes STATE_MANAGERS with four reactive state tuples
4. Cell 3 loads plugins from `IP/plugins/` directory using dynamic importlib
   - Scans for `.py` files matching pattern `XX_*.py` (not `__*`)
   - Validates PLUGIN_NAME, PLUGIN_ORDER attributes
   - Validates render(STATE_MANAGERS) function exists
   - Sorts by PLUGIN_ORDER value
5. Cell 4 renders plugins by calling module.render(STATE_MANAGERS) for each
6. Cell 5 creates system logs tab
7. Cell 6 builds main layout with header, controls, and tabs
8. Cell 7 displays layout

**Plugin Rendering Flow:**

1. Plugin receives STATE_MANAGERS dict
2. Plugin extracts relevant state getters: `get_root, set_root = STATE_MANAGERS["root"]`
3. Plugin calls getters to read current state: `root_path = get_root()`
4. Plugin builds Marimo UI with mo.md(), mo.Html(), mo.ui.* components
5. Plugin may update state via setters when user interacts: `set_root(new_path)`
6. STATE_MANAGERS changes trigger reactive re-renders in dependent cells

**File Analysis & Status Flow:**

1. Health checks via `IP/health_checker.py` (mypy, ruff, TypeScript)
2. Import validation via `IP/connection_verifier.py` (resolves and validates imports)
3. Results feed into `IP/woven_maps.py` for Code City visualization
4. Status codes (working=Gold, broken=Blue, combat=Purple) assigned to CodeNode objects
5. Visualization rendered in maestro plugin with colors reflecting status

**State Shape:**

```python
STATE_MANAGERS = {
    "root": (get_root, set_root),           # str - current project root path
    "files": (get_files, set_files),       # dict - current file tree/listing
    "selected": (get_selected, set_selected), # str - currently focused file path
    "logs": (get_logs, set_logs)           # List[str] - system activity log
}
```

## Key Abstractions

**Plugin Protocol:**
- Purpose: Define how plugins integrate with the main app
- Examples: `IP/plugins/00_welcome.py`, `IP/plugins/06_maestro.py`, `IP/plugins/02_explorer.py`
- Pattern: Each plugin exports PLUGIN_NAME (str), PLUGIN_ORDER (int), render(STATE_MANAGERS) function. Render returns Marimo UI element (mo.md, mo.Html, etc.)

**State Managers (Reactive State Tuples):**
- Purpose: Enable reactive data sharing between plugins without global state
- Examples: STATE_MANAGERS["root"], STATE_MANAGERS["logs"]
- Pattern: Tuple of (getter, setter) functions from `mo.state()`. Plugins read via getter(), update via setter(). Changes trigger downstream re-renders.

**CodeNode & Status System:**
- Purpose: Represent individual code files with health/status metadata
- Examples: `IP/woven_maps.py` (CodeNode dataclass)
- Pattern: Dataclass with path, status (working|broken|combat), errors list, position (x,y), metadata (loc, centrality, depth)

**Panel Components:**
- Purpose: Reusable UI components for maestro plugin
- Examples: `IP/plugins/components/ticket_panel.py`, `IP/plugins/components/calendar_panel.py`, `IP/plugins/components/deploy_panel.py`
- Pattern: Classes with render() method returning Marimo UI, style constants for theming

**Service Classes:**
- Purpose: Encapsulate domain-specific operations
- Examples: `LouisWarden` (file protection), `HealthChecker` (code analysis), `CombatTracker` (LLM deployments), `TicketManager` (issue tracking)
- Pattern: Class per domain, stateless where possible, file-based persistence (.orchestr8/, .louis-control/ directories)

## Entry Points

**orchestr8.py:**
- Location: `/home/bozertron/Orchestr8_jr/orchestr8.py`
- Triggers: `marimo run orchestr8.py` or `marimo edit orchestr8.py`
- Responsibilities:
  - Initialize Marimo app
  - Set up STATE_MANAGERS
  - Load plugins dynamically from IP/plugins/
  - Render all plugins into tabs
  - Provide main layout (header, project root input, tabs)
  - Handle plugin errors gracefully

**IP/plugins/06_maestro.py:**
- Location: `/home/bozertron/Orchestr8_jr/IP/plugins/06_maestro.py` (PLUGIN_ORDER=6)
- Triggers: Loaded and rendered as a tab by orchestr8.py
- Responsibilities:
  - Render the "Void" central interface (Woven Maps Code City visualization)
  - Display top navigation (orchestr8, collabor8, JFDI, gener8)
  - Display bottom control surface (maestro input)
  - Integrate all panel components (ticket, calendar, comms, deploy, file_explorer)
  - Enforce three-state color system

**IP/plugins/00_welcome.py:**
- Location: `/home/bozertron/Orchestr8_jr/IP/plugins/00_welcome.py` (PLUGIN_ORDER=0)
- Triggers: Loaded and rendered as first tab
- Responsibilities: Provide getting started guide and plugin overview

## Error Handling

**Strategy:** Graceful degradation with error logging

**Patterns:**

- Plugin load failures caught in `orchestr8.py` Cell 3 plugin_loader: try/except around `importlib.util.spec_from_file_location()` and module loading, errors printed to console with module name
- Plugin render failures caught in Cell 4 plugin_renderer: try/except around `p["module"].render(STATE_MANAGERS)`, errors collected in `plugin_errors` list and printed
- Service layer errors typically surface as status codes: HealthChecker returns HealthCheckResult with status and errors list, ConnectionVerifier returns FileConnectionResult with unresolved_imports, CombatTracker state checked via is_in_combat()
- UI layer errors handled via error state display: `mo.md()` for informational errors, console logging for system errors

## Cross-Cutting Concerns

**Logging:**
- No centralized logger. Errors printed to stdout via print(). System activity logged via STATE_MANAGERS["logs"] (list of strings) in plugins. Manual log updates via `set_logs(existing + [new_entry])`.

**Validation:**
- Plugin discovery validates PLUGIN_NAME and PLUGIN_ORDER attributes
- Plugin protocol enforces render function signature
- File paths validated via pathlib.Path.exists()
- Health checks validate code via external tools (mypy, ruff, TypeScript compiler)

**Authentication:**
- Not implemented. Application assumes single-user local environment.

**Color System (Visual Status Encoding):**
- Gold (#D4AF37): Working - All imports resolve, typecheck passes
- Blue (#1fbdea): Broken - Has errors, needs attention
- Purple (#9D4EDD): Combat - LLM "General" actively deployed
- Black (#0A0A0B): The Void - Background/empty state
- Dark Gray (#121214): Surface - Elevated UI elements

---

*Architecture analysis: 2026-01-30*

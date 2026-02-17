# Codebase Structure

**Analysis Date:** 2026-01-30

## Directory Layout

```
/home/bozertron/Orchestr8_jr/
├── orchestr8.py                           # Main entry point - Marimo app, plugin loader, UI builder
├── pyproject_orchestr8_settings.toml      # Configuration: agents, tools, models, UI settings
├── CLAUDE.md                              # Claude Code guidance and project overview
├── SOT.md                                 # Source of Truth - current state document
├── IP/                                    # Implementation Protocol - core modules
│   ├── __init__.py                        # Package marker
│   ├── plugins/                           # Tab plugins (dynamically loaded)
│   │   ├── __init__.py
│   │   ├── 00_welcome.py                  # Welcome tab (PLUGIN_ORDER=0)
│   │   ├── 01_generator.py                # Generator/wizard plugin (PLUGIN_ORDER=1)
│   │   ├── 02_explorer.py                 # File explorer with Carl integration (PLUGIN_ORDER=2)
│   │   ├── 03_gatekeeper.py               # Louis UI - file protection (PLUGIN_ORDER=3)
│   │   ├── 04_connie_ui.py                # Connie database converter UI (PLUGIN_ORDER=4)
│   │   ├── 05_universal_bridge.py         # Universal bridge UI (PLUGIN_ORDER=5)
│   │   ├── 06_maestro.py                  # ★ THE GOAL - maestro/void interface (PLUGIN_ORDER=6)
│   │   ├── 07_settings.py                 # Settings/config UI (PLUGIN_ORDER=7)
│   │   ├── 08_director.py                 # Director/agent management UI (PLUGIN_ORDER=8)
│   │   ├── 05_cli_bridge.py.deprecated    # Deprecated CLI bridge
│   │   ├── output_renderer.py             # Utility for rendering command output
│   │   ├── status_helpers.py              # Utility helpers for status display
│   │   └── components/                    # Reusable panel components for maestro
│   │       ├── __init__.py
│   │       ├── ticket_panel.py            # Ticket system panel (slides from right)
│   │       ├── calendar_panel.py          # Calendar/schedule panel
│   │       ├── comms_panel.py             # Communications panel
│   │       ├── file_explorer_panel.py     # File browser panel
│   │       └── deploy_panel.py            # Deployment/terminal panel
│   ├── woven_maps.py                      # Code City visualization (core algorithm + rendering)
│   ├── woven_maps_nb.py                   # Marimo notebook version of woven_maps
│   ├── louis_core.py                      # File protection system (chmod 444, lock tracking)
│   ├── combat_tracker.py                  # LLM deployment tracking (Purple status)
│   ├── connection_verifier.py             # Import graph builder (validates imports, detects broken)
│   ├── health_checker.py                  # Health check runner (mypy, ruff, TypeScript)
│   ├── briefing_generator.py              # Context generation for LLM briefings
│   ├── terminal_spawner.py                # Process/terminal session management
│   ├── ticket_manager.py                  # Ticket system (create, update, archive)
│   ├── carl_core.py                       # [TBD] Future module
│   ├── connie.py                          # Database converter core logic
│   ├── connie_gui.py                      # Database converter GUI
│   ├── mermaid_generator.py               # Diagram generation (empire structure, fiefdoms)
│   ├── mermaid_theme.py                   # Mermaid color theme
│   ├── test_styles.py                     # Style testing utility
│   └── styles/
│       ├── font_injection.py              # Font loading utility
│       └── orchestr8.css                  # Global CSS styles
├── one integration at a time/             # Staged integrations (approval required)
│   ├── INTEGRATION_QUEUE.md               # Queue of pending integrations
│   └── docs/                              # Reference specs
├── .orchestr8/                            # Runtime state directory (generated)
│   ├── combat_state.json                  # Current combat deployments
│   └── tickets/                           # Ticket storage
├── .louis-control/                        # Louis file protection config
│   ├── louis-config.json                  # Protected folders list
│   └── protected-files.txt                # List of protected files
└── .planning/                             # Planning documentation
    └── codebase/                          # This analysis output
        ├── ARCHITECTURE.md
        └── STRUCTURE.md
```

## Directory Purposes

**orchestr8.py (Root):**
- Purpose: Main Marimo application entry point
- Contains: 7 cells implementing plugin system, state management, UI rendering
- Key cells: imports, state_management, plugin_loader, plugin_renderer, logs_tab, main_layout, display

**IP/ (Implementation Protocol):**
- Purpose: Core application modules and plugins
- Contains: Service layer, plugin modules, utilities, styles
- Key files: orchestr8.py, pyproject_orchestr8_settings.toml live at root but reference IP structure

**IP/plugins/:**
- Purpose: Tab plugins that render into the main interface
- Contains: 9 ordered plugin files (00_welcome through 08_director), component modules
- Loading: Discovered automatically by orchestr8.py plugin_loader, sorted by PLUGIN_ORDER
- Protocol: Each file exports PLUGIN_NAME (str), PLUGIN_ORDER (int), render(STATE_MANAGERS) function

**IP/plugins/components/:**
- Purpose: Reusable UI panels used by maestro plugin
- Contains: Panel classes with render() methods (ticket, calendar, comms, deploy, file_explorer)
- Styling: Fixed position CSS (right-side panels), maestro color constants

**IP/ Service Modules:**
- Purpose: Domain logic for codebase analysis and control
- Contains:
  - `woven_maps.py`: Code City visualization algorithm
  - `louis_core.py`: File protection via chmod 444
  - `combat_tracker.py`: LLM deployment tracking (.orchestr8/combat_state.json)
  - `connection_verifier.py`: Import validation (Python/JS/TS)
  - `health_checker.py`: Code health via mypy/ruff/TypeScript
  - `briefing_generator.py`: LLM context generation
  - `terminal_spawner.py`: Process management
  - `ticket_manager.py`: Issue tracking (.orchestr8/tickets/)
  - `mermaid_generator.py`: Diagram rendering

**one integration at a time/:**
- Purpose: Staging area for future integrations
- Contains: Pending features awaiting approval
- Policy: Requires Ben's explicit approval before integration into active codebase

**Config Files:**
- `pyproject_orchestr8_settings.toml`: Model selection, agent configuration, UI settings
- `.env`: Runtime secrets (API keys, etc.)
- `CLAUDE.md`: Instructions for Claude Code agent

**State Directories (Generated at Runtime):**
- `.orchestr8/`: Application runtime state
  - `combat_state.json`: Active LLM deployments
  - `tickets/`: Issue tracking files
- `.louis-control/`: File protection state
  - `louis-config.json`: Protected folder configuration
  - `protected-files.txt`: List of locked files

## Key File Locations

**Entry Points:**
- `orchestr8.py`: Main application - `marimo run orchestr8.py` or `marimo edit orchestr8.py`
- `IP/plugins/06_maestro.py`: Goal UI (orchestr8 layout with Void, Woven Maps visualization)

**Configuration:**
- `pyproject_orchestr8_settings.toml`: Models, agents, tools, UI settings
- `.env`: Environment variables and secrets
- `CLAUDE.md`: Claude Code project guidance
- `SOT.md`: Source of Truth document

**Core Logic:**
- `orchestr8.py`: Plugin loading, state management, main UI composition
- `IP/plugins/06_maestro.py`: Central interface (1297 lines)
- `IP/woven_maps.py`: Code City visualization (1981 lines)
- `IP/louis_core.py`: File protection (130 lines)

**Testing/Utilities:**
- `IP/test_styles.py`: Style testing
- `IP/plugins/output_renderer.py`: Command output rendering
- `IP/plugins/status_helpers.py`: Status display helpers

## Naming Conventions

**Files:**
- Plugins: `XX_name.py` where XX is two-digit order (00_welcome, 01_generator, etc.)
- Components: `snake_case_panel.py` (ticket_panel, calendar_panel)
- Modules: `snake_case.py` (louis_core, combat_tracker, health_checker)
- Config: `snake_case.toml` or `.env`

**Directories:**
- Core modules: `IP/`
- Plugins: `IP/plugins/`
- Components: `IP/plugins/components/`
- State: `.directory_name/` (hidden directories, e.g., `.orchestr8/`, `.louis-control/`)
- Styles: `IP/styles/`

**Classes:**
- Service classes: PascalCase, role-descriptive (LouisWarden, CombatTracker, HealthChecker, TicketManager)
- Data classes: PascalCase (CodeNode, Ticket, ImportResult, HealthCheckResult)

**Functions:**
- Plugin export: `render(STATE_MANAGERS)` - standard signature for all plugins
- Constants: SCREAMING_SNAKE_CASE (PLUGIN_NAME, PLUGIN_ORDER, color constants)
- Private/utility: `_snake_case()` or `snake_case()`

## Where to Add New Code

**New Plugin Tab:**
1. Create `IP/plugins/XX_name.py` (choose XX order)
2. Export: `PLUGIN_NAME = "Display Name"`, `PLUGIN_ORDER = XX`, `def render(STATE_MANAGERS):`
3. Return Marimo UI from render() function
4. Plugin auto-loaded on next `marimo run`

**New Panel Component:**
1. Create `IP/plugins/components/name_panel.py`
2. Define class inheriting from panel base or with render() method
3. Use maestro color constants: BLUE_DOMINANT, GOLD_METALLIC, GOLD_DARK, GOLD_SAFFRON, BG_ELEVATED
4. Import in `IP/plugins/06_maestro.py` and add to component registry

**New Service Module:**
1. Create `IP/module_name.py`
2. Define class encapsulating domain logic
3. Use file-based persistence in `.orchestr8/` for state (json files)
4. Import in relevant plugins via `from IP.module_name import ClassName`

**New Utility:**
1. Small utilities: Add to existing module (`status_helpers.py`, `output_renderer.py`)
2. Shared utilities: Create `IP/util_name.py`
3. Styles: Add to `IP/styles/orchestr8.css` or inject via `IP/styles/font_injection.py`

**Testing:**
- Unit tests: Create `IP/tests/` directory (currently no test framework integrated)
- Integration tests: Use `marimo run orchestr8.py` manually for now

## Special Directories

**IP/888/:**
- Purpose: [Undocumented experimental feature]
- Generated: Manual
- Committed: Yes

**one integration at a time/:**
- Purpose: Staged integration queue
- Generated: Manual (requires approval workflow)
- Committed: Yes
- Note: Features staged here must receive Ben's approval before moving to active codebase

**.orchestr8/:**
- Purpose: Application runtime state (combat status, tickets)
- Generated: Yes (auto-created by modules)
- Committed: No (gitignored)

**.louis-control/:**
- Purpose: File protection system state
- Generated: Yes (auto-created by LouisWarden)
- Committed: No (gitignored)

**.planning/codebase/:**
- Purpose: GSD mapping documents (this analysis output)
- Generated: Yes (by GSD mapper)
- Committed: Yes (source of truth for future phases)

## Import Patterns

**Plugin imports:**
```python
# Plugin entry point
PLUGIN_NAME = "Name"
PLUGIN_ORDER = 0

def render(STATE_MANAGERS):
    import marimo as mo
    get_root, set_root = STATE_MANAGERS["root"]
    # ... UI building
    return mo.md("content")
```

**Service imports:**
```python
# In plugins that use services
from IP.health_checker import HealthChecker
from IP.combat_tracker import CombatTracker
from IP.woven_maps import CodeNode, create_code_city

# Services are instantiated with project root
checker = HealthChecker(project_root)
result = checker.check_file(file_path)
```

**State access pattern:**
```python
# All plugins use this pattern
get_root, set_root = STATE_MANAGERS["root"]
get_files, set_files = STATE_MANAGERS["files"]
get_selected, set_selected = STATE_MANAGERS["selected"]
get_logs, set_logs = STATE_MANAGERS["logs"]

# Read state
current_root = get_root()

# Update state
set_root(new_path)
set_logs(get_logs() + [f"New event: {event}"])
```

---

*Structure analysis: 2026-01-30*

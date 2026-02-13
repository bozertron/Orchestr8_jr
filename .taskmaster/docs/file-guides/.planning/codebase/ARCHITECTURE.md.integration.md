# ARCHITECTURE.md Integration Guide

- Source: `.planning/codebase/ARCHITECTURE.md`
- Total lines: `180`
- SHA256: `8e4a03176217c20812f7c0c4d0b038e9cc73392f0ad7a4b5272ebd15ebbe48f4`
- Memory chunks: `2`
- Observation IDs: `1007..1008`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/ARCHITECTURE.md:14` - Three-state color system (Gold=working, Blue=broken, Purple=combat) for visual status
- `.planning/codebase/ARCHITECTURE.md:22` - Depends on: Marimo, STATE_MANAGERS, service layer modules
- `.planning/codebase/ARCHITECTURE.md:23` - Used by: orchestr8.py main app
- `.planning/codebase/ARCHITECTURE.md:34` - Location: `orchestr8.py` (Cell 2: state_management function)
- `.planning/codebase/ARCHITECTURE.md:35` - Contains: STATE_MANAGERS dict with getter/setter tuples for "root", "files", "selected", "logs"
- `.planning/codebase/ARCHITECTURE.md:37` - Used by: All plugins via STATE_MANAGERS injection
- `.planning/codebase/ARCHITECTURE.md:41` - Location: `orchestr8.py` (main entry point)
- `.planning/codebase/ARCHITECTURE.md:50` 1. `orchestr8.py` loads via `marimo run orchestr8.py`
- `.planning/codebase/ARCHITECTURE.md:52` 3. Cell 2 initializes STATE_MANAGERS with four reactive state tuples
- `.planning/codebase/ARCHITECTURE.md:56` - Validates render(STATE_MANAGERS) function exists
- `.planning/codebase/ARCHITECTURE.md:58` 5. Cell 4 renders plugins by calling module.render(STATE_MANAGERS) for each
- `.planning/codebase/ARCHITECTURE.md:65` 1. Plugin receives STATE_MANAGERS dict
- `.planning/codebase/ARCHITECTURE.md:66` 2. Plugin extracts relevant state getters: `get_root, set_root = STATE_MANAGERS["root"]`
- `.planning/codebase/ARCHITECTURE.md:70` 6. STATE_MANAGERS changes trigger reactive re-renders in dependent cells
- `.planning/codebase/ARCHITECTURE.md:77` 4. Status codes (working=Gold, broken=Blue, combat=Purple) assigned to CodeNode objects
- `.planning/codebase/ARCHITECTURE.md:78` 5. Visualization rendered in maestro plugin with colors reflecting status
- `.planning/codebase/ARCHITECTURE.md:83` STATE_MANAGERS = {
- `.planning/codebase/ARCHITECTURE.md:95` - Examples: `IP/plugins/00_welcome.py`, `IP/plugins/06_maestro.py`, `IP/plugins/02_explorer.py`
- `.planning/codebase/ARCHITECTURE.md:96` - Pattern: Each plugin exports PLUGIN_NAME (str), PLUGIN_ORDER (int), render(STATE_MANAGERS) function. Render returns Marimo UI element (mo.md, mo.Html, etc.)
- `.planning/codebase/ARCHITECTURE.md:100` - Examples: STATE_MANAGERS["root"], STATE_MANAGERS["logs"]
- `.planning/codebase/ARCHITECTURE.md:109` - Purpose: Reusable UI components for maestro plugin
- `.planning/codebase/ARCHITECTURE.md:115` - Examples: `LouisWarden` (file protection), `HealthChecker` (code analysis), `CombatTracker` (LLM deployments), `TicketManager` (issue tracking)
- `.planning/codebase/ARCHITECTURE.md:116` - Pattern: Class per domain, stateless where possible, file-based persistence (.orchestr8/, .louis-control/ directories)
- `.planning/codebase/ARCHITECTURE.md:120` **orchestr8.py:**
- `.planning/codebase/ARCHITECTURE.md:121` - Location: `/home/bozertron/Orchestr8_jr/orchestr8.py`

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

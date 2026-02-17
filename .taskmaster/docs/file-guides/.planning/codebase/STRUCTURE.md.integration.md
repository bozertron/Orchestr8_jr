# STRUCTURE.md Integration Guide

- Source: `.planning/codebase/STRUCTURE.md`
- Total lines: `272`
- SHA256: `a90d9ffce4252149d6f0d4030ec9fc9390dd5019fa1b00f6135635f0019657c3`
- Memory chunks: `3`
- Observation IDs: `1029..1031`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/STRUCTURE.md:9` ├── orchestr8.py                           # Main entry point - Marimo app, plugin loader, UI builder
- `.planning/codebase/STRUCTURE.md:10` ├── pyproject_orchestr8_settings.toml      # Configuration: agents, tools, models, UI settings
- `.planning/codebase/STRUCTURE.md:22` │   │   ├── 05_universal_bridge.py         # Universal bridge UI (PLUGIN_ORDER=5)
- `.planning/codebase/STRUCTURE.md:23` │   │   ├── 06_maestro.py                  # ★ THE GOAL - maestro/void interface (PLUGIN_ORDER=6)
- `.planning/codebase/STRUCTURE.md:26` │   │   ├── 05_cli_bridge.py.deprecated    # Deprecated CLI bridge
- `.planning/codebase/STRUCTURE.md:29` │   │   └── components/                    # Reusable panel components for maestro
- `.planning/codebase/STRUCTURE.md:39` │   ├── combat_tracker.py                  # LLM deployment tracking (Purple status)
- `.planning/codebase/STRUCTURE.md:53` │       └── orchestr8.css                  # Global CSS styles
- `.planning/codebase/STRUCTURE.md:57` ├── .orchestr8/                            # Runtime state directory (generated)
- `.planning/codebase/STRUCTURE.md:71` **orchestr8.py (Root):**
- `.planning/codebase/STRUCTURE.md:79` - Key files: orchestr8.py, pyproject_orchestr8_settings.toml live at root but reference IP structure
- `.planning/codebase/STRUCTURE.md:84` - Loading: Discovered automatically by orchestr8.py plugin_loader, sorted by PLUGIN_ORDER
- `.planning/codebase/STRUCTURE.md:85` - Protocol: Each file exports PLUGIN_NAME (str), PLUGIN_ORDER (int), render(STATE_MANAGERS) function
- `.planning/codebase/STRUCTURE.md:88` - Purpose: Reusable UI panels used by maestro plugin
- `.planning/codebase/STRUCTURE.md:90` - Styling: Fixed position CSS (right-side panels), maestro color constants
- `.planning/codebase/STRUCTURE.md:97` - `combat_tracker.py`: LLM deployment tracking (.orchestr8/combat_state.json)
- `.planning/codebase/STRUCTURE.md:102` - `ticket_manager.py`: Issue tracking (.orchestr8/tickets/)
- `.planning/codebase/STRUCTURE.md:111` - `pyproject_orchestr8_settings.toml`: Model selection, agent configuration, UI settings
- `.planning/codebase/STRUCTURE.md:116` - `.orchestr8/`: Application runtime state
- `.planning/codebase/STRUCTURE.md:126` - `orchestr8.py`: Main application - `marimo run orchestr8.py` or `marimo edit orchestr8.py`
- `.planning/codebase/STRUCTURE.md:127` - `IP/plugins/06_maestro.py`: Goal UI (orchestr8 layout with Void, Woven Maps visualization)
- `.planning/codebase/STRUCTURE.md:130` - `pyproject_orchestr8_settings.toml`: Models, agents, tools, UI settings
- `.planning/codebase/STRUCTURE.md:136` - `orchestr8.py`: Plugin loading, state management, main UI composition
- `.planning/codebase/STRUCTURE.md:137` - `IP/plugins/06_maestro.py`: Central interface (1297 lines)
- `.planning/codebase/STRUCTURE.md:158` - State: `.directory_name/` (hidden directories, e.g., `.orchestr8/`, `.louis-control/`)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

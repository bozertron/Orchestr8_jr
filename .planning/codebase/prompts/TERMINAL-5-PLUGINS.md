# Terminal 5: All Plugins (except 06_maestro)

Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

**Files to analyze:**
1. `IP/plugins/__init__.py` (10 lines)
2. `IP/plugins/00_welcome.py` (96 lines)
3. `IP/plugins/01_generator.py` (342 lines)
4. `IP/plugins/02_explorer.py` (264 lines)
5. `IP/plugins/03_gatekeeper.py` (311 lines) — Louis file protection UI
6. `IP/plugins/04_connie_ui.py` (318 lines) — database converter UI
7. `IP/plugins/05_universal_bridge.py` (506 lines) — tool registry
8. `IP/plugins/07_settings.py` (624 lines) — settings panel
9. `IP/plugins/08_director.py` (520 lines) — orchestration
10. `IP/plugins/output_renderer.py` (268 lines)
11. `IP/plugins/status_helpers.py` (101 lines)
12. `IP/plugins/05_cli_bridge.py.deprecated` — note but don't analyze deeply

Read ALL files. For EACH:

1. Does it export PLUGIN_NAME, PLUGIN_ORDER, render()? What values?
2. What does render(STATE_MANAGERS) produce?
3. Marimo API calls — list every mo.* call. Flag incorrect patterns (mo.ui.accordion, style= params, etc.)
4. What core modules does it import and use?
5. Stubs/TODOs/placeholders with line numbers
6. Does it read from orchestr8_settings.toml?
7. Status: Working | Fixed | Partial | Broken

**Also read:** `SOT/MARIMO_API_REFERENCE.md` — this documents known API fixes already applied

**Write report to:** `.planning/codebase/PLUGINS-ANALYSIS.md`

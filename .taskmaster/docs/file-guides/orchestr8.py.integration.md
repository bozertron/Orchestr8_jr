# orchestr8.py Integration Guide

- Source: `orchestr8.py`
- Total lines: `247`
- SHA256: `2bc38945957fb57d0a3f7dac8521ca94986081c0e88ae36362160d901a5bdca6`
- Role: **Entry point** — Marimo app root, STATE_MANAGERS definition, dynamic plugin loader

## Why This Is Painful

- ~~Missing health state keys~~: **RESOLVED** — `STATE_MANAGERS` now has 6 keys: `root`, `files`, `selected`, `logs`, `health`, `health_status`. Health pipeline is fully wired.
- Plugin loader assumes small plugins: `load_plugins()` (line 88) does `spec.loader.exec_module(module)` which executes the entire plugin at import time. For 06_maestro.py (1883 lines), this is expensive and can fail if any import in the chain breaks.
- No error recovery in state: If a plugin crashes during `render()` (line 145), the error is logged but the tab content is skipped — no placeholder or fallback UI.

## Anchor Lines

- `orchestr8.py:19` — `app = marimo.App(width="full")` — Marimo app initialization
- `orchestr8.py:41` — `def state_management(mo, os)` — state management cell
- `orchestr8.py:49` — `get_root, set_root = mo.state(os.getcwd())` — root state (CWD default)
- `orchestr8.py:53` — `get_health, set_health = mo.state({})` — health state (empty dict default)
- `orchestr8.py:54` — `get_health_status, set_health_status = mo.state("idle")` — health status state
- `orchestr8.py:57` — `STATE_MANAGERS = {root, files, selected, logs, health, health_status}` — 6-key state dict
- `orchestr8.py:87` — `def load_plugins()` — scans IP/plugins/*.py, sorted by filename prefix
- `orchestr8.py:105` — `spec = importlib.util.spec_from_file_location(...)` — dynamic plugin import
- `orchestr8.py:111` — `if hasattr(module, "render"):` — plugin protocol validation
- `orchestr8.py:133` — `def plugin_renderer(STATE_MANAGERS, load_plugins, mo)` — renders all plugins into tabs
- `orchestr8.py:145` — `rendered = p["module"].render(STATE_MANAGERS)` — plugin render call with state injection
- `orchestr8.py:220` — `mo.ui.tabs(final_tabs)` — final tabbed UI assembly

## Integration Use

- Health state: **DONE** — `health` and `health_status` keys present in `STATE_MANAGERS` with `mo.state({})` and `mo.state("idle")` defaults.
- Test: Verify `STATE_MANAGERS["health"]` returns `(getter, setter)` tuple and plugin can call `get_health()` without error.

## Resolved Gaps

- [x] Health state keys added to STATE_MANAGERS (health + health_status)
- [x] Return tuple updated to include get_health, set_health, get_health_status, set_health_status

# health_watcher.py Integration Guide

- Source: `IP/health_watcher.py`
- Total lines: `349`
- SHA256: `8278e3243a24f6636a6a8141c5b3d022e429f7ab2183836bdfa82f2cc3d0e0f4`
- Role: **File change watchdog** — debounced file monitoring, triggers HealthChecker, bridges to state/Code City

## Why This Is Painful

- Two implementations, one in use: `HealthWatcher` (line 33, watchdog-based, 100ms debounce) and `HealthWatcherManager` (line 134, Marimo FileWatcherManager, 300ms debounce). 06_maestro.py uses `HealthWatcher` with a callback that now correctly writes to shared state.
- ~~State key dependency~~: **RESOLVED** — `STATE_MANAGERS` in `orchestr8.py` now includes `health` key. `HealthWatcherManager` would work if switched to.
- ~~Callback→state gap~~: **RESOLVED** — `on_health_change()` in 06_maestro.py now merges results into `STATE_MANAGERS["health"]` instead of consuming locally.

## Anchor Lines

- `IP/health_watcher.py:8` — Data flow: `File Change → Debounce → HealthChecker → State → Code City`
- `IP/health_watcher.py:33` — `class HealthWatcher` — watchdog-based, 100ms debounce, callback pattern (in use)
- `IP/health_watcher.py:40` — `DEBOUNCE_MS = 100` — debounce constant
- `IP/health_watcher.py:76` — `def _debounced_check()` — runs health check after debounce, invokes callback
- `IP/health_watcher.py:97` — `def start_watching()` — starts Observer, recursive=True
- `IP/health_watcher.py:134` — `class HealthWatcherManager` — Marimo-integrated, 300ms debounce, state_managers pattern (available but unused)
- `IP/health_watcher.py:144` — `DEBOUNCE_MS = 300` — longer debounce for Marimo integration
- `IP/health_watcher.py:228` — `async def _debounced_check()` — batched health checks, writes to state_managers["health"]
- `IP/health_watcher.py:267` — `if "health" in self._state_managers:` — requires health key in STATE_MANAGERS (now available)
- `IP/health_watcher.py:288` — `from marimo._utils.file_watcher import FileWatcherManager` — Marimo internal import

## Integration Use

- Current approach: `HealthWatcher` + `on_health_change()` callback that merges into `STATE_MANAGERS["health"]`. Works correctly.
- Future upgrade: Switch to `HealthWatcherManager` for tighter Marimo integration (writes directly to state, no callback indirection).
- Test: Modify a .py file, verify debounced health check fires within 100ms and result appears in `get_health()`.

## Resolved Gaps

- [x] HealthWatcher callback now writes to shared state via on_health_change() merge
- [x] STATE_MANAGERS["health"] key exists for both HealthWatcher and HealthWatcherManager paths

# ARCHITECT-FILEWATCHER.md Integration Guide

- Source: `.planning/phases/ARCHITECT-FILEWATCHER.md`
- Total lines: `206`
- SHA256: `f4994c026bb9cfcb94ddef0cbf09e19cf2ed28029cdae3230bfa3a14d32acfd9`
- Memory chunks: `2`
- Observation IDs: `1051..1052`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/ARCHITECT-FILEWATCHER.md:21` - `HealthChecker.check_fiefdom(path)` → `HealthCheckResult` (READY)
- `.planning/phases/ARCHITECT-FILEWATCHER.md:22` - `HealthChecker.check_all_fiefdoms(paths)` → `Dict[str, HealthCheckResult]` (READY)
- `.planning/phases/ARCHITECT-FILEWATCHER.md:26` - **NO bridge** between Marimo's FileWatcherManager and Orchestr8's HealthChecker
- `.planning/phases/ARCHITECT-FILEWATCHER.md:27` - **NO integration** with STATE_MANAGERS reactive system
- `.planning/phases/ARCHITECT-FILEWATCHER.md:36` 3. Calls `HealthChecker.check_fiefdom()` on change
- `.planning/phases/ARCHITECT-FILEWATCHER.md:37` 4. Updates `STATE_MANAGERS["health"]` reactively
- `.planning/phases/ARCHITECT-FILEWATCHER.md:43` ### Primary Location: `orchestr8.py` (entry point)
- `.planning/phases/ARCHITECT-FILEWATCHER.md:46` # orchestr8.py - at module level with other state setup
- `.planning/phases/ARCHITECT-FILEWATCHER.md:47` from IP.health_watcher import HealthWatcherManager
- `.planning/phases/ARCHITECT-FILEWATCHER.md:49` # After STATE_MANAGERS initialization
- `.planning/phases/ARCHITECT-FILEWATCHER.md:50` HEALTH_WATCHER = HealthWatcherManager(
- `.planning/phases/ARCHITECT-FILEWATCHER.md:52` state_managers=STATE_MANAGERS,
- `.planning/phases/ARCHITECT-FILEWATCHER.md:57` ### Alternative: Lazy init in `06_maestro.py` plugin
- `.planning/phases/ARCHITECT-FILEWATCHER.md:61` **Recommendation:** Primary location (orchestr8.py) for immediate real-time behavior.
- `.planning/phases/ARCHITECT-FILEWATCHER.md:71` │  HealthWatcherManager           │
- `.planning/phases/ARCHITECT-FILEWATCHER.md:76` │ 3. Call HealthChecker           │
- `.planning/phases/ARCHITECT-FILEWATCHER.md:80` │  HealthChecker                  │
- `.planning/phases/ARCHITECT-FILEWATCHER.md:88` │  STATE_MANAGERS["health"]       │
- `.planning/phases/ARCHITECT-FILEWATCHER.md:114` class HealthWatcherManager:
- `.planning/phases/ARCHITECT-FILEWATCHER.md:120` self._health_checker = HealthChecker(project_root)
- `.planning/phases/ARCHITECT-FILEWATCHER.md:144` # e.g., "IP/plugins/06_maestro.py" → "IP/"
- `.planning/phases/ARCHITECT-FILEWATCHER.md:161` | `orchestr8.py` integration | ~100 | 1.0 (simple init) | 1 |
- `.planning/phases/ARCHITECT-FILEWATCHER.md:162` | STATE_MANAGERS wiring | ~200 | 1.0 | 1 |
- `.planning/phases/ARCHITECT-FILEWATCHER.md:178` # Verify in orchestr8
- `.planning/phases/ARCHITECT-FILEWATCHER.md:188` | `IP/health_watcher.py` | CREATE | HealthWatcherManager class |

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

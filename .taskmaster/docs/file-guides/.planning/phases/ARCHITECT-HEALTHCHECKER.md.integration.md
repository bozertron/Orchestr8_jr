# ARCHITECT-HEALTHCHECKER.md Integration Guide

- Source: `.planning/phases/ARCHITECT-HEALTHCHECKER.md`
- Total lines: `223`
- SHA256: `c99c2a3e783b74f8c8b5939b162d46cfd5db63170ef19aa3fcc22c2db3cfd8bb`
- Memory chunks: `2`
- Observation IDs: `1053..1054`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:16` | State Management | MISSING | No STATE_MANAGERS connection |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:27` | CodeNode.status | EXISTS | working/broken/combat - NOT populated from HealthChecker |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:31` **Gap:** `analyze_file()` at L234-269 does lightweight scan, ignores HealthChecker.
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:33` ### 06_maestro.py (1298 lines)
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:36` | HealthChecker Import | EXISTS | L77 - imported but unused |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:37` | STATE_MANAGERS | EXISTS | root, selected, logs - NO health state |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:39` | Node Click Handler | EXISTS | `handle_node_click()` for deploy panel |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:41` **Gap:** No health state in STATE_MANAGERS, no reactive health updates.
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:50` - `06_maestro.py` UI structure - stable
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:55` | `woven_maps.py` | Add `build_from_health_results()` to merge HealthChecker output |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:57` | `06_maestro.py` | Add `health` to STATE_MANAGERS |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:58` | `06_maestro.py` | Wire HealthChecker in `build_code_city()` |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:70` **Target:** `06_maestro.py`
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:72` 1. Add `get_health, set_health` to STATE_MANAGERS
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:78` ### Wave 2: HealthWatcher Module (New)
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:81` 1. `HealthWatcher` class wrapping watchdog + HealthChecker
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:93` 3. Update `scan_codebase()` to accept optional `HealthChecker` instance
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:99` **Target:** `IP/plugins/06_maestro.py`
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:101` 1. Instantiate `HealthWatcher` in `render()`
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:114` 3. Prepare for future "Sitting Room" click-to-enter feature
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:128` | `health_watcher.py` → `06_maestro.py` | OUT | Callback receives `Dict[str, HealthCheckResult]` |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:129` | `06_maestro.py` → `STATE_MANAGERS` | OUT | New `health` key in state dict |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:130` | `woven_maps.py` → `06_maestro.py` | IN | Accepts optional health results |
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:133` - `louis_core.py` - LOCKED per CONTEXT.md
- `.planning/phases/ARCHITECT-HEALTHCHECKER.md:163` HealthWatcher._on_file_change() [debounced 100ms]

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

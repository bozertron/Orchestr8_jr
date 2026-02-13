# ARCHITECTURE-health.md Integration Guide

- Source: `.planning/phases/ARCHITECTURE-health.md`
- Total lines: `492`
- SHA256: `73d8fc302a08fce7068af513fa648e3b3681a961d420f3ea15ad85732ae6a78e`
- Memory chunks: `5`
- Observation IDs: `1057..1061`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/ARCHITECTURE-health.md:13` | HealthChecker | `IP/health_checker.py` | 602 | COMPLETE | Multi-language (TS, mypy, ruff, py_compile) |
- `.planning/phases/ARCHITECTURE-health.md:15` | State Manager | `orchestr8.py` | 240 | PARTIAL | Missing health state |
- `.planning/phases/ARCHITECTURE-health.md:16` | Maestro Plugin | `IP/plugins/06_maestro.py` | 1298 | PARTIAL | Uses Code City, no health wiring |
- `.planning/phases/ARCHITECTURE-health.md:22` | No health state in STATE_MANAGERS | Code City can't react to health changes | HIGH |
- `.planning/phases/ARCHITECTURE-health.md:23` | No file watcher integration | Manual refresh only, violates LOCKED spec | HIGH |
- `.planning/phases/ARCHITECTURE-health.md:24` | HealthChecker not wired to Code City | Status from simple analysis, not real checking | HIGH |
- `.planning/phases/ARCHITECTURE-health.md:32` └── HealthChecker EXISTS but NOT CONNECTED
- `.planning/phases/ARCHITECTURE-health.md:35` ### LOCKED Data Flow (REQUIRED)
- `.planning/phases/ARCHITECTURE-health.md:38` File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City
- `.planning/phases/ARCHITECTURE-health.md:47` | Preserve | HealthChecker is complete, no changes needed to core logic | YES |
- `.planning/phases/ARCHITECTURE-health.md:49` | Restructure | STATE_MANAGERS extension is additive, not destructive | YES |
- `.planning/phases/ARCHITECTURE-health.md:54` 1. **HealthChecker is production-ready** — Multi-language, optimized batch checking, proper error parsing
- `.planning/phases/ARCHITECTURE-health.md:56` 3. **STATE_MANAGERS is extensible** — Add `health` key without breaking existing plugins
- `.planning/phases/ARCHITECTURE-health.md:57` 4. **New component required** — FileWatcher/HealthWatcher bridge doesn't exist anywhere
- `.planning/phases/ARCHITECTURE-health.md:64` **Target:** `orchestr8.py`
- `.planning/phases/ARCHITECTURE-health.md:69` # ADD to existing STATE_MANAGERS
- `.planning/phases/ARCHITECTURE-health.md:73` STATE_MANAGERS = {
- `.planning/phases/ARCHITECTURE-health.md:90` **Dependency:** Wave 1 (needs STATE_MANAGERS)
- `.planning/phases/ARCHITECTURE-health.md:92` #### Room: HealthWatcher Class
- `.planning/phases/ARCHITECTURE-health.md:94` class HealthWatcher:
- `.planning/phases/ARCHITECTURE-health.md:101` self.checker = HealthChecker(str(project_root))
- `.planning/phases/ARCHITECTURE-health.md:121` def create_health_watcher_cell(mo, STATE_MANAGERS):
- `.planning/phases/ARCHITECTURE-health.md:123` get_root, set_root = STATE_MANAGERS["root"]
- `.planning/phases/ARCHITECTURE-health.md:126` watcher = HealthWatcher(get_root(), {
- `.planning/phases/ARCHITECTURE-health.md:127` "health": STATE_MANAGERS["health"][1],

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# WIRING_PLAN.md Integration Guide

- Source: `SOT/WIRING_PLAN.md`
- Total lines: `294`
- SHA256: `8334c0cc0c45bfda2c3428cabd6b3fcdd34825ccab8a41d8660402b2d0b85638`
- Memory chunks: `4`
- Observation IDs: `85..88`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `SOT/WIRING_PLAN.md:10` This document outlines the fixes needed to wire up the existing components in 06_maestro.py. The components EXIST - they just need to be connected properly.
- `SOT/WIRING_PLAN.md:16` Replace all legacy brand references with "orchestr8" in the codebase.
- `SOT/WIRING_PLAN.md:22` | `IP/plugins/06_maestro.py` | 7, 873-876 | Brand text updated to "orchestr8" |
- `SOT/WIRING_PLAN.md:23` | `IP/plugins/06_maestro.py` | 189-200 | CSS classes updated to `.orchestr8-*` |
- `SOT/WIRING_PLAN.md:24` | `IP/plugins/06_maestro.py` | 5, 11, 31 | Docstring references |
- `SOT/WIRING_PLAN.md:32` ### Issue 1.1: JFDI Button Opens Wrong Panel
- `SOT/WIRING_PLAN.md:40` # In build_panels(), replace JFDI placeholder with:
- `SOT/WIRING_PLAN.md:67` ### Issue 2.1: HealthChecker Never Instantiated
- `SOT/WIRING_PLAN.md:76` health_checker = HealthChecker(project_root_path)
- `SOT/WIRING_PLAN.md:133` **Expected:** Creating ticket should be linked to combat deployment
- `SOT/WIRING_PLAN.md:196` **Expected:** UI should react to background changes
- `SOT/WIRING_PLAN.md:201` 2. Use file-based signaling (.orchestr8/state.json)
- `SOT/WIRING_PLAN.md:207` **Current:** `cleanup_stale_deployments()` must be called manually
- `SOT/WIRING_PLAN.md:251` **Fix:** Make configurable via orchestr8_settings.toml
- `SOT/WIRING_PLAN.md:261` | A | P0 | Brand replacement (legacy -> orchestr8) | 30 min |
- `SOT/WIRING_PLAN.md:263` | C | P2 | HealthChecker instantiation | 2 hrs |
- `SOT/WIRING_PLAN.md:278` - [ ] Brand shows "orchestr8" with no legacy naming
- `SOT/WIRING_PLAN.md:279` - [ ] CSS classes are `.orchestr8-*`
- `SOT/WIRING_PLAN.md:280` - [ ] Top row: [orchestr8] [collabor8] [JFDI] [gener8]
- `SOT/WIRING_PLAN.md:281` - [ ] JFDI button opens TicketPanel
- `SOT/WIRING_PLAN.md:284` - [ ] HealthChecker is instantiated

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

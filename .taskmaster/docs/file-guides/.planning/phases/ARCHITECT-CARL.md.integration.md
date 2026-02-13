# ARCHITECT-CARL.md Integration Guide

- Source: `.planning/phases/ARCHITECT-CARL.md`
- Total lines: `257`
- SHA256: `af1eeba971059b06d9c005905646b1d159459b3af836e574e89682334bc7e074`
- Memory chunks: `3`
- Observation IDs: `1048..1050`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/ARCHITECT-CARL.md:10` - **Purpose:** TypeScript bridge via subprocess to `unified-context-system.ts`
- `.planning/phases/ARCHITECT-CARL.md:19` | HealthChecker | `health_checker.py:66` | `check_fiefdom(path)` | `HealthCheckResult` |
- `.planning/phases/ARCHITECT-CARL.md:34` - Returns FiefdomContext JSON matching LOCKED structure
- `.planning/phases/ARCHITECT-CARL.md:63` from .health_checker import HealthChecker
- `.planning/phases/ARCHITECT-CARL.md:80` self.health_checker = HealthChecker(root_path)
- `.planning/phases/ARCHITECT-CARL.md:158` **File:** `IP/plugins/06_maestro.py` (Summon panel)
- `.planning/phases/ARCHITECT-CARL.md:168` ### HealthChecker → Carl
- `.planning/phases/ARCHITECT-CARL.md:239` | HealthChecker timeout | Already has timeout handling in source |
- `.planning/phases/ARCHITECT-CARL.md:248` - [ ] Output matches LOCKED JSON structure from CONTEXT.md
- `.planning/phases/ARCHITECT-CARL.md:251` - [ ] Louis remains unchanged (constraint satisfied)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

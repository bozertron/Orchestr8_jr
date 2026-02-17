# ARCH-CARL-CONTEXT.md Integration Guide

- Source: `.planning/phases/ARCH-CARL-CONTEXT.md`
- Total lines: `250`
- SHA256: `62a59b6ed8a64cfb419db32eb9b9a5bdaefe438718038ee06cb665c3dd89695a`
- Memory chunks: `3`
- Observation IDs: `1045..1047`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/phases/ARCH-CARL-CONTEXT.md:9` ## LOCKED Decisions (from CONTEXT.md)
- `.planning/phases/ARCH-CARL-CONTEXT.md:14` | SIGNAL SOURCES | HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden |
- `.planning/phases/ARCH-CARL-CONTEXT.md:37` ### 1. HealthChecker (`IP/health_checker.py`)
- `.planning/phases/ARCH-CARL-CONTEXT.md:118` health_checker: 'HealthChecker',
- `.planning/phases/ARCH-CARL-CONTEXT.md:152` def _gather_health(self, fiefdom_path: str, checker: HealthChecker) -> Dict:
- `.planning/phases/ARCH-CARL-CONTEXT.md:210` | HealthChecker → Carl | IN | `check_fiefdom(path) -> HealthCheckResult` |
- `.planning/phases/ARCH-CARL-CONTEXT.md:219` ## Constraints (MUST NOT)
- `.planning/phases/ARCH-CARL-CONTEXT.md:230` 2. Health signal reflects current HealthChecker status

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

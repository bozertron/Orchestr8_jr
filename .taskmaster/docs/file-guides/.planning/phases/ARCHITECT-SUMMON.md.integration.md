# ARCHITECT-SUMMON.md Integration Guide

- Source: `.planning/phases/ARCHITECT-SUMMON.md`
- Total lines: `150`
- SHA256: `f863f650c4d73d9c9d4b90b14ceadbcfcd00e23dbc7164e0d2f03df9b54bc98e`
- Memory chunks: `2`
- Observation IDs: `1055..1056`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/phases/ARCHITECT-SUMMON.md:11` **Location:** `IP/plugins/06_maestro.py:1081-1095`
- `.planning/phases/ARCHITECT-SUMMON.md:33` 4. **Emergence Animation** — Panel emerges from Void, no breathing
- `.planning/phases/ARCHITECT-SUMMON.md:37` ## 3. Modification Order for 06_maestro.py
- `.planning/phases/ARCHITECT-SUMMON.md:98` # This must NOT block — Carl runs async or returns cached data
- `.planning/phases/ARCHITECT-SUMMON.md:100` carl = Carl(STATE_MANAGERS)
- `.planning/phases/ARCHITECT-SUMMON.md:114` | Signal source wiring (HealthChecker, etc.) | **PENDING** | Context accuracy |
- `.planning/phases/ARCHITECT-SUMMON.md:143` - [ ] Three-state colors only (gold, teal, purple)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

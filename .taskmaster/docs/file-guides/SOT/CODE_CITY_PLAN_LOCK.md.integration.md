# CODE_CITY_PLAN_LOCK.md Integration Guide

- Source: `SOT/CODE_CITY_PLAN_LOCK.md`
- Total lines: `98`
- SHA256: `981b32bbe04af8cee21d4b77e70ee4052996b66a7027eee265dd4d7ea734ae36`
- Memory chunks: `1`
- Observation IDs: `134..134`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `SOT/CODE_CITY_PLAN_LOCK.md:1` # CODE CITY PLAN LOCK (orchestr8)
- `SOT/CODE_CITY_PLAN_LOCK.md:4` Status: Active implementation contract
- `SOT/CODE_CITY_PLAN_LOCK.md:5` Naming lock: orchestr8 only
- `SOT/CODE_CITY_PLAN_LOCK.md:11` │ [orchestr8]              [collabor8]              [JFDI]        │
- `SOT/CODE_CITY_PLAN_LOCK.md:15` │         Gold = Working    Teal = Broken    Purple = Combat      │
- `SOT/CODE_CITY_PLAN_LOCK.md:17` │ [Apps] [Calendar*] [Comms*] [Files] == [maestro] == [Search]    │
- `SOT/CODE_CITY_PLAN_LOCK.md:42` - `File Change -> HealthWatcher -> HealthChecker -> STATE_MANAGERS -> Code City`
- `SOT/CODE_CITY_PLAN_LOCK.md:61` ### 5.3 Sitting Room
- `SOT/CODE_CITY_PLAN_LOCK.md:70` - Validate border/contract compatibility before write
- `SOT/CODE_CITY_PLAN_LOCK.md:87` 4. Implement Sitting Room transition + handoff contract
- `SOT/CODE_CITY_PLAN_LOCK.md:94` - Color contract unchanged
- `SOT/CODE_CITY_PLAN_LOCK.md:95` - Formula contract used in runtime building generation

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

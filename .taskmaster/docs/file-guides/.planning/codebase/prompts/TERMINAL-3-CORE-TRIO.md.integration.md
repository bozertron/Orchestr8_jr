# TERMINAL-3-CORE-TRIO.md Integration Guide

- Source: `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md`
- Total lines: `25`
- SHA256: `255424f6fce6cc07cc1de81aa5189b844542cffb95cd6b737c885b36d1505595`
- Memory chunks: `1`
- Observation IDs: `1023..1023`

## Why This Is Painful

- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:5` These 3 modules feed data into Code City node colors. They're the data pipeline.
- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:9` 2. `IP/health_checker.py` (601 lines) — determines node colors (Gold/Teal)
- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:10` 3. `IP/combat_tracker.py` (114 lines) — tracks LLM deployments (Purple)
- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:16` 3. Integration surface: How does 06_maestro.py or woven_maps.py consume this?
- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:21` 8. Config: Does it read from orchestr8_settings.toml?
- `.planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md:23` **Critical question:** Health data is supposed to color Code City nodes. Trace the FULL pipeline: health_checker → ??? → woven_maps node colors. Where does it break?

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

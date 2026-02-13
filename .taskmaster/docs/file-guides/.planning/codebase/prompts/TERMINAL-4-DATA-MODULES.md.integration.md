# TERMINAL-4-DATA-MODULES.md Integration Guide

- Source: `.planning/codebase/prompts/TERMINAL-4-DATA-MODULES.md`
- Total lines: `25`
- SHA256: `d44d4f285c5a52fe8ac6658024c5952829aca5fd456da7cd0ce4a981d7c3e1cd`
- Memory chunks: `1`
- Observation IDs: `1024..1024`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `.planning/codebase/prompts/TERMINAL-4-DATA-MODULES.md:8` 3. `IP/ticket_manager.py` (260 lines) — JFDI ticket system
- `.planning/codebase/prompts/TERMINAL-4-DATA-MODULES.md:16` 3. How it's consumed by 06_maestro.py
- `.planning/codebase/prompts/TERMINAL-4-DATA-MODULES.md:22` - `ticket_panel.py` — JFDI button in 06_maestro.py opens a PLACEHOLDER instead of using this. Why? How to fix?

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

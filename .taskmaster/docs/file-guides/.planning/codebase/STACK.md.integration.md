# STACK.md Integration Guide

- Source: `.planning/codebase/STACK.md`
- Total lines: `134`
- SHA256: `0bed6dbceb5b77ced6a6630f5b34928b4669a58a3c3fc0f8c3b3940ca586f0d9`
- Memory chunks: `2`
- Observation IDs: `1027..1028`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `.planning/codebase/STACK.md:17` - Python 3.12+ (required per `orchestr8.py` docstring)
- `.planning/codebase/STACK.md:28` - Used in `orchestr8.py` (entry point: `marimo.App()`)
- `.planning/codebase/STACK.md:55` - Try/except handling in `IP/plugins/06_maestro.py`
- `.planning/codebase/STACK.md:63` - toml - Configuration file parsing (`pyproject_orchestr8_settings.toml`)
- `.planning/codebase/STACK.md:66` - json - State persistence (`.orchestr8/combat_state.json`)
- `.planning/codebase/STACK.md:77` - Configuration via `pyproject_orchestr8_settings.toml` (340+ lines)
- `.planning/codebase/STACK.md:101` - Development: `marimo edit orchestr8.py` (hot reload)
- `.planning/codebase/STACK.md:102` - Production: `marimo run orchestr8.py`
- `.planning/codebase/STACK.md:122` - File system: `.orchestr8/` directory for state persistence

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

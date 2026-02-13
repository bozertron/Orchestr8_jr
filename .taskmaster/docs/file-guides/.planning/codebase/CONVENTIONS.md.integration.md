# CONVENTIONS.md Integration Guide

- Source: `.planning/codebase/CONVENTIONS.md`
- Total lines: `214`
- SHA256: `7e710affd1728e03d2cd87c9412d7dcb17498d91cf408224efa50f02527b4257`
- Memory chunks: `2`
- Observation IDs: `1011..1012`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/codebase/CONVENTIONS.md:8` - Main entry point: `orchestr8.py` (root level)
- `.planning/codebase/CONVENTIONS.md:12` - Config files: `pyproject_orchestr8_settings.toml`
- `.planning/codebase/CONVENTIONS.md:17` - Plugin interface function: Always named `render(STATE_MANAGERS)` - mandatory for plugin protocol
- `.planning/codebase/CONVENTIONS.md:31` - Custom types for protocols: Plugin protocol expects `(STATE_MANAGERS)` parameter returning UI element
- `.planning/codebase/CONVENTIONS.md:101` - Module-level docstrings: Always use triple-quoted docstrings for file headers (see `orchestr8.py`, `00_welcome.py`)
- `.planning/codebase/CONVENTIONS.md:129` - Use TYPE_MANAGERS pattern for passing state to plugins: `render(STATE_MANAGERS: dict)`
- `.planning/codebase/CONVENTIONS.md:165` def render(STATE_MANAGERS):
- `.planning/codebase/CONVENTIONS.md:180` - State getters/setters bundled in tuples and passed through STATE_MANAGERS dict
- `.planning/codebase/CONVENTIONS.md:181` - Plugin render functions are pure functions taking STATE_MANAGERS

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

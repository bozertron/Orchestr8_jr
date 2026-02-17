# TERMINAL-5-PLUGINS.md Integration Guide

- Source: `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md`
- Total lines: `31`
- SHA256: `5399e2d8f020a96d7b44c623c6a703fa370b6e832bf8be7bbc486dc0f9578b0d`
- Memory chunks: `1`
- Observation IDs: `1025..1025`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md:1` # Terminal 5: All Plugins (except 06_maestro)
- `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md:12` 7. `IP/plugins/05_universal_bridge.py` (506 lines) — tool registry
- `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md:17` 12. `IP/plugins/05_cli_bridge.py.deprecated` — note but don't analyze deeply
- `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md:22` 2. What does render(STATE_MANAGERS) produce?
- `.planning/codebase/prompts/TERMINAL-5-PLUGINS.md:26` 6. Does it read from orchestr8_settings.toml?

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

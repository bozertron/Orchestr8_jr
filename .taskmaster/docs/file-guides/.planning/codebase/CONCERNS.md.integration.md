# CONCERNS.md Integration Guide

- Source: `.planning/codebase/CONCERNS.md`
- Total lines: `211`
- SHA256: `77fd03d66869c13f56d1a7efda89480717d9227383d872fed2d32a3df7aa9c4b`
- Memory chunks: `2`
- Observation IDs: `1009..1010`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/CONCERNS.md:14` - Issue: Chat functionality in `IP/plugins/06_maestro.py` (lines 88-92) gracefully degrades if anthropic not installed, but core functionality depends on environment variable `ANTHROPIC_API_KEY` without validation
- `.planning/codebase/CONCERNS.md:15` - Files: `IP/plugins/06_maestro.py` (handle_send function, lines 753-844)
- `.planning/codebase/CONCERNS.md:17` - Fix approach: Add initialization-time validation of `ANTHROPIC_API_KEY` in `orchestr8.py` entry point; log clear warning if missing before any chat attempt
- `.planning/codebase/CONCERNS.md:20` - Issue: `pyproject_orchestr8_settings.toml` contains many placeholder values like `[local_doc_model]`, `[path_to_image_model]`, `[neo4j_password]` that are never validated
- `.planning/codebase/CONCERNS.md:21` - Files: `pyproject_orchestr8_settings.toml` (lines 47, 121, 130, 149, 162, 237, etc.)
- `.planning/codebase/CONCERNS.md:28` - Symptoms: If `build_code_city()` throws exception in `06_maestro.py`, error appears inline in UI but doesn't prevent rest of interface from loading
- `.planning/codebase/CONCERNS.md:29` - Files: `IP/plugins/06_maestro.py` (build_code_city function, lines 917-944)
- `.planning/codebase/CONCERNS.md:31` - Workaround: Set project root to a valid directory; check `.orchestr8/` subdirectory isn't corrupted
- `.planning/codebase/CONCERNS.md:35` - Files: `IP/plugins/06_maestro.py` (toggle_calendar, toggle_comms, toggle_file_explorer functions, lines 441-485)
- `.planning/codebase/CONCERNS.md:41` - Files: `IP/terminal_spawner.py` (spawn function, lines 71-95), `IP/plugins/06_maestro.py` (handle_apps, handle_matrix, handle_files functions, lines 657-720)
- `.planning/codebase/CONCERNS.md:49` - Files: `IP/plugins/06_maestro.py` (anthropic client initialization, lines 754-785)
- `.planning/codebase/CONCERNS.md:51` - Recommendations: (1) Add rate limiting on API calls, (2) Never log full API responses, (3) Consider proxy pattern for API calls, (4) Document that this application should not be exposed to untrusted networks
- `.planning/codebase/CONCERNS.md:64` - Files: `IP/plugins/06_maestro.py` (lines 659-720)
- `.planning/codebase/CONCERNS.md:74` - Improvement path: (1) Add `.orchestr8/scan_cache.json` with timestamp, (2) Invalidate cache only on file modification, (3) Cache imports graph for faster connection verification
- `.planning/codebase/CONCERNS.md:83` - Problem: Every state change in `06_maestro.py` triggers full re-render of panels that read that state
- `.planning/codebase/CONCERNS.md:84` - Files: `IP/plugins/06_maestro.py` (state management pattern, lines 375-423)
- `.planning/codebase/CONCERNS.md:91` - Files: `orchestr8.py` (plugin_loader function, lines 88-124)
- `.planning/codebase/CONCERNS.md:93` - Safe modification: (1) Before changing plugin names/order, verify no other plugins import them, (2) Add plugin dependency declaration mechanism, (3) Test all plugins load by running `marimo run orchestr8.py`
- `.planning/codebase/CONCERNS.md:97` - Files: `IP/plugins/06_maestro.py` (lines 403-407 create panel instances), `IP/plugins/components/ticket_panel.py`, `IP/plugins/components/calendar_panel.py`, etc.
- `.planning/codebase/CONCERNS.md:100` - Test coverage: No tests for panel visibility state machine; changes must be manually tested in UI
- `.planning/codebase/CONCERNS.md:103` - Files: All plugins that use `STATE_MANAGERS` pattern
- `.planning/codebase/CONCERNS.md:104` - Why fragile: Distributed state across many cells; no centralized state schema; easy to create stale state if cells don't properly depend on each other
- `.planning/codebase/CONCERNS.md:109` - Files: `IP/woven_maps.py` (COLORS dict, lines 30-48), `IP/plugins/06_maestro.py` (constants lines 128-134, CSS lines 139-328)
- `.planning/codebase/CONCERNS.md:110` - Why fragile: Color system is three-state (Gold/Blue/Purple) but exact hex values appear in multiple places; inconsistencies will appear visually
- `.planning/codebase/CONCERNS.md:111` - Safe modification: (1) If you change one color constant, search all files for that hex value and update, (2) Verify the CSS in 06_maestro.py matches the Python constants, (3) Test visual rendering after any color change

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

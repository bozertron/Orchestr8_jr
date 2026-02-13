# TESTING.md Integration Guide

- Source: `.planning/codebase/TESTING.md`
- Total lines: `303`
- SHA256: `f7642e15df4de734e1ebd004f4893259b7b4cfc4e627837ed98a8fa0c6a1c839`
- Memory chunks: `3`
- Observation IDs: `1034..1036`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/codebase/TESTING.md:127` 'app_context': 'orchestr8'
- `.planning/codebase/TESTING.md:187` {'invalid_structure': 'this should cause an error'}
- `.planning/codebase/TESTING.md:191` # Adapter should handle gracefully
- `.planning/codebase/TESTING.md:233` - STATE_MANAGERS injection: Not tested
- `.planning/codebase/TESTING.md:234` - File path: `orchestr8.py` (lines 78-156) - plugin_loader function

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

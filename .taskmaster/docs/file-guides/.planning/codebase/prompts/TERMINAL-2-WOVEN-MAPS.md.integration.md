# TERMINAL-2-WOVEN-MAPS.md Integration Guide

- Source: `.planning/codebase/prompts/TERMINAL-2-WOVEN-MAPS.md`
- Total lines: `29`
- SHA256: `5a5693f5d75546f4c70dca8c0d1309efd15065412ec0b986ff50188fe80247ae`
- Memory chunks: `1`
- Observation IDs: `1022..1022`

## Why This Is Painful

- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/prompts/TERMINAL-2-WOVEN-MAPS.md:16` 5. **Control panel**: What buttons exist in the bottom 5th? Gold/Teal/Purple filters, keyframes, audio, Re-Emerge, Clear
- `.planning/codebase/prompts/TERMINAL-2-WOVEN-MAPS.md:20` 9. **Click handling**: WOVEN_MAPS_NODE_CLICK postMessage events

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

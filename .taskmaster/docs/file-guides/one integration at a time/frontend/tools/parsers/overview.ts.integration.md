# overview.ts Integration Guide

- Source: `one integration at a time/frontend/tools/parsers/overview.ts`
- Total lines: `234`
- SHA256: `5eebb70c88b27828be38e51ee85c6d67097a6ac58a62bc1047501a925152ee82`
- Memory chunks: `2`
- Observation IDs: `626..627`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/frontend/tools/parsers/overview.ts:61` * Check if a path should be ignored based on patterns.
- `one integration at a time/frontend/tools/parsers/overview.ts:63` function shouldIgnore(name: string): boolean {
- `one integration at a time/frontend/tools/parsers/overview.ts:110` if (shouldIgnore(item.name)) continue;

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

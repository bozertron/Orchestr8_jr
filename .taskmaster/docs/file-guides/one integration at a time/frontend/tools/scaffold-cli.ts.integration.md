# scaffold-cli.ts Integration Guide

- Source: `one integration at a time/frontend/tools/scaffold-cli.ts`
- Total lines: `368`
- SHA256: `a436bdcfc551a1ed6950703f966d1875c2b217482bf8b8a3b00e955418f90d45`
- Memory chunks: `4`
- Observation IDs: `629..632`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/frontend/tools/scaffold-cli.ts:68` * Every parser plugin must implement this interface to be discoverable
- `one integration at a time/frontend/tools/scaffold-cli.ts:265` throw new Error('Invalid plugin structure - must implement ScaffoldPlugin interface');

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

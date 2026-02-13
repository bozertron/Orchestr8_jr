# migrationAssistantParser.md Integration Guide

- Source: `one integration at a time/Staging/migrationAssistantParser.md`
- Total lines: `102`
- SHA256: `095cb632eb63cb61b876c53155773912412e368863c38d9394e645ebec1a7570`
- Memory chunks: `1`
- Observation IDs: `832..832`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/Staging/migrationAssistantParser.md:10` This plugin aims to bridge the gap between raw analysis data and actionable integration steps, significantly aiding developers (human or LLM) in the migration process.
- `one integration at a time/Staging/migrationAssistantParser.md:17` * `options`: An object containing the necessary data, likely passed from `integr8` or a dedicated command. This **must** include:

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

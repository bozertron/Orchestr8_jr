# extension.toml Integration Guide

- Source: `one integration at a time/orchestr8-zed/extension.toml`
- Total lines: `27`
- SHA256: `aee908f38ddd6310dba4f626cab076cd47c8facea60d683fedf8b95b500d3a0e`
- Memory chunks: `1`
- Observation IDs: `672..672`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/orchestr8-zed/extension.toml:1` id = "orchestr8"
- `one integration at a time/orchestr8-zed/extension.toml:4` schema_version = 1
- `one integration at a time/orchestr8-zed/extension.toml:7` repository = "https://github.com/bozertron/orchestr8-zed"
- `one integration at a time/orchestr8-zed/extension.toml:10` [context_servers.orchestr8]

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# Cargo.toml Integration Guide

- Source: `one integration at a time/orchestr8-zed/Cargo.toml`
- Total lines: `12`
- SHA256: `24471e83e05ef272596e63e31498e16fc1b067cb12a53499bc0424ce8c17f991`
- Memory chunks: `1`
- Observation IDs: `671..671`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/orchestr8-zed/Cargo.toml:2` name = "orchestr8"

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

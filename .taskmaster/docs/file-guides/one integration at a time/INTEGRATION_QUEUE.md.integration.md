# INTEGRATION_QUEUE.md Integration Guide

- Source: `one integration at a time/INTEGRATION_QUEUE.md`
- Total lines: `98`
- SHA256: `267add2009f4f2ccd01581f33086c7cceb597dc0f822bf67833013f8ddd26f9e`
- Memory chunks: `1`
- Observation IDs: `649..649`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/INTEGRATION_QUEUE.md:16` ║   Each integration must be pressure tested with Ben's feedback. ║
- `one integration at a time/INTEGRATION_QUEUE.md:39` | 13 | `orchestr8-zed/` | Zed IDE extension | Rust | Pending |
- `one integration at a time/INTEGRATION_QUEUE.md:43` | 17 | `orchestr8_mcp.py` | MCP server for IDE integration | ~490 | Pending |
- `one integration at a time/INTEGRATION_QUEUE.md:44` | 18 | `orchestr8_standalone.py` | Legacy monolithic version (reference) | ~710 | Pending |
- `one integration at a time/INTEGRATION_QUEUE.md:45` | 19 | `IP--orchestr8_app.py` | Redundant loader (merge or discard) | ~250 | Pending |
- `one integration at a time/INTEGRATION_QUEUE.md:75` - `marimo run orchestr8.py` works
- `one integration at a time/INTEGRATION_QUEUE.md:76` - `06_maestro.py` renders correctly

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

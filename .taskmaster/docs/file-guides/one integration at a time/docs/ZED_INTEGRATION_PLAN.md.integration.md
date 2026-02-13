# ZED_INTEGRATION_PLAN.md Integration Guide

- Source: `one integration at a time/docs/ZED_INTEGRATION_PLAN.md`
- Total lines: `457`
- SHA256: `9f2af1548356f0156065465fdac6b4e23904f006f502a6da2c3276ced5b982f9`
- Memory chunks: `4`
- Observation IDs: `484..487`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:13` 2. maestro AI orchestration layer
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:37` │                    │  orchestr8_mcp.py │                        │
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:57` orchestr8-zed/
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:64` └── orchestr8_mcp.py     # Symlinked/bundled MCP server
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:70` id = "orchestr8"
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:73` schema_version = 1
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:76` repository = "https://github.com/bozertron/orchestr8-zed"
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:79` [context_servers.orchestr8]
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:99` name = "orchestr8"
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:154` // Return path to orchestr8_mcp.py
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:156` Ok("/home/bozertron/Orchestr8_jr/orchestr8_mcp.py".to_string())
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:213` Zed's Agent Panel can use MCP servers for context. Our `orchestr8_mcp.py` provides:
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:231` - maestro state indicator (OFF/OBSERVE/ON)
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:244` │   ├── orchestr8_app.py     # Main Marimo app
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:249` └── orchestr8_mcp.py         # MCP server (already created)
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:258` mkdir -p ~/Orchestr8_jr/orchestr8-zed/src
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:259` cd ~/Orchestr8_jr/orchestr8-zed
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:265` - Select `orchestr8-zed` directory
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:285` | Port maestro CSS | Convert 06_maestro.py styles to Zed theme | 4h |
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:287` | Status bar item | maestro state indicator | 2h |
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:315` ### In orchestr8_mcp.py (Python subprocess)
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:322` The Marimo app (`IP/orchestr8_app.py`) could:
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:335` mkdir -p ~/Orchestr8_jr/orchestr8-zed/src
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:338` cat > ~/Orchestr8_jr/orchestr8-zed/extension.toml << 'EOF'
- `one integration at a time/docs/ZED_INTEGRATION_PLAN.md:339` id = "orchestr8"

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

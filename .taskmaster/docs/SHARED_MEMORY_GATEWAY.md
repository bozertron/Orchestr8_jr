# Shared Memory Gateway

This stack gives all agents a single memory backend and a universal HTTP API.

- Backend store: `~/.claude-mem`
- claude-mem worker: `127.0.0.1:37777`
- Universal gateway: `127.0.0.1:37888`

## Why this exists

- Claude Code can use `claude-mem` via MCP.
- Other tools (VS Code, Antigravity, scripts, task workers) can use one stable REST interface.
- Everyone reads/writes the same memory store.

## Start / Stop

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
bash .taskmaster/tools/memory-gateway/memory-stack.sh status
bash .taskmaster/tools/memory-gateway/memory-stack.sh stop
```

## Universal API

- `GET /v1/memory/schema` - capability + endpoint schema
- `GET /v1/memory/health` - gateway + worker health
- `GET|POST /v1/memory/search` - search index
- `GET|POST /v1/memory/timeline` - timeline around anchor/query
- `POST /v1/memory/observations` - full observation payloads
- `POST /v1/memory/save` - manual memory write
- `GET|POST /v1/memory/brief` - budget-capped shortlist + observation IDs
- `GET|POST /v1/memory/graph` - lightweight query/file/risk/anchor/observation graph

Compatibility aliases:

- `POST /api/memory/save` -> same as `/v1/memory/save`
- `POST /api/observations/save` -> same as `/v1/memory/save` (legacy caller compatibility)

## Minimal examples

```bash
curl -s "http://127.0.0.1:37888/v1/memory/search?query=code+city&limit=5"
```

```bash
curl -s -X POST "http://127.0.0.1:37888/v1/memory/save" \
  -H "Content-Type: application/json" \
  -d '{"title":"Code City lock","text":"Three-state color system: Gold/Teal/Purple"}'
```

```bash
curl -s -X POST "http://127.0.0.1:37888/v1/memory/observations" \
  -H "Content-Type: application/json" \
  -d '{"ids":[1,2,3]}'
```

```bash
curl -s "http://127.0.0.1:37888/v1/memory/brief?q=code+city&budget=1600&file_limit=6"
```

```bash
curl -s "http://127.0.0.1:37888/v1/memory/graph?q=node+click+bridge&file_limit=8&anchor_limit=3"
```

## Anti-15K Strategy

Use strict staged retrieval:

1. `brief` to shortlist files + IDs under a fixed budget.
2. `graph` to understand relationship neighborhoods.
3. `observations` only for selected IDs.

## MCP wiring in this repo

Project `.mcp.json` includes:

- `claude-mem` MCP server (`mcp-server.cjs`) pointing to this shared store.
- `task-master-ai` MCP server for planning/task operations.

This means Claude sessions in this repo and local gateway clients can use the same memory database.

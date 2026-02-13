# CODE_CITY_LANDSCAPE.md Integration Guide

- Source: `SOT/CODE_CITY_LANDSCAPE.md`
- Total lines: `90`
- SHA256: `0833f76a8dd526bd4fed39ed56e83339e028f9b6e5a228c6cdcc65d1c09de666`
- Memory chunks: `2`
- Observation IDs: `68..69`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `SOT/CODE_CITY_LANDSCAPE.md:22` | Canonical frame (`orchestr8/collabor8/JFDI`, no `gener8`) | behavior | `SOT/CODE_CITY_PLAN_LOCK.md:7`, `IP/plugins/06_maestro.py:1185` | Top-row labels, Void center, bottom control frame, no brand drift | UI regression check for top-row contract | partial |
- `SOT/CODE_CITY_LANDSCAPE.md:23` | Three-state color contract | behavior | `SOT/CODE_CITY_PLAN_LOCK.md:22`, `IP/woven_maps.py:116` | Gold/Teal/Purple + Void/Surface, no extra states | Shared enum/constants module consumed by all renderers/services | partial |
- `SOT/CODE_CITY_LANDSCAPE.md:31` | Tooltip + node click event contract | routine | `IP/woven_maps.py:2651`, `IP/woven_maps.py:2689`, `IP/plugins/06_maestro.py:1716` | Event schema (`path/status/errors/metrics`), routing to UI handlers | JS event arrives, but no Python bridge calling `handle_node_click()` | missing |
- `SOT/CODE_CITY_LANDSCAPE.md:35` | Sitting Room transition + return | feature | `SOT/CODE_CITY_PLAN_LOCK.md:61` | Entry trigger, morph animation, context handoff to collaboration surface | No Sitting Room runtime implementation | missing |
- `SOT/CODE_CITY_LANDSCAPE.md:36` | Health flow (`File Change -> HealthWatcher -> HealthChecker -> STATE -> Code City`) | routine | `IP/health_watcher.py:8`, `IP/plugins/06_maestro.py:1207`, `orchestr8.py:55`, `IP/woven_maps.py:527` | Global health state in app root, watcher lifecycle, merge function call in render pipeline | Root app state lacks `health` key; health merge function exists but not wired through `create_code_city()` | partial |
- `SOT/CODE_CITY_LANDSCAPE.md:45` | Broken-node deploy + ticket generation flow | routine | `IP/plugins/06_maestro.py:678`, `IP/plugins/06_maestro.py:709`, `SOT/todo.md:102` | Ticket payload schema from Carl/health + deploy action chain | Auto-ticket generation from node click not wired end-to-end | partial |
- `SOT/CODE_CITY_LANDSCAPE.md:54` - Transport: iframe `postMessage` payload + Marimo handler contract.
- `SOT/CODE_CITY_LANDSCAPE.md:57` - `mode` (`overview`, `dive`, `focus`, `room`, `sitting_room`), `position`, `target`, `zoom`, `return_stack`.
- `SOT/CODE_CITY_LANDSCAPE.md:58` - Includes warp-dive timing and easing parameters.
- `SOT/CODE_CITY_LANDSCAPE.md:80` 2. Wire root state (`health`/`health_status`) in `orchestr8.py`.
- `SOT/CODE_CITY_LANDSCAPE.md:81` 3. Wire node-click bridge (`postMessage` -> `handle_node_click` path).
- `SOT/CODE_CITY_LANDSCAPE.md:83` 5. Add camera overview + warp dive + return stack.
- `SOT/CODE_CITY_LANDSCAPE.md:90` If a future run remembers only one file, it should remember this one: `SOT/CODE_CITY_LANDSCAPE.md`.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

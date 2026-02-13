# code_city_landscape_blind_integration_prd.txt Integration Guide

- Source: `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt`
- Total lines: `287`
- SHA256: `9e26f334452e024b06de4eccd36027987d865aaf0c2acc3e814624e51f0efb03`
- Memory chunks: `4`
- Observation IDs: `7..10`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:8` - Root health state in `orchestr8.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:9` - Node-click bridge into `handle_node_click()` in `IP/plugins/06_maestro.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:11` The result should be immediately task-generatable in Taskmaster and executable without recovering prior chat context.
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:32` Adds `health` and `health_status` to `STATE_MANAGERS` in `orchestr8.py` and keeps plugin compatibility.
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:36` Turns `WOVEN_MAPS_NODE_CLICK` browser events into reactive Python state updates and invokes `handle_node_click()`.
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:48` Implementation must preserve:
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:49` - Top row `[orchestr8] [collabor8] [JFDI]`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:51` - Emergence-only motion (no breathing/pulsing)
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:52` - Three-state color contract (`#D4AF37`, `#1fbdea`, `#9D4EDD`)
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:62` 3. Maestro receives event -> `handle_node_click()` executes
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:74` - App scope remains `orchestr8` only
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:88` - `orchestr8.py` currently defines `STATE_MANAGERS` with `root/files/selected/logs` only
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:90` - `IP/woven_maps.py` posts `WOVEN_MAPS_NODE_CLICK` with node payload
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:92` - `IP/plugins/06_maestro.py` defines `handle_node_click(node_data)`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:121` - `zoom: float`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:150` 1. Root health channels in `orchestr8.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:151` - Extend `STATE_MANAGERS` with:
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:158` - Existing plugins expecting previous keys must continue to render
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:160` 2. Node-click bridge into `handle_node_click()` in `IP/plugins/06_maestro.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:166` - Invoke `handle_node_click(...)` on valid payload
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:175` 4. On success, call `handle_node_click(validated_payload_dict)`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:187` - `orchestr8.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:188` - `IP/plugins/06_maestro.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:209` 1. Add `health` and `health_status` to `STATE_MANAGERS` in `orchestr8.py`
- `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:213` 1. `marimo run orchestr8.py` starts successfully

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

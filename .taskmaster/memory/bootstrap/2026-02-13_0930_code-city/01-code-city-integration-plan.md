# Code City Blind Integration Plan

- Source: `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt`
- Taskmaster status at capture: 10 tasks, 33 subtasks, 1 in-progress, 9 pending.

## Planned execution order

1. Task 1: Create `IP/contracts` package foundation.
2. Tasks 2/3/4/5: Implement schema + merge policy contracts (parallelizable after Task 1).
3. Task 6: Add unit tests for contracts.
4. Task 7: Root health state wiring in `orchestr8.py`.
5. Tasks 8/9: Node-click bridge and `woven_maps.py` merge integration (parallelizable after Task 7).
6. Task 10: Canonical acceptance checks.

## Critical findings

- JS->Python bridge gap: WOVEN_MAPS_NODE_CLICK is emitted in JS, but Python `handle_node_click()` is not invoked.
- Preferred bridge in marimo runtime: hidden `mo.ui.text` + `on_change` callback.
- `STATE_MANAGERS` in `orchestr8.py` needs explicit `health`/`health_status` channels.
- Existing contract style target: dataclass + `to_dict()` camelCase JSON serialization.

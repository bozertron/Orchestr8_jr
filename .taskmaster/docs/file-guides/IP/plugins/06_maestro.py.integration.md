# 06_maestro.py Integration Guide

- Source: `IP/plugins/06_maestro.py`
- Total lines: `1673`
- SHA256: `e7d7f76d1070f4d000b31085c3154adf4f72553235e10b37d1c99058eb568891`
- Role: **The Void runtime bridge hub** — routes Code City node/context handoff, camera navigation events, and connection result relay back into the panel surface

## Why This Is Painful

- Multiple bridge channels (node clicks, camera nav, connection results) share one monolithic plugin runtime.
- Context handoff now spans Carl context, BuildingPanel contract validation, and sitting-room transitions.
- JS relay script and Python state transitions must stay in sync on event names and payload shapes.

## Anchor Lines

- `IP/plugins/06_maestro.py:426` `build_code_city_context_payload(...)` handoff on node click
- `IP/plugins/06_maestro.py:1043` `process_camera_navigation(...)`
- `IP/plugins/06_maestro.py:1090` `camera_nav_bridge` hidden bridge state
- `IP/plugins/06_maestro.py:1261` `build_sitting_room()` runtime view
- `IP/plugins/06_maestro.py:1503` `relayConnectionResult()` iframe result relay
- `IP/plugins/06_maestro.py:1544` `WOVEN_MAPS_CAMERA_NAVIGATE` message bridge listener

## Integration Use

- Node click handling now stores normalized Code City context used by Summon/Collabor8 and Sitting Room views.
- Camera navigation events from the iframe route through hidden `camera_nav_bridge` input to Python handlers.
- Connection action result relay remains active for in-panel patchbay status/history updates.

## Open Gaps

- [ ] Signed/verified actor identity (role is currently declarative metadata)
- [ ] 2D/3D keyframe systems remain independent (single behavior contract pending)

# woven_maps_template.html Integration Guide

- Source: `IP/static/woven_maps_template.html`
- Total lines: `4910`
- SHA256: `98fb4667c416b63c3cd65efbbd41a313d3db20df4872543cb4a0bb0330c34b84`
- Role: **Code City iframe runtime template** — canvas interaction loop, bridge events, patchbay panel, and 2D/3D navigation controls

## Why This Is Painful

- Large inline JS/CSS surface makes small interaction fixes high-risk.
- Python bridge event names must stay perfectly aligned with `06_maestro.py`.
- Patchbay UX now spans selection, drag gesture, action dispatch, and result replay.

## Anchor Lines

- `IP/static/woven_maps_template.html:1657` `loadConnectionActionHistory()`
- `IP/static/woven_maps_template.html:1684` `pushConnectionActionHistory(...)`
- `IP/static/woven_maps_template.html:1912` `captureThreeCameraState()`
- `IP/static/woven_maps_template.html:1936` `applyThreeCameraState(...)`
- `IP/static/woven_maps_template.html:2484` `setViewMode(...)` with deferred 3D camera apply
- `IP/static/woven_maps_template.html:2800` `startRewireDrag(event)`
- `IP/static/woven_maps_template.html:2831` `handleRewireDrop(event)`
- `IP/static/woven_maps_template.html:4774` `WOVEN_MAPS_CONNECTION_RESULT` listener

## Integration Use

- Patchbay history is now persistent via `localStorage` key `orchestr8_patchbay_history_v1`.
- Dragging a path-row onto the rewire input sets the target and triggers a guarded dry-run.
- Connection result messages append to the persistent history and refresh the panel.
- Keyframe payload now captures/restores both 2D pan/zoom state and 3D camera pose/keyframe metadata.

## Open Gaps

- [ ] Interactive cross-browser viewport validation artifact still pending (Taskmaster #24)

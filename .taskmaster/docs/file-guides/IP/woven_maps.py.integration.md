# woven_maps.py Integration Guide

- Source: `IP/woven_maps.py`
- Total lines: `4070`
- SHA256: `0a9f75dd3a71291d4a74ac7c73a7edab11a4f0273432c8850d06088961475852`
- Role: **Code City renderer + patchbay panel UI** — emits actions with actor role, renders latest action result, and shows per-connection result history

## Why This Is Painful

- Connection panel now merges diagnostics, command dispatch, latest status, and history.
- UI permission + backend permission must remain consistent.
- Template remains a large JS/CSS bundle with many coupled states.

## Anchor Lines

- `IP/woven_maps.py:1274` apply enable flag injection
- `IP/woven_maps.py:2362` `renderConnectionActionResult(...)`
- `IP/woven_maps.py:2389` `renderConnectionActionHistory(...)`
- `IP/woven_maps.py:2417` actor role sourcing (`global`/`localStorage`/default)
- `IP/woven_maps.py:2459` apply button enabled/disabled branch
- `IP/woven_maps.py:2499` payload includes `actorRole`
- `IP/woven_maps.py:3818` result listener appends history
- `IP/woven_maps.py:3832` phase indicator updates from result

## Integration Use

- `actorRole` is emitted with every connection action.
- History is per-connection and capped (latest 5 shown, 40 retained in memory).
- Keep result rendering escaped (`escapeHtml`) to avoid injection from message payloads.

## Open Gaps

- [ ] Drag-to-rewire gesture (currently button-driven)
- [ ] Persist history across reloads/sessions

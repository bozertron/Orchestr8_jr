# connection_action_event.py Integration Guide

- Source: `IP/contracts/connection_action_event.py`
- Total lines: `107`
- SHA256: `31646c63c7bed448ad44559a3cffb2d98477152bb52c385997bbbf57b570df77`
- Role: **Edge action bridge schema** — validates connection-panel actions (`dry_run_rewire`, `apply_rewire`) and actor role metadata

## Why This Is Painful

- Action enum drift breaks UI->handler compatibility.
- Schema is now a safety gate for write-capable behavior and role gating.

## Anchor Lines

- `IP/contracts/connection_action_event.py:6` action enum includes `apply_rewire`
- `IP/contracts/connection_action_event.py:30` `actorRole` field on action envelope
- `IP/contracts/connection_action_event.py:73` actor role normalization in validator
- `IP/contracts/connection_action_event.py:101` example payload includes `actorRole`

## Integration Use

- Keep action enum + validator allowlist in sync.
- Treat `actorRole` as optional metadata with lowercased normalization.

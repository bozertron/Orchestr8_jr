# 06_maestro.py Integration Guide

- Source: `IP/plugins/06_maestro.py`
- Total lines: `2307`
- SHA256: `46938da17bbe489f576f087ff3e53efae190639531fdbef6ab2cebb330e95b80`
- Role: **The Void runtime bridge hub** — routes connection actions, enforces role-aware apply permissions, and relays structured results back to Code City

## Why This Is Painful

- Bidirectional bridge logic (ingress + result egress) is now tightly coupled.
- Apply writes are gated by both feature flag and role allowlist.
- Monolithic file structure increases regression blast radius.

## Anchor Lines

- `IP/plugins/06_maestro.py:500` connection action result state channel
- `IP/plugins/06_maestro.py:726` `emit_connection_action_result(...)`
- `IP/plugins/06_maestro.py:762` actor role derivation (`event.actorRole` + env fallback)
- `IP/plugins/06_maestro.py:871` apply feature flag guard (`ORCHESTR8_PATCHBAY_APPLY`)
- `IP/plugins/06_maestro.py:883` role allowlist guard (`ORCHESTR8_PATCHBAY_ALLOWED_ROLES`)
- `IP/plugins/06_maestro.py:1567` hidden result bridge input
- `IP/plugins/06_maestro.py:2145` relayConnectionResult() iframe broadcast

## Integration Use

- Apply requires both: feature enabled and actor role allowed.
- Keep result payload relay active for in-panel status updates.
- Keep contract validation as hard entry gate before any action handling.

## Open Gaps

- [ ] Signed/verified actor identity (role is currently declarative metadata)
- [ ] Persistent result history store beyond in-memory panel list

# Autonomy Boundary: P07-FC-02 (or8_founder_console)

## Objective

Advance the founder console from skeleton to active operations cockpit for packet tracking, unread guidance visibility, and rapid decision feedback.

## Allowed Work

- Extend FastAPI endpoints for packet-state and guidance observability.
- Add founder-action endpoints that log directives/checkpoints to shared memory.
- Add tests for new API routes.
- Produce canonical report with exact pass counts.

## Must Not Do

- Modify canonical project runtime code in `Orchestr8_jr`.
- Introduce destructive memory controls (no stop/restart orchestration commands).
- Bypass hard requirements or checkout protocol.

## Required Evidence

- New/updated endpoints for:
  - packet board summary endpoint at /api/v1/packets/summary
  - unread guidance/flags aggregation endpoint at /api/v1/flags/unread (enhanced)
  - founder directive log write endpoint at /api/v1/founder/directive
- Test command + pass count in report.
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-02_REPORT.md` with delivery proof.

## Required Validation

```bash
python -m pytest -v
```

## Unlock Authority

- Unlocked by: Codex (P07 orchestration)
- Effective: 2026-02-16

# Autonomy Boundary: P07-FC-05 (or8_founder_console)

## Objective

Implement founder workflow completion round: review bundle endpoint, decision audit export, and consistency checks for async pre-mayor annotation flow.

## Allowed Work

- Add review bundle and audit export API endpoints.
- Add tests for endpoint behavior and data consistency.
- Deliver canonical report with pass counts and proof.

## Must Not Do

- Modify Orchestr8_jr runtime code.
- Add destructive memory controls.

## Required Evidence

- `/home/bozertron/or8_founder_console/routers/review_bundle.py`
- `/home/bozertron/or8_founder_console/routers/audit_export.py`
- `/home/bozertron/or8_founder_console/tests/test_review_bundle.py`
- `/home/bozertron/or8_founder_console/tests/test_audit_export.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-05_REPORT.md`

## Required Validation

```bash
python -m pytest tests/ -v
```

## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16

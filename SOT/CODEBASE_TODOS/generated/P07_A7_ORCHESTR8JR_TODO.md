# orchestr8_jr TODO (P07/P07-A7)

Date: 2026-02-16
Mode: Long-run

## Objective

Run Wave-4 governance loop with auto-forward unlock prep and batch replay decisions.

## Scope

Canonical governance + autop-run packet compiler oversight

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| 1 | ACK Wave-4 checkouts and keep long-run windows active | none | ready | /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md |
| 2 | Replay all Wave-4 bundles and issue accept-rework matrix | 1 | ready | /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md |
| 3 | Publish Wave-5 unlock set using phase prep compiler | 2 | ready | /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md |

## Validation

```bash
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py tests/city/test_wiring_view.py tests/city/test_parity.py -q
```

## Ambiguity Log (No Assumptions)

Rules:
1. Add ambiguity line item.
2. Probe local facts once.
3. Probe cross-codebase facts once.
4. If still unresolved: `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 | Probe 2 | Outcome |
|---|---|---|---|---|
| 1 | none logged | n/a | n/a | n/a |

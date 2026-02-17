# or8_founder_console TODO (P07/P07-FC-06)

Date: 2026-02-16
Mode: Long-run

## Objective

Ship C2P Wave-4 MVP: observation sync + review queue for launch-ready packets.

## Scope

Founder tooling packet: comment ingestion + proposal queue

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| 1 | Implement scanner and unprocessed intent persistence | none | ready | /home/bozertron/or8_founder_console/services/intent_scanner.py |
| 2 | Implement review endpoints for approve-edit-launch | 1 | ready | /home/bozertron/or8_founder_console/routers/intent_queue.py |
| 3 | Run tests and publish canonical FC-06 report | 2 | ready | /home/bozertron/or8_founder_console/tests/test_intent_scanner.py |

## Validation

```bash
python -m pytest tests/ -v
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

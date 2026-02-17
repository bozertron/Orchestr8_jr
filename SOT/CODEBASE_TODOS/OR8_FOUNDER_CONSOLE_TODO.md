# or8_founder_console Comprehensive TODO

Last Updated: 2026-02-16  
Lane: Founder Tooling (`or8_founder_console`)  
Packet Focus: `P07-FC-04`

## Read First

1. `/home/bozertron/Orchestr8_jr/README.AGENTS`
2. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-04_OR8_FOUNDER_CONSOLE.md`
5. `SOT/CODEBASE_TODOS/OR8_FOUNDER_CONSOLE_TODO.md` (this file)

## Sprint Objective

Ship founder decision throughput improvements (annotation governance + timeline context + auditable exports) with full test evidence.

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| FC-01 | Implement annotation moderation controls | none | ready | `routers/annotations.py` + tests |
| FC-02 | Implement timeline decision filters and packet views | FC-01 | ready | `routers/timeline.py` + tests |
| FC-03 | Add founder review bundle endpoint | FC-02 | ready | endpoint code + integration tests |
| FC-04 | Add packet decision audit export endpoint | FC-03 | ready | export route + schema proof |
| FC-05 | Add endpoint tests for FC-04 scope | FC-04 | ready | passing `pytest` output |
| FC-06 | Add data consistency checks for review/audit paths | FC-05 | ready | test coverage and checks |
| FC-07 | Publish FC-04 canonical evidence report | FC-06 | ready | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md` |
| FC-08 | Draft FC-05 scope proposal | FC-07 | ready | proposal appendix in report |

## Required Validation

```bash
python -m pytest tests/ -v
```

Record exact command output and pass counts.

## Delivery Contract

Update canonical report:

```bash
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md
```

## Ambiguity Log (No Assumptions)

If anything is unclear:
1. Add one row below.
2. Perform two hard-fact probes max.
3. If unresolved, mark `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 (local facts) | Probe 2 (cross-lane facts) | Outcome |
|---|---|---|---|---|
| FC-XX |  |  |  |  |


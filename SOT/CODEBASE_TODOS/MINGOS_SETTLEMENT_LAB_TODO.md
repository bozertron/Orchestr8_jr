# mingos_settlement_lab Comprehensive TODO

Last Updated: 2026-02-16  
Lane: Settlement/Visual Specs (`mingos_settlement_lab`)  
Packet Focus: `P07-MSL-05` production UI constraints + synthesis

## Read First

1. `/home/bozertron/Orchestr8_jr/README.AGENTS`
2. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-04_MINGOS_SETTLEMENT_LAB.md`
5. `SOT/CODEBASE_TODOS/MINGOS_SETTLEMENT_LAB_TODO.md` (this file)

## Sprint Objective

Convert settlement outputs into strict implementation-grade test/matrix/handoff artifacts consumed without ambiguity by `a_codex_plan` and canonical replay.

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| MSL-01 | Refine test-hook coverage across active module domains | none | complete | updated `MSL_04_TEST_HOOKS.md` |
| MSL-02 | Tighten acceptance matrix strictness and evidence mapping | MSL-01 | complete | updated `MSL_04_ACCEPTANCE_MATRIX.md` |
| MSL-03 | Cross-link matrix criteria to B5/C5/FC-04 packet outputs | MSL-02 | complete | traceability table with packet IDs |
| MSL-04 | Publish direct implementation handoff notes for `a_codex_plan` | MSL-03 | complete | handoff section with file/contract pointers |
| MSL-05 | Publish canonical `MSL-04_REPORT.md` update with delivery-proof text | MSL-04 | complete | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-04_REPORT.md` |
| MSL-06 | Draft MSL-05 support packet from latest integration findings | MSL-05 | complete | draft section appended to report |
| MSL-07 | Synthesize Wave-2 integration logs into UI constraint logic | MSL-06 | complete | `MSL_05_UI_CONSTRAINTS_PACKET.md` |
| MSL-08 | Map Aesthetic Reference variables to production Handoff | MSL-07 | complete | `MSL_05_INTEGRATION_HANDOFF.md` |
| MSL-09 | Publish canonical `MSL-05_REPORT.md` with full traceability | MSL-08 | complete | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-05_REPORT.md` |
| MSL-10 | Draft Wave-4 / P08 promotion criteria | MSL-09 | complete | appended to MSL-05 report |

## Required Source Inputs

- `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html`
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_04_TEST_HOOKS.md`
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_04_ACCEPTANCE_MATRIX.md`

## Delivery Contract

Update canonical report:

```bash
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-04_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-04_REPORT.md
```

## Ambiguity Log (No Assumptions)

If anything is unclear:

1. Add one row below.
2. Perform two hard-fact probes max.
3. If unresolved, mark `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 (local facts) | Probe 2 (cross-lane facts) | Outcome |
|---|---|---|---|---|
| MSL-XX |  |  |  |  |

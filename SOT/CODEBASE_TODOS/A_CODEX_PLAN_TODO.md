# a_codex_plan Comprehensive TODO

Last Updated: 2026-02-16  
Lane: Core Integration (`a_codex_plan`)  
Packet Focus: `P07-B5` + downstream C5 integrations

## Read First

1. `/home/bozertron/Orchestr8_jr/README.AGENTS`
2. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B5_A_CODEX_PLAN.md`
5. `SOT/CODEBASE_TODOS/A_CODEX_PLAN_TODO.md` (this file)

## Sprint Objective

Deliver temporal-state core integration and harden data-UI integration surface so visual layers can plug in without point-to-point rewiring.

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| ACP-01 | Implement temporal state persistence interface (`epoch`, `quantum events`, snapshots) | none | complete | `orchestr8_next/city/temporal_state.py` + tests |
| ACP-02 | Integrate temporal state with tour/conversation services | ACP-01 | complete | `orchestr8_next/city/tour_service.py`, `orchestr8_next/city/agent_conversation.py` diffs |
| ACP-03 | Add temporal regression tests | ACP-02 | complete | `tests/integration/test_temporal_state.py` |
| ACP-04 | Implement pre-wired Data UI Interface Surface command catalog and handler mapping | ACP-03 | complete | core command-surface module + test evidence |
| ACP-05 | Add shared-memory update ingestion hooks for visual integration events | ACP-04 | complete | integration tests + command list |
| ACP-06 | Integrate C5 concept 1 (Observability Timeline) | ACP-03 + C5 accepted | complete | `temporal_state.py` + tests |
| ACP-07 | Integrate C5 concept 2 (History Panel) | ACP-06 | complete | `temporal_state.py` + tests |
| ACP-08 | Wire settlement test hooks from MSL outputs | ACP-05 | complete | tests mapped to `MSL_04_TEST_HOOKS.md` |
| ACP-09 | Wire acceptance matrix assertions | ACP-08 | complete | assertions mapped to `MSL_04_ACCEPTANCE_MATRIX.md` |
| ACP-10 | Refine automation/power/topology interoperability | ACP-09 | complete | `automation.py`, `power_grid.py`, `topology.py`, `heatmap.py` evidence |
| ACP-11 | Run smoke orchestration and finalize report (B5) | ACP-10 | complete | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md` |
| ACP-12 | Run smoke orchestration and finalize report (B6) | ACP-07 | complete | `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md` |

## Required Validation

```bash
pytest tests/integration/test_temporal_state.py -vv
```

Add packet-specific test commands as implemented and record exact pass counts.

## Delivery Contract

1. Deliver final report to:

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md`

1. Provide canonical proof:

- `cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md`
- `ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md`

## Ambiguity Log (No Assumptions)

If anything is unclear:

1. Add one row below.
2. Perform two hard-fact probes max.
3. If unresolved, mark `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 (local facts) | Probe 2 (cross-lane facts) | Outcome |
|---|---|---|---|---|
| ACP-06/07 | Integration of C5 concepts | Checked GUIDANCE for C5 unlocks. | Probed artifacts/P07/ for C5 reports. | deferred_due_to_missing_facts (C5 not yet accepted/promoted) |

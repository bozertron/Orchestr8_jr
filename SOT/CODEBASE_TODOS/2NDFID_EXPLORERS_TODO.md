# 2ndFid_explorers Comprehensive TODO

Last Updated: 2026-02-16  
Lane: Extraction (`2ndFid_explorers`)  
Packet Focus: `P07-C6`

## Read First

1. `/home/bozertron/Orchestr8_jr/README.AGENTS`
2. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C6_2NDFID_EXPLORERS.md`
5. `SOT/CODEBASE_TODOS/2NDFID_EXPLORERS_TODO.md` (this file)

## Sprint Objective

Produce two high-value, licensing-safe C6 extraction packets (operator decision throughput and state explainability) that are immediately consumable by `a_codex_plan`.

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| C6-01 | Kickoff: preflight + checkout + bootstrap + lint | none | complete | checkout ack + worklist + lint pass |
| C6-02 | Select two C6 candidate systems | C6-01 | complete | candidate list with source paths and rationale |
| C6-03 | Produce packet `P07_C6_01_*` | C6-02 | complete | canonical artifact file |
| C6-04 | Produce packet `P07_C6_02_*` | C6-03 | complete | canonical artifact file |
| C6-05 | Run licensing and provenance risk pass | C6-04 | complete | explicit risk class + licensing flag for both packets |
| C6-06 | Map target contracts for `a_codex_plan` | C6-05 | complete | contract mapping section in both packets |
| C6-07 | Deliver canonical artifacts with proof | C6-06 | complete | `cp` + `ls -l` proof |
| C6-08 | Closeout: run script + ping | C6-07 | complete | closeout pass + completion ping |

## Required Artifact Targets

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_01_*.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_02_*.md`

Each packet must include:

- source provenance
- concept summary
- orchestr8/code-city value
- clean-room implementation plan
- target contracts for `a_codex_plan`
- risk class and licensing status

## Delivery Contract

For each packet:

```bash
cp <lane_packet> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/<packet_name>.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/<packet_name>.md
```

## Ambiguity Log (No Assumptions)

If anything is unclear:

1. Add one row below.
2. Perform two hard-fact probes max.
3. If unresolved, mark `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 (local facts) | Probe 2 (cross-lane facts) | Outcome |
|---|---|---|---|---|
| C6-XX |  |  |  |  |

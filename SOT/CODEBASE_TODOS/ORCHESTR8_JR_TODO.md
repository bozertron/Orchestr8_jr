# Orchestr8_jr Comprehensive TODO

Last Updated: 2026-02-16  
Lane: Canonical Governance + Runtime (`Orchestr8_jr`)  
Packet Focus: `P07-A5` (COMPLETE)

## Read First

1. `README.AGENTS`
2. `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A5_ORCHESTR8JR.md`
5. `SOT/CODEBASE_TODOS/ORCHESTR8_JR_TODO.md` (this file)

## Sprint Objective

Keep all lanes moving in parallel while maintaining canonical replay authority and reducing integration ambiguity across Code City interfaces.

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| OR8-01 | Create `A5_ACTIVE_GOVERNANCE_REPORT.md` with Wave-2 replay/decision matrix | none | **COMPLETE** | `.planning/orchestr8_next/artifacts/P07/A5_ACTIVE_GOVERNANCE_REPORT.md` |
| OR8-02 | Reconcile `STATUS.md`, worklists, and closeout truth for B5/C5/FC-04/MSL-04 | OR8-01 | **COMPLETE** | STATUS.md updated 2026-02-16 |
| OR8-03 | Resolve C5 canonical state: accept with artifacts or explicit blocker decision | OR8-02 | **COMPLETE** | C5 ACCEPTED in Wave-2 batch |
| OR8-04 | Refresh stale SOT execution status docs to match live P07 posture | OR8-02 | **COMPLETE** | `SOT/CODEBASE_ROADMAP_CANONICAL.md` updated |
| OR8-05 | Add repeatable Code City acceptance gate command set | OR8-04 | **COMPLETE** | Baseline: 11 passed (reliability) + 8 passed (city) |
| OR8-06 | Define/lock event contract for node click bridge and camera state handoff | OR8-05 | **COMPLETE** | `A5_NODE_CLICK_CAMERA_CONTRACT.md` |
| OR8-07 | Generate next unlock batch based on completed lane bundles | OR8-03 | **COMPLETE** | `A5_WAVE3_UNLOCK_GUIDANCE.md` prepared |

## Strategic Runtime Backlog (Execute If OR8-01..05 Stable)

| ID | Task | Status | Evidence |
|---|---|---|---|
| OR8-ENG-01 | GPU telemetry and performance thresholds (`frame_time`, `particle_count`, `dispatch_load`) | ready | telemetry capture + thresholds |
| OR8-ENG-02 | Visual-contract + behavior acceptance automation | ready | automated gate run output |
| OR8-ENG-03 | Neighborhood/town-square/lock-overlay contract verification | ready | contract checks with pass/fail output |

## Canonical Replay Baseline

Use these at minimum where scope applies:

```bash
# Core reliability
pytest tests/reliability/test_reliability.py -q

# Code City baseline (8 tests)
pytest tests/city/test_binary_payload.py tests/city/test_parity.py tests/city/test_wiring_view.py -v

# Integration tests (as needed by packet scope)
pytest tests/integration/test_graphs.py -vv
pytest tests/integration/test_temporal_state.py -vv
pytest tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
```

### Baseline Pass Counts

| Suite | Pass Count |
|-------|------------|
| Reliability | 11 passed |
| Code City | 8 passed |
| Integration (temporal_state) | 3 passed |
| Integration (tour/conversation) | 4 passed |

## Ambiguity Log (No Assumptions)

If anything is unclear:
1. Add one row below.
2. Perform two hard-fact probes max.
3. If unresolved, mark `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 (local facts) | Probe 2 (cross-lane facts) | Outcome |
|---|---|---|---|---|
| OR8-XX |  |  |  |  |


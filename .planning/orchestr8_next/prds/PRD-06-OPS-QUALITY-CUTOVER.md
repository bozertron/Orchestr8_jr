# PRD P06: Quality Gates, Operations, and Cutover

## Phase

- ID: `P06`
- Name: Quality Gates, Operations, and Cutover
- Goal: Validate orchestr8_next for daily reliability and promote it to canonical runtime path.

## In Scope

- End-to-end test suite and regression pack
- Operational runbooks and incident response notes
- Cutover checklist and rollback plan
- Performance and reliability thresholds

## Out of Scope

- net-new product features
- exploratory R&D not tied to cutover

## Functional Requirements

- FR-06-01: Full lower-fifth interaction suite passes.
- FR-06-02: Adapter failure isolation validated end-to-end.
- FR-06-03: Code City mode and chat mode both stable.
- FR-06-04: Check-in protocol operational for all active workstreams.
- FR-06-05: No open P0 debt remains in `CODE_CITY_DEEP_FIX_QUEUE.md` before cutover.

## Non-Functional Requirements

- NFR-06-01: Startup success rate target met.
- NFR-06-02: Latency SLOs for key control actions met.
- NFR-06-03: Error budgets and telemetry alerts configured.

## Cutover Plan

1. Freeze legacy feature changes.
2. Run final gate suite on orchestr8_next.
3. Capture baseline metrics.
4. Enable orchestr8_next feature flag for pilot users.
5. Observe and collect incident data.
6. Promote to default runtime.
7. Keep rollback window open for one cycle.

## Rollback Triggers

- critical control pathway failure
- repeated startup failure above threshold
- uncontained adapter fault propagation

## Files (Target)

- `orchestr8_next/tests/`
- `orchestr8_next/ops/RUNBOOK.md`
- `orchestr8_next/ops/CUTOVER_CHECKLIST.md`
- `orchestr8_next/ops/ROLLBACK_PLAN.md`
- `.planning/orchestr8_next/artifacts/` (gate evidence)

## Acceptance Criteria

1. All phase gates P00-P05 have evidence artifacts.
2. Reliability and performance thresholds pass.
3. Cutover + rollback rehearsals completed.
4. Canonical runtime toggle documented and reversible.
5. `P0` lane in `.planning/orchestr8_next/execution/CODE_CITY_DEEP_FIX_QUEUE.md` is fully green.

## Risks

- R-06-01: Hidden dependencies on legacy paths discovered late.
- R-06-02: Incomplete incident tooling slows diagnosis.

## Mitigations

- M-06-01: pre-cutover dependency audit
- M-06-02: mandatory runbook drills

## Exit Gate `G-P06`

Required evidence:
- full regression report
- performance/SLO report
- cutover rehearsal report
- rollback rehearsal report
- deep-fix queue status report (`P0` complete)

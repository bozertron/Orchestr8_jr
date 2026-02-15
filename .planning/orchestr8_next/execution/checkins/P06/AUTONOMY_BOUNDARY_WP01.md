# P06 Autonomy Boundary Packet (WP01)

Date: 2026-02-15
Author: Codex
Scope: External builder lane only (P06 startup)

## Goal

Execute `P06-WP01` (regression + reliability harness) with evidence suitable for `G-P06` review.

## Authority Window

Builder is authorized to execute only `P06-WP01` (steps `251-260`) until further notice.

## Allowed Scope

1. Build/organize regression test harness for orchestr8_next quality gates.
2. Add reliability checks for startup, core controls, and adapter-failure isolation.
3. Produce initial reliability test report artifact for P06.
4. Update P06 check-in artifacts (`STATUS.md`, `BLOCKERS.md`) with command + result evidence.

## File Scope (Allowed)

- `orchestr8_next/tests/*` (new or updated quality-gate tests)
- `orchestr8_next/ops/RUNBOOK.md` (only sections tied to WP01 execution)
- `.planning/orchestr8_next/artifacts/P06/*` (test reports/evidence)
- `.planning/orchestr8_next/execution/checkins/P06/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P06/BLOCKERS.md`

## Hard No-Go Zones

1. No net-new feature work.
2. No cutover/rollback execution yet (that is `WP02`).
3. No broad architecture refactors.
4. No changes to core shell behavior unless required to fix a test-detected defect and explicitly documented.

## Required Deliverables Before Any Expansion

1. Regression harness command set documented and executable.
2. Reliability run report with pass/fail totals and known failure taxonomy.
3. Adapter failure-isolation validation evidence.
4. Updated STATUS/BLOCKERS with exact commands and outputs summary.

## Stop Conditions (Must Pause and Request Guidance)

1. Any work needed outside allowed file scope.
2. Blocker requiring cutover/rollback rehearsal before WP01 evidence is complete.
3. Repeated critical test failure with unknown root cause after one mitigation attempt.

## Completion Definition For Autonomy Window

Autonomy window completes when `P06-WP01` evidence is submitted and reviewed. No automatic authority expansion after completion.

# P06 Autonomy Boundary Packet (WP02)

Date: 2026-02-15
Author: Codex
Scope: External builder lane only (after WP01 acceptance)

## Goal

Execute `P06-WP02` cutover + rollback rehearsal with deterministic evidence and zero net-new feature scope.

## Authority Window

Builder is authorized to execute only `P06-WP02` (steps `261-270`) until further notice.

## Allowed Scope

1. Build and run cutover rehearsal checklist.
2. Build and run rollback rehearsal checklist.
3. Capture timings, failure points, and recovery validation.
4. Update operational docs needed for rehearsal reproducibility.
5. Update P06 check-in artifacts (`STATUS.md`, `BLOCKERS.md`) with command + result evidence.

## File Scope (Allowed)

- `orchestr8_next/ops/CUTOVER_CHECKLIST.md`
- `orchestr8_next/ops/ROLLBACK_PLAN.md`
- `orchestr8_next/ops/RUNBOOK.md` (rehearsal sections only)
- `.planning/orchestr8_next/artifacts/P06/*` (cutover/rollback reports)
- `.planning/orchestr8_next/execution/checkins/P06/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P06/BLOCKERS.md`

## Hard No-Go Zones

1. No net-new product features.
2. No broad architecture refactors.
3. No contract schema redesign unrelated to rehearsal findings.
4. No phase structure changes.

## Required Deliverables Before Any Expansion

1. Cutover rehearsal report with exact command/procedure transcript.
2. Rollback rehearsal report with trigger criteria and observed recovery behavior.
3. Updated runbook entries for rehearsal repeatability.
4. STATUS/BLOCKERS update with gate recommendation (`green|yellow|red`).

## Stop Conditions (Must Pause and Request Guidance)

1. Need for changes outside allowed file scope.
2. Rehearsal uncovers critical failure without viable rollback.
3. Repeated nondeterministic cutover behavior after one mitigation attempt.

## Completion Definition For Autonomy Window

Autonomy window completes when `P06-WP02` evidence is submitted and reviewed. No automatic authority expansion after completion.

# P05 Autonomy Boundary Packet (WP03)

Date: 2026-02-15
Author: Codex
Scope: External builder lane only (after WP02 acceptance)

## Goal

Close `P05` with parity validation and promotion-ready evidence for the WP01/WP02 City stack.

## Authority Window

Builder is authorized to execute only `P05-WP03` (steps `241-250`) until further notice.

## Allowed Scope

1. Produce parity report comparing:
   - 3D `WIDGET` path
   - 3D `IFRAME` fallback path
   - 2D Wiring View path
2. Add/adjust tests needed for parity assertions and regression protection.
3. Produce promotion memo for P05 gate review.
4. Update P05 check-in artifacts (`STATUS.md`, `BLOCKERS.md`) with command + result evidence.

## File Scope (Allowed)

- `tests/city/*` (parity/regression tests only)
- `orchestr8_next/city/notebook.py` (only minimal fixes needed for parity tests)
- `orchestr8_next/city/wiring.py` (only bugfixes if parity tests expose defects)
- `orchestr8_next/city/widget.py` (only bugfixes if parity tests expose defects)
- `.planning/orchestr8_next/execution/checkins/P05/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P05/BLOCKERS.md`
- `.planning/orchestr8_next/artifacts/P05/*` (parity report + promotion memo)

## Hard No-Go Zones

1. No new feature lanes outside parity/promotion evidence.
2. No core shell/lower-fifth changes.
3. No phase structure or PRD renaming.
4. No runtime dependency on `marimo new` / AI codegen path.

## Required Deliverables Before Any Expansion

1. Parity test run summary with exact commands + pass counts.
2. Explicit fallback behavior confirmation (IFRAME still operational).
3. P05 promotion memo with decision: promote / hold / rollback.
4. Updated STATUS and BLOCKERS reflecting final gate state recommendation.

## Stop Conditions (Must Pause and Request Guidance)

1. Need for non-bugfix changes outside allowed file scope.
2. Parity failure with unclear root cause after one mitigation attempt.
3. Any requirement to remove fallback path.

## Completion Definition For Autonomy Window

Autonomy window completes when `P05-WP03` evidence is submitted and reviewed. No automatic authority expansion after completion.

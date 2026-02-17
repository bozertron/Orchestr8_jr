# Autonomy Boundary: P07-A4 (orchestr8_jr canonical lane)

## Objective

Run active multi-lane governance while all packets execute in parallel, including replay validation and accept/rework decisions.

## Allowed Work

- Intake and replay validation for B3, C3, FC-02, MSL-02.
- Update canonical status, guidance, and blockers on every decision point.
- Issue corrective guidance and unlock follow-up packets.
- Maintain visual lock and runtime contract integrity.

## Must Not Do

- Skip replay validation before accept/rework.
- Allow non-canonical artifact paths to pass acceptance.
- Pause all lanes without a blocker-level reason.

## Required Evidence

- `.planning/orchestr8_next/artifacts/P07/A4_ACTIVE_GOVERNANCE_REPORT.md`
- replay command log + pass counts per packet intake
- decision matrix (accept/rework) for each packet
- memory observation IDs for each guidance/ack cycle

## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16

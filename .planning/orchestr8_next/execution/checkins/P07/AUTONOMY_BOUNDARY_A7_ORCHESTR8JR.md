# Autonomy Boundary: P07-A7 (orchestr8_jr)

## Objective

Run Wave-4 governance loop with auto-forward unlock prep and batch replay decisions.

## Scope

Canonical governance + autop-run packet compiler oversight

## Allowed Work

- Monitor and ACK all Wave-4 checkouts
- Batch intake/replay accept-rework for Wave-4 bundles
- Generate Wave-5 unlock artifacts without parking lanes

## Must Not Do

- Pause lane flow for routine micro-checkins
- Accept packets without replay evidence and closeout proof

## Required Evidence

- /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md

## Required Validation

```bash
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py tests/city/test_wiring_view.py tests/city/test_parity.py -q
```
## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16

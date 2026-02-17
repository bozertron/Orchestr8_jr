# P05 Autonomy Boundary Packet

Date: 2026-02-14
Author: Codex
Scope: External builder lane only (not this local canonical runtime path)

## Goal

Allow independent progress on P05 without architectural drift, hidden refactors, or cutover risk.

## Authority Window

Builder is authorized to execute only `P05-WP01` (steps `221-230`) until further notice.

## Allowed Scope

1. Implement binary payload hardening for Code City widget lane.
2. Keep dual render mode available (`WIDGET` primary, `IFRAME` fallback).
3. Add or update tests only for P05-WP01 acceptance criteria.
4. Update P05 check-in artifacts (`STATUS.md`, `BLOCKERS.md`) with command + result evidence.

## File Scope (Allowed)

- `orchestr8_next/city/widget.py`
- `orchestr8_next/city/notebook.py`
- `orchestr8_next/city/bridge.py` (only if needed for payload/chunk metadata)
- `orchestr8_next/city/contracts.py` (only additive/compatible changes)
- `tests/city/*`
- `.planning/orchestr8_next/execution/checkins/P05/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P05/BLOCKERS.md`

## Hard No-Go Zones

1. No edits to core Orchestr8 runtime shell or lower-fifth flow.
2. No rename/restructure of phase folders, PRDs, or packet IDs.
3. No dependency on `marimo new` / AI codegen path at runtime.
4. No silent fallback removal; `IFRAME` rollback path must remain.
5. No broad refactors outside listed file scope.

## Required Deliverables Before Any Expansion

1. `traitlets.Bytes` transport for large payload path.
2. Deterministic chunking metadata:
   - `payload_id`
   - `chunk_index`
   - `chunk_total`
3. Explicit max payload guardrail with clear error surface.
4. Passing tests for:
   - under-threshold payload
   - over-threshold chunked payload
   - malformed chunk sequence rejection
5. Status evidence with exact test command + pass counts.

## Stop Conditions (Must Pause and Request Guidance)

1. Any change needed outside allowed file scope.
2. Any breaking contract change in bridge/events schema.
3. Any inability to preserve `WIDGET` + `IFRAME` dual-path.
4. Any runtime path that requires browser-only validation with no host-access proof.
5. Any blocker older than one check-in cycle without mitigation.

## Reporting Contract

Every update must include:

1. Gate color (`green|yellow|red`) and percent complete.
2. What changed (file list + short purpose).
3. Exact validation commands run.
4. Pass/fail totals.
5. Next three actions.

## Completion Definition For Autonomy Window

Autonomy window completes when `P05-WP01` is fully evidenced and reviewed. No automatic authority expansion after completion; await next architect packet.

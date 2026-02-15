# P05 Autonomy Boundary Packet (WP02)

Date: 2026-02-15
Author: Codex
Scope: External builder lane only (after WP01 acceptance)

## Goal

Deliver Wiring View integration as a contained `P05-WP02` slice without destabilizing the WP01 binary payload lane.

## Authority Window

Builder is authorized to execute only `P05-WP02` (steps `231-240`) until further notice.

## Allowed Scope

1. Implement a 2D Wiring View module (Pyvis or D3-backed) in city lane.
2. Expose Wiring View in `notebook.py` using tabbed or equivalent layout.
3. Preserve existing `CodeCityWidget` (`WIDGET`) and `IFRAME` fallback behavior.
4. Add focused tests for wiring rendering/data contracts.
5. Update P05 check-in artifacts (`STATUS.md`, `BLOCKERS.md`) with command + result evidence.

## File Scope (Allowed)

- `orchestr8_next/city/wiring.py`
- `orchestr8_next/city/notebook.py`
- `orchestr8_next/city/contracts.py` (only additive/compatible changes)
- `tests/city/test_wiring_view.py` (or equivalent city wiring tests)
- `.planning/orchestr8_next/execution/checkins/P05/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P05/BLOCKERS.md`

## Hard No-Go Zones

1. No edits to core Orchestr8 runtime shell or lower-fifth flow.
2. No broad refactors in widget binary payload path (`WP01`) unless blocker-level bugfix.
3. No rename/restructure of phase folders, PRDs, or packet IDs.
4. No runtime dependency on `marimo new` / AI codegen path.

## Required Deliverables Before Any Expansion

1. Wiring View renders valid 2D relationship graph from contract data.
2. Notebook exposes user-selectable switch (tabs or equivalent) between 3D city and 2D wiring.
3. `WIDGET` + `IFRAME` paths remain intact for Code City.
4. Tests pass for wiring view basics and payload contract sanity.
5. Status evidence includes exact commands + pass counts.

## Stop Conditions (Must Pause and Request Guidance)

1. Any change needed outside allowed file scope.
2. Any breaking contract change in existing city bridge/events schema.
3. Any attempted replacement/removal of WP01 payload mechanism.
4. Any blocker older than one check-in cycle without mitigation.

## Completion Definition For Autonomy Window

Autonomy window completes when `P05-WP02` is fully evidenced and reviewed. No automatic authority expansion after completion; await next architect packet.

# Code City Aggregated TODO

Last Updated: 2026-02-16
Owner: Mayor + Founder
Purpose: single execution queue for Code City work across all lanes.

## Source Inputs

- `SOT/todo.md`
- `SOT/CODE_CITY_LANDSCAPE.md`
- `SOT/CODE_CITY_PLAN_LOCK.md`
- `SOT/CODE_CITY_UI_CONTRACT.md`
- `.planning/orchestr8_next/execution/CODE_CITY_DEEP_FIX_QUEUE.md`
- `.planning/mvp/taskmaster/*.tasks.json`
- `.planning/orchestr8_next/execution/checkins/P07/*`

## Status Legend

- `ready`: can execute now.
- `blocked`: waiting on explicit dependency.
- `in_reconcile`: evidence/docs disagree and must be normalized first.
- `batch_closeout`: execute at long-run window close, not during active implementation flow.

## Canonical Reconciliation (Orchestr8_jr)

1. `CC-OR8-01` (`batch_closeout`): create `A5_ACTIVE_GOVERNANCE_REPORT.md` and align Wave-2 accept/rework records.
2. `CC-OR8-02` (`batch_closeout`): reconcile `STATUS.md`, worklists, and packet closeout checkboxes for `B5`, `FC-04`, `MSL-04`.
3. `CC-OR8-03` (`batch_closeout`): either deliver C5 canonical artifacts or record explicit C5 blocker decision.
4. `CC-OR8-04` (`ready`): refresh stale SOT status docs to reflect live P07 posture and active lanes.
5. `CC-OR8-05` (`ready`): add repeatable Code City acceptance gate commands (contract tests + perf sanity).

## Core Integration (`a_codex_plan`)

1. `CC-B-00` (`ready`): implement pre-wired `Data UI Interface Surface` (command catalog + reactive handler surface + memory update ingestion).
2. `CC-B-01` (`ready`): temporal state persistence interface.
3. `CC-B-02` (`ready`): temporal state hooks into tour/conversation flow.
4. `CC-B-03` (`ready`): temporal regression tests (edge/state transitions).
5. `CC-B-04` (`blocked` by `CC-C-02/03`): integrate C5 concept 1.
6. `CC-B-05` (`blocked` by `CC-C-02/03`): integrate C5 concept 2.
7. `CC-B-06` (`ready`): wire MSL test hooks and acceptance-matrix assertions.
8. `CC-B-07` (`ready`): smoke orchestration script + canonical report updates.

## Extraction (`2ndFid_explorers`)

1. `CC-C-01` (`ready`): select two C5 candidate systems (timeline/inspection).
2. `CC-C-02` (`ready`): produce `P07_C5_01_*.md`.
3. `CC-C-03` (`ready`): produce `P07_C5_02_*.md`.
4. `CC-C-04` (`ready`): licensing risk pass for both C5 packets.
5. `CC-C-05` (`ready`): map contracts/hand-off notes for `a_codex_plan`.
6. `CC-C-06` (`ready`): canonical delivery proof + completion ping.

## Settlement/Visual Specs (`mingos_settlement_lab`)

1. `CC-MSL-01` (`ready`): refine test-hook coverage by module.
2. `CC-MSL-02` (`ready`): tighten acceptance matrix strictness and evidence map.
3. `CC-MSL-03` (`ready`): cross-link matrix criteria to active packet outputs.
4. `CC-MSL-04` (`ready`): publish updated `MSL-04_REPORT.md` with complete delivery-proof text.
5. `CC-MSL-05` (`ready`): produce static-dashboard transfer packet from:
   - `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html`

## Founder Console (`or8_founder_console`)

1. `CC-FC-01` (`ready`): annotation moderation controls.
2. `CC-FC-02` (`ready`): timeline decision filters.
3. `CC-FC-03` (`ready`): founder review bundle endpoint.
4. `CC-FC-04` (`ready`): packet decision audit export.
5. `CC-FC-05` (`ready`): endpoint tests + data consistency checks.
6. `CC-FC-06` (`ready`): publish FC-04 evidence and FC-05 scope proposal.

## High-Value Runtime Backlog (Code City Engine)

1. `CC-ENG-01` (`ready`): validate sustained 1M particle runtime on current machine profile.
2. `CC-ENG-02` (`ready`): add GPU telemetry (`frame_time`, `particle_count`, `dispatch_load`).
3. `CC-ENG-03` (`ready`): formalize neighborhood grouping and building-panel data contract verification.
4. `CC-ENG-04` (`ready`): add acceptance automation for visual-contract + behavior gates.
5. `CC-ENG-05` (`ready`): evaluate and gate advanced effect modes (short-edge threshold, ping-pong/FBO, curl, wave interference, emergence phase machine) behind feature flags.

## Execution Constraints

1. Keep all five lanes actively developing in parallel unless a blocker is explicitly declared.
2. Use long-run windows:
- one kickoff per lane
- uninterrupted build window
- one end-of-window evidence bundle per lane
3. Mid-window comms are blocker-only or safety-only.
4. End-of-window bundles must include canonical artifact paths, exact commands, pass counts, observation IDs, and closeout results.
5. Mayor performs batch replay and returns consolidated rework lists after bundle intake.

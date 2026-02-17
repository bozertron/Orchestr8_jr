# Canonical Codebase Roadmap

Last Updated: 2026-02-16
Owner: Mayor + Founder
Purpose: one execution roadmap per codebase with enough guardrails to prevent drift and enough autonomy to keep velocity.

## Founder Directive: Auto-Forward Long Runs

Effective now:
1. Default posture is one-shot long-run execution windows, not micro-coordination.
2. If a task is likely to produce meaningful value within ~2 hours, include it in active wave scope.
3. Maintain a large forward roadmap so rails remain visible even when details evolve.

Primary roadmap reference for this mode:
- `SOT/MVP_AUTOFORWARD_MASTER_ROADMAP.md`
- `SOT/PLATFORM_TARGET_DESKTOP_LINUX.md`
- `SOT/APP_FIRST_TAURI_READY_PLAN.md`
- Wave-4 execution package spec:
  - `SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WAVE4_AUTORUN.toml`
- Wave-4 launch prompt pack:
  - `SOT/CODEBASE_TODOS/LAUNCH_PROMPTS_P07_WAVE4_LONGRUN.md`

## Founder Directive Addendum: Desktop Linux Target Lock

Effective now:
1. MVP platform target is desktop Linux (`x86_64`) with fullscreen high-resolution operation.
2. Android/tablet/mobile-specific build targets are out of scope unless explicitly unlocked.
3. Runtime posture remains marimo-first with `WIDGET` primary render mode and tested `IFRAME` rollback.
4. Performance planning must prioritize GPU-accelerated rendering paths and replay-safe fallbacks.
5. Upstream marimo planning references are pinned under:
- `third_party_refs/marimo_docs_upstream_main_20260216/docs/`
- `third_party_refs/marimo_docs_upstream_main_20260216/SOURCE_PIN.txt`

## Operating Rules (Anti-Yolo, Anti-Bureaucracy)

1. One active queue per codebase. No duplicate trackers.
2. Every queued item must name one owner lane and one delivery artifact path.
3. Acceptance is replay + evidence, not narrative.
4. If blocked, write one blocker line with decision needed; otherwise keep moving.
5. Keep launch prompts short, but always run lint/closeout against resume prompts that contain full hard requirements.
6. All five lanes should be actively developing something at the same time unless explicitly blocked.
7. Preserve packets/tokens/proof assets, but submit them in end-of-run bundles instead of micro-checkins.

## Cadence Mode: Long-Run Batch Submission

1. Start-of-window:
- one checkout + worklist + lint per lane.
- one declared implementation window (`LONG_RUN_WINDOW_ID`).
2. In-window:
- uninterrupted development by each lane.
- no routine back-and-forth messages; only blocker/safety escalations.
3. End-of-window:
- each lane submits one bundle: artifacts, exact commands, pass counts, memory observation IDs, closeout output.
4. Mayor intake:
- replay evidence in batch.
- issue consolidated `accept`/`rework` outcomes.
5. Rework:
- applied in next long-run window, not fragmented into tiny setup cycles.

## Canonical Lane: `Orchestr8_jr`

Mission:
- governance authority, replay decisions, contract lock for visual/runtime.

Current verified state:
- P07 status file reports `A6 ACTIVE`, `A5 COMPLETE`, and Wave-3 packets `B6/C6/FC-05/MSL-05 UNLOCKED`.
- Wave-2 artifacts exist for all packets and are accepted: `B5`, `C5`, `FC-04`, `MSL-04`.
- `A5_ACTIVE_GOVERNANCE_REPORT.md` delivered with full decision matrix.
- `A6_ACTIVE_GOVERNANCE_REPORT.md` started with Wave-3 launch matrix and kickoff evidence.

Now:
1. Monitor and ACK Wave-3 checkouts.
2. Intake Wave-3 evidence bundles and run replay acceptance loop.
3. Keep SOT docs aligned to live phase truth (reduce stale drift).
4. Enforce desktop Linux target gates (resolution, render-mode fallback, packaging posture) in canonical decisions.

Next:
1. Build compact MVP gate memo from accepted packet set.
2. Move packaging/compliance only after explicit core-complete decision.

Primary sources:
- `.planning/orchestr8_next/execution/checkins/P07/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `.planning/orchestr8_next/artifacts/P07/`

## Core Integration Lane: `a_codex_plan`

Mission:
- build clean marimo-first core with deterministic tests and a pre-wired reactive data-UI interface surface.

Current verified state:
- B1-B5 accepted; B5 report exists with `3/3` packet tests.
- Taskmaster queue defines pending tasks for next integration cycle.

Now:
1. Implement `Data UI Interface Surface` foundation:
- internal command catalog for UI actions (no point-to-point wiring per button).
- reactive state surface that maps button intents to pre-wired handlers.
- shared-memory ingestion for visual integration update events.
2. Implement temporal persistence interface.
3. Integrate temporal state into tour/conversation flow.
4. Expand temporal regression coverage.
5. Wire settlement test hooks and acceptance-matrix assertions.
6. Keep smoke orchestration/reporting deterministic and replayable.
7. Add desktop packaging baseline path (Linux-focused launcher strategy + runtime contract checks) without introducing mobile target scope.

Next:
1. Integrate C5 concept 1 after C5 acceptance.
2. Integrate C5 concept 2 after C5 acceptance.
3. Refine city automation/power/topology interoperability.
4. Draft packaging/acceleration implementation packet for desktop Linux MVP hardening.

Primary sources:
- `.planning/mvp/roadmaps/ROADMAP_A_CODEX_PLAN_TO_MVP.md`
- `.planning/mvp/taskmaster/a_codex_plan.tasks.json`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B5_A_CODEX_PLAN.md`

## Extraction Lane: `2ndFid_explorers`

Mission:
- extract high-value concepts with provenance and licensing-safe clean-room conversion plans.

Current verified state:
- C1-C5 packet pairs are delivered in canonical artifacts.
- C5 is ACCEPTED in Wave-2 batch decision.
- Task queue has pending tasks for next extraction cycle.

Now:
1. Select C5 candidate systems (timeline/inspection focus).
2. Produce `P07_C5_01_*` packet with provenance, value, clean-room plan.
3. Produce `P07_C5_02_*` packet with provenance, value, clean-room plan.
4. Run licensing risk pass for both packets.
5. Map target contracts for `a_codex_plan`.
6. Deliver canonical artifacts with `cp` + `ls -l` proof and completion ping.

Next:
1. Draft next extraction shortlist from canonical accept/rework feedback.

Primary sources:
- `.planning/mvp/roadmaps/ROADMAP_2NDFID_EXPLORERS_TO_MVP.md`
- `.planning/mvp/taskmaster/2ndfid_explorers.tasks.json`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C5_2NDFID_EXPLORERS.md`

## Settlement/Visual Spec Lane: `mingos_settlement_lab`

Mission:
- convert concept and visual direction into implementation-grade transfer artifacts.

Current verified state:
- MSL-01 through MSL-04 reports exist in canonical artifacts; all ACCEPTED.
- Static visual reference file is present at:
  - `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html`

Now:
1. Refine test-hook coverage across active module domains.
2. Tighten acceptance-matrix pass/fail strictness.
3. Cross-link matrix criteria to active B/C/FC packet outputs.
4. Publish direct integration handoff notes for `a_codex_plan`.
5. Update `MSL-04` canonical report with complete delivery-proof text.
6. Produce a focused transfer packet translating approved static dashboard references into implementable UI constraints.

Next:
1. Draft MSL-05 support packet from newest integration findings.

Primary sources:
- `.planning/mvp/roadmaps/ROADMAP_MINGOS_SETTLEMENT_LAB_TO_MVP.md`
- `.planning/mvp/taskmaster/mingos_settlement_lab.tasks.json`
- `.planning/projects/mingos_settlement_lab/ROADMAP.md`

## Founder Tooling Lane: `or8_founder_console`

Mission:
- give founder an async decision cockpit that batches context before mayor escalation.

Current verified state:
- FC-01 through FC-04 reports exist; FC-04 report shows 37 passing tests in lane report.
- Queue has 8 pending tasks for moderation, decision filtering, consistency, and evidence publishing.

Now:
1. Add annotation moderation controls.
2. Add timeline decision filters and packet-focused timeline views.
3. Add founder review bundle endpoint (queue + annotations + timeline summary).
4. Add packet decision audit export endpoint.
5. Expand endpoint tests and data-consistency checks.
6. Publish FC-04 evidence package and FC-05 scope proposal.

Next:
1. Add minimal UX flow for draft annotations before dispatch to mayor.
2. Add founder-side "send bundle" action that emits one structured comms payload.

Primary sources:
- `.planning/mvp/roadmaps/ROADMAP_OR8_FOUNDER_CONSOLE_TO_MVP.md`
- `.planning/mvp/taskmaster/or8_founder_console.tasks.json`
- `.planning/projects/or8_founder_console/ROADMAP.md`

## Dependency Map

1. `2ndFid_explorers C5` -> unlocks `a_codex_plan` C5 integration tasks.
2. `mingos_settlement_lab` hook/matrix updates -> tighten `a_codex_plan` test assertions.
3. `or8_founder_console` review tools -> reduce mayor interruption cost and improve decision throughput.
4. `Orchestr8_jr` acceptance loop -> determines promotion/rework and when packaging can start.

# Code City Deep Fix Queue (No-Dangling-TODO Policy)

Date: 2026-02-14
Scope: orchestr8 only
Status: Active

## Policy Lock

1. If we observe a bug, warning, error, or technical debt item, we fix it to completion before promoting new feature work in that lane.
2. A checkbox is not "done" without evidence: tests, runtime verification, and artifact updates.
3. No silent carry-forward TODOs: unresolved items must stay in this queue with owner, gate, and explicit blocker reason.
4. `maestro` remains flagship-agent identity only.

## Source Inputs (Canonical)

- `SOT/todo.md`
- `SOT/CODE_CITY_LANDSCAPE.md`
- `.taskmaster/docs/file-guides/IP/woven_maps.py.integration.md`
- `SOT/WIRING_PLAN.md`
- `.planning/orchestr8_next/prds/PRD-04-CODE-CITY-VALUE-LAYER.md`
- `.planning/orchestr8_next/prds/PRD-06-OPS-QUALITY-CUTOVER.md`

## Inventory Snapshot

- `SOT/todo.md`: 35 open items
- `.taskmaster/docs/file-guides/IP/woven_maps.py.integration.md`: 0 open integration gaps
- `SOT/WIRING_PLAN.md`: 0 open wiring checks
- `.taskmaster/tasks/tasks.json`: 1 pending top-level task
- Raw total across trackers: 36 (includes overlap; queue below is de-duplicated execution order)

## Execution Order (Strict)

### P0: Correctness and Contract Closure (Blockers First)

#### P0-A: Core Flow Contracts

- [x] Confirm neighborhood grouping and room semantics in runtime code.
- [x] Lock building panel data contract for imports/exports/routines.
- [x] Define room entry trigger for broken room/function.
- [x] Implement Sitting Room transition and return path.
- [x] Define data handoff from Code City to deploy/collab flows.
- [x] Verify full health path: `File Change -> HealthWatcher -> HealthChecker -> STATE -> Code City`.
- [x] Make combat precedence explicit and testable at integration level.
- [x] Wire Summon/Collabor8 context views to Code City-local context.

Gate `G-P0-A`:
- Contract docs updated where relevant.
- Integration tests pass for node-click + panel handoff + status precedence.
- No known broken callback path remains.
- Evidence:
- `IP/features/maestro/code_city_context.py`
- `IP/features/maestro/tests/test_code_city_context.py`
- `IP/features/code_city/tests/test_health_flow.py`
- `IP/contracts/tests/test_status_merge_policy.py`
- `IP/plugins/06_maestro.py`
- `IP/features/maestro/views/shell.py`

#### P0-B: Patchbay and Interaction Debt

- [x] Bridge the 2D/3D keyframe gap (single behavior contract).
- [x] Implement drag-to-rewire gesture in patchbay (currently button-driven only).
- [x] Persist patchbay history across reloads/sessions.
- [x] Ensure apply/dry-run feedback remains policy-guarded and auditable.

Gate `G-P0-B`:
- Patchbay UX flow is deterministic across reload.
- Rewire gesture works with guardrails enabled.
- Regression run passes for connection action events.
- Evidence:
- `IP/static/woven_maps_template.html`

#### P0-C: Known Wiring Debt Outside Renderer

- [x] Implement campaign log JSON path in `.orchestr8/campaigns/`.
- [x] Wire Mermaid generation into Carl briefing pipeline.
- [x] Reconcile stale task trackers (Taskmaster markdown/status drift) to a single truthful status source.

Gate `G-P0-C`:
- `SOT/WIRING_PLAN.md` open checks closed.
- Briefing includes Mermaid output on expected path.
- Task status drift removed from active execution surfaces.
- Evidence:
- `IP/briefing_generator.py`

### P1: Performance and Operational Proof

#### P1-A: Render Throughput and Telemetry

1. Validate sustained high-density runtime at 1M particle target on this machine profile.
2. Add GPU-path telemetry: frame time, particle count, dispatch load.
3. Capture mode-switch and burst-click baselines required by P04.
4. Verify degraded fallback behavior with no shell lockup.

Gate `G-P1-A`:
- Baseline report captured in artifacts.
- Threshold pass/fail criteria explicitly recorded.
- No renderer-startup freeze on fallback path.

#### P1-B: Acceptance Automation

1. Convert repeated manual checks into executable gate suite where practical.
2. Enforce "feature cannot pass with open blocker in same lane" in check-in cadence.

Gate `G-P1-B`:
- Repeatable gate commands documented.
- Check-in protocol reflects blocker enforcement.

### P2: Value-Layer Deepening (After P0/P1 Green)

#### P2-A: Effect Math Pack

1. Barradeau short-edge threshold layering hook.
2. WebGPU/FBO ping-pong simulation path evaluation and decision.
3. Mesh-volume particle seeding mode.
4. Curl-noise field mode with tunables.
5. Dual-source wave-interference field mode.
6. Explicit emergence phase machine:
   - `VOID -> AWAKENING -> TUNING -> COALESCING -> EMERGENCE -> TRANSITION -> READY`
7. Lock transition semantics (teal in transition, gold at ready, no post-ready oscillation).

Gate `G-P2-A`:
- Modes are feature-flagged and bounded.
- No breathing/pulsing regressions.
- Emergence contract remains intact.

#### P2-B: Interaction Surface

1. Neighborhood detail card with status/health/errors/notes/history.
2. Communication-surface behaviors (note stack, aggregation, escalation).
3. Directional panel emergence contract (agents top, tickets/settings right, detail center).
4. Detail-card action strip (deploy, files, connections, campaign log).

Gate `G-P2-B`:
- Card and action strip drive real handlers.
- Directional emergence behavior is predictable and stable.

#### P2-C: Broken-Node Deployment Automation

1. Auto-generate structured ticket payload on broken-node click.
2. Node-context action API: deploy, navigate, graph, mission edit, cancel.
3. Lock-aware deployment handoff in modal + briefing defaults.
4. Temporary unlock/relock handshake for approved write paths.

Gate `G-P2-C`:
- Broken-node click can reach full ticket/deploy flow.
- Lock constraints are visible and enforced.

#### P2-D: Stylization Control Plane (Optional but Tracked)

1. Desktop stylization control panel.
2. One-toggle propagation across typography/motion/density/pacing.
3. Preset packs + instant canonical revert.

Gate `G-P2-D`:
- Revert-to-canonical works in one action.
- No visual-contract drift under toggles.

## Definition of Done (Per Item)

An item is complete only when all conditions hold:

1. Implementation merged in the canonical path.
2. Verification commands executed and passing.
3. Relevant sidecar/docs updated.
4. Related queue line marked complete with artifact reference.
5. No open blocker remains for that item.

## Check-In Contract

For each active packet update:

- Update `.planning/orchestr8_next/execution/checkins/P04/STATUS.md` (or active phase equivalent).
- Record blockers in corresponding `BLOCKERS.md`.
- Attach artifact links under `.planning/orchestr8_next/artifacts/`.

## Immediate Next Packet (Recommended)

Start with `P0-A` in this order:

1. Health/combat/context flow verification and tests.
2. Building panel + room semantics contract lock.
3. Sitting Room trigger/transition/handoff closure.

Rationale: closes highest-impact correctness debt before deeper renderer innovation.

# Orchestr8 Code City TODO

> 2026-02-16 canonical update:
> Active execution queue is `SOT/CODE_CITY_AGGREGATED_TODO.md`.
> Keep this file as historical concept/backlog context and backport only accepted queue items.

Created: 2026-02-12 22:40:19 PST
Scope lock: orchestr8 only, canonical colors unchanged (`#D4AF37`, `#1fbdea`, `#9D4EDD`)

## 2026-02-15 Checkpoint and Next Authorization Queue

- [x] `orchestr8_next/P05` complete and promoted (WP01/WP02/WP03 evidence filed).
- [x] `orchestr8_next/P06` complete and promoted (reliability + cutover + rollback + gate memo).
- [x] Canonical validation rerun in this repo (`11 passed`, rehearsal pass in both modes).
- [ ] Authorize next dual-track sprint packet:
- [ ] Track A (Orchestr8_jr): deepen Code City value layer and shell reliability without reopening core layout.
- [ ] Track B (secondary repo lane): modular execution on adapter and bridge-heavy work for faster throughput.
- [ ] Define convergence gate where both tracks merge into one promotion packet with shared acceptance tests.
- [x] Lane refactor approved:
- [x] `Orchestr8_jr` (canonical approval + UI contract),
- [x] `a_codex_plan` (marimo-core integration),
- [x] `2ndFid_explorers` (line-by-line extraction lane).
- [x] Sequence lock approved: compliance + packaging begins only after core acceptance.
- [x] Deprecated asset rule approved: move deprecated artifacts into `deprecated assets/` (ignored by git/context).
- [x] Checkout/completion proof loop marked critical and mandatory for all lanes.

## Canon Lock (Timestamped)

Locked: 2026-02-12 22:51:55 PST
Authority order: `.planning/phases/CONTEXT.md` -> `.planning/VISION-ALIGNMENT.md` -> `.planning/phases/ARCHITECT-BARRADEAU.md`

- [x] Brand/UI scope is `orchestr8` implementation only.
- [x] Top row canonical: `[orchestr8] [collabor8] [JFDI]`
- [x] `gener8` is excluded from the active UI canon.
- [x] Motion rule: emergence-only behavior.
- [x] Breathing/pulsing animation is forbidden (`no breathing` retained).
- [x] Color system fixed to three states only:
- [x] Working = `#D4AF37` (gold)
- [x] Broken = `#1fbdea` (teal)
- [x] Combat = `#9D4EDD` (purple)
- [x] Building formulas locked:
- [x] Height = `3 + (exports * 0.8)`
- [x] Footprint = `2 + (lines * 0.008)`

## Recovered Concept Backlog (Timestamped)

Added: 2026-02-12 23:27:47 PST
Scope: Net-new, feasible concepts recovered from archival planning/spec fragments
Primary sources:

- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md`
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md`
- `/tmp/markdown-preview/8b051589-179e-4f96-8d9c-ed5fcdd9c77b-sub-3dcc449a-c29c-4c33-866c-79eb7037ca16/Report.md`
- `SOT/MASTER_ROADMAP.md`
- `one integration at a time/Big Pickle/REFERENCES.md`

### Camera + Navigation Behavior (Net-New)

- [x] Lock default Code City entry camera to distant overview perspective for rapid hotspot triage. (Verified: initializeCamera() at line 1445)
- [x] Implement click-to-dive "warp jump" on broken areas: camera dives to neighborhood/building with particles flying past the camera. (Verified: warpDiveTo() + spawnWarpBurst())
- [x] Define round-trip navigation contract: overview -> neighborhood -> building -> room -> Sitting Room -> return to previous focus/camera context. (Verified: navigateToLevel() + returnFromDive())
- [x] Add `focus8` parity behavior: selected-node dive with keyboard shortcut support. (Verified: focus8() + F key)
- [x] Add 3D camera keyframe save/load behavior compatible with existing keyframe workflow. (2D keyframes done, 2D/3D bridge pending)

### Situational Error/Signal Behavior (Net-New)

- [x] Implement broken-node "error pollution" particles with emission intensity driven by error count/severity. (Verified: spawnErrorParticles() at line 4133)
- [x] Lock pollution behavior to rise/fade only (no idle breathing/pulsing loops). (Verified: only spawns in PHASES.READY)
- [x] Lock node interaction contract: hover tooltip shows path/status/errors; click emits structured node event for panel handoff. (Verified: tooltip at line 4672)

### Boundaries, Contracts, Locks (Net-New)

- [x] Render neighborhood boundary overlays (labeled regions with integration crossing badges). (Implemented: woven_maps.py + woven_maps_3d.js)
- [x] Add border-contract metadata surfacing (allowed/forbidden crossing types) on boundary/integration hover. (Implemented: EdgeData extended with contract metadata)
- [x] Add locked-file indicator on building connection points using Louis lock state. (Implemented: barradeau_builder.py + woven_maps_3d.js)
- [x] Define "Town Square" handling for infrastructure files (configs/deps/ignore artifacts) outside normal building rendering. (Implemented: town_square zone in woven_maps.py)

### Data Ingestion + Emergence Semantics (Net-New)

- [x] Add settlement survey ingestion adapter to map fiefdom/files/wiring/agent activity into node and edge metadata. (Verified: IP/contracts/settlement_survey.py)
- [x] Lock merged status precedence when signals overlap: `combat > broken > working`. (Verified: IP/contracts/status_merge_policy.py)
- [x] Add distance-based emergence staggering and decay timing for readability at scale, while preserving emergence-only motion. (Verified: woven_maps.py line 4109)

## Recovered Concept Backlog II (Timestamped)

Added: 2026-02-12 23:30:51 PST
Scope: Net-new concepts recovered from files 5/6/7 with implementation feasibility emphasis
Primary sources:

- `one integration at a time/ROADMAP_ORCHESTR8_V4.md`
- `one integration at a time/Context King/# 👑 EMPEROR'S DECREE: The Orchestr8 Coo.md`
- `one integration at a time/Big Pickle/REFERENCES.md`

### Effect Math + Render Techniques (Net-New)

- [ ] Add Barradeau short-edge threshold layering hook (draw only edges below dynamic threshold per layer).
- [ ] Evaluate WebGPU/FBO ping-pong simulation path for particle position/velocity textures to stabilize very high particle counts.
- [ ] Add mesh-volume particle seeding mode (odd/even ray-intersection inside test) for richer interior fills.
- [ ] Add curl-noise field mode with tunables: `freq`, `amplitude`, `maxDistance`, and falloff `mix(position, target, pow(d, 4))`.
- [ ] Add dual-source wave-interference field mode (`wave1 + wave2`) as optional low-frequency landscape morph driver.
- [ ] Add explicit emergence phase machine for effects control:
- [ ] `VOID -> AWAKENING -> TUNING -> COALESCING -> EMERGENCE -> TRANSITION -> READY`
- [ ] Lock phase transition semantics: teal during transition -> gold at ready, with no post-ready oscillation.

### Audio Mapping Math (Net-New)

- [x] Normalize audio into deterministic bands: low `10-250Hz`, mid `250-2000Hz`, high `2000-20000Hz`. (Implemented: IP/audio/config.py)
- [x] Map bands to effect parameters: `high -> amplitude`, `mid -> offsetGain`, `low -> time-step` with clamp bounds for stability. (Implemented: IP/audio/mapper.py)
- [x] Add optional BPM-derived event clock for discrete bursts (event-driven only, no breathing loops). (Implemented: IP/audio/bpm.py)

### Interaction + Operational Surface (Net-New)

- [ ] Add neighborhood detail card emerging from void center on node/list click with:
- [ ] status, health command, recent errors, stacked notes, recent campaign history.
- [ ] Add communication-surface behavior for the neighborhood list:
- [ ] note stacking, error aggregation, escalation indicators.
- [ ] Add directional panel-emergence contract for predictability:
- [ ] Agents from top, Tickets/Settings from right, detail card from center.
- [ ] Add action strip on detail card:
- [ ] deploy, view files, show connections, view campaign log.

### Broken-Node Deployment Flow (Net-New)

- [ ] On broken-node click, auto-generate structured ticket payload from Carl context + health failures + suggested mission.
- [ ] Add ticket action API surface from node context:
- [ ] deploy, navigate, show graph, edit mission, cancel.
- [ ] Add lock-aware deployment handoff: include Louis lock status in deployment modal and briefing by default.
- [ ] Add temporary unlock/relock handshake pattern (callback-guarded) for approved writes in future patchbay write path.

## Step 1: WebGPU Particle Core First

- [x] Implement `particle_gpu_field` in `IP/woven_maps.py` (WebGPU compute + render)
- [x] Keep existing CPU canvas renderer as automatic fallback
- [x] Map existing control semantics to GPU path:
- [x] `densit8`
- [x] `orbit8`
- [x] `focus8`
- [x] `layer8`
- [x] audio-reactive (low/mid/high mapping)
- [x] Keep current control panel/layout intact
- [ ] Validate sustained high-density runtime with 1M target on this machine profile
- [ ] Add GPU path performance telemetry (frame time, particles, dispatch load)

**Gap Analysis Finding (2026-02-13):** Task claims "done" but GPU validation and telemetry not implemented.

## Step 2: Hit Code City Planning Hard (Architecture Pass)

### A. Spatial/Building Rules

Completed formula lock: 2026-02-13 02:36 PST (`IP/woven_maps.py`)

- [x] Lock building size implementation to planning formulas:
- [x] Height: `3 + (exports * 0.8)`
- [x] Footprint: `2 + (lines * 0.008)`
- [ ] Confirm neighborhood grouping and room semantics in code
- [ ] Define/verify building panel data contract for imports/exports/routines

**Gap Analysis Finding (2026-02-13):** Building formulas locked but neighborhood/room semantics and building panel data contract not verified.

### B. Connection Panels + Wiring Behavior

Completed connection panel/path highlight pass: 2026-02-13 03:02 PST (`IP/woven_maps.py`)
Enhanced connection panel UI: 2026-02-13 03:12 PST (`IP/woven_maps.py`)
Patchbay dry-run bridge pass: 2026-02-13 03:03 PST (`IP/woven_maps.py`, `IP/plugins/06_maestro.py`, `IP/connection_verifier.py`)
Patchbay apply path pass: 2026-02-13 03:04 PST (`IP/connection_verifier.py`, `IP/plugins/06_maestro.py`, `IP/woven_maps.py`)
Patchbay result-feedback + permission guard pass: 2026-02-13 03:30 PST (`IP/plugins/06_maestro.py`, `IP/woven_maps.py`, `IP/connection_verifier.py`)
Patchbay role+history pass: 2026-02-13 03:51 PST (`IP/plugins/06_maestro.py`, `IP/woven_maps.py`, `IP/contracts/connection_action_event.py`)

- [x] Ensure connection panels show file names clearly (no per-wire color noise)
- [x] Implement full signal path highlight on connection click
- [x] Add close button (×) to connection panel
- [x] Extract basenames in panel display (no full path noise)
- [x] Add status color coding (Gold for resolved, Teal for unresolved)
- [x] Update edge colors to canonical Gold/Teal scheme (Gold=working, Teal=broken)
- [x] Plan patchbay rewiring interaction contract (drag connection -> import rewrite path)
- [x] Add non-destructive dry-run validator path (no file writes yet)
- [x] Add guarded apply path (`apply_rewire`) with post-write verification + rollback
- [x] Add panel-visible action result feedback for patchbay actions (dry-run/apply)
- [x] Add explicit apply permission guard (`ORCHESTR8_PATCHBAY_APPLY=1`) in UI + backend
- [x] Add role-aware apply gate (`actorRole` payload + `ORCHESTR8_PATCHBAY_ALLOWED_ROLES`)
- [x] Add per-connection patchbay action history panel (latest 5 events)
- [x] Persist patchbay action history across reloads/sessions (localStorage-backed)
- [x] Add drag-to-set rewire target gesture (panel path drag-and-drop + auto dry-run)
- [x] Define edge truth source precedence (`ConnectionVerifier` -> `woven_maps`)

### C. Sitting Rooms + Collaboration Flow

- [x] Define room entry trigger for broken room/function
- [x] Define Sitting Room transition (particle morph) and return path
- [x] Define data handoff from Code City -> deploy/collab workflows

**Verification (2026-02-14):** Implemented in `IP/features/maestro/code_city_context.py`, `IP/plugins/06_maestro.py`, and `IP/features/maestro/views/shell.py` with tests in `IP/features/maestro/tests/test_code_city_context.py`.

### D. Health + Combat + Context Flow

- [x] Verify end-to-end flow: `File Change -> HealthWatcher -> HealthChecker -> STATE -> Code City`
- [x] Ensure combat state (purple) precedence is explicit and testable
- [x] Wire context views so Summon/Collabor8 can surface Code City-local context

**Verification (2026-02-14):** Added flow + precedence tests in `IP/features/code_city/tests/test_health_flow.py` and `IP/contracts/tests/test_status_merge_policy.py`; Summon/Collabor8 context cards wired via `IP/features/maestro/views/shell.py`.

### E. Layout + UI Lock Validation

- [ ] Re-verify canonical UI frame:
- [ ] Top: `[orchestr8] [collabor8] [JFDI]`
- [ ] Center: `THE VOID (Code City / App Matrix / Chat)`
- [ ] Bottom controls exactly as locked
- [ ] Keep emergence-only motion (no breathing behavior)

**Gap Analysis Finding (2026-02-13):** CSS styling tasks 11-24 marked "done" but not fully implemented. Skipping per user direction.

## Step 3: Integration Cadence (One Feature At A Time)

- [ ] After Step 2 architecture pass, integrate features incrementally with verification per feature
- [ ] Gate each feature on visual + behavioral acceptance before next feature

**Gap Analysis Finding (2026-02-13):** Step 2 architecture pass incomplete - neighborhood semantics, Sitting Rooms, and health flow verification pending.

## Step 4: Global Stylization Control Plane

- [ ] Add a desktop-friendly stylization control panel for global UI toggles and sliders.
- [ ] Ensure one-toggle global propagation across typography, motion profile, panel density, and interaction pacing.
- [ ] Add preset packs + instant revert to canonical visual contract.

## orchestr8_next Surgical Transplant Planning Pack (2026-02-14)

- [x] Canonical planning pack created at `.planning/orchestr8_next/`
- [x] Architecture blueprint: `.planning/orchestr8_next/architecture/ARCHITECTURE_BLUEPRINT.md`
- [x] Wiring diagrams: `.planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md`
- [x] Program PRDs P00-P06: `.planning/orchestr8_next/prds/`
- [x] High-level roadmap: `.planning/orchestr8_next/roadmap/ORCHESTR8_FUTURE_ROADMAP.md`
- [x] Master execution inventory (280 steps): `.planning/orchestr8_next/execution/MASTER_STEP_INVENTORY.md`
- [x] Phase completion prompt template: `.planning/orchestr8_next/execution/PHASE_COMPLETION_PROMPT_TEMPLATE.md`
- [x] Parallel check-in protocol + phase folders: `.planning/orchestr8_next/execution/checkins/`

**Gap Analysis Finding (2026-02-13):** Settings panel exists but shows 160 dummy parameters. Font selector UI not implemented (Task 14 marked done but incomplete). Skipping per user direction.

## Tracking Notes

- This file is the active stack tracker for Code City/WebGPU work.
- Planning contract companion: `SOT/CODE_CITY_PLAN_LOCK.md`
- Blind integration context pack: `SOT/CODE_CITY_LANDSCAPE.md`
- Update timestamp and checkboxes at each completed pass.

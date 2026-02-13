# Orchestr8 Code City TODO

Created: 2026-02-12 22:40:19 PST
Scope lock: orchestr8 only, canonical colors unchanged (`#D4AF37`, `#1fbdea`, `#9D4EDD`)

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

- [ ] Lock default Code City entry camera to distant overview perspective for rapid hotspot triage.
- [ ] Implement click-to-dive "warp jump" on broken areas: camera dives to neighborhood/building with particles flying past the camera.
- [ ] Define round-trip navigation contract: overview -> neighborhood -> building -> room -> Sitting Room -> return to previous focus/camera context.
- [ ] Add `focus8` parity behavior: selected-node dive with keyboard shortcut support.
- [ ] Add 3D camera keyframe save/load behavior compatible with existing keyframe workflow.

### Situational Error/Signal Behavior (Net-New)

- [ ] Implement broken-node "error pollution" particles with emission intensity driven by error count/severity.
- [ ] Lock pollution behavior to rise/fade only (no idle breathing/pulsing loops).
- [ ] Lock node interaction contract: hover tooltip shows path/status/errors; click emits structured node event for panel handoff.

### Boundaries, Contracts, Locks (Net-New)

- [ ] Render neighborhood boundary overlays (labeled regions with integration crossing badges).
- [ ] Add border-contract metadata surfacing (allowed/forbidden crossing types) on boundary/integration hover.
- [ ] Add locked-file indicator on building connection points using Louis lock state.
- [ ] Define "Town Square" handling for infrastructure files (configs/deps/ignore artifacts) outside normal building rendering.

### Data Ingestion + Emergence Semantics (Net-New)

- [ ] Add settlement survey ingestion adapter to map fiefdom/files/wiring/agent activity into node and edge metadata.
- [ ] Lock merged status precedence when signals overlap: `combat > broken > working`.
- [ ] Add distance-based emergence staggering and decay timing for readability at scale, while preserving emergence-only motion.

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

- [ ] Normalize audio into deterministic bands: low `10-250Hz`, mid `250-2000Hz`, high `2000-20000Hz`.
- [ ] Map bands to effect parameters:
- [ ] `high -> amplitude`, `mid -> offsetGain`, `low -> time-step` (with clamp bounds for stability).
- [ ] Add optional BPM-derived event clock for discrete bursts (event-driven only, no breathing loops).

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

## Step 2: Hit Code City Planning Hard (Architecture Pass)

### A. Spatial/Building Rules

Completed formula lock: 2026-02-13 02:36 PST (`IP/woven_maps.py`)

- [x] Lock building size implementation to planning formulas:
- [x] Height: `3 + (exports * 0.8)`
- [x] Footprint: `2 + (lines * 0.008)`
- [ ] Confirm neighborhood grouping and room semantics in code
- [ ] Define/verify building panel data contract for imports/exports/routines

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
- [x] Define edge truth source precedence (`ConnectionVerifier` -> `woven_maps`)

### C. Sitting Rooms + Collaboration Flow

- [ ] Define room entry trigger for broken room/function
- [ ] Define Sitting Room transition (particle morph) and return path
- [ ] Define data handoff from Code City -> deploy/collab workflows

### D. Health + Combat + Context Flow

- [ ] Verify end-to-end flow: `File Change -> HealthWatcher -> HealthChecker -> STATE -> Code City`
- [ ] Ensure combat state (purple) precedence is explicit and testable
- [ ] Wire context views so Summon/Collabor8 can surface Code City-local context

### E. Layout + UI Lock Validation

- [ ] Re-verify canonical UI frame:
- [ ] Top: `[orchestr8] [collabor8] [JFDI]`
- [ ] Center: `THE VOID (Code City / App Matrix / Chat)`
- [ ] Bottom controls exactly as locked
- [ ] Keep emergence-only motion (no breathing behavior)

## Step 3: Integration Cadence (One Feature At A Time)

- [ ] After Step 2 architecture pass, integrate features incrementally with verification per feature
- [ ] Gate each feature on visual + behavioral acceptance before next feature

## Tracking Notes

- This file is the active stack tracker for Code City/WebGPU work.
- Planning contract companion: `SOT/CODE_CITY_PLAN_LOCK.md`
- Blind integration context pack: `SOT/CODE_CITY_LANDSCAPE.md`
- Update timestamp and checkboxes at each completed pass.

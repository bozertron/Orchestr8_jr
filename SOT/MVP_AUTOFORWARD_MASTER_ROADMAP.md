# MVP Auto-Forward Master Roadmap

Last Updated: 2026-02-16
Owner: Mayor + Founder
Intent: keep all lanes shipping in long runs with minimal coordination overhead while preserving replay-grade governance.

## Why This Mode Exists

Founder directive:
- reduce setup chatter and micro-approval latency
- prefer one-shot long runs with hard evidence at closeout
- prioritize any work likely to create visible value within ~2 hours

Mayor interpretation:
- default to auto-forward packet trains
- only interrupt for blocker/safety/legal issues
- batch decisions at end-of-window replay

## MVP North Star (Friendly-Circle Test Ready)

MVP is considered ready when all items below are true:
1. Code City core runtime is stable under canonical replay gates.
2. Founder can annotate intent and review launch-ready packet proposals from one console flow.
3. Settings-driven data/UI behavior is internally pre-wired and test-backed.
4. Visual/token contract is consistent enough to demo without manual patching.
5. Evidence and decisions are reproducible from canonical artifacts and command transcripts.

## Platform Lock (Desktop Linux, High-Resolution)

1. Build target is desktop Linux (`x86_64`) fullscreen laptop workflows.
2. Android/tablet/mobile target-build work is deferred.
3. Default render path is marimo + `WIDGET`; fallback path (`IFRAME`) remains continuously verified.
4. Performance work must favor GPU-accelerated rendering and deterministic rollback paths.
5. Planning references are pinned to:
- `SOT/PLATFORM_TARGET_DESKTOP_LINUX.md`
- `third_party_refs/marimo_docs_upstream_main_20260216/docs/`

## Auto-Forward Execution Contract

1. One kickoff per lane per window.
2. One uninterrupted implementation run per lane.
3. One closeout bundle per lane.
4. Mayor replay + accept/rework decisions in batch.
5. Next wave unlock prepared before current wave closeout finishes.

Required closeout bundle fields:
- canonical artifact path(s)
- exact commands run
- pass counts
- memory observation IDs
- packet closeout result
- residual risk list (`none` allowed)

## Current Packet Train

Wave-4 packet set (auto-generated prep assets already created):
- A7: canonical governance + auto-forward supervision
- B7: Phreak/CSE foundation in core integration lane
- C7: extraction pair for intent parsing + settings validation patterns
- FC-06: C2P observation sync + review queue MVP
- MSL-06: Phreak token and CSE UI constraint transfer packet

Generated launch assets:
- `SOT/CODEBASE_TODOS/LAUNCH_PROMPTS_P07_WAVE4_LONGRUN.md`
- `scripts/generated/P07_wave4_unlock_broadcast.sh`
- `scripts/generated/P07_wave4_canonical_kickoff.sh`
- `SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WAVE4_AUTORUN.toml`

## 2-Hour Impact Plan (Immediate Wins)

1. FC-06 ships founder comment ingestion + review endpoints.
2. B7 ships settings service scaffold + persistence/validation tests.
3. MSL-06 ships token mapping + UI constraint matrix for Phreak/CSE controls.
4. C7 publishes extraction pair that reduces implementation ambiguity for B8/FC-07.
5. A7 captures replay decisions and produces next unlock set without lane parking.
6. Canonical lane publishes desktop Linux packaging + accelerator shortlist gates for Wave-5 packetization.

Expected benefit after 2 hours:
- founder has less manual packet writing load
- core settings work becomes deterministic and testable
- visual direction becomes executable constraints instead of narrative-only guidance

## 24-Hour Plan (Wave-4/5 Bridge)

1. Accept/rework all Wave-4 bundles with replay matrix.
2. Unlock Wave-5 packets immediately using compiler-driven prep.
3. FC-07 adds approve-edit-launch UI for intent queue.
4. B8 binds settings service into additional runtime surfaces.
5. MSL-07 expands constraint coverage to interaction choreography.
6. C8 extracts decision-audit linking patterns for end-to-end traceability.

## 72-Hour Plan (MVP Preflight)

1. Run multi-window long-run cycle with no parked lanes.
2. Freeze MVP demo scenario and script walkthrough.
3. Execute canonical reliability + city integration + founder-console suites.
4. Record baseline performance and UX risk register.
5. Produce friendly-circle test packet:
- demo guide
- known limits
- rollback plan

## Week-One Plan (Pilot Readiness)

1. Harden C2P from assisted mode toward guarded auto-dispatch.
2. Add governance rules for intent risk classes.
3. Add wave-level change budget controls (scope/time/test caps).
4. Finalize onboarding docs for a small external tester cohort.
5. Produce v0.1 release candidate checklist.

## Lane-Specific Backlogs (Advanced Operator Grade)

### Orchestr8_jr (Canonical)

Near-term:
1. Keep replay authority active for every packet decision.
2. Maintain status/guidance integrity and wave continuity.
3. Operate compiler-driven unlock prep every window.

Follow-on:
1. Build acceptance dashboard from closeout/report metadata.
2. Add auto-generated decision matrix templates per wave.

### a_codex_plan (Core Integration)

Near-term:
1. Ship SettingsService module with validation and persistence.
2. Wire settings into command surface and selected city services.
3. Prove determinism through integration plus settings tests.
4. Add Linux desktop packaging baseline with launch profile + render-mode gate checks.

Follow-on:
1. Extend settings-reactive behavior across more runtime domains.
2. Tighten command catalog for data/UI surface prewiring.
3. Integrate approved accelerator hooks (instancing/BVH/profiling telemetry) behind feature flags.

### 2ndFid_explorers (Extraction)

Near-term:
1. Deliver C7 extraction pair for intent parsing + settings models.
2. Publish risk/licensing flags and clean-room contracts.

Follow-on:
1. Maintain rolling shortlist of high-leverage extraction candidates.
2. Feed B/FC lanes with implementation-ready contracts each window.

### or8_founder_console (Founder Tooling)

Near-term:
1. Implement multi-repo intent observation scanner.
2. Implement queue endpoints for founder review and launch prep.
3. Maintain auditable mapping from comment -> packet proposal.

Follow-on:
1. Add packet draft editing and policy lint before dispatch.
2. Add intent quality scoring and duplicate suppression.

### mingos_settlement_lab (Visual/Settlement)

Near-term:
1. Publish Phreak token spec mapped to canonical surfaces.
2. Publish CSE UI constraints and traceability matrix.

Follow-on:
1. Add interactive behavior constraints with test hook references.
2. Maintain transferable UI contracts per wave.

## One-Shot Operating Commands

Build/refresh wave package:

```bash
python scripts/phase_prep_builder.py render --spec SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WAVE4_AUTORUN.toml
```

Broadcast unlocks:

```bash
bash scripts/generated/P07_wave4_unlock_broadcast.sh
```

Kickoff canonical governance loop:

```bash
bash scripts/generated/P07_wave4_canonical_kickoff.sh
```

Optional one-shot combined:

```bash
python scripts/phase_prep_builder.py render --spec SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WAVE4_AUTORUN.toml --send --kickoff-canonical
```

## Risk Controls

1. No packet acceptance without replay + closeout.
2. No silent scope expansion across lanes.
3. No assumptions: two hard-fact probes then defer.
4. No canonical visual ownership violations by non-canonical lanes.
5. No long-run interruption except blocker/safety/legal.

## Decision Policy

When uncertain, prefer:
1. shipping a constrained packet with clear evidence gates
2. deferring unresolved ambiguity into next-wave TODO
3. keeping all lanes productive rather than waiting for perfect plan

This roadmap is intentionally large and forward-biased: its job is to keep the rails visible while work keeps moving.

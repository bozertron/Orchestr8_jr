# Orchestr8 Dual-Track Convergence Plan (2026-02-15)

## Intent

Reset execution after P06 promotion so two parallel lanes can move fast without drifting architecture, then merge into one validated jump forward.

## Shared Outcome Target

- Keep Orchestr8 as deterministic development cockpit.
- Keep `maestro` as flagship-agent identity only.
- Preserve lower-fifth visual contract and core shell reliability.
- Accelerate value-add (Code City + capability slices) with explicit promotion gates.

## Track Split

### Track A (Canonical: `Orchestr8_jr`)

Owner focus: product canon, integration truth, gate authority.

- Maintain and harden the canonical shell + action bus + contracts.
- Own acceptance tests and release-grade gate artifacts.
- Integrate promoted outputs from Track B only through typed contracts.
- Produce weekly canonical checkpoint (`STATUS`, gate memo, test evidence).

### Track B (Secondary lane: `a_codex_plan` / external substrate repo)

Owner focus: high-velocity implementation on bounded packets.

- Implement scoped work packets behind autonomy boundaries.
- Deliver isolated artifacts (code + tests + status + memo).
- Ping canonical lane with evidence for each packet.
- Avoid direct edits to canonical internals until explicit promotion step.

## Interface Contract Between Tracks

Required handoff bundle per packet:

1. Code artifacts (paths listed explicitly)
2. Tests with pass counts and exact commands
3. Status note in phase check-in file
4. Risk + blocker note (even if empty)
5. Ping message with packet ID and completion claim

Canonical lane responsibilities:

1. Pull/sync artifacts
2. Re-run tests in canonical repo
3. Accept/reject with guidance
4. Record decision in shared memory + check-in status

## Next Sprint Packets (Proposed)

### Packet A1 (Track A)

- Build `orchestr8_next` promotion harness for P07 kickoff.
- Add cross-repo artifact intake checklist and validator script.
- Expand regression matrix around shell/action-bus + render-mode toggles.

### Packet B1 (Track B)

- Advance Code City deep-fix queue items that are contract-safe.
- Keep changes behind `city/*` and adapter boundaries.
- Produce parity evidence against canonical sample scenes.

### Packet A2 (Track A)

- Merge approved B1 outputs.
- Run full canonical gate suite.
- Update runbook and release notes.

### Packet B2 (Track B)

- Prototype next capability bridge slice (post-approval only).
- No UI-contract rewrites without explicit architecture RFC.

## Convergence Gates

- **G1 Interface Gate**: contracts stable and validated in both lanes.
- **G2 Behavior Gate**: parity and regression suites green in canonical.
- **G3 Ops Gate**: cutover/rollback rehearsal passes with new changes.

No packet promotion without all applicable gates.

## Planning Cadence (with Ben deeply involved)

1. Joint planning session: finalize packet scope and autonomy boundary.
2. Mid-packet checkpoint: review evidence, adjust risk posture.
3. End-packet promotion review: accept/reject with concrete deltas.
4. Memory/log sync: update README.AGENTS + SOT + shared memory.

## Decisions Needed From Ben Before Execution Starts

1. Choose the exact secondary lane target repo for Track B (`a_codex_plan` vs `2ndFid` vs split usage).
2. Approve first packet pair (`A1` + `B1`) or adjust priority.
3. Confirm non-negotiable freeze list (files/modules Track B must not touch).
4. Confirm desired promotion cadence (daily vs every 2-3 days).

## Definition of Success for This Sprint Pair

- Two parallel lanes run without stepping on each other.
- At least one non-trivial capability packet is promoted into canonical.
- Canonical reliability/cutover posture remains green throughout.

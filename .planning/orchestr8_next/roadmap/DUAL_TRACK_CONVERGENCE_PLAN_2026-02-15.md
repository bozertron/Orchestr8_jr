# Orchestr8 Dual-Track Convergence Plan (2026-02-15)

## Intent

Reset execution after P06 promotion so two parallel lanes can move fast without drifting architecture, then merge into one validated jump forward.

## Shared Outcome Target

- Keep Orchestr8 as deterministic development cockpit.
- Keep `maestro` as flagship-agent identity only.
- Preserve lower-fifth visual contract and core shell reliability.
- Accelerate value-add (Code City + capability slices) with explicit promotion gates.

## Track Split (Refactored 2026-02-15)

### Track A (Canonical: `Orchestr8_jr`)

Owner focus: product canon, integration truth, gate authority.

- Maintain and harden the canonical shell + action bus + contracts.
- Own acceptance tests and release-grade gate artifacts.
- Integrate promoted outputs from Track B only through typed contracts.
- Produce weekly canonical checkpoint (`STATUS`, gate memo, test evidence).

### Track B (Core Integration Lane: `a_codex_plan`)

Owner focus: marimo-first core integration, middleware, adapters, and backend reliability.

- Implement scoped work packets behind autonomy boundaries.
- Deliver isolated artifacts (code + tests + status + memo).
- Ping canonical lane with evidence for each packet.
- Avoid direct edits to canonical internals until explicit promotion step.

### Track C (Research/Extraction Lane: `2ndFid_explorers`)

Owner focus: line-by-line extraction, conversion proposals, and pattern qualification from 2ndFid.

- Perform deep source analysis and produce extraction packets (not blind lifts).
- Send conversion-ready proposals to `Orchestr8_jr` for approval.
- Coordinate with `a_codex_plan` after approval to speed practical integration.
- No direct promotion to canonical without `Orchestr8_jr` acceptance.

## Interface Contract Between Tracks

Required handoff bundle per packet:

1. Code artifacts (paths listed explicitly)
2. Tests with pass counts and exact commands
3. Status note in phase check-in file
4. Risk + blocker note (even if empty)
5. Ping message with packet ID and completion claim

Canonical lane (`Orchestr8_jr`) responsibilities:

1. Pull/sync artifacts
2. Re-run tests in canonical repo
3. Accept/reject with guidance
4. Record decision in shared memory + check-in status

## Execution Sequencing Lock

1. Core and integration work first (`Track B` + approved `Track C` outputs).
2. Packaging/compliance starts only after core is 100% approved and working, including approved `2ndFid_explorers` integrations.
3. No parallel packaging lane before core acceptance.

## Next Sprint Packets (Refactored)

### Packet A1 (`Orchestr8_jr`)

- Publish freeze matrix and surface registry contract.
- Publish extraction acceptance template for `2ndFid_explorers`.
- Publish canonical replay checklist for all incoming packets.

### Packet C1 (`2ndFid_explorers`)

- Line-by-line deep dive and produce first extraction/conversion packet.
- Include licensing/provenance notes and implementation guidance.
- Request approval from `Orchestr8_jr` before integration.

### Packet B1 (`a_codex_plan`)

- Integrate only approved extraction packets plus existing core packet queue.
- Focus on marimo-compliant data handling/routing/adapters.
- Expose capabilities via contract; placement remains a canonical UI concern.

### Packet B2 (`a_codex_plan`, deferred until core acceptance)

- Compliance + packaging:
- Windows (10+), macOS, Linux Mint, Fedora Workstation (43+)
- downloadable, self-configuring install path for internal team usage

## Convergence Gates

- **G1 Interface Gate**: contracts stable and validated in both lanes.
- **G2 Behavior Gate**: parity and regression suites green in canonical.
- **G3 Ops Gate**: cutover/rollback rehearsal passes with new changes.
- **G4 Core-Complete Gate**: packaging lane cannot start until core acceptance is explicit.

No packet promotion without all applicable gates.

## Planning Cadence (with Ben deeply involved)

1. Joint planning session: finalize packet scope and autonomy boundary.
2. Mid-packet checkpoint: review evidence, adjust risk posture.
3. End-packet promotion review: accept/reject with concrete deltas.
4. Memory/log sync: update README.AGENTS + SOT + shared memory.

## Decisions Captured

1. Runtime canon: Marimo-first.
2. Lane model: `Orchestr8_jr` + `a_codex_plan` + `2ndFid_explorers`.
3. Packaging/compliance: sequential after core acceptance, not parallel.
4. Dynamic proof loop (check-out + completion evidence) is mandatory.

## Definition of Success for This Sprint Pair

- Active lanes remain productive without violating freeze boundaries.
- Approved extraction packets flow from `2ndFid_explorers` -> `Orchestr8_jr` -> `a_codex_plan`.
- Core reaches explicit acceptance before packaging lane starts.
- Canonical reliability/cutover posture remains green throughout.

# P07 Operating Model (For Final Founder Approval)

Date: 2026-02-15
Status: Draft for approval

Hard requirements SOT:
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`

## Objective

Run distributed execution without architecture drift:
- `Orchestr8_jr` controls visual canon and promotion gates.
- `a_codex_plan` ships marimo-compliant core integration.
- `2ndFid_explorers` supplies approved extraction/conversion packets.

## Visual Lock and Placement Rule

Visual lock baseline:
- reference snapshot: `/home/bozertron/Downloads/orchestr8_ui_reference.html`
- structure lock: top row + void + lower fifth rhythm
- interaction lock: control semantics and flagship identity rules

Placement rule for non-canonical lanes:
- Track B/C should not decide final UI placement.
- Their responsibility is to expose stable contracts and streams.
- Canonical lane maps those streams to final visual surfaces.

## Runtime Canon

- Marimo-first runtime is canonical.
- Mixed runtime paths are temporary scaffolding and must not become permanent production dependency.

## Lane Ownership

### Lane A: `Orchestr8_jr` (Canonical)

- Own visual contract and UI lock refinement.
- Own protocol contracts and event namespace governance.
- Approve/reject extraction packets.
- Replay tests and promote/reject integration outputs.

### Lane B: `a_codex_plan` (Core Integration)

- Own marimo-compliant data handling, adapter wiring, middleware, routing.
- Integrate only approved extraction packets.
- Produce smoke/regression evidence per packet.
- Do not alter canonical UI files unless explicitly unlocked.

### Lane C: `2ndFid_explorers` (Extraction)

- Perform line-by-line source analysis of 2ndFid.
- Produce extraction packets with provenance and conversion notes.
- Route packets to canonical lane for approval first.

## Freeze Matrix (Immediate)

Frozen to canonical lane unless unlocked by packet:
- `IP/styles/*`
- `IP/static/woven_maps_3d.js`
- `IP/static/woven_maps_template.html`
- visual/layout sections in `IP/plugins/06_maestro.py`

Shared contracts (change by approval only):
- `orchestr8_next/city/contracts.py`
- `orchestr8_next/shell/contracts.py`
- reserved events in `.planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md`

Identity lock:
- `maestro` remains flagship-agent identity only.

## Deprecated Asset Quarantine Policy

When deprecated, asset must be moved to:
- `deprecated assets/`

Controls:
- path ignored by git (`.gitignore`)
- path ignored by context ingestion (`.contextignore`)
- no runtime imports from quarantined assets

## Sequence Lock (Critical)

1. Core completion and approval first.
2. Approved extraction integrations complete and verified.
3. Compliance + packaging phase starts after explicit core acceptance.
4. No parallel packaging lane before step 3 is complete.

## Packet Workflow (Mandatory)

1. Checkout:
- announce packet scope before work (`checkout`, requires ack)
- generate packet worklist and follow it explicitly (`scripts/packet_bootstrap.sh`)
- run prompt/boundary lint before edits (`scripts/packet_lint.sh`)
2. Execute:
- progress updates + blockers in phase check-ins
3. Complete:
- exact commands, pass counts, artifact paths, and risk notes
- run closeout gate before completion ping (`scripts/packet_closeout.sh`)
4. Canonical replay:
- canonical lane reruns verification
5. Decision:
- accept/rework recorded in guidance + shared memory

## Packaging Phase (Deferred Until Core Acceptance)

Target deliverables after core acceptance:
- Windows 10+
- macOS
- Linux Mint
- Fedora Workstation 43+

Install expectation:
- downloadable and self-configuring for internal team rollout

## Approval Checklist

1. Approve lane model (A/B/C).
2. Approve freeze matrix.
3. Approve sequence lock (core before packaging).
4. Approve packet workflow as mandatory governance.

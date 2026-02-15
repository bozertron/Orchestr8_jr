# orchestr8_next Planning System

This directory is the canonical planning and execution package for the Orchestr8 surgical transplant.

## Mission

Build a deterministic, reliable Orchestr8 core that launches from checked-in code, has fully working controls, and isolates visual/value-add systems so high-value capabilities can evolve without UI fragility.

## Strategic Position

- Keep Marimo as the canonical Orchestr8 runtime.
- Keep Code City 3D as an isolated web/Three visualization module.
- Use anywidget/Comm selectively for structured state sync and 2D wiring use-cases.
- Treat AI code generation as a prototyping lane, not a boot dependency.
- Integrate advanced capabilities through explicit bridges, one vertical slice at a time.

## Directory Map

- `architecture/`
  - System boundaries, contracts, wiring diagrams.
- `roadmap/`
  - High-level product roadmap and phase timeline.
- `prds/`
  - Program PRDs for each phase.
- `execution/`
  - Operator prompts, step inventory, and check-in protocol.
- `artifacts/`
  - Reserved for generated reports, gate evidence, and milestone outputs.

## Active Program Phases

- `P00`: Program guardrails and scaffolding
- `P01`: Core shell + lower fifth + action bus
- `P02`: Service adapters + comms bridge
- `P03`: Workspace/IDE integrations as optional adapters
- `P04`: Code City value layer reintegration
- `P05`: capability bridge + slice migration
- `P06`: quality gates, cutover, and hardening

## Current Program Status (2026-02-15)

- `P00-P04`: Completed in prior waves.
- `P05`: Completed and evidence archived in `artifacts/P05/`.
- `P06`: Completed and gate decision is **PROMOTE** (`artifacts/P06/GATE_REVIEW.md`).
- Current posture: **Clean/Parked** pending next authorization packet.

## Non-Negotiables

1. `maestro` always/only refers to the flagship agent in Orchestr8.
2. App boot must be deterministic; no runtime AI code generation required at startup.
3. IDE integrations are optional adapters; core controls work without them.
4. Lower fifth layout and control rhythm are the visual contract.
5. No direct coupling from core shell internals into 3D renderer internals.
6. Every phase must pass explicit acceptance gates before promotion.

## How to Use This Pack

1. Read `architecture/ARCHITECTURE_BLUEPRINT.md` first.
2. Read `architecture/WIRING_DIAGRAMS.md` second.
3. Execute PRDs in order (`P00` -> `P06`).
4. Use `execution/MASTER_STEP_INVENTORY.md` to assign work packets.
5. Use `execution/CHECKIN_PROTOCOL.md` and `execution/checkins/Pxx/*` to report progress and receive guidance.

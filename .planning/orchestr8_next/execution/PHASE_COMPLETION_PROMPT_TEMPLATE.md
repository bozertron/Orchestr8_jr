# Phase Completion Prompt Template

Use this template when assigning or reviewing any phase/work packet.

---

You are implementing **{PHASE_ID} / {WORK_PACKET_ID}** for `orchestr8_next`.

## Mission

Complete steps **{STEP_RANGE}** from:
- `.planning/orchestr8_next/execution/MASTER_STEP_INVENTORY.md`

You must obey:
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/architecture/ARCHITECTURE_BLUEPRINT.md`
- `.planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md`
- `.planning/orchestr8_next/prds/PRD-{PHASE_ID}-*.md`

## Hard Constraints

1. Do not bypass action bus/reducer/store contracts.
2. Do not introduce direct provider calls in UI layer.
3. Keep `maestro` as flagship agent identity only.
4. Keep IDE adapters optional; core must run without them.
5. Preserve lower-fifth visual contract.

## Required Outputs

1. Code changes for all steps in range.
2. A packet report at:
   - `.planning/orchestr8_next/artifacts/{PHASE_ID}/{WORK_PACKET_ID}-packet-report.md`
3. Update status at:
   - `.planning/orchestr8_next/execution/checkins/{PHASE_ID}/STATUS.md`
4. If blocked, update:
   - `.planning/orchestr8_next/execution/checkins/{PHASE_ID}/BLOCKERS.md`

## Mandatory Guardrails

Before edits:
1. Read order complete (`README.AGENTS` -> `HARD_REQUIREMENTS.md` -> `LONG_RUN_MODE.md` -> boundary -> prompt -> check-ins)
2. `scripts/packet_bootstrap.sh {PHASE_ID} {WORK_PACKET_ID} <agent_id>`
3. `scripts/packet_lint.sh <prompt_file> <boundary_file>`
4. Send checkout with `requires_ack=true`

Before completion ping:
1. `scripts/packet_closeout.sh {PHASE_ID} {WORK_PACKET_ID}`
2. Submit one end-of-window evidence bundle (commands, pass counts, artifacts, risks)

## Packet Report Format

- Scope completed
- Step IDs completed
- Files changed
- Tests/run commands
- Contract changes (if any)
- Risks introduced
- Follow-up required

## Definition of Done

All steps completed + evidence present + no critical blocker unresolved.

---

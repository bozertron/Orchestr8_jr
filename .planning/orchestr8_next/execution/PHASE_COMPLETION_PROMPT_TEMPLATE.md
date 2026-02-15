# Phase Completion Prompt Template

Use this template when assigning or reviewing any phase/work packet.

---

You are implementing **{PHASE_ID} / {WORK_PACKET_ID}** for `orchestr8_next`.

## Mission

Complete steps **{STEP_RANGE}** from:
- `.planning/orchestr8_next/execution/MASTER_STEP_INVENTORY.md`

You must obey:
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


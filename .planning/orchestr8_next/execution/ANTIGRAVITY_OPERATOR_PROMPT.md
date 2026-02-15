# Antigravity Operator Prompt (Master)

Use this prompt when spinning up parallel builders for orchestr8_next.

```text
You are a software implementation agent working on orchestr8_next.

Read these files first, in order:
1) .planning/orchestr8_next/README.md
2) .planning/orchestr8_next/architecture/ARCHITECTURE_BLUEPRINT.md
3) .planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md
4) .planning/orchestr8_next/prds/README.md
5) .planning/orchestr8_next/prds/PRD-{PHASE}.md
6) .planning/orchestr8_next/execution/MASTER_STEP_INVENTORY.md
7) .planning/orchestr8_next/execution/PHASE_COMPLETION_PROMPT_TEMPLATE.md

Your assignment:
- Phase: {PHASE}
- Work packet: {WORK_PACKET}
- Step range: {STEP_RANGE}

Constraints:
- Lower fifth UI contract is locked.
- Action bus/reducer/store is the only route for control actions.
- No direct service/provider calls from UI.
- IDE integrations are optional adapters.
- `maestro` refers only to flagship agent identity.

Required outputs:
1) Complete all steps in the assigned range.
2) Create packet report:
   .planning/orchestr8_next/artifacts/{PHASE}/{WORK_PACKET}-packet-report.md
3) Update check-in status:
   .planning/orchestr8_next/execution/checkins/{PHASE}/STATUS.md
4) If blocked, log blocker:
   .planning/orchestr8_next/execution/checkins/{PHASE}/BLOCKERS.md

Definition of done:
- All assigned steps complete
- Evidence report present
- No unresolved critical blocker

If any instruction conflicts with architecture boundaries, stop and log blocker.
```


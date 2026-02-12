---
name: gsd-plan-checker
description: "SETTLEMENT ENHANCED — Validates agent counts match token/complexity, border contracts maintained, room assignments valid."
settlement_enhancements:
  - Verify agent counts match token/complexity calculations
  - Verify border contracts are maintained by plan
  - Verify room assignments are valid (rooms exist, line ranges correct)
---

## SETTLEMENT ENHANCEMENTS

### Agent Count Validation

Check every task's agent count:
```
expected = ceil(task_tokens × complexity_mult × responsibility_mult / 2500) × 3
actual = task.agents
if actual < expected: FAIL — underprovisioned, risk of agent explosion
if actual > expected × 1.5: WARN — overprovisioned, wasted resources
```

### Border Contract Compliance

For every task that touches a file with border connections:
1. Load relevant border contract(s)
2. Check: does the planned action introduce new border crossings?
3. Check: does the planned action remove required interface items?
4. If violation: FAIL with specific contract reference

### Room Assignment Validation

For every task with room assignment:
1. Verify room exists in Surveyor data
2. Verify line range matches Surveyor's recorded boundaries
3. If stale: FAIL — Surveyor data needs refresh
4. Verify room is not assigned to multiple tasks in the same wave (conflict)

---
name: gsd-planner
description: "SETTLEMENT ENHANCED — 'Do X Here' instruction format, room-level task assignment, agent count calculation per task."
settlement_enhancements:
  - Task format includes explicit filepath + line range + exact action
  - Room assignment (which logic block)
  - Agent count calculation per task using scaling formula
---

## SETTLEMENT ENHANCEMENTS

### Room-Level Task Assignment

When Settlement System is active, every task specifies:

1. **Exact room:** Not just file, but specific function/class/block
2. **Exact line range:** From Surveyor data
3. **Token estimate:** For scaling calculation
4. **Agent count:** Calculated from scaling formula

```xml
<task id="1" type="auto" room="login()" lines="25-89" tokens="3500" agents="9">
  <n>Add rate limiting to login</n>
  <files>src/security/auth.ts</files>
  <action>
    Import RateLimiter from ../utils/rateLimiter.
    At line 46, instantiate: const limiter = new RateLimiter(5, 60000)
    Wrap lines 48-65 in rate limit check.
    Do NOT modify function signature.
    Do NOT touch other rooms in this file.
  </action>
  <verify>6th attempt blocked, 5th succeeds, cooldown works</verify>
  <done>Rate limiting active on login, existing tests pass</done>
</task>
```

**Example calculation:** 3500 tokens × 1.7 (complexity 7) × 1.0 (STANDARD) = 5950 effective → ceil(5950/2500) = 3 work units → 3 × 3 = 9 agents

### Agent Count Calculation

For each task, calculate deployment using the **execution-tier** complexity multiplier (0.10):
```text
task_tokens × (1 + complexity_score × 0.10) × responsibility_multiplier
÷ 2500 = work_units
× 3 = total agents (with sentinels)
```

Note: The City Manager uses different complexity multipliers per tier (survey: 0.15, analysis: 0.12, execution: 0.10). Plans produce execution-tier work, so 0.10 is correct here.

Include in plan frontmatter:
```yaml
settlement_deployment:
  total_agents: 45
  work_units: 15
  waves: 3
```

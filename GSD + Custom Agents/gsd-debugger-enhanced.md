---
name: gsd-debugger
description: "SETTLEMENT ENHANCED — Sentinel failure context consumption, root cause pattern identification, future prevention recommendations."
settlement_enhancements:
  - Sentinel failure context consumption
  - Root cause pattern identification
  - Future prevention recommendations
  - FAILURE_PATTERNS.md consultation before debugging
---

## SETTLEMENT ENHANCEMENTS

### Pre-Debug: Read Failure Patterns

Before starting any debug session:
```bash
cat .planning/FAILURE_PATTERNS.md 2>/dev/null
```

Check if the current issue matches a known pattern. If yes:
- Apply the documented successful fix
- Skip hypothesis generation — the pattern tells you the answer

### Sentinel Failure Context

When debugging failures reported by Sentinels:
1. Read the Sentinel's FAILURE_REPORT
2. Read the executor's FAILURE_REPORT
3. Cross-reference: do they agree on root cause?
4. If they disagree: investigate both hypotheses

### Root Cause Pattern Identification

After resolving a bug, check if it matches an existing failure pattern:
- If YES: update pattern frequency count
- If NO: create new pattern entry

Log findings to `.planning/settlement/pattern-logs/` for Failure Pattern Logger (Tier 10):
```markdown
### Debug Finding for Pattern Logger

**Matches existing pattern:** [FP-XXX or NONE]
**Root cause category:** [from failure categories]
**New pattern?** [yes/no]
**Prevention recommendation:** [what would have prevented this]
```

### Prevention Recommendations

After every debug session, produce:
- What upstream change would have prevented this bug?
- Should the Surveyor have caught this? (stale data?)
- Should the Instruction Writer have been more specific?
- Should the Border Agent have flagged this?

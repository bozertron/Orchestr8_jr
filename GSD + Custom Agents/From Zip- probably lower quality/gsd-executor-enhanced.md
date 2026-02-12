---
name: gsd-executor
description: "SETTLEMENT ENHANCED — Sentinel probe response, room-level execution, failure reporting format, Settlement git commit convention."
settlement_enhancements:
  - Sentinel probe response protocol
  - Room-level git commits with Settlement format
  - Failure reporting format for sentinel consumption
---

## SETTLEMENT ENHANCEMENTS

### Sentinel Probe Response

When a Sentinel probes you:
- Report current task, current progress, last file modified
- If stuck: report what you're stuck on (be specific)
- If in error loop: report the error and what you've tried

### Room-Level Execution

When executing Settlement work orders:
- Stay within assigned room (exact line range)
- Do NOT modify other rooms in the same file
- If you discover a needed change outside your room: LOG IT, don't do it
- Let the Sentinel system handle out-of-scope discoveries

### Git Commit Convention

```bash
git commit -m "[Tier 9][${FIEFDOM}][${ROOM}] ${description}

${type}(${scope}): ${concise_description}
- ${key_change_1}
- ${key_change_2}
"
```

### Failure Reporting

If you cannot complete your work unit, produce:
```markdown
## EXECUTOR FAILURE REPORT

**Work Unit:** WU-{id}
**Execution Packet:** EP-{id}
**File:** [path]
**Room:** [name]
**Lines:** [range]

### What I Attempted
[Specific actions taken]

### Where I Failed
[Exact point of failure]

### Error Details
[Error messages, stack traces]

### My Assessment
[What I think went wrong]

### Suggested Fix
[If I have one]
```

This report is consumed by the Sentinel for investigation.

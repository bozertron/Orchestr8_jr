---
name: gsd-phase-researcher
description: "SETTLEMENT ENHANCED — Room-level analysis, wiring research, integration point status per room."
settlement_enhancements:
  - Room (logic block) identification within phase scope
  - Wiring state per room (Gold/Teal/Purple)
  - Integration point status
---

## SETTLEMENT ENHANCEMENTS

### Room-Level Analysis

When researching a phase, identify individual rooms (functions, classes, blocks) within scope:

```markdown
### Room Analysis: auth.ts

| Room | Lines | Tokens | Wiring Status | Integration Points |
|------|-------|--------|--------------|-------------------|
| login() | 25-89 | 1200 | TEAL | validateSession (out to P2P) |
| validateCreds() | 91-130 | 800 | GOLD | None |
| refreshToken() | 132-190 | 1100 | GOLD | AuthToken (out to Calendar) |
```

### Wiring State Per Room

For each room, assess current wiring health:
- **GOLD:** All connections working, types match
- **TEAL:** Has issues — type mismatches, deprecated APIs, missing error handling
- **PURPLE:** Currently being modified

### Integration Point Status

For each room that exports to or imports from other fiefdoms:
- What border contract governs this connection?
- Is the current implementation compliant?
- What changes are needed?

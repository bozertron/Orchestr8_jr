---
name: gsd-verifier
description: "SETTLEMENT ENHANCED — Border contract verification, wiring state update, room-level verification."
settlement_enhancements:
  - Border contract validation after execution
  - Wiring state update (Gold/Teal/Purple)
  - Room-level verification (per-room, not just per-phase)
---

## SETTLEMENT ENHANCEMENTS

### Border Contract Verification

After execution completes, verify all border contracts:

1. Re-scan all import/export statements in modified files
2. Compare against border contracts
3. Flag any NEW violations introduced by execution
4. Flag any RESOLVED violations (previously TEAL, now GOLD)

```markdown
## Border Contract Verification

| Border | Pre-Execution | Post-Execution | Change |
|--------|--------------|----------------|--------|
| Security ↔ P2P | TEAL (1 violation) | GOLD (0 violations) | ✅ Resolved |
| P2P ↔ Calendar | GOLD | GOLD | — No change |
```

### Wiring State Update

Update all wiring statuses based on execution results:
- Connections fixed → TEAL → GOLD
- Connections broken → GOLD → TEAL (CRITICAL)
- Connections modified → PURPLE → GOLD or TEAL

### Room-Level Verification

Verify each modified room individually:
- Does the room still have correct exports?
- Do internal relationships still hold?
- Does the room's function signature match what dependents expect?
- Run room-specific tests if available

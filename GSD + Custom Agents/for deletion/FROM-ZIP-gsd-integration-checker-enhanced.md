---
name: gsd-integration-checker
description: "SETTLEMENT ENHANCED — Cross-fiefdom integration validation, border contract compliance, wiring consistency."
settlement_enhancements:
  - Cross-fiefdom integration validation
  - Border contract compliance check
  - Wiring consistency check
---

## SETTLEMENT ENHANCEMENTS

### Cross-Fiefdom Integration Validation

After execution, verify ALL cross-fiefdom integrations:

1. For each border contract:
   - Are all ALLOWED items still accessible?
   - Are all FORBIDDEN items still blocked?
   - Has the interface surface changed?

2. For each integration point:
   - Does the consumer still receive the expected type?
   - Does the provider still export the expected interface?
   - Are there new uncontracted crossings?

### Wiring Consistency Check

Compare pre-execution wiring map with post-execution state:
- Any Gold wires turned Teal? → REGRESSION
- Any Teal wires turned Gold? → IMPROVEMENT
- Any new wires? → Verify they're in a contract
- Any removed wires? → Verify removal was intentional

### Output

```markdown
## Integration Check: Post-Execution

**Status:** [PASS | WARN | FAIL]

### Border Compliance
[Per-border status]

### Wiring Changes
| Wire | Pre | Post | Assessment |
|------|-----|------|-----------|
| auth.ts → connection.ts | TEAL | GOLD | Resolved ✅ |

### Regressions
[Any new violations or broken wires]
```

# Border Contract Template

**Border ID:** B-[NNN]
**Between:** [FIEFDOM_A] ↔ [FIEFDOM_B]
**Contract Version:** [N.N]
**Created:** [DATE]
**Last Validated:** [DATE]

## Allowed Crossings

### Into [FIEFDOM_A] from [FIEFDOM_B]
| Type | Name | Source File | Reason |
|------|------|------------|--------|
| [type/function/data] | [NAME] | `[FILE]` | [WHY NEEDED] |

### Into [FIEFDOM_B] from [FIEFDOM_A]
| Type | Name | Source File | Reason |
|------|------|------------|--------|
| [type/function/data] | [NAME] | `[FILE]` | [WHY NEEDED] |

## Forbidden Crossings
| Item | Direction | Reason |
|------|-----------|--------|
| [NAME] | [any/in/out] | [WHY FORBIDDEN] |

## Interface Surface
### [FIEFDOM_A] Exports to [FIEFDOM_B]
- `[NAME]` ([type]) from `[FILE]`

### [FIEFDOM_B] Exports to [FIEFDOM_A]
- `[NAME]` ([type]) from `[FILE]`

## Current Violations
| File | Violation | Classification | Remediation |
|------|----------|---------------|-------------|
| `[FILE]` | [DESCRIPTION] | [LEAKING/DANGEROUS] | [FIX] |

## Health
**Status:** [GOLD/TEAL/RED]
**Reason:** [EXPLANATION]

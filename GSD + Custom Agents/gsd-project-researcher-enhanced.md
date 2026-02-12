---
name: gsd-project-researcher
description: "SETTLEMENT ENHANCED — Research per fiefdom, integration point catalog per border, dependency direction analysis."
settlement_enhancements:
  - Research scoped per fiefdom (not just global)
  - Integration point catalog per border
  - Dependency direction analysis (who depends on whom)
---

## SETTLEMENT ENHANCEMENTS

### Fiefdom-Scoped Research

When Settlement System is active, research is organized by fiefdom:

```markdown
## Research: [Fiefdom Name]

### Technology Stack (Fiefdom-Specific)
[What frameworks/libraries are used specifically in this fiefdom]

### Integration Points
| Border | Direction | Types Crossing | Pattern Used |
|--------|-----------|---------------|-------------|
| Security ↔ P2P | P2P imports from Security | AuthToken | Direct import |

### Dependency Direction Analysis
- **This fiefdom DEPENDS ON:** [list of fiefdoms it imports from]
- **DEPENDS ON this fiefdom:** [list of fiefdoms that import from it]
- **Coupling assessment:** [tight | loose | appropriate]

### Fiefdom-Specific Concerns
[Issues unique to this fiefdom's domain]
```

### Integration Point Catalog

Produce per border:
```markdown
### Border: [Fiefdom A] ↔ [Fiefdom B]

**Integration Points:**
1. `AuthToken` — type shared for session validation
   - Defined in: `src/security/types.ts`
   - Consumed by: `src/p2p/connection.ts`, `src/p2p/handshake.ts`
   - Pattern: Direct named import
   - Assessment: Appropriate — minimal surface area

2. `UserModel` — direct DB model import (LEAKING)
   - Defined in: `src/security/models.ts`
   - Consumed by: `src/p2p/legacy-auth.ts`
   - Pattern: Direct named import
   - Assessment: VIOLATION — should use AuthToken instead
```

### Dependency Direction

For each fiefdom pair, determine:
- **Who is the provider?** (exports more)
- **Who is the consumer?** (imports more)
- **Is the relationship balanced or one-directional?**
- **Does the direction make architectural sense?**

Flag inversions: e.g., if a "utility" fiefdom depends on a "feature" fiefdom, the dependency direction is likely wrong.

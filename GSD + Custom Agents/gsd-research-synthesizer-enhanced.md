---
name: gsd-research-synthesizer
description: "SETTLEMENT ENHANCED — Now generates fiefdom map output, agent deployment recommendations, and border contract summaries."
settlement_enhancements:
  - Fiefdom map output (visual representation)
  - Agent deployment recommendations per fiefdom
  - Border contract summary
---

## SETTLEMENT ENHANCEMENTS

### Fiefdom Map Generation

When synthesizing research across fiefdoms, produce a visual fiefdom map:

```
┌─────────────────────────────────────────────────────────┐
│                     THE VOID (Codebase)                  │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │ Security │◄──►│   P2P    │◄──►│ Calendar │           │
│  │ 85K tok  │    │ 120K tok │    │ 45K tok  │           │
│  │ 12 files │    │ 18 files │    │ 8 files  │           │
│  └──────────┘    └──────────┘    └──────────┘           │
│       ▲               ▲                                  │
│       │               │                                  │
│  ┌────┴───────────────┴────┐                            │
│  │   Shared Infrastructure  │                            │
│  │   utils/ types/ config/  │                            │
│  └──────────────────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

### Agent Deployment Recommendations

Per fiefdom, recommend agent counts based on scaling formula:

```markdown
## Deployment Recommendation: Security Fiefdom

| Tier | Agent Type | Count | Rationale |
|------|-----------|-------|-----------|
| 1 | Surveyor (SURVEY×1.6) | 54 | 85K tokens × complexity 6.2 |
| 2 | Pattern Identifier | 12 | Cross-file analysis, 12 files |
| 2 | Import/Export Mapper | 18 | Hub file (auth.ts) needs thorough mapping |
| 9 | Executor + Sentinels | 180 | Highest tier, full scaling |
| **Total** | | **264** | |
```

### Border Contract Summary

Synthesize all border data into executive summary:

```markdown
## Border Contract Summary

| Border | Health | Crossings | Violations | Priority |
|--------|--------|-----------|-----------|----------|
| Security ↔ P2P | TEAL | 8 | 1 (UserModel leak) | HIGH |
| Security ↔ Calendar | GOLD | 3 | 0 | LOW |
| P2P ↔ Calendar | GOLD | 2 | 0 | LOW |
```

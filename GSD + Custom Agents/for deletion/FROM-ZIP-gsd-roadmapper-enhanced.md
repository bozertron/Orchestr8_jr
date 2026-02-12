---
name: gsd-roadmapper
description: "SETTLEMENT ENHANCED — Organizes phases by fiefdom, includes border work as explicit phases, includes agent count estimates per phase."
settlement_enhancements:
  - Organize phases by fiefdom
  - Include border work as explicit phases
  - Include agent count estimates per phase
---

## SETTLEMENT ENHANCEMENTS

### Fiefdom-Based Phase Organization

When Settlement System is active, phases are organized by fiefdom with explicit border phases:

```markdown
## Roadmap (Settlement-Enhanced)

### Phase 1: Survey & Map Codebase
- **Scope:** All fiefdoms
- **Agents:** ~200 (Surveyors + Complexity Analyzers)
- **Output:** Fiefdom maps, border contracts

### Phase 2: Security Fiefdom
- **Scope:** src/security/
- **Agents:** ~264
- **Borders affected:** Security ↔ P2P, Security ↔ Calendar

### Phase 3: Border Work — Security ↔ P2P
- **Scope:** Border remediation
- **Agents:** ~30
- **Output:** Clean border contract, violations resolved

### Phase 4: P2P Fiefdom
- **Scope:** src/p2p/
- **Agents:** ~380
- **Borders affected:** P2P ↔ Calendar
```

### Agent Count Estimates

Each phase includes total estimated agent deployments:
- Survey tier agents
- Execution tier agents (with sentinel overhead)
- Validation tier agents

These estimates use the Universal Scaling Formula with responsibility multipliers.

### Border Phases

Border work gets its OWN phase between fiefdom phases:
- Resolves violations before downstream fiefdoms depend on clean contracts
- Small scope (typically 20-50 agents)
- Must complete before any fiefdom that depends on this border

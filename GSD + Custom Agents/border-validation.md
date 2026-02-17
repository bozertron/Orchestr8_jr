---
name: border-validation
description: "Validate border contracts are maintained after execution. Run by Border Agents during Tier 10."
triggers: City Manager (after execution completes)
---

# Border Validation Workflow

## Purpose
Post-execution verification that all fiefdom border contracts remain intact.

## Prerequisites
- Execution (Tier 9) complete
- Border contracts exist from Tier 3

## Steps

### 1. Re-scan Border Crossings
For each modified file:
```bash
grep -n "^import\|^export" ${FILE} 2>/dev/null
```
Compare against pre-execution import/export map.

### 2. Check Contract Compliance
For each border:
- Are all ALLOWED items still present and functional?
- Are all FORBIDDEN items still blocked?
- Have new crossings been introduced without contract update?
- Has interface surface changed?

### 3. Produce Compliance Report
```markdown
## Border Validation Report

| Border | Contract Version | Pre | Post | Status |
|--------|-----------------|-----|------|--------|
| Security ↔ P2P | 1.0 | TEAL | GOLD | ✅ Improved |
| P2P ↔ Calendar | 1.0 | GOLD | GOLD | ✅ Maintained |
```

### 4. Update Contracts
If execution introduced intentional contract changes:
- Update contract version
- Document what changed and why
- Ensure Civic Council approved the change

### 5. Flag Violations
If execution introduced NEW violations:
- HALT further work on affected fiefdoms
- Report to City Manager
- Create remediation work orders

## Output
- `.planning/settlement/borders/VALIDATION_REPORT.md`
- Updated border contracts (if changed)

## Completion Criteria
- [ ] All borders validated
- [ ] No unintended violations
- [ ] Contract versions updated if changed
- [ ] Violations flagged and remediation planned

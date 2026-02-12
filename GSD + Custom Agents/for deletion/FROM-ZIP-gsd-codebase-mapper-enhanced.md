---
name: gsd-codebase-mapper
description: "SETTLEMENT ENHANCED — Explores codebase and writes structured analysis documents. Now includes fiefdom detection, border identification, token counting per file, and complexity scoring. Writes documents directly to reduce orchestrator context load."
tools: Read, Write, Edit, Bash, Grep, Glob
color: cyan
settlement_enhancements:
  - Fiefdom boundary detection based on directory structure and coupling
  - Border contract inference (what types/data cross boundaries)
  - Token count per file output
  - Complexity score calculation
---

## SETTLEMENT ENHANCEMENTS

The following sections are ADDED to the existing gsd-codebase-mapper agent prompt.
All original functionality is preserved. These sections extend the mapper's output
to support the Settlement System's fiefdom architecture.

### Enhanced Output: FIEFDOMS.md

In addition to existing documents (STACK.md, ARCHITECTURE.md, etc.), the mapper
now produces `FIEFDOMS.md` when the `settlement` flag is set.

**Added to `arch` focus:**

```markdown
# Fiefdom Analysis

**Analysis Date:** [YYYY-MM-DD]

## Detected Fiefdoms

### [Fiefdom Name]
- **Path:** `src/[directory]/`
- **Boundary Confidence:** [HIGH | MEDIUM | LOW]
- **Boundary Signals:**
  - Path structure: [clear directory | ambiguous]
  - Internal coupling ratio: [0.0-1.0]
  - Functional cohesion: [single-domain | mixed]
- **Files:** [count]
- **Total Tokens:** [count]
- **Key Buildings:**
  - `[file.ts]` — [tokens] tokens, complexity [score]
- **Borders:**
  - ↔ [Other Fiefdom]: [crossing count] crossings

## Border Crossings

### [Fiefdom A] ↔ [Fiefdom B]
- **Types crossing:** [list]
- **Functions crossing:** [list]
- **Direction:** [A→B | B→A | bidirectional]
- **Health:** [GOLD | TEAL | RED]

## Shared Infrastructure (Not Fiefdoms)
- `src/utils/` — shared utilities
- `src/types/` — shared type definitions
- `src/config/` — configuration

## Token Summary

| Fiefdom | Files | Tokens | Avg Complexity |
|---------|-------|--------|---------------|
| Security | 12 | 85,000 | 6.2 |
| P2P | 18 | 120,000 | 7.1 |
| Total | 145 | 450,000 | 5.5 |
```

### Enhanced Exploration Commands

**For fiefdom detection (added to arch focus):**
```bash
# Directory-level import analysis for coupling detection
for dir in src/*/; do
  echo "=== $dir ==="
  # Internal imports (within this directory)
  grep -r "from '\.\./\|from '\./" "$dir" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l
  # External imports (from other directories)
  grep -r "from '.*src/" "$dir" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v "from '.*$(basename $dir)" | wc -l
done

# Token estimation per file
find src/ -name "*.ts" -o -name "*.tsx" | while read f; do
  chars=$(wc -c < "$f")
  tokens=$((chars / 4))
  echo "$tokens $f"
done | sort -rn | head -30

# Complexity indicators
find src/ -name "*.ts" -o -name "*.tsx" | while read f; do
  depth=$(grep -c "if\|else\|for\|while\|switch\|catch" "$f")
  echo "$depth $f"
done | sort -rn | head -20
```

### Integration with Settlement Pipeline

When Settlement System is active:
1. FIEFDOMS.md is read by Surveyors (Tier 1) as initial fiefdom hypothesis
2. Cartographers (Tier 3) confirm or revise boundaries using comprehensive survey data
3. Border Agents (Tier 3) build contracts from crossing data

**IMPORTANT:** The mapper's fiefdom detection is a HYPOTHESIS based on directory structure
and basic coupling analysis. The Cartographer makes the FINAL boundary determination
using all three convergence signals (path + coupling + cohesion).

# Settlement System Consolidation & Quality Review Prompt

## Your Mission

You are reviewing the Settlement System v5 documentation that was generated across multiple sessions. Due to context limits and iterative refinement, there are **duplicate files at different quality levels**. Your job is to:

1. **Identify all duplicates** — files with the same base name but different versions
2. **Compare quality** — determine which version is most complete and aligned with specifications
3. **Consolidate** — merge the best content into canonical files
4. **Remove redundancy** — flag files for deletion
5. **Produce a clean, final package** — ready for deployment to `~/.claude/agents/settlement/`

---

## Directory Structure You're Working With

```
GSD + Custom Agents/
├── From Zip- probably lower quality/    ← Earlier versions, likely inferior
│   ├── *.md files                       ← Compare against main folder versions
│   └── settlement-system-complete.tar.gz ← Backup archive
├── files(6).zip                         ← Another archive (may have unique content)
├── OPUS_HANDOFF_PROMPT.md               ← Original spec (REFERENCE ONLY)
├── SETTLEMENT_SYSTEM_PRESSURE_TEST.md   ← Canonical architecture decisions
├── The_Story_of_Mingos_A_Tale_of_Emergence.md ← Founding document (KEEP)
├── settlement-*.md                      ← Main agent prompts
├── settlement-*([0-9]).md               ← Numbered duplicates (iterations)
├── gsd-*-enhanced.md                    ← GSD enhancements
├── *.md (workflows/templates)           ← Supporting documents
```

---

## Known Duplicates to Resolve

| Base Name | Versions Found | Action Needed |
|-----------|----------------|---------------|
| settlement-luminary | `.md`, `(1).md`, `(2).md`, `From Zip/` | Compare, keep best |
| settlement-sentinel | `.md`, `From Zip/` | Compare, keep best |
| settlement-surveyor | `.md`, `(1).md`, `From Zip/` | Compare, keep best |
| settlement-pattern-identifier | `.md`, `(1).md`, `(2).md`, `From Zip/` | Compare, keep best |
| settlement-instruction-writer | `.md`, `(1).md`, `From Zip/` | Compare, keep best |
| settlement-integration-synthesizer | `.md`, `(1).md`, `(2).md`, `From Zip/` | Compare, keep best |
| settlement-vision-walker | `.md`, `From Zip/` | Compare, keep best |
| settlement-failure-pattern-logger | `.md`, `From Zip/` | Compare, keep best |
| settlement-wiring-mapper | `.md`, `From Zip/` | Compare, keep best |
| settlement-work-order-compiler | `.md`, `From Zip/` | Compare, keep best |
| All gsd-*-enhanced.md | Main folder, `From Zip/` | Compare, keep best |
| All workflow/template files | Main folder, `From Zip/` | Compare, keep best |

---

## Quality Criteria (In Priority Order)

When comparing duplicate files, use these criteria:

### 1. Structural Completeness
- Has frontmatter (name, description, tools, model, tier, color)
- Has `<role>` section with clear identity
- Has detailed operational sections (not just placeholders)
- Has `<success_criteria>` with specific checkboxes
- Has output format examples

### 2. Alignment with Pressure Test Decisions
Reference `SETTLEMENT_SYSTEM_PRESSURE_TEST.md` for:
- Correct agent consolidations (e.g., Super-Surveyor absorbed File Structure Mapper)
- Correct tier assignments
- Correct model assignments (Opus vs 1M Sonnet vs Sonnet)
- Universal Scaling Formula with correct multipliers

### 3. Founder's Specifications
- "Founder" terminology (NOT "Emperor")
- Non-military language
- Hardware/manufacturing analogies where appropriate
- Explicit boundaries ("Ambiguity is a no go")
- Rolling Sentinel: always 3 on site
- 40% raw info / 60% reasoning budget

### 4. Operational Depth
- Concrete examples, not abstract descriptions
- Bash commands where appropriate
- JSON output formats specified
- Error handling and escalation paths
- Integration with other agents clearly defined

### 5. File Size as Tiebreaker
Larger files are generally more complete (but verify — padding is not quality)

---

## Expected Output

Produce a consolidation report with this structure:

```markdown
# CONSOLIDATION REPORT

## Summary
- Files reviewed: [N]
- Duplicates identified: [N]
- Files to KEEP (canonical): [N]
- Files to DELETE: [N]
- Files needing MERGE: [N]

## Per-File Decisions

### settlement-luminary.md
**Versions compared:**
- `settlement-luminary.md` (7,979 bytes) — Main folder
- `settlement-luminary(1).md` (3,916 bytes) — Main folder
- `settlement-luminary(2).md` (7,979 bytes) — Main folder
- `From Zip/settlement-luminary.md` (3,916 bytes)

**Best version:** `settlement-luminary.md` (and identical `(2).md`)
**Reasoning:** Most complete, has full success_criteria, proper Opus model assignment
**Action:** KEEP `settlement-luminary.md`, DELETE others
**Merge needed:** No

---
[Repeat for each duplicate set]
---

## Final Package Structure

```
~/.claude/agents/settlement/
├── settlement-luminary.md
├── settlement-city-manager.md
├── settlement-civic-council.md
├── settlement-surveyor.md
├── settlement-complexity-analyzer.md
├── settlement-pattern-identifier.md
├── settlement-import-export-mapper.md
├── settlement-cartographer.md
├── settlement-border-agent.md
├── settlement-integration-researcher.md
├── settlement-vision-walker.md
├── settlement-context-analyst.md      ← NOTE: May need to create (absorbed Discussion Analyzer + Context Writer)
├── settlement-architect.md            ← NOTE: May need to create
├── settlement-work-order-compiler.md
├── settlement-integration-synthesizer.md
├── settlement-wiring-mapper.md
├── settlement-instruction-writer.md
├── settlement-sentinel.md
└── settlement-failure-pattern-logger.md

~/.claude/agents/  (GSD enhancements - modify existing)
├── gsd-codebase-mapper.md
├── gsd-project-researcher.md
├── gsd-research-synthesizer.md
├── gsd-roadmapper.md
├── gsd-phase-researcher.md
├── gsd-planner.md
├── gsd-plan-checker.md
├── gsd-executor.md
├── gsd-verifier.md
├── gsd-integration-checker.md
└── gsd-debugger.md

~/.claude/get-shit-done/workflows/settlement/
├── survey-codebase.md
├── vision-alignment.md
├── deploy-scaled-agents.md
├── sentinel-protocol.md
└── border-validation.md

~/.claude/get-shit-done/templates/settlement/
├── fiefdom-map.md
├── border-contract.md
├── work-order.md
├── building-panel.md
├── failure-pattern.md
└── deployment-plan.md
```

## Missing Agents (Need Creation)

Based on SETTLEMENT_SYSTEM_PRESSURE_TEST.md, these agents are specified but may not have files:
- [ ] settlement-context-analyst.md (Tier 6 — absorbed Discussion Analyzer + Context Writer)
- [ ] settlement-architect.md (Tier 7 — 1M Sonnet, designs approach)

If missing, flag for creation in next phase.

## Files to Delete

```bash
# Run this to clean up duplicates after review
rm "GSD + Custom Agents/settlement-luminary(1).md"
rm "GSD + Custom Agents/settlement-luminary(2).md"
# ... etc
```

## Merge Instructions

[For any files requiring content merge from multiple versions, provide specific instructions]
```

---

## Reference Documents

### SETTLEMENT_SYSTEM_PRESSURE_TEST.md — THE CANONICAL ARCHITECTURE
This document contains:
- All consolidation decisions (44 → 30 agents)
- Tier-by-tier agent assignments
- Model assignments (Opus/1M Sonnet/Sonnet)
- Universal Scaling Formula with multipliers
- Ben's critical notes integrated

**Trust this document for architectural decisions.**

### OPUS_HANDOFF_PROMPT.md — ORIGINAL SPECIFICATION
This was the input prompt. Some specifications were refined during pressure testing.
**Use for reference, but PRESSURE_TEST.md takes precedence where they differ.**

### The_Story_of_Mingos_A_Tale_of_Emergence.md — VISION DOCUMENT
Founding story. Do not modify. Keep as-is.

---

## Workflow

1. **Read SETTLEMENT_SYSTEM_PRESSURE_TEST.md first** — understand the canonical architecture
2. **List all files** in `GSD + Custom Agents/` including subdirectories
3. **Group by base name** — identify all versions of each agent/workflow/template
4. **Compare each group** — use quality criteria above
5. **Produce consolidation report** — with specific keep/delete/merge decisions
6. **Generate cleanup script** — bash commands to remove duplicates
7. **Flag missing agents** — any specified in pressure test but not found

---

## Important Constraints

- **DO NOT modify content** — just identify best versions and flag for cleanup
- **DO NOT delete files yourself** — produce a script for the Founder to review and execute
- **DO preserve archives** — `files(6).zip` and `settlement-system-complete.tar.gz` may be useful for recovery
- **DO flag uncertainty** — if two versions are equally good, note it for human decision

---

## Begin

Start by listing all files in the directory, then proceed with the consolidation analysis.

---
name: survey-codebase
description: "Run Tier 1-3 pipeline: Survey → Pattern Recognition → Cartography. Produces fiefdom map, token budgets, border contracts."
triggers: City Manager
tiers: 1, 2, 3
---

# Survey Codebase Workflow

## Purpose
Execute the complete survey pipeline from raw codebase to fiefdom map.

## Prerequisites
- GSD project initialized
- `.planning/` directory exists

## Steps

### Phase 1: Tier 1 — Survey & Measurement
**Deploy:** Surveyors (SURVEY class, ×1.6 multiplier) + Complexity Analyzers (STANDARD)
**Parallelization:** HIGH — all read-only
**Wave size:** 20-30 agents

1. City Manager calculates total survey scope (all files)
2. Apply scaling formula: `file_tokens × complexity_est × 1.6 / 2500 × 3`
3. Deploy Surveyors in waves of 20-30
4. Deploy Complexity Analyzers after Surveyors complete (operate on survey output)
5. Collect all survey JSON and complexity scores

**Output:** `.planning/settlement/surveys/` — one JSON per file
**Output:** `.planning/settlement/complexity/` — one JSON per file

### Phase 2: Tier 2 — Pattern Recognition
**Deploy:** Pattern Identifiers + Import/Export Mappers (both STANDARD)
**Parallelization:** MEDIUM — cross-file analysis requires some coordination

1. Deploy Pattern Identifiers across all surveyed files
2. Deploy Import/Export Mappers across all surveyed files
3. Import/Export Mappers flag all cross-fiefdom border crossings

**Output:** `.planning/settlement/patterns/PATTERN_REGISTRY.json`
**Output:** `.planning/settlement/wiring/IMPORT_EXPORT_MAP.json`

### Phase 3: Tier 3 — Cartography & Borders
**Deploy:** Cartographers (SYNTHESIS class, ×1.8 multiplier) + Border Agents (STANDARD)

1. Cartographer synthesizes ALL Tier 1-2 outputs
2. Fiefdom boundaries defined using three-signal convergence
3. Ambiguous boundaries escalated to Luminary
4. Token budgets calculated (40/60 split)
5. Deployment plans generated per fiefdom
6. Border Agents produce contracts for every fiefdom border

**Output:** `.planning/settlement/FIEFDOM_MAP.json`
**Output:** `.planning/settlement/borders/` — one contract per border pair
**Output:** `.planning/settlement/DEPLOYMENT_PLAN.json`

## Completion Criteria
- [ ] All files surveyed with room-level data
- [ ] Complexity scores calculated for all files
- [ ] Pattern registry complete
- [ ] Import/export graph complete
- [ ] Fiefdom map produced with explicit boundaries
- [ ] Border contracts produced for all fiefdom pairs
- [ ] Deployment plan calculated with correct responsibility multipliers
- [ ] Ambiguous boundaries resolved or escalated

## Next Step
→ `vision-alignment.md` (Tier 5: Vision Walker with Founder)

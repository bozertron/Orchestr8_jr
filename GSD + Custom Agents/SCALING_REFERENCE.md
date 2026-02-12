# Settlement System — Universal Scaling Reference

**Version:** 4.1 (Consolidated)
**Date:** 2026-02-12

---

## Universal Scaling Formula

```text
INPUTS:
  file_tokens          = approximate token count of target
  complexity_score     = 1-10 based on nesting, dependencies, patterns
  responsibility_class = agent responsibility tier (see table below)

CONSTANTS:
  MAX_TOKENS_PER_AGENT = 2,500 tokens (leaves massive reasoning space)
  COMPLEXITY_MULTIPLIER = 1.0 + (complexity_score × 0.1)
  RESPONSIBILITY_MULTIPLIER = see Responsibility Classes below

FORMULA:
  effective_tokens = file_tokens × COMPLEXITY_MULTIPLIER × RESPONSIBILITY_MULTIPLIER
  work_units = ceil(effective_tokens / MAX_TOKENS_PER_AGENT)
  agents_per_work_unit = 3 (rolling sentinel deployment)
  ═══════════════════════════════════════════════════════════════
  TOTAL_AGENTS = work_units × 3
```

---

## Responsibility Classes

Merged agents do MORE work per deployment than narrow specialists. Their scaling
formula must reflect this to prevent context overload — the exact failure mode
the Settlement System exists to prevent.

| Class | Multiplier | Applies To | Rationale |
|-------|-----------|------------|-----------|
| STANDARD | 1.0 | Single-responsibility agents | Baseline — one job, one focus |
| ENRICHED | 1.2 | Instruction Writer | Absorbed Atomic Task Generator — minimal additional load (near-identical job) |
| COMBINED | 1.3 | Context Analyst | Absorbed Discussion Analyzer + Context Writer — sequential analysis + formatting in one pass |
| HEAVY | 1.4 | City Manager | Absorbed District Planner + Relief Deployer — orchestration + per-fiefdom allocation + failure recovery |
| SURVEY | 1.6 | Surveyor | Absorbed Token Counter + File Structure Mapper + Function Cataloger — comprehensive single-pass file analysis |
| SYNTHESIS | 1.8 | Cartographer | Absorbed Boundary Definer + Token Budget Calculator + Deployment Planner + explicit boundary detection |

### Why This Matters

A Surveyor processing a 138KB file (35K tokens, complexity 7):

**Without responsibility scaling (WRONG):**
```text
35000 × 1.7 = 59,500 → 24 work units → 72 agents
```

**With responsibility scaling (CORRECT):**
```text
35000 × 1.7 × 1.6 = 95,200 → 39 work units → 117 agents
```

The merged agent does 60% more cognitive work per file. Deploy 60% more agents.
Anything less recreates the "agent thinks it's got this, then explodes" failure mode.

---

## Rolling Sentinel Deployment

**Always 3 agents on site per work unit.**

```text
INITIAL STATE:
  Agent 1 = PRIMARY (attempts work)
  Agent 2 = SENTINEL (probes Agent 1 every 30s)
  Agent 3 = SENTINEL (probes Agent 1 every 30s, offset 15s)

SCENARIO A: Agent 1 SUCCEEDS
  • Agent 1 moves to completion
  • Agent 4 deploys (new primary for next work unit)
  • Agents 2 & 3 shift to watch Agent 4
  • Always 3 on site

SCENARIO B: Agent 1 FAILS
  • Agent 2 investigates root cause (Agent 3 watches Agent 2)
  • Agent 4 deploys immediately (maintains 3 on site)

  IF Agent 2 finds fix:
    • Agent 2 applies fix
    • Agent 4 becomes new primary (with fix context)
    • Agents 3 & 5 (new) watch Agent 4

  IF Agent 2 ALSO fails:
    • Agent 3 releases Agents 5 & 6 with combined failure notes
    • Agent 5 becomes primary, Agents 6 & 7 watch
    • Rinse, repeat until solved

INVARIANT: There are ALWAYS 3 agents on site for any active work unit
```

---

## Model Assignments

| Role | Model | Model ID | Reason |
|------|-------|----------|--------|
| Luminary | Opus | opus-4-6 | Deep reasoning, architectural decisions |
| Vision Walker | Opus | opus-4-6 | Nuanced founder interaction |
| Civic Council | Opus | opus-4-6 | Quality verification, cleanup |
| Surveyors | 1M Sonnet | sonnet-4-5-1m | Need to read lots of files |
| Cartographers | 1M Sonnet | sonnet-4-5-1m | Synthesize massive survey data |
| Integration Synthesizers | 1M Sonnet | sonnet-4-5-1m | Hold all connection points |
| Architects | 1M Sonnet | sonnet-4-5-1m | Complex design spanning fiefdoms |
| Work Order Compiler | 1M Sonnet | sonnet-4-5-1m | Needs full picture |
| All execution agents | Sonnet | sonnet-4-5 | Fast, focused, atomic tasks |
| Sentinels | Sonnet | sonnet-4-5 | Quick probe/investigate cycles |
| Border Agents | Sonnet | sonnet-4-5 | Focused contract validation |

---

## Scaling Examples

### Small utility (2.5K tokens, complexity 3, STANDARD agent):
```text
effective = 2500 × 1.3 × 1.0 = 3,250
work_units = ceil(3250 / 2500) = 2
TOTAL_AGENTS = 2 × 3 = 6 agents
```

### Medium file (10K tokens, complexity 5, SURVEY agent):
```text
effective = 10000 × 1.5 × 1.6 = 24,000
work_units = ceil(24000 / 2500) = 10
TOTAL_AGENTS = 10 × 3 = 30 agents
```

### Large file (35K tokens, complexity 7, SURVEY agent):
```text
effective = 35000 × 1.7 × 1.6 = 95,200
work_units = ceil(95200 / 2500) = 39
TOTAL_AGENTS = 39 × 3 = 117 agents
```

### P2P module (200K tokens, complexity 9, SYNTHESIS agent):
```text
effective = 200000 × 1.9 × 1.8 = 684,000
work_units = ceil(684000 / 2500) = 274
TOTAL_AGENTS = 274 × 3 = 822 agents
```

### Sanity Check
If TOTAL_AGENTS > 100 for a single target: LOG WARNING. Confirm with City Manager.
If TOTAL_AGENTS > 500 for a single target: ESCALATE to Luminary. May need to subdivide target.

---

## Demoted Items (Conventions, Not Agents)

### Git Commit Convention
All executors follow this commit message format:
```text
[Tier X][Fiefdom][Room] description

type(scope): concise description
- key change 1
- key change 2
```

This is embedded in every executor's prompt, not a separate agent.

### Scaling Calculation
The formula above is embedded in the City Manager's prompt and the
Deployment section of the Cartographer's output. Not a separate agent.
A formula is a function call, not a context window.

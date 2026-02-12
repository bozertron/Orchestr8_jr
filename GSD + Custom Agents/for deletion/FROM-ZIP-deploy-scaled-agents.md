---
name: deploy-scaled-agents
description: "Deploy agents using Universal Scaling Formula with responsibility multipliers. Used by City Manager for all tier deployments."
triggers: City Manager
---

# Deploy Scaled Agents Workflow

## Purpose
Standard procedure for deploying the correct number of agents to any target.

## Input
- Target: file path, directory, or fiefdom
- Agent type: which agent to deploy
- Responsibility class: STANDARD | ENRICHED | COMBINED | HEAVY | SURVEY | SYNTHESIS

## Procedure

### 1. Calculate Scale
```
RESPONSIBILITY_MULTIPLIERS:
  STANDARD  = 1.0
  ENRICHED  = 1.2
  COMBINED  = 1.3
  HEAVY     = 1.4
  SURVEY    = 1.6
  SYNTHESIS = 1.8

For each target file:
  complexity_mult = 1.0 + (complexity_score × 0.1)
  effective_tokens = file_tokens × complexity_mult × responsibility_mult
  work_units = ceil(effective_tokens / 2500)
  agents_needed = work_units × 3
```

### 2. Sanity Check
- If agents_needed > 100 for single file: LOG WARNING
- If agents_needed > 500 for single file: ESCALATE to Luminary
- If total deployment > 1000: Confirm with Luminary

### 3. Create Deployment Waves
- Max 30 agents per wave
- Waves process sequentially
- Within wave: agents run in parallel

### 4. Deploy with Sentinels
For each work unit:
- 1 primary agent
- 2 sentinel agents (probe at 30s/15s offset)
- = 3 agents per work unit

### 5. Monitor and Recover
- City Manager tracks all deployments
- On failure: deploy replacement with failure context
- Maintain 3-on-site invariant

## Output
- Deployment log with all agent IDs, statuses, timestamps
- Failure reports (if any)
- Completion confirmation per wave

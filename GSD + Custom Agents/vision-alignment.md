---
name: vision-alignment
description: "Run Tier 5: Vision Walker walks Founder through each fiefdom for alignment. BEFORE any planning."
triggers: City Manager (after survey-codebase completes)
tiers: 5
model: opus
---

# Vision Alignment Workflow

## Purpose
Ensure Founder's vision is captured and locked before any planning or execution.

## Prerequisites
- Survey-codebase workflow complete
- Fiefdom map available
- Border contracts available

## Steps

### 1. Deploy Vision Walker (Opus)
One instance, interactive with Founder.

### 2. Walk Each Fiefdom
For each fiefdom in the fiefdom map:
1. Present territory (buildings, health, borders)
2. Explain current understanding
3. Propose approach
4. Ask clarifying questions
5. Capture decisions (LOCKED / DISCRETION / DEFERRED)
6. Confirm alignment

### 3. Walk Each Border
For critical borders (TEAL or RED health):
1. Present current state
2. Explain proposed remediation
3. Get Founder input on contract changes

### 4. Deploy Context Analyst
After Vision Walker completes:
1. Context Analyst processes all alignment output
2. Produces CONTEXT.md per fiefdom
3. Cross-references against borders and patterns

## Output
- `.planning/vision/` — one alignment doc per fiefdom
- `.planning/phases/*/CONTEXT.md` — per phase/fiefdom

## Completion Criteria
- [ ] Every fiefdom walked with Founder
- [ ] Every decision classified (LOCKED/DISCRETION/DEFERRED)
- [ ] Founder approval recorded
- [ ] CONTEXT.md produced
- [ ] No planning proceeds without approval

## Next Step
→ GSD planning workflow (Tier 6-7) with Settlement enhancements

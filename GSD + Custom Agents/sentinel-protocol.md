---
name: sentinel-protocol
description: "Defines the sentinel probe/investigate/fix cycle used by all execution phases."
triggers: All execution deployments
---

# Sentinel Protocol

## Purpose
Standard operating procedure for sentinel watchdog agents during execution.

## Deployment Configuration
Per work unit: 2 sentinels + 1 primary = 3 agents on site

- Sentinel A: probes at T+30s, T+60s, T+90s, T+120s, ... (every 30s)
- Sentinel B: probes at T+15s, T+45s, T+75s, T+105s, ... (every 30s, 15s offset)
- Combined coverage: probe every 15 seconds

## Probe Checklist
Every probe cycle:
1. ☐ Is primary agent producing output?
2. ☐ Have files been modified since last probe?
3. ☐ Has a new commit been made?
4. ☐ Is progress toward verification criteria evident?

## Failure Detection
Trigger investigation if:
- 2 consecutive probes show no progress (60 seconds stalled)
- Primary agent produces error output
- Primary agent's output quality degrades (signs of context exhaustion)

## Investigation Protocol
1. Assess failure type (context exhaustion, logic error, missing dep, architectural mismatch, border violation)
2. Investigate AROUND the problem — check file state, previous changes, packet accuracy
3. Determine root cause
4. If fixable: apply fix, allow primary to resume or deploy fresh agent with fix
5. If not fixable: escalate to City Manager with full report

## Escalation Ladder
- 1st failure: Sentinel investigates and fixes
- 2nd failure: Sentinel investigates, deploys replacement with combined failure notes
- 3rd failure: Escalate to City Manager → may escalate to Luminary

## Invariant
**ALWAYS 3 agents on site for any active work unit.** No exceptions.
When a primary completes or fails, replacement deploys immediately.

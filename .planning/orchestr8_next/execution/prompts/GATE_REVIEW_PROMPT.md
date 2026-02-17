# Prompt: Phase Gate Review

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

Use this prompt after a phase reports complete.

```text
You are reviewing completion evidence for phase {PHASE_ID}.

Read:
1) .planning/orchestr8_next/prds/PRD-{PHASE_ID}-*.md
2) .planning/orchestr8_next/execution/checkins/{PHASE_ID}/STATUS.md
3) .planning/orchestr8_next/execution/checkins/{PHASE_ID}/BLOCKERS.md
4) .planning/orchestr8_next/artifacts/{PHASE_ID}/

Evaluate against gate criteria exactly.

Output required:
- Gate Decision: pass | conditional-pass | fail
- Evidence Summary: what proves completion
- Gaps: specific missing artifacts/tests/contracts
- Required Remediation Steps
- Confidence: low | medium | high

Do not infer completion if evidence is missing.
```


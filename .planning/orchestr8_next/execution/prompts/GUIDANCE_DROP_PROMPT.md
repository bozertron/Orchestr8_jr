# Prompt: Architect Guidance Drop

Use this prompt to generate precise guidance when a packet or phase drifts.

```text
You are the architect issuing guidance for {PHASE_ID}/{WORK_PACKET_ID}.

Read:
- Current status: .planning/orchestr8_next/execution/checkins/{PHASE_ID}/STATUS.md
- Blockers: .planning/orchestr8_next/execution/checkins/{PHASE_ID}/BLOCKERS.md
- Packet report: .planning/orchestr8_next/artifacts/{PHASE_ID}/{WORK_PACKET_ID}-packet-report.md

Write guidance that includes:
1) Correction summary
2) Non-negotiable constraints
3) Exact files to update
4) Acceptance checks to rerun
5) Deadline for next check-in

Place output in:
- .planning/orchestr8_next/execution/checkins/{PHASE_ID}/GUIDANCE.md
```


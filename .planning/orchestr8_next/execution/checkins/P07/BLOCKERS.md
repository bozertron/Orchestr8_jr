# P07 Blockers

Use this file to track blockers requiring architect/founder decisions.

## Entry Template

- Date:
- Owner:
- Severity:
- Packet ID:
- Blocker:
- Decision Needed:
- Unblocking Options:
- Temporary Workaround:

## Current

- None.

## Resolved

| Date | Packet | Blocker | Resolution |
|------|--------|---------|------------|
| 2026-02-15 | P07-A1 | Cross-repo artifact delivery procedural gap | Added `ARTIFACT_DELIVERY_CONTRACT.md` with explicit destination paths |
| 2026-02-15 | P07-M1 | Outbox replay fragility and lane failover ambiguity | Hardened `scripts/agent_comms.sh` (lane-aware endpoints + `jq` replay annotation), then validated 5/5 scenarios and published `M1_MEMORY_HARDENING_REPORT.md` |
| 2026-02-16 | P07-GH1 | Prompt/boundary drift causing false-complete packets | Added `HARD_REQUIREMENTS.md`, guardrail scripts (`packet_bootstrap/lint/closeout`), and aligned B2/C2 naming contracts |

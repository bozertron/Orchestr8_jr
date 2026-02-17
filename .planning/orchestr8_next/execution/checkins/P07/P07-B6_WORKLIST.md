# P07-B6 Worklist

- Phase: P07
- Packet ID: P07-B6
- Agent ID: a_codex_plan
- Boundary: .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B6_A_CODEX_PLAN.md
- Prompt:
- Generated: 2026-02-16T09:47:42Z

## Preconditions

- [x] Read order complete (README.AGENTS -> HARD_REQUIREMENTS -> LONG_RUN_MODE -> boundary -> prompt -> check-ins)
- [x] Preflight comms complete
- [x] Prompt/boundary lint passed
- [x] Checkout sent and ack recorded

## Work Items

- [ ] ACP-06: Implement bucketization engine in `temporal_state.py` (SessionActivityGraph)
- [ ] ACP-07: Implement event management/filtering in `temporal_state.py` (HistoryPanel)
- [ ] ACP-13: Enhance `tour_service.py` and `agent_conversation.py` with enriched event metadata
- [ ] ACP-14: Add regression tests for C5-driven core behaviors
- [ ] Execute tests for packet scope
- [ ] Record exact command outputs and pass counts

## Required Evidence

- [ ] `orchestr8_next/city/temporal_state.py`
- [ ] `orchestr8_next/city/tour_service.py`
- [ ] `orchestr8_next/city/agent_conversation.py`
- [ ] `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md`

## Closeout

- [ ] scripts/packet_closeout.sh P07 P07-B6 passed
- [ ] Completion ping sent
- [ ] Outbox checked/flushed if needed
- [ ] Residual risks recorded (or none)

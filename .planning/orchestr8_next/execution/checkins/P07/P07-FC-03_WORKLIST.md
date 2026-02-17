# P07-FC-03 Worklist

- Phase: P07
- Packet ID: P07-FC-03
- Agent ID: or8_founder_console
- Boundary: .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-03_OR8_FOUNDER_CONSOLE.md
- Prompt: 
- Generated: 2026-02-16T02:58:20Z

## Preconditions

- [ ] Read order complete (README.AGENTS -> HARD_REQUIREMENTS -> LONG_RUN_MODE -> boundary -> prompt -> check-ins)
- [ ] Preflight comms complete
:   - scripts/agent_flags.sh unread or8_founder_console P07
:   - scripts/agent_comms.sh health
- [ ] Prompt/boundary lint passed
:   - scripts/packet_lint.sh  .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-03_OR8_FOUNDER_CONSOLE.md
- [ ] Checkout sent and ack recorded

## Work Items

- [ ] Itemize implementation tasks from scope
- [ ] Execute tests for packet scope
- [ ] Record exact command outputs and pass counts

## Required Evidence

- [ ] `/home/bozertron/or8_founder_console/routers/review.py`
- [ ] `/home/bozertron/or8_founder_console/tests/test_review.py`
- [ ] `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-03_REPORT.md`

## Closeout

- [ ] scripts/packet_closeout.sh P07 P07-FC-03 passed
- [ ] Completion ping sent
- [ ] Outbox checked/flushed if needed
- [ ] Residual risks recorded (or none)

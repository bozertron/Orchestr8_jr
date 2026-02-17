# P07-B2 Worklist

- Phase: P07
- Packet ID: P07-B2
- Agent ID: a_codex_plan
- Boundary: .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B2_A_CODEX_PLAN.md
- Prompt: 
- Generated: 2026-02-16T01:14:02Z

## Preconditions

- [ ] Read order complete (README.AGENTS -> HARD_REQUIREMENTS -> LONG_RUN_MODE -> boundary -> prompt -> check-ins)
- [ ] Preflight comms complete
:   - scripts/agent_flags.sh unread a_codex_plan P07
:   - scripts/agent_comms.sh health
- [ ] Prompt/boundary lint passed
:   - scripts/packet_lint.sh  .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B2_A_CODEX_PLAN.md
- [ ] Checkout sent and ack recorded

## Work Items

- [ ] Itemize implementation tasks from scope
- [ ] Execute tests for packet scope
- [ ] Record exact command outputs and pass counts

## Required Evidence

- [ ] `orchestr8_next/city/topology.py` delivered/updated in canonical repo.
- [ ] `orchestr8_next/city/heatmap.py` delivered/updated in canonical repo.
- [ ] `tests/integration/test_graphs.py` delivered/updated in canonical repo.
- [ ] `B2_INTEGRATION_SMOKE_REPORT.md` delivered to canonical path.
- [ ] Exact test commands + pass counts.
- [ ] Status updates via comms to codex.
- [ ] Canonical destination delivery proof:
- [ ] `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B2_INTEGRATION_SMOKE_REPORT.md`

## Closeout

- [ ] scripts/packet_closeout.sh P07 P07-B2 passed
- [ ] Completion ping sent
- [ ] Outbox checked/flushed if needed
- [ ] Residual risks recorded (or none)

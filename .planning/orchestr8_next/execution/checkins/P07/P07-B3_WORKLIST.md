# P07-B3 Worklist

- Phase: P07
- Packet ID: P07-B3
- Agent ID: a_codex_plan
- Boundary: .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B3_A_CODEX_PLAN.md
- Prompt: 
- Generated: 2026-02-16T02:13:31Z

## Preconditions

- [ ] Read order complete (README.AGENTS -> HARD_REQUIREMENTS -> LONG_RUN_MODE -> boundary -> prompt -> check-ins)
- [ ] Preflight comms complete
:   - scripts/agent_flags.sh unread a_codex_plan P07
:   - scripts/agent_comms.sh health
- [ ] Prompt/boundary lint passed
:   - scripts/packet_lint.sh  .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B3_A_CODEX_PLAN.md
- [ ] Checkout sent and ack recorded

## Work Items

- [ ] Itemize implementation tasks from scope
- [ ] Execute tests for packet scope
- [ ] Record exact command outputs and pass counts

## Required Evidence

- [ ] `orchestr8_next/city/automation.py` (new/updated)
- [ ] `orchestr8_next/city/power_grid.py` (new/updated)
- [ ] `tests/integration/test_city_automation.py`
- [ ] `tests/integration/test_city_power_grid.py`
- [ ] `.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md`
- [ ] Exact validation command + pass counts.
- [ ] Canonical destination delivery proof:
- [ ] `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md`

## Closeout

- [ ] scripts/packet_closeout.sh P07 P07-B3 passed
- [ ] Completion ping sent
- [ ] Outbox checked/flushed if needed
- [ ] Residual risks recorded (or none)

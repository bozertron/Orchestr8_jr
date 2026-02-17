# Resume Prompt - a_codex_plan (Post-B5)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming the `a_codex_plan` lane for packet `P07-B6`.

## Packet

- Packet ID: `P07-B6`
- Scope: Integrate accepted C5 concepts into core service flow and harden pre-wired data-UI behavior.

## Preconditions (must pass before coding)

```bash
scripts/agent_flags.sh unread <agent_id> P07
scripts/agent_comms.sh health
```

If health is unreachable:

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B6_A_CODEX_PLAN.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_01_SessionActivityGraph.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_02_HistoryPanel.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-B6; scope=c5 integration + data-ui surface hardening; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist and lint before edits:

```bash
scripts/packet_bootstrap.sh P07 P07-B6 <agent_id>
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_B5_A_CODEX_PLAN.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B6_A_CODEX_PLAN.md
```

## Required outputs

- `orchestr8_next/city/temporal_state.py`
- `orchestr8_next/city/tour_service.py`
- `orchestr8_next/city/agent_conversation.py`
- `.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md
```

Required validation:

```bash
pytest tests/integration/test_temporal_state.py tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
```

Before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-B6
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B6 complete; evidence posted"
```

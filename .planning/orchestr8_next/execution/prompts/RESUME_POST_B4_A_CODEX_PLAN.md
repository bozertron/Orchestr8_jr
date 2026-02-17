# Resume Prompt - a_codex_plan (Post-B4)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming the `a_codex_plan` lane for packet `P07-B5`.

## Packet

- Packet ID: `P07-B5`
- Scope: Temporal-state core services (epoch timeline, quantum events, snapshots).

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
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B5_A_CODEX_PLAN.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/mingos_settlement_lab/transfer/SETTLEMENT_MASTER_PRD.md`
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_03_IMPLEMENTATION_BACKLOG.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_01_QuickActions.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_02_LayerStack.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-B5; scope=temporal state core services; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist and lint before edits:

```bash
scripts/packet_bootstrap.sh P07 P07-B5 <agent_id>
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_B4_A_CODEX_PLAN.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B5_A_CODEX_PLAN.md
```

## Required outputs

- `orchestr8_next/city/temporal_state.py`
- `tests/integration/test_temporal_state.py`
- `.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B5_INTEGRATION_SMOKE_REPORT.md
```

Required validation:

```bash
pytest tests/integration/test_temporal_state.py -vv
```

Before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-B5
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B5 complete; evidence posted"
```

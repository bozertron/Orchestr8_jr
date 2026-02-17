# Resume Prompt - a_codex_plan (Post-B2)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming the `a_codex_plan` lane for packet `P07-B3`.

## Packet

- Packet ID: `P07-B3`
- Scope: Integrate accepted C2 concepts (automation + power grid telemetry) into marimo-first core runtime.

## Preconditions (must pass before coding)

1. Preflight comms (required):

```bash
scripts/agent_flags.sh unread <agent_id> P07
scripts/agent_comms.sh health
```

If health is unreachable, run recovery start (allowed cross-lane):

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

2. Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B3_A_CODEX_PLAN.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

3. Send checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-B3; scope=automation+power-grid integration; files=<files>; tests=<tests>; eta=<eta>"
```

4. Generate and follow packet worklist (required):

```bash
scripts/packet_bootstrap.sh P07 P07-B3 <agent_id>
```

5. Enforce prompt/boundary consistency before edits:

```bash
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_B2_A_CODEX_PLAN.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B3_A_CODEX_PLAN.md
```

## Required outputs

- `orchestr8_next/city/automation.py`
- `orchestr8_next/city/power_grid.py`
- `tests/integration/test_city_automation.py`
- `tests/integration/test_city_power_grid.py`
- `.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md`

Canonical delivery proof (required):

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md
```

Required validation:

```bash
pytest tests/integration/test_city_automation.py tests/integration/test_city_power_grid.py -vv
```

Before completion ping (required):

```bash
scripts/packet_closeout.sh P07 P07-B3
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B3 complete; evidence posted"
```

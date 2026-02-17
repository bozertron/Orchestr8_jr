# Resume Prompt - a_codex_plan (Post-B3)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming the `a_codex_plan` lane for packet `P07-B4`.

## Packet

- Packet ID: `P07-B4`
- Scope: Integrate accepted C3 concepts into core runtime services (tour + conversation).

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
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B4_A_CODEX_PLAN.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C3_01_MaestroWizard.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C3_02_WizardConversation.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-B4; scope=tour+conversation core services; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist and lint before edits:

```bash
scripts/packet_bootstrap.sh P07 P07-B4 <agent_id>
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_B3_A_CODEX_PLAN.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B4_A_CODEX_PLAN.md
```

## Required outputs

- `orchestr8_next/city/tour_service.py`
- `orchestr8_next/city/agent_conversation.py`
- `tests/integration/test_city_tour_service.py`
- `tests/integration/test_agent_conversation.py`
- `.planning/orchestr8_next/artifacts/P07/B4_INTEGRATION_SMOKE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B4_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B4_INTEGRATION_SMOKE_REPORT.md
```

Required validation:

```bash
pytest tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -vv
```

Before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-B4
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B4 complete; evidence posted"
```

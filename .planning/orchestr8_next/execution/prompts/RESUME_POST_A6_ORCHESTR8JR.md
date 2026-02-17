# Resume Prompt - orchestr8_jr (P07-A7)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-A7`.

## Packet

- Packet ID: `P07-A7`
- Scope: Canonical governance + autop-run packet compiler oversight

## Objective

Run Wave-4 governance loop with auto-forward unlock prep and batch replay decisions.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread orchestr8_jr P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A7_ORCHESTR8JR.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/SOT/MVP_AUTOFORWARD_MASTER_ROADMAP.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send orchestr8_jr codex P07 checkout true "packet=P07-A7; scope=wave4 active governance + batch replay + wave5 prep; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-A7 orchestr8_jr
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_A6_ORCHESTR8JR.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A7_ORCHESTR8JR.md
```

## Required outputs

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A7_ACTIVE_GOVERNANCE_REPORT.md
```

Validation:

```bash
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py tests/city/test_wiring_view.py tests/city/test_parity.py -q
```
Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-A7
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-A7 long-run bundle complete; updated TODO + evidence posted"
```

# Resume Prompt - or8_founder_console (P07-FC-06)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-FC-06`.

## Packet

- Packet ID: `P07-FC-06`
- Scope: Founder tooling packet: comment ingestion + proposal queue

## Objective

Ship C2P Wave-4 MVP: observation sync + review queue for launch-ready packets.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread or8_founder_console P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-06_OR8_FOUNDER_CONSOLE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/or8_founder_console/C2P_STRATEGIC_PLAN.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-05_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send or8_founder_console codex P07 checkout true "packet=P07-FC-06; scope=c2p wave4 observation sync + review queue; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-FC-06 or8_founder_console
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_06.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-06_OR8_FOUNDER_CONSOLE.md
```

## Required outputs

- `/home/bozertron/or8_founder_console/services/intent_scanner.py`
- `/home/bozertron/or8_founder_console/routers/intent_queue.py`
- `/home/bozertron/or8_founder_console/tests/test_intent_scanner.py`
- `/home/bozertron/or8_founder_console/tests/test_intent_queue.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-06_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-06_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-06_REPORT.md
```

Validation:

```bash
python -m pytest tests/ -v
```
Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-FC-06
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-FC-06 long-run bundle complete; updated TODO + evidence posted"
```

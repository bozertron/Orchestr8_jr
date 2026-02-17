# Resume Prompt - FC-04 (Founder Console)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-FC-04`.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread <agent_id> P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-04_OR8_FOUNDER_CONSOLE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-03_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-FC-04; scope=annotations+timeline endpoints; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-FC-04 <agent_id>
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_04.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-04_OR8_FOUNDER_CONSOLE.md
```

## Required outputs

- `/home/bozertron/or8_founder_console/routers/annotations.py`
- `/home/bozertron/or8_founder_console/routers/timeline.py`
- `/home/bozertron/or8_founder_console/tests/test_annotations.py`
- `/home/bozertron/or8_founder_console/tests/test_timeline.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md
```

Validation:

```bash
python -m pytest tests/ -v
```

Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-FC-04
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-FC-04 complete; evidence posted"
```

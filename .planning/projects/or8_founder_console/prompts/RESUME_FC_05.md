# Resume Prompt - FC-05 (Founder Console)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-FC-05`.

## Packet

- Packet ID: `P07-FC-05`
- Scope: Review bundle endpoint, decision audit export, and consistency checks.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread <agent_id> P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-05_OR8_FOUNDER_CONSOLE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-04_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-FC-05; scope=review bundle + audit export; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-FC-05 <agent_id>
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_05.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-05_OR8_FOUNDER_CONSOLE.md
```

## Required outputs

- `/home/bozertron/or8_founder_console/routers/review_bundle.py`
- `/home/bozertron/or8_founder_console/routers/audit_export.py`
- `/home/bozertron/or8_founder_console/tests/test_review_bundle.py`
- `/home/bozertron/or8_founder_console/tests/test_audit_export.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-05_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-05_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/FC-05_REPORT.md
```

Validation:

```bash
python -m pytest tests/ -v
```

Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-FC-05
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-FC-05 complete; evidence posted"
```

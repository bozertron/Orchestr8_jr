# Resume Prompt - Orchestr8_jr (Post-A5)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are running canonical packet `P07-A6`.

## Packet

- Packet ID: `P07-A6`
- Scope: Active governance and replay for Wave-3 packet set (`B6`, `C6`, `FC-05`, `MSL-05`).

## Preconditions

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_comms.sh health
```

Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A6_ORCHESTR8JR.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

Send checkout (requires ack):

```bash
scripts/agent_comms.sh send orchestr8_jr codex P07 checkout true "packet=P07-A6; scope=wave3 active governance + replay; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist and run lint:

```bash
scripts/packet_bootstrap.sh P07 P07-A6 orchestr8_jr
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_A5_ORCHESTR8JR.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A6_ORCHESTR8JR.md
```

Required output:

- `.planning/orchestr8_next/artifacts/P07/A6_ACTIVE_GOVERNANCE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A6_ACTIVE_GOVERNANCE_REPORT.md
```

Closeout before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-A6
```

# Resume Prompt - Orchestr8_jr (Post-A3)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are running canonical packet `P07-A4`.

## Scope

- Keep all active lanes moving (B3, C3, FC-02, MSL-02).
- Perform replay validation and accept/rework decisions.
- Keep STATUS/GUIDANCE/BLOCKERS current and compaction-safe.

## Preconditions

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_comms.sh health
```

Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A4_ORCHESTR8JR.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

Send checkout (requires ack):

```bash
scripts/agent_comms.sh send orchestr8_jr codex P07 checkout true "packet=P07-A4; scope=active governance + replay; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist:

```bash
scripts/packet_bootstrap.sh P07 P07-A4 orchestr8_jr
```

Closeout before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-A4
```

# Resume Prompt - Orchestr8_jr (Post-A4)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are running canonical packet `P07-A5`.

## Scope

- Keep all Wave-2 lanes moving with zero idle transitions:
  - `P07-B5` (`a_codex_plan`)
  - `P07-C5` (`2ndFid_explorers`)
  - `P07-FC-04` (`or8_founder_console`)
  - `P07-MSL-04` (`mingos_settlement_lab`)
- Perform replay validation and accept/rework decisions.
- Keep `STATUS.md`, `GUIDANCE.md`, and `BLOCKERS.md` current and compaction-safe.

## Preconditions

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_comms.sh health
```

Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A5_ORCHESTR8JR.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

Send checkout (requires ack):

```bash
scripts/agent_comms.sh send orchestr8_jr codex P07 checkout true "packet=P07-A5; scope=wave2 active governance + replay; files=<files>; tests=<tests>; eta=<eta>"
```

Generate worklist:

```bash
scripts/packet_bootstrap.sh P07 P07-A5 orchestr8_jr
```

Required output:

- `.planning/orchestr8_next/artifacts/P07/A5_ACTIVE_GOVERNANCE_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/A5_ACTIVE_GOVERNANCE_REPORT.md
```

Closeout before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-A5
```

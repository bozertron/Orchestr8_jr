# Resume Prompt - 2ndFid_explorers (Post-C3)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming `2ndFid_explorers` for packet `P07-C4`.

## Preconditions (required)

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
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C4_2NDFID_EXPLORERS.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-C4; scope=command+layer extraction pair; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
scripts/packet_bootstrap.sh P07 P07-C4 <agent_id>
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_C3_2NDFID_EXPLORERS.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C4_2NDFID_EXPLORERS.md
```

## Required outputs

- `.planning/orchestr8_next/artifacts/P07/P07_C4_01_<Name>.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C4_02_<Name>.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_source_packet_01> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_01_<Name>.md
cp <lane_source_packet_02> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_02_<Name>.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_01_<Name>.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_02_<Name>.md
```

Before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-C4
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C4 complete; extraction packets delivered with proof"
```

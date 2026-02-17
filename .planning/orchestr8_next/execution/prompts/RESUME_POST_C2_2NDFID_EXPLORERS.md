# Resume Prompt - 2ndFid_explorers (Post-C2)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming `2ndFid_explorers` for packet `P07-C3`.

## Packet

- Packet ID: `P07-C3`
- Scope: deliver next two extraction packets for orchestration UX + observability value.

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
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C3_2NDFID_EXPLORERS.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

3. Send checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-C3; scope=next extraction pair; files=<files>; tests=<tests>; eta=<eta>"
```

4. Generate and follow packet worklist (required):

```bash
scripts/packet_bootstrap.sh P07 P07-C3 <agent_id>
```

5. Enforce prompt/boundary consistency before edits:

```bash
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_C2_2NDFID_EXPLORERS.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C3_2NDFID_EXPLORERS.md
```

## Required outputs

- `.planning/orchestr8_next/artifacts/P07/P07_C3_01_<Name>.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C3_02_<Name>.md`
- Canonical delivery proof (`cp` + `ls -l`)

Canonical delivery proof (required):

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_source_packet_01> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C3_01_<Name>.md
cp <lane_source_packet_02> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C3_02_<Name>.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C3_01_<Name>.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C3_02_<Name>.md
```

Before completion ping (required):

```bash
scripts/packet_closeout.sh P07 P07-C3
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C3 complete; extraction packets delivered with proof"
```

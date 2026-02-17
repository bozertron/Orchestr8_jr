# Resume Prompt - 2ndFid_explorers (P07-C7)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-C7`.

## Packet

- Packet ID: `P07-C7`
- Scope: Extraction packet pair for C2P + CSE accelerators

## Objective

Deliver extraction pair for intent parsing and settings validation patterns.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread 2ndFid_explorers P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C7_2NDFID_EXPLORERS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_01_ExecutionQueueBrowser.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_02_ToolCallCard.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send 2ndFid_explorers codex P07 checkout true "packet=P07-C7; scope=intent parser + settings validator extraction pair; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-C7 2ndFid_explorers
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C6_2NDFID_EXPLORERS.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C7_2NDFID_EXPLORERS.md
```

## Required outputs

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C7_01_*.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C7_02_*.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_output_files> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C7_01_*.md and /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C7_02_*.md
```
Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-C7
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C7 long-run bundle complete; updated TODO + evidence posted"
```

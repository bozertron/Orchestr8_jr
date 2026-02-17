# Resume Prompt - 2ndFid_explorers (Post-C5)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-C6`.

## Packet

- Packet ID: `P07-C6`
- Scope: Produce the next extraction pair for operator decision throughput and state explainability.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread <agent_id> P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C6_2NDFID_EXPLORERS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_01_SessionActivityGraph.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_02_HistoryPanel.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-C6; scope=next extraction pair; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-C6 <agent_id>
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C5_2NDFID_EXPLORERS.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C6_2NDFID_EXPLORERS.md
```

## Required outputs

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_01_*.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_02_*.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp /home/bozertron/2ndFid/extraction_packets/P07_C6_01_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp /home/bozertron/2ndFid/extraction_packets/P07_C6_02_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_01_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C6_02_*.md
```

Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-C6
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C6 complete; extraction packets delivered with proof"
```

# Resume Prompt - 2ndFid_explorers (Post-C4)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-C5`.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread <agent_id> P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C5_2NDFID_EXPLORERS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_01_QuickActions.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C4_02_LayerStack.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-C5; scope=timeline+inspection extraction pair; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-C5 <agent_id>
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C4_2NDFID_EXPLORERS.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C5_2NDFID_EXPLORERS.md
```

## Required outputs

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_01_*.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_02_*.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp /home/bozertron/2ndFid/extraction_packets/P07_C5_01_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp /home/bozertron/2ndFid/extraction_packets/P07_C5_02_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_01_*.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C5_02_*.md
```

Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-C5
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C5 complete; extraction packets delivered with proof"
```

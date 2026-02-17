# Long-Run Mode (Execution Cadence)

Status: Active
Last Updated: 2026-02-16
Authority: Founder directive via Mayor

## Purpose

Reduce setup churn and comms overhead while preserving packet rigor, proof assets, and replay-based acceptance.

## Rules

1. Keep all active lanes developing in parallel unless explicitly blocked.
2. Start each lane run with one kickoff sequence:
- preflight comms
- checkout (`requires_ack=true`)
- worklist generation
- prompt/boundary lint
3. During implementation window:
- no routine micro-checkins
- only blocker/safety/legal escalations interrupt run
4. End each implementation window with one evidence bundle per lane.
5. Mayor performs replay and returns consolidated `accept`/`rework` outcomes after bundle intake.

## Kickoff Sequence (Per Lane)

```bash
scripts/agent_flags.sh unread <agent_id> <phase>
scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex <phase> checkout true "packet=<packet_id>; window=<LONG_RUN_WINDOW_ID>; scope=<scope>; files=<files>; tests=<tests>; eta=<eta>"
scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>
scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>
```

## End-of-Window Bundle (Per Lane)

Required payload:

1. canonical artifact path(s)
2. exact command list used
3. pass counts
4. memory observation IDs
5. closeout result
6. residual risks (`none` if none)

Required gate:

```bash
scripts/packet_closeout.sh <PHASE> <PACKET_ID>
```

Completion ping format:

```bash
OR8_PHASE=<PHASE> /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "<packet_id> long-run bundle posted; evidence ready for replay"
```

## Message Discipline

1. `checkout` and blocker `question/guidance` messages require `requires_ack=true`.
2. Non-blocking progress noise should be avoided during active implementation.
3. Bundle-complete message should include canonical artifact pointer(s).

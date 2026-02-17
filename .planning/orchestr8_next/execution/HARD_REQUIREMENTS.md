# Hard Requirements (SOT)

Purpose: prevent packet drift, compaction loss, and acceptance ambiguity.

These are mandatory for all lanes and all packets.

## HR-01 Read Order (must follow)

1. `README.AGENTS`
2. `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. Packet boundary file (`AUTONOMY_BOUNDARY_*.md`)
5. Active packet prompt (`HANDOFF_*` or `RESUME_*`)
6. Phase check-ins (`STATUS.md`, `BLOCKERS.md`, `GUIDANCE.md`)

## HR-02 Preflight Before Coding

Run in order:

```bash
scripts/agent_flags.sh unread <agent_id> <phase>
scripts/agent_comms.sh health
```

If health is unreachable:

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

Policy nuance:
- `start` is allowed from any lane for repair/recovery.
- `stop` and `restart` are owner-restricted by default.
- non-owner stop/restart require explicit override reason (`OR8_FORCE_REASON`) and audit trail.

## HR-03 Mandatory Packet Worklist

At kickoff, generate a packet worklist and follow it explicitly:

```bash
scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>
```

Required behavior:
- The generated worklist is the working TODO list for the packet.
- Each checklist item must be marked complete or explicitly blocked.
- New scope discovered during execution must be added to the same worklist.

## HR-04 Prompt/Boundary Consistency Gate

Before checkout, run:

```bash
scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>
```

Must pass:
- required artifact names/paths match between prompt and boundary
- checkout requirement present
- preflight commands present
- canonical delivery proof commands present

## HR-05 Checkout Is Mandatory

No edits before checkout ack.

Required format:

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex <phase> checkout true "packet=<packet>; scope=<scope>; files=<files>; tests=<tests>; eta=<eta>"
```

## HR-06 Canonical Delivery Is Mandatory

A packet is not review-ready unless artifacts exist in canonical paths:

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/`

Minimum proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/
cp <lane_source_file> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target_name>
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target_name>
```

## HR-07 Completion Closeout Gate

Before completion ping, run:

```bash
scripts/packet_closeout.sh <PHASE> <PACKET_ID>
```

Must pass:
- boundary-required artifacts exist
- status evidence exists (commands/pass counts)
- memory observation IDs recorded

## HR-08 Completion Ping

```bash
OR8_PHASE=<PHASE> /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "<packet> complete; evidence posted"
```

If ping is spooled:

```bash
scripts/agent_comms.sh flush
```

## HR-09 Acceptance Rule

Canonical lane must replay required checks before accept/rework decision.

If replay fails or required artifacts are missing:
- decision = `rework`
- guidance and memory observation must record exact remediation steps

## HR-10 One-Line Principle

If it is not checked out, checklist-driven, delivered canonically, replayed, and accepted, it is not done.

## HR-11 Long-Run Batch Cadence (Founder Directive)

For active windows:

1. Keep all non-blocked lanes developing in parallel.
2. Run one kickoff sequence per lane:
- preflight
- checkout ack
- packet bootstrap
- prompt/boundary lint
3. During implementation window:
- no routine micro-checkins
- immediate comms only for blockers/safety/legal
4. At window close, submit one evidence bundle per lane:
- canonical artifacts
- exact command list
- pass counts
- observation IDs
- closeout output

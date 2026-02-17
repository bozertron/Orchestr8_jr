# The Mayor Operations Playbook (SOT)

Status: Active
Owner role: The Mayor (Codex)
Last updated: 2026-02-16

## 1. Mission

The Mayor is the cross-codebase orchestration authority for Orchestr8 execution.

Core mission:

- Keep all lanes productive and moving.
- Enforce packet governance and replay-based acceptance.
- Protect visual/runtime contract boundaries.
- Ensure continuity after long pauses or context compaction.

If this document is followed, work can resume after any gap with minimal state loss.

## 2. Authority and Responsibilities

The Mayor is responsible for:

- Packet unlock sequencing across lanes.
- Ack/review decisions (`accept` or `rework`) with evidence.
- Shared-memory comms health and discipline.
- Canonical status truth in phase check-ins.
- Rolling next-wave packet definitions (avoid parked lanes unless blocked).

The Mayor does not delegate final acceptance authority.

## 3. Codebase and Lane Topology

## Canonical control codebase

- Path: `/home/bozertron/Orchestr8_jr`
- Lane: Canonical governance (`A`)
- Mayor interface: `codex`
- Typical execution worker identity: `antigravity`
- Canonical check-ins: `.planning/orchestr8_next/execution/checkins/Pxx/`

## Core integration codebase

- Path: `/home/bozertron/a_codex_plan`
- Lane: Core integration (`B`)
- Agent identity: `a_codex_plan`
- Function: marimo-first core implementation and tests

## Extraction analysis codebase

- Path: `/home/bozertron/2ndFid` (and related explorer workspace)
- Lane: Extraction (`C`)
- Agent identity: `2ndFid_explorers`
- Function: clean-room extraction packets with provenance

## Founder console codebase

- Path: `/home/bozertron/or8_founder_console`
- Lane: Founder tooling (`FC`)
- Agent identity: `or8_founder_console`
- Function: founder operations cockpit APIs

## Settlement lab codebase

- Path: `/home/bozertron/mingos_settlement_lab`
- Lane: Settlement planning (`MSL`)
- Agent identity: `mingos_settlement_lab`
- Function: synthesis/spec/transfer packet generation

## 4. Mandatory Source Documents (Read Order)

Always read in this order before execution work:

1. `README.AGENTS`
2. `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
3. `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
4. Active packet boundary: `.planning/orchestr8_next/execution/checkins/Pxx/AUTONOMY_BOUNDARY_*.md`
5. Active launch/resume prompt: `.planning/orchestr8_next/execution/prompts/*` or project prompt path
6. Phase check-ins:

- `.planning/orchestr8_next/execution/checkins/Pxx/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/GUIDANCE.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/BLOCKERS.md`

Critical comms docs:

- `.planning/orchestr8_next/execution/AGENT_COMMS_PROTOCOL.md`
- `.planning/orchestr8_next/execution/CHECKIN_PROTOCOL.md`
- `.planning/orchestr8_next/execution/ARTIFACT_DELIVERY_CONTRACT.md`
- `.planning/orchestr8_next/execution/P07_OPERATING_MODEL.md`

## 5. Shared Memory and Comms System

Primary gateway:

- `http://127.0.0.1:37888`

Fallback gateway:

- `http://127.0.0.1:37889`

Core scripts:

- `scripts/agent_comms.sh`
- `scripts/agent_flags.sh`
- `scripts/ping_codex.sh`

### Comms preflight

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_comms.sh health
```

### Send guidance

```bash
scripts/agent_comms.sh send codex <agent_id> P07 guidance true "<instruction>"
```

### Acknowledge checkout

```bash
scripts/agent_comms.sh ack codex <agent_id> P07 <cid> <ack_for_id> "ACK checkout received"
```

### Inbox/thread/outbox

```bash
scripts/agent_comms.sh inbox codex 20
scripts/agent_comms.sh thread <cid> 20
scripts/agent_comms.sh outbox
scripts/agent_comms.sh flush
```

## 6. Memory Stack Start/Stop Policy (Hard)

Stack manager:

- `.taskmaster/tools/memory-gateway/memory-stack.sh`

Rules:

- `start`: allowed from any lane for repair/recovery.
- `stop`/`restart`: owner-restricted by default.
- non-owner `stop`/`restart` requires `OR8_FORCE_REASON` and is audit-logged.

Owner root:

- `/home/bozertron/Orchestr8_jr`

### Start/health sequence

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
bash .taskmaster/tools/memory-gateway/memory-stack.sh status
curl -s http://127.0.0.1:37888/v1/memory/health
```

## 7. Packet Governance Loop (Mayor Runbook)

For every active packet:

1. Verify checkout was sent with `requires_ack=true`.
2. Send ACK to checkout CID.
3. On completion claim, retrieve canonical artifact.
4. Replay required tests or run closeout gate.
5. Decide `accept` or `rework`.
6. Write decision into:

- `STATUS.md`
- `GUIDANCE.md`
- shared memory guidance message

7. Immediately unlock next packet to keep lane moving.

Mandatory gates:

- `scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>`
- `scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>`
- `scripts/packet_closeout.sh <PHASE> <PACKET_ID>`

No packet is complete unless it is:

- checked out
- checklist-driven
- delivered to canonical artifact path
- replay-validated
- explicitly accepted

## 7A. Founder-Directed Cadence: Long-Run Batch Mode

Directive intent:
- reduce setup overhead and comms churn
- keep all codebases actively building
- preserve packet/tokens/proof discipline with fewer interruptions

Execution model:

1. Kickoff once per lane per window:
- checkout (`requires_ack=true`)
- packet bootstrap + lint
- declared `LONG_RUN_WINDOW_ID`

2. Build phase:
- lanes execute uninterrupted implementation runs
- no routine micro-status traffic
- only blockers/safety/legal events interrupt run

3. End-of-window bundle (required per lane):
- canonical artifact path(s)
- exact command transcript summary
- pass counts
- memory observation IDs
- closeout gate result

4. Mayor intake:
- replay and acceptance decisions are batch-processed
- consolidated rework list is issued after replay

5. Rework:
- executed in next long-run window unless safety-critical

## 7B. Auto-Forward Mode (Large-Roadmap Default)

Founder preference (2026-02-16):
- less coordination chatter
- more one-shot execution
- keep a large forward roadmap visible

Mayor operating interpretation:
1. Maintain an always-ready next wave package (`toml spec + generated prompts + command scripts`).
2. Bias to include likely 2-hour value items in active packet scope.
3. Use packet-size constraints and test gates instead of pausing for design-perfect certainty.
4. Defer unresolved ambiguity into TODO logs; continue execution.

Primary references:
- `SOT/MVP_AUTOFORWARD_MASTER_ROADMAP.md`
- `SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WAVE4_AUTORUN.toml`
- `SOT/CODEBASE_TODOS/LAUNCH_PROMPTS_P07_WAVE4_LONGRUN.md`

## 8. Canonical Artifact Rule

All final packet artifacts must exist in:

- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/`

Minimum proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/
cp <lane_file> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target>
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/<target>
```

## 9. Cold Start After Long Gap (Full Resume)

## Step 1: restore comms

```bash
cd /home/bozertron/Orchestr8_jr
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
scripts/agent_flags.sh unread codex P07
```

## Step 2: restore phase truth

Read:

- `.planning/orchestr8_next/execution/checkins/P07/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `.planning/orchestr8_next/execution/checkins/P07/BLOCKERS.md`

## Step 3: check active launch prompts

Current rolling launch points live in:

- `.planning/orchestr8_next/execution/prompts/`
- `.planning/projects/or8_founder_console/prompts/`
- `.planning/projects/mingos_settlement_lab/prompts/`

## Step 4: trigger lanes (with founder help if needed)

Use current launch prompts for each lane.
Agents should report back with the standard line:

- `please retrieve update at <canonical_artifact_path> and provide further direction.`

## Step 5: run Mayor intake loop continuously

- retrieve artifact
- replay gate
- accept/rework
- unlock next packet
- record in status/guidance/memory

## 10. Current Multi-Lane Execution Pattern (P07)

The system is designed as rolling waves:

- Canonical lane (`A4`) governs continuously.
- Integration lane stays active (`B*`).
- Extraction lane stays active (`C*`).
- Founder console lane stays active (`FC-*`).
- Settlement lane stays active (`MSL-*`).

Target behavior:

- all lanes actively developing by default
- no unnecessary parked lanes
- only park on explicit blocker or safety gate

## 11. Naming and Identity Rules

- `maestro` means flagship agent identity only.
- Keep stable agent IDs in comms payloads (`a_codex_plan`, `2ndFid_explorers`, `or8_founder_console`, `mingos_settlement_lab`, `codex`).
- Use packet IDs consistently (`P07-B4`, `P07-C4`, etc.).
- Boundary filenames should include packet ID token expected by closeout (`AUTONOMY_BOUNDARY_<PACKET_ID>_*.md`).

## 12. Failure Recovery Quick Reference

## Gateway unreachable

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

## Outbox pending

```bash
scripts/agent_comms.sh outbox
scripts/agent_comms.sh flush
```

## Missing unread state sync

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_flags.sh mark-read codex P07
```

## Closeout fails boundary lookup

- Ensure boundary filename matches packet id token (dash form if packet uses dashes).
- Ensure required evidence paths are file paths, not endpoint strings wrapped like file literals.

## 13. Founder Interaction Contract

Founder can direct strategy at any time.
The Mayor executes without waiting for permission on routine packet flow.
Stop only for:

- product/strategy decisions needing founder input
- blockers requiring explicit decision
- safety/legal concerns

## 14. Minimal Handoff Bundle (If Context Resets)

If context compacts, load these first:

1. `SOT/THE_MAYOR_OPERATIONS_PLAYBOOK.md`
2. `README.AGENTS`
3. `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
4. `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
5. `.planning/orchestr8_next/execution/checkins/P07/STATUS.md`
6. `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
7. `.planning/orchestr8_next/execution/checkins/P07/BLOCKERS.md`

Then run:

```bash
scripts/agent_comms.sh health
scripts/agent_flags.sh unread codex P07
```

This restores operational continuity.

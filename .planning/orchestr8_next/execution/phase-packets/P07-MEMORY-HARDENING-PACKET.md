# Packet: P07-M1 Shared Memory Hardening

## Objective

Stabilize cross-agent communications under concurrent multi-repo execution.

## Root Cause Hypothesis (Validated)

- Each repo has a local `memory-stack.sh` with local PID/state files.
- All stacks default to the same worker/gateway ports:
  - worker `127.0.0.1:37777`
  - gateway `127.0.0.1:37888`
- If multiple repos start/stop/restart independently, they can flap the shared port and create intermittent `curl: (7)` failures.

## Scope

- Harden operational topology and scripts for reliable comms.
- Add explicit per-lane provisioning guidance.
- Add unread-flag system for pending guidance/messages.

## Work Packages

### M1-WP01: Topology Lock + Ownership Rules

1. Establish one memory ownership model:
   - `Orchestr8_jr` owns stack lifecycle (start/stop/restart)
   - other lanes use external gateway only (no local start/stop)
2. Document lane configuration matrix in `README.AGENTS`.
3. Add a guard in scripts to prevent non-owner stop/restart.

Acceptance:
- Non-owner lane cannot accidentally stop shared gateway.
- README contains explicit lane provisioning commands.

### M1-WP02: Multi-Path Gateway and Failover

1. Add optional secondary gateway port and fallback behavior.
2. Update comms scripts to try primary then fallback endpoint.
3. Add exponential backoff retry (bounded) for transient failures.

Acceptance:
- Simulated primary outage still delivers message through fallback.
- Comms command surfaces deterministic error after bounded retries.

### M1-WP03: Outbox Spool (No Message Loss)

1. Add local outbox queue for failed sends.
2. Add flush command to replay queued messages.
3. Annotate replayed messages with original timestamp.

Acceptance:
- Failed send is persisted and replayable.
- Flush reports sent/failed counts.

### M1-WP04: Unread Flag System

1. Implement `scripts/agent_flags.sh` with:
   - unread OR8-COMMS items addressed to agent
   - unread guidance updates per phase (`GUIDANCE.md` mtime/hash tracking)
2. Store per-agent watermark state in a local state file.
3. Optional integrate with `agent_comms.sh inbox` and startup hooks.

Acceptance:
- Agent can run one command and see unread guidance/messages.
- Watermark updates only after explicit ack/read action.

## Deliverables

- `.planning/orchestr8_next/artifacts/P07/M1_MEMORY_HARDENING_REPORT.md`
- `README.AGENTS` updated with lane provisioning matrix
- Updated scripts (`agent_comms.sh`, optional new `agent_flags.sh`)
- Verification logs and command outputs

## Verification Commands

- Health checks under concurrent load
- Send/ack tests from at least 3 lanes
- Forced gateway interruption test + retry/failover behavior
- Unread flags test (new guidance + unread message detection)

## Non-Goals

- Replacing shared memory backend technology in this packet
- Full distributed queue service rollout

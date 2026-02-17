# Handoff Prompt - Shared Memory Hardening Agent

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are assigned packet `P07-M1` for shared memory hardening.

Read first:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/phase-packets/P07-MEMORY-HARDENING-PACKET.md`
- `.taskmaster/tools/memory-gateway/memory-stack.sh`
- `.taskmaster/tools/memory-gateway/server.mjs`
- `scripts/agent_comms.sh`
- `README.AGENTS` (lane provisioning + artifact delivery contract)

## Startup

1. Send checkout to codex (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-M1; scope=memory hardening; files=<list>; eta=<eta>"
```

2. Update `P07` status/blockers before coding.

## Priority Order (Do This First, Not Later)

1. Implement **multi-endpoint failover + lane-aware fallback + outbox spool** first.
2. Ensure no “busy line” stalls execution:
- retries with bounded backoff
- fallback endpoint attempt
- queue unsent messages for replay
3. Then implement unread-flag system.
4. Keep all changes backward compatible with existing OR8-COMMS commands.

## Start/Stop Policy Nuance (Required)

- `start`: should be allowed from any lane for repair/recovery when system is down.
- `stop` and `restart`: must be restricted to owner lane by default.
- non-owner stop/restart allowed only with explicit override + reason trail (auditable).

Implement this policy in scripts and docs so “fix it if broken” is possible, but unauthorized shutdown is blocked.

## Required outputs

- Implement M1-WP01..M1-WP04 or report blockers with evidence.
- Produce report:
  - `.planning/orchestr8_next/artifacts/P07/M1_MEMORY_HARDENING_REPORT.md`
- Include exact commands and outcomes.
- Include canonical artifact delivery proof.

## Critical constraints

- Do not break existing OR8-COMMS semantics.
- Keep changes backward compatible where possible.
- No destructive actions on active memory data.

## Completion

Send completion ping and include:
- tests passed
- failover results
- unread flags demo
- start/stop policy validation results
- memory observation IDs

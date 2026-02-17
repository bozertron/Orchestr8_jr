# P07-M1 Memory Hardening Report

Date: 2026-02-15
Owner: codex_m1 (self-lane)
Packet: P07-M1

## Scope Delivered

1. Multi-endpoint failover with lane-aware endpoint resolution.
2. Bounded retry/backoff and no-stall outbox spool + replay.
3. Unread-flag tracking and watermark flow.
4. Start/stop policy nuance validation:
   - `start` allowed cross-lane for recovery.
   - `stop`/`restart` owner-restricted by default.
   - non-owner override requires explicit `OR8_FORCE_REASON` and writes audit trail.

## Script Updates

- Updated `scripts/agent_comms.sh`:
  - Added `resolve_endpoints()` with lane-aware env support:
    - `MEMORY_GATEWAY_URL_<LANE>`
    - `MEMORY_GATEWAY_FALLBACK_URL_<LANE>`
    - `MEMORY_GATEWAY_URLS_<LANE>` (comma-separated)
    - plus global `MEMORY_GATEWAY_URLS`
  - Hardened outbox serialization to store JSON object payloads when valid.
  - Replaced `sed` replay mutation with `jq` object-safe annotation for `replayed_at` and `original_ts`.
  - Extended `health` output to print lane and resolved endpoints.

- Existing `scripts/agent_flags.sh` validated (unread flags / guidance watermark).
- Existing `.taskmaster/tools/memory-gateway/memory-stack.sh` policy validated with owner/non-owner behavior and audit entries.

## Verification Matrix

### 1) Concurrent lane simulation with no gateway flap
Command:
```bash
seq 1 18 | xargs -I{} -P6 bash -lc 'lane=$(({}%3)); OR8_LANE="sim_lane_${lane}" scripts/agent_comms.sh send "sim_lane_${lane}" codex P07 progress false "M1 concurrent lane probe {}"'
```
Evidence:
- 18 sends succeeded (`saved_id=1478..1495`)
- health remained `status: ok`
- outbox remained `outbox_pending: 0`

### 2) Transient primary failure with fallback success
Command:
```bash
MEMORY_GATEWAY_URL=http://127.0.0.1:37999 \
MEMORY_GATEWAY_FALLBACK_URL=http://127.0.0.1:37888 \
OR8_MAX_RETRIES=1 OR8_BACKOFF_BASE=0 OR8_LANE=failover_probe \
scripts/agent_comms.sh send failover_probe codex P07 progress false \
"M1 transient primary failure with fallback success (captured)"
```
Evidence:
- `saved_id=1497`
- Fallback succeeded and message persisted.

### 3) Outbox replay success
Commands:
```bash
scripts/agent_comms.sh outbox
MEMORY_GATEWAY_URL=http://127.0.0.1:37998 MEMORY_GATEWAY_FALLBACK_URL=http://127.0.0.1:37999 \
OR8_MAX_RETRIES=1 OR8_BACKOFF_BASE=0 OR8_LANE=outbox_probe \
scripts/agent_comms.sh send outbox_probe codex P07 progress false "M1 force spool for replay"
scripts/agent_comms.sh flush
scripts/agent_comms.sh outbox
```
Evidence:
- Forced spool created (`saved_id=unknown`, `OUTBOX: message spooled -> ...`).
- Replay succeeded: `outbox flush: total=7 sent=7 failed=0`
- Final queue: `outbox_pending: 0`

### 4) Unread flags demo
Commands:
```bash
scripts/agent_flags.sh reset codex_m1_watch
scripts/agent_comms.sh send codex codex_m1_watch P07 guidance true "M1 unread flags probe"
scripts/agent_flags.sh unread codex_m1_watch P07
scripts/agent_flags.sh mark-read codex_m1_watch P07
scripts/agent_flags.sh unread codex_m1_watch P07
```
Evidence:
- Before mark-read: `unread_messages: 50`, `guidance_P07: UPDATED (unread)`
- After mark-read: `unread_messages: 0`, `guidance_P07: up-to-date`

### 5) Start/stop policy validation
Non-owner denied (no override):
```bash
cd /tmp/non_owner_repo && OR8_LANE=non_owner_test bash .taskmaster/tools/memory-gateway/memory-stack.sh stop
cd /tmp/non_owner_repo && OR8_LANE=non_owner_test bash .taskmaster/tools/memory-gateway/memory-stack.sh restart
```
Evidence:
- `ERROR: stop restricted to owner lane ...`
- `ERROR: restart restricted to owner lane ...`

Non-owner start allowed + non-owner stop with override:
```bash
cd /tmp/non_owner_repo && OR8_LANE=non_owner_test MEMORY_GATEWAY_PORT=37995 CLAUDE_MEM_WORKER_PORT=37795 \
  bash .taskmaster/tools/memory-gateway/memory-stack.sh start
cd /tmp/non_owner_repo && OR8_LANE=non_owner_test OR8_FORCE_REASON="cleanup stub service" MEMORY_GATEWAY_PORT=37995 CLAUDE_MEM_WORKER_PORT=37795 \
  bash .taskmaster/tools/memory-gateway/memory-stack.sh stop
```
Evidence:
- start succeeded in non-owner lane (`gateway started ...`, health ok on 37995)
- override stop succeeded with warning and reason trail.
- audit log entries include:
  - `action=stop-DENIED`
  - `action=restart-DENIED`
  - `action=start ... reason=recovery-allowed`
  - `action=stop ... reason=cleanup stub service`

## Pass Counts

- Scenario checks: 5/5 passed.
- Script syntax checks: 3/3 passed (`bash -n` on comms, flags, memory-stack).

## Evidence Files

- `/tmp/p07_m1_verify/01_concurrent_send.txt`
- `/tmp/p07_m1_verify/02_failover_send_success.txt`
- `/tmp/p07_m1_verify/03_flush_result.txt`
- `/tmp/p07_m1_verify/04_flags_unread_before_mark.txt`
- `/tmp/p07_m1_verify/04_flags_unread_after_mark.txt`
- `/tmp/p07_m1_verify/05_policy_stop_denied.txt`
- `/tmp/p07_m1_verify/05_policy_restart_denied.txt`
- `/tmp/p07_m1_verify/05_policy_start_allowed_escalated.txt`
- `/tmp/p07_m1_verify/05_policy_stop_override_escalated.txt`
- `/tmp/p07_m1_verify/05_policy_audit_escalated.log`

## Canonical Artifact Delivery Proof

Command:
```bash
install -d .planning/orchestr8_next/artifacts/P07 && \
cp /tmp/p07_m1_verify/M1_MEMORY_HARDENING_REPORT.md .planning/orchestr8_next/artifacts/P07/M1_MEMORY_HARDENING_REPORT.md && \
ls -l .planning/orchestr8_next/artifacts/P07/M1_MEMORY_HARDENING_REPORT.md
```

Output:
```text
-rw-r--r--. 1 bozertron bozertron 5016 Feb 15 15:18 .planning/orchestr8_next/artifacts/P07/M1_MEMORY_HARDENING_REPORT.md
```

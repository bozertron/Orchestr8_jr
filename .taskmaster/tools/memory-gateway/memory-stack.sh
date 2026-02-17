#!/usr/bin/env bash
set -euo pipefail

# P07-M1 Hardened memory-stack with ownership guards.
# - start: allowed from any lane (repair/recovery).
# - stop/restart: owner-restricted by default; override with OR8_FORCE_REASON.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WORKER_CLI="$ROOT/.taskmaster/tools/claude-mem/plugin/scripts/worker-cli.js"
GATEWAY_SERVER="$ROOT/.taskmaster/tools/memory-gateway/server.mjs"

CLAUDE_MEM_DATA_DIR="${CLAUDE_MEM_DATA_DIR:-$HOME/.claude-mem}"
CLAUDE_MEM_WORKER_HOST="${CLAUDE_MEM_WORKER_HOST:-127.0.0.1}"
CLAUDE_MEM_WORKER_PORT="${CLAUDE_MEM_WORKER_PORT:-37777}"
MEMORY_GATEWAY_HOST="${MEMORY_GATEWAY_HOST:-127.0.0.1}"
MEMORY_GATEWAY_PORT="${MEMORY_GATEWAY_PORT:-37888}"

# --- Ownership model ---
# Canonical owner repo root (Orchestr8_jr). Only this repo may stop/restart
# without an explicit override.
OWNER_ROOT="/home/bozertron/Orchestr8_jr"
OR8_LANE="${OR8_LANE:-}"
OR8_FORCE_REASON="${OR8_FORCE_REASON:-}"

STATE_DIR="$ROOT/.taskmaster/memory"
PID_DIR="$STATE_DIR/pids"
LOG_DIR="$STATE_DIR/logs"
AUDIT_LOG="$LOG_DIR/ownership-audit.log"
GATEWAY_PID_FILE="$PID_DIR/memory-gateway.pid"
GATEWAY_LOG_FILE="$LOG_DIR/memory-gateway.log"

mkdir -p "$CLAUDE_MEM_DATA_DIR" "$PID_DIR" "$LOG_DIR"

# --- Ownership guard ---
is_owner() {
  [[ "$(cd "$ROOT" && pwd)" == "$OWNER_ROOT" ]]
}

audit_entry() {
  local action="$1" who="$2" reason="$3"
  printf '%s | action=%s | lane=%s | root=%s | reason=%s\n' \
    "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$action" "$who" "$ROOT" "$reason" \
    >> "$AUDIT_LOG"
}

require_owner_or_override() {
  local action="$1"
  if is_owner; then
    audit_entry "$action" "owner" "owner-lane"
    return 0
  fi
  if [[ -n "$OR8_FORCE_REASON" ]]; then
    echo "WARNING: non-owner $action with override: $OR8_FORCE_REASON" >&2
    audit_entry "$action" "${OR8_LANE:-non-owner}" "$OR8_FORCE_REASON"
    return 0
  fi
  echo "ERROR: $action restricted to owner lane ($OWNER_ROOT)." >&2
  echo "  Set OR8_FORCE_REASON=\"<auditable reason>\" to override." >&2
  audit_entry "${action}-DENIED" "${OR8_LANE:-non-owner}" "no override"
  return 1
}

usage() {
  cat <<'EOF'
Usage: memory-stack.sh <start|stop|restart|status>

Ownership policy (P07-M1):
  start   - allowed from ANY lane (repair/recovery)
  stop    - owner-only by default; override with OR8_FORCE_REASON
  restart - owner-only by default; override with OR8_FORCE_REASON
  status  - unrestricted

Environment overrides:
  CLAUDE_MEM_DATA_DIR     default: ~/.claude-mem
  CLAUDE_MEM_WORKER_HOST  default: 127.0.0.1
  CLAUDE_MEM_WORKER_PORT  default: 37777
  MEMORY_GATEWAY_HOST     default: 127.0.0.1
  MEMORY_GATEWAY_PORT     default: 37888
  OR8_LANE                lane identity (for audit trail)
  OR8_FORCE_REASON        non-owner override reason (required for stop/restart)
EOF
}

gateway_running() {
  if [[ ! -f "$GATEWAY_PID_FILE" ]]; then
    return 1
  fi
  local pid
  pid="$(cat "$GATEWAY_PID_FILE" 2>/dev/null || true)"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

start_worker() {
  CLAUDE_MEM_DATA_DIR="$CLAUDE_MEM_DATA_DIR" \
  CLAUDE_MEM_WORKER_HOST="$CLAUDE_MEM_WORKER_HOST" \
  CLAUDE_MEM_WORKER_PORT="$CLAUDE_MEM_WORKER_PORT" \
    bun "$WORKER_CLI" start >/dev/null
}

stop_worker() {
  CLAUDE_MEM_DATA_DIR="$CLAUDE_MEM_DATA_DIR" \
  CLAUDE_MEM_WORKER_HOST="$CLAUDE_MEM_WORKER_HOST" \
  CLAUDE_MEM_WORKER_PORT="$CLAUDE_MEM_WORKER_PORT" \
    bun "$WORKER_CLI" stop >/dev/null || true
}

start_gateway() {
  if gateway_running; then
    echo "gateway already running (pid $(cat "$GATEWAY_PID_FILE"))"
    return 0
  fi

  CLAUDE_MEM_DATA_DIR="$CLAUDE_MEM_DATA_DIR" \
  CLAUDE_MEM_WORKER_HOST="$CLAUDE_MEM_WORKER_HOST" \
  CLAUDE_MEM_WORKER_PORT="$CLAUDE_MEM_WORKER_PORT" \
  MEMORY_GATEWAY_HOST="$MEMORY_GATEWAY_HOST" \
  MEMORY_GATEWAY_PORT="$MEMORY_GATEWAY_PORT" \
    nohup node "$GATEWAY_SERVER" >>"$GATEWAY_LOG_FILE" 2>&1 &

  echo $! > "$GATEWAY_PID_FILE"
  sleep 1
  if gateway_running; then
    echo "gateway started (pid $(cat "$GATEWAY_PID_FILE"))"
  else
    echo "gateway failed to start; check $GATEWAY_LOG_FILE"
    return 1
  fi
}

stop_gateway() {
  if ! gateway_running; then
    rm -f "$GATEWAY_PID_FILE"
    echo "gateway already stopped"
    return 0
  fi

  local pid
  pid="$(cat "$GATEWAY_PID_FILE")"
  kill "$pid" 2>/dev/null || true
  sleep 1

  if kill -0 "$pid" 2>/dev/null; then
    kill -9 "$pid" 2>/dev/null || true
  fi
  rm -f "$GATEWAY_PID_FILE"
  echo "gateway stopped"
}

status_stack() {
  echo "claude-mem data dir: $CLAUDE_MEM_DATA_DIR"
  echo "worker: $CLAUDE_MEM_WORKER_HOST:$CLAUDE_MEM_WORKER_PORT"
  echo "gateway: $MEMORY_GATEWAY_HOST:$MEMORY_GATEWAY_PORT"

  CLAUDE_MEM_DATA_DIR="$CLAUDE_MEM_DATA_DIR" \
  CLAUDE_MEM_WORKER_HOST="$CLAUDE_MEM_WORKER_HOST" \
  CLAUDE_MEM_WORKER_PORT="$CLAUDE_MEM_WORKER_PORT" \
    bun "$WORKER_CLI" status || true

  if gateway_running; then
    echo "gateway pid: $(cat "$GATEWAY_PID_FILE")"
  else
    echo "gateway pid: not running"
  fi

  if command -v curl >/dev/null 2>&1; then
    echo "health:"
    curl -fsS "http://$MEMORY_GATEWAY_HOST:$MEMORY_GATEWAY_PORT/v1/memory/health" || true
    echo
  fi
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

case "$1" in
  start)
    # Start is allowed from any lane for repair/recovery
    audit_entry "start" "${OR8_LANE:-$(is_owner && echo owner || echo non-owner)}" "recovery-allowed"
    start_worker
    start_gateway
    status_stack
    ;;
  stop)
    require_owner_or_override "stop" || exit 1
    stop_gateway
    stop_worker
    status_stack
    ;;
  restart)
    require_owner_or_override "restart" || exit 1
    stop_gateway || true
    stop_worker || true
    start_worker
    start_gateway
    status_stack
    ;;
  status)
    status_stack
    ;;
  *)
    usage
    exit 1
    ;;
esac

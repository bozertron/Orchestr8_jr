#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WORKER_CLI="$ROOT/.taskmaster/tools/claude-mem/plugin/scripts/worker-cli.js"
GATEWAY_SERVER="$ROOT/.taskmaster/tools/memory-gateway/server.mjs"

CLAUDE_MEM_DATA_DIR="${CLAUDE_MEM_DATA_DIR:-$HOME/.claude-mem}"
CLAUDE_MEM_WORKER_HOST="${CLAUDE_MEM_WORKER_HOST:-127.0.0.1}"
CLAUDE_MEM_WORKER_PORT="${CLAUDE_MEM_WORKER_PORT:-37777}"
MEMORY_GATEWAY_HOST="${MEMORY_GATEWAY_HOST:-127.0.0.1}"
MEMORY_GATEWAY_PORT="${MEMORY_GATEWAY_PORT:-37888}"

STATE_DIR="$ROOT/.taskmaster/memory"
PID_DIR="$STATE_DIR/pids"
LOG_DIR="$STATE_DIR/logs"
GATEWAY_PID_FILE="$PID_DIR/memory-gateway.pid"
GATEWAY_LOG_FILE="$LOG_DIR/memory-gateway.log"

mkdir -p "$CLAUDE_MEM_DATA_DIR" "$PID_DIR" "$LOG_DIR"

usage() {
  cat <<'EOF'
Usage: memory-stack.sh <start|stop|restart|status>

Environment overrides:
  CLAUDE_MEM_DATA_DIR     default: ~/.claude-mem
  CLAUDE_MEM_WORKER_HOST  default: 127.0.0.1
  CLAUDE_MEM_WORKER_PORT  default: 37777
  MEMORY_GATEWAY_HOST     default: 127.0.0.1
  MEMORY_GATEWAY_PORT     default: 37888
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
    start_worker
    start_gateway
    status_stack
    ;;
  stop)
    stop_gateway
    stop_worker
    status_stack
    ;;
  restart)
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

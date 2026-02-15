#!/usr/bin/env bash
set -euo pipefail

# Quick progress ping to Codex over OR8-COMMS.
# Can be run from any directory.

ROOT="/home/bozertron/Orchestr8_jr"
COMMS="${ROOT}/scripts/agent_comms.sh"

AGENT="${AGENT_NAME:-antigravity}"
PHASE="${OR8_PHASE:-P05}"
KIND="${OR8_KIND:-progress}"
REQUIRES_ACK="${OR8_ACK:-false}"

usage() {
  cat <<'EOF'
Usage:
  /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh <percent> <message...>

Examples:
  /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 35 "Contracts done; starting tests"
  OR8_PHASE=P06 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 80 "Gate evidence uploaded"
  OR8_ACK=true /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "WP01 complete; please confirm"
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

if [[ ! -x "$COMMS" ]]; then
  echo "ERROR: comms script not found/executable: $COMMS" >&2
  exit 2
fi

percent="$1"
shift
msg="$*"
ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

"$COMMS" send "$AGENT" codex "$PHASE" "$KIND" "$REQUIRES_ACK" "[${percent}%] ${msg} (ts=${ts})"

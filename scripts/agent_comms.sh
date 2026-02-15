#!/usr/bin/env bash
set -euo pipefail

# Orchestr8 cross-agent messaging over shared memory gateway.
# Protocol: OR8-COMMS v1

BASE_URL="${MEMORY_GATEWAY_URL:-http://127.0.0.1:37888}"
PROTO="or8-comms-v1"

usage() {
  cat <<'EOF'
Usage:
  scripts/agent_comms.sh health
  scripts/agent_comms.sh send <from> <to> <phase> <kind> <requires_ack:true|false> <message...>
  scripts/agent_comms.sh ack <from> <to> <phase> <cid> <ack_for_id> <message...>
  scripts/agent_comms.sh inbox <agent> [limit]
  scripts/agent_comms.sh thread <cid> [limit]

Examples:
  scripts/agent_comms.sh send codex antigravity P05 guidance true "Run P05-WP01 only."
  scripts/agent_comms.sh inbox antigravity 10
  scripts/agent_comms.sh ack antigravity codex P05 p05-cid-123 1427 "Ack received."
  scripts/agent_comms.sh thread p05-cid-123 20
EOF
}

json_escape() {
  printf '%s' "${1:-}" \
    | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e ':a' -e 'N' -e '$!ba' -e 's/\n/\\n/g'
}

urlencode_min() {
  local s="${1:-}"
  s="${s// /%20}"
  s="${s//=/%3D}"
  s="${s//\"/%22}"
  printf '%s' "$s"
}

now_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

gen_cid() {
  local from="$1"
  local to="$2"
  local phase="$3"
  printf '%s' "cid-$(date +%s%3N)-${phase}-${from}-to-${to}"
}

save_observation() {
  local title="$1"
  local text="$2"
  local payload
  payload="{\"title\":\"$(json_escape "$title")\",\"text\":\"$(json_escape "$text")\"}"
  curl -sS -X POST "${BASE_URL}/v1/memory/save" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

extract_saved_id() {
  sed -n 's/.*"id":[[:space:]]*\([0-9][0-9]*\).*/\1/p' | head -n 1
}

search_ids() {
  local query="$1"
  local limit="${2:-10}"
  local encoded
  encoded="$(urlencode_min "$query")"
  curl -sS "${BASE_URL}/v1/memory/search?query=${encoded}&limit=${limit}" \
    | grep -o '#[0-9]\+' \
    | tr -d '#'
}

ids_to_json_array() {
  local ids_csv="$1"
  awk -F',' '{
    printf "[";
    for (i = 1; i <= NF; i++) {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $i);
      if ($i ~ /^[0-9]+$/) {
        printf "%s%s", $i, (i < NF ? "," : "");
      }
    }
    printf "]";
  }' <<<"$ids_csv"
}

fetch_observations() {
  local ids_csv="$1"
  local ids_json
  ids_json="$(ids_to_json_array "$ids_csv")"
  curl -s -X POST "${BASE_URL}/v1/memory/observations" \
    -H "Content-Type: application/json" \
    -d "{\"ids\":${ids_json}}"
}

cmd_health() {
  curl -s "${BASE_URL}/v1/memory/health"
}

cmd_send() {
  if [[ $# -lt 6 ]]; then
    usage
    exit 1
  fi
  local from="$1"
  local to="$2"
  local phase="$3"
  local kind="$4"
  local requires_ack="$5"
  shift 5
  local body="$*"
  local cid
  cid="$(gen_cid "$from" "$to" "$phase")"
  local ts
  ts="$(now_utc)"

  local title="OR8-COMMS to=${to} from=${from} kind=${kind} phase=${phase} cid=${cid}"
  local text
  text="{\"protocol\":\"${PROTO}\",\"to\":\"${to}\",\"from\":\"${from}\",\"phase\":\"${phase}\",\"kind\":\"${kind}\",\"cid\":\"${cid}\",\"requires_ack\":${requires_ack},\"ts\":\"${ts}\",\"body\":\"$(json_escape "$body")\"}"

  local resp
  resp="$(save_observation "$title" "$text")"
  local id
  id="$(printf '%s' "$resp" | extract_saved_id)"

  printf 'saved_id=%s\ncid=%s\n' "${id:-unknown}" "$cid"
  printf '%s\n' "$resp"
}

cmd_ack() {
  if [[ $# -lt 6 ]]; then
    usage
    exit 1
  fi
  local from="$1"
  local to="$2"
  local phase="$3"
  local cid="$4"
  local ack_for_id="$5"
  shift 5
  local body="$*"
  local ts
  ts="$(now_utc)"

  local title="OR8-COMMS to=${to} from=${from} kind=ack phase=${phase} cid=${cid} ack_for=${ack_for_id}"
  local text
  text="{\"protocol\":\"${PROTO}\",\"to\":\"${to}\",\"from\":\"${from}\",\"phase\":\"${phase}\",\"kind\":\"ack\",\"cid\":\"${cid}\",\"ack_for\":${ack_for_id},\"requires_ack\":false,\"ts\":\"${ts}\",\"body\":\"$(json_escape "$body")\"}"

  local resp
  resp="$(save_observation "$title" "$text")"
  local id
  id="$(printf '%s' "$resp" | extract_saved_id)"

  printf 'saved_id=%s\ncid=%s\nack_for=%s\n' "${id:-unknown}" "$cid" "$ack_for_id"
  printf '%s\n' "$resp"
}

cmd_inbox() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi
  local agent="$1"
  local limit="${2:-10}"
  local query="OR8-COMMS ${agent}"
  local ids
  ids="$(search_ids "$query" "$limit" | sort -n | uniq | paste -sd, -)"

  if [[ -z "$ids" ]]; then
    echo "No messages found for agent=${agent}"
    exit 0
  fi

  echo "Message IDs: $ids"
  local obs
  obs="$(fetch_observations "$ids")"
  printf '%s\n' "$obs" \
    | jq --arg prefix "OR8-COMMS to=${agent} " '[ .[] | select((.title // "") | startswith($prefix)) ]'
}

cmd_thread() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi
  local cid="$1"
  local limit="${2:-20}"
  local query="${cid}"
  local ids
  ids="$(search_ids "$query" "$limit" | sort -n | uniq | paste -sd, -)"

  if [[ -z "$ids" ]]; then
    echo "No messages found for cid=${cid}"
    exit 0
  fi

  echo "Message IDs: $ids"
  local obs
  obs="$(fetch_observations "$ids")"
  printf '%s\n' "$obs" \
    | jq --arg needle "cid=${cid}" '[ .[] | select((.title // "") | contains($needle)) ]'
}

main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi
  local cmd="$1"
  shift

  case "$cmd" in
    health) cmd_health "$@" ;;
    send) cmd_send "$@" ;;
    ack) cmd_ack "$@" ;;
    inbox) cmd_inbox "$@" ;;
    thread) cmd_thread "$@" ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"

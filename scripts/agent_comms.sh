#!/usr/bin/env bash
set -euo pipefail

# Orchestr8 cross-agent messaging over shared memory gateway.
# Protocol: OR8-COMMS v1
# P07-M1: multi-endpoint failover, bounded retry/backoff, outbox spool.

# --- Endpoint configuration (primary + fallback + lane-aware overrides) ---
OR8_LANE="${OR8_LANE:-default}"
OR8_PRIMARY_URL="${MEMORY_GATEWAY_URL:-http://127.0.0.1:37888}"
OR8_FALLBACK_URL="${MEMORY_GATEWAY_FALLBACK_URL:-http://127.0.0.1:37889}"
OR8_ENDPOINTS_RAW="${MEMORY_GATEWAY_URLS:-}"
PROTO="or8-comms-v1"

# --- Retry/backoff config ---
OR8_MAX_RETRIES="${OR8_MAX_RETRIES:-3}"
OR8_BACKOFF_BASE="${OR8_BACKOFF_BASE:-1}"   # seconds
OR8_BACKOFF_MAX="${OR8_BACKOFF_MAX:-8}"     # cap

# --- Outbox spool ---
OR8_OUTBOX_DIR="${OR8_OUTBOX_DIR:-/home/bozertron/Orchestr8_jr/.orchestr8/state/outbox}"
mkdir -p "$OR8_OUTBOX_DIR"

usage() {
  cat <<'EOF'
Usage:
  scripts/agent_comms.sh health
  scripts/agent_comms.sh send <from> <to> <phase> <kind> <requires_ack:true|false> <message...>
  scripts/agent_comms.sh ack <from> <to> <phase> <cid> <ack_for_id> <message...>
  scripts/agent_comms.sh inbox <agent> [limit]
  scripts/agent_comms.sh thread <cid> [limit]
  scripts/agent_comms.sh flush              # replay spooled outbox messages
  scripts/agent_comms.sh outbox             # list pending outbox items

Examples:
  scripts/agent_comms.sh send codex antigravity P07 guidance true "Run P07-B5 only."
  scripts/agent_comms.sh inbox antigravity 10
  scripts/agent_comms.sh ack antigravity codex P07 p07-cid-123 1427 "Ack received."
  scripts/agent_comms.sh thread p07-cid-123 20
  scripts/agent_comms.sh flush
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

# --- Resilient HTTP with failover + bounded retry/backoff ---
resolve_endpoints() {
  local lane_key
  lane_key="$(printf '%s' "$OR8_LANE" | tr '[:lower:]-' '[:upper:]_')"
  local lane_primary_var="MEMORY_GATEWAY_URL_${lane_key}"
  local lane_fallback_var="MEMORY_GATEWAY_FALLBACK_URL_${lane_key}"
  local lane_urls_var="MEMORY_GATEWAY_URLS_${lane_key}"
  local lane_primary="${!lane_primary_var:-$OR8_PRIMARY_URL}"
  local lane_fallback="${!lane_fallback_var:-$OR8_FALLBACK_URL}"
  local configured="${!lane_urls_var:-$OR8_ENDPOINTS_RAW}"
  local endpoints=()

  if [[ -n "$configured" ]]; then
    local raw item trimmed
    IFS=',' read -r -a raw <<< "$configured"
    for item in "${raw[@]}"; do
      trimmed="$(printf '%s' "$item" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
      [[ -n "$trimmed" ]] && endpoints+=("$trimmed")
    done
  else
    endpoints+=("$lane_primary" "$lane_fallback")
  fi

  # Deduplicate while preserving order.
  local ep
  local seen=","
  for ep in "${endpoints[@]}"; do
    if [[ "$seen" != *",$ep,"* ]]; then
      echo "$ep"
      seen="${seen}${ep},"
    fi
  done
}

_curl_with_failover() {
  # Attempts: primary -> fallback, each with bounded exponential backoff.
  # Returns curl output on first success, or spools to outbox on total failure.
  local method="$1"; shift
  local path="$1"; shift
  # remaining args are extra curl flags (e.g. -d payload)

  local endpoints=()
  mapfile -t endpoints < <(resolve_endpoints)
  if [[ "${#endpoints[@]}" -eq 0 ]]; then
    printf '{"error":"no_endpoints_configured"}'
    return 1
  fi
  local attempt=0 delay="$OR8_BACKOFF_BASE" rc=0 output=""

  for ep in "${endpoints[@]}"; do
    attempt=0
    delay="$OR8_BACKOFF_BASE"
    while (( attempt < OR8_MAX_RETRIES )); do
      output=$(curl -sS --max-time 10 -X "$method" "${ep}${path}" "$@" 2>&1) && rc=0 || rc=$?
      if [[ $rc -eq 0 && "$output" != *'"error"'* ]]; then
        printf '%s' "$output"
        return 0
      fi
      attempt=$((attempt + 1))
      if (( attempt < OR8_MAX_RETRIES )); then
        sleep "$delay"
        delay=$(( delay * 2 ))
        (( delay > OR8_BACKOFF_MAX )) && delay=$OR8_BACKOFF_MAX
      fi
    done
  done

  # Total failure — return last output and non-zero
  printf '%s' "$output"
  return 1
}

_spool_to_outbox() {
  local title="$1" payload="$2" orig_ts="$3"
  local spool_file="${OR8_OUTBOX_DIR}/$(date +%s%N).json"
  local payload_json
  if payload_json="$(printf '%s' "$payload" | jq -c . 2>/dev/null)"; then
    :
  else
    payload_json="$(printf '%s' "$payload" | jq -Rs .)"
  fi
  printf '{"title":%s,"payload":%s,"original_ts":"%s","spooled_at":"%s"}\n' \
    "$(printf '%s' "$title" | jq -Rs .)" \
    "$payload_json" \
    "$orig_ts" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > "$spool_file"
  echo "OUTBOX: message spooled -> $spool_file" >&2
}

save_observation() {
  local title="$1"
  local text="$2"
  local payload
  payload="{\"title\":\"$(json_escape "$title")\",\"text\":\"$(json_escape "$text")\"}"

  local resp
  if resp=$(_curl_with_failover POST "/v1/memory/save" \
    -H "Content-Type: application/json" \
    -d "$payload"); then
    printf '%s' "$resp"
  else
    # Spool failed message to outbox for later replay
    _spool_to_outbox "$title" "$payload" "$(now_utc)"
    printf '{"spooled":true,"title":"%s"}' "$(json_escape "$title")"
  fi
}

extract_saved_id() {
  sed -n 's/.*"id":[[:space:]]*\([0-9][0-9]*\).*/\1/p' | head -n 1
}

search_ids() {
  local query="$1"
  local limit="${2:-10}"
  local encoded
  encoded="$(urlencode_min "$query")"
  _curl_with_failover GET "/v1/memory/search?query=${encoded}&limit=${limit}" \
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
  _curl_with_failover POST "/v1/memory/observations" \
    -H "Content-Type: application/json" \
    -d "{\"ids\":${ids_json}}"
}

cmd_health() {
  echo "lane: $OR8_LANE"
  echo "primary_default: $OR8_PRIMARY_URL"
  echo "fallback_default: $OR8_FALLBACK_URL"
  echo "endpoints_resolved:"
  resolve_endpoints | sed 's/^/  - /'
  echo "outbox_dir: $OR8_OUTBOX_DIR"
  echo "outbox_pending: $(find "$OR8_OUTBOX_DIR" -name '*.json' 2>/dev/null | wc -l)"
  echo "---"
  _curl_with_failover GET "/v1/memory/health" || echo '{"status":"unreachable"}'
}

# --- WP03: Outbox flush (replay spooled messages) ---
cmd_flush() {
  local sent=0 failed=0 total=0
  local files
  files=$(find "$OR8_OUTBOX_DIR" -name '*.json' -type f 2>/dev/null | sort)
  if [[ -z "$files" ]]; then
    echo "outbox: empty (0 pending)"
    return 0
  fi

  for f in $files; do
    total=$((total + 1))
    local payload orig_ts replayed_at annotated
    payload=$(jq -c '.payload // .' "$f" 2>/dev/null || cat "$f")
    orig_ts=$(jq -r '.original_ts // "unknown"' "$f" 2>/dev/null || echo "unknown")
    replayed_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    # Annotate replayed message with replay/original timestamps.
    if ! annotated="$(printf '%s' "$payload" | jq -c \
      --arg replayed_at "$replayed_at" \
      --arg original_ts "$orig_ts" \
      'if type == "object" then
         . + {replayed_at:$replayed_at, original_ts:$original_ts}
       else
         {title:"OR8-OUTBOX-REPLAY", text:(tostring), replayed_at:$replayed_at, original_ts:$original_ts}
       end' 2>/dev/null)"; then
      annotated="$(jq -nc \
        --arg text "$payload" \
        --arg replayed_at "$replayed_at" \
        --arg original_ts "$orig_ts" \
        '{title:"OR8-OUTBOX-REPLAY", text:$text, replayed_at:$replayed_at, original_ts:$original_ts}')"
    fi

    if _curl_with_failover POST "/v1/memory/save" \
      -H "Content-Type: application/json" \
      -d "$annotated" >/dev/null 2>&1; then
      sent=$((sent + 1))
      rm -f "$f"
    else
      failed=$((failed + 1))
    fi
  done

  echo "outbox flush: total=$total sent=$sent failed=$failed"
}

cmd_outbox() {
  local count
  count=$(find "$OR8_OUTBOX_DIR" -name '*.json' -type f 2>/dev/null | wc -l)
  echo "outbox_pending: $count"
  if (( count > 0 )); then
    find "$OR8_OUTBOX_DIR" -name '*.json' -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | awk '{print $2}'
  fi
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
    flush) cmd_flush "$@" ;;
    outbox) cmd_outbox "$@" ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"

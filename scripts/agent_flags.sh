#!/usr/bin/env bash
set -euo pipefail

# P07-M1 WP04: Unread flag system for OR8-COMMS messages and guidance updates.
# Tracks per-agent watermarks so agents see only new items.

ROOT="/home/bozertron/Orchestr8_jr"
COMMS="${ROOT}/scripts/agent_comms.sh"
STATE_DIR="${ROOT}/.orchestr8/state/flags"
CHECKINS_DIR="${ROOT}/.planning/orchestr8_next/execution/checkins"

mkdir -p "$STATE_DIR"

usage() {
  cat <<'EOF'
Usage:
  scripts/agent_flags.sh unread <agent> [phase]     # show unread messages + guidance
  scripts/agent_flags.sh mark-read <agent> [phase]  # update watermark (ack all current)
  scripts/agent_flags.sh status <agent>             # summary: unread counts
  scripts/agent_flags.sh reset <agent>              # clear watermarks (see everything again)

Environment:
  MEMORY_GATEWAY_URL   default: http://127.0.0.1:37888

Examples:
  scripts/agent_flags.sh unread codex P07
  scripts/agent_flags.sh mark-read codex P07
  scripts/agent_flags.sh status codex
EOF
}

# --- Watermark file paths ---
_msg_watermark() { echo "${STATE_DIR}/${1}.msg_watermark"; }
_guidance_watermark() { echo "${STATE_DIR}/${1}.guidance_watermark"; }

# --- Message watermark: highest seen observation ID ---
get_msg_watermark() {
  local agent="$1"
  local wm_file
  wm_file="$(_msg_watermark "$agent")"
  if [[ -f "$wm_file" ]]; then
    cat "$wm_file"
  else
    echo "0"
  fi
}

set_msg_watermark() {
  local agent="$1" new_wm="$2"
  echo "$new_wm" > "$(_msg_watermark "$agent")"
}

# --- Guidance watermark: md5 hash of GUIDANCE.md mtime+size ---
_guidance_fingerprint() {
  local phase="$1"
  local gfile="${CHECKINS_DIR}/${phase}/GUIDANCE.md"
  if [[ -f "$gfile" ]]; then
    stat -c '%Y_%s' "$gfile" 2>/dev/null || stat -f '%m_%z' "$gfile" 2>/dev/null || echo "missing"
  else
    echo "missing"
  fi
}

get_guidance_watermark() {
  local agent="$1" phase="$2"
  local wm_file
  wm_file="${STATE_DIR}/${agent}.guidance_${phase}"
  if [[ -f "$wm_file" ]]; then
    cat "$wm_file"
  else
    echo "none"
  fi
}

set_guidance_watermark() {
  local agent="$1" phase="$2" fingerprint="$3"
  echo "$fingerprint" > "${STATE_DIR}/${agent}.guidance_${phase}"
}

# --- Unread messages ---
_unread_messages() {
  local agent="$1"
  local watermark
  watermark="$(get_msg_watermark "$agent")"

  # Search for messages addressed to this agent
  local query="OR8-COMMS to=${agent}"
  local encoded
  encoded="${query// /%20}"
  encoded="${encoded//=/%3D}"

  local raw_ids
  raw_ids=$(curl -sS --max-time 5 \
    "${MEMORY_GATEWAY_URL:-http://127.0.0.1:37888}/v1/memory/search?query=${encoded}&limit=50" 2>/dev/null \
    | grep -o '#[0-9]\+' | tr -d '#' | sort -n | uniq || true)

  if [[ -z "$raw_ids" ]]; then
    echo "0"
    return 0
  fi

  # Filter: only IDs > watermark
  local unread_count=0
  local max_id="$watermark"
  local unread_ids=""
  while IFS= read -r mid; do
    if [[ -n "$mid" ]] && (( mid > watermark )); then
      unread_count=$((unread_count + 1))
      unread_ids="${unread_ids:+${unread_ids},}${mid}"
      (( mid > max_id )) && max_id=$mid
    fi
  done <<< "$raw_ids"

  echo "${unread_count}|${max_id}|${unread_ids}"
}

# --- Commands ---
cmd_unread() {
  if [[ $# -lt 1 ]]; then usage; exit 1; fi
  local agent="$1"
  local phase="${2:-}"

  echo "=== Unread flags for agent=${agent} ==="

  # Messages
  local result
  result="$(_unread_messages "$agent")"
  local msg_count msg_max msg_ids
  IFS='|' read -r msg_count msg_max msg_ids <<< "$result"

  echo "unread_messages: ${msg_count}"
  if (( msg_count > 0 )); then
    echo "  new_ids: ${msg_ids}"
    echo "  watermark: $(get_msg_watermark "$agent") -> latest: ${msg_max}"
  fi

  # Guidance (if phase specified)
  if [[ -n "$phase" ]]; then
    local current_fp
    current_fp="$(_guidance_fingerprint "$phase")"
    local stored_fp
    stored_fp="$(get_guidance_watermark "$agent" "$phase")"

    if [[ "$current_fp" == "missing" ]]; then
      echo "guidance_${phase}: no GUIDANCE.md found"
    elif [[ "$current_fp" != "$stored_fp" ]]; then
      echo "guidance_${phase}: UPDATED (unread)"
      echo "  file: ${CHECKINS_DIR}/${phase}/GUIDANCE.md"
      echo "  fingerprint: ${stored_fp} -> ${current_fp}"
    else
      echo "guidance_${phase}: up-to-date"
    fi
  else
    # Check all known phases
    for pdir in "${CHECKINS_DIR}"/P*/; do
      if [[ -d "$pdir" ]]; then
        local p
        p=$(basename "$pdir")
        local fp
        fp="$(_guidance_fingerprint "$p")"
        local sfp
        sfp="$(get_guidance_watermark "$agent" "$p")"
        if [[ "$fp" != "missing" && "$fp" != "$sfp" ]]; then
          echo "guidance_${p}: UPDATED (unread)"
        fi
      fi
    done
  fi
}

cmd_mark_read() {
  if [[ $# -lt 1 ]]; then usage; exit 1; fi
  local agent="$1"
  local phase="${2:-}"

  # Mark messages read
  local result
  result="$(_unread_messages "$agent")"
  local msg_count msg_max msg_ids
  IFS='|' read -r msg_count msg_max msg_ids <<< "$result"

  if (( msg_max > 0 )); then
    set_msg_watermark "$agent" "$msg_max"
    echo "messages: watermark updated to ${msg_max} (${msg_count} marked read)"
  else
    echo "messages: no new messages"
  fi

  # Mark guidance read
  if [[ -n "$phase" ]]; then
    local fp
    fp="$(_guidance_fingerprint "$phase")"
    if [[ "$fp" != "missing" ]]; then
      set_guidance_watermark "$agent" "$phase" "$fp"
      echo "guidance_${phase}: marked read (fp=${fp})"
    fi
  fi
}

cmd_status() {
  if [[ $# -lt 1 ]]; then usage; exit 1; fi
  local agent="$1"

  echo "agent: ${agent}"
  echo "msg_watermark: $(get_msg_watermark "$agent")"

  local result
  result="$(_unread_messages "$agent")"
  local msg_count msg_max msg_ids
  IFS='|' read -r msg_count msg_max msg_ids <<< "$result"
  echo "unread_messages: ${msg_count}"

  local guidance_unread=0
  for pdir in "${CHECKINS_DIR}"/P*/; do
    if [[ -d "$pdir" ]]; then
      local p fp sfp
      p=$(basename "$pdir")
      fp="$(_guidance_fingerprint "$p")"
      sfp="$(get_guidance_watermark "$agent" "$p")"
      if [[ "$fp" != "missing" && "$fp" != "$sfp" ]]; then
        guidance_unread=$((guidance_unread + 1))
      fi
    fi
  done
  echo "unread_guidance_phases: ${guidance_unread}"
}

cmd_reset() {
  if [[ $# -lt 1 ]]; then usage; exit 1; fi
  local agent="$1"
  rm -f "${STATE_DIR}/${agent}".* 2>/dev/null || true
  echo "watermarks cleared for agent=${agent}"
}

# --- Main ---
main() {
  if [[ $# -lt 1 ]]; then usage; exit 1; fi
  local cmd="$1"; shift

  case "$cmd" in
    unread)    cmd_unread "$@" ;;
    mark-read) cmd_mark_read "$@" ;;
    status)    cmd_status "$@" ;;
    reset)     cmd_reset "$@" ;;
    *)         usage; exit 1 ;;
  esac
}

main "$@"

#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/packet_closeout.sh <PHASE> <PACKET_ID> [STATUS_FILE]

Validates packet closeout readiness against boundary + status evidence.
USAGE
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

PHASE="$1"
PACKET_ID="$2"
SHORT_PACKET="$PACKET_ID"
if [[ "$PACKET_ID" == "${PHASE}-"* ]]; then
  SHORT_PACKET="${PACKET_ID#${PHASE}-}"
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECKIN_DIR="$ROOT/.planning/orchestr8_next/execution/checkins/$PHASE"
STATUS_FILE="${3:-$CHECKIN_DIR/STATUS.md}"

if [[ ! -d "$CHECKIN_DIR" ]]; then
  echo "FAIL: missing check-in directory: $CHECKIN_DIR" >&2
  exit 1
fi

BOUNDARY_FILE="$(ls "$CHECKIN_DIR"/AUTONOMY_BOUNDARY_"${PACKET_ID}"_*.md "$CHECKIN_DIR"/AUTONOMY_BOUNDARY_"${SHORT_PACKET}"_*.md 2>/dev/null | head -n 1 || true)"
if [[ -z "$BOUNDARY_FILE" ]]; then
  echo "FAIL: boundary not found for ${PACKET_ID} or ${SHORT_PACKET}" >&2
  exit 1
fi
if [[ ! -f "$STATUS_FILE" ]]; then
  echo "FAIL: status file missing: $STATUS_FILE" >&2
  exit 1
fi

fail=0

mapfile -t boundary_artifacts < <(grep -Eo '/home/bozertron/Orchestr8_jr/\.planning/orchestr8_next/artifacts/[^ )`"]+' "$BOUNDARY_FILE" | sort -u)
if [[ ${#boundary_artifacts[@]} -eq 0 ]]; then
  echo "FAIL: no required canonical artifact path in boundary" >&2
  fail=1
fi

for path in "${boundary_artifacts[@]}"; do
  if [[ "$path" == *"*"* ]]; then
    if compgen -G "$path" > /dev/null; then
      echo "OK: pattern matched -> $path"
    else
      echo "FAIL: required artifact pattern missing -> $path" >&2
      fail=1
    fi
  else
    if [[ -f "$path" ]]; then
      echo "OK: artifact exists -> $path"
    else
      echo "FAIL: required artifact missing -> $path" >&2
      fail=1
    fi
  fi
done

# Validate explicit code/test file evidence declared in backticks under Required Evidence.
required_evidence_lines="$(
  awk '
    /^## Required Evidence/ { in_section=1; next }
    /^## / && in_section { exit }
    in_section { print }
  ' "$BOUNDARY_FILE"
)"

mapfile -t required_paths < <(
  printf '%s\n' "$required_evidence_lines" \
    | sed -n 's/.*`\([^`]*\/[^`]*\)`.*/\1/p' \
    | sort -u
)

for p in "${required_paths[@]}"; do
  target="$p"
  if [[ "$target" != /* ]]; then
    target="$ROOT/$target"
  fi

  if [[ "$target" == *"*"* ]]; then
    if compgen -G "$target" > /dev/null; then
      echo "OK: required path pattern matched -> $p"
    else
      echo "FAIL: required path pattern missing -> $p" >&2
      fail=1
    fi
  else
    if [[ -f "$target" ]]; then
      echo "OK: required file exists -> $p"
    else
      echo "FAIL: required file missing -> $p" >&2
      fail=1
    fi
  fi
done

if ! grep -Eq "${PACKET_ID}|${SHORT_PACKET}" "$STATUS_FILE"; then
  echo "FAIL: status file does not reference packet id ${PACKET_ID} or ${SHORT_PACKET}" >&2
  fail=1
fi
if ! grep -Eiq 'pass count|[0-9]+ passed|pass(es|ed)?' "$STATUS_FILE"; then
  echo "FAIL: status file missing pass-count evidence" >&2
  fail=1
fi
if ! grep -Eiq 'Memory Observation IDs|observation #[0-9]+|obs #[0-9]+' "$STATUS_FILE"; then
  echo "FAIL: status file missing memory observation evidence" >&2
  fail=1
fi

if [[ -x "$ROOT/scripts/agent_comms.sh" ]]; then
  outbox_output="$($ROOT/scripts/agent_comms.sh outbox 2>/dev/null || true)"
  outbox_count="$(printf '%s\n' "$outbox_output" | awk '/outbox_pending:/ {print $2}' | head -n 1)"
  if [[ -n "$outbox_count" ]] && [[ "$outbox_count" =~ ^[0-9]+$ ]] && (( outbox_count > 0 )); then
    echo "FAIL: outbox not empty (pending=$outbox_count). run: scripts/agent_comms.sh flush" >&2
    fail=1
  fi
fi

if [[ $fail -ne 0 ]]; then
  echo "packet_closeout: FAIL" >&2
  exit 1
fi

echo "packet_closeout: PASS"

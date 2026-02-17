#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>

Checks packet prompt/boundary consistency before execution.
USAGE
}

if [[ $# -ne 2 ]]; then
  usage
  exit 1
fi

PROMPT_FILE="$1"
BOUNDARY_FILE="$2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

[[ "$PROMPT_FILE" = /* ]] || PROMPT_FILE="$ROOT/$PROMPT_FILE"
[[ "$BOUNDARY_FILE" = /* ]] || BOUNDARY_FILE="$ROOT/$BOUNDARY_FILE"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "FAIL: prompt file missing: $PROMPT_FILE" >&2
  exit 1
fi
if [[ ! -f "$BOUNDARY_FILE" ]]; then
  echo "FAIL: boundary file missing: $BOUNDARY_FILE" >&2
  exit 1
fi

fail=0

pattern_to_regex() {
  local p
  p="$(basename "$1")"
  p="${p//./\\.}"
  p="${p//\*/.*}"
  printf '^%s$' "$p"
}

mapfile -t boundary_artifacts < <(grep -Eo '/home/bozertron/Orchestr8_jr/\.planning/orchestr8_next/artifacts/[^ )`"]+' "$BOUNDARY_FILE" | sort -u)
mapfile -t prompt_artifacts < <(grep -Eo '(/home/bozertron/Orchestr8_jr/)?\.planning/orchestr8_next/artifacts/[^ )`"]+' "$PROMPT_FILE" | sed 's#^\./##' | sort -u)

if [[ ${#boundary_artifacts[@]} -eq 0 ]]; then
  echo "FAIL: no canonical artifact path found in boundary" >&2
  fail=1
fi
if [[ ${#prompt_artifacts[@]} -eq 0 ]]; then
  echo "FAIL: no artifact path found in prompt" >&2
  fail=1
fi

for b in "${boundary_artifacts[@]}"; do
  regex="$(pattern_to_regex "$b")"
  matched=0
  for p in "${prompt_artifacts[@]}"; do
    if [[ "$(basename "$p")" =~ $regex ]]; then
      matched=1
      break
    fi
  done
  if [[ $matched -eq 0 ]]; then
    echo "FAIL: boundary artifact pattern not represented in prompt: $(basename "$b")" >&2
    fail=1
  fi
done

if ! grep -q 'checkout true' "$PROMPT_FILE"; then
  echo "FAIL: prompt missing checkout requires_ack=true" >&2
  fail=1
fi
if ! grep -q 'scripts/agent_flags.sh unread' "$PROMPT_FILE"; then
  echo "FAIL: prompt missing unread preflight command" >&2
  fail=1
fi
if ! grep -q 'scripts/agent_comms.sh health' "$PROMPT_FILE"; then
  echo "FAIL: prompt missing health preflight command" >&2
  fail=1
fi
if ! grep -Eq 'LONG_RUN_MODE\.md|Long-run mode:' "$PROMPT_FILE"; then
  echo "FAIL: prompt missing long-run mode reference (LONG_RUN_MODE.md)" >&2
  fail=1
fi
if ! grep -q 'ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/' "$PROMPT_FILE"; then
  echo "FAIL: prompt missing canonical delivery proof command (ls -l)" >&2
  fail=1
fi

if [[ $fail -ne 0 ]]; then
  echo "packet_lint: FAIL" >&2
  exit 1
fi

echo "packet_lint: PASS"

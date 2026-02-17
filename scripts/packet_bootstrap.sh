#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>

Generates packet worklist file in canonical check-in path.
Example:
  scripts/packet_bootstrap.sh P07 P07-B2 a_codex_plan
USAGE
}

if [[ $# -ne 3 ]]; then
  usage
  exit 1
fi

PHASE="$1"
PACKET_ID="$2"
AGENT_ID="$3"
SHORT_PACKET="$PACKET_ID"
if [[ "$PACKET_ID" == "${PHASE}-"* ]]; then
  SHORT_PACKET="${PACKET_ID#${PHASE}-}"
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECKIN_DIR="$ROOT/.planning/orchestr8_next/execution/checkins/$PHASE"
PROMPTS_DIR="$ROOT/.planning/orchestr8_next/execution/prompts"
WORKLIST_PATH="$CHECKIN_DIR/${PACKET_ID}_WORKLIST.md"

if [[ ! -d "$CHECKIN_DIR" ]]; then
  echo "ERROR: check-in directory not found: $CHECKIN_DIR" >&2
  exit 1
fi

BOUNDARY_FILE="$(ls "$CHECKIN_DIR"/AUTONOMY_BOUNDARY_"${PACKET_ID}"_*.md "$CHECKIN_DIR"/AUTONOMY_BOUNDARY_"${SHORT_PACKET}"_*.md 2>/dev/null | head -n 1 || true)"
PROMPT_FILE="$(rg -l "Packet ID:[[:space:]]*.*${PACKET_ID}|Packet ID:[[:space:]]*.*${SHORT_PACKET}" "$PROMPTS_DIR" -g '*.md' | head -n 1 || true)"

if [[ -z "$BOUNDARY_FILE" ]]; then
  echo "ERROR: boundary file not found for packet $PACKET_ID in $CHECKIN_DIR" >&2
  exit 1
fi

EVIDENCE_ITEMS="$(awk '
  /^## Required Evidence/ { in_section=1; next }
  /^## / && in_section { exit }
  in_section && /^[[:space:]]*- / { sub(/^[[:space:]]*/, ""); print }
' "$BOUNDARY_FILE")"

if [[ -z "$EVIDENCE_ITEMS" ]]; then
  EVIDENCE_ITEMS=$'- [ ] Exact test command(s) + pass counts\n- [ ] Artifact path(s)\n- [ ] Canonical delivery proof (cp + ls -l)'
fi

cat > "$WORKLIST_PATH" <<WORKLIST
# ${PACKET_ID} Worklist

- Phase: ${PHASE}
- Packet ID: ${PACKET_ID}
- Agent ID: ${AGENT_ID}
- Boundary: ${BOUNDARY_FILE#$ROOT/}
- Prompt: ${PROMPT_FILE#$ROOT/}
- Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Preconditions

- [ ] Read order complete (README.AGENTS -> HARD_REQUIREMENTS -> LONG_RUN_MODE -> boundary -> prompt -> check-ins)
- [ ] Preflight comms complete
:   - scripts/agent_flags.sh unread ${AGENT_ID} ${PHASE}
:   - scripts/agent_comms.sh health
- [ ] Prompt/boundary lint passed
:   - scripts/packet_lint.sh ${PROMPT_FILE#$ROOT/} ${BOUNDARY_FILE#$ROOT/}
- [ ] Checkout sent and ack recorded

## Work Items

- [ ] Itemize implementation tasks from scope
- [ ] Execute tests for packet scope
- [ ] Record exact command outputs and pass counts

## Required Evidence

$(printf '%s
' "$EVIDENCE_ITEMS" | sed 's/^- /- [ ] /')

## Closeout

- [ ] scripts/packet_closeout.sh ${PHASE} ${PACKET_ID} passed
- [ ] Completion ping sent
- [ ] Outbox checked/flushed if needed
- [ ] Residual risks recorded (or none)
WORKLIST

echo "Generated: ${WORKLIST_PATH#$ROOT/}"
if [[ -n "$PROMPT_FILE" ]]; then
  echo "Prompt: ${PROMPT_FILE#$ROOT/}"
fi

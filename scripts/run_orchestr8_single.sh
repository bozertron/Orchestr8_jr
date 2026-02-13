#!/usr/bin/env bash
set -euo pipefail

# Canonical launcher: keep exactly one marimo process for orchestr8.py.
# Usage:
#   scripts/run_orchestr8_single.sh            # foreground, port 2719
#   scripts/run_orchestr8_single.sh 2718       # foreground, custom port
#   HEADLESS=1 scripts/run_orchestr8_single.sh # headless mode

PORT="${1:-2719}"
APP_FILE="${APP_FILE:-orchestr8.py}"
HEADLESS="${HEADLESS:-0}"
LEGACY_FILES=(
  "orchestr8_no_plugin_system.py"
  "maestro_standalone.py"
  "IP/woven_maps_nb.py"
  "IP/woven_maps.py.backup"
)

if [[ ! -f "$APP_FILE" ]]; then
  echo "error: $APP_FILE not found in $(pwd)" >&2
  exit 1
fi

for legacy in "${LEGACY_FILES[@]}"; do
  if [[ -f "$legacy" ]]; then
    echo "error: duplicate legacy file present: $legacy" >&2
    echo "       canonical startup is marimo run orchestr8.py" >&2
    exit 1
  fi
done

mapfile -t PIDS < <(pgrep -f "marimo run ${APP_FILE}" || true)
if (( ${#PIDS[@]} > 0 )); then
  echo "stopping existing marimo orchestr8 processes: ${PIDS[*]}"
  kill -TERM "${PIDS[@]}" 2>/dev/null || true
  sleep 1
fi

CMD=(marimo run "$APP_FILE" --port "$PORT")
if [[ "$HEADLESS" == "1" ]]; then
  CMD+=(--headless)
fi

echo "starting single orchestr8 instance: ${CMD[*]}"
exec "${CMD[@]}"

#!/usr/bin/env bash
set -euo pipefail

PHASE=P07
PACKET=P07-A7

/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread orchestr8_jr "$PHASE"
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send orchestr8_jr codex "$PHASE" checkout true 'packet=P07-A7; scope=wave4 active governance + batch replay + wave5 prep; files=<files>; tests=<tests>; eta=<eta>'
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh "$PHASE" "$PACKET" orchestr8_jr
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_A6_ORCHESTR8JR.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A7_ORCHESTR8JR.md

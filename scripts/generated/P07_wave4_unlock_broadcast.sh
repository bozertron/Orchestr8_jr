#!/usr/bin/env bash
set -euo pipefail

PHASE=P07

/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health

/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex a_codex_plan "$PHASE" guidance true 'unlock=P07-B7; wave=Wave-4; scope=settings service + phreak token + integration hardening; resume=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_B6_A_CODEX_PLAN.md; boundary=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B7_A_CODEX_PLAN.md; mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer'
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex 2ndFid_explorers "$PHASE" guidance true 'unlock=P07-C7; wave=Wave-4; scope=intent parser + settings validator extraction pair; resume=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C6_2NDFID_EXPLORERS.md; boundary=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C7_2NDFID_EXPLORERS.md; mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer'
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex or8_founder_console "$PHASE" guidance true 'unlock=P07-FC-06; wave=Wave-4; scope=c2p wave4 observation sync + review queue; resume=/home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_06.md; boundary=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-06_OR8_FOUNDER_CONSOLE.md; mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer'
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex mingos_settlement_lab "$PHASE" guidance true 'unlock=P07-MSL-06; wave=Wave-4; scope=phreak token + cse UI constraint transfer; resume=/home/bozertron/Orchestr8_jr/.planning/projects/mingos_settlement_lab/prompts/RESUME_MSL_06.md; boundary=/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-06_MINGOS_SETTLEMENT_LAB.md; mode=long-run; assumptions=none; ambiguity=local_probe+cross_probe_then_defer'
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send codex antigravity "$PHASE" guidance true 'Wave-4 unlock mirror; packets=P07-B7, P07-C7, P07-FC-06, P07-MSL-06; long-run active; no assumptions; use canonical guidance files'

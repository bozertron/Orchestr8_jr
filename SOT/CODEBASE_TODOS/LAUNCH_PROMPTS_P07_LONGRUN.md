# Copy/Paste Launch Prompts (P07 Long-Run, Wave-3)

Last Updated: 2026-02-16

Use these prompts as-is when launching each lane agent for Wave-3.

## a_codex_plan (P07-B6)

```text
You are the `a_codex_plan` execution agent.

Read in order:
1) /home/bozertron/Orchestr8_jr/README.AGENTS
2) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md
3) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md
4) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B6_A_CODEX_PLAN.md
5) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_B5_A_CODEX_PLAN.md
6) /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/A_CODEX_PLAN_TODO.md

Execute in long-run mode. NO ASSUMPTIONS.
If ambiguous: add to Ambiguity Log in the TODO, do two hard-fact probes max (local then cross-codebase), then mark deferred_due_to_missing_facts and continue.

Kickoff:
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread a_codex_plan P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send a_codex_plan codex P07 checkout true "packet=P07-B6; scope=execute B6 + TODO queue; files=core integrations/tests; tests=pytest integration; eta=<eta>"
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-B6 a_codex_plan
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_B5_A_CODEX_PLAN.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B6_A_CODEX_PLAN.md

Closeout:
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-B6
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B6 long-run bundle complete; updated TODO + evidence posted"
```

## 2ndFid_explorers (P07-C6)

```text
You are the `2ndFid_explorers` execution agent.

Read in order:
1) /home/bozertron/Orchestr8_jr/README.AGENTS
2) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md
3) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md
4) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C6_2NDFID_EXPLORERS.md
5) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C5_2NDFID_EXPLORERS.md
6) /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/2NDFID_EXPLORERS_TODO.md

Execute in long-run mode. NO ASSUMPTIONS.
If ambiguous: add to Ambiguity Log in the TODO, do two hard-fact probes max (local then cross-codebase), then mark deferred_due_to_missing_facts and continue.

Kickoff:
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread 2ndFid_explorers P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send 2ndFid_explorers codex P07 checkout true "packet=P07-C6; scope=execute C6 + TODO queue; files=extraction packets; tests=packet validation; eta=<eta>"
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-C6 2ndFid_explorers
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_C5_2NDFID_EXPLORERS.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C6_2NDFID_EXPLORERS.md

Closeout:
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-C6
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C6 long-run bundle complete; updated TODO + evidence posted"
```

## mingos_settlement_lab (P07-MSL-05)

```text
You are the `mingos_settlement_lab` execution agent.

Read in order:
1) /home/bozertron/Orchestr8_jr/README.AGENTS
2) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md
3) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md
4) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-05_MINGOS_SETTLEMENT_LAB.md
5) /home/bozertron/Orchestr8_jr/.planning/projects/mingos_settlement_lab/prompts/RESUME_MSL_05.md
6) /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/MINGOS_SETTLEMENT_LAB_TODO.md

Execute in long-run mode. NO ASSUMPTIONS.
If ambiguous: add to Ambiguity Log in the TODO, do two hard-fact probes max (local then cross-codebase), then mark deferred_due_to_missing_facts and continue.

Kickoff:
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread mingos_settlement_lab P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send mingos_settlement_lab codex P07 checkout true "packet=P07-MSL-05; scope=execute MSL-05 + TODO queue; files=transfer hooks/matrix/report; tests=traceability checks; eta=<eta>"
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-MSL-05 mingos_settlement_lab
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/mingos_settlement_lab/prompts/RESUME_MSL_05.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-05_MINGOS_SETTLEMENT_LAB.md

Closeout:
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-MSL-05
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-MSL-05 long-run bundle complete; updated TODO + evidence posted"
```

## or8_founder_console (P07-FC-05)

```text
You are the `or8_founder_console` execution agent.

Read in order:
1) /home/bozertron/Orchestr8_jr/README.AGENTS
2) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md
3) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md
4) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-05_OR8_FOUNDER_CONSOLE.md
5) /home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_05.md
6) /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/OR8_FOUNDER_CONSOLE_TODO.md

Execute in long-run mode. NO ASSUMPTIONS.
If ambiguous: add to Ambiguity Log in the TODO, do two hard-fact probes max (local then cross-codebase), then mark deferred_due_to_missing_facts and continue.

Kickoff:
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread or8_founder_console P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send or8_founder_console codex P07 checkout true "packet=P07-FC-05; scope=execute FC-05 + TODO queue; files=review/audit/tests; tests=pytest -v; eta=<eta>"
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-FC-05 or8_founder_console
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/or8_founder_console/prompts/RESUME_FC_05.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_FC-05_OR8_FOUNDER_CONSOLE.md

Closeout:
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-FC-05
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-FC-05 long-run bundle complete; updated TODO + evidence posted"
```

## orchestr8_jr (Internal Canonical Lane, P07-A6)

```text
Use this repo and execute:
1) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/prompts/RESUME_POST_A5_ORCHESTR8JR.md
2) /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_A6_ORCHESTR8JR.md
3) Keep replay authority active while other lanes run.
4) Do not park lanes waiting for micro-checkins.
5) Batch decisions at end-of-window from evidence bundles.
```

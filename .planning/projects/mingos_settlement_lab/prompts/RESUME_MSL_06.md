# Resume Prompt - mingos_settlement_lab (P07-MSL-06)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-MSL-06`.

## Packet

- Packet ID: `P07-MSL-06`
- Scope: Settlement packet: token spec + interaction constraints + handoff

## Objective

Publish implementable Phreak visual transfer packet and CSE UI constraints matrix.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread mingos_settlement_lab P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-06_MINGOS_SETTLEMENT_LAB.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`
- `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-05_REPORT.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send mingos_settlement_lab codex P07 checkout true "packet=P07-MSL-06; scope=phreak token + cse UI constraint transfer; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-MSL-06 mingos_settlement_lab
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/mingos_settlement_lab/prompts/RESUME_MSL_06.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL-06_MINGOS_SETTLEMENT_LAB.md
```

## Required outputs

- `/home/bozertron/mingos_settlement_lab/transfer/MSL_06_PHREAK_TOKEN_SPEC.md`
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_06_CSE_UI_CONSTRAINTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-06_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-06_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-06_REPORT.md
```

Validation:

```bash
Traceability table complete in report
```
Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-MSL-06
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-MSL-06 long-run bundle complete; updated TODO + evidence posted"
```

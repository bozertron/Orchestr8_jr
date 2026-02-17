# Resume Prompt - MSL-02 (Mingos Settlement Lab)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are executing packet `P07-MSL-02`.

## Preconditions (required)

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_flags.sh unread <agent_id> P07
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh health
```

Read:
- `/home/bozertron/Orchestr8_jr/README.AGENTS`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL_02_MINGOS_SETTLEMENT_LAB.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

Checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-MSL-02; scope=module-spec + transfer packet; files=<files>; tests=<tests>; eta=<eta>"
```

Worklist + lint:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_bootstrap.sh P07 P07-MSL-02 <agent_id>
/home/bozertron/Orchestr8_jr/scripts/packet_lint.sh /home/bozertron/Orchestr8_jr/.planning/projects/mingos_settlement_lab/prompts/RESUME_MSL_02.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_MSL_02_MINGOS_SETTLEMENT_LAB.md
```

## Required outputs

- `/home/bozertron/mingos_settlement_lab/specs/MSL_02_MODULE_01_CITY_LIFE.md`
- `/home/bozertron/mingos_settlement_lab/specs/MSL_02_MODULE_02_POWER_GRID.md`
- `/home/bozertron/mingos_settlement_lab/specs/MSL_02_MODULE_03_TEMPORAL_STATE.md`
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_02_TRANSFER_PACKET.md`
- Updated `/home/bozertron/mingos_settlement_lab/transfer/SETTLEMENT_PRD_OUTLINE.md`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-02_REPORT.md`

Canonical delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-02_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/MSL-02_REPORT.md
```

Closeout + ping:

```bash
/home/bozertron/Orchestr8_jr/scripts/packet_closeout.sh P07 P07-MSL-02
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-MSL-02 complete; evidence posted"
```

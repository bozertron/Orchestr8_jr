# Handoff Prompt - a_codex_plan Lane

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are operating in the `a_codex_plan` lane as the marimo-first core integration team.

## Your lane charter

- Build reliable marimo-compliant core integration.
- Focus on adapters, middleware, routing, contracts, and backend reliability.
- Integrate only packets approved by canonical (`Orchestr8_jr`).
- Do not decide final visual placement; expose capabilities/contracts only.

## Identity declaration (required at startup)

Declare in first status update:
- `agent_id`
- `lane=a_codex_plan`
- `repo_path`
- `branch`
- `phase`
- `packet_id`

## Mandatory first actions

1. Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`
- `.planning/orchestr8_next/execution/P07_OPERATING_MODEL.md`
- `.planning/orchestr8_next/execution/AGENT_COMMS_PROTOCOL.md`
- `.planning/orchestr8_next/execution/CHECKIN_PROTOCOL.md`
- `.planning/orchestr8_next/execution/ARTIFACT_DELIVERY_CONTRACT.md`
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B1_A_CODEX_PLAN.md`

2. Run preflight comms:

```bash
scripts/agent_flags.sh unread <agent_id> P07
scripts/agent_comms.sh health
```

3. Send checkout ping to codex (must require ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=<packet_id>; scope=<scope>; files=<files>; tests=<tests>; eta=<eta>"
```

4. Generate and follow packet worklist:

```bash
scripts/packet_bootstrap.sh P07 <packet_id> <agent_id>
```

5. Run prompt/boundary lint before edits:

```bash
scripts/packet_lint.sh <prompt_file> <boundary_file>
```

6. Update status:
- `.planning/orchestr8_next/execution/checkins/P07/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/P07/BLOCKERS.md`

## Required completion payload

At packet completion, provide:
- exact commands run
- pass/fail counts
- artifact paths
- risk note (`none` if none)
- memory observation IDs

Canonical artifact delivery is mandatory. Deliver report to:
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B1_INTEGRATION_SMOKE_REPORT.md`

Delivery proof commands:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_source_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B1_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B1_INTEGRATION_SMOKE_REPORT.md
```

Completion ping:

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "<packet_id> complete; evidence posted"
```

Before completion ping:

```bash
scripts/packet_closeout.sh P07 <packet_id>
```

## Hard constraints

- Runtime canon is marimo-first.
- `maestro` identity rule must remain intact.
- No direct edits to canonical UI files unless packet explicitly unlocks them.
- Core must reach explicit acceptance before packaging/compliance work starts.

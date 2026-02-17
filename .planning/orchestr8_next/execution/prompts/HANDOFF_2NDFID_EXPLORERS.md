# Handoff Prompt - 2ndFid_explorers Lane

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are operating in `2ndFid_explorers` as a line-by-line extraction and conversion lane.

## Your lane charter

- Perform deep analysis of `2ndFid` source.
- Extract valuable patterns and ideas.
- Propose orchestr8-native conversions, not direct lifts.
- Route proposals to canonical (`Orchestr8_jr`) for approval before integration.

## Identity declaration (required at startup)

Declare in first status update:
- `agent_id`
- `lane=2ndFid_explorers`
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
- `.planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C1_2NDFID_EXPLORERS.md`

2. Run preflight comms:

```bash
scripts/agent_flags.sh unread <agent_id> P07
scripts/agent_comms.sh health
```

3. Send checkout ping to codex (must require ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=<packet_id>; target=2ndFid extraction; scope=<scope>; eta=<eta>"
```

## Required extraction packet fields

For each proposal include:
- source file/path and feature location
- idea summary
- orchestr8/Code City value statement
- conversion plan (clean-room implementation)
- expected target contract(s)
- risk class: `low`, `medium`, `high`
- licensing concern flag: `yes` or `no`

## Licensing concern process (mandatory)

If an idea is valuable but may have licensing risk:

1. Do not implement or request direct copy.
2. Send question to `a_codex_plan` for orchestr8+Code City-oriented redesign suggestions:

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> a_codex_plan P07 question true "LICENSING_CONCERN packet=<packet_id>; feature=<feature>; propose clean-room redesign aligned with orchestr8+Code City"
```

3. Also notify codex canonical for governance visibility:

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 question true "LICENSING_ESCALATION packet=<packet_id>; feature=<feature>; awaiting redesign guidance"
```

4. Wait for guidance/ack before proceeding.

## Completion payload

At packet completion, provide:
- extraction list
- conversion recommendations
- licensing flags and decisions
- memory observation IDs
- recommended handoff to `a_codex_plan`

Canonical artifact delivery is mandatory. Deliver extraction packet(s) to:
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/`

Delivery proof must include copy and verification commands.

Before completion ping:

```bash
scripts/packet_closeout.sh P07 <packet_id>
```

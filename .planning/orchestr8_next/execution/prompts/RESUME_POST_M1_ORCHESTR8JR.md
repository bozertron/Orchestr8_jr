# Resume Prompt - Orchestr8_jr Canonical (Post-M1)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming canonical orchestration after shared memory hardening (`P07-M1`) is approved.

## Packet

- Packet ID: `P07-A2`
- Scope: Govern resumed lanes, validate incoming packets, continue frontend governance progression.

## Preconditions

1. Confirm `P07-M1` acceptance and updated comms scripts active.
2. Run preflight checks:

```bash
scripts/agent_flags.sh unread codex P07
scripts/agent_comms.sh health
```

If health is unreachable, run:

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

3. If unread guidance is present, read and mark:

```bash
scripts/agent_flags.sh mark-read codex P07
```

4. Send checkout to codex (self-checkout record) with packet scope.
5. Note policy: `stop`/`restart` are owner-restricted by default; require explicit override reason for non-owner action.
6. Generate and follow packet worklist:

```bash
scripts/packet_bootstrap.sh P07 P07-A2 codex
```

## Required work

1. Lane control:
- unlock `P07-B2` for `a_codex_plan`
- unlock `P07-C2` for `2ndFid_explorers`
- enforce artifact delivery contract strictly

2. Canonical validations:
- replay tests for any incoming B2 outputs
- review C2 extraction packets and approve/reject

3. Frontend canonical progress:
- complete visual baseline screenshot capture referenced by:
- `.planning/orchestr8_next/artifacts/P07/visual_baselines/README.md`
- update SOT docs with accepted delta decisions only

## Required outputs

- `.planning/orchestr8_next/artifacts/P07/A2_RESUME_GOVERNANCE_REPORT.md`
- updated `.planning/orchestr8_next/execution/checkins/P07/STATUS.md`
- updated `.planning/orchestr8_next/execution/checkins/P07/GUIDANCE.md`

## Completion

Include:
- commands/pass counts
- packet decisions (accept/rework)
- memory IDs
- next unlock recommendation

Before completion ping:

```bash
scripts/packet_closeout.sh P07 P07-A2
```

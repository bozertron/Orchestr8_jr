# Resume Prompt - a_codex_plan (Post-M1)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming the `a_codex_plan` lane after shared memory hardening (`P07-M1`) is approved by codex.

## Packet

- Packet ID: `P07-B2`
- Scope: Integrate approved C1 extractions into marimo-first core runtime (DocumentGraph first, ActivityGraph second).

## Preconditions (must pass before coding)

1. Confirm codex has accepted `P07-M1` in canonical.
2. Preflight comms (required):

```bash
scripts/agent_flags.sh unread <agent_id> P07
scripts/agent_comms.sh health
```

If health is unreachable, run recovery start (allowed cross-lane):

```bash
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
scripts/agent_comms.sh health
```

If unread guidance is present, read it then mark read:

```bash
scripts/agent_flags.sh mark-read <agent_id> P07
```

3. Note policy: do not run `stop`/`restart` unless owner-authorized or explicit override reason is provided.
4. Read:
- `README.AGENTS`
- `.planning/orchestr8_next/execution/P07_OPERATING_MODEL.md`
- `.planning/orchestr8_next/execution/ARTIFACT_DELIVERY_CONTRACT.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C1_01_DocumentGraph.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C1_02_ActivityGraph.md`

5. Send checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-B2; scope=C1 integration; files=<files>; tests=<tests>; eta=<eta>"
```

6. Generate and follow packet worklist (required):

```bash
scripts/packet_bootstrap.sh P07 P07-B2 <agent_id>
```

7. Enforce prompt/boundary consistency before edits:

```bash
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_M1_A_CODEX_PLAN.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_B2_A_CODEX_PLAN.md
```

## Required work

1. Implement C1-01 first:
- Add clean-room topology service and layout integration hooks.
- Keep final UI placement decisions out of this lane.

2. Implement C1-02 second:
- Add time-bucketing service + heatmap layer contract hooks.

3. Add tests and smoke evidence for each integration slice.

## Required outputs

- `orchestr8_next/city/topology.py` (canonical repo, implemented)
- `orchestr8_next/city/heatmap.py` (canonical repo, implemented)
- `tests/integration/test_graphs.py` (canonical repo, implemented)
- `.planning/orchestr8_next/artifacts/P07/B2_INTEGRATION_SMOKE_REPORT.md`
- Updated P07 status/blockers in lane
- Canonical artifact delivery proof:

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_report> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B2_INTEGRATION_SMOKE_REPORT.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B2_INTEGRATION_SMOKE_REPORT.md
```

Validation command (required):

```bash
pytest tests/integration/test_graphs.py -vv
```

## Completion ping

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-B2 complete; C1 integration evidence posted"
```

If ping is spooled, run:

```bash
scripts/agent_comms.sh flush
```

Before completion ping (required):

```bash
scripts/packet_closeout.sh P07 P07-B2
```

# Resume Prompt - 2ndFid_explorers (Post-M1)

Long-run mode: follow `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` for kickoff, low-interruption execution, and end-of-window bundle submission.

You are resuming `2ndFid_explorers` after shared memory hardening (`P07-M1`) is approved by codex.

## Packet

- Packet ID: `P07-C2`
- Scope: Continue line-by-line extraction packets focused on orchestr8+Code City value.

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

5. Send checkout (requires ack):

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <agent_id> codex P07 checkout true "packet=P07-C2; scope=next extraction set; files=<files>; eta=<eta>"
```

6. Generate and follow packet worklist (required):

```bash
scripts/packet_bootstrap.sh P07 P07-C2 <agent_id>
```

7. Enforce prompt/boundary consistency before edits:

```bash
scripts/packet_lint.sh .planning/orchestr8_next/execution/prompts/RESUME_POST_M1_2NDFID_EXPLORERS.md .planning/orchestr8_next/execution/checkins/P07/AUTONOMY_BOUNDARY_C2_2NDFID_EXPLORERS.md
```

## Required work

Create next 2 extraction packets (C2-01, C2-02) with required fields:
- source path/provenance
- idea summary
- orchestr8/Code City value
- clean-room conversion plan
- expected contracts
- risk class
- licensing concern flag

## Licensing concern rule (strict)

If concern exists:
1. Stop implementation proposal that depends on direct lift.
2. Ask `a_codex_plan` for orchestr8-native redesign suggestions.
3. Notify codex in parallel with `LICENSING_ESCALATION`.
4. Wait for ack/guidance.

## Required outputs

- `.planning/orchestr8_next/artifacts/P07/P07_C2_01_<Name>.md`
- `.planning/orchestr8_next/artifacts/P07/P07_C2_02_<Name>.md`
- Canonical artifact delivery proof commands and output (`ls -l`)

```bash
install -d /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/
cp <lane_source_packet_01> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C2_01_<Name>.md
cp <lane_source_packet_02> /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C2_02_<Name>.md
ls -l /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C2_01_<Name>.md /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/P07_C2_02_<Name>.md
```

## Completion ping

```bash
OR8_PHASE=P07 /home/bozertron/Orchestr8_jr/scripts/ping_codex.sh 100 "P07-C2 complete; extraction packets delivered with proof"
```

If ping is spooled, run:

```bash
scripts/agent_comms.sh flush
```

Before completion ping (required):

```bash
scripts/packet_closeout.sh P07 P07-C2
```

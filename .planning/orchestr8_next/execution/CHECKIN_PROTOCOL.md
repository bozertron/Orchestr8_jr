# Check-in Protocol

This protocol ensures architect visibility across parallel builders.

Hard requirements SOT:
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`

## Directory Model

Per phase:
- `execution/checkins/Pxx/STATUS.md`
- `execution/checkins/Pxx/GUIDANCE.md`
- `execution/checkins/Pxx/BLOCKERS.md`

## Cadence

- Long-run mode default:
- one kickoff check-in per lane
- one completion bundle check-in per lane
- immediate check-in on blocker/safety/legal event
- mandatory packet checkout before implementation starts

## STATUS.md Rules

Must include:
- owner
- branch
- packet ID
- percent complete
- gate color (`green` / `yellow` / `red`)
- completed items
- in-progress items
- next three actions
- proof links (tests, reports, commands)

## GUIDANCE.md Rules

Architect-only guidance drops, with:
- context
- instruction
- impacted files
- follow-up expectations

Builders must acknowledge guidance in next `STATUS.md` update.

## BLOCKERS.md Rules

Every blocker entry must include:
- severity
- decision needed
- unblocking options
- temporary workaround (if any)

## Gate Colors

- `green`: on plan, no high/critical blockers
- `yellow`: risk present, but route clear
- `red`: blocked pending architect decision

## Packet Lifecycle (Mandatory)

1. `CHECKOUT`
- Send OR8-COMMS checkout message with packet ID, scope, and target files.
- Receive ack before coding starts.
- Generate packet worklist and run prompt/boundary lint before edits.
  - `scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>`
  - `scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>`
2. `IN PROGRESS`
- During long-run windows, avoid routine progress spam.
- Record blockers immediately; otherwise continue execution.
3. `COMPLETE`
- Post one end-of-window bundle: exact commands, pass counts, artifact paths, observation IDs, and risk notes.
- Send OR8-COMMS completion ping with packet ID.
- Run closeout gate before completion ping.
  - `scripts/packet_closeout.sh <PHASE> <PACKET_ID>`
4. `CANONICAL REPLAY`
- Canonical lane reruns verification before acceptance.
5. `ACCEPT/REWORK`
- Architect response is recorded in guidance + memory observation.

## Dynamic Memory Rule (Critical)

For every checkout and completion event:
- save an observation to shared memory gateway (`/v1/memory/save`)
- record the observation ID in `STATUS.md`

## Escalation

Escalate immediately when:
- contract ambiguity blocks progress
- phase scope needs change
- security or license risk appears

## Architect Audit Checklist

1. Is packet scope aligned to assigned step range?
2. Do changes honor architecture boundaries?
3. Are reports and evidence complete?
4. Are new risks documented?
5. Does packet qualify for gate progression?

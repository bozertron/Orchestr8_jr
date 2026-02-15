# Check-in Protocol

This protocol ensures architect visibility across parallel builders.

## Directory Model

Per phase:
- `execution/checkins/Pxx/STATUS.md`
- `execution/checkins/Pxx/GUIDANCE.md`
- `execution/checkins/Pxx/BLOCKERS.md`

## Cadence

- Minimum check-in every 90 minutes while active.
- Immediate check-in on blocker.
- Mandatory check-in on packet completion.

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


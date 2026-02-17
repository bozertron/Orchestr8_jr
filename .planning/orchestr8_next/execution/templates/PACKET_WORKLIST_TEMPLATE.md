# Packet Worklist Template

- Phase:
- Packet ID:
- Agent ID:
- Lane:
- Boundary:
- Prompt:

## Preconditions

- [ ] Read order complete (`README.AGENTS` -> `HARD_REQUIREMENTS.md` -> `LONG_RUN_MODE.md` -> boundary -> prompt -> check-ins)
- [ ] Preflight comms complete (`unread`, `health`)
- [ ] Checkout sent and ack recorded
- [ ] Prompt/boundary lint passed (`scripts/packet_lint.sh`)

## Work Items

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Required Evidence

- [ ] Tests executed with exact command
- [ ] Pass count captured
- [ ] Artifact(s) written
- [ ] Canonical copy + `ls -l` proof captured

## Closeout

- [ ] `scripts/packet_closeout.sh <PHASE> <PACKET_ID>` passed
- [ ] Completion ping sent
- [ ] Outbox checked (`scripts/agent_comms.sh outbox`)
- [ ] Residual risks documented (or `none`)

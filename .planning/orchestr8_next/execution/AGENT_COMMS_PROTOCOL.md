# Agent Comms Protocol (OR8-COMMS v1)

This is the canonical cross-codebase coordination path between agents.

## Transport

1. Shared memory gateway at `http://127.0.0.1:37888`.
2. Message envelope saved via `/v1/memory/save`.
3. Discovery via `/v1/memory/search`.
4. Full payload retrieval via `/v1/memory/observations`.

## Why This Path

`one integration at a time/888/comms/adapter.py` is currently an in-process mock/global-state adapter. It is useful for API shape testing but not reliable as a cross-process/cross-codebase message bus.

Use memory gateway as the cross-agent transport until a real external comms backend is in place.

## Tooling

Use:

- `scripts/agent_comms.sh`

Commands:

- `health`
- `send <from> <to> <phase> <kind> <requires_ack:true|false> <message...>`
- `ack <from> <to> <phase> <cid> <ack_for_id> <message...>`
- `inbox <agent> [limit]`
- `thread <cid> [limit]`

## Startup Handshake

1. Agent A sends `kind=hello` to Agent B with `requires_ack=true`.
2. Agent B runs `inbox`, confirms receipt, and replies with `ack`.
3. Agent A validates ack in `thread <cid>`.
4. Only then begin phase packet work.

## Message Rules

1. Include phase in every message (`P04`, `P05`, etc.).
2. Use one `cid` per work packet/topic thread.
3. Critical guidance must require ack.
4. If no ack in one check-in cycle, resend and mark blocker.

## Canonical Artifacts

Even with memory transport, these files remain source-of-truth for work state:

- `.planning/orchestr8_next/execution/checkins/Pxx/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/BLOCKERS.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/GUIDANCE.md`

## Example

```bash
# A -> B handshake
scripts/agent_comms.sh send codex antigravity P05 hello true "Handshake for P05-WP01 lane."

# B checks inbox and acknowledges
scripts/agent_comms.sh inbox antigravity 10
scripts/agent_comms.sh ack antigravity codex P05 <cid> <saved_id> "Ack: received and proceeding in scope."

# A inspects full thread
scripts/agent_comms.sh thread <cid> 20
```

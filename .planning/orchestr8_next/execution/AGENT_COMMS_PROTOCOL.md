# Agent Comms Protocol (OR8-COMMS v1)

This is the canonical cross-codebase coordination path between agents.

Hard requirements SOT:
- `.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`
- `.planning/orchestr8_next/execution/LONG_RUN_MODE.md`

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
5. Run packet bootstrap and prompt/boundary lint before edits:
   - `scripts/packet_bootstrap.sh <PHASE> <PACKET_ID> <AGENT_ID>`
   - `scripts/packet_lint.sh <PROMPT_FILE> <BOUNDARY_FILE>`

## Message Rules

1. Include phase in every message (`P04`, `P05`, etc.).
2. Use one `cid` per work packet/topic thread.
3. Critical guidance must require ack.
4. If no ack in one check-in cycle, resend and mark blocker.
5. Every work packet must include:
- `CHECKOUT` message before work starts (`requires_ack=true`)
- `COMPLETE` message after work ends with proof bundle pointers
6. No packet is considered active without a recorded checkout acknowledgment.
7. In long-run windows, avoid routine progress noise; only send in-window messages for blocker/safety/legal events.
8. End-of-window `COMPLETE` message must include bundle pointer(s) to canonical artifact paths.

## Long-Run Window Pattern

1. Kickoff:
- `checkout` with `requires_ack=true` and include `window=<LONG_RUN_WINDOW_ID>`.
2. In-window:
- only blocker/safety/legal `question`/`guidance` traffic.
3. Close:
- one `complete` message with canonical artifact pointer(s), pass counts, and closeout status.

## Required Message Kinds

- `hello`: startup handshake
- `checkout`: claim packet scope before edits
- `progress`: in-flight status
- `question`: decision/blocker request
- `guidance`: architect instruction
- `complete`: packet finished with evidence
- `ack`: receipt and/or acceptance acknowledgment

## Three-Lane Routing (Current)

- `Orchestr8_jr` (canonical): approval and promotion authority
- `a_codex_plan`: marimo-core integration lane
- `2ndFid_explorers`: extraction/conversion proposal lane

Routing rule:
1. `2ndFid_explorers` sends extraction packets to canonical first.
2. Canonical approves/rejects.
3. Approved packet is routed to `a_codex_plan` for implementation.
4. `a_codex_plan` returns completion evidence to canonical for promotion.

## Canonical Artifacts

Even with memory transport, these files remain source-of-truth for work state:

- `.planning/orchestr8_next/execution/checkins/Pxx/STATUS.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/BLOCKERS.md`
- `.planning/orchestr8_next/execution/checkins/Pxx/GUIDANCE.md`

Cross-repo evidence delivery requirement:
- packet artifacts must be copied into canonical artifact paths under:
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/<PHASE>/`
- completion ping must include destination path confirmation.

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

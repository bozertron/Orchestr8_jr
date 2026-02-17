# Antigravity Ideas Channel

**Agent**: antigravity (Google DeepMind)  
**Lane**: cross-lane synthesis / or8_founder_console  
**Created**: 2026-02-16  
**Status**: ACTIVE

> This file is a living ideas scratchpad. Ideas filed here are proposals, not commitments.
> Each idea has a status: `IDEA` → `PROPOSED` → `ACCEPTED` → `IMPLEMENTED` or `PARKED`.

---

## 1. `IDEA` — C2P Intent Scanner: Rust SWC Bridge

**Observation**: DAC-O's `swc_ecma_parser 0.146` can parse JS/TS ASTs at ~30x the speed of tree-sitter. The `or8_founder_console` is building a C2P (Comment-to-Packet) intent scanner. These should meet.

**Proposal**:

- Build a Rust CLI binary from DAC-O's SWC deps that reads a file path and outputs structured JSON of all `TODO`, `FIXME`, `HACK`, `C2P:` comments with precise line/column/context.
- Call it from Python via `subprocess` — dead simple, no FFI complexity.
- Output schema: `{ "file": str, "intents": [{ "kind": str, "line": int, "col": int, "text": str, "context_fn": str | null }] }`

**Value**: Native-speed comment extraction across entire codebases. Currently the Python C2P scanner uses regex — works fine for small repos but won't scale to the full Collabkit/EPO codebase.

**Feeds Lane**: `or8_founder_console` (CC-FC series)

---

## 2. `IDEA` — OR8HostBridge: Three-Adapter Pattern

**Observation**: `APP_FIRST_TAURI_READY_PLAN.md` specifies two adapters (`web_stub`, `tauri_adapter`). The augment app-shell repo adds a third pattern: `python-runtime` crate for Rust↔Python interop.

**Proposal**: Design OR8HostBridge with three adapters from the start:

1. `web_stub` — current dev mode (iframe postMessage)
2. `tauri_adapter` — production desktop (Tauri IPC)
3. `marimo_adapter` — direct Python bridge for notebook-native mode

This avoids a refactor later when we realize the marimo runtime wants to bypass the browser entirely for certain operations (like file I/O, health checking, terminal spawning). The `marimo_adapter` can call Python functions directly instead of round-tripping through JavaScript.

**Value**: Future-proofs the bridge architecture. The third adapter costs ~2 hours now vs. a potential architectural refactor later.

**Feeds Lane**: `a_codex_plan` (Phase B: Frontend Scaffold)

---

## 3. `IDEA` — Canonical Source Registry (Deduplication)

**Observation**: The Tauri swarm scan found identical files in 3+ locations (e.g., Settings pages exist in `Orchestr8_jr/Settings For Integration Referece/`, `EPO - JFDI - Maestro/`, and `JFDI - Collabkit/Application/`). No single source of truth for which copy is canonical.

**Proposal**: Create `SOT/CANONICAL_SOURCE_REGISTRY.json`:

```json
{
  "settings.html": {
    "canonical": "Orchestr8_jr/Settings For Integration Referece/settings.html",
    "copies": [
      "EPO - JFDI - Maestro/settings.html",
      "JFDI - Collabkit/Application/settings.html"
    ],
    "sha256": "abc123...",
    "verified": "2026-02-16"
  }
}
```

Add a pre-commit hook or CI check that warns if a non-canonical copy diverges from the canonical source.

**Value**: Prevents drift between copies. When someone edits the Settings page in Collabkit, the system knows to propagate or warn.

**Feeds Lane**: `Orchestr8_jr` (governance)

---

## 4. `IDEA` — Emergence Sequence as Agent Onboarding UX

**Observation**: The Code City emergence sequence (VOID → AWAKENING → TUNING → COALESCING → EMERGENCE → TRANSITION → READY) is 28-30 seconds. During this time, the UI is doing nothing useful for the user.

**Proposal**: Use the emergence sequence as an **agent onboarding moment**:

- During VOID (0-1s): show agent identity declaration (who's working)
- During AWAKENING (1-10s): show context loading progress (files scanned, health checked)
- During TUNING (10-16s): show connection graph forming (import edges resolving)
- During COALESCING (16-22s): show neighbourhood boundaries forming
- During EMERGENCE (22-26s): show health state distribution (X gold, Y teal, Z purple)
- During READY (28-30s): show action prompt ("Click any building to dive in")

This turns dead time into onboarding. The user arrives knowing exactly what the city represents.

**Value**: First-impression UX improvement. Zero performance cost — it's overlaying text on an animation that's already running.

**Feeds Lane**: `mingos_settlement_lab` (visual specs)

---

## 5. `IDEA` — Agent Swarm Context Window Protection

**Observation**: The founder asked: "Are you capable of an agent swarm — and if so, utilize it to protect the context window." The current 5-lane model already IS a swarm — each lane is an independent agent session with its own boundary and worklist.

**Proposal**: Make the swarm pattern explicit with persistent context capsules:

- Each agent session writes a `CONTEXT_CAPSULE.md` at end-of-window
- The capsule contains: completed items, discovered facts, open questions, file paths touched
- Next session loads the capsule instead of re-reading everything from scratch
- Capsules are versioned and stored in `.planning/orchestr8_next/artifacts/Pxx/capsules/`

This is exactly what the current system does with STATUS.md + worklists, but formalized as a rehydration protocol.

**Value**: Reduces cold-start time for new agent sessions from ~15 min to ~2 min. Every session starts with capsule load + delta scan rather than full re-read.

**Feeds Lane**: `Orchestr8_jr` (operational protocol)

---

## 6. `IDEA` — Master Synthesis as Living Dashboard

**Observation**: I just wrote a ~400-line `MASTER_SYNTHESIS.md` that connects the Tauri swarm findings to the SOT vision. This document will become stale within a week as packets are completed.

**Proposal**: Convert the synthesis doc into a generated dashboard:

- A script reads: STATUS.md, GUIDANCE.md, AGGREGATED_TODO.md, and the tauri scan results
- It generates a fresh synthesis with: current sprint state, lane health, acquisition progress, risk register
- Run it as part of end-of-window closeout
- Output to `SOT/CODEBASE_TODOS/TAURI_SWARM_REPORTS/DASHBOARD.md`

**Value**: Living document vs. stale snapshot. The founder gets a single-page view of the whole program every time.

**Feeds Lane**: `Orchestr8_jr` (governance tooling)

---

## 7. `IDEA` — Void Zone for Unassigned Code

**Observation**: Code City has three states (gold/teal/purple) but no representation for **unassigned files** — files that exist but aren't part of any fiefdom, aren't health-checked, and aren't tracked by any agent.

**Proposal**: Add a fourth visual state — **Void** (the background color `#0A0A0B` from the Void design):

- Unassigned files render as dim, translucent ghost buildings
- They sit at the edges of the city, outside any neighbourhood
- Clicking one prompts: "This file has no owner. Assign to fiefdom?"

This aligns with the Mingos philosophy: things emerge from the Void when they're needed. Unassigned files are potential — not absence.

**Value**: Visual accountability. You can immediately see what percentage of your codebase is "in the Void" vs. actively managed.

> [!NOTE]
> This idea pushes against the "three states only" contract in `CODE_CITY_PLAN_LOCK.md`. It would need explicit founder approval to add a fourth visual state. The alternative is to render void files as very dim gold (working but unassigned).

**Feeds Lane**: `mingos_settlement_lab` (visual specs) + `Orchestr8_jr` (contract change)

---

## Meta: How to Use This Channel

1. Anyone can file ideas by appending to this file
2. Ideas get discussed in agent comms: `scripts/agent_comms.sh send <agent> antigravity P07 idea true "<feedback>"`
3. Founder marks ideas as `PROPOSED` to signal lane assignment
4. Lane owner marks `ACCEPTED` when the idea enters their worklist
5. Ideas that conflict with existing contracts are marked `PARKED` with reason

---

*Filed by antigravity. Read the SOT, did the scan, these fell out.*

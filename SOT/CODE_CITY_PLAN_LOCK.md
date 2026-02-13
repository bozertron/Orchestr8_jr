# CODE CITY PLAN LOCK (orchestr8)

Generated: 2026-02-12 22:40:19 PST  
Status: Active implementation contract  
Naming lock: orchestr8 only

## 1. Canonical UI Frame

```
┌─────────────────────────────────────────────────────────────────┐
│ [orchestr8]              [collabor8]              [JFDI]        │
├─────────────────────────────────────────────────────────────────┤
│                           THE VOID                              │
│              (Code City / App Matrix / Chat)                    │
│         Gold = Working    Teal = Broken    Purple = Combat      │
├─────────────────────────────────────────────────────────────────┤
│ [Apps] [Calendar*] [Comms*] [Files] == [maestro] == [Search]    │
│ [Record] [Playback] [Phreak>] [Send] [Attach] [Settings]        │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Color/State Contract

- Working: `#D4AF37`
- Broken: `#1fbdea`
- Combat: `#9D4EDD`
- Void background: `#0A0A0B`
- Elevated surface: `#121214`
- Three states only for health/combat state encoding

## 3. Building Geometry Contract

- Height formula: `3 + (exports * 0.8)`
- Footprint formula: `2 + (lines * 0.008)`
- Building = particle structure (Barradeau-derived)
- Rooms = functions/classes inside the file
- Neighborhood = cluster of related buildings

## 4. Code City Data Flow Contract

- Required health flow:
- `File Change -> HealthWatcher -> HealthChecker -> STATE_MANAGERS -> Code City`
- Connection source of truth: `IP/connection_verifier.py`
- Combat source of truth: `IP/combat_tracker.py`
- Context source of truth for Summon/Collabor8 overlays: `IP/carl_core.py`

## 5. Panel/Interaction Contracts

### 5.1 Connection Panel

- Show explicit file-level relationship names
- No per-wire rainbow coloring
- Clicking a connection highlights full signal path across related nodes

### 5.2 Building Panel

- Show imports, exports, routines/rooms
- Include current state (gold/teal/purple)
- Include combat/ticket/context references when available

### 5.3 Sitting Room

- Entry trigger: room/function issue or selected error context
- Transition: particle morph from building/room into collaboration view
- Exit returns to previous Code City focus context

### 5.4 Patchbay Rewiring

- Drag connection from source to target
- Validate border/contract compatibility before write
- Write path updates real import statements
- Re-run verification and update visualization state

## 6. Rendering Contract

- Primary path: WebGPU `particle_gpu_field` (compute + render)
- Fallback path: current CPU canvas renderer
- Control semantics shared across both paths:
- `densit8`, `orbit8`, `focus8`, `layer8`, audio-reactive mapping
- Keep existing control panel and labels stable

## 7. Implementation Order (One Feature At A Time)

1. Stabilize WebGPU runtime and telemetry
2. Lock building sizing + panel data structures
3. Implement connection panel + signal path highlighting
4. Implement Sitting Room transition + handoff contract
5. Implement Patchbay rewiring workflow
6. Validate end-to-end health/combat/context synchronization

## 8. Acceptance Gates

- UI frame matches canonical lock
- Color contract unchanged
- Formula contract used in runtime building generation
- Signal path highlighting works from connection click
- WebGPU and CPU fallback both functional
- No uncontrolled scope creep between phases

# Orchestr8 Vision Alignment Document

**Date:** 2026-02-12
**Participants:** Founder (Ben) + Claude
**Status:** LOCKED — All decisions finalized

---

## Executive Summary

This document captures the vision alignment session that established the foundational decisions for Orchestr8's development. These decisions are **LOCKED** and should not be changed without explicit Founder approval.

---

## The Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  orchestr8 (Marimo, Python)                                     │
│  ─────────────────────────────                                  │
│  The STAGING GROUND. The conductor's podium.                    │
│  Ben uses THIS to see connections, visualize the codebase,      │
│  and "knit together" the dense stereOS system.                  │
│                                                                 │
│  The orchestra practices on orchestr8 itself first.             │
│                                                                 │
│                         ↓ stages / visualizes                   │
│                                                                 │
│  stereOS (Tauri, Rust, JS, TS, Three.js, html)                 │
│  ───────────────────────────────────                            │
│  THE PRODUCT. The actual application.                           │
│  Bound to ∅明nos as the UI that "observes the Void."            │
│                                                                 │
│                         ↓ contains / displays                   │
│                                                                 │
│  ∅明nos (Mingos)                                                │
│  ───────                                                        │
│  The visual representation of Electronic Pixel Orchestra's      │
│  internal business systems. Not a coding tool — the city       │
│  where hardware/firmware commercialization, product dev,       │
│  energy systems, modular housing programs LIVE as space.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Locked Decisions

### Point 1: Building Anatomy & Formula

| Decision | Value |
|----------|-------|
| **Height formula** | `3 + (exports × 0.8)` — taller = more contribution to system |
| **Footprint formula** | `2 + (lines × 0.008)` — wider = more implementation |
| **Building** | Particle cluster using Barradeau technique |
| **Panel** | Exterior I/O interface (imports, exports, routines) with file names clearly labeled |
| **Rooms** | Interior functions/classes |
| **Edges** | Relationship-based, dynamic, reflects reality in real-time |
| **Interaction** | Patchbay rewiring — drag connections to rewire code |
| **Sitting Room** | Particles morph into collaboration space for human+LLM discussion |
| **Terminology** | "Neighborhood" (not "Fiefdom") for UI/display |

**REJECTED:**

- Fiefdom = building (WRONG — neighborhood contains multiple buildings)
- Pre-defined edges (WRONG — edges render from actual relationships)
- Red for errors (WRONG — teal indicates broken state)
- Complex state gradients (WRONG — three states only)
- Breathing animations (FORBIDDEN — things EMERGE, not breathe)

---

### Point 2: Health Checking & Telemetry

| Decision | Value |
|----------|-------|
| **Check frequency** | File watcher (real-time, dynamic) |
| **Watcher mechanism** | Marimo's `FileWatcherManager` + watchdog |
| **VS Code integration** | postMessage bridge to Marimo iframe |
| **Barradeau integration** | Reference implementation, patterns extracted during integration |
| **Health visualization** | Building TEAL → Room with error GLOWS → Click to enter Sitting Room |

**Data Flow:**

```
File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City
```

**Connection Panel Behavior:**

- NOT each import/export has its own color (visual nightmare)
- Connection panel shows file names clearly
- Clicking a connection GLOWS that signal path everywhere it connects

**Barradeau Reference Files:**

- `one integration at a time/Barradeau/void-phase0-buildings.html` — PRIMARY
- `one integration at a time/Barradeau/barradeau-3d.html` — SECONDARY
- Align colors: `#C9A962` → `#D4AF37` (canonical gold)

---

### Point 3: Campaign Log Format

| Decision | Value |
|----------|-------|
| **Format** | JSON files |
| **Location** | `.orchestr8/campaigns/` |
| **Purpose** | Track Settlement System deployments, agent work, outcomes |

**Rationale:** Structured, easy to parse, can be read by agents for historical context.

---

### Point 4: Combat Staleness

| Decision | Value |
|----------|-------|
| **Threshold** | Manual only |
| **Behavior** | No automatic cleanup of inactive deployments |

**Rationale:** Full control — Founder decides when to clear combat status.

---

### Point 5: Carl vs Louis (Two Distinct Characters)

#### Carl = Context Carl (Data Collector)

| Aspect | Value |
|--------|-------|
| **Role** | Collect and present data to agents — NOT blocking |
| **Signal sources** | HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden |
| **Output** | FiefdomContext JSON for agents and Summon panel |
| **UI** | Summon panel with search + context display |
| **Priority** | HIGH — implement this round |

**Carl's Output Structure:**

```json
{
  "fiefdom": "IP/",
  "health": { "status": "broken", "errors": [...] },
  "connections": { "imports_from": [...], "broken": [...] },
  "combat": { "active": true, "model": "claude-3" },
  "tickets": ["TICKET-001"],
  "locks": [{"file": "louis_core.py", "reason": "Core protection"}]
}
```

#### Louis = Lock 'Em Up Louis (The Blocker)

| Aspect | Value |
|--------|-------|
| **Role** | Block edits to production files |
| **Mechanism** | chmod 444 (locked) / chmod 644 (unlocked) |
| **UI** | Gatekeeper plugin (03_gatekeeper.py) |
| **Status** | ✅ COMPLETE — no changes needed |

**They don't cross paths.** Carl gathers intel. Louis locks doors.

---

### Point 6: Mermaid Generator

| Decision | Value |
|----------|-------|
| **Status** | KEEP |
| **Integration** | Carl deploys Mermaid diagrams to agents in briefing documents |

**Rationale:** Visual diagrams help agents understand code structure quickly.

---

## Color System (Canonical)

```css
:root {
    /* State Colors — THREE STATES ONLY */
    --gold-metallic: #D4AF37;    /* Working state */
    --blue-dominant: #1fbdea;    /* Broken state, UI default */
    --purple-combat: #9D4EDD;    /* Combat state - General deployed */

    /* Gold Variations */
    --gold-dark: #B8860B;        /* Borders, strokes */
    --gold-saffron: #F4C430;     /* Highlights */

    /* Background — The Void */
    --bg-primary: #0A0A0B;       /* THE VOID — potential, not absence */
    --bg-elevated: #121214;      /* Surface/cards */
    --bg-surface: #1a1a1c;       /* Additional surface */
}
```

---

## Key Architecture Decisions

### 1. Relationship-Based Edges

Edges are NOT pre-defined. They render from actual file relationships. If code changes, visualization reflects reality automatically.

### 2. Emergence, Not Animation

UI elements do not "load" or "breathe" — they EMERGE when summoned. The only motion is emergence from the Void.

### 3. Patchbay Rewiring

Humans can physically rewire files by dragging connections from one building to another. The system updates actual code imports.

### 4. Sitting Room Collaboration

When a room (function) has an issue, click to enter the Sitting Room — particles morph into a presentation area where human and LLM collaborate on fixes.

### 5. Signal Path Visualization

Clicking a connection highlights the ENTIRE signal path — all places that connection touches glow, making dependencies traceable at a glance.

---

## vscode-marimo Integration

The vscode-marimo extension provides telemetry via postMessage bridge:

```
VS Code Extension → File Watcher → Telemetry Aggregator → postMessage → Marimo iframe
```

**Note:** Official extension is being deprecated. May need to fork or create standalone Orchestr8 extension.

---

## File Structure Reference

```
IP/
├── carl_core.py           # Context aggregator
├── louis_core.py          # File locker (COMPLETE)
├── health_checker.py      # Health checking (needs wiring)
├── connection_verifier.py # Import resolution (WORKING)
├── combat_tracker.py      # LLM deployment tracking
├── briefing_generator.py  # Agent mission briefings
├── mermaid_generator.py   # Diagram generation (KEEP)
├── woven_maps.py          # Code City visualization
└── plugins/
    ├── 06_maestro.py      # Main UI (Summon panel needs Carl)
    ├── 03_gatekeeper.py   # Louis UI (COMPLETE)
    └── components/        # Panel components

vscode-marimo/             # VS Code extension (needs telemetry work)
```

---

## Next Steps

1. Execute Phases 2-9 of the planning process
2. Wire HealthChecker to Code City
3. Implement Carl's `gather_context()` method
4. Replace Summon panel placeholder with Carl integration
5. Implement file watcher for real-time health updates
6. Integrate Barradeau patterns from reference HTML files

---

**Document Status:** LOCKED
**Last Updated:** 2026-02-12
**Next Review:** After Phase 9 completion

# CONTEXT.md — Settlement System
## Generated: 2026-02-12
## Source: Vision Walker Alignment Session
## Status: AUTHORITATIVE

---

## How to Read This Document

| Classification | Meaning |
|----------------|---------|
| **LOCKED** | Non-negotiable. Do exactly this. Violating these is a critical error. |
| **CONSTRAINT** | Boundary condition. Must NOT happen. Violating this is failure. |
| **PREFERENCE** | Try to honor. May flex if technical reality conflicts, but document deviation. |
| **FLEXIBLE** | Agent discretion granted. Make reasonable choices. |
| **DEFERRED** | Do not implement now. Explicitly postponed to future work. |

---

## Project Priority Order

1. **Wire HealthChecker to Code City** — Real-time health visualization is foundational
2. **Implement Carl's `gather_context()` method** — Context aggregation enables agent deployment
3. **Replace Summon panel placeholder with Carl integration** — UI needs functional context display
4. **Implement file watcher for real-time health updates** — Enables dynamic visualization
5. **Integrate Barradeau patterns from reference HTML files** — Building visualization refinement

---

## Fiefdom: Building Anatomy

### Founder's Vision
Buildings in Code City represent source files. Their physical dimensions encode semantic information about the code — taller buildings contribute more to the system, wider buildings contain more implementation.

### LOCKED Decisions
- **HEIGHT FORMULA:** `3 + (exports × 0.8)` — taller = more contribution to system
- **FOOTPRINT FORMULA:** `2 + (lines × 0.008)` — wider = more implementation
- **BUILDING IMPLEMENTATION:** Particle cluster using Barradeau technique
- **PANEL DEFINITION:** Exterior I/O interface (imports, exports, routines) with file names clearly labeled
- **ROOMS DEFINITION:** Interior functions/classes
- **EDGES IMPLEMENTATION:** Relationship-based, dynamic, reflects reality in real-time
- **INTERACTION MODEL:** Patchbay rewiring — drag connections to rewire code
- **SITTING ROOM DEFINITION:** Particles morph into collaboration space for human+LLM discussion
- **UI TERMINOLOGY:** "Neighborhood" (NOT "Fiefdom") for all UI/display contexts

### Constraints
- **NO:** Fiefdom = building (neighborhood CONTAINS multiple buildings)
- **NO:** Pre-defined edges (edges render from ACTUAL relationships)
- **NO:** Complex state gradients (THREE STATES ONLY)
- **NO:** Breathing animations (FORBIDDEN — things EMERGE, not breathe)
- **NO:** Red for errors (teal indicates broken state)

### Preferences
- Reference Barradeau technique for particle aesthetics
- File names must be clearly labeled on panels

### Flexible Areas
- Exact particle clustering algorithms
- Visual embellishments that don't violate emergence principle

### Deferred to Later
- None identified

---

## Fiefdom: Health Checking & Telemetry

### Founder's Vision
Real-time health monitoring that flows through the system and updates Code City dynamically. No polling — file watcher drives everything.

### LOCKED Decisions
- **CHECK FREQUENCY:** File watcher (real-time, dynamic)
- **WATCHER MECHANISM:** Marimo's `FileWatcherManager` + watchdog
- **VS CODE INTEGRATION:** postMessage bridge to Marimo iframe
- **HEALTH VISUALIZATION FLOW:** Building TEAL → Room with error GLOWS → Click to enter Sitting Room
- **DATA FLOW:** `File Change → HealthWatcher → HealthChecker → STATE_MANAGERS → Code City`

### Constraints
- **NO:** Each import/export has its own color (visual nightmare)
- **NO:** Automatic combat staleness cleanup (manual only)

### Preferences
- Clicking a connection GLOWS that signal path everywhere it connects
- Connection panel shows file names clearly

### Flexible Areas
- Exact glow animation timing
- Panel layout details

### Deferred to Later
- None identified

---

## Fiefdom: Campaign Log

### Founder's Vision
Structured tracking of Settlement System deployments, agent work, and outcomes.

### LOCKED Decisions
- **FORMAT:** JSON files
- **LOCATION:** `.orchestr8/campaigns/`

### Constraints
- Must be structured and parseable by agents

### Preferences
- Include historical context for agent decision-making

### Flexible Areas
- Exact schema structure
- Retention policy

### Deferred to Later
- None identified

---

## Fiefdom: Carl (Context Carl)

### Founder's Vision
Carl is the data collector — he gathers intelligence and presents it to agents and the UI. He does NOT block anything.

### LOCKED Decisions
- **ROLE:** Collect and present data to agents — NOT blocking
- **SIGNAL SOURCES:** HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden
- **OUTPUT FORMAT:** FiefdomContext JSON
- **UI:** Summon panel with search + context display
- **PRIORITY:** HIGH — implement this round
- **MERMAID INTEGRATION:** Carl deploys Mermaid diagrams to agents in briefing documents

### Carl's Output Structure (LOCKED)
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

### Constraints
- **NO:** Blocking behavior
- **NO:** Overlapping with Louis functionality

### Preferences
- Fast context gathering
- Clear, actionable output

### Flexible Areas
- Internal implementation details
- Caching strategy

### Deferred to Later
- None identified

---

## Fiefdom: Louis (Lock 'Em Up Louis)

### Founder's Vision
Louis is the blocker — he locks production files to prevent accidental modification.

### LOCKED Decisions
- **ROLE:** Block edits to production files
- **MECHANISM:** chmod 444 (locked) / chmod 644 (unlocked)
- **UI:** Gatekeeper plugin (03_gatekeeper.py)
- **STATUS:** COMPLETE — no changes needed

### Constraints
- **NO:** Changes to Louis (he's done)
- **NO:** Carl crossing into Louis territory

### Preferences
- Maintain existing behavior

### Flexible Areas
- None (complete)

### Deferred to Later
- None

---

## Fiefdom: Color System

### Founder's Vision
Three states only. No gradients. No complexity. The Void is potential, not absence.

### LOCKED Decisions
- **WORKING STATE:** `#D4AF37` (gold-metallic)
- **BROKEN STATE:** `#1fbdea` (blue-dominant, teal)
- **COMBAT STATE:** `#9D4EDD` (purple-combat)
- **BACKGROUND (THE VOID):** `#0A0A0B`
- **STATE COUNT:** THREE STATES ONLY

### Constraints
- **NO:** Complex state gradients
- **NO:** Additional states without Founder approval
- **NO:** Red for errors

### Preferences
- **Gold dark:** `#B8860B` (borders, strokes)
- **Gold saffron:** `#F4C430` (highlights)
- **Elevated background:** `#121214`
- **Surface background:** `#1a1a1c`

### Flexible Areas
- Minor variations for accessibility if needed (document deviations)

### Deferred to Later
- None

---

## Fiefdom: Architecture Principles

### Founder's Vision
Code City is not decoration — it carries semantic information. Things emerge from the Void.

### LOCKED Decisions
- **RELATIONSHIP-BASED EDGES:** Edges are NOT pre-defined. They render from actual file relationships. If code changes, visualization reflects reality automatically.
- **EMERGENCE PRINCIPLE:** UI elements do not "load" or "breathe" — they EMERGE when summoned. The only motion is emergence from the Void.
- **PATCHBAY REWIRING:** Humans can physically rewire files by dragging connections from one building to another. The system updates actual code imports.
- **SITTING ROOM COLLABORATION:** When a room (function) has an issue, click to enter the Sitting Room — particles morph into a presentation area where human and LLM collaborate on fixes.
- **SIGNAL PATH VISUALIZATION:** Clicking a connection highlights the ENTIRE signal path — all places that connection touches glow, making dependencies traceable at a glance.

### Constraints
- **NO:** Breathing/pulsing animations
- **NO:** Pre-defined edge configurations
- **NO:** "Probably" in border contracts — explicit only

### Preferences
- Motion should feel like emergence, not animation
- Every file belongs to exactly ONE neighborhood

### Flexible Areas
- Exact timing of emergence animations
- Interaction feedback details

### Deferred to Later
- None

---

## Fiefdom: vscode-marimo Integration

### Founder's Vision
VS Code extension provides telemetry to the Marimo dashboard running in iframe.

### LOCKED Decisions
- **INTEGRATION METHOD:** postMessage bridge to Marimo iframe
- **DATA FLOW:** `VS Code Extension → File Watcher → Telemetry Aggregator → postMessage → Marimo iframe`

### Constraints
- Official extension being deprecated — may need alternative

### Preferences
- Fork official Marimo extension if possible
- Maintain compatibility with existing workflows

### Flexible Areas
- Implementation approach (fork vs. standalone)
- Extension architecture details

### Deferred to Later
- Full vscode-marimo telemetry implementation
- Extension fork/creation decision

---

## Fiefdom: Barradeau Integration

### Founder's Vision
Extract and apply Barradeau patterns for building visualization.

### LOCKED Decisions
- **PRIMARY REFERENCE:** `one integration at a time/Barradeau/void-phase0-buildings.html`
- **SECONDARY REFERENCE:** `one integration at a time/Barradeau/barradeau-3d.html`
- **COLOR ALIGNMENT:** `#C9A962` → `#D4AF37` (canonical gold)

### Constraints
- Must align with canonical color system

### Preferences
- Extract patterns during integration rather than wholesale copy

### Flexible Areas
- Implementation details
- Additional optimizations

### Deferred to Later
- None

---

## Fiefdom: Mermaid Generator

### Founder's Vision
Visual diagrams help agents understand code structure quickly.

### LOCKED Decisions
- **STATUS:** KEEP
- **INTEGRATION:** Carl deploys Mermaid diagrams to agents in briefing documents

### Constraints
- Must integrate with Carl's briefing generation

### Preferences
- Clear, readable diagram output

### Flexible Areas
- Diagram styling
- Output format options

### Deferred to Later
- None

---

## Founder's Success Criteria

1. **Code City renders** with buildings sized by formula
2. **Health updates flow** from file watcher to visualization in real-time
3. **Carl provides context** to Summon panel and agent briefings
4. **Three-state color system** works consistently
5. **Things emerge** — no breathing animations
6. **Clicking connections** shows full signal path
7. **Sitting Room** enables human+LLM collaboration on problematic code

---

## Anti-Goals

What Founder explicitly does NOT want:

1. **Breathing/pulsing animations** — Things emerge, they don't breathe
2. **Complex color gradients** — Three states only
3. **Red for errors** — Teal indicates broken state
4. **Pre-defined edges** — Edges come from actual relationships
5. **Carl blocking operations** — Carl collects, Louis blocks
6. **Automatic combat cleanup** — Manual control only
7. **Per-connection colors** — Visual nightmare
8. **Changes to Louis** — He's complete
9. **"Probably" in contracts** — Explicit only
10. **Multiple neighborhood membership** — One file, one neighborhood

---

## Gaps in Coverage

The following areas were not explicitly addressed in the Vision Alignment session and may require clarification:

1. **Exact schema for Campaign Log JSON** — Structure implied but not defined
2. **Retention policy for campaign logs** — How long to keep?
3. **Error severity levels** — Are all errors treated equally in visualization?
4. **Multi-file transaction handling** — If multiple files change simultaneously
5. **Accessibility requirements** — Color blind considerations?
6. **Performance thresholds** — Maximum file count before degradation?
7. **Backup/restore procedures** — For protected files and locks

---

## File Structure Reference

```
IP/
├── carl_core.py           # Context aggregator (HIGH PRIORITY)
├── louis_core.py          # File locker (COMPLETE — DO NOT MODIFY)
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
.orchestr8/campaigns/      # Campaign log storage (to be created)
```

---

**Document Status:** AUTHORITATIVE
**Last Updated:** 2026-02-12
**Next Review:** After Phase 9 completion or Founder request

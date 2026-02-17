# Orchestr8

## What This Is

Orchestr8 is the initial settlement of ∅明nos — a Marimo-based spatial environment where human and machine intelligence collaborate through shared visual experience. It provides a Code City visualization (Woven Maps), multi-agent coordination via the Settlement System, and a stereOS interface that renders codebases as living cities. The Founder sees the whole system; agents work room by room.

## Core Value

The Code City visualization must render as an accurate, interactive spatial representation of the codebase — every file a building, every connection infrastructure, every health state visible — enabling human and AI to co-inhabit and co-evolve the same space.

## Current Milestone: v2.0 Vision Audit + Full Wiring

**Goal:** Systematically audit every file, plugin, and feature against the ∅明nos vision; complete v1.0 wiring; connect Settlement System output to Code City.

**Target features:**
- Complete v1.0 wiring (nav, health, briefing, combat)
- Audit every IP module and plugin against the vision
- Ensure every Marimo integration uses correct reactive methods
- Connect Settlement System survey data to Code City rendering
- Wire Collabor8 panel to settlement agent deployment status
- Identify and remove dead code / stale references
- Validate full pipeline: orchestr8.py → plugins → woven_maps → Code City

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- [x] Code City visualization (Woven Maps) - 78KB complete
- [x] Import graph analysis (connection_verifier.py) - 34KB complete
- [x] Multi-language health checking (health_checker.py) - 22KB complete
- [x] Database converter (connie.py) - 13KB complete
- [x] Ticket system (ticket_manager.py) - 8KB complete
- [x] File locking (louis_core.py) - 5KB complete
- [x] Combat tracking (combat_tracker.py) - 4KB complete
- [x] Cross-platform terminal spawning - 4KB complete
- [x] Slide-out panels (Ticket, Calendar, Comms, FileExplorer) - all complete
- [x] Chat with Claude API - working

### Active

<!-- Current scope. Building toward these. -->

- [ ] Top row buttons wired correctly
- [ ] HealthChecker instantiated and updating node colors
- [ ] Campaign log parsing implemented
- [ ] Combat cleanup on initialization
- [ ] Every IP module audited against vision
- [ ] Every plugin audited against vision
- [ ] Settlement System data → Code City integration
- [ ] Marimo reactive methods verified correct
- [ ] Collabor8 panel wired to settlement agent status

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- vscode-marimo plugin development — defer to v3.0, scaffold only exists
- ∅明nos multi-tenant architecture — defer to v3.0+, requires stereOS completion
- State synchronization (Tickets/Combat/Briefings linked) — defer to v2.1
- Summon/Carl search integration — low priority, defer

## Context

**Existing Codebase:** Brownfield project with 12 core IP modules, 9 plugins, 5 panel components. Most functionality exists but is not wired to the UI.

**Key Problems Identified:**
1. Top row buttons don't match spec
2. JFDI doesn't use the built TicketPanel
3. HealthChecker is imported but never instantiated
4. Campaign log stub returns empty list
5. Brand still says "stereOS"
6. CSS classes use `.stereos-*` prefix

**Source of Truth Documents:**
- `SOT/CURRENT_STATE.md` — Complete audit
- `SOT/UI_SPECIFICATION.md` — Approved UI spec
- `SOT/WIRING_PLAN.md` — Prioritized fix plan
- `GSD + Custom Agents/SETTLEMENT_SYSTEM_PRESSURE_TEST.md` — Settlement architecture
- `GSD + Custom Agents/The_Story_of_Mingos_A_Tale_of_Emergence.md` — Origin story and vision

## Constraints

- **Tech stack:** Marimo 0.19.6 (older API, some limitations)
- **Target file:** Most changes in `IP/plugins/06_maestro.py` (44KB)
- **Validation:** Must pass `marimo run orchestr8.py` without errors

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Top row: [orchestr8] [collabor8] [JFDI] [gener8] | Per UI spec, naming rule: ends with 8 = lowercase start | — Pending |
| JFDI → TicketPanel (not new panel) | Component already built, just needs wiring | — Pending |
| gener8 → Settings | User decided settings is the function | — Pending |
| Remove ~~~ waves button | Not part of spec | — Pending |

---
*Last updated: 2026-02-12 after v2.0 milestone initialization*

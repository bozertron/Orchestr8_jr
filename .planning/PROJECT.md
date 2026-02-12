# Orchestr8

## What This Is

Orchestr8 is a Marimo-based developer tool that enables a human operator ("The Emperor") to coordinate multiple Claude Code instances ("Generals") across a complex codebase. It provides a "God View" dashboard with Code City visualization, terminal spawning, ticket management, and a three-color health system (Gold/Blue/Purple).

## Core Value

The Code City visualization must render with accurate health status colors, showing the Emperor which fiefdoms (directories) need attention and which Generals are deployed.

## Current Milestone: v1.0 Wiring Phase

**Goal:** Connect existing built components to the UI — the components exist, they just need to be wired.

**Target features:**
- Replace stereOS branding with orchestr8
- Wire top row buttons correctly (JFDI→TicketPanel, gener8→Settings)
- Instantiate HealthChecker for live status
- Implement campaign log parsing
- Auto-cleanup stale combat deployments

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

- [ ] Brand replacement (stereOS → orchestr8)
- [ ] Top row buttons wired correctly
- [ ] HealthChecker instantiated and updating node colors
- [ ] Campaign log parsing implemented
- [ ] Combat cleanup on initialization

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- State synchronization (Tickets/Combat/Briefings linked) — defer to v1.1, requires MissionManager design
- Collabor8 agent panel replacement — defer to v1.1, needs agent deployment strategy
- Summon/Carl search integration — defer to v1.1, low priority
- Director background thread fixes — accept manual refresh for MVP

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
*Last updated: 2026-01-30 after milestone initialization*

# Planning Notes — What We Know

## Scope

**Two directories, every file:**
- `SOT/` — 7 spec docs, 2,418 lines
- `IP/` — 35 source files, 12,623 lines (+ CSS, docs)
- Plus: `orchestr8.py` entry point (239 lines)

## What Already Exists (Found Piles)

### `.orchestr8/tickets/` — Working ticket system
- Has 1 test ticket (5f9f6e77.json)
- Archive directory exists
- ticket_manager.py is complete
- ticket_panel.py is complete
- **BUT** JFDI button in 06_maestro.py shows placeholder instead of using it

### `one integration at a time/888/` — Staging area with adapters
- 11 subsystem adapters: actu8, calendar, comms, communic8, cre8, director, innov8, integr8, panel_foundation, professor, senses
- Each has `__init__.py` + `adapter.py`
- Director has extra files: ooda_engine.py, predictive_engine.py, etc.
- panel_foundation has base_panel.py + panel_registry.py
- **These are the INTEGRATIONS waiting to be wired in**

### `one integration at a time/.taskmaster/` — Task Master data
- Has tasks.json with existing task definitions
- Integration queue managed here

### `ui/components/` — Ghost directory
- Only has __pycache__ from old ticket_panel.py
- Real components live at IP/plugins/components/
- This directory can be cleaned up

## The 14 Known Wiring Problems

From SOT/CURRENT_STATE.md + Big Pickle/wiring_problems.md:

| # | Problem | Our Phase | Severity |
|---|---------|-----------|----------|
| 1 | sys.path manipulation | 9 (cleanup) | Low |
| 2 | CarlContextualizer hollow | 6 (module audit) | Medium |
| 3 | Generator phase persistence | 7 (plugin audit) | Low |
| 4 | Maestro "coming soon" panels | 2+8 (nav+settlement) | HIGH |
| 5 | Dangling UI actions (buttons only log) | 2 (nav) | HIGH |
| 6 | Gatekeeper no rescan | 7 (plugin audit) | Low |
| 7 | Connie pandas fallback | 7 (plugin audit) | Low |
| 8 | Director async disconnect | 7 (plugin audit) | Medium |
| 9 | Briefing campaign stub | 4 (briefing) | HIGH |
| 10 | Platform assumptions | 9 (cleanup) | Low |
| 11 | Unsynchronized mission state | Deferred v2.1 | Medium |
| 12 | Manual combat cleanup | 4 (combat) | Medium |
| 13 | Brittle alias resolution | 9 (cleanup) | Low |
| 14 | Health check assumptions | 3 (health) | Medium |

## Critical Insight From 06_maestro.py

I read the full 1297 lines. Here's the real situation:

**What WORKS right now:**
- Code City renders via create_code_city() (line 935)
- Chat with Claude API (lines 753-843)
- Terminal spawning (lines 586-621)
- Panel toggling for Calendar/Comms/FileExplorer (lines 441-484)
- Deploy panel for broken nodes (lines 486-564)
- Ticket panel renders when toggled (line 1233)
- All services instantiated (lines 399-407): CombatTracker, BriefingGenerator, TerminalSpawner, all panels

**What's BROKEN/PLACEHOLDER:**
- Line 893: Gener8 only logs `"Switch to Generator tab"` — should open settings
- Lines 1037-1057: Collabor8 panel is `<div>...coming soon...</div>`
- Lines 1059-1079: JFDI panel is `<div>...coming soon...</div>` — despite TicketPanel being instantiated at line 403!
- Lines 1081-1095: Summon panel is `<div>...Integration with Carl contextualizer pending...</div>`
- Lines 1199-1202: ~~~ button only logs
- Line 77: HealthChecker imported, NEVER instantiated
- Line 75: Mermaid generator imported, never used
- Line 907: Button says "Home" instead of "orchestr8"
- Lines 900-903: Extra "Tickets" button not in spec

## Phase Execution Order

```
Phase 2 (Nav) → Phase 3 (Health) → Phase 4 (Brief+Combat)
                                  ↗
Phase 5 (Marimo) ─────────────────→ Phase 6 (Modules) → Phase 7 (Plugins)
                                                       ↘
                                         Phase 8 (Settlement) → Phase 9 (Pipeline)
```

Phases 2-4 are sequential (each builds on previous).
Phase 5 can run parallel with 3-4.
Phase 6-7 sequential after 5.
Phase 8 after 3+6.
Phase 9 after everything.

## How Reports Work

Each phase writes `PHASE-N-*-REPORT.md` BESIDE the files it touched.
When you see the report file appear, that phase is done.
Read the report to verify before starting the next phase.

## Reference Docs (in .planning/codebase/)

Background agents are writing these — check if they've landed:
- SOT-ANALYSIS.md
- IP-CORE-ANALYSIS.md
- IP-PLUGINS-ANALYSIS.md
- IP-COMPONENTS-ANALYSIS.md
- WOVEN-MAPS-DEEP-ANALYSIS.md
- CORE-TRIO-ANALYSIS.md
- DATA-MODULES-ANALYSIS.md
- REMAINING-MODULES-ANALYSIS.md

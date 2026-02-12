# Orchestr8 Current State Audit

**Audit Date:** 2026-01-30
**Auditor:** Claude (Session review-sot-documents-Y89aP)

---

## Executive Summary

**Good news:** Almost everything described in the ROADMAP is ALREADY BUILT.
**Bad news:** Much of it is NOT WIRED UP or uses placeholder UI.

The gap is not implementation - it's integration.

---

## I. What Exists (Implementation Status)

### Core IP Modules

| Module | Size | Purpose | Status |
|--------|------|---------|--------|
| `IP/woven_maps.py` | 78KB | Code City visualization | COMPLETE - Full canvas-based viz with three-color system |
| `IP/connection_verifier.py` | 34KB | Import graph analysis | COMPLETE - Node types, cycles, centrality |
| `IP/health_checker.py` | 22KB | Multi-language health checks | COMPLETE - TypeScript, Python support |
| `IP/connie.py` | 13KB | Database converter | COMPLETE - SQLite to LLM-friendly formats |
| `IP/ticket_manager.py` | 8KB | Ticket system | COMPLETE - Create, update, notes, archive |
| `IP/briefing_generator.py` | 5KB | BRIEFING.md generation | PARTIAL - `load_campaign_log()` is a stub |
| `IP/louis_core.py` | 5KB | File locking | COMPLETE - OS-level chmod locks |
| `IP/mermaid_theme.py` | 5KB | Mermaid styling | COMPLETE - Three-color theming |
| `IP/combat_tracker.py` | 4KB | Deployment tracking | COMPLETE - Purple state management |
| `IP/terminal_spawner.py` | 4KB | Cross-platform terminal | COMPLETE - Linux/Mac/Windows |
| `IP/carl_core.py` | 3KB | Context gatherer | EXISTS - needs integration |
| `IP/mermaid_generator.py` | 2KB | Mermaid graph | COMPLETE - but superseded by woven_maps |

### Plugin Components (Slide-out Panels)

| Component | Purpose | Status |
|-----------|---------|--------|
| `ticket_panel.py` | JFDI ticket panel | COMPLETE - Full UI, wired to TicketManager |
| `calendar_panel.py` | Calendar integration | COMPLETE - Basic implementation |
| `comms_panel.py` | P2P communications | COMPLETE - Basic implementation |
| `file_explorer_panel.py` | File browser | COMPLETE - Basic implementation |
| `deploy_panel.py` | "House a Digital Native?" modal | COMPLETE - Full deploy UI |

### Plugins

| Plugin | Purpose | Status |
|--------|---------|--------|
| `00_welcome.py` | Welcome tab | WORKING |
| `01_generator.py` | 7-Phase Wizard | FIXED (marimo API) |
| `02_explorer.py` | File explorer | FIXED (marimo API) |
| `03_gatekeeper.py` | Louis UI | WORKING |
| `04_connie_ui.py` | Connie UI | WORKING |
| `05_universal_bridge.py` | Tool registry | FIXED (marimo API) |
| `06_maestro.py` | THE VOID | PARTIALLY WIRED |
| `07_settings.py` | Settings | FIXED (marimo API) |
| `08_director.py` | Director | FIXED (marimo API) |

---

## II. What's Wired in 06_maestro.py

### Services Instantiated (Lines 400-407)

```python
combat_tracker = CombatTracker(project_root_path)      # USED
briefing_generator = BriefingGenerator(project_root_path)  # USED (partially)
terminal_spawner = TerminalSpawner(project_root_path)  # USED
ticket_panel = TicketPanel(project_root_path)          # USED
calendar_panel = CalendarPanel(project_root_path)      # USED
comms_panel = CommsPanel(project_root_path)            # USED
file_explorer_panel = FileExplorerPanel(project_root_path)  # USED
deploy_panel = DeployPanel(project_root_path)          # USED
```

### Imports That Are NEVER Used

```python
from IP.health_checker import HealthChecker           # IMPORTED, NEVER INSTANTIATED
from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid  # IMPORTED, NEVER USED
```

### What Works

- Code City visualization (`create_code_city()`) - Line 935
- Chat with Claude API - Lines 753-843
- Terminal spawning - Lines 586-621
- Panel toggling (Calendar, Comms, File Explorer) - Lines 441-484
- Deploy panel for broken nodes - Lines 486-564
- Ticket panel (via separate "Tickets" button) - Line 1233

### What DOESN'T Work

| Issue | Location | Problem |
|-------|----------|---------|
| Brand says "stereOS" | Lines 873-876 | Should be "orchestr8" |
| CSS uses `.stereos-*` classes | Lines 189-200 | Should be `.orchestr8-*` |
| Gener8 button does nothing | Lines 891-894 | Only logs "Switch to Generator tab" |
| JFDI opens placeholder | Lines 1059-1079 | Has "coming soon" text, ignores TicketPanel |
| Collabor8 opens placeholder | Lines 1037-1057 | Has "coming soon" text, no agent wiring |
| Summon opens placeholder | Lines 1081-1095 | Not wired to Carl/search |
| Settings button is "~~~" | Lines 1200-1202 | Should be "gener8" and open settings |
| HealthChecker never runs | Line 77 | Imported but never instantiated |
| Mermaid generator unused | Line 75 | Code City replaced it entirely |

---

## III. Roadmap vs Reality

| Phase | Roadmap Says | Reality |
|-------|--------------|---------|
| Phase 1 | Build mermaid, health checker, spawner | ALL EXIST - but HealthChecker not wired |
| Phase 2 | Create ticket system | COMPLETE - but JFDI button doesn't use it |
| Phase 3 | BRIEFING.md, wisdom system | PARTIAL - `load_campaign_log()` is stub |
| Phase 4 | Git hooks, Louis | Louis exists, hooks not implemented |
| Phase 5 | PyVis interactive graph | SUPERSEDED by Woven Maps (78KB!) |
| Phase 6 | Testing integration | NOT STARTED |

---

## IV. The 14 Known Wiring Problems

From `one integration at a time/Big Pickle/wiring_problems.md`:

1. **sys.path manipulation** - Brittle path resolution (04_connie_ui.py, 08_director.py)
2. **CarlContextualizer hollow** - Only dumps JSON, doesn't influence state
3. **Generator phase locking** - Not persisted across sessions
4. **Maestro "coming soon" panels** - Placeholder UI (Collabor8, JFDI, Summon)
5. **Dangling UI actions** - Buttons only log to console (Gener8, Apps, Matrix, Files)
6. **Gatekeeper no rescan** - Can't remove folders, no auto-refresh
7. **Connie fragile fallback** - Assumes pandas exists
8. **Director async disconnect** - Background thread doesn't trigger UI refresh
9. **Briefing campaign history stub** - Always returns empty list
10. **Platform assumptions** - Hardcoded gnome-terminal, npm run typecheck
11. **Unsynchronized mission state** - Tickets, Combat, Briefings not linked
12. **Manual state cleanup** - Combat status persists on crash
13. **Brittle alias resolution** - Assumes @/ maps to src/
14. **Health check assumptions** - Assumes "typecheck" script exists

---

## V. Summary

### What Works Today

- Code City renders (Woven Maps)
- Chat with Claude works (if API key set)
- Terminal spawning works
- Ticket panel renders (via separate button)
- Slide-out panels (Calendar, Comms, Files) render

### Critical Gaps

1. Top row buttons don't match spec
2. JFDI doesn't use TicketPanel
3. HealthChecker never runs
4. No automatic fiefdom health status
5. Campaign log history is empty
6. Brand still says "stereOS"

### Path Forward

See `SOT/WIRING_PLAN.md` for the comprehensive fix plan.

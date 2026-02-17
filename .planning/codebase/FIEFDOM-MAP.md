# FIEFDOM MAP: Orchestr8

## Generated: 2026-02-12

## Version: 1.0

---

## Overview

| Fiefdom | Files | Total Tokens | Avg Complexity | Agent Estimate | Borders |
|---------|-------|-------------|----------------|----------------|---------|
| Core | 15 | 47,000 | 5.8 | 186 | Plugins, Entry |
| Plugins | 11 | 17,500 | 6.2 | 78 | Core, Components, Entry |
| Components | 6 | 9,200 | 4.5 | 42 | Plugins |
| Entry | 1 | 2,000 | 4.0 | 12 | Core, Plugins |
| Staging | ~30 | 45,000+ | 6.5 | 180 | Future integration |
| **TOTAL** | **63** | **120,700+** | **5.6** | **498** | |

---

## Fiefdom: Core (IP/)

**Boundary:** IP/*.py (15 Python files)
**Boundary Basis:** Directory clustering + functional cohesion (infrastructure modules)
**Boundary Type:** EXPLICIT — DETERMINISTIC

### Buildings

| File | Tokens | Complexity | Rooms | Largest Room | Exports | Health |
|------|--------|------------|-------|-------------|---------|--------|
| woven_maps.py | 13,678 | 8 | 45 | generate_html() 2,100 | 14 | GOLD |
| connection_verifier.py | 6,234 | 7 | 28 | ConnectionVerifier 1,842 | 12 | GOLD |
| health_checker.py | 4,156 | 6 | 22 | HealthChecker 3,068 | 5 | GOLD |
| connie_gui.py | 4,127 | 6 | 18 | ConnieTheConverter 1,678 | 4 | GOLD |
| connie.py | 2,684 | 5 | 14 | ConversionEngine 2,684 | 2 | GOLD |
| woven_maps_nb.py | 4,956 | 5 | 16 | WovenMapsNotebook 1,500 | 14 | GOLD |
| briefing_generator.py | 1,247 | 4 | 8 | generate() 658 | 1 | TEAL |
| ticket_manager.py | 1,806 | 4 | 12 | TicketManager 1,806 | 2 | GOLD |
| combat_tracker.py | 782 | 3 | 10 | CombatTracker 782 | 1 | TEAL |
| louis_core.py | 892 | 3 | 8 | LouisWarden 594 | 2 | GOLD |
| carl_core.py | 687 | 3 | 5 | CarlContextualizer 687 | 1 | GOLD |
| terminal_spawner.py | 834 | 3 | 6 | TerminalSpawner 834 | 1 | GOLD |
| mermaid_theme.py | 987 | 2 | 6 | generate_file_dependency_graph() 234 | 4 | GOLD |
| mermaid_generator.py | 567 | 2 | 4 | generate_empire_mermaid() 234 | 5 | GOLD |
| **init**.py | 182 | 1 | 2 | verify_structure() 98 | 4 | GOLD |

### Border Crossings

| Border | Direction | Crossing Count | Risk | Items |
|--------|-----------|---------------|------|-------|
| → Plugins | Plugins import from Core | 15 | low | All major modules exported |
| → Entry | Entry imports from Core | 0 | none | Entry only imports plugins |
| ← Plugins | Core imports from Plugins | 0 | none | No plugin imports in Core |

### Token Budget

| Tier | Input Budget | Agents | Waves |
|------|-------------|--------|-------|
| Survey | 18,800 | 75 | 3 |
| Pattern Analysis | 11,750 | 22 | 1 |
| Import/Export Mapping | 11,750 | 22 | 1 |
| Execution | per work order | TBD at Tier 8 | TBD |

### Critical Issues

1. **briefing_generator.py:12** - load_campaign_log() is STUB (BREF-01)
2. **combat_tracker.py:60** - cleanup_stale_deployments() not called at startup (CMBT-01)
3. **health_checker.py** - imported but never instantiated in maestro.py (HLTH-01)

---

## Fiefdom: Plugins (IP/plugins/)

**Boundary:** IP/plugins/*.py (11 Python files)
**Boundary Basis:** PLUGIN_PROTOCOL contract + UI tab pattern
**Boundary Type:** EXPLICIT — DETERMINISTIC

### Buildings

| File | Tokens | Complexity | Rooms | Largest Room | Exports | Health |
|------|--------|------------|-------|-------------|---------|--------|
| 06_maestro.py | 5,192 | 8 | 35 | render() 4,042 | 3 | TEAL |
| 07_settings.py | 2,500 | 5 | 12 | render() 1,340 | 3 | GOLD |
| 08_director.py | 2,084 | 5 | 10 | render() 769 | 3 | GOLD |
| 05_universal_bridge.py | 2,028 | 5 | 10 | render() 1,153 | 3 | GOLD |
| 01_generator.py | 1,372 | 4 | 8 | render() 1,157 | 4 | GOLD |
| 04_connie_ui.py | 1,276 | 4 | 10 | render() 1,086 | 3 | GOLD |
| 03_gatekeeper.py | 1,248 | 4 | 8 | render() 1,128 | 3 | GOLD |
| 02_explorer.py | 1,062 | 4 | 8 | render() 662 | 3 | GOLD |
| 00_welcome.py | 385 | 2 | 4 | render() 270 | 3 | GOLD |
| output_renderer.py | 1,076 | 3 | 6 | detect_and_render_output() 160 | 2 | GOLD |
| status_helpers.py | 408 | 1 | 6 | progress_bar() 105 | 6 | GOLD |

### Border Crossings

| Border | Direction | Crossing Count | Risk | Items |
|--------|-----------|---------------|------|-------|
| → Components | Maestro imports components | 5 | low | All 5 panel components |
| → Core | Plugins import from Core | 15 | low | woven_maps, combat_tracker, etc. |
| → Entry | Entry imports plugins | 11 | low | Dynamic plugin discovery |
| ← Core | Core imports from Plugins | 0 | none | No core imports from plugins |

### Critical Issues

1. **06_maestro.py:77** - HealthChecker imported but NEVER instantiated
2. **06_maestro.py:1037-1057** - Collabor8 panel is PLACEHOLDER HTML
3. **06_maestro.py:1059-1079** - JFDI panel is PLACEHOLDER HTML (should use TicketPanel)
4. **06_maestro.py:1081-1095** - Summon panel is PLACEHOLDER HTML
5. **06_maestro.py:893** - Gener8 button only logs, doesn't open Settings
6. **06_maestro.py:907** - Home button says "Home" not "orchestr8"
7. **06_maestro.py:900-903** - Extra Tickets button not in spec
8. **06_maestro.py:1199-1202** - ~~~ waves button exists but shouldn't

---

## Fiefdom: Components (IP/plugins/components/)

**Boundary:** IP/plugins/components/*.py (6 Python files)
**Boundary Basis:** Reusable panel components pattern
**Boundary Type:** EXPLICIT — DETERMINISTIC

### Buildings

| File | Tokens | Complexity | Rooms | Largest Room | Exports | Health |
|------|--------|------------|-------|-------------|---------|--------|
| ticket_panel.py | 1,945 | 4 | 12 | render() 795 | 2 | GOLD |
| calendar_panel.py | 2,100 | 4 | 12 | CALENDAR_PANEL_CSS 1,100 | 2 | GOLD |
| comms_panel.py | 2,120 | 4 | 12 | COMMS_PANEL_CSS 1,080 | 2 | GOLD |
| deploy_panel.py | 1,860 | 4 | 10 | DEPLOY_PANEL_CSS 920 | 2 | GOLD |
| file_explorer_panel.py | 1,650 | 4 | 12 | FILE_EXPLORER_CSS 700 | 2 | GOLD |
| **init**.py | 45 | 1 | 1 | Documentation 45 | 0 | GOLD |

### Border Crossings

| Border | Direction | Crossing Count | Risk | Items |
|--------|-----------|---------------|------|-------|
| ← Plugins | Components imported by Maestro | 5 | low | All 5 panels instantiated |
| → Core | Components import from Core | 2 | low | TicketManager |

### Integration Status

All 5 panel components are **FULLY WIRED** to 06_maestro.py:

- Instantiation at lines 403-407
- Visibility control via set_visible()
- State management via mo.state() hooks

---

## Fiefdom: Entry (orchestr8.py)

**Boundary:** orchestr8.py (single file)
**Boundary Basis:** Application bootstrap responsibility
**Boundary Type:** EXPLICIT — DETERMINISTIC

### Buildings

| File | Tokens | Complexity | Rooms | Purpose | Health |
|------|--------|------------|-------|---------|--------|
| orchestr8.py | 2,000 | 4 | 8 | Plugin discovery, dynamic loading, main entry | GOLD |

### Border Crossings

| Border | Direction | Crossing Count | Risk | Items |
|--------|-----------|---------------|------|-------|
| → Plugins | Entry imports plugins dynamically | 11 | low | All plugins via importlib |
| → Core | Entry imports from Core | 0 | none | No direct core imports |

---

## Fiefdom: Staging (one integration at a time/888/)

**Boundary:** one integration at a time/888/*/ (11 subsystems)
**Boundary Basis:** Future integration pattern (adapters)
**Boundary Type:** EXPLICIT — FUTURE

### Subsystems

| Subsystem | Purpose | Status |
|-----------|---------|--------|
| actu8 | Terminal/action spawning | Ready |
| calendar | Calendar integration | Ready |
| comms | P2P communications | Ready |
| communic8 | Communication bridge | Ready |
| cre8 | Creation/generation | Ready |
| director | Agent orchestration | Ready |
| innov8 | Innovation/research | Ready |
| integr8 | Integration hub | Ready |
| panel_foundation | Base panel classes | Ready |
| professor | Knowledge/teaching | Ready |
| senses | Data collection | Ready |

### Border Crossings

| Border | Direction | Crossing Count | Risk | Items |
|--------|-----------|---------------|------|-------|
| → Plugins | Future integration | 0 | TBD | Adapters waiting |
| → Core | Future integration | 0 | TBD | Adapters waiting |

---

## Deployment Plan

### Agent Requirements by Tier

| Fiefdom | Survey | Pattern | Import/Export | Execution | Total |
|---------|--------|---------|---------------|-----------|-------|
| Core | 75 | 22 | 22 | 67 | 186 |
| Plugins | 32 | 12 | 12 | 22 | 78 |
| Components | 17 | 7 | 7 | 11 | 42 |
| Entry | 5 | 2 | 2 | 3 | 12 |
| Staging | 30 | 15 | 15 | 120 | 180 |
| **TOTAL** | **159** | **58** | **58** | **223** | **498** |

### Sanity Checks

- ✅ Single file max: 75 agents (woven_maps.py) < 100 threshold
- ✅ Single fiefdom max: 186 agents (Core) < 300 threshold
- ✅ Every tier has >0 agents

---

## Vision Alignment Context

This is the **∅明nos (Mingos)** vision - a spatial environment where code is a living city:

- **Every file** = A building in the Code City
- **Every connection** = Infrastructure (edges between buildings)
- **Every health state** = Visible color (Gold=working, Teal=broken, Purple=combat)
- **Every fiefdom** = A neighborhood with clear boundaries

The Settlement System treats this codebase as a city to be surveyed, mapped, and developed room by room.

---

## Resolution of Ambiguous Files

| File | Original Ambiguity | Resolution | Reasoning |
|------|-------------------|------------|-----------|
| IP/**init**.py | Core or Shared? | Core | Package init for IP/ |
| IP/plugins/**init**.py | Plugins or Shared? | Plugins | Package init for plugins/ |
| IP/plugins/components/**init**.py | Components or Shared? | Components | Package init for components/ |
| output_renderer.py | Plugins or Shared? | Plugins | Only used by universal_bridge |
| status_helpers.py | Plugins or Shared? | Plugins | Only styling utilities |

---

*Map Complete: All files assigned, all borders documented, all budgets calculated.*

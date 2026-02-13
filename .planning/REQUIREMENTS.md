# Requirements: Orchestr8

**Defined:** 2026-01-30
**Updated:** 2026-02-12 (v2.0 milestone)
**Core Value:** Code City visualization as accurate, interactive spatial representation — human and AI co-inhabiting the same space

## v1 Requirements (Completed)

### Branding

- [x] **BRAND-01**: Application displays "orchestr8" instead of "stereOS" in all visible text
- [x] **BRAND-02**: CSS classes use `.orchestr8-*` prefix instead of `.stereos-*`
- [x] **BRAND-03**: Docstrings reference "orchestr8" not "stereOS"

## v2 Requirements

### Navigation (carry-forward from v1)

- [ ] **NAV-01**: Top row displays exactly: [orchestr8] [collabor8] [JFDI] [gener8]
- [ ] **NAV-02**: JFDI button opens the TicketPanel component (not placeholder)
- [ ] **NAV-03**: gener8 button opens Settings panel
- [ ] **NAV-04**: ~~~ waves button is removed from UI

### Health (carry-forward from v1)

- [ ] **HLTH-01**: HealthChecker is instantiated with project root on render
- [ ] **HLTH-02**: Health check results update Code City node colors
- [ ] **HLTH-03**: Refresh action triggers health recheck

### Briefing (carry-forward from v1)

- [ ] **BREF-01**: `load_campaign_log()` parses CAMPAIGN_LOG.md files
- [ ] **BREF-02**: Campaign history displays in briefing panel

### Combat (carry-forward from v1)

- [ ] **CMBT-01**: Stale combat deployments are cleaned up on app initialization
- [ ] **CMBT-02**: Combat status accurately reflects active deployments

### Vision Audit — IP Modules

- [ ] **VMOD-01**: Each IP module has clear purpose aligned to ∅明nos vision
- [ ] **VMOD-02**: woven_maps.py renders Code City per vision spec (buildings, connections, health)
- [ ] **VMOD-03**: connection_verifier.py feeds import graph to Code City correctly
- [ ] **VMOD-04**: health_checker.py results map to Gold/Teal/Purple color system
- [ ] **VMOD-05**: combat_tracker.py integrates with Code City (Purple nodes for active combat)
- [ ] **VMOD-06**: briefing_generator.py produces actionable context, not stubs
- [ ] **VMOD-07**: ticket_manager.py links to JFDI panel correctly
- [ ] **VMOD-08**: louis_core.py file protection functional and UI-connected
- [ ] **VMOD-09**: connie.py database conversion functional
- [ ] **VMOD-10**: terminal_spawner.py cross-platform spawning works
- [ ] **VMOD-11**: carl_core.py has defined purpose or is marked for removal
- [ ] **VMOD-12**: mermaid_generator.py has defined purpose or is marked for removal

### Vision Audit — Plugins

- [ ] **VPLG-01**: 00_welcome.py displays meaningful project overview
- [ ] **VPLG-02**: 01_generator.py serves its stated purpose
- [ ] **VPLG-03**: 02_explorer.py serves its stated purpose
- [ ] **VPLG-04**: 03_gatekeeper.py correctly wires Louis file protection
- [ ] **VPLG-05**: 04_connie_ui.py correctly wires Connie database converter
- [ ] **VPLG-06**: 05_universal_bridge.py serves its stated purpose
- [ ] **VPLG-07**: 06_maestro.py implements full stereOS layout per SOT.md spec
- [ ] **VPLG-08**: 07_settings.py provides functional settings (gener8 target)
- [ ] **VPLG-09**: 08_director.py orchestrates plugin loading correctly

### Vision Audit — Panel Components

- [ ] **VPNL-01**: ticket_panel.py renders and accepts input
- [ ] **VPNL-02**: calendar_panel.py renders and shows schedule data
- [ ] **VPNL-03**: comms_panel.py renders Claude chat integration
- [ ] **VPNL-04**: deploy_panel.py renders combat deployment status
- [ ] **VPNL-05**: file_explorer_panel.py renders project file tree

### Marimo Integration

- [ ] **MRIM-01**: All `mo.ui.*` calls use Marimo 0.19.6 compatible API
- [ ] **MRIM-02**: Reactive state updates use correct `mo.state()` patterns
- [ ] **MRIM-03**: No deprecated or incorrect Marimo methods in codebase
- [ ] **MRIM-04**: `marimo run orchestr8.py` completes without errors or warnings

### Settlement Integration

- [ ] **SETL-01**: Settlement survey data can feed into Code City rendering
- [ ] **SETL-02**: Collabor8 panel displays agent deployment status
- [ ] **SETL-03**: Fiefdom boundaries visible in Code City visualization
- [ ] **SETL-04**: Code City color system reflects Settlement agent activity (Purple = agents active)

### Pipeline Validation

- [ ] **PIPE-01**: orchestr8.py loads all plugins without error
- [ ] **PIPE-02**: Plugin system discovers and orders plugins correctly
- [ ] **PIPE-03**: 06_maestro.py renders full stereOS layout
- [ ] **PIPE-04**: Woven Maps Code City renders with real project data
- [ ] **PIPE-05**: End-to-end: edit a file → health recheck → Code City color updates

### Cleanup

- [ ] **CLEAN-01**: No dead imports across codebase
- [ ] **CLEAN-02**: No stale references to removed features
- [ ] **CLEAN-03**: CSS uses consistent `.orchestr8-*` prefix (no `.stereos-*` remnants)
- [ ] **CLEAN-04**: Config file references are accurate and current

## Deferred (v2.1+)

### State Synchronization

- **SYNC-01**: MissionManager coordinates Tickets/Combat/Briefings
- **SYNC-02**: Creating ticket links to combat deployment
- **SYNC-03**: Completing mission updates all three systems

### Search

- **SRCH-01**: Summon panel integrates with CarlContextualizer
- **SRCH-02**: Global search returns relevant files/code

## Out of Scope

| Feature | Reason |
|---------|--------|
| vscode-marimo plugin development | Defer to v3.0, scaffold only exists |
| ∅明nos multi-tenant architecture | Defer to v3.0+, requires stereOS completion |
| Director background thread fixes | Accept manual refresh for MVP |
| Mobile responsive layout | Desktop-first tool |

## Traceability

Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BRAND-01..03 | Phase 1 | Complete |
| NAV-01..04 | Phase 2 | Pending |
| HLTH-01..03 | Phase 3 | Pending |
| BREF-01..02 | Phase 4 | Pending |
| CMBT-01..02 | Phase 4 | Pending |
| MRIM-01..04 | Phase 5 | Pending |
| VMOD-01..12 | Phase 6 | Pending |
| VPLG-01..09 | Phase 7 | Pending |
| VPNL-01..05 | Phase 7 | Pending |
| SETL-01..04 | Phase 8 | Pending |
| PIPE-01..05 | Phase 9 | Pending |
| CLEAN-01..04 | Phase 9 | Pending |

**Coverage:**
- v1 completed: 3 (BRAND)
- v2 requirements: 52 total
- Mapped to phases: 52 ✓

---
*Requirements defined: 2026-01-30*
*Last updated: 2026-02-12 for v2.0 milestone*

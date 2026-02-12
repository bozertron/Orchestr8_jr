# Roadmap: Orchestr8 v2.0

## Overview

v2.0 Vision Audit + Full Wiring. Systematically audit every file, plugin, and feature against the ∅明nos vision. Complete v1.0 wiring work. Connect Settlement System to Code City. Validate the full pipeline end-to-end.

52 requirements across 9 phases. Phase 1 (Branding) complete from v1.0.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Branding** - Replace stereOS references with orchestr8
- [ ] **Phase 2: Navigation Wiring** - Wire top row buttons to correct components
- [ ] **Phase 3: Health Integration** - Instantiate HealthChecker and update Code City colors
- [ ] **Phase 4: Briefing + Combat** - Wire campaign log and combat cleanup
- [ ] **Phase 5: Marimo Method Audit** - Verify all reactive methods are 0.19.6 compatible
- [ ] **Phase 6: Vision Audit — IP Modules** - Audit every IP module against ∅明nos vision
- [ ] **Phase 7: Vision Audit — Plugins + Panels** - Audit every plugin and panel component
- [ ] **Phase 8: Settlement Integration** - Connect Settlement System data to Code City
- [ ] **Phase 9: Pipeline Validation + Cleanup** - End-to-end validation and dead code removal

## Phase Details

### Phase 1: Branding ✓
**Goal**: Application consistently displays "orchestr8" branding
**Status**: Complete (2026-01-30)
**Requirements**: BRAND-01, BRAND-02, BRAND-03
Plans:
- [x] 01-01-PLAN.md — Replace stereOS branding with orchestr8

### Phase 2: Navigation Wiring
**Goal**: Top row matches UI spec with all buttons wired to correct components

**Depends on**: Phase 1

**Requirements**: NAV-01, NAV-02, NAV-03, NAV-04

**Success Criteria**:
  1. Top row shows exactly: [orchestr8] [collabor8] [JFDI] [gener8]
  2. JFDI opens TicketPanel component
  3. gener8 opens Settings panel
  4. ~~~ waves button absent from UI

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 3: Health Integration
**Goal**: HealthChecker updates Code City node colors based on actual file health

**Depends on**: Phase 2

**Requirements**: HLTH-01, HLTH-02, HLTH-03

**Success Criteria**:
  1. Code City nodes display Gold/Teal/Purple based on file health
  2. Health refresh triggers color update
  3. HealthChecker instantiates without errors on render

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 4: Briefing + Combat
**Goal**: Campaign history displays in briefing panel; combat tracking shows accurate active deployments

**Depends on**: Phase 3

**Requirements**: BREF-01, BREF-02, CMBT-01, CMBT-02

**Success Criteria**:
  1. Briefing panel shows parsed entries from CAMPAIGN_LOG.md
  2. App startup cleans stale combat deployments
  3. Combat status matches actual active deployments
  4. Purple Code City nodes match real combat state

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 5: Marimo Method Audit
**Goal**: Every Marimo API call uses 0.19.6-compatible methods; no deprecated patterns

**Depends on**: Phase 2 (needs nav wiring complete to test full UI)

**Requirements**: MRIM-01, MRIM-02, MRIM-03, MRIM-04

**Success Criteria**:
  1. All `mo.ui.*` calls verified against Marimo 0.19.6 API
  2. State updates use correct `mo.state()` patterns
  3. No deprecated methods in codebase
  4. `marimo run orchestr8.py` produces no warnings

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 6: Vision Audit — IP Modules
**Goal**: Every IP module has clear purpose aligned to ∅明nos vision; dead/undefined modules identified

**Depends on**: Phase 5

**Requirements**: VMOD-01 through VMOD-12

**Success Criteria**:
  1. woven_maps.py verified as Code City renderer per vision spec
  2. connection_verifier.py confirmed feeding import graph correctly
  3. health_checker.py maps to Gold/Teal/Purple color system
  4. combat_tracker.py integrates with Code City Purple
  5. briefing_generator.py produces real context (not stubs)
  6. ticket_manager.py linked to JFDI panel
  7. louis_core.py file protection working + UI-connected
  8. carl_core.py and mermaid_generator.py have defined purpose or marked for removal
  9. All modules have documented vision alignment

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 7: Vision Audit — Plugins + Panels
**Goal**: Every plugin and panel component serves a defined purpose in the stereOS layout

**Depends on**: Phase 6

**Requirements**: VPLG-01 through VPLG-09, VPNL-01 through VPNL-05

**Success Criteria**:
  1. All 9 plugins serve defined purpose (or marked for consolidation)
  2. 06_maestro.py implements full stereOS layout per SOT.md
  3. All 5 panel components render and accept input
  4. Plugin loading order correct in orchestr8.py
  5. No orphaned or dead-end plugins

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 8: Settlement Integration
**Goal**: Settlement System data visible in Code City; Collabor8 panel shows agent status

**Depends on**: Phase 3 (needs Code City colors working), Phase 6 (needs module audit complete)

**Requirements**: SETL-01, SETL-02, SETL-03, SETL-04

**Success Criteria**:
  1. Settlement survey data can populate Code City
  2. Collabor8 panel displays agent deployment status
  3. Fiefdom boundaries visible in visualization
  4. Purple color reflects Settlement agent activity

**Plans**: TBD
Plans:
- [ ] TBD after planning

### Phase 9: Pipeline Validation + Cleanup
**Goal**: End-to-end pipeline works; dead code and stale references removed

**Depends on**: All previous phases

**Requirements**: PIPE-01 through PIPE-05, CLEAN-01 through CLEAN-04

**Success Criteria**:
  1. orchestr8.py loads all plugins without error
  2. Plugin system discovers/orders correctly
  3. 06_maestro.py renders full stereOS layout
  4. Code City renders with real project data
  5. Edit file → health recheck → Code City color updates (E2E)
  6. No dead imports, stale refs, or `.stereos-*` CSS remnants
  7. Config references accurate and current

**Plans**: TBD
Plans:
- [ ] TBD after planning

## Progress

**Execution Order:**
1 → 2 → 3 → 4 (sequential wiring)
5 can start after 2 (parallel with 3+4)
6 → 7 (sequential vision audit)
8 depends on 3 + 6
9 depends on all

| Phase | Plans | Status | Completed |
|-------|-------|--------|-----------|
| 1. Branding | 1/1 | ✓ Complete | 2026-01-30 |
| 2. Navigation Wiring | 0/TBD | Not started | - |
| 3. Health Integration | 0/TBD | Not started | - |
| 4. Briefing + Combat | 0/TBD | Not started | - |
| 5. Marimo Method Audit | 0/TBD | Not started | - |
| 6. Vision Audit: Modules | 0/TBD | Not started | - |
| 7. Vision Audit: Plugins | 0/TBD | Not started | - |
| 8. Settlement Integration | 0/TBD | Not started | - |
| 9. Pipeline + Cleanup | 0/TBD | Not started | - |

---
*Last updated: 2026-02-12 after v2.0 milestone initialization*

# Roadmap: Orchestr8

## Overview

The v1.0 Wiring Phase connects existing built components to the UI. All functionality exists — it just needs wiring. Five focused phases will systematically connect branding, navigation, health checking, briefing data, and combat tracking to deliver the Code City visualization with accurate health status colors.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Branding** - Replace stereOS references with orchestr8
- [ ] **Phase 2: Navigation** - Wire top row buttons to correct components
- [ ] **Phase 3: Health Integration** - Instantiate HealthChecker and update Code City colors
- [ ] **Phase 4: Briefing Data** - Implement campaign log parsing
- [ ] **Phase 5: Combat Cleanup** - Auto-cleanup stale deployments on initialization

## Phase Details

### Phase 1: Branding
**Goal**: Application consistently displays "orchestr8" branding across all visible text, CSS classes, and documentation

**Depends on**: Nothing (first phase)

**Requirements**: BRAND-01, BRAND-02, BRAND-03

**Success Criteria** (what must be TRUE):
  1. User sees "orchestr8" (not "stereOS") in browser tab title and page header
  2. Browser DevTools shows CSS classes prefixed with `.orchestr8-*` (not `.stereos-*`)
  3. Developer reading code sees "orchestr8" references in docstrings and comments

**Plans:** 1 plan

Plans:
- [ ] 01-01-PLAN.md — Replace stereOS branding with orchestr8 (text, CSS, docstrings)

### Phase 2: Navigation
**Goal**: Top row navigation matches UI specification with all buttons wired to correct components

**Depends on**: Phase 1

**Requirements**: NAV-01, NAV-02, NAV-03, NAV-04

**Success Criteria** (what must be TRUE):
  1. User sees exactly four buttons in top row: [orchestr8] [collabor8] [JFDI] [gener8]
  2. Clicking JFDI opens the TicketPanel component (not placeholder text)
  3. Clicking gener8 opens Settings panel
  4. ~~~ waves button is absent from UI
  5. Navigation persists across page refresh without layout shifts

**Plans**: TBD

Plans:
- [ ] TBD after planning

### Phase 3: Health Integration
**Goal**: HealthChecker actively monitors project health and updates Code City visualization with accurate status colors

**Depends on**: Phase 2

**Requirements**: HLTH-01, HLTH-02, HLTH-03

**Success Criteria** (what must be TRUE):
  1. Code City nodes display colors reflecting actual file health (Gold=working, Blue=broken, Purple=combat)
  2. User can trigger health refresh and see colors update based on current state
  3. Health check runs automatically when Code City first renders
  4. Developer console shows no errors related to HealthChecker instantiation

**Plans**: TBD

Plans:
- [ ] TBD after planning

### Phase 4: Briefing Data
**Goal**: Campaign history displays in briefing panel from parsed CAMPAIGN_LOG.md files

**Depends on**: Phase 3

**Requirements**: BREF-01, BREF-02

**Success Criteria** (what must be TRUE):
  1. User sees campaign history entries in briefing panel (not empty list)
  2. Each briefing entry shows parsed content from CAMPAIGN_LOG.md files
  3. Briefing panel updates when new CAMPAIGN_LOG.md files are added

**Plans**: TBD

Plans:
- [ ] TBD after planning

### Phase 5: Combat Cleanup
**Goal**: Combat tracking accurately reflects active deployments with automatic cleanup of stale entries

**Depends on**: Phase 4

**Requirements**: CMBT-01, CMBT-02

**Success Criteria** (what must be TRUE):
  1. Application startup removes stale combat deployments from tracking
  2. Combat status panel shows only currently active deployments
  3. Code City purple nodes match actual combat deployments (no orphaned purple)
  4. User can verify combat status matches reality in `var/deployments/` directory

**Plans**: TBD

Plans:
- [ ] TBD after planning

## Progress

**Execution Order:**
Phases execute sequentially: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Branding | 0/1 | Planned | - |
| 2. Navigation | 0/TBD | Not started | - |
| 3. Health Integration | 0/TBD | Not started | - |
| 4. Briefing Data | 0/TBD | Not started | - |
| 5. Combat Cleanup | 0/TBD | Not started | - |

---
*Last updated: 2026-01-30 after Phase 1 planning*

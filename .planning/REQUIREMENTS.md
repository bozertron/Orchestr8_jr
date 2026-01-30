# Requirements: Orchestr8

**Defined:** 2026-01-30
**Core Value:** Code City visualization must render with accurate health status colors

## v1 Requirements

Requirements for v1.0 Wiring Phase. Each maps to roadmap phases.

### Branding

- [ ] **BRAND-01**: Application displays "orchestr8" instead of "stereOS" in all visible text
- [ ] **BRAND-02**: CSS classes use `.orchestr8-*` prefix instead of `.stereos-*`
- [ ] **BRAND-03**: Docstrings reference "orchestr8" not "stereOS"

### Navigation

- [ ] **NAV-01**: Top row displays exactly: [orchestr8] [collabor8] [JFDI] [gener8]
- [ ] **NAV-02**: JFDI button opens the TicketPanel component (not placeholder)
- [ ] **NAV-03**: gener8 button opens Settings panel
- [ ] **NAV-04**: ~~~ waves button is removed from UI

### Health

- [ ] **HLTH-01**: HealthChecker is instantiated with project root on render
- [ ] **HLTH-02**: Health check results update Code City node colors
- [ ] **HLTH-03**: Refresh action triggers health recheck

### Briefing

- [ ] **BREF-01**: `load_campaign_log()` parses CAMPAIGN_LOG.md files
- [ ] **BREF-02**: Campaign history displays in briefing panel

### Combat

- [ ] **CMBT-01**: Stale combat deployments are cleaned up on app initialization
- [ ] **CMBT-02**: Combat status accurately reflects active deployments

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### State Synchronization

- **SYNC-01**: MissionManager coordinates Tickets/Combat/Briefings
- **SYNC-02**: Creating ticket links to combat deployment
- **SYNC-03**: Completing mission updates all three systems

### Agent Management

- **AGNT-01**: Collabor8 panel shows available agents
- **AGNT-02**: User can assign agent to fiefdom
- **AGNT-03**: Agent status visible in Code City

### Search

- **SRCH-01**: Summon panel integrates with CarlContextualizer
- **SRCH-02**: Global search returns relevant files/code

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Director background thread fixes | Accept manual refresh for MVP |
| Platform-specific hardcoding fixes | Already has fallback chains |
| sys.path manipulation cleanup | Currently working |
| Mobile responsive layout | Desktop-first tool |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BRAND-01 | Phase 1 | Pending |
| BRAND-02 | Phase 1 | Pending |
| BRAND-03 | Phase 1 | Pending |
| NAV-01 | Phase 2 | Pending |
| NAV-02 | Phase 2 | Pending |
| NAV-03 | Phase 2 | Pending |
| NAV-04 | Phase 2 | Pending |
| HLTH-01 | Phase 3 | Pending |
| HLTH-02 | Phase 3 | Pending |
| HLTH-03 | Phase 3 | Pending |
| BREF-01 | Phase 4 | Pending |
| BREF-02 | Phase 4 | Pending |
| CMBT-01 | Phase 5 | Pending |
| CMBT-02 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---
*Requirements defined: 2026-01-30*
*Last updated: 2026-01-30 after initial definition*

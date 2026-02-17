# Phase 6: Vision Audit — IP Modules Summary

**Date:** 2026-02-12  
**Auditor:** Settlement Vision Walker (Tier 5)  
**Scope:** 15 IP core modules  

---

## Executive Summary

| Status | Count | Files |
|--------|-------|-------|
| ✅ Confirmed | 9 | connection_verifier, ticket_manager, louis_core, terminal_spawner, connie, connie_gui, carl_core, mermaid_generator, mermaid_theme |
| ⚠️ Needs Decision | 6 | briefing_generator, combat_tracker, health_checker, woven_maps, woven_maps_nb, __init__ |

**Critical Issues Found:** 4  
**Stub Functions:** 1  
**Unwired Imports:** 1  

---

## Files Requiring Vision Confirmation

### 1. briefing_generator.py
**Issue:** load_campaign_log() is STUB (returns empty list)  
**Requirement:** BREF-01  
**Decision Needed:** Campaign log format (markdown vs JSON vs SQLite)

### 2. combat_tracker.py
**Issue:** cleanup_stale_deployments() exists but never called at startup  
**Requirement:** CMBT-01  
**Decision Needed:** Staleness threshold (24h vs 12h vs manual)

### 3. health_checker.py
**Issue:** Imported in maestro.py but NEVER instantiated  
**Requirements:** HLTH-01, HLTH-02  
**Decision Needed:** Health check frequency (startup vs manual vs periodic)

### 4. woven_maps.py
**Issue:** Doesn't accept health data from HealthChecker  
**Requirement:** HLTH-02  
**Decision Needed:** Building height formula (size vs complexity vs centrality)

---

## Critical Integration Gaps

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION GAPS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HealthChecker ──❌──> 06_maestro.py                        │
│     (imported but not instantiated)                         │
│                                                             │
│  HealthChecker ──❌──> woven_maps.py                        │
│     (no health_data parameter)                              │
│                                                             │
│  combat_tracker.cleanup() ──❌──> startup                   │
│     (method exists, never called)                           │
│                                                             │
│  briefing_generator ──❌──> CAMPAIGN_LOG.md                 │
│     (stub returns empty)                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Vision Alignment Assessment

### Perfect Alignment (No Changes Needed)
- **connection_verifier.py** - Infrastructure/roads between buildings
- **ticket_manager.py** - Work orders for the city
- **louis_core.py** - Security/protection for critical buildings
- **terminal_spawner.py** - Deployment mechanism for agents
- **connie.py** - Data transformation utility

### Good Alignment (Minor Integration)
- **combat_tracker.py** - Combat metaphor perfect, just needs startup wiring
- **woven_maps.py** - Code City centerpiece, needs health data integration

### Needs Completion
- **briefing_generator.py** - Campaign log parsing not implemented
- **health_checker.py** - Fully implemented but not wired to UI

---

## Next Steps

1. **Review individual VISION-REPORT.md files** in IP/ directory
2. **Provide decisions** for each "Decision Required" section
3. **Confirm vision alignment** for files marked "AWAITING VISION CONFIRMATION"
4. **Proceed to Phase 7** (Plugin audit) after confirmation

---

## Individual Reports

Each module has a detailed VISION-REPORT.md file:

- [briefing_generator.VISION-REPORT.md](../IP/briefing_generator.VISION-REPORT.md)
- [combat_tracker.VISION-REPORT.md](../IP/combat_tracker.VISION-REPORT.md)
- [health_checker.VISION-REPORT.md](../IP/health_checker.VISION-REPORT.md)
- [woven_maps.VISION-REPORT.md](../IP/woven_maps.VISION-REPORT.md)
- [carl_core.VISION-REPORT.md](../IP/carl_core.VISION-REPORT.md)
- [mermaid_generator.VISION-REPORT.md](../IP/mermaid_generator.VISION-REPORT.md)
- [connection_verifier.VISION-REPORT.md](../IP/connection_verifier.VISION-REPORT.md)
- [ticket_manager.VISION-REPORT.md](../IP/ticket_manager.VISION-REPORT.md)
- [louis_core.VISION-REPORT.md](../IP/louis_core.VISION-REPORT.md)
- [terminal_spawner.VISION-REPORT.md](../IP/terminal_spawner.VISION-REPORT.md)
- [connie.VISION-REPORT.md](../IP/connie.VISION-REPORT.md)

---

**Status:** AWAITING FOUNDER VISION CONFIRMATION

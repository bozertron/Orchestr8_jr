# VISION REPORT: combat_tracker.py

**File:** IP/combat_tracker.py  
**Lines:** 115  
**Tokens:** 782  
**Survey Date:** 2026-02-12  

---

## Purpose

Tracks active LLM General deployments (COMBAT status). When an agent is deployed to fix broken code, that file enters "combat" state and is displayed as PURPLE in the Code City.

## Vision Alignment

### ∅明nos Vision Fit

**PERFECT** - This is the "combat" metaphor made real. Files with active agents become PURPLE buildings in the Code City. The Founder can see at a glance where work is happening.

### Current Status: WORKING (with integration gap)

| Aspect | Status | Notes |
|--------|--------|-------|
| Deploy/withdraw | ✅ Working | Tracks when agents start/stop |
| Combat status check | ✅ Working | is_in_combat() for Code City colors |
| Stale cleanup | ✅ Implemented | cleanup_stale_deployments() exists |
| **Startup cleanup** | ❌ **MISSING** | Not called at app initialization |
| State persistence | ✅ Working | JSON file in .orchestr8/ |

## Critical Finding

**Line 60-75: cleanup_stale_deployments() exists but is NEVER called at startup**

This directly impacts **Requirement CMBT-01**.

The method is fully implemented:
```python
def cleanup_stale_deployments(self, max_age_hours: int = 24) -> None:
    """Remove deployments older than max_age_hours."""
    state = self._load_state()
    now = datetime.now().isoformat()
    # ... cleanup logic ...
```

But 06_maestro.py never calls it during initialization.

## To Make It "Done"

1. **Add call in 06_maestro.py render()** at startup:
   ```python
   combat_tracker = CombatTracker(project_root_path)
   combat_tracker.cleanup_stale_deployments()  # <- ADD THIS
   ```

## Decision Required

**Question:** What constitutes "stale"?
- **Option A:** 24 hours (current default)
- **Option B:** 12 hours (more aggressive)
- **Option C:** Only on explicit user action (manual cleanup)

**Default recommendation:** Option A - 24 hours is reasonable for long-running tasks.

**Your decision:** _______________

---

**Status:** AWAITING VISION CONFIRMATION

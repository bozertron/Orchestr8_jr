# Orchestr8 Wiring Plan

**Created:** 2026-01-30
**Status:** PENDING APPROVAL

---

## Executive Summary

This document outlines the fixes needed to wire up the existing components in 06_maestro.py. The components EXIST - they just need to be connected properly.

---

## Priority 0: Brand Replacement (APPROVED)

Replace all "stereOS" references with "orchestr8" in the codebase.

### Files to Update

| File | Lines | Change |
|------|-------|--------|
| `IP/plugins/06_maestro.py` | 7, 873-876 | Brand text "stereOS" -> "orchestr8" |
| `IP/plugins/06_maestro.py` | 189-200 | CSS classes `.stereos-*` -> `.orchestr8-*` |
| `IP/plugins/06_maestro.py` | 5, 11, 31 | Docstring references |

**Estimated effort:** 30 minutes

---

## Priority 1: Top Row Button Fixes

### Issue 1.1: JFDI Button Opens Wrong Panel

**Current:** Opens placeholder "coming soon" panel (Lines 1059-1079)
**Expected:** Opens the fully-built `TicketPanel` component

**Fix:**

```python
# In build_panels(), replace JFDI placeholder with:
if get_show_tasks():
    # Use the actual TicketPanel, not placeholder
    ticket_panel.set_visible(True)
    return ticket_panel.render()
```

**Or simpler:** Wire `toggle_jfdi()` to `toggle_tickets()` since they're the same thing.

### Issue 1.2: Gener8 Button Does Nothing

**Current:** Only logs "Switch to Generator tab" (Line 893)
**Expected:** Should open Settings (per user decision)

**Fix:** Change to navigate to settings or open settings panel.

### Issue 1.3: Waves Button (~~~) Should Be Removed

**Current:** Line 1200-1202 shows `~~~` for settings
**Expected:** Remove waves, use `gener8` in top row for settings

**Estimated effort:** 1 hour

---

## Priority 2: Health Checker Integration

### Issue 2.1: HealthChecker Never Instantiated

**Current:** Imported but never used (Line 77)
**Expected:** Run health checks and update node colors

**Fix:**

```python
# In render(), add:
health_checker = HealthChecker(project_root_path)

# Add periodic health check or on-demand:
def refresh_health():
    fiefdoms = get_registered_fiefdoms()  # From some state
    for f in fiefdoms:
        result = health_checker.check_fiefdom(f)
        # Update fiefdom status in state
```

### Issue 2.2: Mermaid Generator Unused

**Current:** Imported but Woven Maps replaced it entirely
**Expected:** Either use it as fallback or remove import

**Recommendation:** Keep as fallback for simpler visualization mode.

**Estimated effort:** 2-3 hours

---

## Priority 3: Briefing Generator Stub

### Issue 3.1: `load_campaign_log()` Returns Empty

**Location:** `IP/briefing_generator.py` Lines 18-21
**Current:** Has `# ... parsing logic ...` comment, returns empty list
**Expected:** Actually parse CAMPAIGN_LOG.md

**Fix:** Implement the markdown parser:

```python
def load_campaign_log(self, fiefdom_path: str, limit: int = 5) -> List[Dict]:
    log_path = self.project_root / fiefdom_path / "CAMPAIGN_LOG.md"
    if not log_path.exists():
        return []

    content = log_path.read_text()
    entries = []

    # Parse ## [YYYY-MM-DD HH:MM] TICKET-XXX sections
    import re
    pattern = r'## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (TICKET-\d+)'
    # ... actual parsing logic

    return entries[-limit:]
```

**Estimated effort:** 1-2 hours

---

## Priority 4: State Synchronization

### Issue 4.1: Tickets/Combat/Briefings Not Linked

**Current:** Three separate systems for the same mission
**Expected:** Creating ticket should be linked to combat deployment

**Fix:** Create a `MissionManager` that coordinates:

```python
class MissionManager:
    def __init__(self, project_root):
        self.ticket_manager = TicketManager(project_root)
        self.combat_tracker = CombatTracker(project_root)
        self.briefing_generator = BriefingGenerator(project_root)

    def start_mission(self, fiefdom: str, ticket_id: str):
        """Start mission: create briefing, mark combat, link ticket"""
        pass

    def complete_mission(self, fiefdom: str, success: bool):
        """Complete: update ticket, clear combat, log to campaign"""
        pass
```

**Estimated effort:** 3-4 hours

---

## Priority 5: Panel Placeholder Replacement

### Issue 5.1: Collabor8 Panel is Placeholder

**Location:** Lines 1037-1057
**Current:** Static "coming soon" HTML
**Expected:** Actual agent management UI

**Fix options:**

1. Wire to existing agent definitions from `Agent Deployment Strategy/`
2. Create simple agent picker dropdown
3. Integrate with get-shit-done patterns

### Issue 5.2: Summon Panel is Placeholder

**Location:** Lines 1081-1095
**Current:** Static HTML mentioning Carl
**Expected:** Actual search with Carl integration

**Fix:** Wire to `CarlContextualizer`:

```python
if get_show_summon():
    from IP.carl_core import CarlContextualizer
    carl = CarlContextualizer(project_root_path)
    # Build search UI with carl.search() integration
```

**Estimated effort:** 4-6 hours total

---

## Priority 6: Background Process Fixes

### Issue 6.1: Director Monitor Thread Disconnect

**Location:** `08_director.py` Lines 239-247
**Current:** Background thread updates don't trigger UI refresh
**Expected:** UI should react to background changes

**Fix options:**

1. Use polling with Marimo's reactive state
2. Use file-based signaling (.orchestr8/state.json)
3. Accept manual refresh requirement (MVP approach)

### Issue 6.2: Combat State Cleanup

**Location:** `IP/combat_tracker.py` Lines 60-75
**Current:** `cleanup_stale_deployments()` must be called manually
**Expected:** Auto-cleanup on app start

**Fix:** Call cleanup in render() initialization:

```python
# In render(), add at start:
combat_tracker.cleanup_stale_deployments()
```

**Estimated effort:** 1-2 hours

---

## Priority 7: Platform Hardcoding

### Issue 7.1: Hardcoded gnome-terminal

**Location:** `IP/terminal_spawner.py` Line 73-87
**Current:** Tries gnome-terminal first
**Fix:** Already has fallback chain, just document

### Issue 7.2: Hardcoded npm run typecheck

**Location:** `IP/health_checker.py`, `IP/briefing_generator.py`
**Current:** Assumes TypeScript project
**Fix:** Already supports Python, just need proper detection

**Estimated effort:** 30 minutes (documentation only)

---

## Priority 8: Path Resolution

### Issue 8.1: sys.path Manipulation

**Location:** Multiple plugins
**Current:** Using `sys.path.insert()` to resolve imports
**Fix:** This is actually handled correctly now with project root detection

### Issue 8.2: Alias Resolution (@/ mapping)

**Location:** `IP/connection_verifier.py` Lines 356-359
**Current:** Assumes @/ -> src/
**Fix:** Make configurable via orchestr8_settings.toml

**Estimated effort:** 1 hour

---

## Implementation Order

| Phase | Priority | Tasks | Effort |
|-------|----------|-------|--------|
| A | P0 | Brand replacement (stereOS -> orchestr8) | 30 min |
| B | P1 | Top row button fixes | 1 hr |
| C | P2 | HealthChecker instantiation | 2 hrs |
| D | P3 | Briefing stub fix | 1-2 hrs |
| E | P6 | Combat cleanup on init | 30 min |
| F | P4 | State synchronization (if needed) | 3-4 hrs |
| G | P5 | Panel replacement (optional) | 4-6 hrs |

**MVP Total:** Phases A-E = ~5-6 hours
**Full Implementation:** All phases = ~12-15 hours

---

## Validation Checklist

After wiring, verify:

- [ ] Brand shows "orchestr8" not "stereOS"
- [ ] CSS classes are `.orchestr8-*`
- [ ] Top row: [orchestr8] [collabor8] [JFDI] [gener8]
- [ ] JFDI button opens TicketPanel
- [ ] gener8 button opens Settings
- [ ] Code City renders with three colors
- [ ] HealthChecker is instantiated
- [ ] Combat state cleans up on start
- [ ] Briefing generator loads campaign history

---

## Dependencies

- No external dependencies needed
- All required components already exist
- Just need wiring and minor fixes

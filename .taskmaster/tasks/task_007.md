# Task ID: 7

**Title:** Extend orchestr8.py root state with health channels

**Status:** done

**Dependencies:** 5 ✓

**Priority:** high

**Description:** Add health and health_status to STATE_MANAGERS while preserving existing state

**Details:**

Modify orchestr8.py state_management cell to add health state channels without breaking existing plugins.

Implementation:
In the state_management() function (around line 41), add:
```python
@app.cell
def state_management(mo, os):
    """Global state using Marimo's reactive state hooks.
    
    STATE_MANAGERS Pattern:
        Each state is a tuple of (getter, setter) functions.
        Plugins receive STATE_MANAGERS dict and can read/write state reactively.
    """
    # Core state definitions
    get_root, set_root = mo.state(os.getcwd())
    get_files, set_files = mo.state(None)
    get_selected, set_selected = mo.state(None)
    get_logs, set_logs = mo.state([])
    
    # Health state channels (Code City integration)
    get_health, set_health = mo.state({})
    get_health_status, set_health_status = mo.state("idle")
    
    # Bundle state for plugin injection
    STATE_MANAGERS = {
        "root": (get_root, set_root),
        "files": (get_files, set_files),
        "selected": (get_selected, set_selected),
        "logs": (get_logs, set_logs),
        "health": (get_health, set_health),
        "health_status": (get_health_status, set_health_status)
    }
    
    return (
        STATE_MANAGERS,
        get_files,
        get_logs,
        get_root,
        get_selected,
        get_health,
        get_health_status,
        set_files,
        set_logs,
        set_root,
        set_selected,
        set_health,
        set_health_status,
    )
```

Key constraints:
- Keep all existing keys unchanged
- Add health/health_status as NEW keys
- Maintain backwards compatibility

**Test Strategy:**

Run marimo run orchestr8.py and verify: (1) App starts without errors, (2) All existing plugins render correctly, (3) STATE_MANAGERS contains 6 keys including 'health' and 'health_status', (4) No console errors in browser

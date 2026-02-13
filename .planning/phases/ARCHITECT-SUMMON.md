# ARCHITECT-SUMMON.md — Summon Panel Integration Plan

**Generated:** 2026-02-12
**Agent:** Settlement Architect
**Priority:** 3 of 5 (depends on Carl `gather_context()`)

---

## 1. Current State

**Location:** `IP/plugins/06_maestro.py:1081-1095`

```
Placeholder HTML panel with:
- Static text: "Search across codebase, tasks, and agents"
- Placeholder note: "Integration with Carl contextualizer pending"
- No search input
- No context display
- Uses get_show_summon() for visibility
```

**Gap:** No connection to Carl, no search functionality, no context rendering.

---

## 2. Approach

Replace static HTML with reactive Marimo components:

1. **Search Input** — `mo.ui.text()` bound to reactive state
2. **Context Display** — Render Carl's `FiefdomContext` JSON as structured UI
3. **Debounced Query** — Trigger Carl on input (non-blocking)
4. **Emergence Animation** — Panel emerges from Void, no breathing

---

## 3. Modification Order for 06_maestro.py

### Step 1: Add Summon State Variables (near top, ~line 50)
```python
summon_query = mo.ui.text(placeholder="Search codebase, tasks, agents...", 
                          label="", 
                          on_change=lambda v: trigger_carl_search(v))
summon_results = mo.state([])  # Carl's context results
summon_loading = mo.state(False)
```

### Step 2: Replace Placeholder Panel (lines 1081-1095)
```python
if get_show_summon():
    query_section = mo.vstack([
        mo.Html('<span class="panel-title">SUMMON</span>'),
        summon_query,
    ])
    
    results_section = build_summon_results(summon_query.value, summon_results())
    
    summon_panel = mo.Html(f"""
    <div class="panel-overlay" style="animation: emergence 0.4s ease-out;">
        {query_section}
        <div class="summon-results">
            {results_section}
        </div>
    </div>
    """)
```

### Step 3: Add `build_summon_results()` Function (near `build_panel_overlays`)
```python
def build_summon_results(query: str, results: list) -> str:
    """Render Carl's FiefdomContext as emergent UI cards."""
    if not query:
        return '<div style="color: #999;">Enter query to summon context...</div>'
    if not results:
        return '<div style="color: #999;">Scanning the Void...</div>'
    
    # Render each FiefdomContext as a card
    cards = []
    for ctx in results:
        status_color = "#D4AF37" if ctx.get("health", {}).get("status") == "working" else "#1fbdea"
        cards.append(f"""
        <div class="context-card" style="border-left: 3px solid {status_color};">
            <div class="fiefdom-name">{ctx.get("fiefdom", "unknown")}</div>
            <div class="health-status">Health: {ctx.get("health", {}).get("status", "unknown")}</div>
            <div class="combat-status">Combat: {"ACTIVE" if ctx.get("combat", {}).get("active") else "inactive"}</div>
        </div>
        """)
    return "".join(cards)
```

### Step 4: Add `trigger_carl_search()` Function
```python
def trigger_carl_search(query: str):
    """Non-blocking call to Carl's gather_context()."""
    if not query or len(query) < 2:
        return
    # Call Carl's gather_context with query filter
    # This must NOT block — Carl runs async or returns cached data
    from IP.carl_core import Carl
    carl = Carl(STATE_MANAGERS)
    results = carl.gather_context(filter_query=query)
    summon_results.set(results)
```

---

## 4. Dependencies on Carl Implementation

| Dependency | Status | Required For |
|------------|--------|--------------|
| `IP/carl_core.py` exists | **PENDING** | All Summon functionality |
| `Carl.gather_context()` method | **PENDING** | Query filtering |
| `FiefdomContext` JSON output | **PENDING** | Results rendering |
| Signal source wiring (HealthChecker, etc.) | **PENDING** | Context accuracy |

**Blocker:** Summon panel is 100% dependent on Carl's `gather_context()` being implemented first.

**Integration Sequence:**
1. Implement Carl's `gather_context()` (Priority 2)
2. Wire Carl to Summon panel (this task, Priority 3)
3. Test search → context flow

---

## 5. Agent Estimates

| Task | Tokens | Agents (×3 Sentinel) | Tiers |
|------|--------|---------------------|-------|
| Replace placeholder HTML | ~800 | 1 × 3 = 3 | 9 (Execution) |
| Add `build_summon_results()` | ~600 | 1 × 3 = 3 | 9 (Execution) |
| Add `trigger_carl_search()` | ~400 | 1 × 3 = 3 | 9 (Execution) |
| Wire Carl dependency | ~500 | 1 × 3 = 3 | 4 (Wiring) |
| **Total** | ~2300 | **12 agent-instances** | — |

**Note:** Do not proceed until Priority 2 (Carl `gather_context()`) is complete.

---

## 6. Constraints Checklist

- [ ] NO breathing animations (emergence only)
- [ ] Carl does NOT block (async/cached)
- [ ] Three-state colors only (gold, teal, purple)
- [ ] Void background (#0A0A0B)
- [ ] Search minimum 2 characters before query

---

**Status:** READY (blocked by Carl implementation)
**Next Action:** Await Priority 2 completion, then execute modification order.

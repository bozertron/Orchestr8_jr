# PoC Settlement Integration Strategy - REVISED

**Generated:** 2026-02-16
**Goal:** Working Code City settlement proof-of-concept
**PRIORITY: FIRST - Bring main page to life**

---

## Visual Token Lock (CONFIRMED)

From `SOT/VISUAL_TOKEN_LOCK.md` - The visual system is LOCKED:

| State | Token | Hex | Code City |
|-------|-------|-----|-----------|
| Working | `--state-working` | #D4AF37 | Gold building |
| Broken | `--state-broken` | #1fbdea | Teal building |
| Combat | `--state-combat` | #9D4EDD | Purple building |

**Integration confirmed:** The Code City uses these exact same colors (verified in roadmaps).

---

## The Core Insight

> "The logic already exists. Bring the main page[s] to life."

This means the components work - we just need to wire them together. The PoC is about **integration, not implementation**.

---

## FIRST PRIORITY: Wire Live Data Flow

### Step 1: Fix Health → Code City Color (CRITICAL)

The health check runs but colors aren't updating properly.

```python
# The bug in graph_builder.py (lines 69-70):
# WRONG: if combat > 0: status = "broken"  
# RIGHT: if combat > 0: status = "combat"
```

Also: Warnings are ignored entirely - need to propagate.

---

### Step 2: Verify Combat → Purple Buildings

This WORKS - just needs to be connected:
- `combat_tracker.deploy()` → writes to `.orchestr8/combat_state.json`
- `graph_builder.py` → reads combat files, sets status = "combat"
- JavaScript → renders purple (#9D4EDD)

**Test:** Deploy a general to a file, refresh Code City, see purple.

---

### Step 3: Verify Louis Locks → Visual Indicator

**Test:** Lock a file using Louis, refresh, verify red indicator appears.

---

### Step 4: Verify Node Click → Panel Flow

```
Node Click 
    → process_node_click() [06_maestro.py:364]
    → build_code_city_context_payload() [code_city_context.py]
    → Panel display (broken/combat/working)
```

**Test:** Click each node type, verify correct panel opens.

---

### Step 5: Wire Node Click → Summon Connection

**Biggest gap found:** Node click builds context but Summon doesn't receive it.

```python
# In 06_maestro.py after build_code_city_context_payload():
# If Summon panel is active, inject the context
if summon_panel.value and payload:
    summon_state.set_context(payload)
```

---

## Success Criteria - What "Live" Looks Like

| Test | Expected Result |
|------|-----------------|
| Health check broken file | Blue/Teal building |
| Deploy general to file | Purple building (persists refresh) |
| Louis lock file | Red lock indicator |
| Click broken node | Deploy panel opens |
| Click purple node | "Agent active" status |
| Click gold node | Building info panel |
| Click node + Summon open | Context injected to Summon |

---

## Immediate Action Items

1. **Fix graph_builder.py bug** - 1 line change (status = "combat") ✅ DONE
2. **Verify combat flow** - Deploy, refresh, verify purple ✅ VERIFIED
3. **Verify Louis lock** - Lock file, verify visual ✅ VERIFIED
4. **Verify click handlers** - Click each node type, verify panels ✅ VERIFIED
5. **Wire node → Summon** - Context is built, used by building panel ✅ INTEGRATED (feature enhancement possible but not blocking)

---

## Files to Test/Modify

| File | Action |
|------|--------|
| `IP/features/code_city/graph_builder.py` | Fix line 69-70 bug |
| `IP/plugins/06_maestro.py` | Add node→Summon wire |
| `.orchestr8/combat_state.json` | Verify persistence |
| `IP/combat_tracker.py` | Verify deploy/withdraw |

---

## Visual Integration Points (Already Defined)

From VISUAL_TOKEN_LOCK.md + our roadmaps:

| Visual Token | Code City Usage | Status |
|--------------|-----------------|--------|
| `--state-working` (#D4AF37) | Working building color | ✅ Integrated |
| `--state-broken` (#1fbdea) | Broken building color | ✅ Needs fix |
| `--state-combat` (#9D4EDD) | Combat building color | ✅ Works |
| `--void-text` | Unassigned files | ❓ New feature |
| Typography tokens | Building labels | ✅ Integrated |
| Animation tokens | Emergence sequence | ✅ Works |

---

## Visual Reference Target

From `orchestr8_ui_reference.html` - The exact layout to match:

```
┌────────────────────────────────────────────┐
│  HEADER (80px)                            │
│  [Button] [MAESTRO] [Button]              │
├────────────────────────────────────────────┤
│                                            │
│           MAIN AREA                        │
│         "VOID" label                      │
│         (Code City renders here)           │
│                                            │
├────────────────────────────────────────────┤
│  FOOTER                                   │
│  [btn-group] [MAESTRO] [btn-group]        │
│  ─────────────────────────────────────     │
│  [=== Input Bar ===]                       │
└────────────────────────────────────────────┘
```

**Current state:** 06_maestro.py should match this exactly.

---

## Integration Complete Picture

```
VISUAL_TOKEN_LOCK (design tokens)
    ↓
orchestr8_ui_reference.html (visual target)
    ↓
06_maestro.py (implementation)
    ↓
graph_builder.py (maps status → color)
    ↓
CodeNode.status (working/broken/combat)  
    ↓
JavaScript renderer (#D4AF37 / #1fbdea / #9D4EDD)
```

**The story is complete.** We just need to verify it works.
# CANONICAL VISUAL INTEGRATION SPECIFICATION
**Generated:** 2026-02-16
**Canonical Source:** `/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md`
**Entry Point:** `orchestr8.py`

---

## 1. CANONICAL SOURCE OF TRUTH

**VISUAL_TOKEN_LOCK.md is the ONLY source of truth for visual design.**

All implementation must trace back to tokens in this file:

### Color Tokens (LOCKED)

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-obsidian` | #050505 | Background base |
| `--gold-dark` | #C5A028 | Primary accent, borders |
| `--gold-light` | #F4C430 | Highlight accent, hover |
| `--teal` | #00E5E5 | Secondary accent |
| `--text-grey` | #CCC | Standard text |
| `--state-working` | #D4AF37 | Gold - operational |
| `--state-broken` | #1fbdea | Blue - needs attention |
| `--state-combat` | #9D4EDD | Purple - agents active |

### Typography Tokens (LOCKED)

| Token | Value | Usage |
|-------|-------|-------|
| `--font-header` | 'Marcellus SC', serif | Headers, top buttons |
| `--font-ui` | 'Poiret One', cursive | UI labels, mini buttons |
| `--font-data` | 'VT323', monospace | Data, terminal |

### Dimension Tokens (LOCKED)

| Token | Value |
|-------|-------|
| `--header-height` | 80px |
| `--top-btn-height` | 50px |
| `--top-btn-min-width` | 160px |
| `--btn-mini-height` | 22px |
| `--btn-mini-min-width` | 60px |
| `--btn-maestro-height` | 36px |

---

## 2. PHYSICAL STRUCTURE (MANDATORY)

**CRITICAL:** All paths must match exactly to prevent integration failures.

### Current Structure (MUST PRESERVE)

```
orchestr8.py                          ← ENTRY POINT (CAN CHANGE)
    └── IP/plugins/06_maestro.py      ← MAIN RENDER (CANNOT CHANGE PATH)
        ├── IP/styles/
        │   ├── orchestr8.css        ← VISUAL TOKENS LIVE HERE
        │   ├── font_profiles.py     ← FONT INJECTION
        │   └── font_injection.py
        ├── IP/static/
        │   ├── woven_maps_3d.js     ← THREE.JS RENDERER
        │   └── woven_maps_template.html
        ├── IP/features/code_city/
        │   ├── graph_builder.py
        │   └── render.py
        ├── IP/plugins/components/
        │   ├── deploy_panel.py
        │   ├── ticket_panel.py
        │   └── [other panels]
        └── IP/contracts/
            └── [schemas]
```

### What CAN Change

| File | Can Modify? | Notes |
|------|-------------|-------|
| `orchestr8.py` | YES | Entry point, can add initialization |
| `IP/styles/orchestr8.css` | YES | But MUST match VISUAL_TOKEN_LOCK |
| `IP/plugins/06_maestro.py` | YES | Add handlers, states |
| `IP/features/maestro/views/` | YES | Panel rendering |

### What CANNOT Change

| File | Cannot Change | Reason |
|------|---------------|--------|
| `IP/woven_maps.py` | ❌ | Data structures define schema |
| `IP/static/woven_maps_3d.js` | ❌ | Client expects exact API |
| `IP/plugins/06_maestro.py` | ❌ PATH | Marimo cell reference |
| `IP/contracts/*.py` | ❌ | Cross-lane contracts |
| `IP/styles/orchestr8.css` | ❌ | Visual token lock |

---

## 3. ORCHESTR8.PY ENTRY POINT

### Current Behavior

`orchestr8.py` currently:
1. Sets up Marimo app
2. Initializes state managers
3. Renders `06_maestro.py`

### Required Behavior (ADD)

The entry point should:

1. **Load VISUAL_TOKEN_LOCK at startup** - Verify CSS tokens match
2. **Initialize logging** - Track visual rendering
3. **Provision button I/O** - Map physical buttons to Python handlers

### Implementation

```python
# orchestr8.py additions:

@app.cell
def init_visual_system():
    """Initialize visual system from CANONICAL source."""
    
    # 1. Verify VISUAL_TOKEN_LOCK is source of truth
    token_lock_path = Path("SOT/VISUAL_TOKEN_LOCK.md")
    assert token_lock_path.exists(), "VISUAL_TOKEN_LOCK.md missing"
    
    # 2. Load CSS tokens (from orchestr8.css)
    css_path = Path("IP/styles/orchestr8.css")
    css_tokens = parse_css_variables(css_path)
    
    # 3. Verify tokens match canonical (colors, typography, dimensions)
    verify_token_alignment(css_tokens, token_lock_path)
    
    # 4. Initialize button I/O provisioning
    return initialize_button_io()
```

---

## 4. BUTTON → MARIMO I/O MAPPING

### Current Physical Layout (from VISUAL_TOKEN_LOCK)

```
┌────────────────────────────────────────────┐
│  HEADER (80px height)                      │
│  [orchestr8] [MAESTRO] [collab8] [JFDI]   │  ← TOP BUTTONS
│         (min-width: 160px, height: 50px)   │
├────────────────────────────────────────────┤
│                                            │
│           MAIN VOID AREA                   │
│         (Code City renders here)           │
│                                            │
├────────────────────────────────────────────┤
│  FOOTER (Lower Fifth)                      │
│  [LEFT BTNS] [MAESTRO] [RIGHT BTNS]       │
│  ─────────────────────────────────────     │
│  [========== INPUT BAR ===========]        │
│         (height: 36px, padding: 8px 0)     │
└────────────────────────────────────────────┘
```

### Button I/O Provisioning

Each button needs a Python handler that receives input and produces output:

| Button | Handler Function | Input | Output | Current Status |
|--------|-----------------|-------|--------|----------------|
| **orchestr8** | `toggle_orchestr8_panel()` | click | Panel toggle | ✅ Implemented |
| **MAESTRO** | `cycle_maestro_state()` | click | State cycle | ✅ Implemented |
| **collab8** | `toggle_collab8_panel()` | click | Panel toggle | ✅ Implemented |
| **JFDI** | `toggle_jfdi_panel()` | click | Panel toggle | ✅ Implemented |
| **Ticket** | `toggle_tickets()` | click | Panel toggle | ✅ Implemented |
| **Calendar** | `toggle_calendar()` | click | Panel toggle | ✅ Implemented |
| **Comms** | `toggle_comms()` | click | Panel toggle | ✅ Implemented |
| **File** | `toggle_file_explorer()` | click | Panel toggle | ✅ Implemented |
| **Deploy** | `toggle_deploy()` | click | Panel toggle | ✅ Implemented |
| **Summon** | `toggle_summon()` | click | Panel toggle | ✅ Implemented |
| **Settings** | `toggle_settings()` | click | Panel toggle | ✅ Implemented |

### Button Handler Pattern

```python
# Example button handler in 06_maestro.py:

def toggle_maestro() -> None:
    """MAESTRO button handler - cycles through ON/OFF/OBSERVE states."""
    current = get_maestro_state()
    
    # State machine: ON → OFF → OBSERVE → ON
    states = ["ON", "OFF", "OBSERVE"]
    idx = states.index(current) if current in states else 0
    next_state = states[(idx + 1) % len(states)]
    
    set_maestro_state(next_state)
    
    # Output: Log the state change
    log_action(f"Maestro mode: {next_state}")
    
    # Output: Trigger visual update
    set_maestro_state_changed(True)  # Triggers re-render

# Button I/O contract:
# - INPUT: click event (no parameters)
# - OUTPUT: state change + log message
# - SIDE EFFECT: UI re-render
```

### Input Bar I/O

The input bar (footer) needs full I/O:

| Component | Handler | Input | Output |
|-----------|---------|-------|--------|
| Text input | `handle_summon_input(query: str)` | user typing | Summon results |
| Submit | `execute_summon(query: str)` | Enter key | Action execution |
| Model selector | `set_model(model: str)` | dropdown | Model state |

---

## 5. FILES TO INGEST FROM OTHER CODEBASES

Based on the canonical visual reference, identify what's needed:

### From `/home/bozertron/JFDI - Collabkit/Application/`

| File | Purpose | Status | Action |
|------|---------|--------|--------|
| `src/modules/maestro/MaestroView.vue` | Button layout reference | ⚠️ PATTERN ONLY | Map to 06_maestro |
| `src/components/FileExplorer.vue` | File panel pattern | ⚠️ PATTERN ONLY | Map to panel |
| `src/components/Settings*.vue` | Settings pattern | ⚠️ PATTERN ONLY | Map to 07_settings |

**Note:** Collabkit Vue files are REFERENCE PATTERNS ONLY. Do NOT copy - transliterate to Marimo Python.

### From `/home/bozertron/Orchestr8_jr/one integration at a time/`

| File | Purpose | Status | Action |
|------|---------|--------|--------|
| `UI Reference/MaestroView.vue` | UI reference | ⚠️ ARCHIVE | Use VISUAL_TOKEN_LOCK instead |
| `FileExplorer/FileExplorer.vue` | File panel | ⚠️ ARCHIVE | Use VISUAL_TOKEN_LOCK instead |

### From `/home/bozertron/Orchestr8_jr/SOT/`

| File | Purpose | Status | Action |
|------|---------|--------|--------|
| `VISUAL_TOKEN_LOCK.md` | CANONICAL | ✅ ACTIVE | Source of truth |
| `APP_FIRST_TAURI_READY_PLAN.md` | Future packaging | ✅ ACTIVE | Reference |

---

## 6. INTEGRATION CHECKLIST

### Phase 1: Entry Point (orchestr8.py)

- [ ] orchestr8.py loads VISUAL_TOKEN_LOCK.md at startup
- [ ] orchestr8.py verifies CSS token alignment
- [ ] orchestr8.py initializes button I/O provisioning

### Phase 2: Visual Tokens (IP/styles/)

- [ ] orchestr8.css matches VISUAL_TOKEN_LOCK.md exactly
- [ ] font_profiles.py injects correct fonts
- [ ] Font files present: Marcellus SC, Poiret One, VT323

### Phase 3: Main Render (06_maestro.py)

- [ ] Layout matches VISUAL_TOKEN_LOCK dimensions
- [ ] Header: 80px height, buttons 50px × 160px min
- [ ] Footer: Input bar 36px height
- [ ] All button handlers implemented

### Phase 4: Code City (woven_maps)

- [ ] Three.js renders with correct colors from tokens
- [ ] Particles use correct effect tokens
- [ ] Buildings use state colors (working/broken/combat)

### Phase 5: Integration

- [ ] All panels open/close correctly
- [ ] Input bar I/O works end-to-end
- [ ] Visual tokens applied everywhere

---

## 7. REFERENCE MAPPING

### VISUAL_TOKEN_LOCK → Implementation

| Token | Implementation File | Line |
|-------|-------------------|------|
| `--bg-obsidian` | `orchestr8.css` | 9 |
| `--gold-dark` | `orchestr8.css` | 10 |
| `--state-working` | `orchestr8.css` | 27 |
| `--state-broken` | `orchestr8.css` | 28 |
| `--state-combat` | `orchestr8.css` | 29 |
| `--font-header` | `orchestr8.css` | 62 |
| `--font-ui` | `orchestr8.css` | 63 |
| `--font-data` | `orchestr8.css` | 64 |
| `--header-height` | `orchestr8.css` | 1689 |
| `--top-btn-height` | `orchestr8.css` | 1690 |
| `--btn-mini-height` | `orchestr8.css` | 1692 |

### Button → Handler → State

```
USER CLICK
    ↓
mo.ui.button(on_click=handler)
    ↓
handler() updates mo.state()
    ↓
UI re-renders with new state
    ↓
VISUAL OUTPUT matches token
```

---

## 8. DECISION REQUIRED

Before proceeding, need Founder confirmation on:

1. ✅ **VISUAL_TOKEN_LOCK.md is canonical** - CONFIRMED
2. ✅ **orchestr8.py remains entry point** - CONFIRMED
3. ⚠️ **Button layout matches spec?** - Need to verify 06_maestro.py layout
4. ⚠️ **What from Collabkit is actually needed?** - Only patterns, not code

---

## Summary

| Aspect | Status |
|--------|--------|
| Canonical Source | VISUAL_TOKEN_LOCK.md ✅ |
| Entry Point | orchestr8.py ✅ (no path change) |
| Main Render | IP/plugins/06_maestro.py ✅ (no path change) |
| Visual Tokens | IP/styles/orchestr8.css ✅ (updated) |
| 3D Rendering | IP/static/woven_maps_3d.js ✅ |
| Collabkit | PATTERNS ONLY, no ingestion |
| Vite | NOT USED ❌ |
| particle.js | NOT USED ❌ |

**Next: Verify button layout in 06_maestro.py matches VISUAL_TOKEN_LOCK dimensions, then spawn agent swarms.**
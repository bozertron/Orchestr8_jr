# UI Pressure Test Report: 06_maestro.py

**Date:** 2026-01-26
**Tester:** Claude Code
**Reference:** `style/MAESTROVIEW_REFERENCE.md` (authoritative)
**Subject:** `IP/plugins/06_maestro.py` (The Void plugin)

---

## Executive Summary

The `06_maestro.py` plugin has a solid foundation but requires updates to align with the authoritative MaestroView.vue style guide. The plugin is **functional** but **incomplete** for production use.

| Category | Status | Priority |
|----------|--------|----------|
| Color System | 6/7 colors present | HIGH (missing Combat purple) |
| Typography | Matches guide | OK |
| Layout Structure | Correct pattern | OK |
| Control Surface | Missing 5 buttons | MEDIUM |
| Graph Integration | Not implemented | CRITICAL |
| Terminal (actu8) | Not integrated | HIGH |
| Z-Index Hierarchy | Not implemented | MEDIUM |

---

## 1. COLOR SYSTEM

### Present (Correct)
| Variable | Hex | Status |
|----------|-----|--------|
| `BLUE_DOMINANT` | `#1fbdea` | ✓ |
| `GOLD_METALLIC` | `#D4AF37` | ✓ |
| `GOLD_DARK` | `#B8860B` | ✓ |
| `GOLD_SAFFRON` | `#F4C430` | ✓ |
| `BG_PRIMARY` | `#0A0A0B` | ✓ |
| `BG_ELEVATED` | `#121214` | ✓ |

### Missing (CRITICAL)
| Variable | Hex | Purpose |
|----------|-----|---------|
| `PURPLE_COMBAT` | `#9D4EDD` | **Combat state indicator** - General deployed and active |

**Fix Required:**
```python
# Add after line 43
PURPLE_COMBAT = "#9D4EDD"
```

---

## 2. CONTROL SURFACE BUTTONS

### Current vs Required

**Left Group:**
| Style Guide | Current | Status |
|-------------|---------|--------|
| Apps | Apps | ✓ |
| Matrix | Matrix | ✓ |
| Calendar | - | ✗ Missing |
| Comms | - | ✗ Missing |
| Files | Files | ✓ |

**Right Group:**
| Style Guide | Current | Status |
|-------------|---------|--------|
| Search | Search | ✓ |
| Record | - | ✗ Missing |
| Playback | - | ✗ Missing |
| Phreak> | Terminal | ✗ Wrong label |
| Send | Send | ✓ |
| Attach | Attach | ✓ |

**Fix Required:** Rename "Terminal" to "Phreak>" and add missing buttons.

---

## 3. MERMAID GRAPH INTEGRATION

### Current State
The Void currently displays:
- Chat messages (LLM responses)
- Placeholder text when empty

### Required State (per ROADMAP_ORCHESTR8_V4.md)
The Void should display:
1. **Connection Graph** - Mermaid/PyVis visualization of codebase topology
2. **Status Overlays** - Three-color node states (Gold/Blue/Purple)
3. **Agent Markers** - Show which generals are deployed where
4. **Fiefdom Boundaries** - Visual grouping of assigned directories

### Priority: CRITICAL
This is the core differentiator for Orchestr8 v4.0.

---

## 4. TERMINAL (actu8) INTEGRATION

### Current State
- Button labeled "Terminal"
- Toggles `show_terminal` state
- No actual terminal component

### Required State
- Button labeled "Phreak>"
- Opens `actu8` terminal component
- Must import from stereOS/Orchestr8_sr

### Missing Implementation
```python
# In imports section
from nexus_terminal import Actu8Terminal  # Placeholder - verify actual import path

# In control surface
mo.ui.button(
    label="Phreak>",
    on_change=lambda _: toggle_terminal_actu8()
)
```

---

## 5. Z-INDEX HIERARCHY

### Style Guide Requirements
| Layer | z-index | Current Status |
|-------|---------|----------------|
| Settings Portal | 100 | Not implemented |
| Top Row | 50 | Not implemented |
| Agent Chat | 50 | Not implemented |
| Tasks Panel | 45 | Not implemented |
| Agents Panel | 40 | Not implemented |
| Bottom Fifth | 20 | Not implemented |

### Fix Required
Add z-index declarations to CSS:
```css
.maestro-top-row {
    z-index: 50;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
}

.control-surface {
    z-index: 20;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
}

.panel-overlay.agents {
    z-index: 40;
}

.panel-overlay.tasks {
    z-index: 45;
}
```

---

## 6. FUNCTIONAL TEST RESULTS

```
=== PLUGIN LOAD TEST ===
✓ All 7 plugins load successfully
✓ render() function present on all plugins
✓ STATE_MANAGERS pattern correctly implemented

=== RENDER TEST ===
✓ 06_maestro.py render() executes without errors
✓ Returns valid Marimo vstack element
```

---

## 7. PRIORITY FIX LIST

### P0 - Critical (Must Have)
1. Add `PURPLE_COMBAT = "#9D4EDD"` constant
2. Implement Mermaid/PyVis graph in The Void
3. Wire up fiefdom status display

### P1 - High (Should Have)
4. Rename "Terminal" → "Phreak>"
5. Integrate actu8 terminal component
6. Add z-index hierarchy to CSS

### P2 - Medium (Nice to Have)
7. Add missing buttons (Calendar, Comms, Record, Playback)
8. Implement fixed positioning for Top Row and Bottom Fifth
9. Add keyboard shortcuts (Cmd/Ctrl+T, Cmd/Ctrl+A, etc.)

---

## 8. ARCHITECTURE NOTES

### What's Working Well
- Plugin architecture with `STATE_MANAGERS` injection
- CSS styling approach with f-string interpolation
- Event handler pattern (toggle_collabor8, toggle_jfdi, etc.)
- Message emergence pattern

### What Needs Rework
- The Void center should default to **graph view**, not chat
- Chat should be a **secondary mode** or overlay
- Panel emergence needs proper z-index stacking

---

## Conclusion

The foundation is solid. The main gaps are:
1. **Missing Combat color** (quick fix)
2. **No graph visualization** (significant work)
3. **No actu8 integration** (requires stereOS import)

The plugin is **functional for development** but not ready for the "experience engine" role until the graph visualization is implemented.

---

*Report generated during pressure testing session 2026-01-26*

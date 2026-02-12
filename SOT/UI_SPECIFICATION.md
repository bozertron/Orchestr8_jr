# Orchestr8 UI Specification (Source of Truth)

**Version:** 1.0
**Date:** 2026-01-30
**Status:** APPROVED

---

## I. Brand Identity

- **Application Name:** orchestr8 (lowercase, ends with 8)
- **Naming Convention:** Words ending with 8 start lowercase (orchestr8, collabor8, gener8)
- **Legacy Reference:** MaestroView.vue from stereOS is a UI REFERENCE only

---

## II. Color System (EXACT - NO EXCEPTIONS)

```css
:root {
    /* State Colors */
    --gold-metallic: #D4AF37;    /* Working state */
    --gold-dark: #B8860B;        /* Gold accent/stroke */
    --gold-saffron: #F4C430;     /* Gold highlight */
    --blue-dominant: #1fbdea;    /* Broken state, UI default */
    --purple-combat: #9D4EDD;    /* Combat state - General deployed */

    /* Background */
    --bg-primary: #0A0A0B;       /* The Void */
    --bg-elevated: #121214;      /* Surface/cards */

    /* Typography */
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;
}
```

### Three-State System

| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| Working | Gold | #D4AF37 | All imports resolve, typecheck passes |
| Broken | Blue | #1fbdea | Has errors, needs attention |
| Combat | Purple | #9D4EDD | General currently deployed and active |

---

## III. Layout Structure

```
+-------------------------------------------------------------------------+
| TOP ROW (Fixed)                                                          |
| [orchestr8] [collabor8] [JFDI] [gener8]              [Model Picker]     |
+-------------------------------------------------------------------------+
|                                                                          |
|                           THE VOID                                       |
|                                                                          |
|  +----------------------------------+  +-----------------------------+   |
|  |     CODE CITY / MERMAID         |  |   SLIDE-OUT PANELS         |   |
|  |     (Woven Maps visualization)   |  |   (Emerge from RIGHT)      |   |
|  |                                  |  |   - Tickets (JFDI)         |   |
|  |     Gold = Working              |  |   - Calendar               |   |
|  |     Blue = Broken               |  |   - Comms                  |   |
|  |     Purple = Combat             |  |   - File Explorer          |   |
|  |                                  |  |                            |   |
|  +----------------------------------+  +-----------------------------+   |
|                                                                          |
+-------------------------------------------------------------------------+
| BOTTOM FIFTH - Control Surface (NEVER MOVES - The Overton Anchor)       |
| +---------------------------------------------------------------------+ |
| | [Attachments: file1.py, file2.ts]                                   | |
| | [Chat Input: "What would you like to accomplish?"                 ] | |
| | [Apps] [Matrix] [Calendar] [Comms] [Files] == [maestro] == [Search] | |
| | [Record] [Playback] [Phreak>] [Send] [Attach]                       | |
| +---------------------------------------------------------------------+ |
+-------------------------------------------------------------------------+
```

---

## IV. Top Row Buttons (DEFINITIVE)

| Button | Label | Function |
|--------|-------|----------|
| 1 | `orchestr8` | Home - Reset to default state, always present |
| 2 | `collabor8` | Agents dropdown - Domain agent management |
| 3 | `JFDI` | "Just Fucking Do It" - Opens Ticket panel (slides RIGHT) |
| 4 | `gener8` | Settings panel |

**Note:** The "waves" graphic is NOT part of the top row.

---

## V. Control Surface Buttons

### Left Group

| Button | Function |
|--------|----------|
| Apps | Opens Linux app store (gnome-software) |
| Matrix | Opens code editor + shows Collabor8 panel |
| Calendar | Toggles Calendar slide-out panel |
| Comms | Toggles P2P Communications panel |
| Files | Toggles inline File Explorer panel |

### Center

| Button | Function |
|--------|----------|
| maestro | Global search (summon) |

### Right Group

| Button | Function |
|--------|----------|
| Search | Same as maestro - global search |
| Record | Toggle audio recording |
| Playback | Play recorded audio |
| Phreak> | Spawn terminal at current fiefdom |
| Send | Send chat message to void |
| Attach | Attach selected file to conversation |

---

## VI. Panel Behavior

### Slide-Out Panels (from RIGHT)

- **Mutually exclusive:** Only one can be open at a time
- **Trigger:** Button click
- **Animation:** Slide from right edge
- **Panels:**
  - Tickets (JFDI) - Full TicketPanel component
  - Calendar - CalendarPanel component
  - Comms - CommsPanel component
  - File Explorer - FileExplorerPanel component

### Modal Overlays (center)

- **Deploy Panel** - "House a Digital Native?" - triggered by clicking broken node
- **Summon Panel** - Global search overlay

### Top Panels (from TOP)

- **Collabor8** - Agent management dropdown
- Reserved for future use

---

## VII. Emergence Behavior

> "UI elements do not 'load'; they EMERGE when summoned."

### Animation Types

- `emergence` - Translate up + fade in (0.4s)
- `emergence-fade` - Fade in only (0.3s)
- `emergence-scale` - Scale up + fade in (0.5s)

### Rules

- NO breathing animations
- Messages EMERGE from the void
- Input bar NEVER moves (anchored to bottom)
- Staggered delays for multiple elements

---

## VIII. CSS Class Naming

Update from `.stereos-*` to `.orchestr8-*`:

```css
/* OLD */
.stereos-brand { }
.stereos-prefix { }
.stereos-suffix { }

/* NEW */
.orchestr8-brand { }
.orchestr8-prefix { }
.orchestr8-suffix { }
```

---

## IX. Style Reference

The canonical CSS file is: `IP/styles/orchestr8.css`

This file defines all colors, typography, and component styles. Any new components should use these variables.

---

## X. References

- **UI Layout Reference:** `one integration at a time/UI Reference/MaestroView.vue`
- **Style Reference:** `IP/styles/orchestr8.css`
- **Implementation:** `IP/plugins/06_maestro.py`
- **Component Library:** `IP/plugins/components/`

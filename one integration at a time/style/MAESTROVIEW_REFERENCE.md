# MaestroView.vue - Authoritative Style Reference

**Source:** `/UI Reference/MaestroView.vue`  
**Version:** Extracted 2026-01-26  
**Purpose:** Single source of truth for all UI styling decisions

---

## I. COLOR SYSTEM (EXACT - NO EXCEPTIONS)

| Variable | Hex | Usage |
|----------|-----|-------|
| `--blue-dominant` | `#1fbdea` | UI default, borders, interactive elements |
| `--gold-metallic` | `#D4AF37` | UI highlight, active states, working status |
| `--gold-dark` | `#B8860B` | Maestro default, timestamp text, secondary gold |
| `--gold-saffron` | `#F4C430` | Maestro highlight, hover states |
| `--bg-primary` | `#0A0A0B` | The Void background |
| `--bg-elevated` | `#121214` | Surface, elevated panels, inputs |

### Three-State System (from Emperor's Decree + Roadmap v4.0)
| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| **Working** | Gold | `#D4AF37` | All imports resolve, typecheck passes |
| **Broken** | Blue | `#1fbdea` | Has errors, needs attention |
| **Combat** | Purple | `#9D4EDD` | General currently deployed and active |

### Additional Color Variable
| Variable | Hex | Usage |
|----------|-----|-------|
| `--purple-combat` | `#9D4EDD` | Combat status indicator |

---

## II. TYPOGRAPHY

```css
--font-headline: [System headline font]
--font-body: [System body font]  
--font-mono: [Monospace font]
```

### Font Sizes
- Top buttons: `10px`, letter-spacing `0.1em`
- Control buttons: `10px`, letter-spacing `0.08em`
- Body text: `14px`, line-height `1.6`
- Maestro center: `14px`, letter-spacing `0.1em`
- Timestamps: `10px` mono
- stereOS brand: `14px`, letter-spacing `0.08em`

---

## III. LAYOUT ARCHITECTURE

### The Void Structure
```
┌─────────────────────────────────────────────────────┐
│ TOP ROW (fixed, z-index: 50)                        │
│ [stereOS]        [Collabor8] [JFDI] [Gener8]        │
├─────────────────────────────────────────────────────┤
│                                                     │
│                                                     │
│              THE VOID CENTER                        │
│         (LLM responses emerge here)                 │
│                                                     │
│                                                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│ BOTTOM FIFTH (fixed, z-index: 20)                   │
│ [Chat Input - full width, max 900px]                │
│ [Control Surface - edge to edge]                    │
│ Left: Apps|Matrix|Calendar|Comms|Files              │
│ Center: [maestro]                                   │
│ Right: Search|Record|Playback|Phreak>|Send|Attach   │
└─────────────────────────────────────────────────────┘
```

### Key Layout Rules
1. **The Void** = `#0A0A0B` background, pure collaboration space
2. **Bottom Fifth** = "Overton anchor" - IT NEVER MOVES
3. **Top Row** = Fixed position, navigation only
4. **Panels** = Emerge via transitions (slide-down, slide-right, fade)

---

## IV. COMPONENT STYLING

### Buttons - Top Row
```css
.top-btn {
  padding: 5px 12px;
  border-radius: 4px;
  background: #121214;
  border: 1px solid rgba(31, 189, 234, 0.3);
  color: #1fbdea;
  font-size: 10px;
  letter-spacing: 0.1em;
  transition: all 200ms ease-out;
}

.top-btn:hover, .top-btn.active {
  background: rgba(212, 175, 55, 0.1);
  border-color: #D4AF37;
  color: #D4AF37;
}
```

### Buttons - Control Surface
```css
.ctrl-btn {
  padding: 6px 12px;
  background: transparent;
  border: none;
  color: #1fbdea;
  font-size: 10px;
  letter-spacing: 0.08em;
  transition: all 150ms ease-out;
}

.ctrl-btn:hover {
  color: #D4AF37;
}

.ctrl-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
```

### Chat Input
```css
.chat-input {
  width: 100%;
  padding: 12px 16px;
  background: #121214;
  border: 1px solid rgba(31, 189, 234, 0.3);
  border-radius: 6px;
  color: #e8e8e8;
  font-size: 14px;
  min-height: 44px;
  max-height: 120px;
}

.chat-input:focus {
  outline: none;
  border-color: #D4AF37;
}
```

### Emerged Messages (LLM Responses)
```css
.emerged-message {
  padding: 16px 20px;
  background: rgba(18, 18, 20, 0.9);
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}
```

### stereOS Brand
```css
.stereos-text {
  color: #D4AF37;  /* "OS" portion */
}
.stereos-prefix {
  color: #1fbdea;  /* "stere" portion */
}
```

---

## V. TRANSITIONS & ANIMATIONS

### Allowed Transitions
```css
/* Slide down (panels from top) */
transition: transform 300ms ease-out;

/* Slide right (panels from side) */
transition: transform 300ms ease-out;

/* Fade */
transition: opacity 200ms ease-out;

/* Emerge (LLM messages) */
transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
```

### Emerge Animation (Messages from Void)
```css
.emerge-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.emerge-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}
```

---

## VI. STRICT PROHIBITIONS

From MaestroView.vue header comment:

> **NO breathing animations. NO emojis. NO clock.**

Additional design rules:
- UI elements do not "load"; they **EMERGE from the void** when summoned
- The Input Bar is docked at the bottom 5th - **IT NEVER MOVES**
- No permanent UI elements in The Void center

---

## VII. BORDER PATTERNS

| Context | Border Style |
|---------|--------------|
| Default | `1px solid rgba(31, 189, 234, 0.3)` |
| Active/Focused | `border-color: #D4AF37` |
| Panels | `1px solid rgba(31, 189, 234, 0.2)` |
| Gold accent | `1px solid rgba(184, 134, 11, 0.3)` |
| Hover gold | `rgba(212, 175, 55, 0.4)` |

---

## VIII. Z-INDEX HIERARCHY

| Layer | z-index | Elements |
|-------|---------|----------|
| Top Row | 50 | Navigation bar |
| Agent Chat | 50 | Chat overlay |
| Tasks Panel | 45 | Task list overlay |
| Agents Panel | 40 | Agent selection |
| Bottom Fifth | 20 | Control surface |
| Settings Portal | 100 | Soundwave button |

---

## IX. COMPONENTS REFERENCED

MaestroView imports these components (for context):
- `DomainAgentBar.vue` - Agent selection bar
- `TasksPanel.vue` - JFDI task management
- `AgentChatPanel.vue` - Chat with agents
- `SummonResultCard.vue` - Search results
- `HollowDiamond.vue` - Decorative element
- `TaskFocusOverlay.vue` - Task detail view
- `FileExplorer.vue` - File picker
- `NexusTerminal.vue` - Terminal access

---

## X. KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + T` | Toggle Tasks (JFDI) |
| `Cmd/Ctrl + A` | Toggle Agents (Collabor8) |
| `Cmd/Ctrl + G` | Open Generator (Gener8) |
| `Cmd/Ctrl + ,` | Open Settings |
| `/` | Open Summon |
| `Escape` | Hierarchical dismissal |

---

## XI. TERMINAL INTEGRATION

**Terminal Name:** `actu8`

The terminal component for general deployment is called **actu8**. It must be imported from stereOS/Orchestr8_sr.

Referenced in MaestroView.vue as:
- `NexusTerminal.vue` - Terminal access component
- "Phreak>" button in control surface

---

**This document is the authoritative reference. When in doubt, consult MaestroView.vue directly.**

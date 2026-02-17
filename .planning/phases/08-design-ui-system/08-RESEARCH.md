# Phase 08: Real-Time Design UI System - Research

**Researched:** 2026-02-16
**Domain:** UI/UX Design System + Real-time Editing + Particle-based Visualization
**Confidence:** HIGH

## Summary

This research addresses the implementation of a real-time design UI system for Orchestr8 that combines the Collabkit Void Design System, EPO settings patterns, and particle-based UI components. The core vision is an "invisible UI" where components match the background color by default, with text-based interfaces as the primary interaction pattern.

**Primary recommendation:** Implement a text-first design system that uses the Void Design System's exact color tokens and emergence patterns, adapts the EPO settings UI patterns for Marimo, and preserves the Code City visualization contract.

## Standard Stack

### Core Technologies

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **Marimo** | Current (0.19.x+) | Reactive Python notebook/runtime | Per README.AGENTS, Marimo-first is locked |
| **Canvas API** | Native | Particle-based rendering | Used by woven_maps.py, Barradeau technique |
| **WebGL** | Native | 3D building visualization | 3D Code City implementation |
| **TOML** | Python stdlib | Settings persistence | EPO pattern, pyproject standard |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **Pydantic** | 2.x | Settings schema validation | For Tauri-ready config design |
| **toml** | Python stdlib | Config file I/O | Settings persistence |
| **watchdog** | Latest | File watching for real-time updates | Health checking, live reload |

### Color System (EXACT - NO EXCEPTIONS)

Source: VOID_DESIGN_SYSTEM_SOT.md + orchestr8.css

| Token | Value | Meaning | Usage |
|-------|-------|---------|-------|
| `--blue-dominant` | `#1fbdea` | UI Default / Broken state | Standard text, buttons, communication input |
| `--gold-metallic` | `#D4AF37` | UI Highlight / Working state | Active states, hover effects, key actions |
| `--gold-dark` | `#B8860B` | Maestro Default | Logo, Agent avatars, unselected tools |
| `--gold-saffron` | `#F4C430` | Maestro Highlight | Glow effects, active Agent state, high-priority alerts |
| `--purple-combat` | `#9D4EDD` | Combat state | LLM General deployed and active |
| `--bg-primary` | `#0A0A0B` | The Void | Infinite background (ground state) |
| `--bg-elevated` | `#121214` | Surface | Cards, heavy containers |

### Typography System

| Role | Font | Size | Weight | Letter Spacing |
|------|------|------|--------|----------------|
| Headers/Actions | Orchestr8 HardCompn (Futura) | 10-18px | 500-600 | 0.08-0.25em |
| Body/Content | Orchestr8 CalSans (Avenir) | 13-15px | 400 | Normal |
| Monospace/Meta | Orchestr8 Mini Pixel (SF Mono) | 10-12px | 400 | 0.1em |

## Architecture Patterns

### Pattern 1: Emergence-Only Navigation

**What:** UI elements do not load or breathe - they EMERGE when summoned. The default state is emptiness (The Void).

**When to use:** All primary UI components - panels, overlays, messages

**Implementation:**
- CSS keyframes: `emergence` (translateY + scale + opacity)
- Duration: 300-400ms, cubic-bezier(0.16, 1, 0.3, 1)
- NO breathing animations (explicitly disabled in Void Design System)

**Example from orchestr8.css:**
```css
@keyframes emergence {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
```

### Pattern 2: Text-First Interface

**What:** Minimal chrome. Typography and space are the primary interface elements.

**When to use:** Default for all new UI components

**Implementation:**
- No borders by default (use subtle borders: 1px solid rgba(31, 189, 234, 0.2))
- Text at 100% brightness (never below 70%)
- Use the diamond (◇) for dismiss actions, NEVER ✕

**Example from VOID_DESIGN_SYSTEM_SOT.md:**
```css
.diamond-dismiss {
    width: 12px;
    height: 12px;
    border: 1.5px solid var(--muted);
    transform: rotate(45deg);
    background: transparent;
    cursor: pointer;
}
```

### Pattern 3: Bottom-Anchored Input Container

**What:** Input bar fixed at bottom, z-index 20, max-width 600px centered.

**When to use:** Command input, chat, summon interface

**Implementation:**
```css
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 20;
    padding: 0 20px 20px;
}

.input-container {
    max-width: 600px;
    margin: 0 auto;
    border-radius: 8px;
    background: var(--bg-elevated);
    border: 1px solid var(--border-subtle);
    transition: all 300ms ease-out;
}
```

### Pattern 4: Tool Row Configuration

**What:** Row of icon buttons for actions, ordered left-to-right

**When to use:** Context toolbars, action rows

**Standard Order (VOID_DESIGN_SYSTEM_SOT.md):**
1. Gear (⚙) - Settings overlay
2. Upload (↑) - File explorer
3. Documents (📄) - Document browser
4. Terminal (▶_) - Command interface
5. Microphone (🎤) - Voice mode
6. **Center** - Diamond M (Summon)
7. **Right** - Chevron (▶) - Send

### Pattern 5: Settings Tab Navigation

**What:** Horizontal tab buttons with active state indicator

**When to use:** Settings panel, configuration UI

**Implementation from 07_settings.py:**
```python
tabs = {
    "agents": ("Agents", "Configure AI agents"),
    "tools": ("Tools", "Configure 888 tools"),
    "models": ("Models", "Configure local AI models"),
    "ui": ("UI", "User interface preferences"),
    # ...
}
```

### Pattern 6: Particle-Based Code City

**What:** Canvas/WebGL rendering of code as buildings using Barradeau technique

**When to use:** Main visualization component, file dependency mapping

**Implementation from woven_maps.py:**
- Building height: `3 + (exports × 0.8)`
- Building footprint: `2 + (lines × 0.008)`
- Emergence duration: 2.5s
- GPU-first with CPU fallback

### Pattern 7: Three-State Color System

**What:** Only three states for code status - NO gradients, NO complex colors

**When to use:** All status indicators, Code City visualization

| State | Color | Hex | Trigger |
|-------|-------|-----|---------|
| Working | Gold | #D4AF37 | All imports resolve |
| Broken | Blue/Teal | #1fbdea | Has errors, needs attention |
| Combat | Purple | #9D4EDD | LLM General deployed |

## Don't Hand-Roll

### Problems That Already Have Solutions

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| **Settings persistence** | Custom file format | toml + pydantic-settings | EPO pattern proven, Tauri-ready |
| **Color theming** | Custom CSS variables | orchestr8.css CSS variables | Exact Void tokens defined |
| **Particle rendering** | Custom canvas code | woven_maps.py + woven_maps_3d.js | Barradeau technique implemented |
| **File watching** | Custom fsnotify | watchdog + Marimo FileWatcherManager | Per SOT locked decisions |
| **Font loading** | Custom font loader | font_profiles.py | Runtime injection centralized |
| **Emergence animations** | Custom keyframes | orchestr8.css @keyframes | Exactly specified in SOT |
| **Settings schema** | Ad-hoc dicts | Pydantic models | Type-safe, Tauri-compatible |

### Key Insight

The Void Design System explicitly forbids:
- Breathing/pulsing animations
- Emoji characters
- ✕ for dismiss (use ◇ instead)
- Gradients in state colors
- Red for errors (use teal #1fbdea)

## Common Pitfalls

### Pitfall 1: Breathing Animations Still Active

**What goes wrong:** Placeholder text has opacity animations cycling 1.0 → 0.7

**Why it happens:** VOID_DESIGN_SYSTEM_SOT.md notes breathing CSS variables exist for backwards compatibility but are set to no-op values

**How to avoid:** Use emergence animations instead, NOT breathing. Breathing disabled explicitly.

**Warning signs:** Opacity cycling on placeholder text, phase titles, or working indicators

### Pitfall 2: Using ✕ Instead of ◇ for Dismiss

**What goes wrong:** Close buttons use X character instead of diamond

**Why it happens:** Muscle memory from other UI frameworks

**How to avoid:** Always use rotated diamond: `transform: rotate(45deg)` or unicode ◆/◇

**Warning signs:** Any ✕ character in dismiss buttons

### Pitfall 3: Text Below 70% Brightness

**What goes wrong:** Dimmed text violates 100% brightness standard

**Why it happens:** Designers instinctively dim secondary text

**How to avoid:** Use color: var(--text-secondary) with full opacity, not reduced opacity

**Warning signs:** Any text with opacity < 1.0

### Pitfall 4: Red for Error States

**What goes wrong:** Using red for broken/.error states

**Why it happens:** Traditional UX pattern

**How to avoid:** Use teal (#1fbdea) for broken state - SOT LOCKED

**Warning signs:** Any #ef4444 or "red" color for errors

### Pitfall 5: Pre-defined Edges in Code City

**What goes wrong:** Hardcoded relationship lines

**Why it happens:** Simpler to implement static edges

**How to avoid:** Edges render from ACTUAL file relationships via ConnectionVerifier

**Warning signs:** Edges that don't change when code imports change

### Pitfall 6: Particle Payload Size Overflow

**What goes wrong:** Code City iframe payload exceeds Marimo limits (default 9MB)

**Why it happens:** Large codebases generate massive particle arrays

**How to avoid:** 
- Payload size guard in 06_maestro.py: `ORCHESTR8_CODE_CITY_MAX_BYTES`
- Fallback to IP/ subroot
- Streaming mode for 3D: `ORCHESTR8_CODE_CITY_STREAM_BPS`

**Warning signs:** WebSocket errors, render failures on large repos

### Pitfall 7: Incorrect Button Callbacks

**What goes wrong:** Using `on_change` instead of `on_click` for buttons

**Why it happens:** Marimo API confusion

**How to avoid:** Use `on_click` for button callbacks per CLAUDE.md troubleshooting

**Warning signs:** Buttons appear dead, don't respond to clicks

## Code Examples

### Example 1: Emergent Panel (Void Design)

```python
# Source: 06_maestro.py - Panel emergence pattern
def build_summon_results() -> Any:
    """Render search results as emergent cards."""
    return build_summon_results_view(
        mo,
        query=get_summon_query(),
        results=get_summon_results(),
        loading=get_summon_loading(),
        gold_color=GOLD_METALLIC,
        blue_color=BLUE_DOMINANT,
        purple_color=PURPLE_COMBAT,
    )
```

### Example 2: Settings Manager (EPO Pattern)

```python
# Source: 07_settings.py - EPO pattern adaptation
class SettingsManager:
    """Manages loading, editing, and saving pyproject_orchestr8_settings.toml"""
    
    def __init__(self):
        self.settings_file = Path("pyproject_orchestr8_settings.toml")
        self.settings = self.load_settings()
    
    def set_value(self, path: str, value: Any) -> None:
        """Set a specific setting value using dotted path notation."""
        parts = path.split(".")
        current = self.settings
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
```

### Example 3: CSS Variables (Exact Tokens)

```css
/* Source: orchestr8.css */
:root {
    --gold-metallic: #D4AF37;
    --gold-dark: #B8860B;
    --gold-saffron: #F4C430;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
}
```

### Example 4: Diamond Dismiss Button

```css
/* Source: VOID_DESIGN_SYSTEM_SOT.md */
.diamond-dismiss {
    width: 12px;
    height: 12px;
    border: 1.5px solid var(--muted);
    transform: rotate(45deg);
    background: transparent;
    cursor: pointer;
}

.diamond-dismiss:hover {
    border-color: var(--gold);
}
```

### Example 5: Particle-Based Building Generation

```python
# Source: woven_maps.py - Building geometry formulas (LOCKED)
BUILDING_HEIGHT_BASE = 3.0
BUILDING_HEIGHT_EXPORT_SCALE = 0.8
BUILDING_FOOTPRINT_BASE = 2.0
BUILDING_FOOTPRINT_LOC_SCALE = 0.008

def compute_building_geometry(lines: int, exports: int) -> tuple[float, float]:
    """Compute canonical building geometry using locked formulas."""
    height = BUILDING_HEIGHT_BASE + (exports * BUILDING_HEIGHT_EXPORT_SCALE)
    footprint = BUILDING_FOOTPRINT_BASE + (lines * BUILDING_FOOTPRINT_LOC_SCALE)
    return height, footprint
```

### Example 6: Three-State Color Helper

```python
# Source: IP/features/maestro/__init__.py
GOLD_METALLIC = "#D4AF37"
BLUE_DOMINANT = "#1fbdea"
PURPLE_COMBAT = "#9D4EDD"
BG_PRIMARY = "#0A0A0B"

def get_status_color(status: str) -> str:
    """Return exact color for status."""
    return {
        "working": GOLD_METALLIC,
        "broken": BLUE_DOMINANT,
        "combat": PURPLE_COMBAT,
    }.get(status, BLUE_DOMINANT)
```

## State of the Art

### Current Implementation (Feb 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| Void Design CSS | ✅ Complete | orchestr8.css with exact tokens |
| Settings System | ⚠️ Partial | 07_settings.py exists, needs Void styling |
| Code City 3D | ✅ Complete | woven_maps.py + woven_maps_3d.js |
| Particle Rendering | ✅ Complete | Barradeau technique implemented |
| Font Profiles | ✅ Complete | font_profiles.py runtime injection |
| Settings Persistence | ⚠️ Partial | TOML-based, needs pydantic upgrade |

### Deprecated/Outdated

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| HardCompn injection | Font profile system | 2026-02-13 | Dynamic font switching |
| on_change callbacks | on_click callbacks | 2026-02-13 | Button functionality fixed |
| Inline CSS in f-string | orchestr8.css file | 2026-02-13 | Maintainability |
| Global config | Project-scoped TOML | Pre-existing | Settings portability |

### What's Needed for Phase 08

1. **Void-styled settings UI** - Apply Void Design tokens to 07_settings.py
2. **Text-first component library** - Minimal chrome, typography-driven
3. **Summon interface refinement** - Rise animation, diamond dismiss
4. **Settings validation layer** - Pydantic models for Tauri readiness
5. **Real-time preview** - Theme changes apply immediately

## Open Questions

### Question 1: Settings Schema Strategy

**What we know:** 
- Current settings use TOML with dotted path notation
- EPO patterns use Rust config_manager.rs with validation
- Agent 02 recommends Pydantic for Python adaptation

**What's unclear:**
- Should we use pydantic-settings or manual TOML parsing?
- How to handle nested schema migrations?

**Recommendation:** Use Pydantic models for validation, serialize to TOML for persistence. This matches EPO pattern and enables future Tauri packaging.

### Question 2: Visual Richness vs. Text-First

**What we know:**
- CONTEXT.md specifies "Start simple: text + boxes + buttons"
- Void Design allows visual richness via emergence

**What's unclear:**
- How much visual polish is "later"?
- Should we invest in Canvas-based UI beyond Code City?

**Recommendation:** Prioritize text-first patterns, defer Canvas UI components until settings system is stable.

### Question 3: Tauri Integration Timing

**What we know:**
- Tauri packaging path preserved per CONTEXT.md
- Current Marimo-first, no Tauri dependency for core

**What's unclear:**
- When to introduce Tauri-specific features?
- How to handle platform-specific settings?

**Recommendation:** Keep settings Marimo-native for now, design Tauri-ready schemas. Deferred Tauri integration to Phase 09+.

## Sources

### Primary (HIGH confidence)

- **VOID_DESIGN_SYSTEM_SOT.md** - /home/bozertron/JFDI - Collabkit/Application/SOT/
  - Exact color tokens, emergence patterns, component structures
  - Authoritative source for visual design

- **agent_02.md** - /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/TAURI_SWARM_REPORTS/
  - EPO settings patterns, integration recommendations
  - Settings UI template and config schema patterns

- **06_maestro.py** - IP/plugins/
  - Implementation of Void Design in Marimo
  - Code City integration, emergence patterns

- **07_settings.py** - IP/plugins/
  - Current settings implementation
  - SettingsManager class pattern

- **orchestr8.css** - IP/styles/
  - Exact CSS variables matching Void tokens
  - Emergence keyframes

### Secondary (MEDIUM confidence)

- **woven_maps.py** - IP/
  - Particle rendering, building geometry formulas
  - 3D visualization approach

- **CLAUDE.md** - Project root
  - Architecture constraints, execution order
  - Button callback troubleshooting

- **CONTEXT.md** - /home/bozertron/Orchestr8_jr/.planning/phases/08-design-ui-system/
  - Phase scope, locked decisions, research domains

### Tertiary (LOW confidence)

- WebSearch: "Marimo UI customization patterns 2026" - General exploration
- WebSearch: "WebGL particle systems performance 2026" - Canvas optimization

## Metadata

**Confidence breakdown:**
- Standard Stack: HIGH - Exact tokens and implementations verified
- Architecture: HIGH - Patterns from authoritative sources
- Pitfalls: HIGH - Known issues documented in SOT and CLAUDE.md
- Code Examples: HIGH - Sourced from actual implementation files

**Research date:** 2026-02-16
**Valid until:** 2026-03-16 (30 days for stable domain)

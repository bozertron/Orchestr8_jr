# Big Pickle: Marimo Styling Implementation Tasks

**Target:** Match MaestroView.vue aesthetic within Marimo constraints  
**Reference:** `/home/bozertron/Orchestr8_jr/style/MAESTROVIEW_REFERENCE.md`  
**Research Source:** Marimo theming documentation (2026-01-26)

---

## Phase 0: Foundation Setup

### Task 0.1: Create Project-Level CSS File
**File:** `IP/styles/orchestr8.css`

Create the master CSS file with MaestroView.vue color variables:

```css
/* orchestr8.css - MaestroView.vue Alignment */

/* Load fonts */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    /* Primary Colors - EXACT from MaestroView.vue */
    --gold-metallic: #D4AF37;
    --gold-dark: #B8860B;
    --gold-saffron: #F4C430;
    --blue-dominant: #1fbdea;
    --purple-combat: #9D4EDD;
    
    /* Backgrounds - The Void */
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
    --bg-surface: #1a1a1c;
    
    /* Text */
    --text-primary: #e8e8e8;
    --text-secondary: #a0a0a0;
    --text-muted: #666666;
    
    /* Status Colors */
    --status-working: #D4AF37;
    --status-broken: #1fbdea;
    --status-combat: #9D4EDD;
    
    /* Fonts */
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;
    --font-ui: 'IBM Plex Mono', monospace;
    
    /* Override Marimo defaults */
    --marimo-heading-font: var(--font-mono);
    --marimo-monospace-font: var(--font-mono);
}
```

**Acceptance:** File exists at path, loads without errors.

---

### Task 0.2: Configure pyproject.toml for Custom CSS
**File:** `pyproject.toml`

Add marimo display configuration:

```toml
[tool.marimo.display]
custom_css = ["IP/styles/orchestr8.css"]
```

**Acceptance:** Marimo loads the CSS file on notebook startup.

---

### Task 0.3: Create HTML Head Injection (Backup Font Method)
**Location:** App Configuration menu in each notebook

If @import fails, use HTML Head injection:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Acceptance:** Fonts load even if CSS @import blocked.

---

## Phase 1: Global Theme Application

### Task 1.1: Style Body and Root Elements
**File:** `IP/styles/orchestr8.css`

Add global body styling:

```css
body {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-ui) !important;
}

/* Remove any white backgrounds */
.marimo-app, 
.marimo-notebook,
[data-marimo-container] {
    background-color: var(--bg-primary) !important;
}
```

**Acceptance:** Notebook background is `#0A0A0B` (The Void).

---

### Task 1.2: Style All Buttons - Gold Theme
**File:** `IP/styles/orchestr8.css`

```css
/* Primary buttons - Gold */
button, 
.marimo-button,
[data-marimo-element="button"] {
    background-color: transparent !important;
    border: 1px solid var(--gold-metallic) !important;
    color: var(--gold-metallic) !important;
    font-family: var(--font-mono) !important;
    transition: all 0.2s ease !important;
}

button:hover,
.marimo-button:hover {
    background-color: var(--gold-metallic) !important;
    color: var(--bg-primary) !important;
}

/* Active/Selected state */
button:active,
button[data-active="true"] {
    background-color: var(--gold-saffron) !important;
    border-color: var(--gold-saffron) !important;
}
```

**Acceptance:** All buttons have gold borders, gold text, gold hover fill.

---

### Task 1.3: Style Input Fields
**File:** `IP/styles/orchestr8.css`

```css
input, 
textarea,
select,
.marimo-input {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--gold-dark) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
}

input:focus,
textarea:focus {
    border-color: var(--gold-metallic) !important;
    outline: none !important;
    box-shadow: 0 0 0 1px var(--gold-metallic) !important;
}
```

**Acceptance:** Inputs have elevated background, gold border on focus.

---

### Task 1.4: Style Code Blocks and Output
**File:** `IP/styles/orchestr8.css`

```css
/* Code cells */
pre, code,
.marimo-code,
[data-marimo-element="code"] {
    background-color: var(--bg-elevated) !important;
    font-family: var(--font-mono) !important;
    border: 1px solid var(--bg-surface) !important;
}

/* Output areas */
[data-cell-role="output"] {
    background-color: var(--bg-primary) !important;
    border-left: 2px solid var(--gold-dark) !important;
    padding-left: 1rem !important;
}
```

**Acceptance:** Code blocks use elevated background, output has gold accent border.

---

## Phase 2: Cell-Specific Styling

### Task 2.1: Create Named Cell CSS Targets
**File:** `IP/styles/orchestr8.css`

Create reusable cell targeting patterns:

```css
/* Maestro/Void specific cells */
[data-cell-name='maestro_header'] {
    background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-primary) 100%) !important;
    border-bottom: 1px solid var(--gold-dark) !important;
}

[data-cell-name='fiefdom_list'] {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--bg-surface) !important;
}

[data-cell-name='mermaid_graph'] {
    background-color: var(--bg-primary) !important;
    border: 1px solid var(--gold-dark) !important;
}

[data-cell-name='command_input'] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background-color: var(--bg-elevated) !important;
    border-top: 1px solid var(--gold-metallic) !important;
    z-index: 1000 !important;
}
```

**Acceptance:** Named cells receive specific styling when cell names match.

---

### Task 2.2: Update Plugin Cells with Names
**Files:** All files in `IP/plugins/`

Add `@app.cell(name="descriptive_name")` decorators to key cells:

| Plugin | Cell Name | Purpose |
|--------|-----------|---------|
| 06_maestro.py | `maestro_header` | Top navigation |
| 06_maestro.py | `mermaid_graph` | Status visualization |
| 06_maestro.py | `fiefdom_list` | Fiefdom sidebar |
| 06_maestro.py | `command_input` | Bottom input bar |
| 03_gatekeeper.py | `lock_controls` | Lock/Unlock buttons |
| 01_generator.py | `wizard_steps` | 7-phase wizard |

**Acceptance:** CSS cell targeting works for all named cells.

---

## Phase 3: Status Color Implementation

### Task 3.1: Create Status Badge CSS Classes
**File:** `IP/styles/orchestr8.css`

```css
/* Status indicators */
.status-working {
    color: var(--status-working) !important;
    border-color: var(--status-working) !important;
}

.status-broken {
    color: var(--status-broken) !important;
    border-color: var(--status-broken) !important;
}

.status-combat {
    color: var(--status-combat) !important;
    border-color: var(--status-combat) !important;
}

/* Status badges */
.badge-working {
    background-color: var(--status-working) !important;
    color: var(--bg-primary) !important;
    padding: 0.25rem 0.5rem !important;
    border-radius: 2px !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}

.badge-broken {
    background-color: var(--status-broken) !important;
    color: var(--bg-primary) !important;
    padding: 0.25rem 0.5rem !important;
    border-radius: 2px !important;
}

.badge-combat {
    background-color: var(--status-combat) !important;
    color: white !important;
    padding: 0.25rem 0.5rem !important;
    border-radius: 2px !important;
}
```

**Acceptance:** Status classes render correct colors when applied.

---

### Task 3.2: Create Python Helper for Status HTML
**File:** `IP/plugins/status_helpers.py`

```python
"""Status HTML helpers for consistent styling."""

def status_badge(status: str) -> str:
    """Return styled HTML badge for status."""
    status_lower = status.lower()
    if status_lower == "working":
        return '<span class="badge-working">WORKING</span>'
    elif status_lower == "broken":
        return '<span class="badge-broken">BROKEN</span>'
    elif status_lower == "combat":
        return '<span class="badge-combat">COMBAT</span>'
    else:
        return f'<span class="badge-broken">{status.upper()}</span>'

def fiefdom_indicator(status: str) -> str:
    """Return colored circle indicator."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD"
    }
    color = colors.get(status.lower(), "#1fbdea")
    return f'<span style="color: {color}; font-size: 1.5rem;">●</span>'
```

**Acceptance:** Helpers imported and usable in all plugins.

---

## Phase 4: Emerge Transitions

**REMOVED** - Working on this directly with Emperor. See `Big Pickle/EMERGE_ANIMATIONS_REFERENCE.md`

---

## Phase 5: Plugin-Specific Styling

### Task 5.1: Style 06_maestro.py (The Void)
**File:** `IP/plugins/06_maestro.py`

Apply inline styles via `mo.md()` and `mo.Html()`:

```python
# Header with gold accent
mo.md("""
<div style="
    border-bottom: 1px solid #B8860B;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <span style="color: #D4AF37; font-family: 'JetBrains Mono', monospace; font-size: 1.5rem;">
        ORCHESTR8
    </span>
    <div>
        <button class="nav-btn">Agents</button>
        <button class="nav-btn">Tickets</button>
        <button class="nav-btn">Settings</button>
    </div>
</div>
""")
```

**Acceptance:** Maestro header matches MaestroView.vue layout.

---

### Task 5.2: Style 03_gatekeeper.py (Louis UI)
**File:** `IP/plugins/03_gatekeeper.py`

Ensure Lock All/Unlock All buttons use gold theme.

**Acceptance:** Gatekeeper buttons styled consistently.

---

### Task 5.3: Style 01_generator.py (7-Phase Wizard)
**File:** `IP/plugins/01_generator.py`

Style wizard phases with gold progress indicators.

**Acceptance:** Wizard steps show gold active state, muted inactive.

---

## Phase 6: Mermaid Graph Styling

### Task 6.1: Style Mermaid Output
**File:** `IP/styles/orchestr8.css`

```css
/* Mermaid diagram container */
.mermaid, 
[data-marimo-element="mermaid"] {
    background-color: var(--bg-primary) !important;
}

/* Override Mermaid internal colors via CSS variables */
.mermaid .node rect {
    stroke-width: 2px !important;
}

/* Note: Mermaid node colors should be set in the diagram definition, not CSS */
```

**Note:** Mermaid colors are best controlled in the diagram syntax itself:
```
graph TB
    A[src/llm]:::working --> B[src/modules]:::broken
    classDef working fill:#D4AF37,stroke:#B8860B,color:#0A0A0B
    classDef broken fill:#1fbdea,stroke:#1fbdea,color:#0A0A0B
    classDef combat fill:#9D4EDD,stroke:#9D4EDD,color:#fff
```

**Acceptance:** Mermaid nodes render with correct gold/blue/purple fills.

---

### Task 6.2: Create Mermaid Theme Generator
**File:** `IP/mermaid_theme.py`

```python
"""Generate Mermaid diagrams with MaestroView.vue colors."""

MERMAID_CLASSDEFS = """
    classDef working fill:#D4AF37,stroke:#B8860B,color:#0A0A0B
    classDef broken fill:#1fbdea,stroke:#1fbdea,color:#0A0A0B
    classDef combat fill:#9D4EDD,stroke:#9D4EDD,color:#fff
    classDef default fill:#121214,stroke:#B8860B,color:#e8e8e8
"""

def generate_status_graph(fiefdoms: dict) -> str:
    """Generate Mermaid graph with proper status colors."""
    lines = ["graph TB"]
    
    for name, info in fiefdoms.items():
        status = info.get("status", "broken").lower()
        lines.append(f"    {name}[{name}]:::{status}")
    
    # Add relationships
    for name, info in fiefdoms.items():
        for dep in info.get("depends_on", []):
            lines.append(f"    {dep} --> {name}")
    
    lines.append(MERMAID_CLASSDEFS)
    return "\n".join(lines)
```

**Acceptance:** Generated Mermaid uses correct status colors.

---

## Phase 7: Testing & Validation

### Task 7.1: Create Style Test Notebook
**File:** `IP/test_styles.py`

Create a Marimo notebook that displays:
- All color variables as swatches
- All button states
- All status badges
- Sample Mermaid graph
- Sample emerge animations

**Acceptance:** Visual confirmation of all styles.

---

### Task 7.2: Screenshot Comparison
Compare rendered output against MaestroView.vue reference screenshots.

| Element | Expected | Status |
|---------|----------|--------|
| Background | #0A0A0B | ☐ |
| Button border | #D4AF37 | ☐ |
| Button hover | Gold fill | ☐ |
| Input border | #B8860B | ☐ |
| Working badge | Gold | ☐ |
| Broken badge | Blue | ☐ |
| Combat badge | Purple | ☐ |

**Acceptance:** All checkboxes verified.

---

## Execution Order

```
0.1 → 0.2 → 0.3 (Foundation)
    ↓
1.1 → 1.2 → 1.3 → 1.4 (Global Theme)
    ↓
2.1 → 2.2 (Cell-Specific)
    ↓
3.1 → 3.2 (Status Colors)
    ↓
[Phase 4: Animations - handled separately with Emperor]
    ↓
5.1 → 5.2 → 5.3 (Plugin-Specific)
    ↓
6.1 → 6.2 (Mermaid)
    ↓
7.1 → 7.2 (Testing)
```

---

## Dependencies

- Marimo installed and working
- Internet access for Google Fonts (or local font files)
- MaestroView.vue reference document available
- All plugins in IP/plugins/ functional

---

## Success Criteria

1. **The Void** renders with `#0A0A0B` background
2. All interactive elements use gold color scheme
3. Status indicators correctly show gold/blue/purple
4. Fonts are JetBrains Mono / IBM Plex Mono
5. No white backgrounds anywhere
6. Emerge animations work (best effort)
7. Mermaid graphs use correct classDefs

---

**END TASK LIST**

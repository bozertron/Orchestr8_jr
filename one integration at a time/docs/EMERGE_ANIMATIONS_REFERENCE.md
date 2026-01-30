# Emerge Animations in Marimo: Complete Reference

**Purpose:** Every mechanism for implementing "emerge from void" transitions  
**Scope:** Internal work - no external IP needed  
**Status:** RESEARCH COMPLETE - READY FOR DISCUSSION

---

## Overview

MaestroView.vue specifies that UI elements don't "load" - they **EMERGE FROM THE VOID**. This document covers every way to achieve this in Marimo.

**Design Rule:** NO breathing animations. Elements emerge once, then stay static.

---

## Method 1: CSS Keyframe Animations (via Custom CSS File)

**Best For:** Global emerge patterns applied to all notebooks

### 1.1 File Setup

```css
/* IP/styles/orchestr8.css */

/* EMERGE FROM VOID - Fade + Scale */
@keyframes emerge-void {
    0% {
        opacity: 0;
        transform: scale(0.95);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

/* EMERGE FROM RIGHT - Panel slide */
@keyframes emerge-right {
    0% {
        opacity: 0;
        transform: translateX(100%);
    }
    100% {
        opacity: 1;
        transform: translateX(0);
    }
}

/* EMERGE FROM TOP - Dropdown/menu slide */
@keyframes emerge-down {
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* EMERGE FROM BOTTOM - Notification rise */
@keyframes emerge-up {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* EMERGE FROM CENTER - Modal/card pop */
@keyframes emerge-center {
    0% {
        opacity: 0;
        transform: scale(0.8);
    }
    50% {
        transform: scale(1.02);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}
```

### 1.2 Application Classes

```css
/* Apply via class names */
.emerge-void {
    animation: emerge-void 0.3s ease-out forwards;
}

.emerge-right {
    animation: emerge-right 0.3s ease-out forwards;
}

.emerge-down {
    animation: emerge-down 0.3s ease-out forwards;
}

.emerge-up {
    animation: emerge-up 0.3s ease-out forwards;
}

.emerge-center {
    animation: emerge-center 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

/* Delayed emergence for staggered effects */
.emerge-delay-1 { animation-delay: 0.1s; opacity: 0; }
.emerge-delay-2 { animation-delay: 0.2s; opacity: 0; }
.emerge-delay-3 { animation-delay: 0.3s; opacity: 0; }
```

### 1.3 Configuration

```toml
# pyproject.toml
[tool.marimo.display]
custom_css = ["IP/styles/orchestr8.css"]
```

---

## Method 2: Inline CSS via mo.Html()

**Best For:** Per-component animation control

### 2.1 Basic Inline Animation

```python
@app.cell
def _():
    mo.Html("""
    <style>
        @keyframes emerge {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .emerging-panel {
            animation: emerge 0.3s ease-out forwards;
            background: #121214;
            border: 1px solid #B8860B;
            padding: 1rem;
        }
    </style>
    <div class="emerging-panel">
        <h3 style="color: #D4AF37;">Fiefdom Status</h3>
        <p style="color: #e8e8e8;">All systems operational</p>
    </div>
    """)
```

### 2.2 Dynamic Animation with Python

```python
@app.cell
def _():
    def create_emerging_card(title: str, content: str, delay: float = 0) -> mo.Html:
        """Create a card that emerges from the void."""
        return mo.Html(f"""
        <div style="
            animation: emerge-void 0.3s ease-out {delay}s forwards;
            opacity: 0;
            background: #121214;
            border: 1px solid #B8860B;
            border-radius: 4px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <h4 style="color: #D4AF37; margin: 0 0 0.5rem 0;">{title}</h4>
            <p style="color: #e8e8e8; margin: 0;">{content}</p>
        </div>
        """)
    return create_emerging_card
```

### 2.3 Staggered Emergence

```python
@app.cell
def _():
    fiefdoms = [
        ("src/llm", "working"),
        ("src/modules", "broken"),
        ("src/platform", "combat"),
    ]
    
    status_colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD"
    }
    
    cards = []
    for i, (name, status) in enumerate(fiefdoms):
        delay = i * 0.1  # 100ms stagger
        color = status_colors[status]
        cards.append(f"""
        <div style="
            animation: emerge-void 0.3s ease-out {delay}s forwards;
            opacity: 0;
            background: #121214;
            border-left: 3px solid {color};
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
        ">
            <span style="color: {color};">●</span>
            <span style="color: #e8e8e8; margin-left: 0.5rem;">{name}</span>
            <span style="color: #666; float: right;">{status.upper()}</span>
        </div>
        """)
    
    mo.Html(f"""
    <style>
        @keyframes emerge-void {{
            from {{ opacity: 0; transform: scale(0.95); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
    </style>
    <div style="background: #0A0A0B; padding: 1rem;">
        {''.join(cards)}
    </div>
    """)
```

---

## Method 3: The .style() Method

**Best For:** Simple styling without raw HTML

### 3.1 Basic Usage

```python
@app.cell
def _():
    # Style returns a new Html object with wrapper div
    mo.md("# Fiefdom Overview").style({
        "animation": "emerge-void 0.3s ease-out forwards",
        "opacity": "0",  # Initial state before animation
        "background": "#121214",
        "padding": "1rem",
        "border-radius": "4px"
    })
```

### 3.2 Keyword Arguments (Pythonic)

```python
@app.cell
def _():
    mo.md("**Status:** Working").style(
        animation="emerge-void 0.3s ease-out forwards",
        opacity="0",
        background_color="#121214",  # Underscores become hyphens
        padding="1rem",
        border_left="3px solid #D4AF37"
    )
```

### 3.3 Limitation

**IMPORTANT:** The `.style()` method wraps content in a `<div>`. The animation CSS must already be defined (via custom CSS file or earlier mo.Html injection).

---

## Method 4: Cell-Specific CSS Targeting

**Best For:** Animating entire cells by name

### 4.1 Named Cells

```python
@app.cell(name="fiefdom_panel")
def _():
    mo.md("## Fiefdoms")
```

### 4.2 CSS Targeting

```css
/* In orchestr8.css */

/* Target the entire cell */
[data-cell-name='fiefdom_panel'] {
    animation: emerge-right 0.4s ease-out forwards;
    opacity: 0;
}

/* Target only the cell's output */
[data-cell-name='fiefdom_panel'] [data-cell-role='output'] {
    animation: emerge-void 0.3s ease-out 0.1s forwards;
    opacity: 0;
}

/* Specific cells for The Void layout */
[data-cell-name='mermaid_graph'] {
    animation: emerge-void 0.4s ease-out forwards;
}

[data-cell-name='tickets_panel'] {
    animation: emerge-right 0.3s ease-out forwards;
    position: fixed;
    right: 0;
    top: 60px;
    bottom: 80px;
    width: 400px;
    background: #121214;
    border-left: 1px solid #B8860B;
}

[data-cell-name='command_bar'] {
    /* Overton Anchor - NO ANIMATION, always visible */
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 20vh;
    background: #121214;
    border-top: 1px solid #D4AF37;
    z-index: 1000;
}
```

---

## Method 5: mo.ui.anywidget() Custom Animations

**Best For:** Complex interactive animations with state

### 5.1 Custom Animated Widget

```python
import anywidget
import traitlets
import marimo as mo

class EmergingPanel(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        const panel = document.createElement('div');
        panel.className = 'emerging-panel';
        panel.innerHTML = model.get('content');
        
        // Trigger animation on mount
        panel.style.opacity = '0';
        panel.style.transform = 'scale(0.95)';
        
        requestAnimationFrame(() => {
            panel.style.transition = 'all 0.3s ease-out';
            panel.style.opacity = '1';
            panel.style.transform = 'scale(1)';
        });
        
        // Update content when model changes
        model.on('change:content', () => {
            panel.style.opacity = '0';
            setTimeout(() => {
                panel.innerHTML = model.get('content');
                panel.style.opacity = '1';
            }, 150);
        });
        
        el.appendChild(panel);
    }
    export default { render };
    """
    
    _css = """
    .emerging-panel {
        background: #121214;
        border: 1px solid #B8860B;
        border-radius: 4px;
        padding: 1rem;
        color: #e8e8e8;
    }
    """
    
    content = traitlets.Unicode("").tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)

# Usage
panel = mo.ui.anywidget(EmergingPanel(content="<h3>Fiefdom Details</h3>"))
```

### 5.2 State-Triggered Animation

```python
class TogglePanel(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        const panel = document.createElement('div');
        panel.className = 'toggle-panel';
        
        function updateVisibility() {
            if (model.get('visible')) {
                panel.style.transform = 'translateX(0)';
                panel.style.opacity = '1';
            } else {
                panel.style.transform = 'translateX(100%)';
                panel.style.opacity = '0';
            }
        }
        
        panel.style.transition = 'all 0.3s ease-out';
        model.on('change:visible', updateVisibility);
        updateVisibility();
        
        panel.innerHTML = model.get('content');
        el.appendChild(panel);
    }
    export default { render };
    """
    
    _css = """
    .toggle-panel {
        position: fixed;
        right: 0;
        top: 60px;
        bottom: 80px;
        width: 400px;
        background: #121214;
        border-left: 1px solid #B8860B;
        padding: 1rem;
    }
    """
    
    content = traitlets.Unicode("").tag(sync=True)
    visible = traitlets.Bool(False).tag(sync=True)
```

---

## Method 6: mo.iframe() for Isolated Animations

**Best For:** Complex animations that might conflict with Marimo's styles

### 6.1 Self-Contained Animated Component

```python
@app.cell
def _():
    animated_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                background: #0A0A0B;
                font-family: 'JetBrains Mono', monospace;
            }
            
            @keyframes emerge {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .card {
                animation: emerge 0.3s ease-out forwards;
                background: #121214;
                border: 1px solid #B8860B;
                border-radius: 4px;
                padding: 1rem;
                margin: 1rem;
                color: #e8e8e8;
            }
            
            .status-gold { color: #D4AF37; }
            .status-blue { color: #1fbdea; }
            .status-purple { color: #9D4EDD; }
        </style>
    </head>
    <body>
        <div class="card">
            <h3 class="status-gold">src/llm</h3>
            <p>Status: WORKING</p>
        </div>
    </body>
    </html>
    """
    
    mo.iframe(animated_html, width="100%", height="200px")
```

---

## Method 7: Conditional Rendering with mo.state()

**Best For:** Show/hide animations triggered by user interaction

### 7.1 Toggle Panel Pattern

```python
@app.cell
def _():
    get_panel_visible, set_panel_visible = mo.state(False)
    return get_panel_visible, set_panel_visible

@app.cell
def _():
    toggle_btn = mo.ui.button(
        label="Toggle Tickets",
        on_change=lambda _: set_panel_visible(not get_panel_visible())
    )
    toggle_btn

@app.cell
def _():
    if get_panel_visible():
        mo.Html("""
        <div style="
            animation: emerge-right 0.3s ease-out forwards;
            position: fixed;
            right: 0;
            top: 60px;
            bottom: 80px;
            width: 400px;
            background: #121214;
            border-left: 1px solid #B8860B;
            padding: 1rem;
        ">
            <h3 style="color: #D4AF37;">Tickets</h3>
            <p style="color: #e8e8e8;">TICKET-042: Fix type errors</p>
        </div>
        """)
    else:
        None  # Panel hidden
```

### 7.2 Progressive Disclosure

```python
@app.cell
def _():
    get_expanded, set_expanded = mo.state(set())  # Set of expanded items
    return get_expanded, set_expanded

@app.cell
def _():
    def toggle_item(item_id: str):
        current = get_expanded()
        if item_id in current:
            set_expanded(current - {item_id})
        else:
            set_expanded(current | {item_id})
    return toggle_item

@app.cell
def _():
    fiefdoms = ["src/llm", "src/modules", "src/platform"]
    
    items = []
    for fiefdom in fiefdoms:
        is_expanded = fiefdom in get_expanded()
        expand_style = """
            max-height: 200px;
            opacity: 1;
            padding: 1rem;
        """ if is_expanded else """
            max-height: 0;
            opacity: 0;
            padding: 0 1rem;
            overflow: hidden;
        """
        
        items.append(f"""
        <div style="
            background: #121214;
            border: 1px solid #B8860B;
            margin: 0.25rem 0;
        ">
            <div style="
                padding: 0.75rem 1rem;
                cursor: pointer;
                color: #D4AF37;
            " onclick="window.marimoToggle('{fiefdom}')">
                {fiefdom}
            </div>
            <div style="
                transition: all 0.3s ease-out;
                {expand_style}
                background: #0A0A0B;
                color: #e8e8e8;
            ">
                Details for {fiefdom}
            </div>
        </div>
        """)
    
    mo.Html(f"""
    <div style="background: #0A0A0B; padding: 1rem;">
        {''.join(items)}
    </div>
    """)
```

---

## Orchestr8 Animation Specification

### Required Animations

| Element | Animation | Duration | Timing |
|---------|-----------|----------|--------|
| **Fiefdom Cards** | emerge-void | 0.3s | ease-out, staggered 0.1s |
| **Mermaid Graph** | emerge-void | 0.4s | ease-out |
| **Tickets Panel** | emerge-right | 0.3s | ease-out |
| **Agents Panel** | emerge-down | 0.3s | ease-out |
| **Settings Panel** | emerge-right | 0.3s | ease-out |
| **Fiefdom Detail Card** | emerge-center | 0.4s | cubic-bezier bounce |
| **Notifications** | emerge-up | 0.2s | ease-out |
| **Overton Anchor** | NONE | - | Always visible |

### Forbidden Animations

| Type | Why Forbidden |
|------|---------------|
| Breathing/pulsing | Distracting, implies loading |
| Infinite loops | UI should be static after emerge |
| Hover wobble | Unprofessional |
| Loading spinners | Use progress bars if needed |
| Bouncing elements | Childish |

---

## Complete CSS Animation Library

```css
/* IP/styles/animations.css - Import via orchestr8.css */

/* ===============================
   EMERGE ANIMATIONS
   =============================== */

/* From void (default) */
@keyframes emerge-void {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

/* Directional emerges */
@keyframes emerge-right {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes emerge-left {
    from { opacity: 0; transform: translateX(-100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes emerge-down {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes emerge-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Modal/card pop */
@keyframes emerge-center {
    0% { opacity: 0; transform: scale(0.8); }
    70% { transform: scale(1.02); }
    100% { opacity: 1; transform: scale(1); }
}

/* ===============================
   APPLICATION CLASSES
   =============================== */

.emerge-void { animation: emerge-void 0.3s ease-out forwards; }
.emerge-right { animation: emerge-right 0.3s ease-out forwards; }
.emerge-left { animation: emerge-left 0.3s ease-out forwards; }
.emerge-down { animation: emerge-down 0.3s ease-out forwards; }
.emerge-up { animation: emerge-up 0.2s ease-out forwards; }
.emerge-center { animation: emerge-center 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }

/* Stagger delays */
.emerge-delay-100 { animation-delay: 0.1s; opacity: 0; }
.emerge-delay-200 { animation-delay: 0.2s; opacity: 0; }
.emerge-delay-300 { animation-delay: 0.3s; opacity: 0; }
.emerge-delay-400 { animation-delay: 0.4s; opacity: 0; }
.emerge-delay-500 { animation-delay: 0.5s; opacity: 0; }

/* ===============================
   CELL-SPECIFIC ANIMATIONS
   =============================== */

[data-cell-name='mermaid_graph'] [data-cell-role='output'] {
    animation: emerge-void 0.4s ease-out forwards;
}

[data-cell-name='fiefdom_list'] [data-cell-role='output'] {
    animation: emerge-void 0.3s ease-out 0.1s forwards;
    opacity: 0;
}

[data-cell-name='tickets_panel'] [data-cell-role='output'] {
    animation: emerge-right 0.3s ease-out forwards;
}

[data-cell-name='agents_panel'] [data-cell-role='output'] {
    animation: emerge-down 0.3s ease-out forwards;
}

/* NO animation for Overton Anchor */
[data-cell-name='command_bar'] [data-cell-role='output'] {
    animation: none !important;
    opacity: 1 !important;
}

/* ===============================
   TRANSITION UTILITIES
   =============================== */

.transition-all {
    transition: all 0.3s ease-out;
}

.transition-opacity {
    transition: opacity 0.3s ease-out;
}

.transition-transform {
    transition: transform 0.3s ease-out;
}

/* For JS-controlled show/hide */
.hidden {
    opacity: 0;
    pointer-events: none;
}

.visible {
    opacity: 1;
    pointer-events: auto;
}
```

---

## Discussion Points

### 1. Animation Approach

- **Q:** CSS file vs. inline mo.Html() - which should be primary?
- **Q:** Should we create an anywidget for complex animations?
- **Q:** How to handle mobile/reduced-motion preferences?

### 2. Performance

- **Q:** Too many animations on page load?
- **Q:** Should stagger delays be configurable?
- **Q:** GPU acceleration via `transform` vs `left/top`?

### 3. State Transitions

- **Q:** How to animate state changes (working → broken)?
- **Q:** Flash/highlight on status change?
- **Q:** Sound cues allowed? (probably not)

### 4. Panel System

- **Q:** Fixed panels vs. overlay panels?
- **Q:** How to handle panel stacking?
- **Q:** Close animations (reverse of emerge)?

### 5. Testing

- **Q:** How to verify animations work as expected?
- **Q:** Cross-browser testing approach?
- **Q:** Screenshots for documentation?

---

## Action Items After Discussion

1. [ ] Finalize animation timing specifications
2. [ ] Create IP/styles/animations.css
3. [ ] Test emerge-right for Tickets panel
4. [ ] Test emerge-down for Agents panel
5. [ ] Implement staggered fiefdom card emergence
6. [ ] Decide on close animations (fade vs. slide)

---

**END REFERENCE DOCUMENT**

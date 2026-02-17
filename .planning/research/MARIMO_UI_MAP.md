# Marimo UI Research: Complete Map & Shortcut Recommendations

**Project:** Orchestr8 (Code City Visualization)
**Research Date:** 2026-02-13
**Purpose:** Map all marimo UI elements and identify off-the-shelf shortcuts to accelerate development

---

## Executive Summary

Marimo provides a rich ecosystem of built-in UI components plus deep third-party integration via **anywidget**. The platform supports both native Python components AND arbitrary JavaScript widgets, enabling rapid development of complex dashboards like Orchestr8.

**Key Finding:** Most of Orchestr8's UI needs can be met with built-in marimo components + anywidget libraries. Only the Code City visualization itself requires custom canvas/WebGL.

---

## Part 1: Complete UI Element Map

### 1.1 Built-in Inputs (`marimo.ui`)

| Component | Description | Orchestr8 Use Case |
|-----------|-------------|-------------------|
| `mo.ui.button` | Interactive buttons with callbacks | Control panel buttons |
| `mo.ui.slider` | Single value slider | Density, sensitivity controls |
| `mo.ui.range_slider` | Min/max range slider | Layer depth, zoom ranges |
| `mo.ui.text` | Single-line text input | Search, filter inputs |
| `mo.ui.text_area` | Multi-line text | Command input, chat |
| `mo.ui.dropdown` | Single selection | Fiefdom selector, view modes |
| `mo.ui.multiselect` | Multi-selection | Multiple file selection |
| `mo.ui.checkbox` | Boolean toggle | Toggle features on/off |
| `mo.ui.switch` | iOS-style toggle | Feature flags |
| `mo.ui.radio` | Radio button group | View mode selection |
| `mo.ui.number` | Numeric input | Threshold values |
| `mo.ui.date` | Date picker | Date filtering |
| `mo.ui.dates` | Date range picker | Date range selection |
| `mo.ui.file` | File upload | Import config files |
| `mo.ui.file_browser` | Directory browser | File navigation |
| `mo.ui.table` | Interactive data table | Error lists, file listings |
| `mo.ui.dataframe` | Pandas dataframe viewer | Health results display |
| `mo.ui.data_editor` | Editable spreadsheet | Configuration editing |
| `mo.ui.tabs` | Tabbed interface | Panel switching |
| `mo.ui.nav_menu` | Navigation menu | Main navigation |
| `mo.ui.chat` | Chat interface | Collabor8 chat |
| `mo.ui.code_editor` | Monaco code editor | Code viewing/editing |
| `mo.ui.form` | Form with submit | Filter forms |
| `mo.ui.array` | Dynamic list of inputs | Dynamic form fields |
| `mo.ui.dictionary` | Key-value inputs | Configuration dicts |
| `mo.ui.refresh` | Auto-refresh control | Live data updates |
| `mo.ui.run_button` | Run with loading state | Execute actions |
| `mo.ui.batch` | Group inputs for value dict | Combined inputs |
| `mo.ui.anywidget` | Third-party widgets | **KEY INTEGRATION POINT** |

### 1.2 Built-in Layouts (`marimo`)

| Component | Description | Orchestr8 Use Case |
|-----------|-------------|-------------------|
| `mo.vstack` | Vertical stacking | Main layout |
| `mo.hstack` | Horizontal stacking | Control bars |
| `mo.sidebar` | Sidebar container | Right panel |
| `mo.tabs` | Tabbed layout | Panel switching |
| `mo.accordion` | Collapsible sections | Detail views |
| `mo.tree` | Tree structure | File hierarchy |
| `mo.carousel` | Slideshow | Gallery views |
| `mo.callout` | Highlighted box | Status messages |
| `mo.center` | Center alignment | Modal content |
| `mo.left` | Left alignment | Text alignment |
| `mo.right` | Right alignment | Action buttons |
| `mo.plain` | No styling | Raw output |
| `mo.stat` | Statistics display | Health metrics |
| `mo.routes` | Page routing | Multi-page apps |
| `mo.lazy` | Lazy loading | Heavy components |
| `mo.outline` | Table of contents | Navigation |
| `mo.json` | JSON viewer | API responses |

### 1.3 Media & Outputs

| Component | Description | Orchestr8 Use Case |
|-----------|-------------|-------------------|
| `mo.image` | Image display | File previews |
| `mo.audio` | Audio playback | Audio feedback |
| `mo.video` | Video display | Tutorial videos |
| `mo.pdf` | PDF viewer | Documentation |
| `mo.download` | Download button | Export data |
| `mo.plain_text` | Text output | Logs, output |
| `mo.md` | Markdown rendering | Rich text |
| `mo.html` | Raw HTML | Custom components |
| `mo.plotly` | Plotly charts | Data visualization |
| `mo.astream` | Async streaming | Live updates |

### 1.4 State & Reactivity

| Component | Description |
|-----------|-------------|
| `mo.state()` | Reactive state container |
| `mo.cache()` | Memoized computation |
| `mo.async()` | Async cell wrapper |
| `mo.lazy()` | Lazy evaluation |

---

## Part 2: Third-Party Integration (anywidget)

### 2.1 How Anywidget Works

```python
import marimo as mo
from some_widget import Widget

# Wrap anywidget-compatible widget
wrapped = mo.ui.anywidget(Widget())

# Access value reactively
wrapped.value  # Updates on interaction
```

### 2.2 Recommended Third-Party Widgets

| Widget | Stars | Use Case | Recommendation |
|--------|-------|----------|----------------|
| **jupyter-scatter** | 419 | 2D scatter/point clouds | **HIGH** - Could replace custom canvas for simple graphs |
| **drawdata** | 1.3k | Draw scatter plots | Medium - Interactive data entry |
| **lonboard** | 733 | Geospatial maps | Low - Not needed for Orchestr8 |
| **deck.gl** | - | WebGL maps | **HIGH** - Could power 3D Code City |
| **tldraw** | 258 | Whiteboard | Medium - Collaborative drawing |
| **wigglystuff** | 51 | Various widgets | Medium - UI components |
| **obsplot** | 226 | Observable Plot | Medium - Data viz |
| **ipymidi** | 14 | MIDI input | Low - Audio not priority |
| **Tweakpane** | 5 | Debug UI controls | **HIGH** - Parameter tuning panel |

---

## Part 3: Shortcut Recommendations for Orchestr8

### 3.1 What We Can REPLACE with Built-ins

| Current Implementation | Replace With | Effort |
|----------------------|--------------|--------|
| Custom slider controls | `mo.ui.slider`, `mo.ui.range_slider` | LOW |
| Custom buttons | `mo.ui.button` with `on_click` | LOW |
| Custom text input | `mo.ui.text`, `mo.ui.text_area` | LOW |
| Custom tabs | `mo.ui.tabs`, `mo.nav_menu` | LOW |
| Custom tables | `mo.ui.table`, `mo.ui.dataframe` | LOW |
| Custom dropdowns | `mo.ui.dropdown`, `mo.ui.multiselect` | LOW |
| Custom checkboxes | `mo.ui.checkbox`, `mo.ui.switch` | LOW |
| Custom forms | `mo.ui.form` + `mo.ui.batch` | LOW |
| Custom tree | `mo.ui.tree` | LOW |
| Custom callouts | `mo.callout` | LOW |
| Custom stat display | `mo.stat` | LOW |
| Custom layout | `mo.vstack`, `mo.hstack`, `mo.sidebar` | LOW |

### 3.2 What We Can REPLACE with Anywidget

| Component | Shortcut | Benefit |
|-----------|----------|---------|
| Parameter tuning panel | `ipytweakpane` | Debug controls |
| Graph visualization | `jupyter-scatter` or `py_cosmograph` | Replace manual canvas |
| 3D visualization | `deck.gl` (via `ipydeck`) | WebGL-powered 3D |
| Rich text editor | `ipyslides` components | Better editing |
| Data profiling | `quak` | Large file analysis |

### 3.3 What We MUST Keep Custom

| Component | Reason |
|-----------|--------|
| Code City canvas | Unique visualization not in anywidget |
| Woven Maps 3D | Custom emergence behavior |
| Louis lock overlay | Project-specific feature |
| Town Square rendering | Custom infrastructure layout |
| Neighborhood boundaries | Custom polygon rendering |

---

## Part 4: Implementation Roadmap

### Phase 1: Replace Native UI (HIGH ROI)

```python
# BEFORE: Custom HTML/CSS buttons
button = mo.Html("<button class='custom'>Run</button>")

# AFTER: Native marimo button
button = mo.ui.button("Run", on_click=run_action)
```

**Expected savings:** 60-70% reduction in UI boilerplate code

### Phase 2: Integrate Anywidget Libraries

```python
# Example: Use Tweakpane for debug controls
from ipytweakpane import Pane
pane = Pane()
pane.add_control('density', 0.5)
wrapped = mo.ui.anywidget(pane)
```

### Phase 3: Custom Canvas Optimization

Only keep custom canvas for Code City. Consider:
- `deck.gl` for 3D fallback
- `jupyter-scatter` for 2D fallback
- Shared styling with marimo CSS

---

## Part 5: Theming & Customization

### 5.1 CSS Variables (Stable API)

```css
:root {
  --marimo-monospace-font: 'JetBrains Mono', monospace;
  --marimo-text-font: 'Inter', sans-serif;
  --marimo-heading-font: 'Inter', sans-serif;
}
```

### 5.2 Custom CSS Loading

```python
# In App config
app = marimo.App(css_file="orchestr8.css")

# Or in pyproject.toml
[tool.marimo.display]
custom_css = ["orchestr8.css"]
```

### 5.3 Cell Targeting

```css
/* Target specific cells */
[data-cell-name='code_city'] { ... }
[data-cell-name='control_panel'] { ... }

/* Target outputs */
[data-cell-name='code_city'][data-cell-role='output'] { ... }
```

---

## Part 6: Key Findings Summary

### Built-in Components Cover:
- ✅ All basic input needs (buttons, sliders, text, dropdowns)
- ✅ All layout needs (stacks, sidebar, tabs, accordion)
- ✅ All data display (tables, dataframes, trees)
- ✅ Media (images, audio, video)
- ✅ State management (mo.state, mo.cache)

### Anywidget Covers:
- ✅ Complex visualizations (scatter, maps, graphs)
- ✅ Debug UI (Tweakpane)
- ✅ Specialized inputs (MIDI, drawing)

### Must Keep Custom:
- ❌ Code City unique visualization
- ❌ Emergence animations
- ❌ Louis lock overlay
- ❌ Town Square layout

---

## Recommendation

**Immediate action:** Refactor `IP/plugins/06_maestro.py` to use native marimo components instead of custom HTML. This will:
1. Reduce code by ~60%
2. Improve reactivity (native state management)
3. Better accessibility
4. Easier theming

**Future action:** Evaluate `deck.gl` or `jupyter-scatter` as optional fallback for simpler visualization needs.

---

*Research compiled from marimo documentation and anywidget community.*

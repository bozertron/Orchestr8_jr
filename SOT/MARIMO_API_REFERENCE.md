# Marimo API Reference & Compatibility Fixes

**Created:** 2026-01-30
**Source:** marimo source code at `/home/user/marimo-reference/` (cloned from <https://github.com/marimo-team/marimo.git>)
**Target Version:** marimo 0.19.6

---

## Part 1: Definitive API Reference

### Core Layout Functions (`mo.*`)

| Function | Signature | Notes |
|----------|-----------|-------|
| `mo.vstack()` | `(items, *, align=None, justify="start", gap=0.5, heights=None)` | **NO `style` param** |
| `mo.hstack()` | `(items, *, justify="space-between", align=None, wrap=False, gap=0.5, widths=None)` | **NO `style` param** |
| `mo.accordion()` | `(items: dict, multiple=False, lazy=False)` | Items is dict of name->content |
| `mo.callout()` | `(value, kind="neutral")` | kind: neutral/warn/success/info/danger |
| `mo.style()` | `(item, style=None, **kwargs)` | **Wrap element to add CSS** |
| `mo.tabs()` | `(tabs: dict)` | Dict of tab_name->content |
| `mo.md()` | `(text)` | Markdown |
| `mo.Html()` | `(text)` | Raw HTML |
| `mo.state()` | `(initial_value)` | Returns (getter, setter) tuple |
| `mo.mermaid()` | `(text)` | Mermaid diagrams |
| `mo.iframe()` | `(src, ...)` | Embed iframes |

### UI Components (`mo.ui.*`)

| Component | Key Parameters |
|-----------|---------------|
| `mo.ui.button()` | `on_click`, `value`, `kind`, `disabled`, `tooltip`, `label`, `on_change`, `full_width`, `keyboard_shortcut` |
| `mo.ui.text()` | `value`, `label`, `placeholder`, `full_width`, `on_change` |
| `mo.ui.text_area()` | `value`, `label`, `placeholder`, `full_width`, `on_change` |
| `mo.ui.dropdown()` | `options`, `value`, `label`, `on_change` |
| `mo.ui.slider()` | `start`, `stop`, `step`, `value`, `label`, `on_change` |
| `mo.ui.checkbox()` | `value`, `label`, `on_change` |
| `mo.ui.switch()` | `value`, `label`, `on_change` |
| `mo.ui.table()` | `data`, `selection`, `label`, `on_change` |
| `mo.ui.tabs()` | `tabs: dict` |
| `mo.ui.number()` | `start`, `stop`, `step`, `value`, `label`, `on_change` |
| `mo.ui.radio()` | `options`, `value`, `label`, `on_change` |
| `mo.ui.multiselect()` | `options`, `value`, `label`, `on_change` |
| `mo.ui.date()` | `value`, `label`, `on_change` |
| `mo.ui.file()` | `filetypes`, `multiple`, `label`, `on_change` |
| `mo.ui.code_editor()` | `value`, `language`, `label`, `on_change` |

### Status Components (`mo.status.*`)

| Component | Signature | Purpose |
|-----------|-----------|---------|
| `mo.status.progress_bar()` | `(collection, title, subtitle, total, show_rate, show_eta, ...)` | Progress iteration |
| `mo.status.spinner()` | `(title, subtitle, remove_on_exit)` | Loading indicator |
| `mo.status.toast()` | `(message, kind)` | Toast notifications |

### Button `kind` Values

| Kind | Color | Use Case |
|------|-------|----------|
| `"neutral"` | Default gray | Standard actions |
| `"success"` | Green | Confirmations, saves |
| `"warn"` | Yellow/Orange | Warnings |
| `"danger"` | Red | Destructive actions |

---

## Part 2: What DOESN'T Exist

| Wrong Pattern | Correct Alternative |
|---------------|---------------------|
| `mo.ui.progress()` | `mo.status.progress_bar()` |
| `mo.ui.accordion()` | `mo.accordion()` (not under ui) |
| `mo.vstack(..., style={})` | `mo.style(mo.vstack(...), ...)` |
| `mo.hstack(..., style={})` | `mo.style(mo.hstack(...), ...)` |
| `mo.ui.button(..., style={})` | Use `kind=` param or wrap with `mo.style()` |
| `mo.ui.vstack()` | `mo.vstack()` (not under ui) |
| `mo.ui.hstack()` | `mo.hstack()` (not under ui) |
| `mo.ui.card()` | `mo.callout()` or `mo.Html()` with styling |

---

## Part 3: How to Apply Styles Correctly

### Wrapping with `mo.style()`

```python
# WRONG - style param doesn't exist on vstack
mo.vstack([item1, item2], style={"flex": "1"})

# CORRECT - wrap with mo.style()
mo.style(
    mo.vstack([item1, item2]),
    flex="1",
    padding="1rem"
)

# Or use dict form
mo.style(
    mo.vstack([item1, item2]),
    style={"flex": "1", "padding": "1rem"}
)
```

### Button Styling

```python
# WRONG - style param doesn't exist
mo.ui.button(label="Delete", style={"background": "red"})

# CORRECT - use kind parameter for semantic colors
mo.ui.button(label="Delete", kind="danger")   # Red
mo.ui.button(label="Save", kind="success")    # Green
mo.ui.button(label="Warning", kind="warn")    # Yellow
mo.ui.button(label="Action", kind="neutral")  # Gray (default)

# For custom colors, wrap with mo.style()
mo.style(
    mo.ui.button(label="Custom"),
    background="rgba(212, 175, 55, 0.2)"
)
```

### Progress Bars

```python
# WRONG
progress_bar = mo.ui.progress(value=0.5, show_value=True)

# CORRECT - use mo.status.progress_bar() as context manager
with mo.status.progress_bar(total=100) as bar:
    for i in range(100):
        bar.update()

# Or for simple display, use HTML
mo.Html(f'<progress value="{current}" max="{total}"></progress>')

# Or use markdown
mo.md(f"Progress: {current}/{total} ({int(current/total*100)}%)")
```

### Accordion

```python
# WRONG
mo.ui.accordion({"Section 1": content1, "Section 2": content2})

# CORRECT - mo.accordion is at top level, not under ui
mo.accordion({"Section 1": content1, "Section 2": content2})

# With options
mo.accordion(
    {"Section 1": content1, "Section 2": content2},
    multiple=True,  # Allow multiple open
    lazy=True       # Lazy load content
)
```

---

## Part 4: Progress & Findings Log

### 2026-01-30: Initial Compatibility Audit

**Environment:**

- marimo 0.19.6
- Python 3.14.2
- Orchestr8 application

**Test Results:**

- Application launches but 6 of 9 plugins fail to render
- Root cause: Plugins use deprecated/non-existent marimo API patterns

**Files Requiring Fixes:**

| File | Line(s) | Issue | Fix |
|------|---------|-------|-----|
| `01_generator.py` | 61 | `mo.ui.progress()` doesn't exist | Remove or use `mo.md()` |
| `02_explorer.py` | 261-262 | `vstack(..., style=)` invalid | Remove style param |
| `05_universal_bridge.py` | 475, 483 | `mo.ui.accordion()` wrong namespace | Change to `mo.accordion()` |
| `07_settings.py` | 342, 589, 623 | `button(..., style=)` invalid | Use `kind=` param |
| `08_director.py` | 458 | `button(..., style=)` invalid | Use `kind=` param |
| `08_director.py` | import | Missing `director.adapter` module | Fix import path |

**Strategy Chosen:** Option A - Minimal fixes to get running, then iterate

---

## Part 5: Fix Implementation Record

### Fix 1: 01_generator.py

- **Line 61:** `mo.ui.progress(value=current_phase/7, show_value=True)`
- **Action:** Replaced with HTML progress element: `mo.Html(f'<progress value="{current_phase}" max="7"...')`
- **Status:** COMPLETED

### Fix 2: 02_explorer.py

- **Lines 261-262:** `mo.vstack([...], style={...})`
- **Action:** Removed `style` param, used `widths=[2, 1]` on parent hstack for flex layout
- **Status:** COMPLETED

### Fix 3: 05_universal_bridge.py

- **Lines 475, 483:** `mo.ui.accordion(...)`
- **Action:** Changed to `mo.accordion(...)` (correct namespace)
- **Status:** COMPLETED

### Fix 4: 07_settings.py

- **Lines 342, 589:** Tab buttons with `style` param
- **Action:** Removed `style` param, added `[label]` prefix for active state indication
- **Line 618:** Save button with `style` param
- **Action:** Replaced with `kind="success"` for green button
- **Status:** COMPLETED

### Fix 5: 08_director.py

- **Line 458:** `mo.ui.button(..., style={...})`
- **Action:** Replaced with `kind="success"` for green button
- **Import issue:** `director.adapter` import fails because 888 moved to staging
- **Note:** Already handled gracefully via try/except - sets `director_engine = None`
- **Status:** COMPLETED

---

## Part 6: References

- **Marimo Source:** `/home/user/marimo-reference/`
- **Key Files:**
  - `marimo/__init__.py` - Main exports
  - `marimo/_plugins/stateless/flex.py` - vstack/hstack implementation
  - `marimo/_plugins/ui/_impl/input.py` - button implementation
  - `marimo/_plugins/stateless/accordion.py` - accordion implementation
  - `marimo/_plugins/stateless/status/_progress.py` - progress_bar implementation
  - `marimo/_plugins/stateless/style.py` - style wrapper implementation

- **Working Reference:** `one integration at a time/orchestr8_standalone.py` (uses correct patterns)

# Complete Marimo API Reference

**Project:** Orchestr8
**Research Date:** 2026-02-13
**Purpose:** Complete reference of all marimo API categories

---

## Table of Contents

1. [Control Flow](#control-flow)
2. [Plotting](#plotting)
3. [Progress Bars & Status](#progress-bars--status)
4. [Outputs](#outputs)
5. [Diagrams](#diagrams)
6. [Query Parameters](#query-parameters)
7. [Caching](#caching)
8. [State](#state)
9. [App/Cell](#appcell)
10. [Watch](#watch)
11. [Miscellaneous](#miscellaneous)

---

## 1. Control Flow

| Function | Description | Orchestr8 Use |
|----------|-------------|---------------|
| `mo.stop(predicate, output)` | Halt cell execution conditionally | Form validation gates |
| `mo.Thread(target)` | Background threads with frontend comms | Async operations |
| `mo.current_thread()` | Get current thread context | Thread lifecycle |

### Example
```python
# Stop if form not submitted
mo.stop(form.value is None, mo.md("Submit the form to continue"))
```

---

## 2. Plotting

| Library | Function | Description |
|---------|----------|-------------|
| **Altair** | `mo.ui.altair_chart(chart)` | Reactive Altair charts with selection |
| **Plotly** | `mo.ui.plotly(fig)` | Reactive Plotly with selection |
| **Matplotlib** | `mo.mpl.interactive(fig)` | Interactive matplotlib viewer |
| **Leafmap** | - | Geospatial mapping (via anywidget) |

### Example
```python
chart = alt.Chart(data).mark_point().encode(x="x", y="y")
wrapped = mo.ui.altair_chart(chart)
# Select points → wrapped.value gives filtered dataframe
```

---

## 3. Progress Bars & Status

| Function | Description |
|----------|-------------|
| `mo.status.progress_bar(collection)` | Iterate with progress bar (like tqdm) |
| `mo.status.progress_bar(total=10)` | Manual progress with `.step()` |
| `mo.status.spinner(title)` | Loading spinner |

### Example
```python
for i in mo.status.progress_bar(range(10), title="Processing"):
    await asyncio.sleep(0.5)

with mo.status.spinner(title="Loading...") as s:
    data = fetch()
    s.update("Done")
```

---

## 4. Outputs

| Function | Description |
|----------|-------------|
| `mo.output.replace(value)` | Replace cell output |
| `mo.output.append(value)` | Append to cell output |
| `mo.output.clear()` | Clear cell output |
| `mo.output.replace_at_index(value, idx)` | Replace at index |
| `mo.show_code(output)` | Show code with output |
| `mo.redirect_stdout()` | Redirect print to output |
| `mo.redirect_stderr()` | Redirect errors to output |

---

## 5. Diagrams

| Function | Description |
|----------|-------------|
| `mo.mermaid(diagram)` | Render Mermaid diagrams |

### Example
```python
diagram = """
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
"""
mo.mermaid(diagram)
```

---

## 6. Query Parameters

| Function | Description |
|----------|-------------|
| `mo.query_params()` | Get/set URL query parameters |
| `QueryParams.set(key, value)` | Update parameter |
| `QueryParams.to_dict()` | Convert to dict |

### Example
```python
query = mo.query_params()
search = mo.ui.text(value=query.get("search", ""))
# Updates URL: ?search=value
```

---

## 7. Caching

| Function | Description | Persistence |
|---------|-------------|-------------|
| `mo.cache` | In-memory caching | Session only |
| `mo.lru_cache(maxsize=128)` | LRU cache with size limit | Session only |
| `mo.persistent_cache` | Disk-based caching | Across runs |

### Example
```python
@mo.cache
def expensive_computation(x):
    return heavy_calculation(x)

# Or context manager
with mo.persistent_cache("my_data") as cache:
    data = load_data()
```

---

## 8. State

| Function | Description |
|----------|-------------|
| `mo.state(initial_value)` | Create reactive state (getter/setter) |

**⚠️ Warning:** Only use when UI elements won't work. 99% of cases don't need this.

### Example
```python
get_val, set_val = mo.state(0)
# get_val() → 0
# set_val(5) → updates state
```

---

## 9. App/Cell

| Function | Description |
|----------|-------------|
| `@app.cell()` | Define cell in App mode |
| `marimo.App()` | Programmatic app builder |
| `app.run()` | Run the app |

---

## 10. Watch

| Function | Description |
|----------|-------------|
| `mo.watch.file(path)` | Watch file for changes |
| `mo.watch.function(func)` | Watch function changes |

---

## 11. Miscellaneous

| Function | Description |
|----------|-------------|
| `mo.md(text)` | Markdown rendering |
| `mo.html(html)` | Raw HTML output |
| `mo.inspect(obj)` | Object inspection |

---

## Quick Reference Card

```
# Inputs (30+ components)
mo.ui.button, slider, text, dropdown, table, dataframe, tabs, form, ...

# Layouts
mo.vstack, mo.hstack, mo.sidebar, mo.tabs, mo.accordion, mo.tree, ...

# Control Flow
mo.stop(), mo.Thread, mo.current_thread()

# Plotting
mo.ui.altair_chart(), mo.ui.plotly(), mo.mpl.interactive()

# Status
mo.status.progress_bar(), mo.status.spinner()

# Outputs
mo.output.replace(), mo.output.append(), mo.redirect_stdout()

# Diagrams
mo.mermaid()

# Query Params
mo.query_params()

# Caching
@mo.cache, @mo.persistent_cache, @mo.lru_cache

# State (use sparingly)
mo.state()

# Media
mo.image, mo.audio, mo.video, mo.pdf, mo.download

# Theming
app = marimo.App(css_file="theme.css")
```

---

## Orchestr8 Implementation Recommendations

| Need | Use This |
|------|----------|
| Control panel buttons | `mo.ui.button(on_click=...)` |
| Sliders/inputs | `mo.ui.slider`, `mo.ui.text` |
| Progress for scans | `mo.status.progress_bar()` |
| Status spinners | `mo.status.spinner()` |
| Show code in app | `mo.show_code()` |
| Caching expensive ops | `@mo.persistent_cache` |
| URL state sharing | `mo.query_params()` |
| Flow diagrams | `mo.mermaid()` |
| Charts | `mo.ui.altair_chart()` |
| Layout | `mo.vstack`, `mo.hstack`, `mo.sidebar` |

---

*Research compiled from https://docs.marimo.io/api/*

# IP--orchestr8_app.py Integration Guide

- Source: `one integration at a time/IP--orchestr8_app.py`
- Total lines: `251`
- SHA256: `29492d61e13b0a436c60b1d319c894be51edfaa03ca7f46c58e00e8e2c34daf4`
- Memory chunks: `3`
- Observation IDs: `657..659`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `one integration at a time/IP--orchestr8_app.py:7` marimo run IP/orchestr8_app.py
- `one integration at a time/IP--orchestr8_app.py:8` marimo edit IP/orchestr8_app.py
- `one integration at a time/IP--orchestr8_app.py:53` STATE_MANAGERS Pattern:
- `one integration at a time/IP--orchestr8_app.py:55` Plugins receive STATE_MANAGERS dict and can read/write state reactively.
- `one integration at a time/IP--orchestr8_app.py:64` STATE_MANAGERS = {
- `one integration at a time/IP--orchestr8_app.py:72` STATE_MANAGERS,
- `one integration at a time/IP--orchestr8_app.py:92` Valid plugins must have:
- `one integration at a time/IP--orchestr8_app.py:95` - render(STATE_MANAGERS): function returning mo.Html or mo.md
- `one integration at a time/IP--orchestr8_app.py:145` def plugin_renderer(STATE_MANAGERS, load_plugins, mo):
- `one integration at a time/IP--orchestr8_app.py:156` # Render plugin, injecting STATE_MANAGERS
- `one integration at a time/IP--orchestr8_app.py:157` rendered = p["module"].render(STATE_MANAGERS)
- `one integration at a time/IP--orchestr8_app.py:221` def render(STATE_MANAGERS):
- `one integration at a time/IP--orchestr8_app.py:223` get_root, set_root = STATE_MANAGERS["root"]

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

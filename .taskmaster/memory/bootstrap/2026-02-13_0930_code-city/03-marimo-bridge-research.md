# Marimo JS to Python Bridge Research

## Current event flow

1. Code City JS posts message event.
2. Browser receives and dispatches node-click custom event.
3. Flow currently dead-ends before Python callback path.

## Viable bridge options

- Option A: anywidget trait-based bridge (strong architecture, higher setup cost).
- Option B: hidden `mo.ui.text` bridge + `on_change` callback (fastest practical bridge now).

## Implementation recommendation

- Keep deterministic payload contract (`CodeCityNodeEvent`).
- Serialize in JS, parse/validate in Python.
- Route validated payload into `handle_node_click()`.
- Add focused tests for bridge parse/dispatch path.

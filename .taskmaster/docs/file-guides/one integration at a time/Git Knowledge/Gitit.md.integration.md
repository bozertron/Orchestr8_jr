# Gitit.md Integration Guide

- Source: `one integration at a time/Git Knowledge/Gitit.md`
- Total lines: `800`
- SHA256: `d9d2d7e03c6ac6f1bf13ee95250cca63c83e87f3cc279e48daaab67c26331aad`
- Memory chunks: `7`
- Observation IDs: `639..645`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `one integration at a time/Git Knowledge/Gitit.md:31` │   ├── orchestr8_app.py         # Main Marimo application
- `one integration at a time/Git Knowledge/Gitit.md:32` │   ├── carl_core.py             # TypeScript bridge
- `one integration at a time/Git Knowledge/Gitit.md:41` │       └── 05_cli_bridge.py
- `one integration at a time/Git Knowledge/Gitit.md:60` ├── orchestr8.py                 # v1.0 MVP (preserved)
- `one integration at a time/Git Knowledge/Gitit.md:138` | `feat` | New feature | `feat(plugins): add CLI bridge plugin` |
- `one integration at a time/Git Knowledge/Gitit.md:188` BREAKING CHANGE: render() now requires STATE_MANAGERS parameter"
- `one integration at a time/Git Knowledge/Gitit.md:668` git commit -m "feat(plugins): implement CLI bridge
- `one integration at a time/Git Knowledge/Gitit.md:690` marimo edit IP/orchestr8_app.py
- `one integration at a time/Git Knowledge/Gitit.md:697` git add IP/orchestr8_app.py
- `one integration at a time/Git Knowledge/Gitit.md:737` marimo edit IP/orchestr8_app.py
- `one integration at a time/Git Knowledge/Gitit.md:740` python -m py_compile IP/orchestr8_app.py

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

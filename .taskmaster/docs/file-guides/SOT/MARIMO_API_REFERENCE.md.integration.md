# MARIMO_API_REFERENCE.md Integration Guide

- Source: `SOT/MARIMO_API_REFERENCE.md`
- Total lines: `238`
- SHA256: `08985aebdc22b104c23d042f4ab1f1823196f5e22cca6274c3eeca6c66466dbc`
- Memory chunks: `2`
- Observation IDs: `137..138`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `SOT/MARIMO_API_REFERENCE.md:180` | `05_universal_bridge.py` | 475, 483 | `mo.ui.accordion()` wrong namespace | Change to `mo.accordion()` |
- `SOT/MARIMO_API_REFERENCE.md:203` ### Fix 3: 05_universal_bridge.py
- `SOT/MARIMO_API_REFERENCE.md:238` - **Working Reference:** `one integration at a time/orchestr8_standalone.py` (uses correct patterns)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

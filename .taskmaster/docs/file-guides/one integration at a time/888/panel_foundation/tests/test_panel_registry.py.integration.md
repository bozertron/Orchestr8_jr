# test_panel_registry.py Integration Guide

- Source: `one integration at a time/888/panel_foundation/tests/test_panel_registry.py`
- Total lines: `383`
- SHA256: `2f42a2bd907c12678de1b3de8d13c73f827ef41630d62b727925c042c0fcd671`
- Memory chunks: `4`
- Observation IDs: `274..277`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/888/panel_foundation/tests/test_panel_registry.py:352` # Test orchestr8 defaults
- `one integration at a time/888/panel_foundation/tests/test_panel_registry.py:353` caps = registry._get_default_capabilities("orchestr8")

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

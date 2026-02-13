# ooda_engine.py Integration Guide

- Source: `one integration at a time/888/director/ooda_engine.py`
- Total lines: `506`
- SHA256: `f2a5c8e8a397f4bd1f473be8d7ff0f4c46326b95e56af2ec48271b30ca589303`
- Memory chunks: `5`
- Observation IDs: `222..226`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/888/director/ooda_engine.py:135` Best suggestion object if one should be made, None otherwise
- `one integration at a time/888/director/ooda_engine.py:137` if not context.should_show_suggestion():
- `one integration at a time/888/director/ooda_engine.py:388` if len(recent_zones) == 1 and context.current_zone == 'orchestr8':

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

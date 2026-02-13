# test_ooda_engine.py Integration Guide

- Source: `one integration at a time/888/director/tests/test_ooda_engine.py`
- Total lines: `288`
- SHA256: `a2d8233984797123e353a7346e2dadba93ed8d8bdf1bf191cde83351b49aa5d9`
- Memory chunks: `3`
- Observation IDs: `241..243`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/888/director/tests/test_ooda_engine.py:34` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_ooda_engine.py:54` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_ooda_engine.py:57` 'app_context': 'maestro'
- `one integration at a time/888/director/tests/test_ooda_engine.py:82` """Test the Decide phase when no suggestion should be made."""
- `one integration at a time/888/director/tests/test_ooda_engine.py:84` # Set conditions where no suggestion should be made
- `one integration at a time/888/director/tests/test_ooda_engine.py:184` context.tool_usage_patterns['orchestr8:chat'] = 3
- `one integration at a time/888/director/tests/test_ooda_engine.py:220` 'orchestr8:chat': 10,
- `one integration at a time/888/director/tests/test_ooda_engine.py:222` 'orchestr8:settings': 2
- `one integration at a time/888/director/tests/test_ooda_engine.py:231` self.assertEqual(context.productivity_metrics['most_used_tool'], 'orchestr8:chat')
- `one integration at a time/888/director/tests/test_ooda_engine.py:260` 'app_context': 'orchestr8'

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# test_adapter.py Integration Guide

- Source: `one integration at a time/888/director/tests/test_adapter.py`
- Total lines: `358`
- SHA256: `c0f82082beb05d45e7ca023df972999b1c88f7dc5968e61841f66e433a798bd6`
- Memory chunks: `3`
- Observation IDs: `238..240`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/888/director/tests/test_adapter.py:43` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_adapter.py:51` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_adapter.py:54` 'app_context': 'maestro'
- `one integration at a time/888/director/tests/test_adapter.py:74` """Test getting suggestion when none should be provided."""
- `one integration at a time/888/director/tests/test_adapter.py:75` # Fresh context should not provide suggestions immediately
- `one integration at a time/888/director/tests/test_adapter.py:87` # Note: This test may not always produce a suggestion due to timing constraints
- `one integration at a time/888/director/tests/test_adapter.py:95` 'last_app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_adapter.py:138` """Test recording feedback with invalid rating (should be clamped)."""
- `one integration at a time/888/director/tests/test_adapter.py:141` # Test high rating (should be clamped to 1)
- `one integration at a time/888/director/tests/test_adapter.py:148` # Test low rating (should be clamped to -1)
- `one integration at a time/888/director/tests/test_adapter.py:166` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_adapter.py:174` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_adapter.py:177` 'app_context': 'maestro'
- `one integration at a time/888/director/tests/test_adapter.py:250` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_adapter.py:275` self.assertEqual(context_after.current_zone, "orchestr8")  # Default value
- `one integration at a time/888/director/tests/test_adapter.py:282` 'invalid_structure': 'this should cause an error'
- `one integration at a time/888/director/tests/test_adapter.py:289` # The adapter should handle this gracefully and not crash
- `one integration at a time/888/director/tests/test_adapter.py:291` # May succeed or fail depending on error handling, but should not crash
- `one integration at a time/888/director/tests/test_adapter.py:301` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_adapter.py:304` 'app_context': 'maestro'

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

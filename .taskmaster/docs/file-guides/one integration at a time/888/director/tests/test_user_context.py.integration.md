# test_user_context.py Integration Guide

- Source: `one integration at a time/888/director/tests/test_user_context.py`
- Total lines: `287`
- SHA256: `020512dcdffb01b43d4fcd87f76bd5d2b4a46fffec449c528dfb12331e3a63e8`
- Memory chunks: `3`
- Observation IDs: `244..246`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/888/director/tests/test_user_context.py:18` self.assertEqual(self.context.current_zone, "orchestr8")
- `one integration at a time/888/director/tests/test_user_context.py:30` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_user_context.py:33` 'app_context': 'maestro'
- `one integration at a time/888/director/tests/test_user_context.py:42` self.assertEqual(self.context.zone_transitions[0]['from_zone'], 'orchestr8')
- `one integration at a time/888/director/tests/test_user_context.py:54` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_user_context.py:61` self.assertEqual(self.context.active_tools['orchestr8'], 'chat_interface')
- `one integration at a time/888/director/tests/test_user_context.py:62` self.assertEqual(self.context.tool_usage_patterns['orchestr8:chat_interface'], 1)
- `one integration at a time/888/director/tests/test_user_context.py:91` 'last_app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_user_context.py:109` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_user_context.py:130` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_user_context.py:141` 'app_context': 'orchestr8'
- `one integration at a time/888/director/tests/test_user_context.py:162` 'from_zone': 'orchestr8',
- `one integration at a time/888/director/tests/test_user_context.py:165` 'app_context': 'maestro'
- `one integration at a time/888/director/tests/test_user_context.py:209` def test_should_show_suggestion(self):
- `one integration at a time/888/director/tests/test_user_context.py:211` # Initially should not show (too recent)
- `one integration at a time/888/director/tests/test_user_context.py:212` self.assertFalse(self.context.should_show_suggestion())
- `one integration at a time/888/director/tests/test_user_context.py:221` self.assertTrue(self.context.should_show_suggestion())
- `one integration at a time/888/director/tests/test_user_context.py:227` self.assertFalse(self.context.should_show_suggestion())
- `one integration at a time/888/director/tests/test_user_context.py:233` self.assertFalse(self.context.should_show_suggestion())
- `one integration at a time/888/director/tests/test_user_context.py:239` self.assertTrue(self.context.should_show_suggestion())
- `one integration at a time/888/director/tests/test_user_context.py:274` 'app_context': 'maestro'

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

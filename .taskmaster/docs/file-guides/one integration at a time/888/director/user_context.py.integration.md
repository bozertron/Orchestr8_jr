# user_context.py Integration Guide

- Source: `one integration at a time/888/director/user_context.py`
- Total lines: `266`
- SHA256: `871b2be909318660085995f693059267c2ef7daf9603b7b8cb351887282735aa`
- Memory chunks: `3`
- Observation IDs: `247..249`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/888/director/user_context.py:5` across all wrapped applications (orchestr8, integr8, etc.) for behavioral analysis.
- `one integration at a time/888/director/user_context.py:23` current_zone: str = "orchestr8"  # Current active application zone
- `one integration at a time/888/director/user_context.py:245` def should_show_suggestion(self) -> bool:
- `one integration at a time/888/director/user_context.py:250` True if a suggestion should be shown, False otherwise

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

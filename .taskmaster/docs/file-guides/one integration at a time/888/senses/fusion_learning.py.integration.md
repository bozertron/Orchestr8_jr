# fusion_learning.py Integration Guide

- Source: `one integration at a time/888/senses/fusion_learning.py`
- Total lines: `1062`
- SHA256: `219a566a05a693bd7d2beace5595b6c8d9eaeeba40679e9cc73e7576cb33bc77`
- Memory chunks: `9`
- Observation IDs: `305..313`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.

## Anchor Lines

- `one integration at a time/888/senses/fusion_learning.py:90` 'current_panel': 'orchestr8',
- `one integration at a time/888/senses/fusion_learning.py:103` current_panel = context.get('current_panel', 'orchestr8')
- `one integration at a time/888/senses/fusion_learning.py:939` current_panel = context.get('current_panel', 'orchestr8')
- `one integration at a time/888/senses/fusion_learning.py:942` if current_panel == 'orchestr8':
- `one integration at a time/888/senses/fusion_learning.py:978` current_panel = context.get('current_panel', 'orchestr8')
- `one integration at a time/888/senses/fusion_learning.py:982` 'orchestr8': ['library_navigation', 'conversation_start', 'ai_assistance'],

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

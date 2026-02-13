# base_metric.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/metrics/base_metric.py`
- Total lines: `51`
- SHA256: `cd0239f617349c452b9bbae9e159d930309660cf062bba353ba967776d3b69aa`
- Memory chunks: `1`
- Observation IDs: `898..898`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/star-vector/starvector/metrics/base_metric.py:45` This method should be overridden by subclasses to provide the specific metric computation.
- `one integration at a time/star-vector/starvector/metrics/base_metric.py:47` raise NotImplementedError("The metric method must be implemented by subclasses.")

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

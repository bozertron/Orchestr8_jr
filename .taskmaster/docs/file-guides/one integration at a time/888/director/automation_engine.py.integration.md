# automation_engine.py Integration Guide

- Source: `one integration at a time/888/director/automation_engine.py`
- Total lines: `511`
- SHA256: `647133eaf91ee611f0f01bb1e8af55537afba390de9e93f7dceee4b1f0860c55`
- Memory chunks: `5`
- Observation IDs: `216..220`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/888/director/automation_engine.py:111` # Check if rule should be triggered
- `one integration at a time/888/director/automation_engine.py:112` should_trigger, trigger_confidence = self._evaluate_trigger(rule.trigger, context, patterns, insights)
- `one integration at a time/888/director/automation_engine.py:114` if should_trigger and trigger_confidence >= self.thresholds['min_trigger_confidence']:
- `one integration at a time/888/director/automation_engine.py:252` """Evaluate if a trigger should fire based on current context."""

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

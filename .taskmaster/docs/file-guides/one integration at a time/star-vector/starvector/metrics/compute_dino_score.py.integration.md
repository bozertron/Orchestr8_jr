# compute_dino_score.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/metrics/compute_dino_score.py`
- Total lines: `55`
- SHA256: `47a7c27ba0b3dbdf085fbdef38a7da12a80c6f8f3838673b407a37d4ad8e1c25`
- Memory chunks: `1`
- Observation IDs: `900..900`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/star-vector/starvector/metrics/compute_dino_score.py:28` raise ValueError(f"model_size should be either 'small', 'base' or 'large', got {model_size}")
- `one integration at a time/star-vector/starvector/metrics/compute_dino_score.py:42` raise ValueError("Input must be a file path, PIL Image, or tensor of features")

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

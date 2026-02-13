# inception.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/metrics/inception.py`
- Total lines: `341`
- SHA256: `e22c79ac902cb43d75f4ec4bad8b8b63cc401be7bd4c781340faa1ecb92ce4dc`
- Memory chunks: `3`
- Observation IDs: `907..909`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/star-vector/starvector/metrics/inception.py:50` layers is fully convolutional, it should be able to handle inputs

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

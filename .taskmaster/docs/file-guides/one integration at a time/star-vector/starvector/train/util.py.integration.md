# util.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/train/util.py`
- Total lines: `285`
- SHA256: `1462e31b99e3b45b3869467a52c4ada13e70557877bfea77d54cdef26fad3ca1`
- Memory chunks: `3`
- Observation IDs: `982..984`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/star-vector/starvector/train/util.py:77` model.tie_weights()  # This method should tie the weights internally

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

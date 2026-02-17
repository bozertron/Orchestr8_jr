# zero_to_fp32.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/train/zero_to_fp32.py`
- Total lines: `592`
- SHA256: `81f53f3ce7fb314d2075cae5cf3bc94742f0c994954f1437b327747cf3599a2b`
- Memory chunks: `5`
- Observation IDs: `985..989`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.

## Anchor Lines

- `one integration at a time/star-vector/starvector/train/zero_to_fp32.py:65` # there should be only one file

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

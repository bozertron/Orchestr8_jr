# base.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/data/base.py`
- Total lines: `71`
- SHA256: `7b9e081c96531290f9f3592925a052d858cf7780c92f10c93bf577dfca089d92`
- Memory chunks: `1`
- Observation IDs: `886..886`

## Why This Is Painful

- General integration risk: enforce tests around schema, state, and behavior contracts.

## Anchor Lines

- `one integration at a time/star-vector/starvector/data/base.py:71` raise NotImplementedError("This method should be implemented by subclasses")

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

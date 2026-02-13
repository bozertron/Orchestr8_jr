# modeling_gpt_bigcode.py Integration Guide

- Source: `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py`
- Total lines: `1502`
- SHA256: `509f8434b07e74a29e365ce6e57654f5c9798fb4864f306342d9e3689ddc18fe`
- Memory chunks: `13`
- Observation IDs: `918..930`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py:117` f"`embed_dim` must be divisible by num_heads (got `embed_dim`: {self.embed_dim} and `num_heads`:"
- `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py:826` If `past_key_values` is used, only `input_ids` that do not have their past calculated should be passed as
- `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py:836` their past given to this model should not be passed as `input_ids` as they have already been computed.
- `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py:1337` Labels for computing the sequence classification/regression loss. Indices should be in `[0, ...,
- `one integration at a time/star-vector/starvector/model/gpt_bigcode/modeling_gpt_bigcode.py:1464` Labels for computing the sequence classification/regression loss. Indices should be in `[0, ...,

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

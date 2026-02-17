# graph_builder.py Integration Guide

- Source: `IP/features/code_city/graph_builder.py`
- Total lines: `371`
- SHA256: `21440fc5c427d7c56e5a19f09121df9673f71d9428f387d78f16dbeae7d48dbb`
- Role: **Code City graph assembly layer** — builds nodes/edges/neighborhoods and merges health/combat overlays into render-ready graph data

## Why This Is Painful

- Must bridge multiple upstream providers (connection verifier, combat tracker, health signals).
- Status precedence correctness is critical to visual truth in Code City.
- Health payload format can vary (dataclass objects vs serialized dict payloads).

## Anchor Lines

- `IP/features/code_city/graph_builder.py:12` `compute_neighborhoods(...)`
- `IP/features/code_city/graph_builder.py:169` `build_from_connection_graph(...)`
- `IP/features/code_city/graph_builder.py:332` `build_from_health_results(...)`
- `IP/features/code_city/graph_builder.py:334` `_status_of(...)` payload normalization
- `IP/features/code_city/graph_builder.py:346` `_to_error_dict(...)` error mapping

## Integration Use

- Neighborhood grouping derives from parent directories and drives boundary overlays.
- Health merge now accepts both object and dict result payloads.
- Combat precedence remains canonical through `merge_status(...)`.

## Open Gaps

- [ ] Live performance baselines for large graph merges are not captured yet


# Autonomy Boundary: P07-B6 (a_codex_plan)

## Objective

Integrate accepted C5 extraction concepts into core services and advance pre-wired data-UI surface behavior without direct UI-placement decisions.

## Allowed Work

- Integrate C5 concept outputs into temporal/tour/conversation service flow.
- Add/extend integration tests for C5-driven behaviors.
- Deliver smoke report with exact commands/pass counts.

## Must Not Do

- Final visual UI placement/theming.
- Direct code lift from non-canonical sources.
- Packaging/compliance scope.

## Required Evidence

- `orchestr8_next/city/temporal_state.py`
- `orchestr8_next/city/tour_service.py`
- `orchestr8_next/city/agent_conversation.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B6_INTEGRATION_SMOKE_REPORT.md`

## Required Validation

```bash
pytest tests/integration/test_temporal_state.py tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
```

## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16

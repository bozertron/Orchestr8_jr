# Autonomy Boundary: P07-B4 (a_codex_plan)

## Objective

Implement clean-room UX service integrations based on accepted C3 extraction packets (MaestroWizard + WizardConversation) for Orchestr8/Code City core runtime.

## Allowed Work

- Implement non-visual service-layer logic for guided tours and agent conversation streams.
- Wire contracts/events into `orchestr8_next` city/runtime pathways.
- Add integration tests and smoke evidence.
- Deliver canonical report with exact commands/pass counts.

## Must Not Do

- Final visual placement/theming decisions in canonical UI files.
- Direct code lift from 2ndFid sources.
- Packaging/compliance scope.

## Required Evidence

- `orchestr8_next/city/tour_service.py`
- `orchestr8_next/city/agent_conversation.py`
- `tests/integration/test_city_tour_service.py`
- `tests/integration/test_agent_conversation.py`
- `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B4_INTEGRATION_SMOKE_REPORT.md`
- Canonical delivery proof (`cp` + `ls -l`).

## Required Validation

```bash
pytest tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -vv
```

## Unlock Authority

- Unlocked by: Codex (P07 orchestration)
- Effective: 2026-02-16

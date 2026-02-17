# a_codex_plan TODO (P07/P07-B7)

Date: 2026-02-16
Mode: Long-run

## Objective

Ship Phreak/CSE foundation with settings-driven behavior and stable integration tests.

## Scope

Core integration packet: SettingsService + Phreak token wiring

## Task Queue

| ID | Task | Depends On | Status | Required Evidence |
|---|---|---|---|---|
| 1 | Implement SettingsService and schema validation layer | none | ready | /home/bozertron/a_codex_plan/orchestr8_next/settings/service.py |
| 2 | Wire core service settings consumption and command-surface mapping | 1 | ready | /home/bozertron/a_codex_plan/orchestr8_next/settings/schema.py |
| 3 | Run integration plus settings tests and publish canonical smoke report | 2 | ready | /home/bozertron/a_codex_plan/orchestr8_next/city/command_surface.py |

## Validation

```bash
pytest tests/integration/test_temporal_state.py tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
pytest tests/integration/test_settings_service.py -q
```

## Ambiguity Log (No Assumptions)

Rules:
1. Add ambiguity line item.
2. Probe local facts once.
3. Probe cross-codebase facts once.
4. If still unresolved: `deferred_due_to_missing_facts` and continue.

| Item | Ambiguity | Probe 1 | Probe 2 | Outcome |
|---|---|---|---|---|
| 1 | none logged | n/a | n/a | n/a |

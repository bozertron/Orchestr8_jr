# Autonomy Boundary: P07-B7 (a_codex_plan)

## Objective

Ship Phreak/CSE foundation with settings-driven behavior and stable integration tests.

## Scope

Core integration packet: SettingsService + Phreak token wiring

## Allowed Work

- Implement SettingsService for pyproject_orchestr8_settings.toml
- Wire settings read-path into core city services and command surface
- Apply Phreak visual token defaults where non-canonical lane is allowed
- Deliver deterministic smoke report with command transcript

## Must Not Do

- Final canonical UI placement decisions
- Unbounded aesthetic rewrites outside packet scope
- Skip settings validation and persistence tests

## Required Evidence

- /home/bozertron/a_codex_plan/orchestr8_next/settings/service.py
- /home/bozertron/a_codex_plan/orchestr8_next/settings/schema.py
- /home/bozertron/a_codex_plan/orchestr8_next/city/command_surface.py
- /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B7_INTEGRATION_SMOKE_REPORT.md

## Required Validation

```bash
pytest tests/integration/test_temporal_state.py tests/integration/test_city_tour_service.py tests/integration/test_agent_conversation.py -q
pytest tests/integration/test_settings_service.py -q
```
## Unlock Authority

- Unlocked by: Codex
- Effective: 2026-02-16

# Autonomy Boundary: P07-B3 (a_codex_plan)

## Objective

Implement the next core integration slice using accepted C2 extractions (automation + infrastructure telemetry), keeping marimo-first runtime compliance.

## Allowed Work

- Implement clean-room core services derived from accepted C2 packets.
- Wire services into canonical city runtime contracts and bridge pathways.
- Add integration tests and smoke evidence.
- Update canonical report artifacts and packet status evidence.

## Must Not Do

- Make final visual placement decisions in canonical UI surfaces.
- Modify frozen files under `IP/*` unless explicitly unlocked.
- Start packaging/distribution scope.
- Skip canonical delivery proof.

## Required Evidence

- `orchestr8_next/city/automation.py` (new/updated)
- `orchestr8_next/city/power_grid.py` (new/updated)
- `tests/integration/test_city_automation.py`
- `tests/integration/test_city_power_grid.py`
- `.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md`
- Exact validation command + pass counts.
- Canonical destination delivery proof:
  - `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/B3_INTEGRATION_SMOKE_REPORT.md`

## Required Validation

```bash
pytest tests/integration/test_city_automation.py tests/integration/test_city_power_grid.py -vv
```

## Unlock Authority

- Unlocked by: Codex (P07 orchestration)
- Effective: 2026-02-16

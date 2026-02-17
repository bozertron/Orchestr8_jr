# PRD P04: Code City Value Layer Re-Integration

## Phase

- ID: `P04`
- Name: Code City Value Layer Re-Integration
- Goal: Reconnect Code City to orchestr8_next through strict contracts while preserving 3D signature behavior.

## In Scope

- Code City scene contract (`CodeCitySceneModel`)
- Event bridge contract (`CodeCityEvent`)
- Building panel and connection action pipelines
- Optional 2D wiring lane feasibility hook

## Out of Scope

- Rewriting Code City renderer engine from scratch
- Replacing 3D scene with generic charting library

## Functional Requirements

- FR-04-01: City view switches cleanly from shell modes.
- FR-04-02: Node click events update selection/panels deterministically.
- FR-04-03: Connection actions route through adapter policy.
- FR-04-04: Building panel contract validation enforced.
- FR-04-05: Camera state can be observed (not owned) by shell.

## Performance Requirements

- PR-04-01: Mode switch to City under target threshold.
- PR-04-02: No shell lockup during scene initialization.
- PR-04-03: Event bridge handles burst clicks without drops.

## Files (Target)

- `orchestr8_next/city/contracts.py`
- `orchestr8_next/city/bridge.py`
- `orchestr8_next/city/panel_model.py`
- `orchestr8_next/city/connection_actions.py`
- `IP/woven_maps.py` (compat wrappers only as needed)
- `IP/static/woven_maps_3d.js` (contract-aligned event bridge updates)

## Acceptance Criteria

1. City mode initializes and renders from orchestr8_next.
2. Node and connection actions pass validated contracts.
3. Shell remains stable if city renderer errors.
4. Patchbay dry-run/apply pathways remain policy-guarded.

## Test Plan

- Contract validation tests for node/panel/connection payloads
- Event bridge integration tests
- Render init fallback tests (degraded mode)

## Risks

- R-04-01: Contract drift between JS bridge and Python handlers.
- R-04-02: Renderer assumptions about legacy state fields.

## Mitigations

- M-04-01: versioned event payload contract
- M-04-02: compatibility wrapper layer with deprecation logs

## Exit Gate `G-P04`

Required evidence:
- City integration test report
- Event contract conformance report
- Performance baseline capture


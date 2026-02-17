# PRD P01: Core Shell + Lower Fifth + Action Bus

## Phase

- ID: `P01`
- Name: Core Shell + Lower Fifth + Action Bus
- Goal: Deliver a deterministic shell where all 12 lower-fifth controls function through typed actions.

## Background

The lower fifth is the visual and operational contract. Reliability starts by removing direct, ad-hoc wiring and routing every interaction through a unified action pipeline.

## In Scope

- New runtime lane scaffold (`orchestr8_next` app shell)
- Locked lower-fifth control layout and interaction map
- Typed `UIAction` schema
- Action bus and reducer/store primitives
- Basic placeholder center-pane modes (`chat`, `matrix`, `city`)

## Out of Scope

- Full provider integrations
- Legacy plugin parity beyond lower fifth
- Code City 3D reconnect (handled in P04)

## UI Contract (Locked)

Control rhythm: `5 | 1 | 6`

Left cluster (5):

1. Apps
2. Matrix
3. Calendar*
4. Comms*
5. Files

Center cluster (1):

1. Flagship button (`maestro`) + state indicator

Right cluster (6):

1. Search
2. Record
3. Playback
4. Phreak>
5. Send
6. Attach

## Functional Requirements

- FR-01-01: All 12 controls dispatch typed actions.
- FR-01-02: Text area input is fully state-driven and debounced by contract.
- FR-01-03: `maestro` state cycle supports `ON -> OFF -> OBSERVE -> ON`.
- FR-01-04: Placeholder action handlers produce deterministic logs/events.
- FR-01-05: No control directly calls external services.

## Technical Requirements

- TR-01-01: `UIAction` envelope includes `id`, `type`, `timestamp`, `payload`.
- TR-01-02: Reducer transitions are pure and testable.
- TR-01-03: Action bus supports middleware hooks for tracing.
- TR-01-04: Feature flags control route to legacy or new shell.

## Files (Target)

- `orchestr8_next/app.py`
- `orchestr8_next/shell/layout.py`
- `orchestr8_next/shell/actions.py`
- `orchestr8_next/shell/reducer.py`
- `orchestr8_next/shell/store.py`
- `orchestr8_next/shell/selectors.py`
- `orchestr8_next/shell/contracts.py`

## Workstreams

1. Shell layout implementation
2. Action model implementation
3. Reducer/store implementation
4. Event tracing and diagnostics
5. Control behavior tests

## Acceptance Criteria

1. All 12 controls render in locked positions.
2. Every control emits expected action type.
3. No runtime exceptions from any control path.
4. Action trace log captures full event lifecycle.
5. Unit tests validate reducer behavior for all control actions.

## Test Plan

- Reducer table tests for each action type
- Smoke test for complete control sweep
- Snapshot test for shell layout consistency

## Risks

- R-01-01: Layout drift from visual contract.
- R-01-02: Hidden direct service calls from handlers.

## Mitigations

- M-01-01: Snapshot lock on control row.
- M-01-02: Code review rule: handlers only dispatch actions.

## Exit Gate `G-P01`

Required evidence:

- Control sweep report
- Action trace sample
- Reducer test results
- UI contract screenshot set

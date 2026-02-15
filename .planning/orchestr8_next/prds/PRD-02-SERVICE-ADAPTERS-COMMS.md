# PRD P02: Service Adapters + Comms Bridge

## Phase

- ID: `P02`
- Name: Service Adapters + Comms Bridge
- Goal: Implement adapter interfaces and resilient comms so core runtime remains deterministic while integrations become pluggable.

## In Scope

- Adapter interface contracts
- Adapter registry and capability matrix
- Comms bridge for async request/response/event streams
- Failure isolation and degraded mode behavior
- Telemetry hooks per adapter

## Out of Scope

- Full capability bridge implementation (P05)
- Full Code City 3D integration (P04)

## Adapter Set

Required adapters:
1. `LLMAdapter`
2. `MemoryAdapter`
3. `WorkspaceAdapter`
4. `IDEAdapter`
5. `AudioAdapter`
6. `CodeCityAdapter` (stub in this phase)
7. `CapabilityBridgeAdapter` (stub in this phase)

## Functional Requirements

- FR-02-01: Register/unregister adapters at runtime.
- FR-02-02: Health state for each adapter: `offline`, `online`, `degraded`.
- FR-02-03: Action bus routes intents to adapters through typed commands.
- FR-02-04: Adapter failures never crash shell.
- FR-02-05: Comms bridge supports request/response correlation IDs.

## Comms Layer Requirements

- CR-02-01: Envelope schema versioning (`v1`).
- CR-02-02: Timeout + retry policy per command class.
- CR-02-03: Standard error envelope with machine-readable code.
- CR-02-04: Optional streaming chunk support for long responses.

## Observability Requirements

- OR-02-01: Per-adapter latency metrics
- OR-02-02: Failure count and last failure reason
- OR-02-03: Current capability snapshot exposed to shell

## Files (Target)

- `orchestr8_next/adapters/contracts.py`
- `orchestr8_next/adapters/registry.py`
- `orchestr8_next/adapters/events.py`
- `orchestr8_next/adapters/llm.py`
- `orchestr8_next/adapters/memory.py`
- `orchestr8_next/adapters/workspace.py`
- `orchestr8_next/adapters/ide.py`
- `orchestr8_next/adapters/audio.py`
- `orchestr8_next/comms/bridge.py`
- `orchestr8_next/comms/envelopes.py`

## Acceptance Criteria

1. Adapter registry initializes with stubs and reports health.
2. Command dispatch works across all adapter interfaces.
3. Simulated adapter faults move state to degraded mode cleanly.
4. Shell remains responsive when any adapter fails.

## Test Plan

- Registry lifecycle tests
- Adapter fault injection tests
- Comms correlation/timeout tests
- Integration smoke tests from control actions

## Risks

- R-02-01: Interface churn causes action/reducer drift.
- R-02-02: Hidden provider-specific fields leak into core.

## Mitigations

- M-02-01: Strict pydantic/dataclass envelopes.
- M-02-02: Adapter contract lint checks.

## Exit Gate `G-P02`

Required evidence:
- Adapter capability matrix report
- Fault injection test report
- Comms protocol conformance report

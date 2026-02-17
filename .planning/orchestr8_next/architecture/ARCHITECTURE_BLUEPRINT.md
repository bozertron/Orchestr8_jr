# Architecture Blueprint: orchestr8_next

## 1) Problem Statement

Current Orchestr8 behavior is constrained by high coupling between UI, service wiring, visualization internals, and integration points. The result is high breakage risk where simple control changes cascade across unrelated systems.

## 2) Target Architecture

orchestr8_next adopts a layered architecture with explicit boundaries:

1. Presentation Shell (Marimo UI contract)
2. Action Bus + State Store (deterministic orchestration)
3. Service Adapter Layer (IO and integrations)
4. Visualization Layer (Code City isolated engine)
5. Bridge Layer (capability slices + external orchestration)

## 3) Layer Contracts

### L1: Presentation Shell

Purpose:
- Render canonical top row, center pane, and locked lower fifth.
- Emit typed actions only.

Must not:
- Call service backends directly.
- Parse provider payloads.
- Mutate global state outside reducer contract.

Inputs:
- `AppState` snapshot
- Derived selectors

Outputs:
- `UIAction` events to Action Bus

### L2: Action Bus + Store

Purpose:
- Single source of truth for state transitions.
- Deterministic command routing to adapters.

Must not:
- Render UI.
- Depend on provider-specific SDKs.

Inputs:
- `UIAction`
- `ServiceEvent`

Outputs:
- `StatePatch`
- `CommandIntent`

### L3: Service Adapter Layer

Purpose:
- Normalize external systems behind stable interfaces.

Adapters:
- `LLMAdapter`
- `MemoryAdapter`
- `WorkspaceAdapter`
- `IDEAdapter`
- `AudioAdapter`
- `CodeCityAdapter`
- `CapabilityBridgeAdapter`

Must not:
- Own UI state schema.
- Expose provider-specific payloads directly.

### L4: Visualization Layer

Purpose:
- 3D Code City rendering, node interactions, connection interactions.

Contract:
- Consumes `CodeCitySceneModel`.
- Emits `CodeCityEvent` (`node_click`, `connection_action`, `camera_state`).

Must not:
- Access storage or LLM APIs directly.
- Manage orchestration state.

### L5: Bridge Layer

Purpose:
- Move high-value capability slices into shared runtime pathways for Orchestr8.

Contract:
- `BridgeRequest`/`BridgeResponse` via typed envelopes.
- Feature flags for progressive rollout.

## 4) Canonical Data Models

### AppState (minimal)

- `session`: app/session metadata
- `controls`: lower fifth control states
- `chat`: message stream + queue
- `agents`: flagship + worker registry
- `panels`: panel visibility + content model
- `city`: scene metadata + selected entities
- `integrations`: adapter health + capability matrix
- `telemetry`: perf and error counters

### Action Types

- `UIAction`: user intent from controls
- `SystemAction`: startup/timer/bootstrap events
- `ServiceAction`: adapter replies and stream chunks
- `CityAction`: visualization events

## 5) Startup Sequence

1. Load config and feature flags.
2. Boot store and reducer.
3. Render shell with controls enabled in safe mode.
4. Initialize adapters asynchronously.
5. Mark capabilities online incrementally.
6. Attach Code City when `CodeCityAdapter` passes handshake.

## 6) Failure Handling

- Any adapter can fail independently without collapsing shell.
- Failed adapters move to `degraded` state with user-visible indicator.
- Action bus continues to process unaffected domains.

## 7) Security and Safety

- No direct eval or dynamic code execution during boot.
- Outbound provider traffic only through adapter layer.
- Prompt and content redaction policy at adapter boundary.

## 8) Migration Strategy

- Build clean shell first.
- Reconnect one domain at a time behind adapters.
- Keep old system intact until parity gates pass.
- Switch by feature flags + cutover checklist.

## 9) Architecture Acceptance Gates

P00 gate:
- Layer boundaries documented and approved.

P01 gate:
- All 12 lower-fifth controls dispatch typed actions.

P02 gate:
- Service adapters hot-swappable and failure-tolerant.

P03 gate:
- IDE integrations work as optional modules; core remains independent.

P04 gate:
- Code City reconnected without violating shell boundaries.

P05 gate:
- At least one capability slice integrated through bridge contract.

P06 gate:
- End-to-end reliability, test coverage, and cutover evidence complete.

## 10) Out of Scope (for orchestr8_next core)

- Full IDE replacement platform.
- Rewriting external orchestrators wholesale.
- Mandatory dependency on any single LLM provider.

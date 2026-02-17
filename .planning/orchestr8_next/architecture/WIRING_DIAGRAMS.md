# Wiring Diagrams: orchestr8_next

## Diagram 1: System Boundary Map

```mermaid
graph TD
    U[User Input] --> UI[Marimo Presentation Shell]
    UI --> BUS[Action Bus]
    BUS --> STORE[State Store/Reducer]
    STORE --> UI

    BUS --> SA[Service Adapters]
    SA --> LLM[LLM Providers]
    SA --> MEM[Memory Services]
    SA --> WS[Workspace + FS]
    SA --> IDE[IDE Integrations]
    SA --> AUDIO[Audio I/O]

    STORE --> CCM[CodeCity Scene Model]
    CCM --> CC[Code City Renderer/iframe]
    CC --> BUS

    SA --> BRIDGE[Capability Bridge Adapter]
    BRIDGE --> CAPS[Capability Modules]
```

## Diagram 2: Lower Fifth Control Flow

```mermaid
sequenceDiagram
    participant User
    participant Shell as Lower Fifth UI
    participant Bus as Action Bus
    participant Reducer as Reducer
    participant Adapter as Service Adapter
    participant Store as AppState

    User->>Shell: Click button / type input
    Shell->>Bus: UIAction(type, payload)
    Bus->>Reducer: Dispatch(UIAction)
    Reducer->>Store: StatePatch
    Store-->>Shell: Re-render selectors

    alt requires side effect
        Bus->>Adapter: CommandIntent
        Adapter-->>Bus: ServiceEvent
        Bus->>Reducer: Dispatch(ServiceEvent)
        Reducer->>Store: StatePatch
    end
```

## Diagram 3: Code City Event Bridge

```mermaid
sequenceDiagram
    participant City as Code City (Three.js)
    participant Bridge as JS Bridge Runtime
    participant Bus as Action Bus
    participant Store as AppState
    participant Panel as Building/Connection Panel

    City->>Bridge: postMessage(WOVEN_MAPS_NODE_CLICK)
    Bridge->>Bus: CityAction(node_click)
    Bus->>Store: Update selection + panel model
    Store-->>Panel: Render node details

    City->>Bridge: postMessage(WOVEN_MAPS_CONNECTION_ACTION)
    Bridge->>Bus: CityAction(connection_action)
    Bus->>Bus: Route to Connection Adapter
    Bus->>Store: Append result + history
```

## Diagram 4: Optional IDE Integration Boundary

```mermaid
graph LR
    BUS[Action Bus] --> IDEA[IDE Adapter Interface]
    IDEA --> VSC[VS Code Adapter]
    IDEA --> ZED[Zed Adapter]
    IDEA --> ANT[Antigravity Adapter]

    VSC -. optional .-> CORE[Core Runtime]
    ZED -. optional .-> CORE
    ANT -. optional .-> CORE

    CORE -->|never blocks on IDE adapters| CORE
```

## Diagram 5: Capability Slice Migration Lane

```mermaid
graph TD
    A[Capability Candidate] --> B[Define Bridge Contract]
    B --> C[Create Adapter Shim]
    C --> D[Run in Sandbox Feature Flag]
    D --> E[Phase Gate Validation]
    E --> F[Promote to Stable]
    F --> G[Shared Capability: Orchestr8 Core]
```

## Diagram 6: Parallel Build + Check-in Workflow

```mermaid
graph LR
    PLAN[PRD + Step Packet] --> TEAM[External Build Agent]
    TEAM --> OUTBOX[checkins/Pxx/STATUS.md]
    TEAM --> BLOCK[checkins/Pxx/BLOCKERS.md]
    ARCH[Architect Review] --> GUIDE[checkins/Pxx/GUIDANCE.md]
    GUIDE --> TEAM
    OUTBOX --> GATE[Phase Gate Decision]
```

## Wire Protocol Conventions

- All action envelopes use explicit `type`, `id`, `timestamp`, `payload` fields.
- Adapter responses include `source`, `ok`, `error`, `warnings`, and optional `result`.
- Bridge messages use versioned contracts: `contractVersion: "v1"`.

## Event Names (Reserved)

- `ui.apps.open`
- `ui.matrix.open`
- `ui.calendar.toggle`
- `ui.comms.toggle`
- `ui.files.toggle`
- `ui.flagship.cycle`
- `ui.search.invoke`
- `ui.record.toggle`
- `ui.playback.invoke`
- `ui.terminal.open`
- `ui.chat.send`
- `ui.attach.invoke`
- `city.node.click`
- `city.connection.action`
- `adapter.state.changed`

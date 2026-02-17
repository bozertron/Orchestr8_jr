# Extraction Packet: ExecutionQueueBrowser -> Coordination Buffer

**Packet ID**: P07-C6-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Orchestration
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `ExecutionQueueBrowser` logic to create a "City Coordination Buffer". This component manages the pending work for multiple agents, allowing the operator to reorder, delete, or prioritize tasks before they are committed to the city's execution engine.

## 2. Orchestr8 + Code City Value

- **Batch Processing Control**: Allows the operator to "stack" thousands of building modifications and review them in a buffer before "flushing" them to the 3D world.
- **Multi-Agent Conflict Resolution**: By seeing the global queue, the operator can detect if two agents are planning to modify the same building and reorder their tasks to prevent state corruption.
- **Operator Throughput**: Drag-and-drop reordering enables high-frequency task management without individual command entry.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Queue Browser** | `src/renderer/components/ExecutionQueueBrowser.tsx` | 1-609 | Core modal, drag-and-drop logic, and session-switching. |
| **Queue Item** | `QueueItemRow` | 311-608 | Individual task visualization (Command/Message types). |
| **Layer Management** | `useLayerStack` | 46, 83-96 | Integration with z-index and escape-key handling. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Buffer Controller**: Create `orchestr8.orchestration.buffer`.
    - Decouple from React and implement as a state machine for task ordering.
    - Standardize `QueuedItem` to include `impact_radius` (for city conflict detection).
2. **Visual Adaptation**:
    - **The Blueprint Table**: In the 3D City, visualize this as a literal blueprint table where pending "construction orders" are stacked as papers.
    - **Simulation Mode**: Allow the buffer to "pre-visualize" the city state if the queued tasks were applied (ghosting effects).
3. **UI Contract**: Implement the `onReorderItems` and `onRemoveItem` contracts to sync with the Orchestr8 core execution loop.

## 5. Expected Target Contracts

- `Orchestr8.Orchestration.QueueManager`: Persistence and reordering of pending tasks.
- `Orchestr8.City.PreVis`: Visualizes buffered tasks as "ghost buildings".

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Coordination & Buffering" implementation.

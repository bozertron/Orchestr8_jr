# Extraction Packet: SessionActivityGraph -> Observability Timeline

**Packet ID**: P07-C5-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Observability
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `SessionActivityGraph` logic to create an "Observability Timeline" for Code City. This component provides a configurable, bar-chart style visualization of activity over time, with support for different lookback periods (24h, 1 week, etc.) and interactive bucket selection.

## 2. Orchestr8 + Code City Value

- **City Activity Heatmap**: Visualize the history of "Agent Density" or "Construction Intensity" in the city.
- **Time Travel Navigation**: Clicking a bar in the graph can trigger a "Time Machine" flight to that specific historical state of the city.
- **Performance Monitoring**: Integration with the "City Power Grid" to show historical energy usage (token consumption) vs. output.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Activity Graph** | `src/renderer/components/SessionActivityGraph.tsx` | 1-359 | Core bucketization logic, lookback options, and React rendering. |
| **Lookback Options** | `LOOKBACK_OPTIONS` | 12-21 | Standardized time windows. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Bucketization Engine**: Create `orchestr8.observability.timeline`.
    - Decouple from React-specific state if possible (pure logic for bucket calculation).
    - Standardize the `ActivityEntry` interface (timestamp-based).
2. **Visual Adaptation**:
    - **3D Billboard**: In the 3D City, this graph can be rendered as a large holographic billboard in the "Central Plaza".
    - **Mini-Map Inset**: Include as a sparkline in the HUD.
3. **Interactive Contracts**: Define the `onBarClick` behavior to sync with the city's temporal state.

## 5. Expected Target Contracts

- `Orchestr8.Observability.TimelineService`: Provides bucketed data.
- `Orchestr8.City.TimeMachine`: Responds to timeline selections.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Observability & Metrics" implementation.

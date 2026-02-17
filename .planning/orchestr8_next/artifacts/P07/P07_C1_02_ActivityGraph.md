# Extraction Packet: Activity Graph -> City Heatmap

**Packet ID**: P07-C1-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Temporal Visualization
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `SessionActivityGraph` logic to power "Temporal Heatmaps" in Code City. This component buckets activity data (timestamps) into configurable time ranges (24h, 1 week, All Time) for visualization.

## 2. Orchestr8 + Code City Value

- **Temporal Dimension**: Adds a time axis to the spatial Code City layout.
- **Activity Visualization**: Enables "Heatmap Mode" where buildings glow based on recent activity (commits, edits, errors).
- **Bucketing Logic**: Reusable logic for aggregating time-series data at different granularities.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Activity Graph** | `src/renderer/components/SessionActivityGraph.tsx` | 1-359 | Main component with bucketing logic. |
| **Logic** | (Inline) | 120-150 | `getBucketTimeRange`, `LookbackPeriod` definitions. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Logic**: Move `LookbackPeriod` and bucketing helper functions to `orchestr8.city.time` service.
2. **Generalize Input**: Instead of `ActivityEntry` (timestamp only), accept generic `Event` stream (type, timestamp, severity).
3. **Visual Mapping**:
    - Create `CityHeatmapLayer`: Subscribes to time-series data.
    - Maps aggregate counts to `VisualProperty` (Color Intensity, Particle Emission).
    - *Interaction*: Allow user to scrub through time (using the bucket logic to interpolate).

## 5. Expected Target Contracts

- `Orchestr8.City.TimeService`: Aggregates events into time buckets.
- `Orchestr8.City.VisualLayers`: Interface for overlaying data on the city model.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "City Layers" feature set.

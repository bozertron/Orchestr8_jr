# Extraction Packet: ProcessMonitor -> City Power Grid

**Packet ID**: P07-C2-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Infrastructure & Monitoring
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `ProcessMonitor` logic to create the "City Power Grid" visualization. This component tracks, groups, and manages active system processes (AI agents, terminals, scripts), calculating runtime and status.

## 2. Orchestr8 + Code City Value

- **City Vital Signs**: Map active processes to "Energy Usage" or "Grid Status". Active agents light up their respective sectors.
- **Hierarchical Monitoring**: The `buildProcessTree` logic is perfect for visualizing hierarchical infrastructure (City -> District -> Building -> Room).
- **Control Plane**: Provides the logic to `kill` or `restart` processes, serving as the "City Control Center".

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Monitor Logic** | `src/renderer/components/ProcessMonitor.tsx` | 1-800+ | Tree building, polling, grouping logic. |
| **Data Types** | `ActiveProcess`, `ProcessNode` | 32-74 | standardized process schema. |

## 4. Conversion Plan (Clean-Room)

1. **Create Grid Service**: Extract `fetchActiveProcesses` and `buildProcessTree` into `orchestr8.infrastructure.grid`.
    - Standardize `ProcessNode` into `GridEntity`.
2. **Visual Mapping**:
    - **Power Lines**: Visualize process dependencies/parent-child relationships.
    - **Heat/Light**: Process CPU/Activity maps to block brightness.
    - **Outages**: Crashed processes show as "Blackouts" in the city.
3. **Interaction**:
    - Clicking a "Power Station" (Group) shows detailed stats.
    - "Emergency Shutoff": Kill process button maps to a circuit breaker interface.

## 5. Expected Target Contracts

- `Orchestr8.Infrastructure.ProcessService`: Polling and control.
- `Orchestr8.City.GridLayer`: Visualizes system health/activity.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "System Monitoring" integration.

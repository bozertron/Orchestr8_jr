# Extraction Packet: HistoryPanel -> Event Inspector

**Packet ID**: P07-C5-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Observability
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `HistoryPanel` logic to create a "City Event Inspector". This component manages a high-volume, virtualized list of historical events with filtering (Auto/User), search capabilities, and detailed drill-down into specific actions (tool calls, messages, etc.).

## 2. Orchestr8 + Code City Value

- **City Ledger**: A permanent, searchable record of every action taken by every agent in the city.
- **Virtualized Observation**: Efficiently handles thousands of events without crashing the UI, critical for long-running city sessions.
- **Forensic Inspection**: Allows the operator to "click into" a historical agent action and see exactly what changed in the city blueprints (Git diff integration).

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **History Panel** | `src/renderer/components/HistoryPanel.tsx` | 1-1341 | Virtualized list, filtering, search, and entry rendering. |
| **History Item** | `HistoryEntryItem` | 494-719 | Individual entry visualization (Success/Failure, Usage Stats). |
| **Virtualizer** | `@tanstack/react-virtual` | (External) | Dependency for high-performance listing. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Event Management Engine**: Create `orchestr8.observability.events`.
    - Implement high-performance filtering and search logic.
    - Standardize `HistoryEntry` schema for city-wide activity.
2. **Visual Adaptation**:
    - **City Archives**: Visualize as a terminal in a specific "Library" or "Archives" building in the city.
    - **Contextual Inspector**: When an agent is selected in 3D, filter this panel to show only that agent's history.
3. **Integration**: Map `Success/Failure/Validated` status to visual cues in the city (e.g., green/red outlines on modified buildings).

## 5. Expected Target Contracts

- `Orchestr8.Observability.EventStore`: Persistence and retrieval of city events.
- `Orchestr8.UX.VirtualList`: Reusable UI primitive for large datasets.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Audit & Inspection" features.

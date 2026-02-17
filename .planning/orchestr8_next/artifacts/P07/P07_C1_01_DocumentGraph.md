# Extraction Packet: Document Graph -> Code City Topology

**Packet ID**: P07-C1-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Visualization
**Risk Class**: Low
**Licensing Concern**: No (Standard libs d3/dagre used, no conflict headers observed)

## 1. Idea Summary

Extract the `DocumentGraph` subsystem to serve as the foundational "Knowledge Topology" or "City Map" for Code City. This system currently visualizes Markdown file relationships using force-directed and hierarchical layouts, with robust caching and performance/large-file handling.

## 2. Orchestr8 + Code City Value

- **Topology Engine**: The `layoutAlgorithms.ts` (Force/Dagre) provides a physics-based layout engine essential for "City" placement.
- **Performance Patterns**: `graphDataBuilder.ts` implements "Lazy Parsing", "MTime Caching", and "Large File Truncation" — critical patterns for visualizing large codebases in Code City without freezing the UI.
- **Visual Metaphor**: The "Focus Node + Neighbors" interaction model is perfect for exploring code dependencies (Ego-Network view).

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **View/Container** | `src/renderer/components/DocumentGraph/DocumentGraphView.tsx` | 1-800+ | Main orchestration, event handling, state. |
| **Data Builder** | `src/renderer/components/DocumentGraph/graphDataBuilder.ts` | 1-800+ | Core logic. *High Value*. |
| **Layout Engine** | `src/renderer/components/DocumentGraph/layoutAlgorithms.ts` | 1-800+ | Layout logic. *High Value*. Generic. |
| **Visuals** | `src/renderer/components/DocumentGraph/MindMap.tsx` | (Implied) | Canvas rendering logic (need to verify mapping to Code City 3D vs 2D). |

## 4. Conversion Plan (Clean-Room)

Do not copy-paste. Re-implement using Orchestr8 patterns:

1. **Abstract the Builder**: Create `CityTopologyBuilder` service.
    - *Input*: Generic `Node` interface (File, Function, Class), not just Markdown.
    - *Pattern*: Adopt the `_parseFile` caching strategy (mtime-based) but use `Orchestr8.fs` and `Marimo` streams.
    - *Refactoring*: Decouple from specific markdown link parsing; allow pluggable "Edge Detectors" (e.g., Import analyzer for JS/Py).

2. **Port Layout Engine**:
    - Create `orchestr8.city.layout` module.
    - Implement `ForceDirectedLayout` and `HierarchicalLayout` classes.
    - *Enhancement*: Add "Z-axis" support for 3D City height (e.g., Code Complexity -> Height).

3. **UI Adaptation**:
    - Instead of `MindMap` canvas, map nodes to `Code City` 3D entities.
    - Use the `DocumentGraphView`'s "Focus + Depth" state logic (`neighborDepth`, `activeFocusFile`) to control the *Rendered Chunk* of the city (Level of Detail management).

## 5. Expected Target Contracts

- `Orchestr8.City.TopologyService`: Accepts a root and returns a node/edge graph stream.
- `Orchestr8.City.LayoutService`: Accepts graph + config, returns XYZ coordinates.
- `Orchestr8.UI. signals`: `onEntitySelect`, `onEntityFocus`.

## 6. Handoff Recommendation

Route to `a_codex_plan` for integration into the `Code City` core. This is a "Core Capability" extraction.

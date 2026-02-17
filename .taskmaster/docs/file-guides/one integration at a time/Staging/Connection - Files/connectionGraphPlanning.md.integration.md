# connectionGraphPlanning.md Integration Guide

- Source: `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md`
- Total lines: `1625`
- SHA256: `825665e59d28f5e18ac50c5d9c6bfa1edd1b048b472d818c82ceb880ada1eaa7`
- Memory chunks: `14`
- Observation IDs: `705..718`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:256` zoom?: number;
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:416` zoom: number;
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:552` 3. Directionality constraints
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:578` 2. Betweenness centrality (bridge nodes)
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:769` 1. Mouse wheel for zoom
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:771` 3. Double-click to zoom to node
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:1209` 3. Support zoom and pan navigation
- `one integration at a time/Staging/Connection - Files/connectionGraphPlanning.md:1361` 2. Use constraint-based layouts for specific patterns

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

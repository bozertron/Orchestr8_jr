# WORKORDERS-BARRADEAU.json Integration Guide

- Source: `.planning/phases/WORKORDERS-BARRADEAU.json`
- Total lines: `476`
- SHA256: `bc8a417da2d1f71d2897407a22e8b23dac3b0ae8cd6338246b25257078c95d87`
- Memory chunks: `6`
- Observation IDs: `62..67`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/phases/WORKORDERS-BARRADEAU.json:27` "Color MUST use 0xD4AF37 (canonical gold), NOT 0xC9A962"
- `.planning/phases/WORKORDERS-BARRADEAU.json:51` "Background MUST be #0A0A0B (The Void)"
- `.planning/phases/WORKORDERS-BARRADEAU.json:79` "Height formula is LOCKED: 3 + (exports × 0.8)",
- `.planning/phases/WORKORDERS-BARRADEAU.json:80` "Footprint formula is LOCKED: 2 + (lines × 0.008)"
- `.planning/phases/WORKORDERS-BARRADEAU.json:133` "Particles must COALESCE, not animate"
- `.planning/phases/WORKORDERS-BARRADEAU.json:177` "NO sin/cos oscillation (no breathing)"
- `.planning/phases/WORKORDERS-BARRADEAU.json:389` "NO breathing/pulsing (FORBIDDEN)",
- `.planning/phases/WORKORDERS-BARRADEAU.json:445` "Emergence animation (no breathing)",

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

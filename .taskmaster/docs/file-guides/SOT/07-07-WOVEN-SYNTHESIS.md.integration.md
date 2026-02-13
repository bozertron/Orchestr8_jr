# 07-07-WOVEN-SYNTHESIS.md Integration Guide

- Source: `SOT/07-07-WOVEN-SYNTHESIS.md`
- Total lines: `609`
- SHA256: `7ba6cc7d5450ae9d637b1e4a453f73adb9573c54e4f2c319a00d9d086bc436fe`
- Memory chunks: `8`
- Observation IDs: `70..77`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `SOT/07-07-WOVEN-SYNTHESIS.md:132` // Color (from orchestr8)
- `SOT/07-07-WOVEN-SYNTHESIS.md:133` COLOR: 0xD4AF37              // Gold - healthy state
- `SOT/07-07-WOVEN-SYNTHESIS.md:175` // Color by health state (orchestr8 colors)
- `SOT/07-07-WOVEN-SYNTHESIS.md:277` │ [Gold] [Teal] [Purple]  │  [1][2][3][4]  │  [🔊]  │  [densit8 ▽] │

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

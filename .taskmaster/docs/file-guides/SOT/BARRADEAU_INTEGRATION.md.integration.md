# BARRADEAU_INTEGRATION.md Integration Guide

- Source: `SOT/BARRADEAU_INTEGRATION.md`
- Total lines: `287`
- SHA256: `460b9b4963c11202a530682f156497c68ea7c8ebc208a82179fcaded465d040e`
- Memory chunks: `4`
- Observation IDs: `78..81`

## Why This Is Painful

- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `SOT/BARRADEAU_INTEGRATION.md:33` | Working | Gold | #D4AF37 | Healthy, passing tests |
- `SOT/BARRADEAU_INTEGRATION.md:35` | Combat | Purple | #9D4EDD | Active LLM engagement |
- `SOT/BARRADEAU_INTEGRATION.md:55` - Buildings change color in real-time (Gold → Blue → Gold)
- `SOT/BARRADEAU_INTEGRATION.md:73` User clicks building → camera smoothly zooms to building → shows file details
- `SOT/BARRADEAU_INTEGRATION.md:80` type: 'WOVEN_MAPS_NODE_CLICK',
- `SOT/BARRADEAU_INTEGRATION.md:113` zoom: camera.zoom
- `SOT/BARRADEAU_INTEGRATION.md:125` | Gold | `setFrameColor('gold')` | Filter to healthy files |
- `SOT/BARRADEAU_INTEGRATION.md:126` | Teal | `setFrameColor('teal')` | Filter to broken files |
- `SOT/BARRADEAU_INTEGRATION.md:127` | Purple | `setFrameColor('combat')` | Filter to combat files |
- `SOT/BARRADEAU_INTEGRATION.md:148` │ [Gold] [Teal] [Purple]  │  [1][2][3][4]  │  [🔊]  │  [densit8] │

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

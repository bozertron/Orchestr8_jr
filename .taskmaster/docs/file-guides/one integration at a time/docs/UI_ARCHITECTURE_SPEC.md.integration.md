# UI_ARCHITECTURE_SPEC.md Integration Guide

- Source: `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md`
- Total lines: `557`
- SHA256: `4aef4fe396b897f6e338cdbd14fe0b36f0a77079b20d3e2d7981baf01479b148`
- Memory chunks: `5`
- Observation IDs: `474..478`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:5` **Reference:** maestroview.vue (canonical source)
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:16` 5. [Layer 3: Right Slider (JFDI Tickets)](#layer-3-right-slider-jfdi-tickets)
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:38` │         Gold = Working    Blue = Broken                   │ I │
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:39` │                Purple = Combat                            │ C │
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:48` maestro
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:55` 3. **Bottom Panel** - maestro + programmable button grid
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:56` 4. **Right Slider** - JFDI button → Tickets
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:99` | **Working** | Gold (#D4AF37) | Healthy code | Hover for details |
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:100` | **Broken** | Blue (#1fbdea) | Errors present | Click to zoom in |
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:101` | **Combat** | Purple (#9D4EDD) | Active debugging | Shows activity |
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:133` - **Animation:** Synchronized with zoom - panel drops as you travel
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:212` Left Grid                 maestro                    Right Grid
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:215` ### maestro (Center)
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:222` | **OBSERVE** | Dark Gold (#B8960C) | Planning mode, @ mentions only |
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:223` | **ON** | Bright Gold (#D4AF37) | Tier 2 access (full agency) |
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:230` - Can @ maestro (or any LLM) for explicit questions
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:270` ## 5. Layer 3: Right Slider (JFDI Tickets)
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:274` - **Activated by:** JFDI button (top bar, Button 2?)
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:281` │  JFDI TICKETS        │
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:450` From maestroview.vue:
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:527` - [ ] Bottom panel with maestro + button grid
- `one integration at a time/docs/UI_ARCHITECTURE_SPEC.md:540` - [ ] Vector embedding pipeline

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# WOVEN_MAPS_EXECUTION_SPEC.md Integration Guide

- Source: `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md`
- Total lines: `1578`
- SHA256: `46746eb718588fb9e8eac0e392d749240755fa55130c5643a7dd8b392fbee519`
- Memory chunks: `20`
- Observation IDs: `89..108`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:35` - **Gold (#D4AF37)**: Working code - all imports resolve, no errors
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:37` - **Purple (#9D4EDD)**: Combat - LLM "General" is actively debugging
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:50` Implement Woven Maps in `IP/plugins/06_maestro.py` (The Void plugin) so that when the user opens Orchestr8, they see their codebase as a living, breathing city.
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:66` │         IP/orchestr8_app.py             │  ← Main application entry
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:76` │  │ 06_maestro.py  ← THE VOID       │    │  ← THIS IS WHERE WE IMPLEMENT
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:79` │         STATE_MANAGERS                  │  ← Reactive state injection
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:91` Every plugin MUST have:
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:97` def render(STATE_MANAGERS: dict) -> Any:
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:99` get_root, set_root = STATE_MANAGERS["root"]
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:104` ### Current State of 06_maestro.py
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:124` │ [stereOS]              [Collabor8] [JFDI] [Summon]              │
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:133` │    │    Gold buildings = working code                    │     │
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:135` │    │    Purple buildings = combat (LLM active)           │     │
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:138` │    │    Click blue spot → zoom to neighborhood           │     │
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:145` │ [Apps][Matrix][Files]    (maestro)    [Search][Phreak>][Send]   │
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:156` 4. Clicking the building zooms camera into that "neighborhood"
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:164` 2. The scale increases (zoom in)
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:506` // Purple glow for combat
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1031` window.parent.postMessage({
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1052` ### Integration Function for 06_maestro.py
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1055` def create_code_city(STATE_MANAGERS: dict, width: int = 800, height: int = 600) -> Any:
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1061` get_root, _ = STATE_MANAGERS["root"]
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1242` function zoomToNode(node, camera, controls) {
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1318` assert '#D4AF37' in html  # Gold color
- `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:1320` assert '#9D4EDD' in html  # Purple color

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

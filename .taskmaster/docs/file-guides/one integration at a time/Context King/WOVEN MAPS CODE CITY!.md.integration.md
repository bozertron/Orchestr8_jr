# WOVEN MAPS CODE CITY!.md Integration Guide

- Source: `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md`
- Total lines: `1511`
- SHA256: `1a6b138d9ae93434c90c9bb17d1cc5f9ca274d7dcd570808baa38165e7309039`
- Memory chunks: `13`
- Observation IDs: `376..388`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- JS/Python bridge risk: event transport and payload validation can silently fail.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:34` - **Gold (#D4AF37)**: Working code - all imports resolve, no errors
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:36` - **Purple (#9D4EDD)**: Combat - LLM "General" is actively debugging
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:46` Implement Woven Maps in `IP/plugins/06_maestro.py` (The Void plugin) so that when the user opens Orchestr8, they see their codebase as a living, breathing city.
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:60` │         IP/orchestr8_app.py             │  ← Main application entry
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:69` │  │ 05_universal_bridge.py          │    │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:70` │  │ 06_maestro.py  ← THE VOID       │    │  ← THIS IS WHERE WE IMPLEMENT
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:73` │         STATE_MANAGERS                  │  ← Reactive state injection
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:84` Every plugin MUST have:
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:89` def render(STATE_MANAGERS: dict) -> Any:
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:91` get_root, set_root = STATE_MANAGERS["root"]
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:96` ### Current State of 06_maestro.py
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:113` │ [stereOS]              [Collabor8] [JFDI] [Summon]              │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:122` │    │    Gold buildings = working code                    │     │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:124` │    │    Purple buildings = combat (LLM active)           │     │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:127` │    │    Click blue spot → zoom to neighborhood           │     │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:134` │ [Apps][Matrix][Files]    (maestro)    [Search][Phreak>][Send]   │
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:143` 4. Clicking the building zooms camera into that "neighborhood"
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:149` 2. The scale increases (zoom in)
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:478` // Purple glow for combat
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1000` window.parent.postMessage({
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1021` ### Integration Function for 06_maestro.py
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1023` def create_code_city(STATE_MANAGERS: dict, width: int = 800, height: int = 600) -> Any:
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1029` get_root, _ = STATE_MANAGERS["root"]
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1202` function zoomToNode(node, camera, controls) {
- `one integration at a time/Context King/WOVEN MAPS CODE CITY!.md:1276` assert '#D4AF37' in html  # Gold color

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

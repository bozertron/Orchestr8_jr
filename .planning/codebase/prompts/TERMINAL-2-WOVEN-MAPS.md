# Terminal 2: Woven Maps Visualization Analysis

Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

Then analyze these files:

**Primary:** `IP/woven_maps.py` (1981 lines) — the Code City visualization
**Secondary:** `IP/woven_maps_nb.py` (1996 lines) — possible notebook variant

Read BOTH files completely. Then:

1. **Architecture**: How does it generate the visualization? Data flow from Python scan to JS render
2. **create_code_city()**: Full signature, what it takes, what it returns (mo.Html with embedded JS?)
3. **build_graph_data()**: Full signature, what data structure
4. **Embedded JavaScript**: Document ALL JS code — canvas rendering, particle systems, animations
5. **Control panel**: What buttons exist in the bottom 5th? Gold/Teal/Purple filters, keyframes, audio, Re-Emerge, Clear
6. **Node types**: 7 shapes for file types — list them all
7. **Health color integration**: How does health data get into node colors? Is it actually connected?
8. **Connection graph**: How are import edges rendered?
9. **Click handling**: WOVEN_MAPS_NODE_CLICK postMessage events
10. **Emergence animation**: Particle coalescence behavior
11. **Audio reactive**: Microphone integration — working?
12. **woven_maps_nb.py**: What is this? Duplicate? Notebook export? Should it exist?

Also read:
- `SOT/07-07-WOVEN-SYNTHESIS.md` — future 3D spec
- `SOT/BARRADEAU_INTEGRATION.md` — Barradeau technique spec

**Write report to:** `.planning/codebase/WOVEN-MAPS-DEEP-ANALYSIS.md`

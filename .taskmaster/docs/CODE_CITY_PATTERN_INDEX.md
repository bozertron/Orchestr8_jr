# Code City Pattern Index

## Canonical Priority

1. `.planning/phases/CONTEXT.md` (AUTHORITATIVE)
2. `.planning/VISION-ALIGNMENT.md` (LOCKED)
3. `.planning/phases/ARCHITECT-BARRADEAU.md` (architecture implementation direction)
4. `.planning/phases/WORKORDERS-BARRADEAU.json` (execution backlog)
5. `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt` (integration contract for current sprint)

## Integration Patterns

| Pattern | Rule | Primary anchors | Integration implication |
|---|---|---|---|
| Frame contract | Keep top frame and canonical nav semantics stable (`orchestr8/collabor8/JFDI`) | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:49`, `SOT/UI_SPECIFICATION.md:84` | UI work must not drift core frame behavior while wiring internals. |
| Color contract | Three-state only: Gold/Teal/Purple | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:52`, `.planning/phases/CONTEXT.md:193`, `.planning/VISION-ALIGNMENT.md:71` | No extra health states in render logic; normalize all status mapping upstream. |
| Motion contract | Emergence-only; no breathing/pulsing | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:51`, `.planning/phases/CONTEXT.md:50`, `.planning/VISION-ALIGNMENT.md:71` | Remove oscillation-style idle loops; transitions should be event-driven only. |
| Health pipeline | File change to watcher/checker to state to city is fixed | `.planning/phases/CONTEXT.md:76`, `.planning/VISION-ALIGNMENT.md:88` | State wiring must preserve this flow; avoid bypass paths that desync city state. |
| Root state contract | `STATE_MANAGERS` must expose health channels | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:32`, `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:151` | Add `health` and `health_status` without breaking existing manager keys. |
| Node-click bridge | Browser event must reach Python `handle_node_click()` | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:36`, `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:166`, `SOT/CODE_CITY_LANDSCAPE.md:31` | Add deterministic JS->Python bridge channel with schema validation before callback. |
| Camera behavior | Overview first, then zoom/dive, with return stack | `.taskmaster/docs/code_city_landscape_blind_integration_prd.txt:118`, `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:156`, `one integration at a time/docs/WOVEN_MAPS_EXECUTION_SPEC.md:163` | Camera state needs explicit mode machine and reversible transitions. |
| Edge truth | Edges must be relationship-derived and dynamic | `.planning/phases/CONTEXT.md:48`, `.planning/phases/CONTEXT.md:224`, `SOT/CODE_CITY_LANDSCAPE.md:32` | Never hardcode edge topology in UI layer; source from connection graph pipeline. |
| Signal-path explainability | File labels and full path glow on connection click | `.planning/phases/CONTEXT.md:55`, `.planning/phases/CONTEXT.md:228`, `SOT/CODE_CITY_LANDSCAPE.md:33` | Need panel schema + traversal/highlight routine, not only visual node rendering. |
| Sitting Room flow | Problem nodes route into collaborative room mode | `.planning/VISION-ALIGNMENT.md:62`, `.planning/phases/CONTEXT.md:227`, `SOT/CODE_CITY_LANDSCAPE.md:35` | Requires explicit mode transition contract, not ad hoc modal popup behavior. |
| Barradeau building math | Particle clustering + fixed building formulas | `.planning/phases/CONTEXT.md:38`, `.planning/phases/ARCHITECT-BARRADEAU.md:241`, `.planning/phases/ARCHITECT-BARRADEAU.md:242` | Rendering backend must respect locked formula semantics regardless of engine path. |

## Known Friction Themes

| Friction | Why it causes integration failures |
|---|---|
| Spec spread across many docs | Engineers implement local truth and miss a locked rule in another file. |
| UI canon vs legacy remnants | Old naming/labels in historical docs can leak into current code changes. |
| Cross-runtime bridge gap | JS events and Python handlers exist, but transport contract is missing. |
| Implicit state contracts | Health and camera keys are assumed in multiple places but not centralized. |
| Backend/frontend coupling | Dynamic-edge requirement depends on relationship data quality and timing. |

## Full-line Memory Proof

- Corpus ingest manifest: `.taskmaster/memory/bootstrap/2026-02-13_013910_code-city-full-corpus/manifest.json`
- Key line extraction log: `.taskmaster/memory/bootstrap/2026-02-13_013910_code-city-full-corpus/key_lines_with_files.tsv`

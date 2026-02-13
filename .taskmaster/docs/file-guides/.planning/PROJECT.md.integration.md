# PROJECT.md Integration Guide

- Source: `.planning/PROJECT.md`
- Total lines: `101`
- SHA256: `9a3ade9955649cdbf8f50db0ae869590a8fb0d45491393f49b94931f2f1a3dc9`
- Memory chunks: `1`
- Observation IDs: `1076..1076`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/PROJECT.md:9` The Code City visualization must render as an accurate, interactive spatial representation of the codebase — every file a building, every connection infrastructure, every health state visible — enabling human and AI to co-inhabit and co-evolve the same space.
- `.planning/PROJECT.md:22` - Validate full pipeline: orchestr8.py → plugins → woven_maps → Code City
- `.planning/PROJECT.md:46` - [ ] HealthChecker instantiated and updating node colors
- `.planning/PROJECT.md:70` 2. JFDI doesn't use the built TicketPanel
- `.planning/PROJECT.md:71` 3. HealthChecker is imported but never instantiated
- `.planning/PROJECT.md:86` - **Target file:** Most changes in `IP/plugins/06_maestro.py` (44KB)
- `.planning/PROJECT.md:87` - **Validation:** Must pass `marimo run orchestr8.py` without errors
- `.planning/PROJECT.md:95` | Top row: [orchestr8] [collabor8] [JFDI] [gener8] | Per UI spec, naming rule: ends with 8 = lowercase start | — Pending |
- `.planning/PROJECT.md:96` | JFDI → TicketPanel (not new panel) | Component already built, just needs wiring | — Pending |

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

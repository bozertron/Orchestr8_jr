# PRD_ORCHESTR8_V4_CONSOLIDATED.md Integration Guide

- Source: `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md`
- Total lines: `765`
- SHA256: `4736e41abfd6d3e7d8f5a446c118bd5769447774554202523dc2796762a7a974`
- Memory chunks: `7`
- Observation IDs: `675..681`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:51` | **Working** | Gold | `#D4AF37` | All imports resolve, typecheck passes |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:53` | **Combat** | Purple | `#9D4EDD` | General currently deployed and active |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:122` | Connie | Python | Database/schema conversion to LLM-friendly format |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:132` **The Emperor MUST see the subagent choreography.**
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:165` │  │  └──────────┘    └───────────┘            │  │  🟣 src/maestro       │ │
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:167` │  │  🟡 = Working (Gold)                      │  │     General: Active   │ │
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:169` │  │  🟣 = Combat (Purple)                     │  │                        │ │
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:176` │ │ [Files] [Matrix] [Graph] ══════ [maestro] ══════ [Search] [Deploy] [⏎]  │ │
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:210` **actu8** is the terminal component that enables general deployment. It must be imported from stereOS/Orchestr8_sr.
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:259` > **Q6:** What is the ticket data structure/schema?
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:269` │ PENDING  │────►│ IN_PROGRESS │────►│ RESOLVED │     │ BLOCKED  │
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:281` .orchestr8/
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:355` 4. If BLOCKED: Report what's blocking, suggest escalation
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:413` - `src/modules/maestro/` imports from generator - may need similar fix
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:441` - Export schemas as JSON, Markdown, or CSV
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:513` > **Q10:** Which files from stereOS should be migrated to Orchestr8_jr for ChangeChecker?
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:534` | `IP/plugins/05_universal_bridge.py` | EXISTS | Registry-based tool discovery COMPLETE |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:535` | `IP/plugins/06_maestro.py` | EXISTS | THE VOID - primary interface |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:537` | `IP/plugins/05_cli_bridge.py.deprecated` | DEPRECATED | Replaced by universal_bridge |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:549` .orchestr8/
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:567` | Update `06_maestro.py` with Mermaid as primary | P0 | 2-3 hours |
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:621` **Goal:** Match MaestroView.vue aesthetic within Marimo constraints
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:653` ├── orchestr8.py                      # Original Marimo app
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:656` │   ├── orchestr8_app.py             # Main Marimo application
- `one integration at a time/PRDs/PRD_ORCHESTR8_V4_CONSOLIDATED.md:667` │       ├── 05_universal_bridge.py

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

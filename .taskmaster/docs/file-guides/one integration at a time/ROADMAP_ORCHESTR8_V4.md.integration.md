# ROADMAP_ORCHESTR8_V4.md Integration Guide

- Source: `one integration at a time/ROADMAP_ORCHESTR8_V4.md`
- Total lines: `1921`
- SHA256: `67a666e50a1726fe39deafa23f1139a41d5802cc8291d22cc6feeb36b6d85428`
- Memory chunks: `25`
- Observation IDs: `24..48`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:59` **CRITICAL: The Emperor MUST see the full subagent choreography. Hiding it doesn't work - this was tested and failed.**
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:269` │  │  🟡 = Working (Gold)                      │  │  🟣 src/maestro       │ │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:271` │  │  🟣 = Combat (Purple)                     │  │     General: Active   │ │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:291` │ │ [Files] [Matrix] [Graph] ══════ [maestro] ══════ [Search] [Deploy] [⏎]  │ │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:308` | Tickets Panel | Click "Tickets" or JFDI | Slides from RIGHT | All pending tickets, searchable |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:375` | **Working** | Gold | `#D4AF37` | All imports resolve, typecheck passes, no blocking errors |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:377` | **Combat** | Purple | `#9D4EDD` | General currently deployed and active |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:394` ### 4.3 Why Purple Matters
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:402` **Purple = "Someone is in there fighting. Do not disturb."**
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:409` --gold-dark: #B8860B;      /* Gold accent/stroke */
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:494` 4. If BLOCKED: Report what's blocking, suggest escalation
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:516` - **Status:** PENDING | IN_PROGRESS | BLOCKED | RESOLVED
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:564` │ PENDING  │────►│ IN_PROGRESS │────►│ RESOLVED │     │ BLOCKED  │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:576` .orchestr8/
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:631` │ (Purple node)                       │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:720` - Exports to: `src/modules/maestro/`
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:726` | `scaffold-cli.ts` | 🔒 LOCKED | Stable CLI interface |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:727` | `../llm/registry.ts` | 🔒 LOCKED | Core registry, don't touch |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:843` - `src/modules/maestro/` imports from generator - may need similar fix
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:862` - Template paths must be relative to PROJECT ROOT, not fiefdom
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:909` │      (.orchestr8/tickets/)              │
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:964` echo \"BLOCKED: \$file is locked\"
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:975` # orchestr8_watcher.py
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:1133` | Update `06_maestro.py` with Mermaid as primary | P0 | 2-3 hours | Claude |
- `one integration at a time/ROADMAP_ORCHESTR8_V4.md:1220` ├── orchestr8.py                      # Original Marimo app (reference)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

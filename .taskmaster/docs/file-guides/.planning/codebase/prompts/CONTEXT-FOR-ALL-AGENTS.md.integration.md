# CONTEXT-FOR-ALL-AGENTS.md Integration Guide

- Source: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`
- Total lines: `80`
- SHA256: `4b028a2ef3cff9cbf04d9fc76c7a7ac4dd1b1d9b4047ffbd0c5fa53af79562e2`
- Memory chunks: `1`
- Observation IDs: `1019..1019`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:9` - **Entry point:** `orchestr8.py` — loads plugins from `IP/plugins/` via dynamic import
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:10` - **Central UI:** `IP/plugins/06_maestro.py` (1297 lines) — implements "The Void" stereOS layout
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:23` | Working | Gold | #D4AF37 |
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:24` | Broken | Teal | #1fbdea |
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:25` | Combat | Purple | #9D4EDD |
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:31` - **Top row:** [orchestr8] [collabor8] [JFDI] [gener8] — NO waves button
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:35` - **Naming rule:** Words ending with 8 start lowercase (orchestr8, collabor8, gener8)
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:39` 1. HealthChecker imported but NEVER instantiated in 06_maestro.py
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:40` 2. JFDI button opens placeholder "coming soon" — should use TicketPanel
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:41` 3. Collabor8 button opens placeholder — should show agent management
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:42` 4. Summon panel is placeholder — should wire to Carl
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:43` 5. Gener8 button only logs — should open Settings
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:44` 6. ~~~ waves button exists but shouldn't
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:51` Every file must: work (no stubs/TODOs), integrate correctly (wired to UI), and align with the vision (Code City metaphor, correct colors, emergence animations).
- `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md:75` - Needs wiring to: [what should connect but doesn't]

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

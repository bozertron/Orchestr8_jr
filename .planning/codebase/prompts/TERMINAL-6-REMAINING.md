# Terminal 6: Remaining Modules + Components + Styles + SOT Docs

Long-run mode: read `/home/bozertron/Orchestr8_jr/README.AGENTS`, `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`, and `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` before executing this prompt.


Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

## Part A: Remaining IP Core Modules

1. `IP/louis_core.py` (130 lines) — file protection via chmod
2. `IP/connie.py` (386 lines) — database converter
3. `IP/connie_gui.py` (602 lines) — Connie GUI variant
4. `IP/mermaid_generator.py` (81 lines) — Mermaid diagram generation
5. `IP/mermaid_theme.py` (140 lines) — Mermaid theming
6. `IP/terminal_spawner.py` (121 lines) — cross-platform terminal spawning
7. `IP/test_styles.py` (297 lines) — style tests?
8. `IP/__init__.py` (29 lines) — package init

## Part B: Components

9. `IP/plugins/components/__init__.py`
10. `IP/plugins/components/calendar_panel.py`
11. `IP/plugins/components/comms_panel.py`
12. `IP/plugins/components/file_explorer_panel.py`

## Part C: Styles

13. `IP/styles/orchestr8.css` — FULL CSS AUDIT. Every class, every color value, any .stereos-* remnants
14. `IP/styles/font_injection.py` (48 lines)

## Part D: SOT Document Audit

15. `SOT/07-07-WOVEN-SYNTHESIS.md` (609 lines) — 3D integration spec
16. `SOT/BARRADEAU_INTEGRATION.md` (287 lines) — Barradeau technique
17. `SOT/CURRENT_STATE.md` (164 lines) — state audit
18. `SOT/MARIMO_API_REFERENCE.md` (238 lines) — API fixes
19. `SOT/MASTER_ROADMAP.md` (627 lines) — 18-phase roadmap
20. `SOT/UI_SPECIFICATION.md` (199 lines) — UI spec
21. `SOT/WIRING_PLAN.md` (294 lines) — wiring fixes

For SOT docs: Note what's current vs stale, what contradicts other docs, what references old names.

**Write report to:** `.planning/codebase/REMAINING-AND-SOT-ANALYSIS.md`



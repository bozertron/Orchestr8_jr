# Execution Playbook — Point and Shoot

**How it works:** Each phase below has a claude command. Run it in a terminal. When it finishes, a `PHASE-REPORT.md` file appears next to the target files. That's how you know it's done.

## Phase 2: Navigation Wiring

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.

TARGET: IP/plugins/06_maestro.py
REQUIREMENTS: NAV-01 through NAV-04

Do these things and ONLY these things:
1. Change the Home button (line 907) label from 'Home' to 'orchestr8'
2. Wire Gener8 button (line 891-893) to navigate to settings instead of just logging
3. Wire JFDI button (lines 1059-1079) to use the REAL ticket_panel.render() instead of placeholder HTML
4. Remove the standalone Tickets button (line 900-903) — JFDI replaces it
5. Remove the ~~~ button (lines 1199-1202)
6. Verify top row is exactly: [orchestr8] [collabor8] [JFDI] [gener8]

After changes, write a report to IP/plugins/PHASE-2-NAV-REPORT.md documenting every change made with line numbers."
```

## Phase 3: Health Integration

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.

TARGETS: IP/plugins/06_maestro.py, IP/health_checker.py, IP/woven_maps.py
REQUIREMENTS: HLTH-01 through HLTH-03

Do these things:
1. In 06_maestro.py: instantiate HealthChecker with project_root (it's imported at line 77 but never used)
2. Pass health results into create_code_city() call (line 935) — may need to modify woven_maps.py to accept health data
3. Ensure node colors reflect health: Gold=#D4AF37 working, Teal=#1fbdea broken, Purple=#9D4EDD combat
4. Add a refresh mechanism that re-runs health check

Write report to IP/plugins/PHASE-3-HEALTH-REPORT.md"
```

## Phase 4: Briefing + Combat

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.

TARGETS: IP/briefing_generator.py, IP/combat_tracker.py, IP/plugins/06_maestro.py
REQUIREMENTS: BREF-01, BREF-02, CMBT-01, CMBT-02

Do these things:
1. In briefing_generator.py: implement load_campaign_log() — it's currently a stub. Parse CAMPAIGN_LOG.md files from .orchestr8/campaigns/
2. In combat_tracker.py: add cleanup_stale_deployments() call at app startup
3. In 06_maestro.py: call combat_tracker.cleanup_stale_deployments() at start of render()
4. Verify briefing panel shows real data (not empty)

Write report to IP/PHASE-4-BRIEFING-COMBAT-REPORT.md"
```

## Phase 5: Marimo Method Audit

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md AND SOT/MARIMO_API_REFERENCE.md.

TARGETS: Every .py file in IP/ and IP/plugins/ and IP/plugins/components/
REQUIREMENTS: MRIM-01 through MRIM-04

Audit EVERY file for incorrect Marimo 0.19.6 API usage:
- mo.vstack(..., style=) → WRONG, use mo.style() wrapper
- mo.hstack(..., style=) → WRONG, use mo.style() wrapper
- mo.ui.accordion() → WRONG, use mo.accordion()
- mo.ui.button(..., style=) → WRONG, use kind= or mo.style()
- mo.ui.progress() → WRONG, use mo.status.progress_bar()

Fix every instance found. Write report to IP/PHASE-5-MARIMO-REPORT.md listing every fix with file:line."
```

## Phase 6: Vision Audit — IP Modules

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.
Read CLAUDE.md for the full vision.

TARGETS: Every .py file directly in IP/ (not plugins/)
REQUIREMENTS: VMOD-01 through VMOD-12

For EACH of these files, determine:
- Does it serve a clear purpose aligned to the Code City / Mingos vision?
- Is it fully implemented (no stubs, no TODOs, no placeholder returns)?
- Is it referenced/used by any plugin?
- Should it be kept, fixed, or marked for removal?

Files: __init__.py, briefing_generator.py, carl_core.py, combat_tracker.py, connection_verifier.py, connie.py, connie_gui.py, health_checker.py, louis_core.py, mermaid_generator.py, mermaid_theme.py, terminal_spawner.py, ticket_manager.py, woven_maps.py, woven_maps_nb.py, test_styles.py

Write individual reports BESIDE each file: IP/[filename].VISION-REPORT.md
Write summary to IP/PHASE-6-MODULE-AUDIT-SUMMARY.md"
```

## Phase 7: Vision Audit — Plugins + Panels

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.

TARGETS: Every .py file in IP/plugins/ and IP/plugins/components/
REQUIREMENTS: VPLG-01 through VPLG-09, VPNL-01 through VPNL-05

For EACH plugin: Does it export PLUGIN_NAME, PLUGIN_ORDER, render()? Does render() produce working UI? Any stubs?
For EACH component: Does it render? Does it accept input? Is it wired to 06_maestro.py?

Write individual reports BESIDE each file: IP/plugins/[filename].VISION-REPORT.md
Write individual reports: IP/plugins/components/[filename].VISION-REPORT.md
Write summary to IP/plugins/PHASE-7-PLUGIN-AUDIT-SUMMARY.md"
```

## Phase 8: Settlement Integration

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.
Read GSD + Custom Agents/SETTLEMENT_SYSTEM_PRESSURE_TEST.md for Settlement architecture.

TARGETS: IP/plugins/06_maestro.py (Collabor8 panel), IP/woven_maps.py
REQUIREMENTS: SETL-01 through SETL-04

1. Replace Collabor8 placeholder (06_maestro.py lines 1037-1057) with real agent status display
2. Design data format for Settlement survey → Code City integration
3. Add fiefdom boundary visualization concept to woven_maps.py
4. Purple color for Settlement agent activity in Code City

Write report to IP/plugins/PHASE-8-SETTLEMENT-REPORT.md"
```

## Phase 9: Pipeline Validation + Cleanup

```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md for project context.

TARGETS: orchestr8.py, ALL IP files
REQUIREMENTS: PIPE-01 through PIPE-05, CLEAN-01 through CLEAN-04

1. Verify orchestr8.py loads all plugins without error
2. Verify plugin discovery and ordering works
3. Check for dead imports across entire codebase
4. Check for any remaining .stereos-* CSS classes
5. Check config file references are accurate
6. Remove any dead code found

Write report to PHASE-9-PIPELINE-CLEANUP-REPORT.md"
```

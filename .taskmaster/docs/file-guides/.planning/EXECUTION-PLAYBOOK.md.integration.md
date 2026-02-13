# EXECUTION-PLAYBOOK.md Integration Guide

- Source: `.planning/EXECUTION-PLAYBOOK.md`
- Total lines: `146`
- SHA256: `00ad3447eaef05478743a57a4454f0a953840fd40e12607ddf1fbf830549667c`
- Memory chunks: `2`
- Observation IDs: `1038..1039`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/EXECUTION-PLAYBOOK.md:10` TARGET: IP/plugins/06_maestro.py
- `.planning/EXECUTION-PLAYBOOK.md:14` 1. Change the Home button (line 907) label from 'Home' to 'orchestr8'
- `.planning/EXECUTION-PLAYBOOK.md:16` 3. Wire JFDI button (lines 1059-1079) to use the REAL ticket_panel.render() instead of placeholder HTML
- `.planning/EXECUTION-PLAYBOOK.md:17` 4. Remove the standalone Tickets button (line 900-903) — JFDI replaces it
- `.planning/EXECUTION-PLAYBOOK.md:19` 6. Verify top row is exactly: [orchestr8] [collabor8] [JFDI] [gener8]
- `.planning/EXECUTION-PLAYBOOK.md:29` TARGETS: IP/plugins/06_maestro.py, IP/health_checker.py, IP/woven_maps.py
- `.planning/EXECUTION-PLAYBOOK.md:33` 1. In 06_maestro.py: instantiate HealthChecker with project_root (it's imported at line 77 but never used)
- `.planning/EXECUTION-PLAYBOOK.md:35` 3. Ensure node colors reflect health: Gold=#D4AF37 working, Teal=#1fbdea broken, Purple=#9D4EDD combat
- `.planning/EXECUTION-PLAYBOOK.md:46` TARGETS: IP/briefing_generator.py, IP/combat_tracker.py, IP/plugins/06_maestro.py
- `.planning/EXECUTION-PLAYBOOK.md:50` 1. In briefing_generator.py: implement load_campaign_log() — it's currently a stub. Parse CAMPAIGN_LOG.md files from .orchestr8/campaigns/
- `.planning/EXECUTION-PLAYBOOK.md:52` 3. In 06_maestro.py: call combat_tracker.cleanup_stale_deployments() at start of render()
- `.planning/EXECUTION-PLAYBOOK.md:106` For EACH component: Does it render? Does it accept input? Is it wired to 06_maestro.py?
- `.planning/EXECUTION-PLAYBOOK.md:119` TARGETS: IP/plugins/06_maestro.py (Collabor8 panel), IP/woven_maps.py
- `.planning/EXECUTION-PLAYBOOK.md:122` 1. Replace Collabor8 placeholder (06_maestro.py lines 1037-1057) with real agent status display
- `.planning/EXECUTION-PLAYBOOK.md:125` 4. Purple color for Settlement agent activity in Code City
- `.planning/EXECUTION-PLAYBOOK.md:135` TARGETS: orchestr8.py, ALL IP files
- `.planning/EXECUTION-PLAYBOOK.md:138` 1. Verify orchestr8.py loads all plugins without error

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

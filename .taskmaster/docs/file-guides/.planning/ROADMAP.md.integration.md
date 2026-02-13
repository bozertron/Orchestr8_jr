# ROADMAP.md Integration Guide

- Source: `.planning/ROADMAP.md`
- Total lines: `200`
- SHA256: `706701cf5559fbec6f28dcddc71b931be6392b29a43e3fdf9031bf315d047d1d`
- Memory chunks: `2`
- Observation IDs: `1079..1080`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/ROADMAP.md:5` v2.0 Vision Audit + Full Wiring. Systematically audit every file, plugin, and feature against the ∅明nos vision. Complete v1.0 wiring work. Connect Settlement System to Code City. Validate the full pipeline end-to-end.
- `.planning/ROADMAP.md:15` - [x] **Phase 1: Branding** - Replace stereOS references with orchestr8
- `.planning/ROADMAP.md:17` - [ ] **Phase 3: Health Integration** - Instantiate HealthChecker and update Code City colors
- `.planning/ROADMAP.md:28` **Goal**: Application consistently displays "orchestr8" branding
- `.planning/ROADMAP.md:32` - [x] 01-01-PLAN.md — Replace stereOS branding with orchestr8
- `.planning/ROADMAP.md:42` 1. Top row shows exactly: [orchestr8] [collabor8] [JFDI] [gener8]
- `.planning/ROADMAP.md:43` 2. JFDI opens TicketPanel component
- `.planning/ROADMAP.md:52` **Goal**: HealthChecker updates Code City node colors based on actual file health
- `.planning/ROADMAP.md:59` 1. Code City nodes display Gold/Teal/Purple based on file health
- `.planning/ROADMAP.md:61` 3. HealthChecker instantiates without errors on render
- `.planning/ROADMAP.md:78` 4. Purple Code City nodes match real combat state
- `.planning/ROADMAP.md:95` 4. `marimo run orchestr8.py` produces no warnings
- `.planning/ROADMAP.md:111` 3. health_checker.py maps to Gold/Teal/Purple color system
- `.planning/ROADMAP.md:112` 4. combat_tracker.py integrates with Code City Purple
- `.planning/ROADMAP.md:114` 6. ticket_manager.py linked to JFDI panel
- `.planning/ROADMAP.md:132` 2. 06_maestro.py implements full stereOS layout per SOT.md
- `.planning/ROADMAP.md:134` 4. Plugin loading order correct in orchestr8.py
- `.planning/ROADMAP.md:152` 4. Purple color reflects Settlement agent activity
- `.planning/ROADMAP.md:159` **Goal**: End-to-end pipeline works; dead code and stale references removed
- `.planning/ROADMAP.md:166` 1. orchestr8.py loads all plugins without error
- `.planning/ROADMAP.md:168` 3. 06_maestro.py renders full stereOS layout

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

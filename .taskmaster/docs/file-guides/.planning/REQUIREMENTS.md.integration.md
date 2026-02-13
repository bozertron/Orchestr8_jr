# REQUIREMENTS.md Integration Guide

- Source: `.planning/REQUIREMENTS.md`
- Total lines: `152`
- SHA256: `d6a62c3ff71a2113050b1c32ed07296bf054ac82a8e233a4d6393888e87a53ef`
- Memory chunks: `2`
- Observation IDs: `1077..1078`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/REQUIREMENTS.md:11` - [x] **BRAND-01**: Application displays "orchestr8" instead of "stereOS" in all visible text
- `.planning/REQUIREMENTS.md:12` - [x] **BRAND-02**: CSS classes use `.orchestr8-*` prefix instead of `.stereos-*`
- `.planning/REQUIREMENTS.md:13` - [x] **BRAND-03**: Docstrings reference "orchestr8" not "stereOS"
- `.planning/REQUIREMENTS.md:19` - [ ] **NAV-01**: Top row displays exactly: [orchestr8] [collabor8] [JFDI] [gener8]
- `.planning/REQUIREMENTS.md:20` - [ ] **NAV-02**: JFDI button opens the TicketPanel component (not placeholder)
- `.planning/REQUIREMENTS.md:26` - [ ] **HLTH-01**: HealthChecker is instantiated with project root on render
- `.planning/REQUIREMENTS.md:45` - [ ] **VMOD-04**: health_checker.py results map to Gold/Teal/Purple color system
- `.planning/REQUIREMENTS.md:46` - [ ] **VMOD-05**: combat_tracker.py integrates with Code City (Purple nodes for active combat)
- `.planning/REQUIREMENTS.md:48` - [ ] **VMOD-07**: ticket_manager.py links to JFDI panel correctly
- `.planning/REQUIREMENTS.md:62` - [ ] **VPLG-06**: 05_universal_bridge.py serves its stated purpose
- `.planning/REQUIREMENTS.md:63` - [ ] **VPLG-07**: 06_maestro.py implements full stereOS layout per SOT.md spec
- `.planning/REQUIREMENTS.md:80` - [ ] **MRIM-04**: `marimo run orchestr8.py` completes without errors or warnings
- `.planning/REQUIREMENTS.md:87` - [ ] **SETL-04**: Code City color system reflects Settlement agent activity (Purple = agents active)
- `.planning/REQUIREMENTS.md:91` - [ ] **PIPE-01**: orchestr8.py loads all plugins without error
- `.planning/REQUIREMENTS.md:93` - [ ] **PIPE-03**: 06_maestro.py renders full stereOS layout
- `.planning/REQUIREMENTS.md:101` - [ ] **CLEAN-03**: CSS uses consistent `.orchestr8-*` prefix (no `.stereos-*` remnants)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

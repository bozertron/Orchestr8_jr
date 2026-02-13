# WORKORDERS-SUMMON.json Integration Guide

- Source: `.planning/phases/WORKORDERS-SUMMON.json`
- Total lines: `147`
- SHA256: `13e2c227efeb960497bcaa0fea2ad95f0d6542d92c9a8c2d7b451663633d8840`
- Memory chunks: `2`
- Observation IDs: `1073..1074`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/phases/WORKORDERS-SUMMON.json:14` "title": "Add Summon state variables to 06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:15` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:30` "constraints": ["Must use mo.ui.text with on_change callback", "State must be reactive"],
- `.planning/phases/WORKORDERS-SUMMON.json:36` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:53` "constraints": ["Three-state colors only (gold #D4AF37, teal #1fbdea, purple #9D4EDD)", "NO breathing animations"],
- `.planning/phases/WORKORDERS-SUMMON.json:59` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:72` "Instantiate Carl with STATE_MANAGERS",
- `.planning/phases/WORKORDERS-SUMMON.json:77` "constraints": ["Carl does NOT block (async/cached)", "Minimum 2 characters before query"],
- `.planning/phases/WORKORDERS-SUMMON.json:83` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:99` "constraints": ["Use emergence animation (NOT breathing)", "Void background #0A0A0B"],
- `.planning/phases/WORKORDERS-SUMMON.json:105` "file": "IP/plugins/06_maestro.py",
- `.planning/phases/WORKORDERS-SUMMON.json:115` "instantiation": "carl = Carl(STATE_MANAGERS)",
- `.planning/phases/WORKORDERS-SUMMON.json:119` "constraints": ["Non-blocking operation required", "Handle missing Carl gracefully"],
- `.planning/phases/WORKORDERS-SUMMON.json:127` "description": "IP/carl_core.py must exist with gather_context() method",

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

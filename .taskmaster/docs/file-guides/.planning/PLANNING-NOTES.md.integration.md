# PLANNING-NOTES.md Integration Guide

- Source: `.planning/PLANNING-NOTES.md`
- Total lines: `112`
- SHA256: `9c47cd51d0b87e61e464b8a4fc404a925fc3d9ad95f4d23e18f424e4d33723f7`
- Memory chunks: `1`
- Observation IDs: `1075..1075`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/PLANNING-NOTES.md:8` - Plus: `orchestr8.py` entry point (239 lines)
- `.planning/PLANNING-NOTES.md:12` ### `.orchestr8/tickets/` — Working ticket system
- `.planning/PLANNING-NOTES.md:17` - **BUT** JFDI button in 06_maestro.py shows placeholder instead of using it
- `.planning/PLANNING-NOTES.md:56` ## Critical Insight From 06_maestro.py
- `.planning/PLANNING-NOTES.md:70` - Line 893: Gener8 only logs `"Switch to Generator tab"` — should open settings
- `.planning/PLANNING-NOTES.md:72` - Lines 1059-1079: JFDI panel is `<div>...coming soon...</div>` — despite TicketPanel being instantiated at line 403!
- `.planning/PLANNING-NOTES.md:75` - Line 77: HealthChecker imported, NEVER instantiated
- `.planning/PLANNING-NOTES.md:77` - Line 907: Button says "Home" instead of "orchestr8"

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

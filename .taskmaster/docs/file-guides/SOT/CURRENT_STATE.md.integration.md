# CURRENT_STATE.md Integration Guide

- Source: `SOT/CURRENT_STATE.md`
- Total lines: `164`
- SHA256: `bf9dc350d9cacd0ba651737ac953707425baac7b2b96346aae83ade1d5956d59`
- Memory chunks: `2`
- Observation IDs: `135..136`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `SOT/CURRENT_STATE.md:31` | `IP/combat_tracker.py` | 4KB | Deployment tracking | COMPLETE - Purple state management |
- `SOT/CURRENT_STATE.md:40` | `ticket_panel.py` | JFDI ticket panel | COMPLETE - Full UI, wired to TicketManager |
- `SOT/CURRENT_STATE.md:55` | `05_universal_bridge.py` | Tool registry | FIXED (marimo API) |
- `SOT/CURRENT_STATE.md:56` | `06_maestro.py` | THE VOID | PARTIALLY WIRED |
- `SOT/CURRENT_STATE.md:62` ## II. What's Wired in 06_maestro.py
- `SOT/CURRENT_STATE.md:80` from IP.health_checker import HealthChecker           # IMPORTED, NEVER INSTANTIATED
- `SOT/CURRENT_STATE.md:97` | Brand uses legacy naming | Lines 873-876 | Should be "orchestr8" |
- `SOT/CURRENT_STATE.md:98` | CSS uses legacy class names | Lines 189-200 | Should be `.orchestr8-*` |
- `SOT/CURRENT_STATE.md:100` | JFDI opens placeholder | Lines 1059-1079 | Has "coming soon" text, ignores TicketPanel |
- `SOT/CURRENT_STATE.md:104` | HealthChecker never runs | Line 77 | Imported but never instantiated |
- `SOT/CURRENT_STATE.md:113` | Phase 1 | Build mermaid, health checker, spawner | ALL EXIST - but HealthChecker not wired |
- `SOT/CURRENT_STATE.md:114` | Phase 2 | Create ticket system | COMPLETE - but JFDI button doesn't use it |
- `SOT/CURRENT_STATE.md:129` 4. **Maestro "coming soon" panels** - Placeholder UI (Collabor8, JFDI, Summon)
- `SOT/CURRENT_STATE.md:156` 2. JFDI doesn't use TicketPanel
- `SOT/CURRENT_STATE.md:157` 3. HealthChecker never runs

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

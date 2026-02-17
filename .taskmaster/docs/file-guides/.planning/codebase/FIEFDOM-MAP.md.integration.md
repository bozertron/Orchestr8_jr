# FIEFDOM-MAP.md Integration Guide

- Source: `.planning/codebase/FIEFDOM-MAP.md`
- Total lines: `249`
- SHA256: `2110a28bce4628c4268f16e69308ced4ee6432900533855641a57e2b227abeda`
- Memory chunks: `3`
- Observation IDs: `1013..1015`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/codebase/FIEFDOM-MAP.md:34` | health_checker.py | 4,156 | 6 | 22 | HealthChecker 3,068 | 5 | GOLD |
- `.planning/codebase/FIEFDOM-MAP.md:69` 3. **health_checker.py** - imported but never instantiated in maestro.py (HLTH-01)
- `.planning/codebase/FIEFDOM-MAP.md:76` **Boundary Basis:** PLUGIN_PROTOCOL contract + UI tab pattern
- `.planning/codebase/FIEFDOM-MAP.md:83` | 06_maestro.py | 5,192 | 8 | 35 | render() 4,042 | 3 | TEAL |
- `.planning/codebase/FIEFDOM-MAP.md:86` | 05_universal_bridge.py | 2,028 | 5 | 10 | render() 1,153 | 3 | GOLD |
- `.planning/codebase/FIEFDOM-MAP.md:106` 1. **06_maestro.py:77** - HealthChecker imported but NEVER instantiated
- `.planning/codebase/FIEFDOM-MAP.md:107` 2. **06_maestro.py:1037-1057** - Collabor8 panel is PLACEHOLDER HTML
- `.planning/codebase/FIEFDOM-MAP.md:108` 3. **06_maestro.py:1059-1079** - JFDI panel is PLACEHOLDER HTML (should use TicketPanel)
- `.planning/codebase/FIEFDOM-MAP.md:109` 4. **06_maestro.py:1081-1095** - Summon panel is PLACEHOLDER HTML
- `.planning/codebase/FIEFDOM-MAP.md:110` 5. **06_maestro.py:893** - Gener8 button only logs, doesn't open Settings
- `.planning/codebase/FIEFDOM-MAP.md:111` 6. **06_maestro.py:907** - Home button says "Home" not "orchestr8"
- `.planning/codebase/FIEFDOM-MAP.md:112` 7. **06_maestro.py:900-903** - Extra Tickets button not in spec
- `.planning/codebase/FIEFDOM-MAP.md:113` 8. **06_maestro.py:1199-1202** - ~~~ waves button exists but shouldn't
- `.planning/codebase/FIEFDOM-MAP.md:143` All 5 panel components are **FULLY WIRED** to 06_maestro.py:
- `.planning/codebase/FIEFDOM-MAP.md:151` ## Fiefdom: Entry (orchestr8.py)
- `.planning/codebase/FIEFDOM-MAP.md:153` **Boundary:** orchestr8.py (single file)
- `.planning/codebase/FIEFDOM-MAP.md:161` | orchestr8.py | 2,000 | 4 | 8 | Plugin discovery, dynamic loading, main entry | GOLD |
- `.planning/codebase/FIEFDOM-MAP.md:185` | communic8 | Communication bridge | Ready |
- `.planning/codebase/FIEFDOM-MAP.md:230` - **Every health state** = Visible color (Gold=working, Teal=broken, Purple=combat)
- `.planning/codebase/FIEFDOM-MAP.md:244` | output_renderer.py | Plugins or Shared? | Plugins | Only used by universal_bridge |

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

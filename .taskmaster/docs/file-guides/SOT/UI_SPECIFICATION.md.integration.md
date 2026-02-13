# UI_SPECIFICATION.md Integration Guide

- Source: `SOT/UI_SPECIFICATION.md`
- Total lines: `199`
- SHA256: `befa442d67dda444069bb6146ce9c6654ab49fd683d53e0ceccba756ae2d9785`
- Memory chunks: `3`
- Observation IDs: `82..84`

## Why This Is Painful

- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `SOT/UI_SPECIFICATION.md:11` - **Application Name:** orchestr8 (lowercase, ends with 8)
- `SOT/UI_SPECIFICATION.md:12` - **Naming Convention:** Words ending with 8 start lowercase (orchestr8, collabor8, gener8)
- `SOT/UI_SPECIFICATION.md:23` --gold-dark: #B8860B;        /* Gold accent/stroke */
- `SOT/UI_SPECIFICATION.md:24` --gold-saffron: #F4C430;     /* Gold highlight */
- `SOT/UI_SPECIFICATION.md:41` | Working | Gold | #D4AF37 | All imports resolve, typecheck passes |
- `SOT/UI_SPECIFICATION.md:43` | Combat | Purple | #9D4EDD | General currently deployed and active |
- `SOT/UI_SPECIFICATION.md:52` | [orchestr8] [collabor8] [JFDI] [gener8]              [Model Picker]     |
- `SOT/UI_SPECIFICATION.md:60` |  |                                  |  |   - Tickets (JFDI)         |   |
- `SOT/UI_SPECIFICATION.md:61` |  |     Gold = Working              |  |   - Calendar               |   |
- `SOT/UI_SPECIFICATION.md:63` |  |     Purple = Combat             |  |   - File Explorer          |   |
- `SOT/UI_SPECIFICATION.md:72` | | [Apps] [Matrix] [Calendar] [Comms] [Files] == [maestro] == [Search] | |
- `SOT/UI_SPECIFICATION.md:84` | 1 | `orchestr8` | Home - Reset to default state, always present |
- `SOT/UI_SPECIFICATION.md:85` | 2 | `collabor8` | Agents dropdown - Domain agent management |
- `SOT/UI_SPECIFICATION.md:86` | 3 | `JFDI` | "Just Fucking Do It" - Opens Ticket panel (slides RIGHT) |
- `SOT/UI_SPECIFICATION.md:109` | maestro | Global search (summon) |
- `SOT/UI_SPECIFICATION.md:115` | Search | Same as maestro - global search |
- `SOT/UI_SPECIFICATION.md:132` - Tickets (JFDI) - Full TicketPanel component
- `SOT/UI_SPECIFICATION.md:170` Use `.orchestr8-*` classes for branding. Legacy class names should not be used.
- `SOT/UI_SPECIFICATION.md:179` .orchestr8-brand { }
- `SOT/UI_SPECIFICATION.md:180` .orchestr8-prefix { }
- `SOT/UI_SPECIFICATION.md:181` .orchestr8-suffix { }
- `SOT/UI_SPECIFICATION.md:188` The canonical CSS file is: `IP/styles/orchestr8.css`
- `SOT/UI_SPECIFICATION.md:190` This file defines all colors, typography, and component styles. Any new components should use these variables.
- `SOT/UI_SPECIFICATION.md:197` - **Style Reference:** `IP/styles/orchestr8.css`
- `SOT/UI_SPECIFICATION.md:198` - **Implementation:** `IP/plugins/06_maestro.py`

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

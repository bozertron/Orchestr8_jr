# Shared Context for All Analysis Agents

Long-run mode: read `/home/bozertron/Orchestr8_jr/README.AGENTS`, `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`, and `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` before executing this prompt.


## Project: Orchestr8

Orchestr8 is a Marimo 0.19.6 reactive Python dashboard that renders codebases as "Code Cities" — the initial settlement of a vision called Mingos, a collaborative spatial environment for human and machine intelligence.

## Key Facts

- **Entry point:** `orchestr8.py` — loads plugins from `IP/plugins/` via dynamic import
- **Central UI:** `IP/plugins/06_maestro.py` (1297 lines) — implements "The Void" stereOS layout
- **Visualization:** `IP/woven_maps.py` (1981 lines) — Code City via Barradeau particle technique
- **Framework:** Marimo 0.19.6 — reactive notebook framework. Key API gotchas:
  - `mo.vstack()` and `mo.hstack()` have NO `style` param — use `mo.style()` wrapper
  - `mo.accordion()` is top-level, NOT `mo.ui.accordion()`
  - `mo.ui.button()` has NO `style` param — use `kind=` or `mo.style()` wrapper
  - `mo.state()` returns `(getter, setter)` tuple
  - `mo.status.progress_bar()` not `mo.ui.progress()`

## Color System (EXACT)

| State | Color | Hex |
|-------|-------|-----|
| Working | Gold | #D4AF37 |
| Broken | Teal | #1fbdea |
| Combat | Purple | #9D4EDD |
| Void (bg) | Black | #0A0A0B |
| Surface | Dark | #121214 |

## UI Spec (from SOT/UI_SPECIFICATION.md)

- **Top row:** [orchestr8] [collabor8] [JFDI] [gener8] — NO waves button
- **Center:** THE VOID (Code City / Woven Maps visualization)
- **Right panels:** Slide-out, mutually exclusive (Tickets, Calendar, Comms, FileExplorer)
- **Bottom 5th:** Control Surface — NEVER MOVES (the Overton Anchor)
- **Naming rule:** Words ending with 8 start lowercase (orchestr8, collabor8, gener8)

## Known Problems (from SOT/CURRENT_STATE.md)

1. HealthChecker imported but NEVER instantiated in 06_maestro.py
2. JFDI button opens placeholder "coming soon" — should use TicketPanel
3. Collabor8 button opens placeholder — should show agent management
4. Summon panel is placeholder — should wire to Carl
5. Gener8 button only logs — should open Settings
6. ~~~ waves button exists but shouldn't
7. briefing_generator.load_campaign_log() is a stub (returns empty)
8. carl_core.py is "hollow — only dumps JSON"
9. Combat deployments don't auto-cleanup on startup

## What "Done" Means

Every file must: work (no stubs/TODOs), integrate correctly (wired to UI), and align with the vision (Code City metaphor, correct colors, emergence animations).

## Report Format

Write your report to: `/home/bozertron/Orchestr8_jr/.planning/codebase/[REPORT-NAME].md`

For each file analyzed, use this structure:

```markdown
## [filename]

**Purpose:** What this file does
**Status:** Working | Partial | Stub | Dead
**Lines:** N

### What Works
- [bullet list of functional features]

### What's Broken/Stubbed
- **Line N:** [description of stub/issue]

### Integration Points
- Called by: [who calls this]
- Calls: [what this calls]
- Needs wiring to: [what should connect but doesn't]

### To Make It "Done"
1. [specific action item]
2. [specific action item]
```



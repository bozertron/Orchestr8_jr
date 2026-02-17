# Terminal 1: 06_maestro.py Deep Analysis

Long-run mode: read `/home/bozertron/Orchestr8_jr/README.AGENTS`, `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/HARD_REQUIREMENTS.md`, and `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/LONG_RUN_MODE.md` before executing this prompt.


Read the shared context first: `.planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md`

Then analyze this ONE file with extreme thoroughness:

**File:** `IP/plugins/06_maestro.py` (1297 lines)

This is THE most important file in the project. It's the central UI — "The Void."

Read the ENTIRE file. Then:

1. **Map every button** — what label, what handler, what it actually does vs what the UI spec says it should do
2. **Map every panel** — Collabor8, JFDI, Summon, Tickets, Calendar, Comms, FileExplorer, Deploy. For each: is it a real component or placeholder HTML?
3. **Map every state variable** — list all mo.state() calls with their purpose
4. **Map every service instantiation** — CombatTracker, BriefingGenerator, etc. Are they used? How?
5. **Map the render() flow** — what gets built, in what order, what's returned
6. **Identify every "coming soon" or placeholder** with exact line numbers
7. **Identify every button that only logs** vs actually does something
8. **Check Marimo API correctness** — any mo.vstack(..., style=) or other wrong patterns?
9. **Compare to SOT/UI_SPECIFICATION.md** — read that file and identify every deviation

Also read these SOT files for comparison:
- `SOT/UI_SPECIFICATION.md`
- `SOT/WIRING_PLAN.md`
- `SOT/CURRENT_STATE.md`

**Write report to:** `.planning/codebase/MAESTRO-DEEP-ANALYSIS.md`



# How to Run Analysis Terminals

## Setup

Open 6 terminal windows. In each, cd to the project root:
```bash
cd /home/bozertron/Orchestr8_jr
```

## Run Each Terminal

Each terminal runs Claude Code with a specific prompt file:

### Terminal 1: Maestro (THE most important)
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-1-MAESTRO.md exactly. Write your report to .planning/codebase/MAESTRO-DEEP-ANALYSIS.md"
```

### Terminal 2: Woven Maps
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-2-WOVEN-MAPS.md exactly. Write your report to .planning/codebase/WOVEN-MAPS-DEEP-ANALYSIS.md"
```

### Terminal 3: Core Trio
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-3-CORE-TRIO.md exactly. Write your report to .planning/codebase/CORE-TRIO-ANALYSIS.md"
```

### Terminal 4: Data Modules
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-4-DATA-MODULES.md exactly. Write your report to .planning/codebase/DATA-MODULES-ANALYSIS.md"
```

### Terminal 5: Plugins
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-5-PLUGINS.md exactly. Write your report to .planning/codebase/PLUGINS-ANALYSIS.md"
```

### Terminal 6: Remaining + SOT
```bash
claude "Read .planning/codebase/prompts/CONTEXT-FOR-ALL-AGENTS.md then read and follow .planning/codebase/prompts/TERMINAL-6-REMAINING.md exactly. Write your report to .planning/codebase/REMAINING-AND-SOT-ANALYSIS.md"
```

## Expected Output Files

When all 6 complete, you'll have:
```
.planning/codebase/
├── MAESTRO-DEEP-ANALYSIS.md       ← Terminal 1
├── WOVEN-MAPS-DEEP-ANALYSIS.md    ← Terminal 2
├── CORE-TRIO-ANALYSIS.md          ← Terminal 3
├── DATA-MODULES-ANALYSIS.md       ← Terminal 4
├── PLUGINS-ANALYSIS.md            ← Terminal 5
├── REMAINING-AND-SOT-ANALYSIS.md  ← Terminal 6
└── prompts/                       ← The prompt files
```

## After All Complete

Come back to the main session and say:
"All 6 analysis reports are complete in .planning/codebase/. Synthesize them into execution-ready plans."

The main session will read only the report files (compact summaries, not raw output) and produce the master execution plan.

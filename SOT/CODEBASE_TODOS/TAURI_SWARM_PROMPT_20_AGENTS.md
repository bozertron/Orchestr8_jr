# Launch Prompt: 20-Agent Tauri Upside Swarm

Use this prompt as-is for all agents, with per-agent assignment from the matrix below.

## Global Mission

From root (`/home/bozertron`), identify where we should "slide in" to capture the highest upside for Orchestr8 from existing Tauri codebases.

Goal:

1. Find reusable components/contracts that accelerate Orchestr8 MVP.
2. Prioritize app-first execution (no premature packaging lock-in).
3. Preserve path to final Tauri desktop packaging.

## Hard Rules

1. Always search from root.
2. No assumptions allowed.
3. If ambiguous, make two evidence-backed attempts, then mark unresolved and continue.
4. Read-only research only unless explicitly asked to modify code.
5. Every claim must include file evidence (`path:line`).
6. Exclude noise from `node_modules`, `target`, `.git` in footprint estimates.

## Candidate Tauri App Roots (Detected)

1. `/home/bozertron/EPO - JFDI - Maestro`
2. `/home/bozertron/JFDI - Collabkit/Application`
3. `/home/bozertron/Documents/DAC-O`
4. `/home/bozertron/Documents/orchestr8 Integration Staging/CLAUDE INTEGRATION PRE FIX`
5. `/home/bozertron/Documents/augment-projects/Maestro/crates/app-shell`
6. `/home/bozertron/Documents/maestro-scaffolder-tool`
7. `/home/bozertron/Dev Tools/orchestr8_unpack/orchestr8_extracted/orchestr8`
8. Others (archive/copy candidates): `/home/bozertron/Applications/Copies for Safe Keeping/Application`, `/home/bozertron/Documents/orchestr8 Integration Staging/orchestr8`, `/home/bozertron/JFDI - Collabkit/EPO Master/MSTOG`

## Confirmed Seed Facts (Validate + Extend)

1. These are byte-identical:

- `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/settings.js`
- `/home/bozertron/Orchestr8_jr/Settings For Integration Referece/settings.js`

1. These are byte-identical:

- `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/scripts/settings-advanced.js`
- `/home/bozertron/Orchestr8_jr/Settings For Integration Referece/settings-advanced.js`

1. These are byte-identical:

- `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/pages/settings.html`
- `/home/bozertron/Orchestr8_jr/Settings For Integration Referece/settings.html`

1. These are byte-identical:

- `/home/bozertron/EPO - JFDI - Maestro/src-tauri/html/pages/settings-advanced.html`
- `/home/bozertron/Orchestr8_jr/Settings For Integration Referece/settings-advanced.html`

1. These are byte-identical:

- `/home/bozertron/JFDI - Collabkit/Application/src/modules/maestro/MaestroView.vue`
- `/home/bozertron/Orchestr8_jr/one integration at a time/UI Reference/MaestroView.vue`

1. These are byte-identical:

- `/home/bozertron/JFDI - Collabkit/Application/src/components/FileExplorer.vue`
- `/home/bozertron/Orchestr8_jr/one integration at a time/FileExplorer/FileExplorer.vue`

## Output Contract

Each agent must produce:

1. One report file using template:

- `/home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/TAURI_SWARM_REPORT_TEMPLATE.md`

2. Output destination:

- `/home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/TAURI_SWARM_REPORTS/agent_<NN>.md`

3. One-line completion ping in shared memory/comms with:

- repo path reviewed
- total score
- recommendation (`ACQUIRE_NOW` / `ACQUIRE_LATER` / `ARCHIVE_ONLY`)

## Analysis Axes (Required)

1. Strategic fit with Orchestr8 intent.
2. Time-to-value (days, not weeks).
3. Integration complexity into marimo-first app.
4. Decouplability from shell/runtime details.
5. Fedora + Linux Mint packaging compatibility implications.
6. Testability/replay confidence.

## 20-Agent Assignment Matrix

1. Agent 01: EPO - command registry completeness + command domains.
2. Agent 02: EPO - settings pages/scripts + config flows.
3. Agent 03: EPO - event architecture (`listen`, `emit`, status/p2p flows).
4. Agent 04: EPO - auth/chat/p2p command path quality and risks.
5. Agent 05: EPO - UI shell layout primitives transferable to Orchestr8.
6. Agent 06: Collabkit - maestro module surface (`MaestroView`, overlays, terminal hooks).
7. Agent 07: Collabkit - file explorer + navigation + platform hooks.
8. Agent 08: Collabkit - settings system + model/provider configuration flows.
9. Agent 09: Collabkit - generator module and bridge patterns.
10. Agent 10: Collabkit - test harness, vitest/playwright, and quality gates.
11. Agent 11: DAC-O - command parsing/scaffolding pipeline reuse potential.
12. Agent 12: DAC-O - tauri/rust backend patterns, db + signaling applicability.
13. Agent 13: CLAUDE INTEGRATION PRE FIX - orchestr8 command pack salvageability.
14. Agent 14: CLAUDE INTEGRATION PRE FIX - dependency and compile-risk triage.
15. Agent 15: augment-projects/Maestro app-shell - workspace architecture + capabilities model.
16. Agent 16: augment-projects/Maestro bridge/python-runtime - host-bridge ideas for marimo integration.
17. Agent 17: maestro-scaffolder-tool - parser/scaffold utility value extraction.
18. Agent 18: Cross-repo comparison - normalize overlapping assets, detect best canonical source.
19. Agent 19: Packaging lens - Fedora/Linux Mint Tauri readiness and known blockers by repo.
20. Agent 20: Synthesis agent - aggregate all 19 reports into ranked acquisition plan.

## Synthesis Format (Agent 20)

Produce:

1. Ranked Top 5 acquisition opportunities with score + confidence.
2. "Acquire now" packet list for first 2-week sprint.
3. "Do not touch yet" list with rationale.
4. Proposed canonical source per asset family:

- settings UX
- maestro shell UI
- file explorer
- command/event bridge
- packaging baseline

Output file:

- `/home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/TAURI_SWARM_REPORTS/MASTER_SYNTHESIS.md`

## Start Command (for each agent)

Use your normal long-run kickoff flow, then begin with:

```bash
rg -n "src-tauri|tauri.conf|@tauri-apps/api|window.__TAURI__|invoke\\(" -S /home/bozertron
```

Then narrow to your assigned repo/module area.

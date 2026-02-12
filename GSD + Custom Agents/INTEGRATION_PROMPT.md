# SETTLEMENT SYSTEM → GSD INTEGRATION PROMPT

## For: Local Claude Code Instance
## Date: 2025-02-12
## Source Repository: https://github.com/gsd-build/get-shit-done.git
## Integration Source: `GSD + Custom Agents/` folder in this repo

---

## MISSION

Integrate the **Settlement System** — a tiered multi-agent architecture for large-scale codebase analysis, planning, and execution — into the existing **GSD (Get Shit Done)** framework. The Settlement System extends GSD from a solo-developer workflow tool into a scalable multi-agent deployment system capable of surveying, analyzing, planning, and executing work across codebases of any size.

**The prime directive:** Preserve GSD's rock-solid utility and reliability. The Settlement System is an **extension**, not a replacement. Every existing GSD workflow, command, agent, and template must continue to work exactly as it does today. The Settlement System adds new capabilities alongside the existing ones.

---

## WHAT IS GSD?

GSD is a meta-prompting and context-engineering system for Claude Code. It installs to `~/.claude/` and provides:

- **Agents** (`~/.claude/agents/gsd-*.md`) — Specialized Claude Code agents for planning, executing, debugging, researching, and verifying
- **Workflows** (`~/.claude/get-shit-done/workflows/*.md`) — Multi-step orchestration procedures
- **Templates** (`~/.claude/get-shit-done/templates/*`) — Structured output templates
- **Commands** (`~/.claude/commands/gsd/*.md`) — Slash commands (`/gsd:plan-phase`, `/gsd:execute-phase`, etc.)
- **Tooling** (`~/.claude/get-shit-done/bin/gsd-tools.js`) — State management, frontmatter validation, commit helpers

GSD's installer (`bin/install.js`, ~1740 lines) handles copying all files to `~/.claude/`, managing manifests, preserving local patches, and supporting multiple runtimes (Claude Code, OpenCode, Gemini).

## WHAT IS THE SETTLEMENT SYSTEM?

The Settlement System is a **"Code City" metaphor** for managing large codebases with many agents:

- **Fiefdoms** = Major subsystems (e.g., Security, P2P, Calendar)
- **Buildings** = Source files
- **Rooms** = Functions/classes within files
- **Borders** = Integration points between fiefdoms
- **Wiring** = Import/export relationships

It operates in **10 tiers**, from raw survey (Tier 1) through execution (Tier 9) to post-mortem (Tier 10), with a **City Manager** (Tier 0) orchestrating everything and a **Luminary** providing strategic oversight.

The Settlement System introduces:
- **Universal Scaling Formula** — Calculates exactly how many agents to deploy per file based on token count, complexity score, and responsibility class
- **Sentinel Protocol** — Every work unit has 3 agents (1 primary + 2 sentinels) for fault tolerance
- **Border Contracts** — Explicit allowed/forbidden crossings between fiefdoms
- **Room-Level Execution** — Agents work on specific functions, not entire files
- **Vision Alignment** — Founder walkthrough before any planning begins

---

## FILE INVENTORY & DEPLOYMENT MAP

### Category 1: Settlement Agents (19 files) → `agents/`

These are NEW agent files that go alongside the existing `gsd-*.md` agents. They use the `settlement-` prefix.

| File | Tier | Model | Role |
|------|------|-------|------|
| `settlement-city-manager.md` | 0 | sonnet-4-5 | Central orchestrator — deploys all agents, manages resources, handles failures |
| `settlement-surveyor.md` | 1 | sonnet-4-5-1m | Reads source files, catalogs rooms/tokens/exports/imports |
| `settlement-complexity-analyzer.md` | 1 | sonnet-4-5 | Scores file complexity 1-10 for scaling calculations |
| `settlement-pattern-identifier.md` | 2 | sonnet-4-5 | Identifies coding patterns, conventions, naming standards |
| `settlement-import-export-mapper.md` | 2 | sonnet-4-5 | Maps all import/export relationships, calculates coupling ratios |
| `settlement-cartographer.md` | 3 | sonnet-4-5-1m | Synthesizes survey data into definitive fiefdom maps |
| `settlement-border-agent.md` | 3 | sonnet-4-5 | Defines border contracts between fiefdoms |
| `settlement-wiring-mapper.md` | 4 | sonnet-4-5 | Validates all cross-fiefdom wiring against border contracts |
| `settlement-integration-researcher.md` | 4 | sonnet-4-5 | Researches integration approaches for cross-fiefdom work |
| `settlement-vision-walker.md` | 5 | opus-4-6 | Walks Founder through each fiefdom for vision alignment |
| `settlement-context-analyst.md` | 6 | sonnet-4-5 | Extracts and structures decisions from Vision Walker output |
| `settlement-luminary.md` | 6 | opus-4-6 | Strategic oversight — reviews plans, resolves escalations |
| `settlement-civic-council.md` | 6 | opus-4-6 | Reviews full plan for coherence, safety, alignment |
| `settlement-architect.md` | 7 | sonnet-4-5-1m | Designs implementation approach per fiefdom |
| `settlement-work-order-compiler.md` | 8 | sonnet-4-5-1m | Compiles architect plans into atomic work orders |
| `settlement-integration-synthesizer.md` | 8 | sonnet-4-5-1m | Creates integration instructions for cross-fiefdom work orders |
| `settlement-instruction-writer.md` | 8 | sonnet-4-5 | Writes zero-ambiguity "Do X Here" execution packets |
| `settlement-sentinel.md` | 9 | sonnet-4-5 | Watchdog — probes executors, investigates failures, applies fixes |
| `settlement-failure-pattern-logger.md` | 10 | sonnet-4-5 | Post-mortem — identifies recurring failure patterns |

**Deployment:** Copy each file to the GSD `agents/` directory. They should be installed alongside `gsd-*.md` agents.

**Frontmatter format:** These files use extended YAML frontmatter:
```yaml
---
name: settlement-agent-name
description: What this agent does
tools: Read, Write, Bash, Glob, Grep   # comma-separated
model: sonnet-4-5                       # or sonnet-4-5-1m or opus-4-6
tier: N
color: colorname
responsibility_class: STANDARD          # optional: STANDARD|ENRICHED|COMBINED|HEAVY|SURVEY|SYNTHESIS
responsibility_multiplier: 1.0          # optional: numeric multiplier
scaling: analysis                       # optional: scaling category
parallelization: MEDIUM                 # optional: LOW|MEDIUM|HIGH
absorbed:                               # optional: list of agents absorbed into this one
  - agent-name-1
  - agent-name-2
---
```

**IMPORTANT:** The GSD installer currently only handles `gsd-*.md` agents in its uninstall logic. The installer's `removeOldAgents()` function specifically looks for files matching the `gsd-` prefix. Settlement agents use the `settlement-` prefix, so:
1. The installer needs to be updated to also handle `settlement-*.md` agents
2. OR settlement agents can be installed in a separate step/directory

### Category 2: GSD Agent Enhancements (11 files) → MERGE into existing `agents/gsd-*.md`

These are NOT standalone agents. Each `gsd-*-enhanced.md` file contains **Settlement System enhancement sections** that must be APPENDED to the corresponding base GSD agent file.

| Enhancement File | Target Base Agent | What It Adds |
|-----------------|-------------------|--------------|
| `gsd-executor-enhanced.md` | `agents/gsd-executor.md` | Sentinel probe response, room-level execution, Settlement git commit format, failure reporting |
| `gsd-planner-enhanced.md` | `agents/gsd-planner.md` | Room-level task assignment with line ranges, agent count calculation per task |
| `gsd-debugger-enhanced.md` | `agents/gsd-debugger.md` | Sentinel failure context consumption, failure pattern lookup, prevention recommendations |
| `gsd-codebase-mapper-enhanced.md` | `agents/gsd-codebase-mapper.md` | Settlement survey output format, room-level mapping, Code City building panel data |
| `gsd-verifier-enhanced.md` | `agents/gsd-verifier.md` | Fiefdom boundary verification, border contract validation, wiring integrity checks |
| `gsd-integration-checker-enhanced.md` | `agents/gsd-integration-checker.md` | Border contract awareness, cross-fiefdom crossing validation |
| `gsd-plan-checker-enhanced.md` | `agents/gsd-plan-checker.md` | Settlement deployment validation, scaling formula verification |
| `gsd-project-researcher-enhanced.md` | `agents/gsd-project-researcher.md` | Fiefdom-aware research scoping, border-aware dependency analysis |
| `gsd-phase-researcher-enhanced.md` | `agents/gsd-phase-researcher.md` | Settlement tier awareness, fiefdom-scoped research |
| `gsd-research-synthesizer-enhanced.md` | `agents/gsd-research-synthesizer.md` | Fiefdom-level synthesis, border impact assessment, integration point identification |
| `gsd-roadmapper-enhanced.md` | `agents/gsd-roadmapper.md` | Settlement tier ordering in roadmaps, fiefdom-aware phase decomposition |

**Integration approach for each enhanced file:**
1. Read the base GSD agent file from the GSD repo
2. Read the corresponding `gsd-*-enhanced.md` file
3. Update the base agent's `description` field to include "SETTLEMENT ENHANCED" notation
4. Append the entire `## SETTLEMENT ENHANCEMENTS` section from the enhanced file to the END of the base agent file (before the closing `</success_criteria>` if one exists, or at the very end)
5. The base agent's existing content must remain UNCHANGED — only additive modifications

**Example merge result:**
```markdown
---
name: gsd-executor
description: "SETTLEMENT ENHANCED — Executes GSD plans with atomic commits... [original description]. Settlement additions: sentinel probe response, room-level execution."
tools: Read, Write, Edit, Bash, Grep, Glob
color: yellow
---

[... entire original gsd-executor.md content unchanged ...]

## SETTLEMENT ENHANCEMENTS

### Sentinel Probe Response
[... content from gsd-executor-enhanced.md ...]

### Room-Level Execution
[... content from gsd-executor-enhanced.md ...]

[... etc ...]
```

### Category 3: Settlement Workflows (5 files) → `get-shit-done/workflows/settlement/`

These define multi-step orchestration procedures for the Settlement System.

| File | Triggers | Tiers | Purpose |
|------|----------|-------|---------|
| `survey-codebase.md` | City Manager | 1, 2, 3 | Full survey pipeline: Survey → Pattern Recognition → Cartography |
| `vision-alignment.md` | City Manager | 5 | Founder walkthrough of each fiefdom before planning |
| `deploy-scaled-agents.md` | City Manager | all | Standard procedure for deploying agents using Universal Scaling Formula |
| `sentinel-protocol.md` | All execution deployments | 9 | Sentinel probe/investigate/fix cycle |
| `border-validation.md` | Border Agent | 3, 4 | Cross-fiefdom border crossing validation |

**Deployment:** Create directory `get-shit-done/workflows/settlement/` and copy these files there.

**Note:** `vision-alignment.md` model field has already been updated to `opus-4-6`.

### Category 4: Settlement Templates (6 files) → `get-shit-done/templates/settlement/`

These define structured output formats used by Settlement agents.

| File | Used By | Purpose |
|------|---------|---------|
| `border-contract.md` | Border Agent | Template for fiefdom border contracts |
| `building-panel.md` | Surveyor, Cartographer | ASCII art building info panel for Code City |
| `deployment-plan.md` | City Manager, Cartographer | Deployment plan with agent counts and waves |
| `failure-pattern.md` | Failure Pattern Logger | Failure pattern entry format |
| `fiefdom-map.md` | Cartographer | Fiefdom map entry format |
| `work-order.md` | Work Order Compiler | Atomic work order format |

**Deployment:** Create directory `get-shit-done/templates/settlement/` and copy these files there.

### Category 5: Reference Documents (NOT deployed — for human reference only)

These files are architectural documentation and should NOT be deployed to `~/.claude/`. They remain in this repository for reference.

| File | Purpose |
|------|---------|
| `SETTLEMENT_SYSTEM_PRESSURE_TEST.md` | **Canonical architecture specification** — defines all agents, tiers, models, absorption decisions, scaling formulas. THE source of truth. |
| `SCALING_REFERENCE.md` | Responsibility class multipliers (v4.1). Content already integrated into city-manager, cartographer, and deploy-scaled-agents workflow. |
| `OPUS_HANDOFF_PROMPT.md` | Original design prompt that generated the Settlement System |
| `CONSOLIDATION_PROMPT.md` | Instructions used for the deduplication/consolidation pass |
| `CONSOLIDATION_REPORT.md` | Results of the consolidation pass |
| `The_Story_of_Mingos_A_Tale_of_Emergence.md` | Origin story (narrative context) |

---

## INSTALLER UPDATES (`bin/install.js`)

The GSD installer needs modifications to handle Settlement System files:

### 1. Agent Installation

Currently, `removeOldAgents()` (around line 467) specifically removes `gsd-*.md` files:
```javascript
const isGsdAgent = file.startsWith('gsd-') && file.endsWith('.md');
```

**Required change:** Also handle `settlement-*.md` agents:
```javascript
const isGsdAgent = file.startsWith('gsd-') && file.endsWith('.md');
const isSettlementAgent = file.startsWith('settlement-') && file.endsWith('.md');
if (isGsdAgent || isSettlementAgent) { ... }
```

### 2. Workflow Directory

Currently, workflows are copied from `get-shit-done/workflows/*.md` (flat directory).

**Required change:** Also copy `get-shit-done/workflows/settlement/*.md` to `~/.claude/get-shit-done/workflows/settlement/`. The installer should:
1. Create the `settlement/` subdirectory if it doesn't exist
2. Copy all settlement workflow files
3. Include them in the manifest for tracking

### 3. Template Directory

Same pattern as workflows — create `get-shit-done/templates/settlement/` and copy template files there.

### 4. Manifest Updates

The installer's manifest system tracks all installed files. Settlement files need to be included in the manifest so they're properly tracked during updates and uninstalls.

### 5. Frontmatter Handling

The installer converts frontmatter for different runtimes (OpenCode, Gemini). Settlement agent frontmatter includes additional fields (`model`, `tier`, `responsibility_class`, etc.) that the base GSD frontmatter doesn't have. The installer should:
- Preserve these fields for Claude Code (they're used by the Settlement System's orchestration)
- Strip or convert them appropriately for other runtimes

---

## INTEGRATION SEQUENCE

Execute these steps in order:

### Step 1: Clone and Understand
```bash
git clone https://github.com/gsd-build/get-shit-done.git
cd get-shit-done
```
Read `bin/install.js` to understand the current installation flow. Key functions:
- `installGlobal()` / `installLocal()` — Main installation paths
- `removeOldAgents()` — Cleans old agent files before installing new ones
- `copyAgents()` — Copies agent .md files to ~/.claude/agents/
- `copyWorkflows()` — Copies workflow files
- `copyTemplates()` — Copies template files
- `updateManifest()` — Tracks installed files

### Step 2: Add Settlement Agents to `agents/`
Copy all 19 `settlement-*.md` files into the GSD repo's `agents/` directory.

### Step 3: Merge Enhancements into Base GSD Agents
For each of the 11 `gsd-*-enhanced.md` files:
1. Open the corresponding base agent in `agents/gsd-*.md`
2. Add "SETTLEMENT ENHANCED" to the description
3. Add the `settlement_enhancements` list to the frontmatter
4. Append the `## SETTLEMENT ENHANCEMENTS` section and all its subsections to the end of the file
5. Verify the base agent's original content is completely unchanged

### Step 4: Create Settlement Workflow Directory
```bash
mkdir -p get-shit-done/workflows/settlement
```
Copy the 5 workflow/protocol files there. Update `vision-alignment.md`'s model field from `opus` to `opus-4-6`.

### Step 5: Create Settlement Template Directory
```bash
mkdir -p get-shit-done/templates/settlement
```
Copy the 6 template files there.

### Step 6: Update Installer
Modify `bin/install.js` to:
1. Handle `settlement-*.md` agents in removal/installation
2. Copy settlement workflows subdirectory
3. Copy settlement templates subdirectory
4. Update manifest to include settlement files

### Step 7: Create Settlement Commands (Optional — Future Work)
Consider creating slash commands for Settlement operations:
- `/gsd:settlement-survey` — Run the survey-codebase workflow
- `/gsd:settlement-plan` — Run vision alignment + planning tiers
- `/gsd:settlement-execute` — Run execution tiers with sentinel deployment
- `/gsd:settlement-status` — Show fiefdom status and deployment progress

### Step 8: Test
1. Run `npm install` (or the GSD install process) in a test environment
2. Verify all existing GSD agents still install and work correctly
3. Verify settlement agents are installed to `~/.claude/agents/`
4. Verify settlement workflows are installed to `~/.claude/get-shit-done/workflows/settlement/`
5. Verify settlement templates are installed to `~/.claude/get-shit-done/templates/settlement/`
6. Verify enhanced GSD agents contain both original content AND settlement enhancements

---

## ARCHITECTURAL PRINCIPLES TO PRESERVE

### GSD Principles (DO NOT BREAK)
1. **Plans are prompts** — PLAN.md IS the prompt, not a document that becomes one
2. **2-3 tasks per plan** — Context budget management (50% target)
3. **Goal-backward methodology** — Derive requirements from observable truths
4. **Atomic commits** — One commit per task, proper conventional commit format
5. **State management** — STATE.md + gsd-tools.js for tracking progress
6. **Deviation rules** — Rules 1-3 auto-fix, Rule 4 asks (architectural changes)
7. **Checkpoint protocol** — human-verify / decision / human-action types

### Settlement Principles (NEW — must coexist)
1. **Universal Scaling Formula** — `effective_tokens = file_tokens × complexity_multiplier × responsibility_multiplier; agents = ceil(effective_tokens / 2500) × 3`
2. **Sentinel invariant** — Always 3 agents per active work unit (1 primary + 2 sentinels)
3. **Explicit boundaries** — Every file has exactly ONE fiefdom assignment. No ambiguity.
4. **Border contracts** — Cross-fiefdom imports/exports must be explicitly allowed
5. **Room-level execution** — Agents work on specific functions, not whole files
6. **Tier ordering** — Survey (1) → Pattern (2) → Cartography (3) → Wiring (4) → Vision (5) → Context/Strategy (6) → Architecture (7) → Work Orders (8) → Execution (9) → Post-mortem (10)
7. **Founder terminology** — The human user is "Founder" in the Settlement metaphor (not "Emperor")

### Coexistence Rules
- When Settlement System is NOT active, GSD operates exactly as before — no behavioral changes
- When Settlement System IS active (triggered by survey-codebase workflow or settlement commands), the enhanced sections in GSD agents activate
- Settlement agents are only spawned by the City Manager or Settlement workflows — they don't interfere with normal GSD agent spawning
- The `.planning/settlement/` directory is used for all Settlement artifacts, keeping them separate from GSD's `.planning/phases/` structure

---

## MODEL REFERENCE

| Model ID | Context | Used By | Count |
|----------|---------|---------|-------|
| `opus-4-6` | 200K | Luminary, Civic Council, Vision Walker | 3 agents |
| `sonnet-4-5` | 200K | City Manager, Border Agent, Complexity Analyzer, Context Analyst, Failure Pattern Logger, Import/Export Mapper, Instruction Writer, Integration Researcher, Pattern Identifier, Sentinel, Wiring Mapper | 11 agents |
| `sonnet-4-5-1m` | 1M | Surveyor, Cartographer, Architect, Work Order Compiler, Integration Synthesizer | 5 agents |

**Opus** agents handle nuanced interaction and strategic oversight.
**Sonnet** agents handle fast operational work.
**1M Sonnet** agents handle synthesis tasks requiring massive context (holding data from hundreds of files simultaneously).

---

## RESPONSIBILITY CLASSES

Used by the Universal Scaling Formula to adjust agent deployment counts:

| Class | Multiplier | Used By |
|-------|-----------|---------|
| STANDARD | 1.0 | Most agents (default) |
| ENRICHED | 1.2 | Instruction Writer (captures more detail) |
| COMBINED | 1.3 | Context Analyst (absorbed two roles) |
| HEAVY | 1.4 | Reserved for future use |
| SURVEY | 1.6 | Surveyor (reads raw files, heavy extraction) |
| SYNTHESIS | 1.8 | Cartographer (synthesizes ALL prior tier outputs) |

---

## COLOR SYSTEM

| Color | Hex | Meaning |
|-------|-----|---------|
| Gold | #D4AF37 | Working / healthy / verified |
| Teal | #1fbdea | Needs work / needs rewiring / unverified |
| Purple | #9D4EDD | Agents actively deployed / in combat |
| Blue | — | City Manager operations |
| Green | — | Pattern identification |
| Yellow | — | Execution / instruction writing |
| Orange | — | Warning / debugging |

---

## SETTLEMENT OUTPUT DIRECTORY STRUCTURE

When the Settlement System runs, it produces artifacts under `.planning/settlement/`:

```
.planning/
├── settlement/
│   ├── surveys/           # Tier 1: One JSON per surveyed file
│   ├── complexity/        # Tier 1: Complexity scores per file
│   ├── patterns/          # Tier 2: PATTERN_REGISTRY.json
│   ├── wiring/            # Tier 2: IMPORT_EXPORT_MAP.json
│   ├── borders/           # Tier 3: One contract per border pair
│   ├── FIEFDOM_MAP.json   # Tier 3: Definitive fiefdom map
│   ├── DEPLOYMENT_PLAN.json # Tier 3: Agent deployment calculations
│   ├── VISION_ALIGNMENT.md  # Tier 5: Founder's locked/flexible/deferred decisions
│   ├── CONTEXT.md         # Tier 6: Structured context for downstream agents
│   ├── architecture/      # Tier 7: Per-fiefdom architecture plans
│   ├── work-orders/       # Tier 8: Atomic work orders
│   ├── execution-packets/  # Tier 8: "Do X Here" instruction packets
│   └── failure-patterns/   # Tier 10: FAILURE_PATTERNS.md
├── phases/                # Existing GSD phase structure (unchanged)
├── STATE.md               # Existing GSD state (unchanged)
├── ROADMAP.md             # Existing GSD roadmap (unchanged)
└── PROJECT.md             # Existing GSD project (unchanged)
```

---

## CRITICAL WARNINGS

1. **DO NOT modify existing GSD agent behavior** — Enhanced agents must be purely additive. The `## SETTLEMENT ENHANCEMENTS` section activates only when Settlement System is in use.

2. **DO NOT change GSD's .planning/ structure** — Settlement artifacts go in `.planning/settlement/`. The existing `phases/`, `STATE.md`, `ROADMAP.md`, etc. are untouched.

3. **DO NOT change the GSD tools** (`gsd-tools.js`) — Settlement orchestration uses its own coordination through the City Manager agent, not through modifications to gsd-tools.

4. **DO NOT rename existing GSD agents** — The `gsd-` prefix must remain. Settlement enhancements are appended, not replacing.

5. **DO NOT change existing GSD commands** — Settlement gets its own commands (in a future step), separate from existing `/gsd:*` commands.

6. **Preserve the installer's local patch system** — When users have locally modified GSD agents, the installer backs up their changes before updating. This must continue to work with the settlement enhancements.

---

## VALIDATION CHECKLIST

After integration is complete, verify:

- [ ] All 11 existing GSD agents still have their complete original content
- [ ] All 11 enhanced GSD agents have the `## SETTLEMENT ENHANCEMENTS` section appended
- [ ] All 19 settlement agents are in `agents/` with correct frontmatter
- [ ] All 5 settlement workflows are in `get-shit-done/workflows/settlement/`
- [ ] All 6 settlement templates are in `get-shit-done/templates/settlement/`
- [ ] `bin/install.js` handles `settlement-*.md` agents
- [ ] `bin/install.js` copies settlement workflow and template subdirectories
- [ ] Running `npm install` installs everything correctly
- [ ] Running `npm uninstall` removes settlement files
- [ ] Existing GSD test suite passes (if one exists)
- [ ] No reference documents (PRESSURE_TEST, SCALING_REFERENCE, etc.) are deployed to ~/.claude/
- [ ] `vision-alignment.md` model field reads `opus-4-6` (not `opus`)
- [ ] All frontmatter `model:` fields use explicit version IDs (sonnet-4-5, sonnet-4-5-1m, opus-4-6)

---

## SUMMARY

| Category | Count | Destination |
|----------|-------|-------------|
| New settlement agents | 19 | `agents/settlement-*.md` |
| Enhanced GSD agents | 11 | Merged into existing `agents/gsd-*.md` |
| Settlement workflows | 5 | `get-shit-done/workflows/settlement/` |
| Settlement templates | 6 | `get-shit-done/templates/settlement/` |
| Installer updates | 1 | `bin/install.js` |
| Reference docs (not deployed) | 6 | Stay in source repo |
| **Total files to deploy** | **41** | |

The Settlement System transforms GSD from a capable solo-developer tool into a scalable multi-agent orchestration platform — while keeping every existing GSD capability intact and unchanged.

# Settlement System Implementation Prompt

## For: Opus Instance

## Purpose: Generate all agent prompts and GSD modifications for the Settlement System

---

## CRITICAL CONTEXT

You are implementing "The Settlement System" — an enhancement to the GSD (Get Shit Done) framework that adds:

1. **Universal Scaling**: Every agent type scales with token count + complexity
2. **Rolling Sentinels**: Always 3 agents on site per work unit
3. **Code City Integration**: Visual representation of codebase as a city
4. **Vision Alignment**: Founder walkthrough before planning
5. **42 Total Agent Types**: 11 existing GSD + 31 new Settlement agents

**GSD is already installed.** You are MODIFYING it, not replacing it.

---

## REFERENCE MATERIALS

### GSD Repository Structure (Already Installed)

```
~/.claude/
├── agents/
│   ├── gsd-codebase-mapper.md      # Existing - enhance
│   ├── gsd-debugger.md             # Existing - enhance
│   ├── gsd-executor.md             # Existing - enhance
│   ├── gsd-integration-checker.md  # Existing - enhance
│   ├── gsd-phase-researcher.md     # Existing - enhance
│   ├── gsd-plan-checker.md         # Existing - enhance
│   ├── gsd-planner.md              # Existing - enhance
│   ├── gsd-project-researcher.md   # Existing - enhance
│   ├── gsd-research-synthesizer.md # Existing - enhance
│   ├── gsd-roadmapper.md           # Existing - enhance
│   └── gsd-verifier.md             # Existing - enhance
├── get-shit-done/
│   ├── templates/                  # Document templates
│   ├── workflows/                  # Workflow definitions
│   ├── references/                 # Reference docs
│   └── bin/                        # Tools
└── commands/
    └── gsd/                        # Slash commands
```

### Files You Must Read First

Before generating ANY output, read these files to understand GSD's patterns:

1. `~/.claude/agents/gsd-executor.md` — Understand executor pattern
2. `~/.claude/agents/gsd-planner.md` — Understand planner pattern
3. `~/.claude/agents/gsd-verifier.md` — Understand verification pattern
4. `~/.claude/get-shit-done/workflows/execute-phase.md` — Understand workflow orchestration
5. `~/.claude/get-shit-done/workflows/plan-phase.md` — Understand planning workflow
6. `~/.claude/get-shit-done/templates/state.md` — Understand state management

---

## CODE CITY ARCHITECTURE

### Hierarchy

```
THE VOID (entire codebase)
└── FIEFDOMS (feature neighborhoods)
    ├── Security Fiefdom
    ├── P2P Fiefdom
    ├── Calendar Fiefdom
    ├── VS Code Module Fiefdom
    ├── Visual Particle Expression Fiefdom
    ├── LLM Prompt Builder Fiefdom
    └── PRD Generator Fiefdom
        └── BUILDINGS (files)
            ├── Height = export count
            ├── Footprint = line count
            ├── PANEL (front sign) = imports, exports, functions, state, wiring
            └── ROOMS (logic blocks)
                └── One room per function/class/block
                └── Can be inspected, fixed, tested individually
```

### Borders

Between each fiefdom is a BORDER that:

- Dictates where an agent's work starts and stops
- Defines what should be coming IN (imports, types, data)
- Defines what should be going OUT (exports, interfaces, events)

### Border Agents

Special agents whose ONLY job is understanding:

- What structures/types should cross the border
- What the contract is between fiefdoms
- When something violates the border contract

### Building Panel Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BUILDING: filename.ts                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  IMPORTS              │  EXPORTS              │  FUNCTIONS                  │
│  ────────             │  ────────             │  ──────────                 │
│  ○ moduleA            │  ● funcX              │  ◆ funcX()       [GOLD]     │
│  ○ moduleB            │  ● ClassY             │  ◆ funcY()       [TEAL]     │
│  ○ utilC              │  ● constZ             │  ◆ ClassY        [GOLD]     │
│                       │                       │  ◆ helper()      [PURPLE]   │
├─────────────────────────────────────────────────────────────────────────────┤
│  WIRING:                                                                    │
│  → moduleA.funcQ() [TEAL - needs rewiring]                                  │
│  → utilC.parse() [GOLD - working]                                           │
│  ← ClassY consumed by fileD.ts [GOLD]                                       │
│  ← funcX consumed by fileE.ts [TEAL - consumer broken]                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  AGENTS: 24 assigned │ 18 complete │ 6 active                               │
└─────────────────────────────────────────────────────────────────────────────┘

Colors:
• GOLD (#D4AF37) = working
• TEAL (#1fbdea) = needs work / needs rewiring
• PURPLE (#9D4EDD) = agents actively deployed
```

### Rooms (Logic Blocks)

Each room is ONE logic block:

- A function
- A class
- A significant code block

Rooms can be:

- Visually inspected in Code City
- Fixed individually
- Tested individually
- Assigned to specific agents

---

## UNIVERSAL SCALING FORMULA

**This applies to EVERY agent type in EVERY tier.**

```
INPUTS:
  file_tokens = approximate token count of target
  complexity_score = 1-10 based on nesting, dependencies, patterns

CONSTANTS (conservative):
  MAX_TOKENS_PER_AGENT = 2,500 tokens (leaves massive reasoning space)
  COMPLEXITY_MULTIPLIER = 1.0 + (complexity_score × 0.1)

FORMULA:
  effective_tokens = file_tokens × COMPLEXITY_MULTIPLIER
  work_units = ceil(effective_tokens / MAX_TOKENS_PER_AGENT)
  agents_per_work_unit = 3 (rolling sentinel deployment)
  ═══════════════════════════════════════════════════════════════
  TOTAL_AGENTS = work_units × 3

EXAMPLES:
  138KB file (35K tokens, complexity 7):
    effective = 35000 × 1.7 = 59,500
    work_units = ceil(59500 / 2500) = 24
    TOTAL_AGENTS = 24 × 3 = 72 agents

  P2P module (200K tokens, complexity 9):
    effective = 200000 × 1.9 = 380,000
    work_units = ceil(380000 / 2500) = 152
    TOTAL_AGENTS = 152 × 3 = 456 agents

  Small util (2.5K tokens, complexity 3):
    effective = 2500 × 1.3 = 3,250
    work_units = ceil(3250 / 2500) = 2
    TOTAL_AGENTS = 2 × 3 = 6 agents
```

---

## ROLLING SENTINEL DEPLOYMENT

**Always 3 agents on site per work unit.**

```
INITIAL STATE:
  Agent 1 = PRIMARY (attempts work)
  Agent 2 = SENTINEL (probes Agent 1 every 30s)
  Agent 3 = SENTINEL (probes Agent 1 every 30s, offset 15s)

SCENARIO A: Agent 1 SUCCEEDS
  • Agent 1 moves to completion
  • Agent 4 deploys (new primary for next work unit)
  • Agents 2 & 3 shift to watch Agent 4
  • Always 3 on site

SCENARIO B: Agent 1 FAILS
  • Agent 2 investigates root cause (Agent 3 watches Agent 2)
  • Agent 4 deploys immediately (maintains 3 on site)

  IF Agent 2 finds fix:
    • Agent 2 applies fix
    • Agent 4 becomes new primary (with fix context)
    • Agents 3 & 5 (new) watch Agent 4

  IF Agent 2 ALSO fails:
    • Agent 3 releases Agents 5 & 6 with combined failure notes
    • Agent 5 becomes primary, Agents 6 & 7 watch
    • Rinse, repeat until solved

INVARIANT: There are ALWAYS 3 agents on site for any active work unit
```

---

## MODEL ASSIGNMENTS

| Role | Model | Reason |
|------|-------|--------|
| Luminary | Opus | Deep reasoning, architectural decisions |
| Vision Walker | Opus | Nuanced founder interaction |
| Validators | Opus | Quality verification, cleanup |
| Surveyors | 1M Sonnet | Need to read lots of files |
| Cartographers | 1M Sonnet | Synthesize massive survey data |
| Integration Synthesizers | 1M Sonnet | Hold all connection points |
| Architects | 1M Sonnet | Complex design spanning fiefdoms |
| Research Synthesizer | 1M Sonnet | Hold all research findings |
| Work Order Compiler | 1M Sonnet | Needs full picture |
| All execution agents | Sonnet | Fast, focused, atomic tasks |
| Sentinels | Sonnet | Quick probe/investigate cycles |
| Border Agents | Sonnet | Focused contract validation |

---

## THE 11 TIERS

### Tier 0: Coordination (Always Active)

- Luminary, City Manager, District Planner, Git Commit Agent, Scaler, Civic Council
- NOT scaled — fixed coordination layer

### Tier 1: Survey & Measurement

- Surveyors, Complexity Analyzers, File Structure Mappers, Token Counters
- SCALED per target

### Tier 2: Pattern Recognition

- Pattern Identifiers, Import/Export Mappers, Filepath Analyzers, Function Catalogers
- SCALED per target

### Tier 3: Cartography & Synthesis

- Cartographers, District Boundary Definers, Token Budget Calculators, Deployment Planners, Integration Point Mappers
- SCALED per aggregated input

### Tier 4: Research (GSD Enhanced)

- gsd-project-researcher, gsd-phase-researcher, gsd-research-synthesizer, Integration Researcher
- SCALED per fiefdom

### Tier 5: Vision Alignment (NEW)

- Vision Walker (Opus) — walks Founder through each section for feedback
- Before ANY planning begins

### Tier 6: Requirements & Roadmap (GSD Core)

- gsd-roadmapper, Discussion Analyzer, Context Writer
- SCALED per scope

### Tier 7: Planning (GSD Enhanced)

- gsd-planner, gsd-plan-checker, Architect, Work Order Compiler
- SCALED per phase scope

### Tier 8: Pre-Execution Synthesis (NEW)

- Integration Synthesizers, Wiring Mappers, Instruction Writers, Atomic Task Generators
- SCALED per plan complexity

### Tier 9: Execution (ALL AT END)

- gsd-executor (Builder), Sentinels, Relief Deployers
- SCALED per target + rolling deployment

### Tier 10: Validation (ALL AT END)

- gsd-verifier, gsd-integration-checker, gsd-debugger, Failure Pattern Logger
- SCALED per execution output
- Uses OPUS for validation and cleanup

---

## COMPLETE AGENT INVENTORY (42 Agents)

### GSD Agents to ENHANCE (11)

Create modifications to these existing files:

#### 1. `gsd-codebase-mapper.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-codebase-mapper.md`
**Modification:** Add fiefdom detection, border identification, token counting per file
**New sections to add:**

- Fiefdom boundary detection based on directory structure and coupling
- Border contract inference (what types/data cross boundaries)
- Token count per file output
- Complexity score calculation

#### 2. `gsd-project-researcher.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-project-researcher.md`
**Modification:** Add fiefdom-aware research, integration point discovery
**New sections to add:**

- Research per fiefdom (not just global)
- Integration point catalog per border
- Dependency direction analysis

#### 3. `gsd-research-synthesizer.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-research-synthesizer.md`
**Modification:** Add fiefdom map generation, token budget recommendations
**New sections to add:**

- Fiefdom map output (visual representation)
- Agent deployment recommendations per fiefdom
- Border contract summary

#### 4. `gsd-roadmapper.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-roadmapper.md`
**Modification:** Add fiefdom-based phase organization
**New sections to add:**

- Organize phases by fiefdom
- Include border work as explicit phases
- Include agent count estimates per phase

#### 5. `gsd-phase-researcher.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-phase-researcher.md`
**Modification:** Add room-level analysis, wiring research
**New sections to add:**

- Room (logic block) identification
- Wiring state per room (Gold/Teal/Purple)
- Integration point status

#### 6. `gsd-planner.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-planner.md`
**Modification:** Add "Do X Here" instruction format, room-level task assignment
**New sections to add:**

- Task format: explicit filepath + line range + exact action
- Room assignment (which logic block)
- Agent count calculation per task

#### 7. `gsd-plan-checker.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-plan-checker.md`
**Modification:** Add scaling validation, border contract checking
**New sections to add:**

- Verify agent counts match token/complexity
- Verify border contracts are maintained
- Verify room assignments are valid

#### 8. `gsd-executor.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-executor.md`
**Modification:** Add rolling sentinel awareness, room-level execution
**New sections to add:**

- Sentinel probe response protocol
- Room-level git commits
- Failure reporting format for sentinel consumption

#### 9. `gsd-verifier.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-verifier.md`
**Modification:** Add border contract verification, wiring state update
**New sections to add:**

- Border contract validation
- Wiring state update (Gold/Teal/Purple)
- Room-level verification

#### 10. `gsd-integration-checker.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-integration-checker.md`
**Modification:** Add fiefdom border validation
**New sections to add:**

- Cross-fiefdom integration validation
- Border contract compliance check
- Wiring consistency check

#### 11. `gsd-debugger.md` — ENHANCE

**Location:** `~/.claude/agents/gsd-debugger.md`
**Modification:** Add sentinel failure analysis, pattern logging
**New sections to add:**

- Sentinel failure context consumption
- Root cause pattern identification
- Future prevention recommendations

---

### NEW Settlement Agents to CREATE (31)

Create these new files in `~/.claude/agents/settlement/`:

#### Tier 0: Coordination (6 agents)

##### 12. `settlement-luminary.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-luminary.md`
**Model:** Opus
**Purpose:** Holds vision, makes architectural decisions, protects own context window
**Prompt must include:**

- Role: Strategic coordinator, NOT executor
- Responsibilities: Vision alignment, architectural decisions, escalation handling
- Context protection: Delegate all heavy work to sub-agents
- Interaction style: Deep reasoning, Socratic questioning with Founder
- Output format: Strategic decisions, delegation instructions

##### 13. `settlement-city-manager.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-city-manager.md`
**Model:** Sonnet
**Purpose:** Orchestrates all agent deployment across all tiers
**Prompt must include:**

- Role: Deployment orchestrator
- Responsibilities: Apply scaling formula, spawn agents, track progress, handle failures
- Input: Fiefdom maps, token budgets, deployment plans
- Output: Deployment logs, progress reports, escalations
- Integration: Calls Scaler for calculations, Relief Deployer for failures

##### 14. `settlement-district-planner.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-district-planner.md`
**Model:** Sonnet
**Purpose:** Manages resources per fiefdom
**Prompt must include:**

- Role: Fiefdom resource manager
- Responsibilities: Allocate agents to fiefdom, track fiefdom progress, manage borders
- Input: Fiefdom map, token budgets per fiefdom
- Output: Fiefdom deployment plan, border agent assignments

##### 15. `settlement-git-commit-agent.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-git-commit-agent.md`
**Model:** Sonnet
**Purpose:** Handles atomic commits after EACH work unit
**Prompt must include:**

- Role: Git operations ONLY
- Responsibilities: Stage files, write commit message, commit, verify
- Trigger: After EVERY work unit completion (not batched)
- Commit message format: `[Tier X][Fiefdom][Room] description`
- Verification: Confirm commit succeeded before reporting

##### 16. `settlement-scaler.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-scaler.md`
**Model:** Sonnet
**Purpose:** Applies Universal Scaling Formula to any target
**Prompt must include:**

- Role: Calculator
- Input: file_tokens, complexity_score
- Formula: (see Universal Scaling Formula above)
- Output: work_units, total_agents, deployment_plan
- Validation: Warn if agents > 100 for single target (sanity check)

##### 17. `settlement-civic-council.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-civic-council.md`
**Model:** Opus
**Purpose:** Human advocacy — reviews before ANY merge
**Prompt must include:**

- Role: Founder advocate
- Responsibilities: Review all changes for user impact, veto harmful changes
- Analysis framework:
  1. Does this serve the Founder's vision?
  2. Does this create technical debt?
  3. Is this the complete solution or a shortcut?
  4. Would this delight or frustrate the user?
- Veto power: Can block merge with explanation
- Output: ADVOCACY_REPORT.md with recommendation (APPROVE/MODIFY/BLOCK)

---

#### Tier 1: Survey & Measurement (4 agents)

##### 18. `settlement-surveyor.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-surveyor.md`
**Model:** 1M Sonnet
**Purpose:** Measures token count per file/section
**Prompt must include:**

- Role: Measurer (read-only)
- Input: File path or directory
- Process: Read file, count tokens per section, identify room boundaries
- Output format:

  ```json
  {
    "file": "path/to/file.ts",
    "total_tokens": 5000,
    "rooms": [
      {"name": "functionA", "line_start": 10, "line_end": 50, "tokens": 800},
      {"name": "ClassB", "line_start": 52, "line_end": 200, "tokens": 2500}
    ]
  }
  ```

- Parallelization: HIGH (read-only, no collisions)

##### 19. `settlement-complexity-analyzer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-complexity-analyzer.md`
**Model:** Sonnet
**Purpose:** Calculates complexity score (1-10)
**Prompt must include:**

- Role: Analyzer (read-only)
- Complexity factors:
  - Nesting depth (max depth × 0.5)
  - Cyclomatic complexity (branches × 0.3)
  - Dependency count (imports × 0.2)
  - Cross-fiefdom dependencies (× 1.5 multiplier)
- Output: complexity_score (1-10), breakdown of factors

##### 20. `settlement-file-structure-mapper.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-file-structure-mapper.md`
**Model:** Sonnet
**Purpose:** Maps internal file structure (rooms)
**Prompt must include:**

- Role: Structure mapper (read-only)
- Identify: Functions, classes, significant blocks
- Output: Room list with boundaries, relationships between rooms
- Integration: Feeds into Code City building representation

##### 21. `settlement-token-counter.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-token-counter.md`
**Model:** Sonnet
**Purpose:** Precise token counting for budget allocation
**Prompt must include:**

- Role: Counter (read-only)
- Method: Use tiktoken or equivalent for precise counts
- Output: Exact token counts per room, per file, per fiefdom
- Aggregation: Sum up hierarchy (room → file → fiefdom → total)

---

#### Tier 2: Pattern Recognition (4 agents)

##### 22. `settlement-pattern-identifier.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-pattern-identifier.md`
**Model:** Sonnet
**Purpose:** Identifies code patterns, idioms, conventions
**Prompt must include:**

- Role: Pattern detector (read-only)
- Detect: Design patterns, coding conventions, idioms, anti-patterns
- Output: Pattern registry with locations, consistency assessment

##### 23. `settlement-import-export-mapper.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-import-export-mapper.md`
**Model:** Sonnet
**Purpose:** Maps all imports/exports per file
**Prompt must include:**

- Role: Dependency mapper (read-only)
- Track: Every import statement, every export
- Output: Import graph, export catalog, wiring data for Code City panel
- Border detection: Flag cross-fiefdom imports

##### 24. `settlement-filepath-analyzer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-filepath-analyzer.md`
**Model:** Sonnet
**Purpose:** Analyzes file paths, naming conventions, relationships
**Prompt must include:**

- Role: Path analyzer (read-only)
- Detect: Naming conventions, directory patterns, fiefdom boundaries
- Output: Fiefdom suggestions based on path structure

##### 25. `settlement-function-cataloger.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-function-cataloger.md`
**Model:** Sonnet
**Purpose:** Catalogs all functions/classes with signatures
**Prompt must include:**

- Role: Cataloger (read-only)
- Catalog: Function name, parameters, return type, JSDoc/docstring
- Output: Searchable function catalog, API surface per file

---

#### Tier 3: Cartography & Synthesis (6 agents including Border Agent)

##### 26. `settlement-cartographer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-cartographer.md`
**Model:** 1M Sonnet
**Purpose:** Synthesizes surveys into fiefdom maps
**Prompt must include:**

- Role: Map maker
- Input: All survey outputs from Tier 1-2
- Process: Aggregate, identify clusters, draw boundaries
- Output: Fiefdom map with:
  - Fiefdom names and boundaries
  - Building (file) list per fiefdom
  - Total tokens per fiefdom
  - Recommended agent counts

##### 27. `settlement-district-boundary-definer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-district-boundary-definer.md`
**Model:** Sonnet
**Purpose:** Defines fiefdom boundaries based on coupling
**Prompt must include:**

- Role: Boundary analyst
- Criteria: High internal coupling, low external coupling
- Output: Boundary definitions, border crossing points

##### 28. `settlement-token-budget-calculator.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-token-budget-calculator.md`
**Model:** Sonnet
**Purpose:** Conservative budget allocation
**Prompt must include:**

- Role: Budget allocator
- Principle: Cap raw info at 40% of context, leave 60% for reasoning
- Output: Token budget per fiefdom, per phase, per agent

##### 29. `settlement-deployment-planner.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-deployment-planner.md`
**Model:** Sonnet
**Purpose:** Plans agent quantities per target
**Prompt must include:**

- Role: Deployment calculator
- Input: Token counts, complexity scores
- Apply: Universal Scaling Formula
- Output: Agent deployment plan with exact counts per target

##### 30. `settlement-integration-point-mapper.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-integration-point-mapper.md`
**Model:** Sonnet
**Purpose:** Maps all integration points across fiefdoms
**Prompt must include:**

- Role: Integration mapper (read-only)
- Identify: Every point where fiefdoms connect
- Output: Integration point registry, border crossing catalog

##### 31. `settlement-border-agent.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-border-agent.md`
**Model:** Sonnet
**Purpose:** Understands what should cross fiefdom borders
**Prompt must include:**

- Role: Border guardian
- Responsibilities:
  - Define what structures/types should cross each border
  - Define the contract between fiefdoms
  - Detect violations of border contracts
- Input: Integration point map, import/export data
- Output: Border contracts per fiefdom pair:

  ```json
  {
    "border": "Security ↔ P2P",
    "allowed_in": ["AuthToken", "UserCredentials"],
    "allowed_out": ["PeerConnection", "EncryptedPayload"],
    "forbidden": ["RawPassword", "PrivateKey"],
    "contract_version": "1.0"
  }
  ```

---

#### Tier 4: Research Enhancement (1 agent)

##### 32. `settlement-integration-researcher.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-integration-researcher.md`
**Model:** Sonnet
**Purpose:** Deep research on integration patterns
**Prompt must include:**

- Role: Integration specialist researcher
- Focus: How fiefdoms currently integrate, how they should integrate
- Output: Integration research document per border

---

#### Tier 5: Vision Alignment (1 agent)

##### 33. `settlement-vision-walker.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-vision-walker.md`
**Model:** OPUS
**Purpose:** Walks Founder through each section for detailed feedback
**Prompt must include:**

- Role: Vision alignment facilitator
- Timing: BEFORE any planning begins
- Process:
  1. Present fiefdom/feature being addressed
  2. Explain current understanding of vision for that area
  3. Propose approach
  4. Ask clarifying questions
  5. Capture Founder feedback
  6. Confirm alignment before proceeding
- Interaction style: Conversational, Socratic, patient
- Output: Vision-aligned specification with Founder approval recorded
- Example dialogue:

  ```
  "I'd like to walk you through the Security fiefdom.

   Currently, I see these buildings:
   - auth.ts (login, logout, token refresh)
   - permissions.ts (role-based access)
   - encryption.ts (data encryption utilities)

   My understanding of your vision:
   - Security should be invisible to users but absolute
   - No user action should ever expose credentials

   Proposed approach:
   - Treat auth.ts as the single entry point
   - permissions.ts only consulted by auth.ts

   Questions:
   1. Should encryption.ts be accessible from other fiefdoms, or only through Security?
   2. Are there any security patterns from your hardware background you want reflected?

   Does this match your vision?"
  ```

---

#### Tier 6: Requirements & Roadmap (2 agents)

##### 34. `settlement-discussion-analyzer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-discussion-analyzer.md`
**Model:** Sonnet
**Purpose:** Analyzes Founder feedback from Vision Walker
**Prompt must include:**

- Role: Feedback processor
- Input: Vision Walker conversation transcript
- Output: Structured decisions, constraints, preferences
- Format: CONTEXT.md updates

##### 35. `settlement-context-writer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-context-writer.md`
**Model:** Sonnet
**Purpose:** Writes CONTEXT.md per phase
**Prompt must include:**

- Role: Context documenter
- Input: Discussion analysis, vision alignment output
- Output: CONTEXT.md with:
  - Decisions (LOCKED — honor exactly)
  - Claude's Discretion (freedom areas)
  - Deferred Ideas (out of scope)

---

#### Tier 7: Planning Enhancement (2 agents)

##### 36. `settlement-architect.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-architect.md`
**Model:** 1M Sonnet
**Purpose:** Designs approach from fiefdom maps
**Prompt must include:**

- Role: Technical architect
- Input: Fiefdom maps, research, vision alignment
- Output: Architectural decisions:
  - Which rooms to modify
  - In what order
  - What borders are affected
  - What contracts need updating
- Consideration: Token budgets, agent counts, dependencies

##### 37. `settlement-work-order-compiler.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-work-order-compiler.md`
**Model:** 1M Sonnet
**Purpose:** Compiles atomic work orders from plans
**Prompt must include:**

- Role: Work order generator
- Input: Architectural decisions, plans
- Output: Atomic work orders:

  ```json
  {
    "work_order_id": "WO-001",
    "fiefdom": "Security",
    "building": "auth.ts",
    "room": "login()",
    "action": "Add rate limiting: max 5 attempts per minute",
    "line_range": "45-67",
    "tokens": 450,
    "complexity": 4,
    "agents_required": 3,
    "dependencies": [],
    "border_impact": "none"
  }
  ```

- Principle: So precise that executor can "RIP through" knowing only "do X here"

---

#### Tier 8: Pre-Execution Synthesis (4 agents)

##### 38. `settlement-integration-synthesizer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-integration-synthesizer.md`
**Model:** 1M Sonnet
**Purpose:** Creates integration instructions
**Prompt must include:**

- Role: Integration instruction writer
- Input: Work orders, border contracts
- Output: Integration instructions that respect borders:
  - What to import from where
  - What to export to whom
  - What contracts must be maintained

##### 39. `settlement-wiring-mapper.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-wiring-mapper.md`
**Model:** Sonnet
**Purpose:** Maps Code City wiring connections
**Prompt must include:**

- Role: Wiring specialist
- Input: Import/export data, integration points
- Output: Wiring data for Code City panel:
  - Current wiring state (Gold/Teal/Purple per wire)
  - Required wiring changes
  - Wiring health assessment

##### 40. `settlement-instruction-writer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-instruction-writer.md`
**Model:** Sonnet
**Purpose:** Writes "Do X Here" execution packets
**Prompt must include:**

- Role: Instruction writer
- Principle: ZERO AMBIGUITY
- Output format:

  ```
  FILE: src/security/auth.ts
  ROOM: login() function
  LINES: 45-67

  DO THIS:
  1. Add import: `import { RateLimiter } from '../utils/rateLimiter'`
  2. At line 46, add: `const limiter = new RateLimiter(5, 60000)`
  3. Wrap existing logic in: `if (limiter.check(userId)) { ... } else { throw new RateLimitError() }`

  DO NOT:
  - Modify any other function
  - Change the function signature
  - Touch lines outside 45-67

  VERIFY:
  - Rate limiter blocks 6th attempt
  - Existing tests still pass
  ```

##### 41. `settlement-atomic-task-generator.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-atomic-task-generator.md`
**Model:** Sonnet
**Purpose:** Generates unambiguous atomic tasks
**Prompt must include:**

- Role: Task atomizer
- Principle: Each task completable in ONE agent session
- Output: Task that includes:
  - Exact file path
  - Exact line range
  - Exact action
  - Exact verification
  - No dependencies on other tasks in same batch

---

#### Tier 9: Execution Support (2 agents)

##### 42. `settlement-sentinel.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-sentinel.md`
**Model:** Sonnet
**Purpose:** Watchdog — probes, investigates, fixes, escalates
**Prompt must include:**

- Role: Watchdog and recovery agent
- Probe cycle: Every 30 seconds (or 15s offset for second sentinel)
- On probe:
  1. Check if primary agent is responding
  2. Check if progress is being made
  3. Check for hang indicators
- On failure detection:
  1. Log failure context
  2. Investigate AROUND the problem (not just the symptom)
  3. Identify root cause
  4. If fixable: Apply fix, allow primary to resume
  5. If not fixable: Escalate with combined notes
- Output: Failure report with root cause analysis, fix applied (if any)

##### 43. `settlement-relief-deployer.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-relief-deployer.md`
**Model:** Sonnet
**Purpose:** Deploys replacement agents to maintain 3 on site
**Prompt must include:**

- Role: Relief coordinator
- Trigger: Agent success (moves to completion) or agent failure (needs replacement)
- Action: Deploy new agent with:
  - Current work unit context
  - Any failure notes from sentinels
  - Updated "watch out for" patterns
- Invariant: Always maintain exactly 3 agents on site

---

#### Tier 10: Validation Enhancement (1 agent)

##### 44. `settlement-failure-pattern-logger.md` — CREATE

**Location:** `~/.claude/agents/settlement/settlement-failure-pattern-logger.md`
**Model:** Sonnet
**Purpose:** Logs failure patterns for future prevention
**Prompt must include:**

- Role: Pattern archivist
- Input: All sentinel failure reports
- Process: Identify recurring patterns, categorize failures
- Output: FAILURE_PATTERNS.md with:
  - Pattern description
  - Trigger conditions
  - Successful fixes
  - Prevention recommendations
- Integration: Future sentinels and agents read this before starting

---

## NEW WORKFLOWS TO CREATE

Create these in `~/.claude/get-shit-done/workflows/settlement/`:

### 1. `survey-codebase.md`

**Purpose:** Run Tier 1-3 (Survey → Pattern → Cartography)
**Triggers:** Surveyors, Complexity Analyzers, Pattern Identifiers, Cartographers, Border Agents
**Output:** Fiefdom map, token budgets, border contracts

### 2. `vision-alignment.md`

**Purpose:** Run Tier 5 (Vision Walker with Founder)
**Triggers:** Vision Walker (Opus)
**Output:** Vision-aligned specifications

### 3. `deploy-scaled-agents.md`

**Purpose:** Deploy agents using Universal Scaling Formula
**Input:** Target, agent type
**Process:** Calculate work units, deploy with rolling sentinels
**Output:** Deployment log

### 4. `sentinel-protocol.md`

**Purpose:** Define sentinel probe/investigate/fix cycle
**Used by:** All execution phases

### 5. `border-validation.md`

**Purpose:** Validate border contracts are maintained
**Triggers:** Border Agents
**Output:** Border compliance report

---

## NEW TEMPLATES TO CREATE

Create these in `~/.claude/get-shit-done/templates/settlement/`:

### 1. `fiefdom-map.md`

Template for fiefdom map output

### 2. `border-contract.md`

Template for border contract definitions

### 3. `work-order.md`

Template for atomic work orders

### 4. `building-panel.md`

Template for Code City building panel data

### 5. `failure-pattern.md`

Template for failure pattern documentation

### 6. `deployment-plan.md`

Template for agent deployment plans

---

## OUTPUT REQUIREMENTS

You must create the following files:

### Modified GSD Agents (11 files)

Modify existing files in `~/.claude/agents/`:

- [ ] gsd-codebase-mapper.md (enhanced)
- [ ] gsd-project-researcher.md (enhanced)
- [ ] gsd-research-synthesizer.md (enhanced)
- [ ] gsd-roadmapper.md (enhanced)
- [ ] gsd-phase-researcher.md (enhanced)
- [ ] gsd-planner.md (enhanced)
- [ ] gsd-plan-checker.md (enhanced)
- [ ] gsd-executor.md (enhanced)
- [ ] gsd-verifier.md (enhanced)
- [ ] gsd-integration-checker.md (enhanced)
- [ ] gsd-debugger.md (enhanced)

### New Settlement Agents (33 files)

Create new files in `~/.claude/agents/settlement/`:

- [ ] settlement-luminary.md
- [ ] settlement-city-manager.md
- [ ] settlement-district-planner.md
- [ ] settlement-git-commit-agent.md
- [ ] settlement-scaler.md
- [ ] settlement-civic-council.md
- [ ] settlement-surveyor.md
- [ ] settlement-complexity-analyzer.md
- [ ] settlement-file-structure-mapper.md
- [ ] settlement-token-counter.md
- [ ] settlement-pattern-identifier.md
- [ ] settlement-import-export-mapper.md
- [ ] settlement-filepath-analyzer.md
- [ ] settlement-function-cataloger.md
- [ ] settlement-cartographer.md
- [ ] settlement-district-boundary-definer.md
- [ ] settlement-token-budget-calculator.md
- [ ] settlement-deployment-planner.md
- [ ] settlement-integration-point-mapper.md
- [ ] settlement-border-agent.md
- [ ] settlement-integration-researcher.md
- [ ] settlement-vision-walker.md
- [ ] settlement-discussion-analyzer.md
- [ ] settlement-context-writer.md
- [ ] settlement-architect.md
- [ ] settlement-work-order-compiler.md
- [ ] settlement-integration-synthesizer.md
- [ ] settlement-wiring-mapper.md
- [ ] settlement-instruction-writer.md
- [ ] settlement-atomic-task-generator.md
- [ ] settlement-sentinel.md
- [ ] settlement-relief-deployer.md
- [ ] settlement-failure-pattern-logger.md

### New Workflows (5 files)

Create in `~/.claude/get-shit-done/workflows/settlement/`:

- [ ] survey-codebase.md
- [ ] vision-alignment.md
- [ ] deploy-scaled-agents.md
- [ ] sentinel-protocol.md
- [ ] border-validation.md

### New Templates (6 files)

Create in `~/.claude/get-shit-done/templates/settlement/`:

- [ ] fiefdom-map.md
- [ ] border-contract.md
- [ ] work-order.md
- [ ] building-panel.md
- [ ] failure-pattern.md
- [ ] deployment-plan.md

---

## VERIFICATION CHECKLIST

Before completing, verify:

- [ ] All 11 GSD agents enhanced with Settlement concepts
- [ ] All 33 new Settlement agents created with complete prompts
- [ ] All 5 new workflows created
- [ ] All 6 new templates created
- [ ] Universal Scaling Formula implemented in settlement-scaler.md
- [ ] Rolling Sentinel protocol implemented in settlement-sentinel.md
- [ ] Border Agent system implemented
- [ ] Code City concepts (fiefdoms, buildings, rooms, panels, wiring) integrated
- [ ] Model assignments correct (Opus for Luminary/Vision Walker/Civic Council, 1M Sonnet for heavy synthesis, Sonnet for execution)
- [ ] Git commit after each work unit enforced
- [ ] Vision Walker includes Founder interaction examples

---

## FINAL NOTES

1. **GSD is the foundation** — enhance it, don't break it
2. **Universal Scaling applies everywhere** — no exceptions
3. **Rolling Sentinels maintain 3 on site** — always
4. **Borders define agent work boundaries** — agents don't cross without Border Agent approval
5. **Vision Walker runs BEFORE planning** — Founder alignment is non-negotiable
6. **Git commit after EACH work unit** — atomic, traceable history
7. **Conservative token budgets** — leave 60% for reasoning

---

*Generated by Luminary for Opus implementation instance*
*Settlement System v4*
*Date: 2026-02-12*

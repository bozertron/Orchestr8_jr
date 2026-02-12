# Settlement System Pressure Test & Architecture Decision Record

## Date: 2026-02-12
## Authors: Ben Webster & Sol (Opus Instance)
## Status: APPROVED — Ready for Implementation

---

## EXECUTIVE SUMMARY

The original OPUS_HANDOFF_PROMPT.md specified 44 agents (11 enhanced GSD + 33 new Settlement agents). After tier-by-tier pressure testing, we consolidated to **30 agents** (11 enhanced GSD + 19 new Settlement agents) while preserving ALL functional capabilities. Every nuance from the original spec is captured — housed in fewer, more capable agents rather than split across narrow specialists.

**Critical operational context that shaped decisions:** Ben's prior deployments used 20-30 agents per wave in a pipeline model (one fiefdom at a time, one tier at a time). This is a manufacturing line, not a swarm. Agents communicate through artifacts between tiers, not real-time interaction. The Rolling Sentinel system (always 3 on site per work unit) was the ONLY method that worked — without it, agents sent into 40,000+ line directories exploded and couldn't complete tasks. Files up to 138KB required 10 agents with explicit line-range parameters.

---

## BEN'S CRITICAL NOTES (Integrated Throughout)

### Note 1: No Ambiguity in Boundary Detection
> "Ambiguity is a no go: full stop. Probably is not in our charter. I don't mind integrating the function elsewhere, but explicit boundaries are important because that's when guesses happen, which is plausibly a cascade failure point."

**Resolution:** Explicit boundary detection is preserved as a dedicated function within the Cartographer agent. The Cartographer MUST produce explicit, unambiguous fiefdom boundaries — not suggestions, not "probably." Boundary detection uses coupling analysis (high internal coupling, low external coupling) combined with directory structure analysis, import/export flow analysis, and cross-fiefdom dependency mapping. The output is definitive boundary contracts, not heuristics.

### Note 2: Enriched Surveyor Needs Commensurate Scaling
> "Less agent-types is ok, as long as their deployment volume is commensurate with the problem."

**Resolution:** The Universal Scaling Formula is updated with a COMPLEXITY_MULTIPLIER adjustment for the enriched Surveyor. Because the Super-Surveyor now captures rooms, token counts, internal relationships, AND function signatures in a single pass, its per-file workload is heavier. The complexity scoring accounts for this:
- Original Surveyor: `COMPLEXITY_MULTIPLIER = 1.0 + (complexity_score × 0.1)`
- Enriched Surveyor: `COMPLEXITY_MULTIPLIER = 1.0 + (complexity_score × 0.15)` (50% higher multiplier)
- This means a complexity-7 file gets `× 2.05` instead of `× 1.7`, producing more work units and therefore more agents deployed

---

## TIER-BY-TIER ANALYSIS

### Tier 0: Coordination — 6 → 3 agents

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Luminary** | KEEP | Opus-level strategic reasoning. Nothing else does this. |
| **City Manager** | KEEP (ENHANCED) | Absorbs District Planner + Relief Deployer functions |
| **District Planner** | MERGE → City Manager | In pipeline model (one fiefdom at a time), City Manager IS the district planner for the active wave |
| **Git Commit Agent** | DEMOTE → Convention | GSD executors already commit atomically. Commit format `[Tier X][Fiefdom][Room] description` baked into every executor's prompt |
| **Scaler** | DEMOTE → Formula | One line of math: `ceil((tokens × (1 + complexity × 0.1)) / 2500) × 3`. Embedded in City Manager and Deployment Planner prompts |
| **Civic Council** | KEEP | Quality gate / founder advocate. Fires at validation checkpoints, not always-active |

**What City Manager absorbs:**
- District Planner's per-fiefdom resource allocation (City Manager already tracks progress per fiefdom in pipeline model)
- Relief Deployer's failure recovery deployment (City Manager already "spawns agents, tracks progress, handles failures")
- Scaler's formula (embedded as a calculation step, not a separate agent call)

**What's preserved:**
- Per-fiefdom resource tracking (from District Planner)
- Relief deployment with failure context forwarding (from Relief Deployer)
- Universal Scaling Formula calculations (from Scaler)
- Atomic git commit conventions (from Git Commit Agent)

---

### Tier 1: Survey & Measurement — 4 → 2 agents

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Surveyor** | KEEP (ENHANCED → "Super-Surveyor") | Absorbs Token Counter + File Structure Mapper + Function Cataloger |
| **Complexity Analyzer** | KEEP | Genuinely distinct analytical judgment, runs on Surveyor output |
| **File Structure Mapper** | MERGE → Surveyor | Room identification already required for Surveyor's token-per-room counting |
| **Token Counter** | MERGE → Surveyor | Surveyor already counts tokens; aggregation (room → file → fiefdom) added as post-processing step |

**What Super-Surveyor produces (single read pass per file):**
```json
{
  "file": "path/to/file.ts",
  "total_tokens": 5000,
  "rooms": [
    {
      "name": "functionA",
      "type": "function",
      "line_start": 10,
      "line_end": 50,
      "tokens": 800,
      "signature": "async functionA(userId: string, options?: Options): Promise<Result>",
      "params": ["userId: string", "options?: Options"],
      "return_type": "Promise<Result>",
      "jsdoc": "Fetches user data with optional filtering",
      "internal_calls": ["helperB", "validateInput"],
      "relationships": {
        "calls": ["helperB()", "validateInput()"],
        "called_by": ["ClassC.process()"]
      }
    }
  ],
  "aggregation": {
    "total_tokens": 5000,
    "room_count": 12,
    "largest_room_tokens": 2500
  }
}
```

**Scaling adjustment (per Ben's Note 2):**
The enriched Surveyor does more work per file than the original spec's lean Surveyor. The Universal Scaling Formula compensates:
- `COMPLEXITY_MULTIPLIER = 1.0 + (complexity_score × 0.15)` (was 0.1)
- This ensures more agents are deployed for complex files, preventing the "I've got this" failure mode

**Function Cataloger absorption detail:**
The Surveyor now captures function signatures, parameters, return types, and JSDoc during its read pass. This is richer metadata about rooms it's already identifying. The Complexity Analyzer's scoring formula accounts for this enriched data — specifically, the function signature complexity feeds into the cyclomatic complexity calculation.

---

### Tier 2: Pattern Recognition — 4 → 2 agents

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Pattern Identifier** | KEEP | Design patterns, conventions, anti-patterns, consistency assessment across files |
| **Import/Export Mapper** | KEEP (ENHANCED) | Absorbs Integration Point Mapper's cross-fiefdom filtering |
| **Filepath Analyzer** | MERGE → Cartographer (Tier 3) | Fiefdom suggestions from path structure is step one of cartography |
| **Function Cataloger** | MERGE → Surveyor (Tier 1) | Signatures/params/returns captured during Surveyor's read pass |

**What Import/Export Mapper absorbs:**
- Integration Point Mapper's cross-fiefdom connection mapping (cross-fiefdom imports ARE integration points)
- The Mapper's output, filtered to cross-boundary connections, IS the integration point registry
- Explicit flagging of every cross-fiefdom import with source/destination fiefdom labels

**Filepath Analyzer → Cartographer detail (per Ben's Note 1):**
The filepath analysis function is NOT removed — it's relocated to the Cartographer where it serves as ONE INPUT among several for boundary detection. Critically, the Cartographer does NOT rely on path structure alone (that would be "probably" territory). It combines:
1. Directory structure analysis (from filepath patterns)
2. Coupling analysis (high internal, low external — from Import/Export Mapper data)
3. Cross-fiefdom dependency weighting (from Complexity Analyzer scores)
4. Integration point density (from Import/Export Mapper cross-boundary flags)

The result is EXPLICIT boundaries, not suggestions.

---

### Tier 3: Cartography & Synthesis — 6 → 2 agents

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Cartographer** | KEEP (ENHANCED → "Super-Cartographer") | Absorbs Boundary Definer + Token Budget Calculator + Deployment Planner + Filepath Analyzer |
| **District Boundary Definer** | MERGE → Cartographer | Boundary definition IS cartography — can't draw a fiefdom map without defining boundaries |
| **Token Budget Calculator** | MERGE → Cartographer | Arithmetic on data Cartographer already holds (40% cap, 60% reasoning) |
| **Deployment Planner** | MERGE → Cartographer | Applies Universal Scaling Formula to Cartographer's own token/complexity data |
| **Integration Point Mapper** | MERGE → Import/Export Mapper (Tier 2) | Cross-fiefdom imports are integration points |
| **Border Agent** | KEEP | Genuinely distinct: defines contracts (what SHOULD/SHOULDN'T cross), not just maps what does |

**What Super-Cartographer produces:**
```markdown
# FIEFDOM MAP: [Project Name]

## Fiefdom: Security
- **Boundary:** src/security/, src/auth/, src/crypto/
- **Boundary Basis:** 87% internal coupling, 13% external (threshold: 70/30)
- **Buildings:** 12 files
- **Total Tokens:** 45,000
- **Complexity (weighted avg):** 7.2
- **Agent Budget:** ceil(45000 × 2.08 / 2500) × 3 = 114 agents across all tiers
- **Border Crossings:** 8 integration points (→ P2P: 3, → Calendar: 2, → Core: 3)

### Buildings
| File | Tokens | Complexity | Rooms | Largest Room |
|------|--------|------------|-------|-------------|
| auth.ts | 8,500 | 8 | 14 | login() 2,100 tokens |
| permissions.ts | 3,200 | 5 | 6 | checkRole() 900 tokens |
...

## Border: Security ↔ P2P
- **Crossing Points:** 3
- **Direction:** Bidirectional
- **Contracts:** [Defined by Border Agent]
```

**Explicit boundary detection (per Ben's Note 1):**
The Cartographer's boundary detection is DETERMINISTIC, not heuristic:
1. Calculate coupling ratio for each directory cluster: `internal_imports / total_imports`
2. Threshold: ≥ 70% internal coupling = fiefdom candidate
3. Validate against directory structure (path analysis confirms or challenges)
4. Resolve ambiguous files by import direction majority
5. Output: EXPLICIT fiefdom membership per file, no "probably" or "suggested"

---

### Tier 4: Research — No change (1 new + 3 GSD enhanced)

| Agent | Verdict | Notes |
|---|---|---|
| **Integration Researcher** | KEEP | Deep research on how fiefdoms should integrate. Distinct from GSD researchers |
| **gsd-project-researcher** | ENHANCE | Add fiefdom-aware research |
| **gsd-phase-researcher** | ENHANCE | Add room-level analysis, wiring research |
| **gsd-research-synthesizer** | ENHANCE | Add fiefdom map generation |

---

### Tier 5: Vision Alignment — No change (1 agent)

| Agent | Verdict | Notes |
|---|---|---|
| **Vision Walker** | KEEP | Opus model. Socratic dialogue with Founder before any planning. Essential and unique. |

---

### Tier 6: Requirements & Roadmap — 2 → 1 agent (+ GSD enhanced)

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Discussion Analyzer** | MERGE → Context Analyst | Sequential two-step process on same material |
| **Context Writer** | MERGE → Context Analyst | Same agent reads transcript, extracts decisions, writes CONTEXT.md |

**What Context Analyst produces:**
- Reads Vision Walker conversation transcript
- Extracts structured decisions, constraints, preferences
- Writes CONTEXT.md with LOCKED decisions, Claude's Discretion areas, Deferred Ideas
- Single agent, single pass — comprehension then formatting don't require different reasoning capabilities

---

### Tier 7: Planning — No change (2 new + GSD enhanced)

| Agent | Verdict | Notes |
|---|---|---|
| **Architect** | KEEP | 1M Sonnet. Designs approach, room modification order, border impacts. Strategic reasoning. |
| **Work Order Compiler** | KEEP | 1M Sonnet. Translates architectural decisions into atomic JSON work orders. The manufacturing spec. |

---

### Tier 8: Pre-Execution Synthesis — 4 → 3 agents

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Integration Synthesizer** | KEEP | 1M Sonnet. Creates integration instructions respecting border contracts |
| **Wiring Mapper** | KEEP | Produces Code City panel data (Gold/Teal/Purple per wire) |
| **Instruction Writer** | KEEP (absorbs Atomic Task Generator) | Zero-ambiguity "Do X Here" execution packets |
| **Atomic Task Generator** | MERGE → Instruction Writer | Identical output format — both produce exact file/line/action/verification packets |

**Redundancy evidence:**
- Instruction Writer output: `FILE: ... ROOM: ... LINES: ... DO THIS: ... DO NOT: ... VERIFY: ...`
- Atomic Task Generator output: `exact file path, exact line range, exact action, exact verification, no dependencies`
- These are the same artifact described twice with different names.

---

### Tier 9: Execution — 2 → 1 new agent (+ GSD enhanced)

| Original Agent | Verdict | Disposition |
|---|---|---|
| **Sentinel** | KEEP | Probe/investigate/fix cycle. Operationally proven essential. |
| **Relief Deployer** | MERGE → City Manager (Tier 0) | City Manager already handles spawning, progress tracking, and failure recovery |

**Relief deployment preserved in City Manager:**
- On sentinel failure report: City Manager deploys replacement agent with current work unit context + failure notes + "watch out for" patterns
- Maintains invariant: always 3 agents on site per active work unit
- This is just what the City Manager does when a sentinel reports a failure — not a separate agent

---

### Tier 10: Validation — No change (1 new + GSD enhanced)

| Agent | Verdict | Notes |
|---|---|---|
| **Failure Pattern Logger** | KEEP | Pattern archival across sessions. Future agents read FAILURE_PATTERNS.md before starting. |

---

## FINAL AGENT INVENTORY: 30 Agents

### Enhanced GSD Agents (11) — Modify existing files

| # | Agent | Key Enhancements |
|---|---|---|
| 1 | gsd-codebase-mapper | + fiefdom detection, border identification, token counting, complexity scoring |
| 2 | gsd-project-researcher | + fiefdom-aware research, integration point discovery, dependency direction |
| 3 | gsd-research-synthesizer | + fiefdom map generation, agent deployment recommendations, border contract summary |
| 4 | gsd-roadmapper | + fiefdom-based phase organization, border work as explicit phases, agent count estimates |
| 5 | gsd-phase-researcher | + room-level analysis, wiring state (Gold/Teal/Purple), integration point status |
| 6 | gsd-planner | + "Do X Here" instruction format, room-level task assignment, agent count per task |
| 7 | gsd-plan-checker | + scaling validation, border contract checking, room assignment validation |
| 8 | gsd-executor | + sentinel probe response protocol, room-level git commits, failure reporting format |
| 9 | gsd-verifier | + border contract verification, wiring state update, room-level verification |
| 10 | gsd-integration-checker | + cross-fiefdom border validation, border contract compliance, wiring consistency |
| 11 | gsd-debugger | + sentinel failure context consumption, root cause pattern identification, prevention recs |

### New Settlement Agents (19) — Create new files

| # | Agent | Tier | Model | Purpose |
|---|---|---|---|---|
| 12 | settlement-luminary | 0 | Opus | Strategic coordinator, vision holder, architectural decisions |
| 13 | settlement-city-manager | 0 | Sonnet | Deployment orchestration + district planning + relief deployment + scaling |
| 14 | settlement-civic-council | 0 | Opus | Founder advocate, quality gate, veto power before merge |
| 15 | settlement-surveyor | 1 | 1M Sonnet | Comprehensive file survey: rooms, tokens, structure, signatures, relationships |
| 16 | settlement-complexity-analyzer | 1 | Sonnet | Complexity scoring (1-10) with nesting, cyclomatic, dependency factors |
| 17 | settlement-pattern-identifier | 2 | Sonnet | Design patterns, conventions, anti-patterns, consistency assessment |
| 18 | settlement-import-export-mapper | 2 | Sonnet | Import/export graph, wiring data, border detection + integration points |
| 19 | settlement-cartographer | 3 | 1M Sonnet | Fiefdom maps with explicit boundaries, token budgets, deployment plans |
| 20 | settlement-border-agent | 3 | Sonnet | Border contracts: allowed/forbidden types per fiefdom pair |
| 21 | settlement-integration-researcher | 4 | Sonnet | Deep research on fiefdom integration patterns |
| 22 | settlement-vision-walker | 5 | Opus | Socratic founder walkthrough before planning |
| 23 | settlement-context-analyst | 6 | Sonnet | Analyzes Vision Walker output → writes CONTEXT.md |
| 24 | settlement-architect | 7 | 1M Sonnet | Technical architecture: room modification order, border impacts |
| 25 | settlement-work-order-compiler | 7 | 1M Sonnet | Atomic JSON work orders with exact file/line/action/agents |
| 26 | settlement-integration-synthesizer | 8 | 1M Sonnet | Integration instructions respecting border contracts |
| 27 | settlement-wiring-mapper | 8 | Sonnet | Code City panel data: Gold/Teal/Purple per wire |
| 28 | settlement-instruction-writer | 8 | Sonnet | Zero-ambiguity "Do X Here" execution packets |
| 29 | settlement-sentinel | 9 | Sonnet | Probe/investigate/fix watchdog cycle |
| 30 | settlement-failure-pattern-logger | 10 | Sonnet | Failure pattern archival for future prevention |

### Model Distribution

| Model | Count | Agents |
|---|---|---|
| Opus | 3 | Luminary, Civic Council, Vision Walker |
| 1M Sonnet | 5 | Surveyor, Cartographer, Architect, Work Order Compiler, Integration Synthesizer |
| Sonnet | 11 | City Manager, Complexity Analyzer, Pattern Identifier, Import/Export Mapper, Border Agent, Integration Researcher, Context Analyst, Wiring Mapper, Instruction Writer, Sentinel, Failure Pattern Logger |
| (GSD enhanced) | 11 | Per existing model assignments |

---

## UNIVERSAL SCALING FORMULA (Updated)

```
INPUTS:
  file_tokens = approximate token count of target
  complexity_score = 1-10 based on nesting, dependencies, patterns
  agent_type = survey | analysis | execution

CONSTANTS:
  MAX_TOKENS_PER_AGENT = 2,500 tokens (leaves massive reasoning space)
  
  COMPLEXITY_MULTIPLIER by agent type:
    survey (Super-Surveyor):  1.0 + (complexity_score × 0.15)  ← ENRICHED
    analysis (all others):     1.0 + (complexity_score × 0.12)  ← MODERATE
    execution (executors):     1.0 + (complexity_score × 0.10)  ← ORIGINAL

FORMULA:
  effective_tokens = file_tokens × COMPLEXITY_MULTIPLIER
  work_units = ceil(effective_tokens / MAX_TOKENS_PER_AGENT)
  agents_per_work_unit = 3 (rolling sentinel deployment)
  ═══════════════════════════════════════════════════════════════
  TOTAL_AGENTS = work_units × 3

EXAMPLES (138KB file, 35K tokens, complexity 7):
  Survey pass:    35000 × 2.05 = 71,750 → 29 work units → 87 agents
  Analysis pass:  35000 × 1.84 = 64,400 → 26 work units → 78 agents
  Execution pass: 35000 × 1.70 = 59,500 → 24 work units → 72 agents
```

---

## ARTIFACTS TO CREATE

### New Settlement Agent Files (19 files)
Create in `~/.claude/agents/settlement/`:
- [ ] settlement-luminary.md
- [ ] settlement-city-manager.md
- [ ] settlement-civic-council.md
- [ ] settlement-surveyor.md
- [ ] settlement-complexity-analyzer.md
- [ ] settlement-pattern-identifier.md
- [ ] settlement-import-export-mapper.md
- [ ] settlement-cartographer.md
- [ ] settlement-border-agent.md
- [ ] settlement-integration-researcher.md
- [ ] settlement-vision-walker.md
- [ ] settlement-context-analyst.md
- [ ] settlement-architect.md
- [ ] settlement-work-order-compiler.md
- [ ] settlement-integration-synthesizer.md
- [ ] settlement-wiring-mapper.md
- [ ] settlement-instruction-writer.md
- [ ] settlement-sentinel.md
- [ ] settlement-failure-pattern-logger.md

### Enhanced GSD Agent Files (11 files)
Modify existing files in `~/.claude/agents/`:
- [ ] gsd-codebase-mapper.md
- [ ] gsd-project-researcher.md
- [ ] gsd-research-synthesizer.md
- [ ] gsd-roadmapper.md
- [ ] gsd-phase-researcher.md
- [ ] gsd-planner.md
- [ ] gsd-plan-checker.md
- [ ] gsd-executor.md
- [ ] gsd-verifier.md
- [ ] gsd-integration-checker.md
- [ ] gsd-debugger.md

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

### Total: 41 files (19 new agents + 11 enhanced + 5 workflows + 6 templates)

---

## GSD PATTERNS STUDIED (Reference for Implementation)

### GSD Executor Pattern (Key Elements to Preserve)
- XML-structured prompts with `<role>`, `<execution_flow>`, `<step>` tags
- Frontmatter with name, description, tools, color
- Deviation rules (4 rules with clear priority)
- Checkpoint protocol (human-verify 90%, decision 9%, human-action 1%)
- Task commit protocol (individual staging, conventional commits)
- Summary creation with self-check
- State updates via gsd-tools.js
- Continuation handling for multi-session execution

### GSD Planner Pattern (Key Elements to Preserve)
- Context fidelity: LOCKED decisions are NON-NEGOTIABLE
- Plans ARE prompts (not documents that become prompts)
- Quality degradation curve awareness (complete within ~50% context)
- Discovery levels (0-3) for research depth
- Task anatomy: files, action, verify, done
- Dependency graph with wave assignment
- Goal-backward must-have derivation
- Frontmatter validation via gsd-tools.js

### GSD Verifier Pattern (Key Elements to Preserve)
- Goal-backward verification (outcome, not task completion)
- "Do NOT trust SUMMARY.md claims" — verify against actual codebase
- Three-level verification: truths → artifacts → wiring
- Re-verification mode for gap closure
- VERIFICATION.md output with pass/fail per must-have

---

## IMPLEMENTATION APPROACH

Build tier by tier, starting from Tier 0 (coordination) through Tier 10 (validation). Each agent file follows GSD's XML-structured prompt format with frontmatter. Settlement enhancements to GSD agents are additive — new sections added, existing patterns preserved.

All agents reference the Settlement concepts consistently:
- **Fiefdom** = feature neighborhood (directory cluster with high internal coupling)
- **Building** = file (height = exports, footprint = lines)
- **Room** = logic block (function, class, significant code block)
- **Panel** = building front sign (imports, exports, functions, state, wiring)
- **Border** = fiefdom boundary with typed contracts
- **Wiring** = import/export connections (Gold = working, Teal = needs work, Purple = agents active)

---

*Pressure test conducted by Sol (Opus Instance)*
*Approved by Ben Webster*
*Settlement System v5 (consolidated)*
*Date: 2026-02-12*

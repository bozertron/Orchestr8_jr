## orchestr8's Foundational Principles - Agent Deployment Architecture

> **"Collaboration is a direct reflection of consciousness"**
>
> Every agent operates with awareness of the whole system. No agent works in isolation.
> Every decision considers the human element. No technical solution sacrifices user delight.

---

## Role Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MAIN CONTEXT (Claude)                               │
│                                                                             │
│  RESPONSIBILITIES:                                                          │
│  ✅ Hold conversation with human leadership                                 │
│  ✅ Create TASK_MANIFEST.json with strategic direction                      │
│  ✅ Receive STATUS_REPORT.json (compressed, minimal context impact)         │
│  ✅ Make decisions requiring human alignment                                │
│  ✅ Final approval before merges                                            │
│                                                                             │
│  ❌ DO NOT act as Orchestrator                                              │
│  ❌ DO NOT act as Deployment Strategist                                     │
│  ❌ DO NOT make git commits directly                                        │
│  ❌ DO NOT execute fixes directly                                           │
│  ❌ DO NOT suggest removing code without EPO Human Advocacy review          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ TASK_MANIFEST.json
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR AGENT                                  │
│                                                                             │
│  RESPONSIBILITIES:                                                          │
│  • Parse TASK_MANIFEST.json                                                 │
│  • Create WAVE_PLAN.json for Deployment Strategist                          │
│  • Collect all agent outputs                                                │
│  • Run Ralph Wiggum loop until sprint complete                              │
│  • Trigger Git Commit Agent after each wave                                 │
│  • Compile STATUS_REPORT.json for Main Context                              │
│  • Escalate decisions to Main Context (batched)                             │
│                                                                             │
│  RALPH WIGGUM LOOP:                                                         │
│  while not <promise>SPRINT_COMPLETE</promise>:                              │
│      deploy_wave()                                                          │
│      collect_results()                                                      │
│      if failures: trigger_failure_scouts()                                  │
│      if escalations_needed: batch_and_escalate()                            │
│      update_checkpoint()                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ WAVE_PLAN.json
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT STRATEGIST AGENT                            │
│                                                                             │
│  RESPONSIBILITIES:                                                          │
│  • Receive WAVE_PLAN.json from Orchestrator                                 │
│  • Maintain FILE_LOCKS.json (collision prevention)                          │
│  • Calculate parallel batches within each wave                              │
│  • Deploy agents with proper context distribution                           │
│  • Monitor agent health and context usage                                   │
│  • Retry failed agents (2x max)                                             │
│  • Report wave completion to Orchestrator                                   │
│                                                                             │
│  CONTEXT WINDOW MANAGEMENT:                                                 │
│  • Track estimated context per agent                                        │
│  • Split large tasks across multiple agents                                 │
│  • Prefer more agents with smaller scope over fewer with larger scope       │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                           │
         ┌──────────┴──────────────────────────┴──────────┐
         │                                                 │
         ▼                                                 ▼
┌─────────────────────┐                         ┌─────────────────────┐
│   EXECUTION AGENTS  │                         │   QUALITY AGENTS    │
│                     │                         │                     │
│ • Scout             │                         │ • Validator         │
│ • Fixer             │                         │ • EPO Human Advocacy│
│ • Synthesizer       │                         │ • Git Commit        │
└─────────────────────┘                         └─────────────────────┘
```

---

## Agent Type Definitions

### Tier 1: Coordination Agents

#### ORCHESTRATOR

- **Count per sprint:** 1
- **Persistence:** Runs entire sprint via Ralph Wiggum loop
- **Inputs:** TASK_MANIFEST.json
- **Outputs:** STATUS_REPORT.json, CHECKPOINT.json
- **Triggers:** Git Commit Agent after each wave

#### DEPLOYMENT STRATEGIST

- **Count per sprint:** 1
- **Persistence:** Called by Orchestrator for each wave
- **Inputs:** WAVE_PLAN.json
- **Outputs:** DEPLOYMENT_LOG.json, FILE_LOCKS.json
- **Special:** Monitors context window usage across agents

---

### Tier 2: Execution Agents

#### SCOUT

- **Purpose:** Deep-dive analysis, trace code paths to termination
- **Scope:** Can roam freely across codebase
- **Output:** Comprehensive JSON with signal paths, suggested fixes
- **Context:** MEDIUM (reads many files but outputs structured JSON)
- **Parallelization:** HIGH (read-only, no collisions)

#### FIXER

- **Purpose:** Apply approved fixes surgically
- **Scope:** Limited to assigned file(s)
- **Output:** FIX_RESULT.json
- **Context:** LOW (focused scope)
- **Parallelization:** HIGH (with file locks)

#### SYNTHESIZER

- **Purpose:** Combine multiple Scout outputs, identify patterns
- **Scope:** Reads Scout outputs, produces grouped analysis
- **Output:** SYNTHESIS.json with problem groupings
- **Context:** MEDIUM
- **Parallelization:** LOW (depends on Scout outputs)

---

### Tier 3: Quality Agents

#### VALIDATOR

- **Purpose:** Verify fixes work, check for regressions
- **Scope:** Runs tests, import checks, startup tests
- **Output:** VALIDATION_RESULT.json
- **Context:** MEDIUM
- **Parallelization:** MEDIUM (some tests sequential)

#### EPO HUMAN ADVOCACY AGENT ⭐ NEW

- **Purpose:** Ensure all decisions serve the human user
- **Scope:** Reviews failures, removal suggestions, architectural decisions
- **Triggers:**
  - Any suggestion to "remove" code
  - Any "stub" or "placeholder" detected
  - Any failure during validation
  - Before any PR/merge
- **Analysis Framework:**
  1. What would the EPO user want when using this tool?
  2. Does this decision create technical debt?
  3. Does this decision enhance or degrade user delight?
  4. What would a power user expect this feature to do?
  5. Is there a more complete solution that serves the user better?
- **Output:** ADVOCACY_REPORT.json with recommendation
- **Veto Power:** Can block merges if user delight is compromised
- **Context:** LOW (focused analysis)

#### GIT COMMIT AGENT ⭐ NEW

- **Purpose:** Handle all git operations
- **Scope:** Commits, pushes, branch management
- **Triggered By:** Orchestrator (after wave completion)
- **Responsibilities:**
  - Stage appropriate files
  - Write clear commit messages (following conventions)
  - Push to correct branch
  - Handle merge conflicts (escalate if complex)
  - Verify push success
- **Output:** COMMIT_RESULT.json
- **Context:** LOW
- **Special:** Only agent allowed to run git commands

---

## Ralph Wiggum Loop Protocol

The Ralph Wiggum loop is a **self-referential execution pattern** that continues until a completion promise is detected.

### Implementation

```
┌────────────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM LOOP                               │
│                                                                    │
│   START                                                            │
│     │                                                              │
│     ▼                                                              │
│   ┌──────────────────────────────────────────┐                     │
│   │ Load CHECKPOINT.json (or create new)     │                     │
│   └──────────────────────────────────────────┘                     │
│     │                                                              │
│     ▼                                                              │
│   ┌──────────────────────────────────────────┐                     │
│   │ Determine current wave from checkpoint   │                     │
│   └──────────────────────────────────────────┘                     │
│     │                                                              │
│     ▼                                                              │
│   ┌──────────────────────────────────────────┐                     │
│   │ Deploy agents for current wave           │◄─────────┐         │
│   │ (via Deployment Strategist)              │          │         │
│   └──────────────────────────────────────────┘          │         │
│     │                                                   │         │
│     ▼                                                   │         │
│   ┌──────────────────────────────────────────┐          │         │
│   │ Collect agent outputs                    │          │         │
│   └──────────────────────────────────────────┘          │         │
│     │                                                   │         │
│     ▼                                                   │         │
│   ┌──────────────────────────────────────────┐          │         │
│   │ Any failures?                            │          │         │
│   └──────────────────────────────────────────┘          │         │
│     │YES                    │NO                         │         │
│     ▼                       ▼                           │         │
│   ┌────────────────┐  ┌────────────────┐                │         │
│   │Deploy Failure  │  │ Trigger Git    │                │         │
│   │Scout + EPO     │  │ Commit Agent   │                │         │
│   │Advocacy        │  └────────────────┘                │         │
│   └────────────────┘        │                           │         │
│     │                       ▼                           │         │
│     │              ┌────────────────┐                   │         │
│     │              │ Update         │                   │         │
│     │              │ CHECKPOINT     │                   │         │
│     │              └────────────────┘                   │         │
│     │                       │                           │         │
│     ▼                       ▼                           │         │
│   ┌──────────────────────────────────────────┐          │         │
│   │ Batch escalations for Main Context       │          │         │
│   └──────────────────────────────────────────┘          │         │
│     │                                                   │         │
│     ▼                                                   │         │
│   ┌──────────────────────────────────────────┐          │         │
│   │ All waves complete?                      │          │         │
│   └──────────────────────────────────────────┘          │         │
│     │NO                     │YES                        │         │
│     │                       ▼                           │         │
│     │              ┌────────────────────────┐           │         │
│     │              │ <promise>              │           │         │
│     │              │ SPRINT_COMPLETE        │           │         │
│     │              │ </promise>             │           │         │
│     │              └────────────────────────┘           │         │
│     │                       │                           │         │
│     └───────────────────────┼───────────────────────────┘         │
│                             │                                      │
│                             ▼                                      │
│                        END (return to Main Context)                │
└────────────────────────────────────────────────────────────────────┘
```

### Checkpoint Schema

```json
{
  "sprint_id": "SPRINT-002-LOADCALCULATION",
  "current_wave": 3,
  "waves_completed": [1, 2],
  "waves_remaining": [3, 4, 5, 6],
  "agents_deployed": 24,
  "agents_succeeded": 22,
  "agents_failed": 2,
  "escalations_pending": 1,
  "git_commits": ["abc123", "def456"],
  "last_updated": "2026-01-21T16:00:00Z"
}
```

---

## Context Window Management Strategy

### Principle: More Agents with Smaller Scope > Fewer Agents with Larger Scope

| Task Size | Agents | Context per Agent | Rationale |
|-----------|--------|-------------------|-----------|
| Read 1 file | 1 Scout | ~5K tokens | Single focus |
| Read 5 files | 5 Scouts | ~5K each | Parallel, no collision |
| Implement large class | 4+ Fixers | ~8K each | Split by method/section |
| Complex analysis | 1 Scout + 1 Synthesizer | ~10K each | Scout gathers, Synthesizer analyzes |

### Context Estimation by Agent Type

| Agent Type | Typical Input | Typical Output | Est. Context |
|------------|---------------|----------------|--------------|
| Scout | 1-3 files | JSON report | 8-15K tokens |
| Fixer | 1 file + fix spec | Modified file | 5-10K tokens |
| Validator | Test commands | Pass/fail report | 5-8K tokens |
| EPO Advocacy | Failure report | Recommendation | 3-5K tokens |
| Git Commit | File list | Commit result | 2-3K tokens |
| Orchestrator | All outputs | Status report | 15-25K tokens |

### Splitting Large Tasks

**Example: Implement LoadCalculationEngine (estimated 1000 lines)**

Instead of 1 agent implementing entire class:

| Agent | Section | Lines | Context |
|-------|---------|-------|---------|
| FIXER-A | Core class, **init**, primary API | ~200 | 10K |
| FIXER-B | Structural load methods | ~200 | 10K |
| FIXER-C | Thermal load methods | ~200 | 10K |
| FIXER-D | Electrical load methods | ~150 | 8K |
| FIXER-E | Plumbing load methods | ~150 | 8K |
| FIXER-F | Cross-system propagation | ~150 | 10K |
| FIXER-G | Warning system | ~100 | 6K |
| FIXER-H | Optimization integration | ~100 | 8K |

**Total: 8 Fixers instead of 1, each with manageable context**

---

## Trigger Matrix: Who Triggers Whom

| Event | Triggered By | Triggers |
|-------|--------------|----------|
| Sprint start | Main Context | Orchestrator |
| Wave start | Orchestrator | Deployment Strategist |
| Agent deployment | Deployment Strategist | Scout/Fixer/Validator |
| Agent failure | Deployment Strategist | Failure Scout |
| Fix suggestion "remove code" | Scout/Fixer | EPO Human Advocacy |
| Stub detected | Scout | EPO Human Advocacy |
| Wave complete | Deployment Strategist | Git Commit Agent |
| Git commit success | Git Commit Agent | Orchestrator (continue loop) |
| All waves complete | Orchestrator | Main Context (STATUS_REPORT) |
| Validation failure | Validator | Failure Scout + EPO Advocacy |
| PR ready | Orchestrator | EPO Human Advocacy (final review) |

---

## EPO Human Advocacy Agent - Detailed Specification

### Mission Statement

> "Every line of code we write, every decision we make, serves the human who will use this tool to earn their living. Technical excellence and user delight are not competing goals—they are the same goal."

### Trigger Conditions

The EPO Human Advocacy Agent is AUTOMATICALLY triggered when:

1. **Code Removal Suggested**
   - Any suggestion to delete a function, class, or file
   - Any suggestion to remove an import without replacement
   - Any "just remove it" type recommendation

2. **Stub or Placeholder Detected**
   - `pass` statements in functions
   - `# TODO` or `# FIXME` comments
   - Empty function bodies
   - `NotImplementedError` raises

3. **Validation Failure**
   - Import errors
   - Test failures
   - Startup failures

4. **Architectural Decisions**
   - Before any refactoring that touches >3 files
   - Before any change to execution context
   - Before any change to public API

5. **Pre-Merge Review**
   - Before ANY PR is created
   - Before ANY merge to main

### Analysis Framework

```
┌─────────────────────────────────────────────────────────────────┐
│              EPO HUMAN ADVOCACY ANALYSIS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. USER IMPACT ASSESSMENT                                      │
│     • What feature does this code enable for the user?          │
│     • If removed, what capability is lost?                      │
│     • Who at EPO would be affected by this change?              │
│                                                                 │
│  2. TECHNICAL DEBT ASSESSMENT                                   │
│     • Does this decision introduce tech debt? (Score 0-10)      │
│     • Can future developers easily understand this?             │
│     • Is this the "right" solution or a workaround?             │
│                                                                 │
│  3. USER DELIGHT ASSESSMENT                                     │
│     • Does this enhance the user experience?                    │
│     • Would a power user be satisfied with this?                │
│     • Is there a more elegant solution?                         │
│                                                                 │
│  4. COMPLETENESS ASSESSMENT                                     │
│     • Is this feature fully implemented?                        │
│     • Are there missing edge cases?                             │
│     • Would this pass a user acceptance test?                   │
│                                                                 │
│  5. RECOMMENDATION                                              │
│     • APPROVE: Proceed with change                              │
│     • MODIFY: Change approach as specified                      │
│     • IMPLEMENT: Feature should be built, not removed           │
│     • ESCALATE: Requires human leadership decision              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Output Schema

```json
{
  "advocacy_id": "ADV-001",
  "trigger": "code_removal_suggested",
  "subject": "LoadCalculation class import",
  "analysis": {
    "user_impact": {
      "affected_feature": "Unified load calculations across all building systems",
      "users_affected": "All EPO engineers using structural/MEP design",
      "capability_lost": "Cross-system load propagation, warning system",
      "impact_score": 9
    },
    "tech_debt": {
      "score": 8,
      "reasoning": "Removing import masks missing implementation; future devs will trip over this"
    },
    "user_delight": {
      "current_state": "Users cannot see how loads interact across systems",
      "ideal_state": "Dashboard shows all loads with real-time warnings",
      "gap_severity": "HIGH"
    },
    "completeness": {
      "implementation_percentage": 0,
      "missing_components": ["LoadCalculationEngine class", "API endpoints", "UI integration"],
      "effort_to_complete": "10 days"
    }
  },
  "recommendation": "IMPLEMENT",
  "recommendation_detail": "LoadCalculation is a core feature that EPO users expect. Rather than remove the import, implement the full LoadCalculationEngine as specified in the design document. This serves users who need to understand load interactions across building systems.",
  "veto_merge": true,
  "veto_reason": "Incomplete feature would frustrate users expecting unified load analysis"
}
```

---

## Git Commit Agent - Detailed Specification

### Responsibilities

1. **Stage Files** - Determine which files should be in commit
2. **Write Commit Message** - Following project conventions
3. **Execute Commit** - Run git commit
4. **Push to Branch** - Push to correct remote branch
5. **Handle Conflicts** - Resolve simple conflicts, escalate complex ones
6. **Report Result** - Return success/failure with details

### Trigger Protocol

```
Orchestrator: "Wave 3 complete. 4 files modified."
     │
     ▼
Git Commit Agent:
  1. Receive file list from Orchestrator
  2. Run `git status` to verify
  3. Run `git add` for specified files
  4. Generate commit message from wave description
  5. Run `git commit`
  6. Run `git push`
  7. Return COMMIT_RESULT.json to Orchestrator
```

### Commit Message Template

```
[Wave {N}] {Wave Description}
 
{Task List}
- TASK-XXX: {description}
- TASK-YYY: {description}
 
{Summary of changes}
 
Deployed by: {agent_count} agents
Validated by: VALIDATOR-{id}
Approved by: EPO Human Advocacy Agent
```

### Output Schema

```json
{
  "commit_id": "abc123def456",
  "branch": "claude/feature-branch",
  "files_committed": [
    "engine/design/load_calculation.py",
    "engine/api/routes/load.py"
  ],
  "commit_message": "[Wave 3] Implement core LoadCalculationEngine...",
  "push_status": "SUCCESS",
  "remote_url": "https://github.com/org/repo",
  "timestamp": "2026-01-21T16:30:00Z"
}
```

---

## Development Strategy: EPO Continuous Integration

Based on Sprint 001 learnings, here is our ongoing development strategy:

### Principles

1. **Never Remove Without Replacing**
   - If code is referenced, it should exist
   - If it doesn't exist, build it
   - EPO Human Advocacy reviews all removal suggestions

2. **Zero Technical Debt Tolerance**
   - No stubs in production
   - No `# TODO` without a linked ticket
   - No workarounds without architectural review

3. **User Delight First**
   - Every feature should work completely
   - Partial implementations frustrate users
   - If we can't build it right, escalate for prioritization

4. **Agent Architecture Discipline**
   - Main Context holds conversation only
   - Orchestrator coordinates, doesn't execute
   - Deployment Strategist manages agents, doesn't fix code
   - Fixers fix code, don't commit
   - Git Commit Agent commits, doesn't fix

5. **Ralph Wiggum Loop Always**
   - Every sprint runs as a loop until complete
   - Checkpoints enable resume
   - Failures trigger Scout analysis
   - No manual intervention mid-sprint

### Sprint Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    EPO SPRINT LIFECYCLE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PLANNING (Main Context + Human)                             │
│     • Define scope and objectives                               │
│     • Create TASK_MANIFEST.json                                 │
│     • Estimate waves and agent counts                           │
│     • Human approval to proceed                                 │
│                                                                 │
│  2. EXECUTION (Orchestrator via Ralph Wiggum Loop)              │
│     • Deploy waves via Deployment Strategist                    │
│     • Scouts analyze, Fixers implement, Validators verify       │
│     • Git Commit Agent commits after each wave                  │
│     • EPO Advocacy reviews any concerns                         │
│     • Loop until complete                                       │
│                                                                 │
│  3. REVIEW (Main Context + Human)                               │
│     • Receive STATUS_REPORT.json                                │
│     • Review any escalations                                    │
│     • EPO Advocacy final review                                 │
│     • Human approval for merge                                  │
│                                                                 │
│  4. MERGE (Git Commit Agent)                                    │
│     • Create PR (if required)                                   │
│     • Merge to main                                             │
│     • Tag release (if applicable)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

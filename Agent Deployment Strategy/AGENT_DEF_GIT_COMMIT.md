# GIT COMMIT AGENT

**Source:** Context Window Erosion.txt (Lines 2102-2114, 2381-2439)

---

## Overview

The Git Commit Agent is a specialized agent responsible for handling ALL git operations within the EPO Agent Architecture. It is the **only agent authorized to run git commands**, ensuring centralized version control management and preventing conflicts from multiple agents attempting git operations.

**Key Characteristic:** This agent operates with LOW context window requirements as its scope is highly focused on version control operations.

---

## Role and Purpose

- **Purpose:** Handle all git operations
- **Scope:** Commits, pushes, branch management
- **Triggered By:** Orchestrator (after wave completion)
- **Context Level:** LOW (focused operations)
- **Special Designation:** ⭐ Only agent allowed to run git commands

---

## Responsibilities

1. **Stage Files** - Determine which files should be in commit
2. **Write Commit Message** - Following project conventions
3. **Execute Commit** - Run git commit
4. **Push to Branch** - Push to correct remote branch
5. **Handle Conflicts** - Resolve simple conflicts, escalate complex ones
6. **Report Result** - Return success/failure with details

---

## Trigger Protocol

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

---

## Input Schema

**From Orchestrator:**
- Wave number
- Wave description
- List of modified files
- Task IDs and descriptions
- Agent count deployed
- Validator ID
- EPO Human Advocacy approval status

---

## Output Schema

**COMMIT_RESULT.json:**

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

## Commit Message Template

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

---

## Operational Constraints

### What This Agent Does:
- Stage and commit files
- Write standardized commit messages
- Push to branches
- Handle simple merge conflicts
- Report commit results

### What This Agent Does NOT Do:
- Fix code (Fixers handle this)
- Validate implementations (Validators handle this)
- Make architectural decisions (escalate to Main Context)
- Force push without approval
- Commit without Orchestrator trigger

### Escalation Rules:
- **Complex merge conflicts** → Escalate to Main Context
- **Push failures** → Report to Orchestrator with error details
- **Branch protection issues** → Escalate to Main Context

---

## Integration in Agent Architecture

### Trigger Matrix Position:

| Event | Triggered By | Triggers |
|-------|--------------|----------|
| Wave complete | Deployment Strategist | **Git Commit Agent** |
| Git commit success | **Git Commit Agent** | Orchestrator (continue loop) |

### Architecture Discipline (Line 2469):

> "Agent Architecture Discipline:
> - Main Context holds conversation only
> - Orchestrator coordinates, doesn't execute
> - Deployment Strategist manages agents, doesn't fix code
> - Fixers fix code, don't commit
> - **Git Commit Agent commits, doesn't fix**"

---

## Agent Lifecycle in Sprint

1. **Planning Phase:** Not active
2. **Execution Phase:**
   - Triggered after each wave completion
   - Commits validated changes
   - Reports back to Orchestrator
3. **Review Phase:** Not active
4. **Merge Phase:**
   - May create PR if required
   - Handles final merge to main
   - Tags releases if applicable

---

## Context Window Optimization

- **LOW Context:** This agent requires minimal context as it only needs:
  - File list from current wave
  - Wave description
  - Commit message template
  - Git status output

- **No Code Analysis:** Unlike Scouts or Fixers, this agent doesn't need to understand code logic, making it extremely efficient

---

## Success Criteria

A successful Git Commit Agent execution includes:

1. All specified files staged correctly
2. Commit message follows template exactly
3. Commit ID generated and recorded
4. Push succeeds to correct branch
5. COMMIT_RESULT.json returned to Orchestrator
6. No merge conflicts, or simple conflicts resolved
7. Timestamp recorded for audit trail

---

## Failure Handling

If the Git Commit Agent encounters issues:

- **Staging failures:** Report missing files to Orchestrator
- **Commit failures:** Include git error message in result
- **Push failures:** Report authentication/permission issues
- **Merge conflicts:**
  - Simple conflicts: Attempt resolution
  - Complex conflicts: Escalate with conflict details

---

## Source Line References

- **Lines 2102-2114:** Initial agent definition in Tier 2 agents
- **Lines 2381-2439:** Detailed specification with protocols, templates, and schemas
- **Line 2114:** Special designation as only agent with git command authority
- **Line 2264-2265:** Trigger matrix positioning
- **Line 2469:** Architecture discipline statement
- **Line 2493:** Ralph Wiggum Loop integration
- **Line 2503:** Merge phase responsibilities

---

*Last Updated: Extracted from Context Window Erosion.txt on 2026-01-25*

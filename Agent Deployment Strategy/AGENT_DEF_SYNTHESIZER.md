# SYNTHESIZER Agent Definition

**Source:** `/home/bozertron/Orchestr8_jr/Agent Deployment Strategy/Context Window Erosion.txt`

---

## Agent Overview

**Name:** SYNTHESIZER Agent
**Tier:** Tier 2 - Execution Agent
**Primary Location:** Lines 163-186, 2066-2071

---

## Mission

**Find patterns across Scout outputs**

*(Source: Line 165)*

---

## Purpose & Rationale

The SYNTHESIZER agent addresses a critical efficiency problem in large-scale codebase analysis:

- When 10 Scouts analyze different files, they might all identify the same root cause (e.g., "sys.path not set")
- The SYNTHESIZER groups these findings so **one fix addresses many files**
- This prevents redundant fixes and reduces context window consumption

*(Source: Lines 167-171)*

---

## Responsibilities

1. **Receive Scout outputs** - Collect analysis results from multiple Scout agents
2. **Identify patterns** - Find common root causes across different problem reports
3. **Group problems** - Cluster related issues by root cause
4. **Determine fix strategies** - Recommend unified approaches for each problem group
5. **Order dependencies** - Assign dependency_order to problem groups for sequential fixing

---

## Agent Characteristics

| Attribute | Value | Source |
|-----------|-------|--------|
| **Purpose** | Combine multiple Scout outputs, identify patterns | Line 2067 |
| **Scope** | Reads Scout outputs, produces grouped analysis | Line 2068 |
| **Output** | SYNTHESIS.json with problem groupings | Line 2069 |
| **Context Usage** | MEDIUM | Line 2070 |
| **Parallelization** | LOW (depends on Scout outputs) | Line 2071 |
| **Count per Sprint** | 1 | Implied from workflow |
| **Triggered By** | ORCHESTRATOR (after all Scouts complete) | Line 150 |

---

## Output Schema

### SYNTHESIS.json Format

```json
{
  "problem_groups": [
    {
      "group_id": "PG-001",
      "root_cause": "sys.path import pattern inconsistency",
      "affected_files": ["projects.py"],
      "pattern_files": ["hvac.py", "electrical.py", "plumbing.py"],
      "fix_strategy": "align with pattern_files",
      "dependency_order": 1
    }
  ]
}
```

*(Source: Lines 175-186)*

### Schema Fields

- **group_id** (string): Unique identifier for the problem group (format: "PG-###")
- **root_cause** (string): The underlying issue causing problems across multiple files
- **affected_files** (array[string]): Files that need to be fixed
- **pattern_files** (array[string]): Reference files that demonstrate the correct pattern
- **fix_strategy** (string): High-level approach to resolve the problem group
- **dependency_order** (number): Execution sequence (lower numbers = higher priority)

---

## Input Dependencies

### Required Inputs

- Scout output JSON files from all deployed Scouts
- Each Scout output contains:
  - Signal path analysis
  - Problem identification
  - Suggested fixes
  - File-specific diagnostics

### Input Source

Scout outputs are generated during the **Scouting Phase** and collected by the ORCHESTRATOR before deploying the SYNTHESIZER.

*(Source: Lines 148-150)*

---

## Workflow Integration

### Position in Agent Pipeline

```
ORCHESTRATOR
    ↓
Deploys Scouts (parallel)
    ↓
Waits for all Scout outputs
    ↓
Runs SYNTHESIZER ← [YOU ARE HERE]
    ↓
Deploys Fixers (dependency order)
    ↓
VALIDATOR
```

*(Source: Lines 147-152)*

### Context Estimation

When used in complex analysis workflows:
- **Scout + Synthesizer combo**: ~10K tokens each
- **Wave 1 Foundation Analysis**: 8 Scouts + 1 Synthesizer = 69K total context

*(Source: Lines 2220, 2526)*

---

## Constraints & Rules

### Behavioral Constraints

1. **Must wait** for all Scout outputs before processing
2. **Low parallelization** - Only one SYNTHESIZER runs per wave (depends on Scout outputs)
3. **No execution authority** - Does NOT apply fixes, only groups and recommends
4. **Context preservation** - Outputs structured JSON only, never raw file contents

### Design Principles

- **Pattern recognition over repetition** - Group similar problems to avoid redundant fixes
- **Dependency awareness** - Assign execution order to problem groups
- **Reference-based fixes** - Identify working patterns in the codebase to guide fixes

---

## Related Agents

### Upstream Dependencies

- **ORCHESTRATOR**: Triggers SYNTHESIZER after Scout phase completes
- **SCOUT Agents**: Provide input data for pattern analysis

### Downstream Consumers

- **FIXER Agents**: Receive problem group definitions from SYNTHESIS.json
- **ORCHESTRATOR**: Uses synthesis results to plan Fixer deployments in dependency order

---

## Notes

- The SYNTHESIZER is critical for **context window efficiency** at scale
- Without it, fixing 10 files with the same root cause would require 10 separate Fixer deployments
- With it, 1 Fixer deployment can address multiple files using a unified strategy
- The `pattern_files` field enables "learn from existing code" fix strategies

---

**Document Version:** 1.0
**Extracted:** 2026-01-25
**Extraction Source:** Context Window Erosion.txt (28787 tokens)

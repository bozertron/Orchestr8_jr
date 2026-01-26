# AGENT DEFINITION: REPORTER

## Source Information
- **Document**: Context Window Erosion.txt
- **Primary Definition**: Lines 212-220
- **Summary Table**: Line 470
- **Schema Definition**: Lines 734-765
- **Example Output**: Lines 1268-1347

---

## Agent Identity

**Name**: REPORTER Agent (Compression Layer)

**Layer**: Execution

**Mode**: After Validation

**Timing**: Runs after all validation completes in a sprint phase

---

## Mission Statement

Compress verbose outputs for main context.

---

## Role & Responsibilities

The REPORTER agent serves as the critical compression layer between detailed agent outputs and the main context window. Its primary responsibility is to prevent context window erosion by transforming hundreds of lines of detailed JSON outputs into minimal, actionable summaries.

### Core Responsibilities

1. **Read All Sprint Artifacts**: Aggregate outputs from:
   - Scout JSON files (`.claude/sprint/scouts/*.json`)
   - Synthesis outputs (problem groups, fix strategies)
   - Validator results
   - Any escalation artifacts

2. **Compress Intelligence**: Transform verbose data into executive summaries
   - Example: "500 lines of Scout JSON" → "3 problems found, 2 fixable, 1 needs decision"
   - Preserve critical information while eliminating redundancy
   - Focus on actionable insights, not implementation details

3. **Generate STATUS_REPORT.json**: Create the single source of truth for main context consumption

4. **Prioritize Information**: Structure reports by:
   - Blocking issues first
   - Critical issues second
   - Medium/Low issues last
   - Clear "next action" recommendations

---

## Why This Agent Is Needed

### Problem Statement
- Scout outputs can be 500+ lines of JSON per file
- Multiple scouts × multiple files = massive context consumption
- Main context only needs high-level insights for decision-making
- Without compression, context window fills with implementation details

### Solution
The REPORTER reads all sprint JSONs and produces a minimal STATUS_REPORT that preserves decision-critical information while discarding verbose technical details.

---

## Input Requirements

### Input Files
```
.claude/sprint/
├── scouts/
│   ├── file1.json
│   ├── file2.json
│   └── ...
├── synthesis/
│   ├── PROBLEM_GROUPS.json
│   └── FIX_STRATEGIES.json
├── validators/
│   └── *.json (if validation phase)
└── escalations/
    └── *.json (if any)
```

### Expected Input Structure
- All Scout outputs with traced paths and findings
- Synthesized problem groups with dependency chains
- Proposed fix strategies with tech debt assessments
- Validation results (PASS/FAIL per fix)

---

## Output Schema

### Primary Output: STATUS_REPORT.json

**Location**: `.claude/sprint/STATUS_REPORT.json`

**Schema** (from lines 734-765):
```json
{
  "sprint_id": "string",
  "phase": "SCOUTING | SYNTHESIS | AWAITING_APPROVAL | FIXING | COMPLETE",
  "summary": {
    "files_scouted": "number",
    "total_signal_paths": "number",
    "verified": "number",
    "broken": "number",
    "ambiguous": "number"
  },
  "problem_groups": [
    {
      "id": "string",
      "root_cause": "string",
      "affected_files": ["string"],
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "recommended_strategy": "string"
    }
  ],
  "escalations": [
    {
      "type": "string",
      "description": "string",
      "options": ["string"],
      "recommendation": "string"
    }
  ],
  "next_action": "string"
}
```

### Extended Schema (from example at lines 1268-1347):
```json
{
  "sprint_id": "SPRINT-001-IMPORT-ARCHITECTURE",
  "phase": "SCOUTING_COMPLETE",
  "generated_at": "ISO 8601 timestamp",
  "scouts_deployed": "number",
  "scouts_completed": "number",

  "executive_summary": {
    "verdict": "string (e.g., ARCHITECTURAL REFACTOR REQUIRED)",
    "blocking_issues": "number",
    "critical_issues": "number",
    "medium_issues": "number",
    "low_issues": "number",
    "estimated_fix_time": "string",
    "risk_level": "HIGH | MEDIUM | LOW"
  },

  "blocking_issues": [
    {
      "id": "string (e.g., BLOCK-001)",
      "severity": "BLOCKING",
      "title": "string",
      "file": "string (absolute path)",
      "line": "number",
      "code": "string (problematic code snippet)",
      "error": "string (error message)",
      "root_cause": "string (explanation)",
      "suggested_fix": {
        "strategy": "string",
        "code_before": "string",
        "code_after": "string",
        "files_affected": ["string"],
        "tech_debt_assessment": "NONE | LOW | MEDIUM | HIGH"
      }
    }
  ],

  "critical_issues": [
    {
      "id": "string (e.g., CRIT-001)",
      "severity": "CRITICAL",
      "title": "string",
      "files": ["string:line"],
      "code": "string",
      "problem": "string",
      "impact": "string",
      "suggested_fix": {
        "strategy": "string",
        "pattern": "string",
        "files_affected": "number",
        "tech_debt_assessment": "string"
      }
    }
  ]
}
```

---

## Constraints & Rules

### Compression Requirements
1. **Brevity First**: Main context should read the entire STATUS_REPORT in < 2 minutes
2. **No Raw File Contents**: Never include full file contents, only relevant snippets
3. **Structured Severity**: Always categorize by BLOCKING → CRITICAL → MEDIUM → LOW
4. **Actionable Only**: Every issue must have a clear "suggested_fix" or "next_action"

### Information Preservation
- Preserve ALL blocking issues with full context
- Preserve critical issues with root cause analysis
- Summarize medium/low issues (can omit if count > 10)
- Always include "next_action" field for main context guidance

### Format Standards
- Use absolute file paths
- Include line numbers for all code references
- Include code snippets (before/after) for fixes
- Assess tech debt impact for every suggested fix

---

## Relationship to Other Agents

| Agent | Relationship | Data Flow |
|-------|--------------|-----------|
| ORCHESTRATOR | Reports to | REPORTER → STATUS_REPORT.json → ORCHESTRATOR → Main Context |
| SCOUT | Reads outputs | Scout JSON files → REPORTER (compression) |
| SYNTHESIZER | Reads outputs | PROBLEM_GROUPS.json → REPORTER (summarization) |
| VALIDATOR | Reads outputs | Validation results → REPORTER (pass/fail summary) |
| Main Context | Provides to | STATUS_REPORT.json is the ONLY artifact main context reads |

---

## Agent Type Classification

**From Agent Type Summary Table (Line 464-470)**:
```
Agent       Layer       Mode              Responsibility
REPORTER    Execution   After Validation  Compress all outputs into minimal
                                         STATUS_REPORT for main context
```

---

## Key Design Principles

### Context Window Preservation
The REPORTER exists solely to prevent context window erosion. Without it:
- Main context would need to read 500+ line Scout JSONs
- Context fills with implementation details
- Strategic decision-making suffers from information overload

### Single Source of Truth
The STATUS_REPORT.json is the **ONLY** artifact that main context should consume from a sprint. All other JSON files remain in `.claude/sprint/` for audit trail but are not sent to main context.

### Compression Ratio
Target compression ratio: **10:1 to 50:1**
- Input: 500-5000 lines of detailed agent outputs
- Output: 50-200 lines of executive summary

---

## Example Compression

### Before (Scout Output - Verbose)
```json
{
  "file": "/path/to/projects.py",
  "imports": [
    {"line": 14, "code": "from ...core.project_database import ProjectDatabase"},
    // ... 30 more imports
  ],
  "traced_paths": [
    // ... 100 lines of trace data
  ],
  "termination_analysis": {
    // ... 50 lines of analysis
  }
}
```

### After (STATUS_REPORT - Compressed)
```json
{
  "blocking_issues": [
    {
      "id": "BLOCK-001",
      "title": "projects.py relative import beyond top-level package",
      "file": "/path/to/projects.py",
      "line": 14,
      "root_cause": "Three-dot relative import tries to traverse above 'api' package",
      "suggested_fix": {
        "strategy": "Use sys.path pattern like other route files"
      }
    }
  ]
}
```

**Compression achieved**: 200+ lines → 12 lines (16:1 ratio)

---

## Status

**Implementation Status**: Defined in architecture, awaiting template creation

**Dependencies**:
- Requires Scout outputs to exist
- Requires Synthesizer outputs (if synthesis phase complete)
- May require Validator outputs (if validation phase complete)

**Next Steps**:
1. Create REPORTER_PROMPT.md template
2. Define exact compression algorithms
3. Establish quality metrics (compression ratio, information preservation)
4. Test with real Scout outputs

---

## Notes

- The REPORTER is a **reactive** agent - only runs after other agents complete
- It has **read-only** access to sprint artifacts
- It is the **final** agent in any sprint phase before returning to main context
- The Orchestrator is responsible for triggering the REPORTER at appropriate milestones

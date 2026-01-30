# JFDI System Review Prompt Template

**Version**: 1.0  
**Created**: 2025-10-02  
**Purpose**: Comprehensive, reusable template for production-readiness audits of any codebase subsystem  
**Lessons From**: Task 4.1 (Database Initialization), Task 4.2 (P2P Lifecycle Management)

---

## USAGE INSTRUCTIONS

To use this template for a new subsystem review:

1. **Copy this entire template** to a new prompt
2. **Replace ALL bracketed placeholders** with specific values (see Part 1)
3. **Perform context capacity assessment** before starting (see Part 2)
4. **Execute review** following multi-pass strategy if needed (see Part 3)
5. **Create checkpoint reports** if pressure valves trigger (see Part 2)
6. **Complete gap analysis** to verify 100% coverage (see Part 3, Step 6)
7. **Provide consolidated summary** with all findings (see Part 5)

---

## PART 1: MISSION STATEMENT (GENERICIZED)

# MISSION: Final Pass Code Audit - [SUBSYSTEM_NAME] (Task [TASK_NUMBER])

## OBJECTIVE

Conduct a comprehensive, production-readiness audit of the [SUBSYSTEM_NAME] to identify and document ALL issues, incomplete implementations, stubs, architectural conflicts, and technical debt before MVP launch. This is a stabilization pass—NOT a feature development pass.

## SCOPE: Task [TASK_NUMBER] - [SUBSYSTEM_NAME]

**Target Files:**

```
[TARGET_DIRECTORY]
├── [TARGET_FILES_LIST]
│   ├── [file1.rs]
│   ├── [file2.rs]
│   └── [subdirectory/]
│       ├── [file3.rs]
│       └── [file4.rs]
```

**Integration Points:**

```
[INTEGRATION_POINTS_LIST]
├── [integration_file1.rs]
├── [integration_file2.rs]
└── [integration_file3.rs]
```

**Output Report:**

- Primary: `[OUTPUT_REPORT_PATH]`
- Checkpoint (if needed): `[OUTPUT_REPORT_PATH]_CHECKPOINT_[N].md`
- Supplementary (if needed): `[OUTPUT_REPORT_PATH]_SUPPLEMENTARY.md`
- Gap Analysis (if needed): `[OUTPUT_REPORT_PATH]_GAP_ANALYSIS.md`
- Consolidated (if needed): `[OUTPUT_REPORT_PATH]_CONSOLIDATED.md`

**Related Documentation:**

- Pattern Bible: `/home/bozertron/EPO - JFDI - Maestro/CLAUDE_jfdi_pattern_bible.md`
- Task Handoff: `[TASK_SPECIFIC_HANDOFF_DOC]`
- Warnings Log: `[TASK_SPECIFIC_WARNINGS_LOG]`

---

## PART 2: CONTEXT MANAGEMENT & PRESSURE VALVES (CRITICAL)

### CONTEXT CAPACITY ASSESSMENT (Perform BEFORE starting review)

**Step 1: Estimate Total Content Volume**

Use `view` tool with `type=directory` on `[TARGET_DIRECTORY]` to discover all files:

```bash
# Example commands to run:
view [TARGET_DIRECTORY] type=directory
view [TARGET_DIRECTORY]/subdirectory1 type=directory
view [TARGET_DIRECTORY]/subdirectory2 type=directory
```

Create inventory table:

| File Path | Lines | Category |
|-----------|-------|----------|
| [file1.rs] | [XXX] | [Standard/High/Very-High/Extreme] |
| [file2.rs] | [XXX] | [Standard/High/Very-High/Extreme] |

**File Categories:**

- **Extreme-context files (>2000 lines):** Review ALONE in dedicated pass
- **Very-high-context files (1000-2000 lines):** Review with max 2-3 small supporting files (<100 lines each)
- **High-context files (500-1000 lines):** Review with max 5-6 supporting files
- **Standard files (<500 lines):** Review in batches of 8-12 files

**Step 2: Calculate Review Capacity**

**Total files discovered:** [COUNT]  
**Total lines discovered:** [COUNT]  
**Extreme-context files:** [COUNT]  
**Very-high-context files:** [COUNT]  
**High-context files:** [COUNT]  
**Standard files:** [COUNT]

**Recommended Strategy:**

- **Single-pass review:** If total <15,000 lines AND no extreme-context files
- **Multi-pass review:** If total >15,000 lines OR any extreme-context files exist
- **Checkpoint reports:** If any pass exceeds 10,000 lines

**Step 3: Create Review Plan**

**Pass 1 (Core Files):**

- [List largest/most critical files]
- Estimated lines: [COUNT]

**Pass 2 (Supporting Files):**

- [List supporting files and integration points]
- Estimated lines: [COUNT]

**Pass 3 (Helpers/Tests):**

- [List helper modules, tests, edge cases]
- Estimated lines: [COUNT]

**Gap Analysis Pass:**

- Verify nothing was missed
- Create supplementary audit if needed

**User Confirmation Required:** If total content >15,000 lines, confirm plan with user before proceeding.

### PRESSURE VALVE TRIGGERS

You MUST pause and create a checkpoint report if ANY of these occur:

- ✋ You've read >10,000 lines of code in current session
- ✋ You notice yourself forgetting types/structures from earlier files
- ✋ Your issue catalog is becoming disorganized or incomplete
- ✋ You're tempted to "skim" instead of reading every line
- ✋ You're considering marking files as "out of scope" without explicit user confirmation
- ✋ You've been working on this audit for >60 minutes of continuous analysis

### CHECKPOINT REPORT PROTOCOL

When a pressure valve triggers:

1. **Create checkpoint report:** `[OUTPUT_REPORT_PATH]_CHECKPOINT_[N].md`

2. **Checkpoint report structure:**

   ```markdown
   # CHECKPOINT REPORT - REVIEW INCOMPLETE
   
   **Checkpoint Number:** [N]
   **Date:** [DATE]
   **Reason for Checkpoint:** [Pressure valve that triggered]
   
   ## Files Reviewed So Far
   | File Path | Lines | Status |
   |-----------|-------|--------|
   [List all files reviewed with line counts]
   
   ## Files Remaining
   | File Path | Lines | Planned Pass |
   |-----------|-------|--------------|
   [List all files NOT yet reviewed]
   
   ## Issues Found So Far
   [Categorized issue list]
   
   ## Type Inventory So Far
   [Types cataloged so far]
   
   ## Next Steps
   - Resume with Pass [N+1]
   - Starting with: [file list]
   - Estimated lines: [COUNT]
   
   **STATUS:** CHECKPOINT REPORT - REVIEW INCOMPLETE - RESUMING IN NEXT PASS
   ```

3. **Resume with fresh context** starting with remaining files

---

## PART 3: EXECUTION PROCESS (ENHANCED)

### STEP 1: Pre-Review Planning

1. **Perform context capacity assessment** (see Part 2)
2. **Create review plan** with passes defined
3. **Confirm plan with user** if total content >15,000 lines
4. **Document plan** in audit report header

### STEP 2: Deep Dive Code Review (Multi-Pass Capable)

For each pass in your review plan:

**A. Read EVERY Line**

- Use `view` tool to read complete files (no skimming)
- For files >500 lines, use `view_range` to read in chunks if needed
- Document every type, function, struct, enum, trait
- Note every TODO, FIXME, unimplemented!(), todo!()
- Identify all stub implementations

**B. Recursively Explore Directory Structure**

```bash
# Discover all subdirectories
view [TARGET_DIRECTORY] type=directory

# For each subdirectory found:
view [TARGET_DIRECTORY]/subdirectory type=directory

# Continue recursively until all files discovered
```

Look for:

- Hidden helper modules not listed in file tree
- Subdirectories with supporting code
- Related test files (tests.rs, test_*.rs,*_test.rs)
- Configuration files
- Build scripts (build.rs)
- Documentation files

**C. Verify Integration Points**

Read COMPLETE files (not just regex searches) for:

- `[INTEGRATION_POINTS_LIST]`
- Any file that imports from `[TARGET_DIRECTORY]`
- Any file imported by files in `[TARGET_DIRECTORY]`

**D. Identify ALL Issues**

Document every instance of:

- **Stub implementations:** `todo!()`, `unimplemented!()`, placeholder logic, dummy return values
- **Incomplete error handling:** `unwrap()`, `expect()` without context, ignored Results
- **Missing functionality:** Referenced in comments but not implemented
- **Type mismatches:** Inconsistent types, missing conversions
- **Architectural violations:**
  - Files >200 lines (list each with actual line count)
  - Functions >30 lines (list each with actual line count)
  - Circular dependencies
  - JavaScript state (should be Rust-only)
- **Unused code:** Imports, fields, methods (analyze per zero-warning-by-implementation philosophy)
- **Incorrect patterns:** Anti-patterns, inefficient code
- **Dead code:** Unreachable code, duplicate implementations
- **Missing tests:** Untested functionality
- **Configuration gaps:** Missing in-tool config, missing settings panel config

### STEP 3: Cross-Reference Documentation

Review these critical documents:

1. **Pattern Bible** (AUTHORITATIVE SOURCE):
   - `/home/bozertron/EPO - JFDI - Maestro/CLAUDE_jfdi_pattern_bible.md`
   - Focus on "Project Structure - Hyper-Modular Architecture" section
   - Note documented structure for `[TARGET_DIRECTORY]`

2. **Task-Specific Documentation**:
   - `[TASK_SPECIFIC_HANDOFF_DOC]` - Implementation handoff
   - `[TASK_SPECIFIC_WARNINGS_LOG]` - Known warnings and issues

3. **Related Documentation**:
   - Any other docs in `/home/bozertron/EPO - JFDI - Maestro/docs/` related to this subsystem

### STEP 4: Generate Comprehensive Audit Report

**Create file:** `[OUTPUT_REPORT_PATH]`

**NO FILE SIZE RESTRICTIONS** - Comprehensiveness is paramount

**Required Report Structure (7 Mandatory Sections):**

---

#### SECTION 1: TYPE INVENTORY (MANDATORY FIRST SECTION)

List EVERY type used across all reviewed files.

**Categories to include:**

**1.1 Core Domain Types**

- Structs with field descriptions
- Enums with variant descriptions
- Type aliases

**1.2 Configuration Types**

- Config structs
- Settings enums
- Validation types

**1.3 State Management Types**

- AppState fields
- Component state structs
- Lifecycle state enums

**1.4 Event Types**

- Event enums
- Event handler signatures
- Tauri listen/emit types

**1.5 Error Types**

- Error enums
- Result type aliases
- Error context types

**1.6 Integration Types**

- Types shared with other subsystems
- API boundary types
- Message types

**1.7 External Types**

- From dependencies (crates)
- From standard library
- From Tauri framework

**1.8 Naming Conventions Observed**

- snake_case usage
- camelCase usage
- PascalCase usage
- Consistency assessment

**Format for each type:**

```markdown
**TypeName** (`file.rs:line_number`)
- Field/variant 1: Description
- Field/variant 2: Description
- Usage context: Where and how it's used
```

---

#### SECTION 2: TYPE VALIDATION AGAINST PATTERN BIBLE

For each type identified in Section 1:

**2.1 Missing Pattern Bible Types**

- List types that SHOULD be in Pattern Bible but aren't
- Explain why they should be documented

**2.2 Pattern Bible Types Used Correctly**

- List types that match Pattern Bible definitions
- Confirm correct usage patterns

**2.3 Type System Conflicts**

- Document duplicate types (same name, different implementations)
- Document type mismatches (expected vs. actual)
- Document inconsistent naming conventions
- Document missing type conversions

**2.4 Pattern Bible Update Requirements**

- Propose additions to Pattern Bible
- Propose corrections to Pattern Bible
- Propose clarifications to Pattern Bible

---

#### SECTION 3: FILES REVIEWED

Complete inventory with detailed table:

| File | Lines | Purpose | Status | Dependencies | Dependents | Issues |
|------|-------|---------|--------|--------------|------------|--------|
| [file.rs] | [XXX] | [Description] | [Complete/Incomplete/Stub] | [List] | [List] | [Count by severity] |

**3.1 [Subsystem Name] Files**

- List all files in main subsystem
- Include line counts
- Include status assessment

**3.2 Integration Point Files**

- List all integration point files
- Include how they integrate with subsystem

**3.3 Hidden/Undocumented Files**

- List any files discovered that weren't in original scope
- Explain why they're relevant

**3.4 Missing Files**

- List files that SHOULD exist but don't
- Explain what functionality is missing

**3.5 Total Statistics**

- Total files reviewed: [COUNT]
- Total lines reviewed: [COUNT]
- Largest file: [file.rs] ([XXX] lines)
- Smallest file: [file.rs] ([XXX] lines)
- Average file size: [XXX] lines
- Files over 200 lines: [COUNT]
- Files over 150 lines: [COUNT]
- Files under 50 lines: [COUNT]

---

#### SECTION 4: ARCHITECTURE ANALYSIS

**4.1 Current Architecture (As Implemented)**

Describe actual structure:

```
[TARGET_DIRECTORY]/
├── [actual_subdirectory1]/
│   ├── [actual_file1.rs]
│   └── [actual_file2.rs]
└── [actual_subdirectory2]/
    ├── [actual_file3.rs]
    └── [actual_file4.rs]
```

**Module Hierarchy:**

- Parent modules
- Child modules
- Sibling relationships

**Visibility Patterns:**

- Public API surface (pub exports)
- Crate-internal API (pub(crate))
- Private implementation details

**Export Patterns:**

- mod.rs coordinators
- Re-exports
- Facade patterns

**4.2 Intended Architecture (Per Pattern Bible)**

Describe documented structure from Pattern Bible:

```
[Expected structure from CLAUDE_jfdi_pattern_bible.md]
```

**4.3 Discrepancies**

List differences between current and intended:

- Files in wrong locations
- Missing subdirectories
- Extra subdirectories not documented
- Incorrect module hierarchy
- Visibility mismatches

**4.4 Module Dependency Graph**

Document who imports whom:

```
[file1.rs] → imports → [file2.rs], [file3.rs]
[file2.rs] → imports → [file4.rs]
[file3.rs] → imports → [file4.rs]
```

**Circular Dependencies:** [List any found]

**4.5 Integration Wiring**

**Actual Integration (What IS):**

- How subsystem connects to AppState
- How subsystem connects to other subsystems
- Event flows
- Data flows

**Intended Integration (What SHOULD BE):**

- Expected connections per handoff doc
- Expected event flows
- Expected data flows

**Missing Integration (Gaps):**

- Connections that should exist but don't
- Events that should be emitted but aren't
- Data that should flow but doesn't

---

#### SECTION 5: ISSUE CATALOG (BRUTALLY HONEST)

Categorize ALL issues found:

**5.A CRITICAL ISSUES (Blocks MVP)**

Format for each:

```markdown
**A[N]: [Brief Title]**

**Severity**: CRITICAL  
**Location**: `file.rs:line_number`  
**Issue**: [Detailed description of what's wrong]

**Impact**: 
- [What breaks]
- [What data is at risk]
- [What functionality is unavailable]

**Recommendation**: [Detailed fix with code snippets if applicable]
```

Examples of critical issues:

- Stub implementations in core functionality
- Missing core functionality
- Broken integration points
- Compilation errors
- Data loss risks
- Security vulnerabilities

**5.B ARCHITECTURAL VIOLATIONS**

Format for each:

```markdown
**B[N]: [Brief Title]**

**Severity**: HIGH  
**Location**: `file.rs` ([XXX] lines)  
**Issue**: [Description of violation]

**Impact**: 
- [How it violates JFDI principles]
- [What becomes unmaintainable]

**Recommendation**: [How to fix - usually splitting files or refactoring]
```

Examples of architectural violations:

- Files exceeding 200 lines (list each with actual line count)
- Functions exceeding 30 lines (list each with actual line count)
- Circular dependencies
- State management violations (JS state vs. Rust state)
- Duplicate implementations (same name, different files)
- Missing configuration (in-tool or settings panel)

**5.C TYPE SYSTEM ISSUES**

Format for each:

```markdown
**C[N]: [Brief Title]**

**Severity**: MEDIUM  
**Location**: `file.rs:line_number`  
**Issue**: [Description of type issue]

**Impact**: 
- [Compilation issues]
- [Runtime type errors]
- [Maintainability issues]

**Recommendation**: [How to fix type system]
```

Examples of type system issues:

- Type mismatches
- Missing type definitions
- Inconsistent naming conventions
- Missing Pattern Bible types
- Duplicate types (same name, different implementations)
- Missing type conversions

**5.D CODE QUALITY ISSUES**

Format for each:

```markdown
**D[N]: [Brief Title]**

**Severity**: LOW  
**Location**: `file.rs:line_number`  
**Issue**: [Description of quality issue]

**Impact**: 
- [Code maintainability]
- [Developer experience]
- [Technical debt]

**Recommendation**: [How to improve]
```

Examples of code quality issues:

- Unused imports/fields/methods (with zero-warning-by-implementation analysis)
- Poor error handling (unwrap(), expect() without context)
- Missing documentation
- Inefficient patterns
- Dead code
- Inconsistent formatting

**5.E INTEGRATION ISSUES**

Format for each:

```markdown
**E[N]: [Brief Title]**

**Severity**: MEDIUM  
**Location**: `file.rs:line_number` + `integration_file.rs:line_number`  
**Issue**: [Description of integration issue]

**Impact**: 
- [What doesn't connect]
- [What data doesn't flow]
- [What events don't fire]

**Recommendation**: [How to wire correctly]
```

Examples of integration issues:

- Mismatched APIs between modules
- Missing wiring in integration points
- Configuration gaps
- Event handling gaps
- Missing Tauri commands
- Missing AppState fields

---

#### SECTION 6: CODE QUALITY ASSESSMENT

Provide brutally honest 5-star ratings (⭐⭐⭐⭐⭐) for:

**6.1 Code Structure & Organization**

**Rating**: ⭐⭐⭐⭐☆ ([N]/5)

**Strengths**:

- ✅ [List positive aspects]
- ✅ [List positive aspects]

**Weaknesses**:

- ❌ [List negative aspects]
- ❌ [List negative aspects]

**6.2 Efficiency & Performance Patterns**

**Rating**: ⭐⭐⭐⭐⭐ ([N]/5)

**Strengths**:

- ✅ [Async/await usage]
- ✅ [Resource management]
- ✅ [Caching strategies]

**Weaknesses**:

- ❌ [Inefficient patterns]
- ❌ [Resource leaks]

**6.3 Utility & Maintainability**

**Rating**: ⭐⭐⭐⭐☆ ([N]/5)

**Strengths**:

- ✅ [Error handling]
- ✅ [Logging/tracing]
- ✅ [Documentation]

**Weaknesses**:

- ❌ [Poor error messages]
- ❌ [Missing documentation]

**6.4 Adherence to JFDI Principles**

**Rating**: ⭐⭐⭐⭐☆ ([N]/5)

**EXECUTION FIRST Philosophy**: [Assessment]

- ✅/❌ Complete features vs. stubs
- ✅/❌ Functional implementations vs. placeholders

**Modular Architecture**: [Assessment]

- ✅/❌ Files ≤200 lines
- ✅/❌ Functions ≤30 lines
- ✅/❌ No circular dependencies

**Zero-Warning-By-Implementation**: [Assessment]

- ✅/❌ Unused code has implementation plan
- ✅/❌ No suppressed warnings

**Rust-Only State**: [Assessment]

- ✅/❌ All state in Rust
- ✅/❌ No JavaScript state management

**Configuration Everywhere**: [Assessment]

- ✅/❌ In-tool configuration
- ✅/❌ Settings panel configuration
- ✅/❌ Install wizard configuration

**6.5 Technical Debt Accumulation**

**Rating**: ⭐⭐⭐⭐☆ ([N]/5)

**Critical Debt** (Must fix before MVP):

- [List]

**High-Priority Debt** (Should fix before v1.0):

- [List]

**Medium-Priority Debt** (Can defer):

- [List]

**Low-Priority Debt** (Nice to have):

- [List]

**Overall Assessment**: [Summary of technical debt status]

---

#### SECTION 7: STABILIZATION RECOMMENDATIONS

**ONLY suggest improvements to THIS subsystem.**

**7.1 CRITICAL (Must Fix Before MVP)**

Format for each:

```markdown
**C[N]: [Issue Title]**

**File**: `path/to/file.rs`  
**Issue**: [Description]

**Proposed Solution**:
[Detailed fix with code snippets]

```rust
// Example code showing fix
pub fn fixed_function() -> Result<()> {
    // Implementation
    Ok(())
}
```

**Priority**: CRITICAL  
**Effort**: [X hours]  
**Impact**: [What improves]
**Dependencies**: [What must be fixed first]

```

**7.2 HIGH PRIORITY (Should Fix Before Next Task)**

[Same format as 7.1]

**7.3 MEDIUM PRIORITY (Should Address Before v1.0)**

[Same format as 7.1]

**7.4 LOW PRIORITY (Nice to Have)**

[Same format as 7.1]

**7.5 Summary of Recommendations**

| Priority | Count | Total Effort | Must Complete By |
|----------|-------|--------------|------------------|
| CRITICAL | [N] | [X hours] | Before MVP |
| HIGH | [N] | [X hours] | Before Task [N+1] |
| MEDIUM | [N] | [X hours] | Before v1.0 |
| LOW | [N] | [X hours] | Optional |
| **TOTAL** | **[N]** | **[X hours]** | |

**Immediate Action Items** (Before next task):
1. [Action 1] ([X hours])
2. [Action 2] ([X hours])
3. [Action 3] ([X hours])

**Total Immediate Effort**: [X hours]

---

### STEP 5: Pattern Bible Alignment Check

1. **Review Pattern Bible section** for `[TARGET_DIRECTORY]`
2. **Compare actual structure** with documented structure
3. **Note discrepancies** in audit report (Section 4)
4. **Propose Pattern Bible updates** if current structure is correct but undocumented

**Pattern Bible Update Proposal** (if needed):

```markdown
## Proposed Pattern Bible Entry

### Current Entry (Lines [XXX-YYY])
[Quote current Pattern Bible text]

### Proposed Entry
[Provide corrected/enhanced text]

### Rationale
[Explain why update is needed]
```

---

### STEP 6: Gap Analysis & Verification (MANDATORY FINAL STEP)

After completing initial audit:

**A. Exhaustive File Discovery**

```bash
# Run these commands to discover ALL files
view [TARGET_DIRECTORY] type=directory
view [TARGET_DIRECTORY]/subdirectory1 type=directory
view [TARGET_DIRECTORY]/subdirectory2 type=directory
# ... continue for all subdirectories
```

Create complete file list with line counts.

**B. Create Gap Analysis Table**

| File Path | Reviewed in Initial Audit? | Lines | Reason for Omission (if any) |
|-----------|---------------------------|-------|------------------------------|
| [file1.rs] | ✅ YES | [XXX] | Reviewed in Pass 1 |
| [file2.rs] | ❌ NO | [XXX] | **OMITTED - [Reason]** |
| [file3.rs] | ⚠️ PARTIAL | [XXX] | **Only regex search, not full review** |

**C. Calculate Omission Statistics**

| Category | Claimed | Actual | Omitted | Omission Rate |
|----------|---------|--------|---------|---------------|
| [Subsystem] | [N files] | [N files] | [N files] | [X%] |
| **TOTAL** | **[N files]** | **[N files]** | **[N files]** | **[X%]** |

**D. If Gaps Found (Omission Rate >0%)**

1. **Create supplementary audit**: `[OUTPUT_REPORT_PATH]_SUPPLEMENTARY.md`
2. **Use EXACT SAME 7-section structure**
3. **Focus ONLY on omitted files**
4. **Update original audit** with cross-reference banner:

```markdown
# SUPPLEMENTARY AUDIT REQUIRED

**Original Audit**: `[OUTPUT_REPORT_PATH]`  
**Supplementary Audit**: `[OUTPUT_REPORT_PATH]_SUPPLEMENTARY.md`  
**Gap Analysis**: `[OUTPUT_REPORT_PATH]_GAP_ANALYSIS.md`

**Files Omitted from Original Audit**: [N files], [XXX lines] ([X%] of total)

See supplementary audit for complete coverage.
```

**E. Create Consolidated Summary**

**Create file**: `[OUTPUT_REPORT_PATH]_CONSOLIDATED.md`

**Structure**:

1. Executive Summary (original + supplementary findings)
2. Complete File Inventory (all files reviewed)
3. Consolidated Issue Catalog (all issues, re-categorized)
4. Major Discoveries (from supplementary audit)
5. Consolidated Recommendations (merged priorities)
6. Final Production Readiness Assessment

---

## PART 4: CRITICAL CONSTRAINTS

1. ✅ **NO FILE SIZE RESTRICTIONS** on audit report—comprehensiveness is paramount
2. ✅ **READ ENTIRE FILES**—no skimming or sampling (if file is too large, review it alone in dedicated pass)
3. ✅ **DEEP DIRECTORY EXPLORATION**—find all hidden dependencies, tests, helpers
4. ✅ **REALITY CHECK**—document what IS, not what should be (save recommendations for Section 7)
5. ✅ **ZERO NEW FEATURES**—this is stabilization only, not feature development
6. ✅ **PATTERN BIBLE IS LAW**—all recommendations must align with JFDI architectural principles
7. ✅ **TRANSPARENCY**—if you skip ANY file, explicitly acknowledge and explain why
8. ✅ **MULTI-PASS ALLOWED**—quality over speed; create checkpoint reports as needed
9. ✅ **GAP ANALYSIS MANDATORY**—always verify complete coverage at the end
10. ✅ **BRUTALLY HONEST**—document every issue, no matter how small
11. ✅ **CONTEXT MANAGEMENT**—use pressure valves to maintain quality
12. ✅ **SUPPLEMENTARY AUDITS**—create if gaps found, no exceptions

---

## PART 5: SUCCESS CRITERIA

Upon completion, provide:

1. ✅ **Summary of all files reviewed** (with line counts)
   - Original audit: [N files], [XXX lines]
   - Supplementary audit (if any): [N files], [XXX lines]
   - Total: [N files], [XXX lines]

2. ✅ **Total issues found** (categorized by severity)
   - Critical: [N issues]
   - High: [N issues]
   - Medium: [N issues]
   - Low: [N issues]
   - Total: [N issues]

3. ✅ **Pattern Bible alignment status**
   - Compliant: [N files]
   - Violations: [N files]
   - Discrepancies: [N items]

4. ✅ **Top 3-5 critical issues** requiring immediate attention
   - Issue 1: [Title] ([Severity])
   - Issue 2: [Title] ([Severity])
   - Issue 3: [Title] ([Severity])
   - Issue 4: [Title] ([Severity])
   - Issue 5: [Title] ([Severity])

5. ✅ **Gap analysis confirmation**
   - Files discovered: [N]
   - Files reviewed: [N]
   - Files omitted: [N]
   - Coverage: [X%]
   - Supplementary audit created: [YES/NO]

6. ✅ **Checkpoint reports created** (if multi-pass review was needed)
   - Checkpoint 1: [Path]
   - Checkpoint 2: [Path]
   - Total checkpoints: [N]

7. ✅ **Request user feedback** before proceeding to next subsystem

**Final Summary Format**:

```markdown
## Summary

I've completed a comprehensive Final Pass Audit of the [SUBSYSTEM_NAME] (Task [TASK_NUMBER]). Here's what was accomplished:

### Files Reviewed
**Total**: [N files] across [N subsystems] (~[XXX lines])

**Actual Structure**:
- ✅ [Subsystem 1] - [N files] ([XXX lines])
- ✅ [Subsystem 2] - [N files] ([XXX lines])
- ❌ [Missing subsystem] - **NOT IMPLEMENTED**

### Audit Report Created
**Location**: `[OUTPUT_REPORT_PATH]`
**Size**: [XXX lines] (comprehensive analysis)

**Structure**:
1. ✅ Type Inventory - [N+ types] cataloged
2. ✅ Type Validation - Pattern Bible comparison
3. ✅ Files Reviewed - Complete list with dependencies
4. ✅ Architecture Analysis - Current vs. intended
5. ✅ Issue Catalog - [N issues] categorized by severity
6. ✅ Code Quality Assessment - 5-star ratings
7. ✅ Stabilization Recommendations - Prioritized fixes

### Issues Found
**By Severity**:
- Critical: [N issues]
- High: [N issues]
- Medium: [N issues]
- Low: [N issues]

**Total**: [N issues] identified

### Pattern Bible Alignment
**Status**: [✅ COMPLIANT / ⚠️ MOSTLY ALIGNED / ❌ VIOLATIONS FOUND]

**Key Findings**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Top 5 Critical Issues
1. [Issue 1 title] ([Severity])
2. [Issue 2 title] ([Severity])
3. [Issue 3 title] ([Severity])
4. [Issue 4 title] ([Severity])
5. [Issue 5 title] ([Severity])

### Overall Assessment
**Status**: [✅ PRODUCTION-READY / ⚠️ PRODUCTION-READY WITH LIMITATIONS / ❌ NOT PRODUCTION-READY]

[Brief assessment paragraph]

### Immediate Action Items ([X hours] total)
Before proceeding to Task [N+1]:
1. [Action 1] ([X hours])
2. [Action 2] ([X hours])
3. [Action 3] ([X hours])

**Ready for your feedback!** Should I proceed with the immediate action items, or would you like to review the full audit report first?
```

---

## PART 6: LESSONS LEARNED INTEGRATION

### From Task 4.1 (Database Initialization) - SUCCESS FACTORS

**What Worked Well**:

- ✅ Complete file coverage (20 files, ~2,100 lines)
- ✅ Comprehensive type inventory (35+ types cataloged)
- ✅ Detailed issue catalog (10 issues, well-categorized by severity)
- ✅ Honest assessment (production-ready with known limitations)
- ✅ Clear recommendations with effort estimates
- ✅ Pattern Bible comparison identified outdated documentation
- ✅ Discovered dual DatabaseConfig types (configuration drift risk)
- ✅ Identified placeholder implementations (9 functions)
- ✅ Documented missing migration and recovery systems (16 files)

**Key Takeaways**:

- Single-pass review works well for <15,000 lines
- Comprehensive type inventory is essential for understanding system
- Brutally honest assessment builds trust
- Effort estimates help prioritize fixes

### From Task 4.2 (P2P Lifecycle) - LESSONS LEARNED

**What Went Wrong**:

- ⚠️ Initial audit omitted 42% of files (8 files, ~1,069 lines)
- ⚠️ Integration subsystem marked "out of scope" without user confirmation
- ⚠️ Partial reviews (regex searches) instead of full file reads
- ⚠️ Incorrect assessment of relay integration (claimed placeholder, actually 90% complete)
- ⚠️ Incorrect assessment of test coverage (claimed missing, actually comprehensive)
- ⚠️ Major architectural component (event bus) completely missed

**What Went Right**:

- ✅ Gap analysis caught omissions and triggered supplementary audit
- ✅ Supplementary audit discovered major architectural component (event bus)
- ✅ Consolidated summary provided complete picture
- ✅ Transparency about omissions maintained trust
- ✅ Multi-pass review strategy successfully recovered from initial gaps

**Key Takeaways**:

- **NEVER** mark files "out of scope" without explicit user confirmation
- **ALWAYS** read complete files, not just regex searches
- **ALWAYS** perform gap analysis at the end
- **ALWAYS** create supplementary audit if gaps found
- Multi-pass reviews are EXPECTED for large codebases
- Quality over speed is paramount
- Transparency about coverage is critical

### Combined Lessons

**Best Practices**:

1. **Context capacity assessment BEFORE starting** prevents quality degradation
2. **Multi-pass strategy** maintains quality for large codebases
3. **Checkpoint reports** preserve progress and maintain quality
4. **Gap analysis** ensures complete coverage
5. **Supplementary audits** recover from omissions
6. **Consolidated summaries** provide complete picture
7. **Transparency** about coverage builds trust
8. **Brutally honest assessments** identify real issues
9. **Effort estimates** help prioritize fixes
10. **Pattern Bible alignment** ensures architectural consistency

**Anti-Patterns to Avoid**:

1. ❌ Marking files "out of scope" without user confirmation
2. ❌ Partial reviews (regex searches) instead of full file reads
3. ❌ Skimming large files instead of reading every line
4. ❌ Assuming files are "not relevant" without verification
5. ❌ Continuing review when context degradation occurs
6. ❌ Skipping gap analysis at the end
7. ❌ Claiming complete coverage without verification
8. ❌ Making assumptions about implementation status without reading code

---

## PART 7: FINAL NOTES

### Quality Over Speed

- This template prioritizes **QUALITY OVER QUANTITY**
- **Multi-pass reviews are EXPECTED** for large subsystems (>15,000 lines)
- **Checkpoint reports are ENCOURAGED** to maintain quality
- **Gap analysis is MANDATORY** to ensure complete coverage
- **Transparency is REQUIRED** about what was/wasn't reviewed
- The goal is **GROUND TRUTH**, not speed

### When to Use Multi-Pass Strategy

**Single-Pass Review** (Recommended):

- Total content <15,000 lines
- No extreme-context files (>2000 lines)
- All files are standard size (<500 lines)
- Clear, well-documented subsystem

**Multi-Pass Review** (Required):

- Total content >15,000 lines
- Any extreme-context files (>2000 lines)
- Complex integration points
- Poorly documented subsystem
- Context degradation occurs during review

### When to Create Checkpoint Reports

**Create checkpoint if**:

- You've read >10,000 lines in current session
- You notice context degradation (forgetting earlier details)
- Your issue catalog is becoming disorganized
- You're tempted to skim instead of reading every line
- You've been working >60 minutes continuously

### When to Create Supplementary Audits

**Create supplementary audit if**:

- Gap analysis reveals omitted files (omission rate >0%)
- You marked files "out of scope" without user confirmation
- You performed partial reviews (regex searches) instead of full reads
- You discover major components after initial audit

### Success Metrics

**A successful audit**:

- ✅ 100% file coverage (verified by gap analysis)
- ✅ Complete type inventory (all types cataloged)
- ✅ Comprehensive issue catalog (all issues documented)
- ✅ Honest assessment (production-ready status)
- ✅ Clear recommendations (prioritized with effort estimates)
- ✅ Pattern Bible alignment (verified and documented)
- ✅ No omissions (or supplementary audit created if omissions found)

**An unsuccessful audit**:

- ❌ Incomplete coverage (files omitted without supplementary audit)
- ❌ Partial type inventory (types missed)
- ❌ Incomplete issue catalog (issues not documented)
- ❌ Overly optimistic assessment (issues downplayed)
- ❌ Vague recommendations (no effort estimates)
- ❌ Pattern Bible not consulted
- ❌ Omissions not acknowledged

---

## TEMPLATE VERSION HISTORY

**Version 1.0** (2025-10-02):

- Initial template created
- Incorporates lessons from Task 4.1 (Database Initialization)
- Incorporates lessons from Task 4.2 (P2P Lifecycle Management)
- Includes context management strategies
- Includes pressure valve triggers
- Includes multi-pass review capability
- Includes gap analysis and supplementary audit protocols

---

---

## APPENDIX A: EXAMPLE USAGE

### Example: Auditing the Chat Service Subsystem

**Step 1: Fill in placeholders**

```markdown
[TASK_NUMBER] → 5.3
[SUBSYSTEM_NAME] → Chat Service
[TARGET_DIRECTORY] → src-tauri/src/chat/
[TARGET_FILES_LIST] →
├── service/
│   ├── mod.rs
│   ├── chat_service.rs
│   └── message_handler.rs
├── storage/
│   ├── mod.rs
│   └── chat_storage.rs
└── types/
    ├── mod.rs
    └── message.rs

[INTEGRATION_POINTS_LIST] →
├── src-tauri/src/state/app_state.rs
├── src-tauri/src/commands/chat/core.rs
└── src-tauri/src/p2p/message/types.rs

[OUTPUT_REPORT_PATH] → docs/FP/chat_service_FP.md
[TASK_SPECIFIC_HANDOFF_DOC] → docs/task-5.3-chat-service-handoff.md
[TASK_SPECIFIC_WARNINGS_LOG] → docs/task-5.3-warnings-log.md
```

**Step 2: Perform context capacity assessment**

```bash
# Discover all files
view src-tauri/src/chat type=directory
view src-tauri/src/chat/service type=directory
view src-tauri/src/chat/storage type=directory
view src-tauri/src/chat/types type=directory
```

**Result:**

- Total files: 7 files
- Total lines: ~1,200 lines
- Extreme-context files: 0
- Very-high-context files: 0
- High-context files: 1 (chat_service.rs at 650 lines)
- Standard files: 6

**Decision:** Single-pass review (total <15,000 lines, no extreme-context files)

**Step 3: Execute review**

Follow STEP 2 (Deep Dive Code Review) reading all 7 files completely.

**Step 4: Generate audit report**

Create `docs/FP/chat_service_FP.md` with all 7 mandatory sections.

**Step 5: Gap analysis**

Verify all 7 files were reviewed. No gaps found. No supplementary audit needed.

**Step 6: Provide summary**

```markdown
## Summary

I've completed a comprehensive Final Pass Audit of the Chat Service (Task 5.3). Here's what was accomplished:

### Files Reviewed
**Total**: 7 files (~1,200 lines)

### Issues Found
**Total**: 12 issues (1 critical, 3 high, 5 medium, 3 low)

### Top 5 Critical Issues
1. chat_service.rs exceeds 200-line limit (650 lines) - CRITICAL
2. Missing message persistence integration - HIGH
3. Incomplete error handling in message_handler.rs - HIGH
4. Duplicate Message types (chat vs. p2p) - HIGH
5. Missing configuration for message retention - MEDIUM

### Overall Assessment
**Status**: ⚠️ PRODUCTION-READY WITH 1 CRITICAL ARCHITECTURAL VIOLATION

**Ready for your feedback!**
```

---

## APPENDIX B: COMMON PITFALLS & SOLUTIONS

### Pitfall 1: Marking Files "Out of Scope"

**Problem**: Auditor marks integration files as "out of scope" without user confirmation.

**Example** (Task 4.2):
> "Individual integration files (discovery_integration.rs, transport_integration.rs, etc.) were not reviewed in detail for this audit as they are not core to lifecycle management."

**Impact**: 42% of files omitted, major architectural component (event bus) missed.

**Solution**:

- **NEVER** mark files "out of scope" without explicit user confirmation
- If unsure, ask user: "Should I review [files]? They appear related to [subsystem]."
- If context capacity is limited, create checkpoint report and resume later

### Pitfall 2: Partial Reviews (Regex Searches)

**Problem**: Auditor uses regex searches instead of reading complete files.

**Example** (Task 4.2):

```bash
# WRONG: Partial review
view src-tauri/src/state/app_state.rs search_query_regex="p2p|P2P"

# CORRECT: Full review
view src-tauri/src/state/app_state.rs type=file
```

**Impact**: Integration details missed, incomplete understanding of wiring.

**Solution**:

- **ALWAYS** read complete files using `view` tool
- Use regex searches only for initial discovery, then read full files
- Document full file review in "Files Reviewed" section

### Pitfall 3: Context Degradation

**Problem**: Auditor continues review despite forgetting earlier details.

**Symptoms**:

- Forgetting types cataloged earlier
- Losing track of issue catalog
- Struggling to maintain architecture understanding
- Tempted to skim instead of reading every line

**Solution**:

- **STOP** immediately when context degradation occurs
- Create checkpoint report with current findings
- Resume with fresh context in next pass
- Use pressure valve triggers as early warning system

### Pitfall 4: Skipping Gap Analysis

**Problem**: Auditor completes audit without verifying complete coverage.

**Impact**: Omissions not discovered, incomplete audit delivered.

**Solution**:

- **ALWAYS** perform gap analysis at the end (STEP 6)
- Create gap analysis table comparing discovered vs. reviewed files
- If omissions found, create supplementary audit immediately
- Provide consolidated summary merging all findings

### Pitfall 5: Overly Optimistic Assessment

**Problem**: Auditor downplays issues or claims functionality is complete when it's not.

**Example** (Task 4.2 - corrected in supplementary):

- Claimed: "Relay integration is placeholder"
- Reality: Relay integration is 90% complete

**Impact**: Incorrect prioritization, wasted effort on non-issues.

**Solution**:

- **READ THE CODE** - don't assume based on comments
- Document what IS, not what should be
- Be brutally honest about implementation status
- Verify claims by reading actual implementation

---

## APPENDIX C: PRESSURE VALVE DECISION TREE

```
START REVIEW
    ↓
Have you read >10,000 lines? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
Are you forgetting earlier details? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
Is your issue catalog disorganized? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
Are you tempted to skim? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
Considering marking files "out of scope"? ──YES──→ ASK USER FIRST
    ↓ NO
Have you been working >60 minutes? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
CONTINUE REVIEW
    ↓
COMPLETE PASS
    ↓
MORE PASSES NEEDED? ──YES──→ CREATE CHECKPOINT REPORT
    ↓ NO
PERFORM GAP ANALYSIS
    ↓
GAPS FOUND? ──YES──→ CREATE SUPPLEMENTARY AUDIT
    ↓ NO
PROVIDE FINAL SUMMARY
    ↓
END REVIEW
```

---

## APPENDIX D: CHECKPOINT REPORT TEMPLATE

```markdown
# CHECKPOINT REPORT - REVIEW INCOMPLETE

**Checkpoint Number**: [N]
**Date**: [DATE]
**Task**: [TASK_NUMBER] - [SUBSYSTEM_NAME]
**Reason for Checkpoint**: [Pressure valve that triggered]

---

## FILES REVIEWED SO FAR

**Pass [N] Complete**: [N files], [XXX lines]

| File Path | Lines | Status | Issues Found |
|-----------|-------|--------|--------------|
| [file1.rs] | [XXX] | ✅ Complete | [N issues] |
| [file2.rs] | [XXX] | ✅ Complete | [N issues] |
| [file3.rs] | [XXX] | ✅ Complete | [N issues] |

**Total Reviewed**: [N files], [XXX lines]

---

## FILES REMAINING

**Pass [N+1] Planned**: [N files], [XXX lines]

| File Path | Lines | Planned Pass |
|-----------|-------|--------------|
| [file4.rs] | [XXX] | Pass [N+1] |
| [file5.rs] | [XXX] | Pass [N+1] |
| [file6.rs] | [XXX] | Pass [N+1] |

**Total Remaining**: [N files], [XXX lines]

---

## ISSUES FOUND SO FAR

**By Severity**:
- Critical: [N issues]
- High: [N issues]
- Medium: [N issues]
- Low: [N issues]

**Issue List**:

**A1: [Issue Title]** (CRITICAL)
- Location: `file.rs:line`
- Issue: [Description]

**B1: [Issue Title]** (HIGH)
- Location: `file.rs:line`
- Issue: [Description]

[Continue for all issues found so far]

---

## TYPE INVENTORY SO FAR

**Types Cataloged**: [N types]

**Core Types**:
- `TypeName1` (`file.rs:line`)
- `TypeName2` (`file.rs:line`)

[Continue for all types found so far]

---

## ARCHITECTURE NOTES SO FAR

**Current Structure Observed**:
[Description of structure discovered so far]

**Integration Points Verified**:
- [Integration point 1]: ✅ Verified
- [Integration point 2]: ⏳ Not yet reviewed

---

## NEXT STEPS

**Resume with Pass [N+1]**:
- Starting with: [file list]
- Estimated lines: [XXX]
- Estimated time: [X hours]

**Remaining Passes**:
- Pass [N+1]: [Description]
- Pass [N+2]: [Description] (if needed)
- Gap Analysis Pass: Verify complete coverage

---

**STATUS**: CHECKPOINT REPORT - REVIEW INCOMPLETE - RESUMING IN NEXT PASS

**Checkpoint saved**: `[OUTPUT_REPORT_PATH]_CHECKPOINT_[N].md`
```

---

## APPENDIX E: GAP ANALYSIS TEMPLATE

```markdown
# GAP ANALYSIS REPORT

**Date**: [DATE]
**Task**: [TASK_NUMBER] - [SUBSYSTEM_NAME]
**Original Audit**: `[OUTPUT_REPORT_PATH]`
**Status**: [GAPS FOUND / NO GAPS FOUND]

---

## EXHAUSTIVE FILE DISCOVERY

**Discovery Method**: `view` tool with `type=directory` on all subdirectories

**Files Discovered**:

| File Path | Lines | Category |
|-----------|-------|----------|
| [file1.rs] | [XXX] | [Standard/High/Very-High/Extreme] |
| [file2.rs] | [XXX] | [Standard/High/Very-High/Extreme] |
| [file3.rs] | [XXX] | [Standard/High/Very-High/Extreme] |

**Total Discovered**: [N files], [XXX lines]

---

## GAP ANALYSIS TABLE

| File Path | Reviewed in Initial Audit? | Lines | Reason for Omission (if any) |
|-----------|---------------------------|-------|------------------------------|
| [file1.rs] | ✅ YES | [XXX] | Reviewed in Pass 1 |
| [file2.rs] | ✅ YES | [XXX] | Reviewed in Pass 1 |
| [file3.rs] | ❌ NO | [XXX] | **OMITTED - Marked "out of scope"** |
| [file4.rs] | ❌ NO | [XXX] | **OMITTED - Not discovered initially** |
| [file5.rs] | ⚠️ PARTIAL | [XXX] | **Only regex search, not full review** |

---

## OMISSION STATISTICS

**By File Count**:

| Category | Claimed | Actual | Omitted | Omission Rate |
|----------|---------|--------|---------|---------------|
| [Subsystem 1] | [N files] | [N files] | [N files] | [X%] |
| [Subsystem 2] | [N files] | [N files] | [N files] | [X%] |
| **TOTAL** | **[N files]** | **[N files]** | **[N files]** | **[X%]** |

**By Line Count**:

| Category | Claimed | Actual | Omitted | Omission Rate |
|----------|---------|--------|---------|---------------|
| [Subsystem 1] | [XXX lines] | [XXX lines] | [XXX lines] | [X%] |
| [Subsystem 2] | [XXX lines] | [XXX lines] | [XXX lines] | [X%] |
| **TOTAL** | **[XXX lines]** | **[XXX lines]** | **[XXX lines]** | **[X%]** |

---

## ROOT CAUSE ANALYSIS

**Why Were Files Omitted?**

**Stated Reason** (from initial audit):
> [Quote from initial audit explaining omission]

**Analysis**: [Assessment of whether reason was valid]

**Actual Reason**: [Root cause - context degradation, incorrect scope assumption, etc.]

---

## IMPACT ASSESSMENT

**Critical Issues Potentially Missed**:
1. [Issue 1 description]
2. [Issue 2 description]
3. [Issue 3 description]

**Severity of Omissions**: [CRITICAL / HIGH / MEDIUM / LOW]

---

## CORRECTIVE ACTION REQUIRED

**Immediate Actions**:

1. ✅ **Create Supplementary Audit Report**: `[OUTPUT_REPORT_PATH]_SUPPLEMENTARY.md`
   - Review all [N] omitted files using EXACT SAME 7-section methodology
   - Focus on [subsystem] ([N files], [XXX lines])

2. ✅ **Update Original Audit Report**: `[OUTPUT_REPORT_PATH]`
   - Add "SUPPLEMENTARY AUDIT REQUIRED" banner at top
   - Update file counts: [N] → [N] files
   - Update line counts: [XXX] → [XXX] lines
   - Cross-reference supplementary audit

3. ✅ **Provide Consolidated Summary**: `[OUTPUT_REPORT_PATH]_CONSOLIDATED.md`
   - Merge findings from original + supplementary audits
   - Re-categorize issues by severity
   - Update top 5 critical issues
   - Revise immediate action items

---

## SUPPLEMENTARY AUDIT SCOPE

The supplementary audit will cover:

**Primary Focus** ([N files], [XXX lines]):
1. [file1.rs] ([XXX lines])
2. [file2.rs] ([XXX lines])
3. [file3.rs] ([XXX lines])

**Total Supplementary Audit Scope**: [N files], [XXX lines]

---

## CONCLUSION

The initial audit was **[COMPLETE / INCOMPLETE]** with [X%] of files omitted.

**Next Step**: Create comprehensive supplementary audit report covering all omitted files.

---

**Gap Analysis Complete** - Proceeding to supplementary audit creation.
```

---

## APPENDIX F: CONSOLIDATED SUMMARY TEMPLATE

```markdown
# CONSOLIDATED AUDIT SUMMARY

**Date**: [DATE]
**Task**: [TASK_NUMBER] - [SUBSYSTEM_NAME]
**Original Audit**: `[OUTPUT_REPORT_PATH]`
**Supplementary Audit**: `[OUTPUT_REPORT_PATH]_SUPPLEMENTARY.md`
**Gap Analysis**: `[OUTPUT_REPORT_PATH]_GAP_ANALYSIS.md`
**Status**: COMPLETE COVERAGE ACHIEVED

---

## EXECUTIVE SUMMARY

**Complete Audit Coverage**:
- **Original Audit**: [N files], [XXX lines]
- **Supplementary Audit**: [N files], [XXX lines]
- **Total Coverage**: [N files], [XXX lines] (100% of scope)

**Critical Findings (Consolidated)**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Overall Assessment**: [Status]

---

## COMPLETE FILE INVENTORY

**Total Files**: [N files], [XXX lines]

| File | Lines | Status | Issues | Reviewed In |
|------|-------|--------|--------|-------------|
| [file1.rs] | [XXX] | ✅ Complete | [N] | Original |
| [file2.rs] | [XXX] | ✅ Complete | [N] | Original |
| [file3.rs] | [XXX] | ✅ Complete | [N] | Supplementary |
| [file4.rs] | [XXX] | ✅ Complete | [N] | Supplementary |

---

## CONSOLIDATED ISSUE CATALOG

**Total Issues**: [N] (up from [N] in original audit)

| Severity | Count | Key Issues |
|----------|-------|------------|
| **Critical** | [N] | [List] |
| **High** | [N] | [List] |
| **Medium** | [N] | [List] |
| **Low** | [N] | [List]  |

**Detailed Issue List**:

[Merge issues from original + supplementary, re-categorize by severity]

---

## MAJOR DISCOVERIES (FROM SUPPLEMENTARY AUDIT)

**Discovery 1**: [Title]
- **What Was Missed**: [Description]
- **What Was Found**: [Description]
- **Impact**: [Assessment]

**Discovery 2**: [Title]
- **What Was Missed**: [Description]
- **What Was Found**: [Description]
- **Impact**: [Assessment]

---

## CONSOLIDATED RECOMMENDATIONS

**CRITICAL (Before MVP)** - [X hours]:
1. [Recommendation 1] ([X hours])

**HIGH PRIORITY (Before Next Task)** - [X hours]:
2. [Recommendation 2] ([X hours])
3. [Recommendation 3] ([X hours])

**MEDIUM PRIORITY (Before v1.0)** - [X hours]:
4. [Recommendation 4] ([X hours])
5. [Recommendation 5] ([X hours])

**LOW PRIORITY (Optional)** - [X hours]:
6. [Recommendation 6] ([X hours])

**Total Effort**: [X hours]

---

## PRODUCTION READINESS ASSESSMENT (CONSOLIDATED)

**Status**: [Assessment]

**Core System**: [Assessment]
**Architectural Compliance**: [Assessment]
**Code Quality**: [Assessment]

**Blocking Issues**: [List]
**Non-Blocking Issues**: [List]

**Recommendation**: [Final recommendation]

---

## CONCLUSION

[Summary paragraph]

**Next Step**: [What should happen next]

---

**Consolidated Audit Complete** - Awaiting user decision on immediate actions.
```

---

**END OF TEMPLATE**

To use this template, copy it to a new prompt and replace all bracketed placeholders with specific values for your subsystem review.

**Template saved**: `/home/bozertron/EPO - JFDI - Maestro/system_review_prompt.md`

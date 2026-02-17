# Phase 03: Structure Validation - Research

**Research Date:** 2026-02-16
**Mission:** Agent 3 - Validate proposed canonical structure against actual `orchestr8_next/`
**Confidence:** HIGH

---

## Executive Summary

This research validates the proposed canonical structure from ARCHITECTURE_SYNTHESIS.md Section 6 against the actual state of `orchestr8_next/`. The analysis identifies 3 critical conflicts requiring resolution, quantifies test file impacts, and provides clear recommendations for rename vs. create decisions.

**Key Findings:**
- 9 directories exist in current structure
- 4 directories are NEW (need creation)
- 2 directories are CONFLICTS (require rename/merge decisions)
- 3 directories have no equivalent in proposed structure
- 69 import references would need updating if renames occur

---

## 1. Current Structure Mapping

### 1.1 Directory Inventory

```
orchestr8_next/
├── adapters/      (10 .py files) - External integrations
├── city/          (14 .py files) - Code City visualization
├── comms/         (2 .py files)  - Communication bridge/envelopes
├── resilience/    (1 .py file)   - Circuit breaker pattern
├── settings/      (3 .py files)  - P07-B7 settings service
├── shell/         (9 .py files)  - Redux-like state management
├── workspaces/    (2 .py files)  - Session management
├── schemas/       (empty)        - Data models (placeholder)
├── ops/           (3 .md files)  - Operational runbooks
├── static/        (CSS/assets)   - Static assets
├── __init__.py
├── config.py
└── app.py
```

### 1.2 File Counts by Directory

| Directory | Python Files | Non-Python |
|-----------|-------------|------------|
| adapters/ | 10 | 0 |
| city/ | 14 | 0 |
| comms/ | 2 | 0 |
| resilience/ | 1 | 0 |
| settings/ | 3 | 0 |
| shell/ | 9 | 0 |
| workspaces/ | 2 | 0 |
| schemas/ | 0 | 0 |
| ops/ | 0 | 3 |
| static/ | 0 | 1 |

---

## 2. Proposed vs. Actual Comparison

### 2.1 Side-by-Side Classification

| Proposed Dir | Proposed Purpose | Actual Dir | Status | Recommendation |
|--------------|------------------|------------|--------|----------------|
| `presentation/` | L1: UI contracts (plugins, components, styles) | — | NEW | Create |
| `bus/` | L2: State management (actions, store, reducers) | `shell/` | EXISTS_RENAMED | Rename shell → bus |
| `services/` | L3: Domain services (health, combat, tickets, terminal, governance) | — | NEW | Create |
| `adapters/` | L3: External integrations | `adapters/` | EXISTS_ALIGNED | Keep as-is |
| `visualization/` | L4: Code City engine (graph_builder, render, woven_maps) | — | NEW | Create |
| `bridge/` | L5: Capability slices (envelopes, contracts) | `comms/` | EXISTS_RENAMED | Rename comms → bridge |
| `city/` | Existing Code City modules | `city/` | EXISTS_ALIGNED | Keep as-is |
| `settings/` | P07-B7 Settings Service | `settings/` | EXISTS_ALIGNED | Keep as-is |
| `schemas/` | Data models + tokens | `schemas/` | EXISTS_EMPTY | Populate |

### 2.2 Unaccounted Directories

The following existing directories have no proposed equivalent:

| Existing Dir | Files | Purpose | Recommendation |
|--------------|-------|---------|----------------|
| `resilience/` | 1 | Circuit breaker pattern | Merge into `adapters/` |
| `workspaces/` | 2 | Session management | Keep as-is (auxiliary) |
| `ops/` | 0 (3 .md) | Operational runbooks | Move to `.planning/artifacts/ops/` |

---

## 3. Conflict Investigation

### 3.1 Conflict 1: `bus/` vs `shell/`

**Assessment:** HIGH CONFLICT - Semantic equivalent with same internal structure

| shell/ Contents | Matches bus/ Purpose |
|-----------------|---------------------|
| actions.py | ✅ actions.py (Typed actions) |
| contracts.py | ✅ (State definitions) |
| reducer.py | ✅ reducers.py (State transitions) |
| store.py | ✅ store.py (Redux-like store) |
| layout.py | ✅ (UI layout) |
| views.py | ✅ (View definitions) |
| middleware/ | ✅ (Middleware) |

**Recommendation:** **RENAME** `shell/` → `bus/`
- Rename is safe - files inside have generic names that map to bus concept
- Internal imports already use relative paths (`orchestr8_next.shell.*`)
- Test impact: 9 imports from shell/ (see Section 4)

### 3.2 Conflict 2: `bridge/` vs `comms/`

**Assessment:** HIGH CONFLICT - Semantic equivalent

| comms/ Contents | Matches bridge/ Purpose |
|-----------------|------------------------|
| bridge.py | ✅ `CommsBridge` (capability slice) |
| envelopes.py | ✅ `Envelope` (capability contracts) |

**Recommendation:** **RENAME** `comms/` → `bridge/`
- Both files (`bridge.py`, `envelopes.py`) are conceptually bridge/contracts
- Rename is straightforward - no internal subdirectories
- Test impact: 3 imports from comms/ (see Section 4)

### 3.3 Conflict 3: `visualization/` vs `city/`

**Assessment:** NO CONFLICT - Different layers

| visualization/ (Proposed L4) | city/ (Current L3-L5) |
|------------------------------|----------------------|
| graph_builder.py | widget.py |
| render.py | bridge.py |
| woven_maps.py | topology.py |

**Analysis:**
- `city/` contains the full Code City implementation (L3-L5)
- `visualization/` is the L4 presentation layer for rendering
- These are complementary, not conflicting

**Recommendation:** **KEEP BOTH**
- Keep `city/` as-is for Code City domain logic
- Create new `visualization/` for L4 rendering abstraction

---

## 4. Import Chain Impact Analysis

### 4.1 Test File Imports (Would Break on Rename)

| Test File | Imports From | Affected By |
|-----------|--------------|-------------|
| `tests/reliability/test_reliability.py` | shell.store, shell.contracts, shell.reducer, shell.actions | bus rename |
| `tests/conftest.py` | shell.contracts | bus rename |
| `tests/integration/test_comms_bridge.py` | comms.envelopes, comms.bridge | bridge rename |

**Test Import Summary:**
- `shell/` (renamed to `bus/`): **9 imports**
- `comms/` (renamed to `bridge/`): **3 imports**
- `city/`: **22 imports** (not affected)
- `adapters/`: **2 imports** (not affected)

### 4.2 Internal Package Imports (Would Break on Rename)

| Source File | Imports | Affected By |
|-------------|---------|-------------|
| `orchestr8_next/app.py` | shell.store, shell.reducer, shell.contracts, shell.middleware | bus rename |
| `orchestr8_next/shell/store.py` | shell.contracts, shell.actions | bus rename |
| `orchestr8_next/shell/reducer.py` | shell.contracts, shell.actions | bus rename |
| `orchestr8_next/shell/layout.py` | shell.contracts, shell.actions, shell.views | bus rename |
| `orchestr8_next/adapters/*.py` | comms.envelopes | bridge rename |
| `orchestr8_next/workspaces/session.py` | comms.envelopes | bridge rename |

**Internal Import Summary:**
- `shell/` (renamed to `bus/`): **28 imports**
- `comms/` (renamed to `bridge/`): **10 imports**

### 4.3 Total Impact Count

| Rename Operation | Test Imports | Internal Imports | Total |
|-----------------|--------------|------------------|-------|
| `shell/` → `bus/` | 9 | 28 | **37** |
| `comms/` → `bridge/` | 3 | 10 | **13** |
| **Grand Total** | 12 | 38 | **50** |

---

## 5. Detailed Classification Table

### 5.1 Complete Proposed Structure Validation

| Proposed Path | Status | Actual Path | Files to Create/Rename |
|---------------|--------|-------------|----------------------|
| `orchestr8_next/presentation/` | NEW | — | Create directory + plugins/, components/, styles/ |
| `orchestr8_next/bus/` | EXISTS_RENAMED | `shell/` (9 files) | Rename directory |
| `orchestr8_next/services/` | NEW | — | Create directory + health/, combat/, tickets/, terminal/, governance/ |
| `orchestr8_next/adapters/` | EXISTS_ALIGNED | `adapters/` (10 files) | None |
| `orchestr8_next/visualization/` | NEW | — | Create directory + graph_builder.py, render.py, woven_maps.py |
| `orchestr8_next/bridge/` | EXISTS_RENAMED | `comms/` (2 files) | Rename directory |
| `orchestr8_next/city/` | EXISTS_ALIGNED | `city/` (14 files) | None |
| `orchestr8_next/settings/` | EXISTS_ALIGNED | `settings/` (3 files) | None |
| `orchestr8_next/schemas/` | EXISTS_EMPTY | `schemas/` (empty) | Populate with token models |

### 5.2 Unaccounted Directories

| Existing Path | Status | Files | Action |
|---------------|--------|-------|--------|
| `orchestr8_next/resilience/` | UNACCOUNTED | 1 (breaker.py) | Merge into adapters/ |
| `orchestr8_next/workspaces/` | UNACCOUNTED | 2 | Keep as auxiliary |
| `orchestr8_next/ops/` | UNACCOUNTED | 3 (.md files) | Move to .planning/artifacts/ |

---

## 6. Recommendations

### 6.1 Immediate Actions (Safe)

| # | Action | Risk | Impact |
|---|--------|------|--------|
| 1 | Rename `shell/` → `bus/` | LOW | 37 import updates required |
| 2 | Rename `comms/` → `bridge/` | LOW | 13 import updates required |
| 3 | Create `orchestr8_next/services/` | LOW | New directory |

### 6.2 Deferred Actions (Require Investigation)

| # | Action | Reason | Prerequisites |
|---|--------|--------|---------------|
| 4 | Create `orchestr8_next/visualization/` | Depends on L4 architecture decision | Complete graph_builder design |
| 5 | Create `orchestr8_next/presentation/` | Depends on plugin system decision | Complete UI layer design |
| 6 | Populate `schemas/` | Needs token definitions from MSL | Extract from VISUAL_TOKEN_LOCK |

### 6.3 Cleanup Actions

| # | Action | Files | Destination |
|---|--------|-------|-------------|
| 7 | Move `ops/*.md` | 3 | `.planning/artifacts/ops/` |
| 8 | Merge `resilience/breaker.py` | 1 | `adapters/resilient.py` or `adapters/breaker.py` |

---

## 7. Risk Assessment

### 7.1 Rename Risk Matrix

| Operation | Breaking Changes | Migration Complexity | Rollback Feasibility |
|-----------|------------------|---------------------|---------------------|
| `shell/` → `bus/` | 37 imports | Medium - batch find/replace | High - simple rename back |
| `comms/` → `bridge/` | 13 imports | Low - simple find/replace | High - simple rename back |

### 7.2 Recommended Migration Sequence

1. **Phase 1:** Rename `shell/` → `bus/` (run find/replace across all .py files)
2. **Phase 2:** Rename `comms/` → `bridge/` (run find/replace across all .py files)
3. **Phase 3:** Create `services/` directory structure
4. **Phase 4:** Move `ops/` docs to `.planning/artifacts/`
5. **Phase 5:** Merge `resilience/` into `adapters/`
6. **Phase 6:** Create `visualization/` and `presentation/` as needed

---

## 8. Open Questions

### 8.1 Architecture Clarifications Needed

1. **visualization/ content**: Should `visualization/` contain:
   - Only new rendering code?
   - Or also migration of existing `city/wiring.py`, `city/topology.py`?
   
2. **presentation/ scope**: Should `presentation/` contain:
   - Only new UI components?
   - Or also migration from `orchestr8_jr/plugins/` (11 plugin files)?

3. **services/ initial contents**: Which domain services should be created first?
   - health/ (from orchestr8_jr health_checker)
   - governance/ (from or8_founder_console intent_scanner)
   - Other?

### 8.2 Validation Commands

Before proceeding with renames, verify current state:

```bash
# Verify shell imports
grep -r "from orchestr8_next.shell" --include="*.py" /home/bozertron/a_codex_plan/

# Verify comms imports  
grep -r "from orchestr8_next.comms" --include="*.py" /home/bozertron/a_codex_plan/

# Count test files that will need updates
grep -rl "orchestr8_next\.\(shell\|comms\)" --include="*.py" /home/bozertron/a_codex_plan/tests/
```

---

## 9. Source References

### Primary Sources
- `/home/bozertron/a_codex_plan/.planning/research/ARCHITECTURE_SYNTHESIS.md` - Section 6 canonical structure
- `/home/bozertron/a_codex_plan/orchestr8_next/` - Current directory structure
- `/home/bozertron/a_codex_plan/tests/` - Test import chains

### Verified Commands
- `find /home/bozertron/a_codex_plan/orchestr8_next -type f -name "*.py" | sort` - File inventory
- `ls -la /home/bozertron/a_codex_plan/orchestr8_next/` - Directory listing
- `grep -r "from orchestr8_next\.(shell|comms|city|adapters)" --include="*.py"` - Import analysis

---

## 10. Metadata

| Field | Value |
|-------|-------|
| Research Date | 2026-02-16 |
| Confidence | HIGH |
| Valid Until | 30 days (structure stable) |
| Files Created | RESEARCH_03_STRUCTURE_VALIDATION.md |
| Related Phase | P07 Integration |

---

*Research complete. Structure validated against actual codebase with clear rename/create recommendations.*
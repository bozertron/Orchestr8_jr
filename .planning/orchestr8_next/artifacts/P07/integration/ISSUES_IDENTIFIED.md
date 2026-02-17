# ISSUES IDENTIFIED FROM AGENT ANALYSIS
**Generated:** 2026-02-16
**Phase:** P07 Integration Analysis

---

## Summary

Agents A-1 through A-10 analyzed key subsystems in Orchestr8_jr. This document captures the issues and ambiguities identified that need addressing.

---

## CRITICAL ISSUES (Fix Now)

### 1. Unused HealthWatcherManager
**Location:** `IP/health_watcher.py`
**Issue:** HealthWatcherManager exists (lines 134-326) but is never instantiated in 06_maestro.py
**Impact:** Dead code, potential confusion
**Fix:** Either integrate into 06_maestro.py or remove

### 2. Default Watch Paths Limited
**Location:** `IP/health_watcher.py:150`
**Issue:** Default `watch_paths=["IP/"]` may miss other fiefdoms
**Impact:** Health checks may not run for other directories
**Fix:** Make configurable to watch entire project

### 3. Terminal Preference Not Configurable
**Location:** `IP/terminal_spawner.py`
**Issue:** Terminal preference is hardcoded
**Fix:** Added `preferred_terminal` parameter to __init__ (DONE)

---

## AMBIGUITIES (Needs Clarification)

### 4. Neighborhood Status Bug
**Location:** `IP/features/code_city/graph_builder.py:69-74`
**Issue:** Code shows combat > broken > working but there's comment saying neighborhoods mark combat as broken
**Clarification needed:** Which is correct?

### 5. Fiefdom Extraction Fragility
**Location:** `IP/features/code_city/graph_builder.py:161-166`
**Issue:** `_extract_fiefdom()` only uses first directory - nested fiefdoms collapse
**Impact:** `IP/features/code_city/file.py` becomes just `IP`
**Clarification:** Is this intentional?

### 6. Health Result Path Matching
**Location:** `IP/features/code_city/graph_builder.py:366`
**Issue:** Substring matching can cause false positives (`/utils` matches `/utils_helper.py`)
**Clarification:** Should use exact path matching?

### 7. Carl run_deep_scan() Non-functional
**Location:** `IP/carl_core.py`
**Issue:** TypeScript tool is in wrong location (staging vs project root)
**Clarification:** Should we fix the path or remove the method?

### 8. Connection Verifier Hardcoded Builtins
**Location:** `IP/connection_verifier.py`
**Issue:** Stdlib/Node builtins hardcoded, not configurable
**Clarification:** Should this be configurable?

### 9. Connection Verifier Dual Import Paths
**Location:** `IP/connection_verifier.py` vs `IP/features/connections/service.py`
**Issue:** Two ways to import - feature-sliced vs direct
**Clarification:** Standardize on one pattern?

### 10. Terminal Spawner JSON Race Condition
**Location:** `IP/terminal_spawner.py:21-33`
**Issue:** No file locking on state JSON - concurrent writes could collide
**Clarification:** Is this a real concern with marimo's single-threaded model?

---

## NON-CRITICAL (Nice to Have)

### 11. Edge Count Unbounded
**Location:** `IP/features/code_city/graph_builder.py`
**Issue:** No filtering on edge count despite `wire_count` config
**Impact:** Performance with large codebases

### 12. JS Alias Resolution Limited
**Location:** `IP/connection_verifier.py`
**Issue:** Only `@/` and `~/` aliases supported
**Impact:** Complex TypeScript projects may miss broken imports

### 13. No jsconfig.json Support
**Location:** `IP/connection_verifier.py`
**Issue:** No path alias resolution from jsconfig.json
**Impact:** Modern TypeScript projects may have broken resolution

---

## STATUS: RESOLVED

- [x] Terminal preference configurable (added preferred_terminal param)
- [ ] HealthWatcherManager integration (TODO)
- [ ] Watch paths configuration (TODO)
- [ ] Other issues require clarification

---

## QUESTIONS FOR OTHER CODEBASE TEAMS

1. **For mingos_settlement_lab:** Should we fix the neighborhood status bug in graph_builder, or is the current behavior acceptable?

2. **For 2ndFid_explorers:** Should we standardize on feature-sliced imports (service.py) or direct imports for ConnectionVerifier?

3. **For a_codex_plan:** Should run_deep_scan() be fixed or removed from CarlContextualizer?

4. **For all lanes:** Any concerns about the JSON race condition in terminal_spawner, or is marimo's single-threaded model sufficient protection?
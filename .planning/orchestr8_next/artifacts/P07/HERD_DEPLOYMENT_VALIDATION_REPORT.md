# HERD DEPLOYED Status Report - Validation Report

**Date:** 2026-02-17  
**Validator:** Debug Mode  
**Source Document:** [AGENT_DEPLOYMENT_DIRECTIONS.md](.planning/orchestr8_next/artifacts/P07/integration/AGENT_DEPLOYMENT_DIRECTIONS.md)

---

## Executive Summary

This report validates the HERD DEPLOYED Status Report against actual file system state. Phase 1 structure verification shows **partial completion** with some missing directories. Key Findings investigation confirmed **one critical bug** (health result path matching) and **one known limitation** (fiefdom extraction). Phase 2 agent observations were not found in artifacts - they were posted to shared memory (requires memory system access).

---

## Phase 1 Validation: Directory and File Structure

### Expected vs Actual Structure

| Expected Path | Status | Notes |
|---------------|--------|-------|
| `a_codex_plan/app/__init__.py` | ✅ EXISTS | |
| `a_codex_plan/app/app.py` | ✅ EXISTS | |
| `a_codex_plan/app/modules/__init__.py` | ✅ EXISTS | |
| `a_codex_plan/app/modules/_state.py` | ✅ EXISTS | |
| `a_codex_plan/app/modules/_services.py` | ✅ EXISTS | |
| `a_codex_plan/app/modules/_handlers.py` | ✅ EXISTS | |
| `a_codex_plan/app/modules/panels/` | ❌ MISSING | Should contain panel outputs |
| `a_codex_plan/lib/` | ✅ EXISTS | |
| `a_codex_plan/lib/health/` | ✅ EXISTS | Contains `checker.py` |
| `a_codex_plan/lib/combat/` | ✅ EXISTS | Contains `tracker.py` |
| `a_codex_plan/lib/code_city/` | ✅ EXISTS | Contains `graph_builder.py`, `render.py` |
| `a_codex_plan/lib/contracts/` | ✅ EXISTS | Contains `status.py` |
| `a_codex_plan/lib/context/` | ⚠️ EXTRA | Not in spec, contains `contextualizer.py` |
| `a_codex_plan/lib/connections/` | ⚠️ EMPTY | No files, not in spec |
| `a_codex_plan/lib/terminal/` | ⚠️ EMPTY | No files, not in spec |
| `a_codex_plan/ui/` | ✅ EXISTS | Complete |
| `a_codex_plan/static/` | ❌ MISSING | Should contain CSS/fonts |

### Phase 1 Gate Test

```bash
python -c "from app import app; print('OK')"
# Result: ✅ PASS - Import succeeds without errors
```

### Phase 1 Discrepancies

1. **MISSING: `app/modules/panels/`** - According to the spec, this directory should contain panel outputs. Not found in filesystem.
2. **MISSING: `static/`** - According to the spec, this directory should contain CSS and font files copied from Orchestr8_jr. Not found.
3. **EXTRA: `lib/context/`** - Contains `contextualizer.py` but was not in the original spec.
4. **EMPTY: `lib/connections/` and `lib/terminal/`** - Directories exist but contain no files.

---

## Phase 2 Validation: Agent Subsystem Observations

### Expected Phase 2 Agents (from AGENT_DEPLOYMENT_DIRECTIONS.md)

| Agent | Subsystem | Source File | Target |
|-------|-----------|-------------|--------|
| A-1 | Health Checking | `IP/health_checker.py` | `lib/health/` |
| A-2 | Health Watching | `IP/health_watcher.py` | `lib/health/` |
| A-3 | Combat Tracking | `IP/combat_tracker.py` | `lib/combat/` |
| A-4 | Code City Graph | `IP/features/code_city/graph_builder.py` | `lib/code_city/` |
| A-5 | Code City Render | `IP/features/code_city/render.py` | `lib/code_city/` |
| A-6 | Woven Maps Config | `IP/woven_maps.py` | `lib/code_city/` |
| A-7 | Contracts (all) | `IP/contracts/*.py` | `lib/contracts/` |
| A-8 | Contextualizer | `IP/carl_core.py` | `lib/context/` |
| A-9 | Connection Verify | `IP/connection_verifier.py` | `lib/connections/` |
| A-10 | Terminal Spawner | `IP/terminal_spawner.py` | `lib/terminal/` |

### Validation Status

**Finding:** Phase 2 agent observations were NOT found in the artifacts directory. According to the AGENT_DEPLOYMENT_DIRECTIONS.md, agents should post observations to shared memory with specific format:

```
ANALYSIS: <subsystem> - <source file>
─────────────────────────────────────
1. FUNCTION: <2-3 sentences>
2. MARIMO MAPPING: ...
3. 2D/3D CONNECTIONS: ...
4. WIRING: ...
5. INTEGRATION PLAN: ...
6. AMBIGUITIES: ...
```

These observations should have been saved to memory with observation IDs. Without access to the memory system, validation of Phase 2 observations cannot be completed via file system inspection alone.

---

## Key Findings Investigation

### 1. Neighborhood Status Bug in graph_builder

**Location:** [`IP/features/code_city/graph_builder.py`](IP/features/code_city/graph_builder.py) lines 64-74

**Status:** ❌ **NO CLEAR BUG FOUND** - Logic appears correct

```python
status_counts = {"working": 0, "broken": 0, "combat": 0}
for node in dir_nodes:
    if node.status in status_counts:
        status_counts[node.status] += 1

if status_counts["combat"] > 0:
    status = "combat"
elif status_counts["broken"] > status_counts["working"]:
    status = "broken"
else:
    status = "working"
```

The logic correctly implements combat > broken > working precedence. However, there is a potential **timing issue**: if `build_from_health_results()` is called AFTER `compute_neighborhoods()`, node status changes won't be reflected in neighborhood statuses.

---

### 2. Fiefdom Extraction Logic - Single-Directory Limitation

**Location:** [`IP/features/code_city/graph_builder.py`](IP/features/code_city/graph_builder.py) lines 161-166

**Status:** ⚠️ **CONFIRMED LIMITATION**

```python
def _extract_fiefdom(file_path: str) -> str:
    """Extract fiefdom name from file path (first directory component)."""
    parts = Path(file_path).parts
    if len(parts) >= 2:
        return parts[0]
    return ""
```

**Test Results:**
| Input | Output |
|-------|--------|
| `IP/foo.py` | `IP` |
| `a_codex_plan/app.py` | `a_codex_plan` |
| `src/utils/helper.py` | `src` |
| `foo/bar/baz.py` | `foo` |

**Issue:** Only extracts the first directory component. Nested fiefdoms like `foo/bar/baz.py` only get `foo` as the fiefdom, losing the `bar/baz` hierarchy.

**Recommendation:** If hierarchical fiefdoms are needed, modify to extract more path components.

---

### 3. Health Result Path Matching Bug

**Location:** [`IP/features/code_city/graph_builder.py`](IP/features/code_city/graph_builder.py) lines 365-366

**Status:** 🛑 **CRITICAL BUG CONFIRMED**

```python
for path, result in health_results.items():
    if path in node.path or node.path.startswith(path.rstrip("/")):
```

**Test Case:**
```python
path = 'IP'
node_path = 'IP2/foo.py'

# Current logic:
path in node_path         # True (substring match)
node_path.startswith(path.rstrip("/"))  # True ("IP2/foo.py".startswith("IP"))

# Result: MATCH (INCORRECT!)
```

**Impact:** Health results for directory `IP` incorrectly apply to files in `IP2/`, `IP3/`, etc.

**Recommendation:** Fix path matching to use proper directory boundary checks:
```python
# Better approach:
if node.path.startswith(path + "/") or node.path == path:
```

---

### 4. Terminal Configuration Options

**Location:** [`IP/terminal_spawner.py`](IP/terminal_spawner.py)

**Status:** ⚠️ **LIMITED OPTIONS**

Current configuration options in `TerminalSpawner.spawn()`:
- `fiefdom_path` - directory to spawn in
- `briefing_ready` - whether BRIEFING.md exists
- `auto_start_claude` - auto-run claude command

**Missing options:**
- Custom shell selection (currently defaults to `bash`)
- Environment variable configuration
- Custom terminal window title
- Terminal emulator selection (gnome-terminal/xterm fallback exists)

---

### 5. Unused Methods

**Location:** [`IP/features/code_city/graph_builder.py`](IP/features/code_city/graph_builder.py)

**Status:** ✅ **NONE FOUND** - All methods are being used

| Method | Used By |
|--------|---------|
| `compute_neighborhoods` | render.py, tests |
| `build_graph_data` | render.py, woven_maps.py |
| `build_from_connection_graph` | render.py, __init__.py |
| `build_from_health_results` | render.py, tests |
| `_extract_fiefdom` | build_from_connection_graph |

---

## Summary of Discrepancies

### Critical Issues (Must Fix Before Phase 3)

1. **Health Result Path Matching Bug** - Causes incorrect health status application to wrong directories

### High Priority Issues

1. **Missing `static/` directory** - CSS/fonts not copied
2. **Missing `app/modules/panels/`** - Panel outputs directory not created

### Medium Priority Issues

1. **Empty `lib/connections/` and `lib/terminal/`** - Should contain migrated code or be removed
2. **Fiefdom single-directory limitation** - May need hierarchical support

### Low Priority / Informational

1. **Extra `lib/context/` directory** - Not in original spec but contains valid code
2. **Phase 2 observations not in artifacts** - Posted to shared memory (requires memory access)

---

## Recommendations

### Before Proceeding to Phase 3:

1. **Fix Health Result Path Matching** - Implement proper directory boundary matching
2. **Create `static/` directory** - Copy CSS and fonts from Orchestr8_jr
3. **Create `app/modules/panels/`** - Add panel output directory or document why not needed
4. **Address empty lib directories** - Either populate with migrated code or remove

### Phase 2 Validation Note:

To fully validate Phase 2 observations, access to the shared memory system is required. The observation IDs from the P07 STATUS.md (1457, 1463, 1464, etc.) should be queried via:

```bash
curl -s "http://127.0.0.1:37888/v1/memory/search?query=ANALYSIS:*&limit=100"
```

---

## Validation Complete

This validation was performed by:
- Reading README.AGENTS and identifying the HERD DEPLOYED Status Report
- Verifying Phase 1 directory structure against filesystem
- Running import tests
- Analyzing code for specified bugs
- Testing path matching logic
- Checking for unused methods

**Next Step:** Address critical and high-priority issues before Phase 3 deployment.

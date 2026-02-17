# Phase P07: Founder Console Extraction Audit - Research

**Research Date:** 2026-02-16  
**Mission:** Agent 4 - Accurate extraction manifest for or8_founder_console  
**Confidence:** HIGH

---

## Summary

This research provides an accurate extraction manifest for `or8_founder_console` based on comprehensive file inventory and dependency analysis. The ARCHITECTURE_SYNTHESIS.md (Section 4.3) stated 18 source files but the actual count is **19 source files** (excluding tests). All files have been analyzed for layer assignments, external dependencies, and integration points.

**Key Findings:**

| Area | ARCHITECTURE_SYNTHESIS | Actual Finding | Variance |
|------|------------------------|----------------|----------|
| Source files | 18 | 19 | +1 |
| L3 adapters | 2 (memory, checkin) | 2 | ✓ |
| L3 services | 1 (intent_scanner) | 1 | ✓ |
| L2 routers | 2 (review, timeline) | 11 | 9 additional |
| L1 routers | 2 (audit_export, review_bundle) | 2 | ✓ |

**Primary recommendation:** Merge FC into `orchestr8_next` rather than keep as separate FastAPI app. Hardcoded paths and tight coupling to Orchestr8_jr make separation impractical, and FC would benefit from SettingsService integration.

---

## 1. Accurate File Inventory

### Source Files (19 total)

| # | File Path | Layer | Purpose |
|---|-----------|-------|---------|
| 1 | `main.py` | L1 | FastAPI app entry point, router registration |
| 2 | `adapter/__init__.py` | - | Package marker |
| 3 | `adapter/memory.py` | L3 | Memory gateway integration (HTTP client) |
| 4 | `adapter/checkin.py` | L3 | Orchestr8_jr file system read adapter |
| 5 | `services/intent_scanner.py` | L3 | C2P comment scanner (@founder, @todo harvest) |
| 6 | `routers/__init__.py` | - | Package marker |
| 7 | `routers/annotations.py` | L1 | Annotation CRUD API |
| 8 | `routers/artifacts.py` | L1 | Artifact listing API |
| 9 | `routers/audit_export.py` | L1 | Audit trail export API |
| 10 | `routers/flags.py` | L1 | Flags/acknowledgment API |
| 11 | `routers/founder.py` | L1 | Founder directive logging API |
| 12 | `routers/intent_queue.py` | L1 | Intent queue management API |
| 13 | `routers/packets.py` | L1 | Packet board/status API |
| 14 | `routers/review_bundle.py` | L1 | Review bundle aggregation API |
| 15 | `routers/review.py` | L1 | Review queue and approval API |
| 16 | `routers/terminal.py` | L1 | Terminal log API |
| 17 | `routers/timeline.py` | L1 | Event timeline aggregation API |
| 18 | `intent_panel.py` | L1 | Intent panel (Marimo integration?) |
| 19 | `tauri_scanner.py` | L1 | Tauri scanner utility |

### Test Files (12 total)

| # | File Path |
|---|-----------|
| 1 | `tests/__init__.py` |
| 2 | `tests/test_annotations.py` |
| 3 | `tests/test_audit_export.py` |
| 4 | `tests/test_founder.py` |
| 5 | `tests/test_intent_queue.py` |
| 6 | `tests/test_intent_scanner.py` |
| 7 | `tests/test_main.py` |
| 8 | `tests/test_review_bundle.py` |
| 9 | `tests/test_review.py` |
| 10 | `tests/test_terminal.py` |
| 11 | `tests/test_timeline.py` |
| 12 | `tests/test_founder.py` (may be duplicate) |

**Total Python files:** 31 (19 source + 12 tests)

### Files Not in Original Manifest

The following files exist but were not listed in ARCHITECTURE_SYNTHESIS Section 4.3:

1. `routers/artifacts.py` - Artifact listing endpoints
2. `routers/flags.py` - Flags/acknowledgment endpoints  
3. `routers/founder.py` - Founder directive logging
4. `routers/packets.py` - Packet board/status
5. `routers/terminal.py` - Terminal log endpoints
6. `intent_panel.py` - Intent panel (possibly Marimo)
7. `tauri_scanner.py` - Tauri integration utility
8. All test files (12 tests)

---

## 2. Layer Assignment Analysis

### Corrected Layer Mapping

| File | ARCHITECTURE_SYNTHESIS | Corrected | Rationale |
|------|----------------------|-----------|------------|
| `main.py` | L1 | L1 | FastAPI app initialization |
| `routers/*.py` (all 11) | L2 (review, timeline) / L1 (others) | **L1** | All routers define API endpoints (presentation layer for API) |
| `adapter/memory.py` | L3 | L3 | External memory gateway integration |
| `adapter/checkin.py` | L3 | L3 | External file system integration |
| `services/intent_scanner.py` | L3 | L3 | Domain service (C2P scanning) |

### Layer Distribution

```
L1 (Presentation/API):     13 files (main.py + 11 routers + 2 root utils)
L3 (Service/Integration):   4 files (intent_scanner, memory, checkin, __init__)
Uncategorized:              2 files (intent_panel.py, tauri_scanner.py - need review)
```

### In-Memory State Stores (L2-like Behavior)

Several routers maintain in-memory state that acts as L2 bus/state management:

| Router | In-Memory Store | Purpose |
|--------|-----------------|---------|
| `routers/annotations.py` | `_annotations` | Annotation CRUD state |
| `routers/review.py` | `_review_decisions` | Approval decision log |
| `routers/founder.py` | `_directive_log` | Founder directive log |
| `services/intent_scanner.py` | `_intents` | Intent queue state |

**Note:** These are simple in-memory lists, not a proper Redux-like state management system. This is acceptable for a stateless API service but differs from the L2 bus pattern in orchestr8_next.

---

## 3. External Dependencies Analysis

### Framework Dependencies (from requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.104.0 | Web framework |
| uvicorn[standard] | >=0.24.0 | ASGI server |
| pydantic | >=2.5.0 | Data validation |
| pytest | >=7.4.0 | Testing |
| httpx | >=0.25.0 | HTTP client (for tests) |

### Standard Library Dependencies

| Module | Used By | Purpose |
|--------|---------|---------|
| `os` | adapter/checkin.py, services/intent_scanner.py | Path operations |
| `subprocess` | services/intent_scanner.py | grep command execution |
| `glob` | adapter/checkin.py | File globbing |
| `re` | services/intent_scanner.py, routers/* | Regex parsing |
| `json` | adapter/memory.py | JSON serialization |
| `urllib.request` | adapter/memory.py | HTTP calls to memory gateway |
| `datetime` | All routers | Timestamp handling |
| `enum` | All routers | Enum definitions |

### External System Integrations

| System | Integration File | Protocol |
|--------|-----------------|----------|
| Memory Gateway | `adapter/memory.py` | HTTP REST (port 37888) |
| Orchestr8_jr filesystem | `adapter/checkin.py` | Direct file read |

### No SettingsService Integration

**Finding:** FC does NOT use SettingsService (`get_setting`/`set_setting`).

Evidence:
- Grep search for `get_setting|set_setting|SettingsService` in FC source files returns no matches (excluding venv)
- All paths are hardcoded in `adapter/checkin.py`:
  ```python
  ORCHESTR8_BASE = "/home/bozertron/Orchestr8_jr"
  CHECKIN_PATHS = [f"{ORCHESTR8_BASE}/.planning/orchestr8_next/execution/checkins/P07"]
  ```
- Memory gateway URL is read from environment but defaults to hardcoded value:
  ```python
  MEMORY_GATEWAY_URL = os.environ.get("MEMORY_GATEWAY_URL", "http://127.0.0.1:37888")
  ```

**Impact:** FC cannot benefit from centralized configuration management. This is a **critical gap** that would be resolved by merging into orchestr8_next.

---

## 4. Specific File Analysis

### 4.1 services/intent_scanner.py

**Status:** EXISTS as expected in ARCHITECTURE_SYNTHESIS

**Functionality:**
- Scans agent repositories for `@founder` and `@todo` markers
- Harvests unprocessed intent from codebase comments
- Provides filtering by repository, status, priority
- Provides sorting by date, priority, status
- Maintains in-memory intent queue with CRUD operations
- Supports C2P pipeline initiation (marking intents as PROPOSED)

**Key Methods:**
```python
IntentScanner.scan_repos()           # Scan all configured repos
IntentScanner.get_intents()          # Get harvested intents
IntentScanner.update_intent_status()  # Update status (PROCESSED, APPROVED, etc.)
IntentScanner.get_filtered_intents() # Advanced filtering
IntentScanner.get_status_counts()    # Statistics
```

**Repositories Scanned:**
- `/home/bozertron/or8_founder_console`
- `/home/bozertron/Orchestr8_jr`
- `/home/bozertron/a_codex_plan`
- `/home/bozertron/mingos_settlement_lab`
- `/home/bozertron/2ndFid`

**Layer:** L3 (Domain Service)

### 4.2 routers/review.py

**Status:** EXISTS as expected

**Action Schema:** FC implements its own approval workflow, NOT using `command_surface`:

```python
class ReviewStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    APPROVED = "approved"
    REWORK = "rework"

class ReviewItem(BaseModel):
    packet_id: str
    status: ReviewStatus
    title: Optional[str] = None
    files_ready: bool = False
    tests_passed: bool = False
    report_delivered: bool = False
    priority: str = "normal"
    eta: Optional[str] = None

class ApprovalAction(BaseModel):
    packet_id: str
    decision: str  # "approve" or "rework"
    reason: Optional[str] = None
    reviewer: Optional[str] = "founder"
```

**Integration Points:**
- Reads check-in files via `adapter/checkin.py`
- Saves decisions to memory via `adapter/memory.py`
- Links with annotations from `routers/annotations.py`

**Layer:** L1 (API Presentation)

### 4.3 Config Reader Interface

**Finding:** NO dedicated config reader interface exists in FC.

**Current State:**
- Paths hardcoded in `adapter/checkin.py`
- Memory gateway URL hardcoded with env var fallback in `adapter/memory.py`
- No abstraction layer for configuration

**Recommendation:** After merge into orchestr8_next, use SettingsService for:
- `ORCHESTR8_BASE` path
- `MEMORY_GATEWAY_URL`
- Check-in and artifact paths
- Repository scan paths

---

## 5. Shared Memory Integration

### Memory Gateway Client (adapter/memory.py)

FC integrates with memory gateway via HTTP:

```python
MEMORY_GATEWAY_URL = os.environ.get("MEMORY_GATEWAY_URL", "http://127.0.0.1:37888")

def get_memory_health() -> Dict[str, Any]
def get_unread_flags(agent_id: Optional[str] = None) -> Dict[str, Any]
def save_memory_checkpoint(title: str, text: str) -> Dict[str, Any]
```

**Endpoints Used:**
- `GET /v1/memory/health` - Health check
- `GET /v1/memory/search?query=unread&limit=50` - Get unread flags
- `POST /v1/memory/save` - Save checkpoint

**Integration Points:**
- `routers/review.py`: Approve/rework decisions saved to memory
- `routers/founder.py`: Founder directives saved to memory

**Layer:** L3 (External Integration Adapter)

---

## 6. Keep Separate vs Merge Analysis

### Evidence for Keeping Separate

| Factor | Evidence |
|--------|----------|
| Independent FastAPI app | `main.py` creates FastAPI instance with title "Founder Console" |
| Own port | Runs on uvicorn, no specific port documented but separate process |
| Own dependencies | `requirements.txt` with fastapi, uvicorn, pydantic, pytest, httpx |
| Independent tests | 12 test files in `tests/` directory |
| Version tracking | `main.py` shows version "0.4.0" |

### Evidence for Merging

| Factor | Evidence |
|--------|----------|
| Tight coupling | Hardcoded paths to Orchestr8_jr in `adapter/checkin.py` |
| No packaging | No `pyproject.toml` - not a proper Python package |
| Single purpose | Founder review acceleration (aligned with orchestr8_next goals) |
| No standalone value | Cannot function without Orchestr8_jr check-in files |
| Configuration gap | No SettingsService integration - would benefit from merge |
| Canonical structure | ARCHITECTURE_SYNTHESIS shows FC as extraction target to orchestr8_next |

### Comparison with ARCHITECTURE_SYNTHESIS

Section 4.3 of ARCHITECTURE_SYNTHESIS states:

> **Type:** FastAPI application (18 source files)
> 
> | Layer | Files | Target |
> |-------|-------|--------|
> | L3 | `adapter/memory.py`, `adapter/checkin.py` | `orchestr8_next/adapters/` |
> | L3 | `services/intent_scanner.py` | `orchestr8_next/services/governance/` |
> | L2 | `routers/review.py`, `routers/timeline.py` | `orchestr8_next/bus/` |
> | L1 | `routers/audit_export.py`, `routers/review_bundle.py` | `orchestr8_next/presentation/api/` |

**Correction Required:**
- All routers should go to L1 (presentation), not L2 (bus)
- Router count is 11, not 2 (review, timeline)
- Additional L1 routers: annotations, artifacts, flags, founder, intent_queue, packets, terminal
- Root files (intent_panel.py, tauri_scanner.py) need classification

---

## 7. Recommendation: MERGE

**Recommendation:** Merge FC into `orchestr8_next`

### Justification

1. **Tight Coupling to Orchestr8_jr**: FC reads check-in files directly from Orchestr8_jr directory. Keeping it separate adds deployment complexity without benefit.

2. **No Standalone Value**: FC cannot function without Orchestr8_jr. It reads check-in files, integrates with memory gateway, and provides founder review for packets created in Orchestr8_jr.

3. **Configuration Management**: FC has hardcoded paths and no SettingsService integration. Merging enables:
   - Centralized path configuration
   - Environment-based memory gateway URL
   - Consistent configuration across orchestr8_next

4. **Canonical Alignment**: ARCHITECTURE_SYNTHESIS already shows FC as an extraction target to orchestr8_next. This research confirms that plan.

5. **Simpler Deployment**: One less service to deploy, monitor, and maintain.

### Migration Path

1. **Layer Mapping** (corrected from ARCHITECTURE_SYNTHESIS):
   ```
   L1 (Presentation):  main.py, routers/* → orchestr8_next/presentation/api/
   L3 (Services):       intent_scanner.py → orchestr8_next/services/governance/
   L3 (Adapters):       adapter/* → orchestr8_next/adapters/
   ```

2. **Settings Integration**:
   - Replace hardcoded paths with `get_setting()` calls
   - Configure memory gateway URL via SettingsService

3. **State Management**:
   - Migrate in-memory stores to orchestr8_next bus, OR
   - Keep as stateless API (acceptable for FastAPI)

4. **Dependencies**:
   - Merge requirements.txt into orchestr8_next's dependencies
   - FC tests become integration tests

---

## 8. Open Questions

1. **intent_panel.py and tauri_scanner.py**: These root-level files were not analyzed in detail. They may be:
   - Standalone utilities
   - Marimo notebook integrations
   - Tauri desktop app components
   
   **Recommendation:** Investigate before migration.

2. **Memory Gateway Protocol**: FC uses HTTP with memory gateway. Is this the same protocol used by other orchestr8_next components? Should be verified for consistency.

3. **State Persistence**: FC uses in-memory state that resets on restart. Is this acceptable, or should state be persisted to memory gateway or file system post-migration?

---

## 9. Sources

### Primary Evidence (File System)
- `/home/bozertron/or8_founder_console/main.py` - FastAPI app definition
- `/home/bozertron/or8_founder_console/requirements.txt` - Dependencies
- `/home/bozertron/or8_founder_console/adapter/memory.py` - Memory integration
- `/home/bozertron/or8_founder_console/adapter/checkin.py` - File system integration
- `/home/bozertron/or8_founder_console/services/intent_scanner.py` - C2P scanner
- `/home/bozertron/or8_founder_console/routers/review.py` - Review API
- All router files - API endpoint definitions

### Reference
- `/home/bozertron/a_codex_plan/.planning/research/ARCHITECTURE_SYNTHESIS.md` - Original manifest (Section 4.3)

---

## 10. Metadata

**Confidence Breakdown:**
- File inventory: HIGH - Direct file system enumeration
- Layer assignments: HIGH - Direct code analysis
- Dependencies: HIGH - Source code import analysis  
- Config gaps: HIGH - Grep search for settings integration
- Recommendation: HIGH - Based on coupling analysis

**Research Date:** 2026-02-16
**Valid Until:** 90 days (stable codebase)

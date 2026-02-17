# ANALYSIS: Carl Contextualizer

**Source:** `/home/bozertron/Orchestr8_jr/IP/carl_core.py`  
**Analysis Date:** 2026-02-16  
**Agent:** A-8 (Analysis Agent)

---

## 1. Overview

**Carl Contextualizer** is the context aggregation engine for Orchestr8. It acts as a bridge between Python analysis tools and TypeScript tooling, providing unified context for fiefdoms (directory clusters) in the Code City visualization.

**Purpose:** Gather and aggregate context from multiple signal sources (health, connections, combat, tickets, locks) for any given fiefdom, enabling intelligent UI behavior and search.

---

## 2. Function Summary

### Core Class: `CarlContextualizer`

| Method | Purpose | Signature |
|--------|---------|-----------|
| `__init__` | Initialize with root path and signal sources | `(root_path: str, timeout: int = 30, state_managers: Optional[Dict] = None)` |
| `run_deep_scan()` | Execute TypeScript analyzer via subprocess | `() -> Dict[str, Any]` |
| `get_file_context()` | Legacy fallback for LLM file injection | `(rel_path: str) -> str` |
| `gather_context()` | Aggregate all signals for a fiefdom | `(fiefdom_path: str) -> FiefdomContext` |
| `gather_context_json()` | JSON-serialized context for UI | `(fiefdom_path: str) -> str` |

### Data Class: `FiefdomContext`

```python
@dataclass
class FiefdomContext:
    fiefdom: str                           # Fiefdom path (e.g., "IP/")
    health: Dict[str, Any]                 # Health check results
    connections: Dict[str, Any]            # Import graph data
    combat: Dict[str, Any]                 # LLM deployment status
    tickets: List[str]                      # Active tickets
    locks: List[Dict[str, str]]            # Louis file locks
```

---

## 3. Signal Sources (Dependencies)

Carl orchestrates five signal sources:

| Source | Module | Purpose |
|--------|--------|---------|
| Health | `IP/health_checker.py` → `HealthChecker` | Syntax errors, import failures |
| Connections | `IP/connection_verifier.py` → `ConnectionVerifier` | Import graph, broken imports |
| Combat | `IP/combat_tracker.py` → `CombatTracker` | Active LLM deployments |
| Tickets | `IP/ticket_manager.py` → `TicketManager` | Task tracking per fiefdom |
| Locks | `IP/louis_core.py` → `LouisWarden` | File protection status |

**Key Behavior:** All signal sources are optional. Louis initialization uses try/except fallback (lines 61-65).

---

## 4. Marimo Integration

### Import Location
- **`IP/plugins/06_maestro.py:87`** — `from IP.carl_core import CarlContextualizer`

### Instantiation
- **`IP/plugins/06_maestro.py:228`** — `carl = CarlContextualizer(str(project_root_path))`
- Instantiated once at module load, stored in panel initialization block

### Usage Points

#### 1. Code City Node Click (Line 421)
```python
context_scope = derive_context_scope(file_path)  # e.g., "IP/plugins"
context = carl.gather_context(context_scope)
```
- Triggered when user clicks a building in Code City
- `derive_context_scope()` maps file path → parent directory
- Returns `FiefdomContext` with health, connections, combat, tickets, locks
- Passed to `build_code_city_context_payload()` for BuildingPanel display

#### 2. Summon Search (Line 964)
```python
scoped_target = scope or get_selected() or context_scope or "IP"
context = carl.gather_context(scoped_target)
```
- Triggered when user types in Summon search bar
- Search queries are matched against fiefdom name, errors, warnings, tickets
- Returns enriched context dict for result display

#### 3. Shell View (via `IP/features/maestro/views/shell.py:184`)
```python
context_json = carl.gather_context_json(selected_fiefdom)
```

---

## 5. Wiring Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      06_maestro.py                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐ │
│  │ Code City    │    │ Summon       │    │ Shell View       │ │
│  │ Node Click   │    │ Search       │    │ (shell.py)       │ │
│  └──────┬───────┘    └──────┬───────┘    └────────┬─────────┘ │
│         │                    │                      │            │
│         └────────────────────┼──────────────────────┘            │
│                              ▼                                   │
│                    ┌─────────────────┐                          │
│                    │ CarlContextualizer │                         │
│                    │   .gather_context() │                       │
│                    └─────────┬─────────┘                          │
│                              │                                    │
│         ┌────────────────────┼────────────────────┐              │
│         ▼                    ▼                    ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ HealthChecker│    │ Connection  │    │ CombatTracker│        │
│  │             │    │ Verifier    │    │             │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ TicketManager│    │ LouisWarden │    │ TS Tool     │        │
│  │             │    │ (optional)   │    │ (optional)  │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. TypeScript Tool Integration

### Configuration
- **Tool Path:** `frontend/tools/unified-context-system.ts` (referenced in `one integration at a time/` staging area)
- **Expected Output:** `docs/project-context.json`
- **Runner:** `npx tsx` via subprocess
- **Timeout:** 30 seconds (configurable)

### Current Status
The TypeScript tool path in `carl_core.py:23` is:
```python
TS_TOOL_PATH = "frontend/tools/unified-context-system.ts"
```

However, the tool lives at:
```
/home/bozertron/Orchestr8_jr/one integration at a time/frontend/tools/unified-context-system.ts
```

**Ambiguity:** The tool appears to be in a staging area (`one integration at a time/`) rather than the project root. The `run_deep_scan()` method will likely fail if called directly, as the path resolution would look in the wrong location.

### Tool Analysis
The TypeScript tool (`unified-context-system.ts`) is designed for **Rust/Tauri + Vue** projects:
- Phase 1: Runs Rust context-cartographer
- Phase 2: Runs Vue flow analyzer
- Phases 3-7: Pattern analysis, insights, IDE helpers, LLM instructions

**Relevance to Orchestr8:** The tool is designed for a different stack (Rust/Tauri/Vue) than Orchestr8 (Python/Marimo). It may need adaptation or may be deprecated in favor of Python-native analysis.

---

## 7. Integration into a_codex_plan

### Current Status
Carl Contextualizer is **WIRED** per `SOT/CURRENT_STATE.md:56`:
> "CarlContextualizer | WIRED | Summon search + node click context"

### Integration Points for a_codex_plan

| Component | Source | Target | Notes |
|-----------|--------|--------|-------|
| CarlContextualizer | `IP/carl_core.py` | `a_codex_plan/app/modules/context/` | Core module |
| FiefdomContext | dataclass | TypedDict variant | JSON serialization |
| gather_context() | method | context service | Stateless aggregation |
| run_deep_scan() | method | optional adapter | Requires TS tool path fix |

### Required Adaptations for a_codex_plan

1. **Path Resolution:** Update `TS_TOOL_PATH` to point to correct location
2. **TypedDict Variants:** Add static typing for `FiefdomContext` fields
3. **Service Pattern:** Convert to injectable context service
4. **State Management:** Integrate with a_codex_plan's temporal state system

---

## 8. Ambiguities & Concerns

### Ambiguity 1: TypeScript Tool Path
- **Issue:** `TS_TOOL_PATH = "frontend/tools/unified-context-system.ts"` resolves relative to project root, but tool is in `one integration at a time/frontend/tools/`
- **Impact:** `run_deep_scan()` will fail with "file not found"
- **Fix:** Relocate tool or update path constant

### Ambiguity 2: Tool Stack Mismatch
- **Issue:** The TS tool analyzes Rust/Tauri + Vue, not Python/Marimo
- **Impact:** Even if path is correct, output schema doesn't match Orchestr8's needs
- **Fix:** Either adapt tool for Python or deprecate in favor of native analysis

### Ambiguity 3: Deep Scan Usage
- **Issue:** `run_deep_scan()` is defined but never called in the current codebase
- **Impact:** Dead code path; unclear if intended for future use
- **Status:** Currently unused; all context comes from `gather_context()`

### Ambiguity 4: Louis Integration Incomplete
- **Issue:** LouisWarden is instantiated but only checks lock status for matching fiefdom paths (lines 174-178)
- **Impact:** Lock information may be incomplete for nested paths
- **Fix:** Review lock lookup logic for hierarchical fiefdoms

---

## 9. File Locations Summary

| File | Role |
|------|------|
| `IP/carl_core.py` | Main implementation (216 lines) |
| `IP/plugins/06_maestro.py` | Primary consumer (lines 87, 228, 421, 964) |
| `IP/features/maestro/views/shell.py` | Secondary consumer (line 184) |
| `IP/features/maestro/code_city_context.py` | `derive_context_scope()` helper |
| `one integration at a time/frontend/tools/unified-context-system.ts` | TS tool (staging area) |

---

## 10. Test Coverage

No dedicated test file found for `carl_core.py`. Integration tested implicitly via:
- Manual UI testing of node clicks
- Summon search behavior verification

---

## Summary

Carl Contextualizer is a well-architected aggregation layer that pulls together five signal sources into a unified `FiefdomContext` structure. It is actively wired into the Orchestr8 UI via Code City node clicks and Summon search. The main areas requiring attention are the TypeScript tool integration (path mismatch + stack incompatibility) and potential expansion of test coverage.

**Integration into a_codex_plan** is straightforward: the module can be ported as-is with minor path corrections and TypedDict additions for static typing.

# ANALYSIS: Combat Tracking

**Source:** `/home/bozertron/Orchestr8_jr/IP/combat_tracker.py`  
**Date:** 2026-02-16  
**Agent:** A-3 (Analysis Agent)

---

## Overview

The **CombatTracker** is a lightweight state management module that tracks active LLM "General" deployments across the codebase. It marks files that currently have an AI agent working on them, visualizing them as **Purple/COMBAT** status in the Code City.

---

## Architecture

### Core Design
- **Pattern:** File-based JSON state storage
- **State File:** `.orchestr8/combat_state.json`
- **No external dependencies** (pure Python stdlib)
- **115 lines of code** — self-contained and simple

### Data Model
```json
{
  "active_deployments": {
    "/path/to/file.py": {
      "deployed_at": "2026-02-16T10:30:00.000000",
      "terminal_id": "term-001",
      "model": "claude-sonnet-4-20250514"
    }
  }
}
```

---

## API Surface

| Method | Purpose |
|--------|---------|
| `deploy(file_path, terminal_id, model)` | Mark file as actively being worked on |
| `withdraw(file_path)` | Remove deployment when agent finishes |
| `is_in_combat(file_path)` | Check if file has active agent |
| `get_active_deployments()` | Get all deployments with full metadata |
| `get_combat_files()` | Get list of file paths in combat |
| `get_deployment_info(file_path)` | Get metadata for specific file |
| `cleanup_stale_deployments(max_age_hours=24)` | Auto-remove old deployments |

---

## Integration Points

### Primary Consumer: `IP/plugins/06_maestro.py`
- Instantiates `CombatTracker` at render time (line 219)
- Calls `cleanup_stale_deployments()` on each render (line 300)
- Uses `get_deployment_info()` for hover tooltips (line 513)
- Calls `deploy()` when agent selected (lines 540, 616, 650, 898)

### Visualization: `IP/features/code_city/graph_builder.py`
- Imports `CombatTracker` (line 128)
- Gets `combat_files = tracker.get_combat_files()` (line 131)
- Sets `node.status = "combat"` for active files (line 134)

### Context Manager: `IP/carl_core.py`
- Stores `self.combat_tracker` instance (line 57)
- Uses `get_deployment_info()` for fiefdom context (line 163)

---

## Status in System

| Attribute | Value |
|-----------|-------|
| **Integration Status** | WIRED (per SOT/CURRENT_STATE.md) |
| **Completeness** | COMPLETE - Purple state management |
| **Dependencies** | None (stdlib only) |
| **Testability** | High — no external state |

---

## Key Behaviors

### 1. Automatic Cleanup
- Stale deployments (default: 24 hours) are auto-removed on each render
- Prevents zombie deployments from stuck agents

### 2. Status Precedence
From `SOT/CODE_CITY_LANDSCAPE.md`:
> Combat flow + status merge precedence: `combat > broken > working`

This means Purple (combat) takes priority over Blue (broken) and Gold (working).

### 3. Fallback Grace
The graph_builder wraps the import in try/except — if CombatTracker is unavailable, it gracefully degrades without breaking the visualization.

---

## Observations

### Strengths
1. **Zero dependencies** — portable, testable, no version conflicts
2. **Simple state file** — human-readable JSON, easy to debug
3. **Graceful degradation** — consumers handle import failures
4. **Auto-cleanup** — prevents state pollution
5. **Timestamp tracking** — enables staleness detection

### Potential Improvements (Non-Critical)
1. **No locking** — concurrent writes could cause race conditions (unlikely in practice with marimo's single-threaded cell model)
2. **No validation** — accepts any string for terminal_id/model
3. **No event system** — consumers poll rather than react
4. **Single project** — state file is project-scoped, not global

---

## Usage Pattern

```python
from IP.combat_tracker import CombatTracker

tracker = CombatTracker("/path/to/project")

# Track an agent deployment
tracker.deploy("src/main.py", "terminal-7", "claude-opus")

# Check status
if tracker.is_in_combat("src/main.py"):
    info = tracker.get_deployment_info("src/main.py")
    print(f"Agent active since {info['deployed_at']}")

# Agent finished — withdraw
tracker.withdraw("src/main.py")
```

---

## Summary

The CombatTracker is a **mature, stable module** with a clear single responsibility: track which files have active LLM agents deployed. It integrates cleanly with the Code City visualization pipeline and provides the Purple/COMBAT status layer. No immediate concerns — it works as designed.

---

*End of Analysis*

# ANALYSIS: Terminal Spawner

**Source:** `/home/bozertron/Orchestr8_jr/IP/terminal_spawner.py`  
**Date:** 2026-02-16  
**Agent:** A-10 (Analysis Agent)

---

## 1. Function Overview

**Purpose:** Cross-platform terminal spawning for fiefdom deployment. Spawns native terminal windows with proper working directory and startup message context for Claude Code execution.

**Module Size:** 122 lines, 834 tokens

### Core Class: `TerminalSpawner`

| Method | Purpose |
|--------|---------|
| `__init__(project_root: str)` | Initialize with project root path |
| `update_fiefdom_status(fiefdom_path: str, status: str)` | Update fiefdom status in `.orchestr8/state/fiefdom-status.json` |
| `spawn(fiefdom_path: str, briefing_ready: bool, auto_start_claude: bool) -> bool` | Spawn terminal at path, update status to COMBAT |
| `mark_combat_complete(fiefdom_path: str, success: bool)` | Mark combat as complete in state file |

### Platform Support

| Platform | Terminal | Fallback |
|----------|----------|----------|
| Linux | gnome-terminal | xterm |
| macOS | Terminal.app | — |
| Windows | cmd.exe | — |

### State File Management

- **Location:** `.orchestr8/state/fiefdom-status.json`
- **Format:** `{"fiefdoms": {"path/to/fiefdom": {"status": "combat|broken|pending_health_check", "updated_at": "ISO8601"}}}`

---

## 2. Marimo Mapping

### Entry Point: `IP/plugins/06_maestro.py`

**Import (line 77):**
```python
from IP.terminal_spawner import TerminalSpawner
```

**Instantiation (line 221):**
```python
terminal_spawner = TerminalSpawner(project_root_path)
```

The `TerminalSpawner` is instantiated at render time inside the `render(STATE_MANAGERS)` function in `06_maestro.py`. It shares the lifecycle of the marimo cell where it's created.

---

## 3. Wiring

### Call Site 1: Agent Deployment with Terminal Mode (lines 554-559)

**Trigger:** DeployPanel → "terminal" mode deployment  
**Function:** `handle_deploy()` → `terminal_spawner.spawn()`

```python
# 06_maestro.py:554-559
if mode == "terminal":
    briefing_path = project_root_path / file_path
    if briefing_path.is_file():
        briefing_path = briefing_path.parent

    terminal_spawner.spawn(
        fiefdom_path=str(briefing_path),
        briefing_ready=True,
        auto_start_claude=True,  # Immediately runs Claude in terminal
    )
    log_action(f"Terminal spawned for {file_path}")
```

**Flow:** User selects fiefdom → DeployPanel opens → chooses "terminal" mode → clicks DEPLOY → `spawn()` is called with `auto_start_claude=True`

### Call Site 2: Phreak> Button (lines 641-644)

**Trigger:** Phreak> button in control surface  
**Function:** `handle_terminal()` → `terminal_spawner.spawn()`

```python
# 06_maestro.py:623-644
def handle_terminal() -> None:
    """Toggle terminal panel and spawn actu8 if opening."""
    current = get_show_terminal()
    set_show_terminal(not current)

    if not current:  # Opening terminal
        set_phreak_sfx_tick(get_phreak_sfx_tick() + 1)
        selected = get_selected()
        fiefdom_path = selected if selected else "."

        # Check if BRIEFING.md exists
        briefing_path = project_root_path / fiefdom_path
        if briefing_path.is_file():
            briefing_path = briefing_path.parent
        briefing_ready = (briefing_path / "BRIEFING.md").exists()

        # Spawn the terminal
        success = terminal_spawner.spawn(
            fiefdom_path=str(fiefdom_path),
            briefing_ready=briefing_ready,
            auto_start_claude=False,  # Manual start
        )
```

**Flow:** User clicks Phreak> → checks for BRIEFING.md → spawns terminal at selected fiefdom (or project root) → `auto_start_claude=False` (user must type `claude` manually)

### Status Update Wiring

- **On spawn:** Calls `update_fiefdom_status(fiefdom_path, "combat")` → sets status to PURPLE in Code City
- **On failure:** Reverts to `"broken"` status (line 108)
- **On combat complete:** Sets to `"pending_health_check"` (line 121)

---

## 4. Integration into a_codex_plan

### Recommended Module Location

```
a_codex_plan/app/modules/deployment/
├── __init__.py
├── terminal_spawner.py    # Port from IP/terminal_spawner.py
└── types.py               # TypedDict for state contracts
```

### Required Adaptations for a_codex_plan

1. **Path Resolution:** The `project_root` is currently hardcoded to the current working directory. For a_codex_plan, this should accept an injectable `Path` or be configurable via settings service.

2. **State Management:** Currently writes directly to `.orchestr8/state/fiefdom-status.json`. In a_codex_plan, this should integrate with the temporal state system or use the settings service for configuration.

3. **Platform Detection:** The `platform.system()` detection is functional but could be extended to detect desktop environment (KDE, GNOME, XFCE) for better terminal selection.

4. **Startup Message Customization:** The echo message format is hardcoded. Consider making this configurable or reading from a template.

### Integration Points for a_codex_plan

| Component | Source | Target in a_codex_plan |
|-----------|--------|------------------------|
| TerminalSpawner class | `IP/terminal_spawner.py` | `a_codex_plan/app/modules/deployment/terminal_spawner.py` |
| Fiefdom status state | `.orchestr8/state/fiefdom-status.json` | Settings service or state store |
| Spawn trigger | 06_maestro.py buttons | a_codex_plan UI handlers |

### State Contract

For a_codex_plan integration, define a TypedDict:

```python
from typing import TypedDict
from datetime import datetime

class FiefdomStatus(TypedDict):
    status: Literal["working", "broken", "combat", "pending_health_check"]
    updated_at: str  # ISO8601
```

---

## 5. Ambiguities & Concerns

### Ambiguity 1: Terminal Preference Not User-Configurable

**Issue:** Linux terminals are tried in fixed order (gnome-terminal → xterm). No way for users to prefer konsole, tilix, or other terminals.

**Current behavior:**
```python
# IP/terminal_spawner.py:72-87
try:
    subprocess.Popen(["gnome-terminal", ...])
except FileNotFoundError:
    subprocess.Popen(["xterm", ...])
```

**Recommendation:** Read terminal preference from settings or detect available terminals at runtime.

### Ambiguity 2: auto_start_claude Flag Logic

**Issue:** Two call sites use different `auto_start_claude` values:
- Deploy mode: `True` (auto-starts Claude)
- Phreak> button: `False` (manual start)

This inconsistency may confuse users about expected behavior. The VISION REPORT notes this but doesn't specify intended UX.

### Ambiguity 3: Status File Race Conditions

**Issue:** Multiple concurrent spawns could cause race conditions when reading/writing the JSON state file.

**Current code:**
```python
# IP/terminal_spawner.py:21-33
if self.state_file.exists():
    with open(self.state_file) as f:
        state = json.load(f)
# ... modify state ...
with open(self.state_file, "w") as f:
    json.dump(state, f, indent=2)
```

**No file locking** — concurrent writes could corrupt state.

### Ambiguity 4: mark_combat_complete() Called But Status Not Really Updated

**Issue:** Line 121 sets status to `"pending_health_check"` but comments note "Status will be updated by next health check" — this creates an inconsistent intermediate state.

```python
# IP/terminal_spawner.py:119-121
def mark_combat_complete(self, fiefdom_path: str, success: bool) -> None:
    # Status will be updated by next health check
    # This just logs the completion
    self.update_fiefdom_status(fiefdom_path, "pending_health_check")
```

### Ambiguity 5: CombatTracker Integration Missing

**Concern noted in COMBAT_TRACKER_TASK.md:** TerminalSpawner spawns terminals but doesn't call `CombatTracker.deploy()`. This means:
- Terminal is opened
- Fiefdom status is set to "combat" 
- BUT no deployment is tracked in CombatTracker

**Per `one integration at a time/Big Pickle/COMBAT_TRACKER_TASK.md:44`:**
> `terminal_spawner.py` should call `tracker.deploy()` when spawning

---

## 6. Status Summary

| Attribute | Value |
|-----------|-------|
| **Integration Status** | WIRED (per SOT/CURRENT_STATE.md) |
| **Completeness** | FUNCTIONAL but incomplete wiring to CombatTracker |
| **Platform Support** | Complete (Linux/macOS/Windows) |
| **Dependencies** | stdlib only (platform, subprocess, json, pathlib) |
| **Testability** | Medium — requires platform-specific terminal availability |
| **a_codex_plan Ready** | Yes, with minor path/config adaptations |

---

## 7. Action Items for a_codex_plan Integration

1. **Port module** to `a_codex_plan/app/modules/deployment/terminal_spawner.py`
2. **Add TypedDict** for state contracts
3. **Integrate with settings service** for terminal preference
4. **Add CombatTracker.deploy()** call in spawn method
5. **Implement file locking** for concurrent state writes
6. **Clarify auto_start_claude UX** — document expected behavior difference

---

*Analysis complete. TerminalSpawner is a working cross-platform utility with solid foundations, but benefits from tighter CombatTracker integration and user-configurable preferences for a_codex_plan.*

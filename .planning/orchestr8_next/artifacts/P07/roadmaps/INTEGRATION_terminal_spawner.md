# TerminalSpawner Integration Roadmap

**Source:** `IP/terminal_spawner.py`  
**Purpose:** Spawns embedded terminals in the UI (OS-native terminal windows)  
**Status:** Standalone utility class, not yet integrated into Orchestr8 plugin system

---

## GAP Analysis

### 1. Type Contracts

**Current State:**
- No TypedDict definitions exist
- Uses primitive types: `str`, `bool`, `Path`
- State persisted to JSON file: `.orchestr8/state/fiefdom-status.json`

**Required Contracts:**

```python
from typing import TypedDict, Literal
from datetime import datetime

class TerminalConfig(TypedDict):
    project_root: str
    default_shell: Literal["bash", "zsh", "powershell", "cmd"]
    auto_start_claude: bool
    briefing_ready: bool

class TerminalSession(TypedDict):
    fiefdom_path: str
    status: Literal["pending", "combat", "pending_health_check", "working", "broken"]
    updated_at: str
    pid: int | None  # OS process ID
    auto_start_claude: bool
```

**Gap Priority:** MEDIUM - Adding TypedDict improves type safety and enables future state management

---

### 2. State Boundary

**Current State:**
- State stored in external JSON file (`fiefdom-status.json`)
- No in-memory `_component_state` dictionary
- No connection to Orchestr8's STATE_MANAGERS system

**Required Boundary:**
```python
class TerminalSpawner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        # NEW: In-memory state cache
        self._component_state: dict[str, TerminalSession] = {}
        # NEW: Load from persisted state on init
        self._load_state()
    
    def _load_state(self) -> None:
        """Load state from JSON into memory cache"""
        ...
    
    def _persist_state(self) -> None:
        """Write memory state to JSON file"""
        ...
```

**Gap Priority:** HIGH - Without in-memory state, UI cannot react to terminal spawn events

---

### 3. Bridge (PTY/Process Protocols)

**Current State:**
- External process bridge: spawns OS-native terminals
- Supports: gnome-terminal, xterm (Linux), Terminal.app (macOS), cmd.exe (Windows)
- No PTY embedded in UI - opens separate terminal window

**Bridge Protocol:**
```
TerminalSpawner.spawn() 
    → subprocess.Popen([terminal_emulator, ...])
    → Opens OS-native terminal window
    → Returns bool success/failure
```

**Gap Priority:** LOW (by design) - This is an external spawner, not an embedded terminal

**Future Consideration:**
- If embedded terminals needed in UI: consider `xterm.js` + `node-pty` bridge
- Current design intentionally spawns OS-native terminals for Claude CLI integration

---

### 4. Integration Logic

**Entry Points:**

| Method | Purpose | Integration Point |
|--------|---------|-------------------|
| `spawn(fiefdom_path, briefing_ready, auto_start_claude)` | Main entry - spawn terminal + set status to COMBAT | Connect to Code City node click / Quick Actions |
| `update_fiefdom_status(fiefdom_path, status)` | Status management | Called by spawn, mark_combat_complete |
| `mark_combat_complete(fiefdom_path, success)` | Mark combat done | Called by ExecutionQueue on task completion |

**Required Integration:**
1. **Plugin Export:** Add to `IP/plugins/` system (e.g., `IP/plugins/08_terminal_spawner.py`)
2. **STATE_MANAGERS Hook:** Register with global state management
3. **UI Trigger:** Wire to Code City node click or Quick Actions panel
4. **Status Sync:** Update Code City colors when status changes

---

## Implementation Roadmap

### Phase 1: Type Safety (Priority: MEDIUM)
- [ ] Add TypedDict definitions for TerminalConfig, TerminalSession
- [ ] Add Literal types for status values
- [ ] Add pid tracking to TerminalSession

### Phase 2: State Boundary (Priority: HIGH)
- [ ] Add `_component_state` dict to __init__
- [ ] Implement `_load_state()` method
- [ ] Implement `_persist_state()` method
- [ ] Add state synchronization between memory and JSON file

### Phase 3: Integration (Priority: HIGH)
- [ ] Create plugin wrapper: `IP/plugins/08_terminal_spawner.py`
- [ ] Export PLUGIN_NAME, PLUGIN_ORDER, render()
- [ ] Wire spawn() to Code City node click handler
- [ ] Add "Spawn Terminal" button to Quick Actions panel

### Phase 4: Bridge Enhancement (Priority: LOW)
- [ ] Add error handling for missing terminal emulators
- [ ] Add configurable shell preference
- [ ] Add terminal window positioning options

---

## Integration Points

### With Code City (06_maestro.py)
- Spawn terminal when user clicks on fiefdom node
- Update node color based on terminal status (COMBAT = purple)

### With ExecutionQueue (if exists)
- Call `mark_combat_complete()` when agent task finishes
- Sync status back to fiefdom-state.json

### With QuickActions (P07_C4_01)
- Add "Spawn Terminal" action button
- Pass fiefdom_path context to spawner

---

## Files to Modify

1. **Create:** `IP/terminal_spawner_types.py` - TypedDict definitions
2. **Modify:** `IP/terminal_spawner.py` - Add state management
3. **Create:** `IP/plugins/08_terminal_spawner.py` - Plugin wrapper
4. **Modify:** `IP/plugins/06_maestro.py` - Wire to Code City clicks
5. **Modify:** `IP/plugins/04_quick_actions.py` - Add spawn button

---

## Dependencies

- `subprocess` (stdlib) - Already used
- `pathlib` (stdlib) - Already used
- `json` (stdlib) - Already used
- `platform` (stdlib) - Already used
- `typing.TypedDict` - Python 3.8+ stdlib

No external dependencies required.

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Terminal emulator not installed | LOW | Fallback chain: gnome-terminal → xterm → basic bash |
| Platform detection failure | LOW | Explicit Windows/macOS/Linux branches |
| State file corruption | MEDIUM | Add try/except around JSON parse, rebuild from empty |
| Claude CLI not in PATH | LOW | Display message in spawned terminal |

---

## Success Criteria

1. TerminalSpawner can spawn terminals for any fiefdom
2. Status updates reflect in Code City visualization
3. Clicking a fiefdom node spawns terminal at that path
4. State persists across Orchestr8 restarts
5. Works on Linux, macOS, and Windows

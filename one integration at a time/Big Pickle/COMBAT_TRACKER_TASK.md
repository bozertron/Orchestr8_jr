# Combat Tracker Implementation Task

## Priority: MEDIUM
## Status: READY FOR EXECUTION

---

## What Exists
- `IP/mermaid_generator.py` defines `FiefdomStatus.COMBAT` but nothing sets it
- `IP/terminal_spawner.py` spawns terminals for LLM deploys but doesn't track state

## What You're Building
Create `IP/combat_tracker.py` - tracks which files have an LLM General deployed (Purple/COMBAT status)

## Requirements

### 1. State File
Location: `.orchestr8/combat_state.json`
```json
{
  "active_deployments": {
    "IP/plugins/06_maestro.py": {
      "deployed_at": "2025-01-25T10:30:00",
      "terminal_id": "term_abc123",
      "model": "claude-3-sonnet"
    }
  }
}
```

### 2. Core Functions
```python
class CombatTracker:
    def __init__(self, project_root: str)
    def deploy(self, file_path: str, terminal_id: str, model: str = "unknown") -> None
    def withdraw(self, file_path: str) -> None
    def is_in_combat(self, file_path: str) -> bool
    def get_active_deployments(self) -> Dict[str, dict]
    def get_combat_files(self) -> List[str]  # For mermaid_generator
```

### 3. Integration Points
- `mermaid_generator.py` can call `tracker.get_combat_files()` to set Purple status
- `terminal_spawner.py` should call `tracker.deploy()` when spawning
- Auto-expire stale deployments (optional: >24h = auto-withdraw)

### 4. Directory Creation
Create `.orchestr8/` if it doesn't exist (like `.git/`)

## Reference Files
- `IP/mermaid_generator.py` - See `FiefdomStatus.COMBAT` enum
- `IP/terminal_spawner.py` - See spawn pattern

## Deliverable
- `IP/combat_tracker.py` (~100-150 lines)
- Works standalone: `python IP/combat_tracker.py` shows active deployments

## DO NOT
- Modify existing files (just create the new tracker)
- Add external dependencies
- Mock anything - real file I/O only

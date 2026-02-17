# ARCHITECT-CARL.md — Carl Context Aggregator Architecture
## Generated: 2026-02-12
## Status: IMPLEMENTATION PLAN

---

## 1. Current State Analysis

### carl_core.py (Lines 1-99)
- **Purpose:** TypeScript bridge via subprocess to `unified-context-system.ts`
- **Methods:** `run_deep_scan()`, `get_file_context()`
- **Gap:** NO `gather_context()` method — core requirement missing
- **Gap:** NO integration with signal sources

### Signal Sources Ready for Integration

| Source | File | Key Method | Output Type |
|--------|------|------------|-------------|
| HealthChecker | `health_checker.py:66` | `check_fiefdom(path)` | `HealthCheckResult` |
| ConnectionVerifier | `connection_verifier.py:197` | `verify_file(path)` | `FileConnectionResult` |
| CombatTracker | `combat_tracker.py:8` | `get_deployment_info(path)` | `Optional[dict]` |
| TicketManager | `ticket_manager.py:31` | `get_tickets_for_fiefdom(path)` | `List[Ticket]` |
| LouisWarden | `louis_core.py:43` | `get_protection_status()` | `dict` |

---

## 2. Approach Selection

**Chosen:** Lightweight aggregator pattern

- Carl imports signal sources directly
- `gather_context()` calls each source's existing method
- No caching initially (flexible area per CONTEXT.md)
- Returns FiefdomContext JSON matching LOCKED structure

**Rationale:**
- Signal sources already exist with stable interfaces
- Non-blocking: fast method calls, no subprocess
- Minimal changes to existing code

---

## 3. Wave-by-Wave Modification Order

### Wave 1: Data Classes (New)
**File:** `IP/carl_core.py` (append)

```python
@dataclass
class FiefdomContext:
    fiefdom: str
    health: Dict[str, Any]
    connections: Dict[str, Any]
    combat: Dict[str, Any]
    tickets: List[str]
    locks: List[Dict[str, str]]
```

### Wave 2: Import Signal Sources
**File:** `IP/carl_core.py` (top)

```python
from .health_checker import HealthChecker
from .connection_verifier import ConnectionVerifier
from .combat_tracker import CombatTracker
from .ticket_manager import TicketManager
from .louis_core import LouisWarden, LouisConfig
```

### Wave 3: Refactor CarlContextualizer
**File:** `IP/carl_core.py` (class body)

Add constructor params:
```python
def __init__(self, root_path: str, state_managers: Optional[Dict] = None):
    self.root = Path(root_path)
    self.state_managers = state_managers or {}
    
    # Initialize signal sources
    self.health_checker = HealthChecker(root_path)
    self.connection_verifier = ConnectionVerifier(root_path)
    self.combat_tracker = CombatTracker(root_path)
    self.ticket_manager = TicketManager(root_path)
    
    # Louis requires config
    louis_config = LouisConfig(root_path)
    self.louis_warden = LouisWarden(louis_config)
```

### Wave 4: Implement gather_context()
**File:** `IP/carl_core.py` (new method)

```python
def gather_context(self, fiefdom_path: str) -> FiefdomContext:
    """
    Aggregate context from all signal sources for a fiefdom.
    NON-BLOCKING: calls existing methods on signal sources.
    """
    
    # Health
    health_result = self.health_checker.check_fiefdom(fiefdom_path)
    health = {
        "status": health_result.status,
        "errors": [{"file": e.file, "line": e.line, "message": e.message} 
                   for e in health_result.errors],
        "warnings": [{"file": w.file, "line": w.line, "message": w.message} 
                     for w in health_result.warnings]
    }
    
    # Connections
    conn_result = self.connection_verifier.verify_file(fiefdom_path)
    connections = {
        "imports_from": [imp.target_module for imp in conn_result.local_imports],
        "broken": [{"import": imp.target_module, "line": imp.line_number} 
                   for imp in conn_result.broken_imports]
    }
    
    # Combat
    deployment = self.combat_tracker.get_deployment_info(fiefdom_path)
    combat = {
        "active": deployment is not None,
        "model": deployment.get("model", "") if deployment else "",
        "terminal_id": deployment.get("terminal_id", "") if deployment else ""
    }
    
    # Tickets
    ticket_objs = self.ticket_manager.get_tickets_for_fiefdom(fiefdom_path)
    tickets = [f"{t.id}: {t.title}" for t in ticket_objs if t.status != "archived"]
    
    # Locks
    protection = self.louis_warden.get_protection_status()
    locks = []
    for path, status in protection.items():
        if fiefdom_path in path and status.get("locked"):
            locks.append({"file": path, "reason": "Louis protection"})
    
    return FiefdomContext(
        fiefdom=fiefdom_path,
        health=health,
        connections=connections,
        combat=combat,
        tickets=tickets,
        locks=locks
    )
```

### Wave 5: JSON Serialization
**File:** `IP/carl_core.py` (method)

```python
def gather_context_json(self, fiefdom_path: str) -> str:
    """Return context as JSON string for agent briefings."""
    ctx = self.gather_context(fiefdom_path)
    return json.dumps(asdict(ctx), indent=2)
```

### Wave 6: UI Integration Point
**File:** `IP/plugins/06_maestro.py` (Summon panel)

- Import `CarlContextualizer`
- Call `carl.gather_context_json(selected_fiefdom)` on panel open
- Display in Summon panel context section

---

## 4. Integration Points

### HealthChecker → Carl
```
health_checker.py:426 check_fiefdom(fiefdom_path)
  → returns HealthCheckResult
  → Carl extracts: status, errors[], warnings[]
```

### ConnectionVerifier → Carl
```
connection_verifier.py:422 verify_file(file_path)
  → returns FileConnectionResult
  → Carl extracts: local_imports[], broken_imports[]
```

### CombatTracker → Carl
```
combat_tracker.py:77 get_deployment_info(file_path)
  → returns Optional[dict]
  → Carl extracts: active, model, terminal_id
```

### TicketManager → Carl
```
ticket_manager.py:199 get_tickets_for_fiefdom(fiefdom)
  → returns List[Ticket]
  → Carl extracts: id, title (non-archived only)
```

### LouisWarden → Carl
```
louis_core.py:66 get_protection_status()
  → returns dict {path: {locked, protected}}
  → Carl filters: paths matching fiefdom, locked=True
```

---

## 5. Agent Estimates

Using Universal Scaling Formula:
```
agents = ceil(tokens / 2500) × 3
```

| Wave | Tokens | Agents | Role |
|------|--------|--------|------|
| Wave 1 | ~200 | 1×3=3 | Data class definition |
| Wave 2 | ~100 | 1×3=3 | Import statements |
| Wave 3 | ~400 | 1×3=3 | Constructor refactor |
| Wave 4 | ~800 | 1×3=3 | gather_context() implementation |
| Wave 5 | ~150 | 1×3=3 | JSON serialization |
| Wave 6 | ~600 | 1×3=3 | UI integration |

**Total:** ~2250 tokens, 3 work units × 3 agents = **9 agents** (Sentinel Protocol)

### Agent Distribution (if deployed)

| Tier | Count | Assignment |
|------|-------|------------|
| Survey | 1 | Verify signal source interfaces |
| Pattern | 1 | Match existing code conventions |
| Execution | 3 | Implement waves 1-5 |
| Post-mortem | 1 | Verify non-blocking behavior |

---

## 6. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Louis config not initialized | Fallback: skip locks if config missing |
| HealthChecker timeout | Already has timeout handling in source |
| Circular import | Use lazy imports if needed |
| State managers not passed | Graceful degradation to fresh instances |

---

## 7. Verification Checklist

- [ ] `gather_context()` returns FiefdomContext dataclass
- [ ] Output matches LOCKED JSON structure from CONTEXT.md
- [ ] No blocking subprocess calls in gather path
- [ ] Signal sources not modified (read-only integration)
- [ ] Louis remains unchanged (constraint satisfied)

---

**Document Status:** READY FOR IMPLEMENTATION
**Estimated Implementation Time:** 1-2 hours
**Dependencies:** None (signal sources exist)

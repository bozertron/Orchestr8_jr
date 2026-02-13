# ARCH-CARL-CONTEXT.md — Settlement Architect Plan
## Fiefdom: Carl Context Aggregation
## Tier: 7 (Settlement Architect)
## Generated: 2026-02-12
## Status: READY FOR EXECUTION

---

## LOCKED Decisions (from CONTEXT.md)

| Decision | Value |
|----------|-------|
| ROLE | Collect and present data — NOT blocking |
| SIGNAL SOURCES | HealthChecker, ConnectionVerifier, CombatTracker, TicketManager, LouisWarden |
| OUTPUT FORMAT | FiefdomContext JSON |
| PRIORITY | HIGH — implement this round |

---

## Target Output Structure

```json
{
  "fiefdom": "IP/",
  "health": { "status": "broken", "errors": [...] },
  "connections": { "imports_from": [...], "broken": [...] },
  "combat": { "active": true, "model": "claude-3" },
  "tickets": ["TICKET-001"],
  "locks": [{"file": "louis_core.py", "reason": "Core protection"}]
}
```

---

## Signal Source Analysis

### 1. HealthChecker (`IP/health_checker.py`)
**Method:** `check_fiefdom(fiefdom_path: str) -> HealthCheckResult`
**Returns:**
- `status`: "working" | "broken"
- `errors`: List[ParsedError] with file, line, message
- `warnings`: List[ParsedError]

**Integration:**
```python
health_result = health_checker.check_fiefdom(fiefdom_path)
health_signal = {
    "status": health_result.status,
    "errors": [{"file": e.file, "line": e.line, "message": e.message} 
               for e in health_result.errors],
    "warnings": [{"file": w.file, "line": w.line, "message": w.message} 
                 for w in health_result.warnings]
}
```

### 2. ConnectionVerifier (`IP/connection_verifier.py`)
**Method:** `verify_file(file_path: str) -> FileConnectionResult`
**Returns:**
- `broken_imports`: List[ImportResult] with target_module, line_number
- `local_imports`: List[ImportResult] with resolved_path
- `status`: "working" | "broken"

**Integration (for fiefdom directory):**
```python
connection_result = verifier.verify_project(extensions={'.py'})
# Filter to fiefdom files, aggregate broken/local imports
```

### 3. CombatTracker (`IP/combat_tracker.py`)
**Method:** `get_deployment_info(file_path: str) -> Optional[dict]`
**Returns:**
- `deployed_at`: timestamp
- `terminal_id`: str
- `model`: str

**Integration:**
```python
active_deployments = combat_tracker.get_active_deployments()
# Filter to files within fiefdom path
```

### 4. TicketManager (`IP/ticket_manager.py`)
**Method:** `get_tickets_for_fiefdom(fiefdom: str) -> List[Ticket]`
**Returns:**
- List of Ticket objects with id, status, title

**Integration:**
```python
tickets = ticket_manager.get_tickets_for_fiefdom(fiefdom_path)
ticket_ids = [t.id for t in tickets if t.status != "archived"]
```

### 5. LouisWarden (`IP/louis_core.py`)
**Method:** `get_protection_status() -> dict`
**Returns:**
- Dict mapping file paths to {"locked": bool, "protected": bool}

**Integration:**
```python
protection = warden.get_protection_status()
# Filter to files within fiefdom path
locks = [{"file": f, "reason": "Protected"} for f, s in protection.items() 
         if s["locked"] and f.startswith(fiefdom_path)]
```

---

## Implementation Plan

### File: `IP/carl_core.py`

#### Add Method: `gather_context()`

```python
def gather_context(
    self, 
    fiefdom_path: str,
    health_checker: 'HealthChecker',
    connection_verifier: 'ConnectionVerifier',
    combat_tracker: 'CombatTracker',
    ticket_manager: 'TicketManager',
    louis_warden: 'LouisWarden'
) -> Dict[str, Any]:
    """
    Aggregate context from all signal sources for a fiefdom.
    
    NON-BLOCKING: This method only collects and presents data.
    It does NOT modify any state or block operations.
    
    Args:
        fiefdom_path: Relative path to fiefdom (e.g., "IP/")
        
    Returns:
        FiefdomContext JSON structure per CONTEXT.md spec
    """
    context = {
        "fiefdom": fiefdom_path,
        "health": self._gather_health(fiefdom_path, health_checker),
        "connections": self._gather_connections(fiefdom_path, connection_verifier),
        "combat": self._gather_combat(fiefdom_path, combat_tracker),
        "tickets": self._gather_tickets(fiefdom_path, ticket_manager),
        "locks": self._gather_locks(fiefdom_path, louis_warden)
    }
    return context
```

#### Add Private Helper Methods

Each helper follows the same pattern: accept fiefdom_path and source, return partial context.

```python
def _gather_health(self, fiefdom_path: str, checker: HealthChecker) -> Dict:
    """Extract health signal for fiefdom."""
    result = checker.check_fiefdom(fiefdom_path)
    return {
        "status": result.status,
        "errors": [{"file": e.file, "line": e.line, "message": e.message} 
                   for e in result.errors[:10]],  # Cap at 10
        "checker_used": result.checker_used
    }

def _gather_connections(self, fiefdom_path: str, verifier: ConnectionVerifier) -> Dict:
    """Extract connection signal for fiefdom."""
    result = verifier.verify_file(fiefdom_path)
    return {
        "imports_from": [imp.resolved_path for imp in result.local_imports[:20]],
        "broken": [{"target": imp.target_module, "line": imp.line_number} 
                   for imp in result.broken_imports[:10]]
    }

def _gather_combat(self, fiefdom_path: str, tracker: CombatTracker) -> Dict:
    """Extract combat signal for fiefdom."""
    deployments = tracker.get_active_deployments()
    fiefdom_combat = {
        path: info for path, info in deployments.items() 
        if path.startswith(fiefdom_path)
    }
    if not fiefdom_combat:
        return {"active": False}
    # Return first deployment info
    path, info = next(iter(fiefdom_combat.items()))
    return {
        "active": True,
        "file": path,
        "model": info.get("model", "unknown"),
        "terminal": info.get("terminal_id", "unknown")
    }

def _gather_tickets(self, fiefdom_path: str, mgr: TicketManager) -> List[str]:
    """Extract ticket IDs for fiefdom."""
    tickets = mgr.get_tickets_for_fiefdom(fiefdom_path)
    return [t.id for t in tickets if t.status != "archived"][:5]

def _gather_locks(self, fiefdom_path: str, warden: LouisWarden) -> List[Dict]:
    """Extract lock status for fiefdom files."""
    protection = warden.get_protection_status()
    return [
        {"file": path, "reason": "Protected"} 
        for path, status in protection.items()
        if status["locked"] and path.startswith(fiefdom_path)
    ][:10]
```

---

## Border Contracts

| Border | Direction | Contract |
|--------|-----------|----------|
| HealthChecker → Carl | IN | `check_fiefdom(path) -> HealthCheckResult` |
| ConnectionVerifier → Carl | IN | `verify_file(path) -> FileConnectionResult` |
| CombatTracker → Carl | IN | `get_active_deployments() -> Dict[str, dict]` |
| TicketManager → Carl | IN | `get_tickets_for_fiefdom(path) -> List[Ticket]` |
| LouisWarden → Carl | IN | `get_protection_status() -> Dict[str, dict]` |
| Carl → Summon Panel | OUT | `FiefdomContext` JSON |

---

## Constraints (MUST NOT)

1. **NO blocking** — Carl only reads, never writes or blocks
2. **NO Louis overlap** — Carl reports lock status, Louis enforces it
3. **NO state modification** — gather_context is pure read operation

---

## Test Criteria

1. `gather_context("IP/", ...)` returns valid FiefdomContext JSON
2. Health signal reflects current HealthChecker status
3. Connections signal shows broken imports
4. Combat signal shows active deployments in IP/
5. Tickets signal shows open tickets for IP/
6. Locks signal shows locked files in IP/
7. Method completes in < 500ms for typical fiefdom

---

## Execution Order

1. Add `gather_context()` method to CarlContextualizer
2. Add 5 private helper methods (_gather_*)
3. Add type hints for signal source imports
4. Test with IP/ fiefdom
5. Wire to Summon panel (separate task)

---

**Architect:** Settlement System Tier 7
**Approved By:** Pending Founder Review

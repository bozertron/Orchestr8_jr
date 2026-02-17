# Integration Roadmap: ticket_manager.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/ticket_manager.py`  
**Target:** `a_codex_plan`  
**Date:** 2026-02-16  
**Pattern:** DENSE + GAP

---

## 1. Public API Surface

### 1.1 Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `Ticket` | Data class representing a single ticket/issue | Dataclass with id, fiefdom, status, title, description, errors, warnings, context, created_at, updated_at, notes |
| `TicketManager` | Manages ticket lifecycle (CRUD operations) | `create_ticket()`, `update_ticket_status()`, `add_note()`, `get_ticket()`, `list_tickets()`, `archive_ticket()`, `get_tickets_for_fiefdom()` |

### 1.2 Functions/Methods

| Method | Signature | Returns |
|--------|-----------|---------|
| `Ticket.__init__` | `(id: str, fiefdom: str, status: str, title: str, description: str, errors: List[str], warnings: List[str], context: Dict, created_at: str, updated_at: str, notes: List[Dict])` | `Ticket` |
| `Ticket.__post_init__` | `() -> None` | Sets timestamps if not provided |
| `TicketManager.__init__` | `(project_root: str)` | `None` |
| `create_ticket` | `(fiefdom: str, title: str, description: str, errors: List[str], warnings: List[str], context: Optional[Dict]) -> str` | Ticket ID (UUID) |
| `update_ticket_status` | `(ticket_id: str, status: str) -> bool` | Success status |
| `add_note` | `(ticket_id: str, author: str, text: str) -> bool` | Success status |
| `get_ticket` | `(ticket_id: str) -> Optional[Ticket]` | Ticket or None |
| `list_tickets` | `(status_filter: Optional[str]) -> List[Ticket]` | List of tickets |
| `archive_ticket` | `(ticket_id: str) -> bool` | Success status |
| `get_tickets_for_fiefdom` | `(fiefdom: str) -> List[Ticket]` | Tickets for fiefdom |
| `_save_ticket` | `(ticket: Ticket) -> None` | Persists to JSON |
| `_load_ticket` | `(ticket_file: Path) -> Optional[Ticket]` | Loads from JSON |
| `_archive_ticket` | `(ticket: Ticket) -> None` | Moves to archive |

### 1.3 State File Schema

**Active Tickets Location:** `.orchestr8/tickets/{ticket_id}.json`

```json
{
  "id": "a1b2c3d4",
  "fiefdom": "IP/components",
  "status": "open",
  "title": "Broken import in foo.py",
  "description": "The import statement is malformed",
  "errors": ["ImportError: cannot import 'bar' from 'baz'"],
  "warnings": ["Warning: unused import 'qux'"],
  "context": {"related_files": ["foo.py", "bar.py"]},
  "created_at": "2026-02-16T10:30:00.000000",
  "updated_at": "2026-02-16T10:30:00.000000",
  "notes": [
    {"time": "10:35:00", "author": "System", "text": "Ticket created from health check"}
  ]
}
```

**Archive Location:** `.orchestr8/tickets/archive/{ticket_id}.json`

Same schema as active tickets.

---

## 2. Dependencies

### 2.1 Standard Library

```python
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json
import uuid
import shutil
```

### 2.2 IP Module Dependencies

| Module | Imported Symbols | Purpose |
|--------|------------------|---------|
| None | - | No internal IP dependencies |

### 2.3 External Dependencies

| Tool/Module | Purpose |
|-------------|---------|
| `pathlib.Path` | File system path handling |
| `json` | Ticket serialization |
| `uuid` | Ticket ID generation |
| `shutil` | File archiving operations |
| `datetime` | Timestamping |

---

## 3. Integration Points

### 3.1 CarlCore Integration

```python
# IP/carl_core.py lines 18, 58, 170-171
from IP.ticket_manager import TicketManager

self.ticket_manager = TicketManager(str(self.root))
ticket_objs = self.ticket_manager.get_tickets_for_fiefdom(fiefdom_path)
tickets = [f"{t.id}: {t.title}" for t in ticket_objs if t.status != "archived"]
```

**Usage Pattern:** Provides ticket data as part of FiefdomContext aggregation. Tickets are included in context for LLM consumption.

### 3.2 TicketPanel Component

```python
# IP/plugins/components/ticket_panel.py lines 6, 319
from IP.ticket_manager import TicketManager, Ticket

self.ticket_manager = TicketManager(project_root)
```

**Usage Pattern:** Full UI panel for ticket management - create, view, update, filter, search, add notes. Renders slide-out panel from right side.

### 3.3 Director Integration (08_director.py)

```python
# IP/plugins/08_director.py lines 446-460
from IP.ticket_manager import TicketManager

ticket_mgr = TicketManager(".")
ticket_id = ticket_mgr.create_ticket(
    fiefdom=f"general/{general_id}",
    title=f"ESCALATION: {general_id} Stuck",
    description=f"General {general_id} stuck and requires Doctor intervention.",
    errors=[f"General {general_id} stuck: {reason}"],
    warnings=[],
    context={"escalated_from": "director", "priority": "high"},
)
ticket_mgr.add_note(ticket_id, "Director", f"Escalated due to: {reason}")
```

**Usage Pattern:** Creates escalation tickets when agents get stuck. Auto-populates ticket with error context.

---

## 4. GAP Analysis & Roadmap

### GAP 1: Type Contracts

**Current State:** Uses `@dataclass` for Ticket with raw string types. No explicit `TicketStatus` type.

**Required Contracts for a_codex_plan:**

| Contract | Type Definition | Notes |
|----------|-----------------|-------|
| `TicketStatus` | `Literal["open", "in_progress", "resolved", "archived"]` | Enum-like status lifecycle |
| `TicketNote` | `TypedDict("TicketNote", {"time": str, "author": str, "text": str})` | Note structure |
| `TicketContext` | `TypedDict("TicketContext", {...}, total=False)` | Flexible context dict |
| `Ticket` | `TypedDict("Ticket", {"id": str, "fiefdom": str, "status": TicketStatus, "title": str, "description": str, "errors": List[str], "warnings": List[str], "context": TicketContext, "created_at": str, "updated_at": str, "notes": List[TicketNote]})` | Full ticket contract |

**Implementation Priority:** HIGH - Foundation for type-safe integration.

---

### GAP 2: State Boundary

**Current State:** No explicit `_component_state` dict. State is managed through:

- `self.project_root` (Path)
- `self.tickets_dir` (Path)
- `self.archive_dir` (Path)
- File-based JSON persistence via `_save_ticket()` / `_load_ticket()`

**Issues Identified:**

1. State loaded on-demand per operation (no in-memory cache)
2. No centralized state tracking across multiple TicketManager instances
3. No dirty flag for batch save optimization
4. No history or audit trail of ticket operations
5. `_component_state` pattern not implemented

**Required State Boundary:**

```python
class TicketManager:
    def __init__(self, project_root: str):
        # Component state - explicit boundary
        self._component_state: Dict[str, Any] = {
            "_initialized": False,
            "_ticket_cache": {},          # In-memory ticket cache
            "_archive_cache": {},          # In-memory archive cache
            "_operation_history": [],      # Log of all operations
            "_dirty_tickets": set(),       # Track unsaved changes
            "_last_sync_time": None,
        }
        
        # Configuration (immutable after init)
        self._config = {
            "project_root": Path(project_root),
            "tickets_dir": Path(project_root) / ".orchestr8" / "tickets",
            "archive_dir": Path(project_root) / ".orchestr8" / "tickets" / "archive",
        }
```

**State Boundary Requirements:**

| Field | Type | Purpose |
|-------|------|---------|
| `_ticket_cache` | `Dict[str, Ticket]` | In-memory cache of active tickets |
| `_archive_cache` | `Dict[str, Ticket]` | In-memory cache of archived tickets |
| `_operation_history` | `List[TicketOperation]` | Historical log of all operations |
| `_dirty_tickets` | `Set[str]` | Track unsaved ticket changes |
| `_last_sync_time` | `Optional[datetime]` | Cache invalidation timestamp |

**Implementation Priority:** HIGH - Required for efficient state management and batch operations.

---

### GAP 3: Bridge Definitions

**Current Bridge:** JSON file-based persistence at `.orchestr8/tickets/` and `.orchestr8/tickets/archive/`.

**File→In-Memory Protocol:**

| Field | Type | Description |
|-------|------|-------------|
| `{ticket_id}.json` | `Ticket` | Active ticket file |
| `archive/{ticket_id}.json` | `Ticket` | Archived ticket file |

**Python→UI Contract:**

```python
# For ticket list rendering
{
    "tickets": [
        {
            "id": "a1b2c3d4",
            "fiefdom": "IP/components",
            "status": "open",
            "title": "Broken import",
            "description": "...",
            "error_count": 2,
            "warning_count": 1,
            "created_at": "2026-02-16T10:30:00",
            "updated_at": "2026-02-16T10:35:00",
            "note_count": 1
        }
    ],
    "total": 10,
    "by_status": {"open": 5, "in_progress": 2, "resolved": 2, "archived": 1}
}

# For ticket detail rendering
{
    "id": "a1b2c3d4",
    "fiefdom": "IP/components",
    "status": "open",
    "title": "Broken import",
    "description": "Full description text",
    "errors": ["Error 1", "Error 2"],
    "warnings": ["Warning 1"],
    "context": {"related_files": ["foo.py"]},
    "created_at": "2026-02-16T10:30:00",
    "updated_at": "2026-02-16T10:35:00",
    "notes": [
        {"time": "10:35:00", "author": "System", "text": "Note content"}
    ]
}
```

**Implementation Priority:** HIGH - Core integration mechanism for UI rendering.

---

### GAP 4: Integration Logic

**Entry Points for a_codex_plan:**

| Entry Point | Validation Required | Returns |
|-------------|---------------------|---------|
| `TicketManager.__init__` | `project_root` exists as directory | `TicketManager` or raises `ValueError` |
| `create_ticket(fiefdom, title, description, errors, warnings, context)` | Valid fiefdom string, non-empty title | Ticket ID or raises |
| `update_ticket_status(ticket_id, status)` | Valid ticket_id, valid status | Success bool |
| `add_note(ticket_id, author, text)` | Valid ticket_id, non-empty text | Success bool |
| `get_ticket(ticket_id)` | None | `Optional[Ticket]` |
| `list_tickets(status_filter)` | None | `List[Ticket]` |
| `get_tickets_for_fiefdom(fiefdom)` | Valid fiefdom string | `List[Ticket]` |

**Validation Requirements:**

```python
def __init__(self, project_root: str):
    # Validate project_root
    root = Path(project_root)
    if not root.exists():
        raise ValueError(f"project_root does not exist: {project_root}")
    if not root.is_dir():
        raise ValueError(f"project_root is not a directory: {project_root}")
    
    # Initialize state
    self._component_state = {
        "_initialized": True,
        "_ticket_cache": {},
        "_archive_cache": {},
        "_operation_history": [],
        "_dirty_tickets": set(),
        "_last_sync_time": datetime.now(),
    }
```

**Batch Operations (for efficiency):**

```python
def bulk_get_tickets(self, ticket_ids: List[str]) -> Dict[str, Optional[Ticket]]:
    """Get multiple tickets efficiently."""
    return {tid: self.get_ticket(tid) for tid in ticket_ids}

def get_ticket_summary(self) -> Dict[str, Any]:
    """Get aggregated ticket statistics."""
    tickets = self.list_tickets()
    by_status = {}
    for t in tickets:
        by_status[t.status] = by_status.get(t.status, 0) + 1
    return {
        "total": len(tickets),
        "by_status": by_status,
        "total_errors": sum(len(t.errors) for t in tickets),
        "total_warnings": sum(len(t.warnings) for t in tickets),
    }

def get_fiefdom_summary(self) -> Dict[str, Dict[str, int]]:
    """Get ticket counts per fiefdom."""
    tickets = self.list_tickets()
    summary = {}
    for t in tickets:
        if t.fiefdom not in summary:
            summary[t.fiefdom] = {"open": 0, "in_progress": 0, "resolved": 0, "archived": 0}
        summary[t.fiefdom][t.status] += 1
    return summary
```

**Implementation Priority:** HIGH - Required for production reliability and efficient bulk operations.

---

## 5. Integration Checklist

- [ ] Define TypedDict contracts: `TicketStatus`, `TicketNote`, `TicketContext`, `Ticket`
- [ ] Migrate from `@dataclass Ticket` to TypedDict (or keep dataclass with TypedDict aliases)
- [ ] Implement `_component_state` boundary with `_ticket_cache`, `_archive_cache`, `_operation_history`, `_dirty_tickets`
- [ ] Add in-memory caching to avoid repeated file I/O
- [ ] Add operation history tracking for audit trail
- [ ] Implement batch operations: `bulk_get_tickets()`, `get_ticket_summary()`, `get_fiefdom_summary()`
- [ ] Add lazy loading - load state once on first access, not every method call
- [ ] Add `__init__` validation with proper error messages
- [ ] Define Python→UI contracts for ticket list and detail rendering
- [ ] Add type hints to all public methods
- [ ] Create integration test suite for a_codex_plan

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-------------|
| Concurrent writes corrupt JSON | MEDIUM | HIGH | Add file locking or use atomic writes |
| Stale in-memory cache vs file | MEDIUM | HIGH | Implement `_dirty_tickets` flag and explicit save |
| Large ticket count slows load | LOW | MEDIUM | Implement pagination or lazy loading |
| Missing tickets directory on first run | LOW | LOW | Handled by mkdir and default state |
| Invalid fiefdom format | LOW | MEDIUM | Add path validation in create_ticket() |
| Archive directory corruption | LOW | MEDIUM | Add validation before move operations |

---

## 7. Dependencies on Other IP Modules

TicketManager has **no internal IP dependencies** and can be integrated independently.

However, other modules depend on TicketManager:

1. **CarlCore** - Uses `TicketManager.get_tickets_for_fiefdom()` for FiefdomContext
2. **TicketPanel** - Full UI for ticket CRUD operations
3. **Director** - Creates escalation tickets for stuck agents

**Recommendation:** TicketManager can be integrated early due to its simplicity and lack of internal dependencies. It should be available before CarlCore integration completes.

---

## 8. Agent Deployment Trigger Notes

TicketManager is the trigger mechanism for agent deployments in the Settlement System:

- **Trigger Event:** New ticket created with status "open"
- **Signal:** Ticket contains `errors` list with actionable issues
- **Flow:**
  1. HealthChecker detects issues → creates Ticket
  2. TicketManager persists ticket → sets status "open"
  3. Director/Carl monitors open tickets → triggers agent deployment
  4. Agent deployed → CombatTracker marks file as COMBAT/Purple
  5. Agent completes → ticket updated to "resolved" or new issues create new tickets

**Required Contract for Agent Triggers:**

```python
# Ticket trigger event
{
    "event": "ticket_created",
    "ticket": {
        "id": "a1b2c3d4",
        "fiefdom": "IP/components",
        "status": "open",
        "title": "Broken import in foo.py",
        "errors": ["ImportError: cannot import 'bar'"],
        "context": {"file_path": "IP/components/foo.py"}
    },
    "requires_agent": true,
    "agent_type": "repair_general"
}
```

---

## 9. Testing Strategy

### Unit Tests

- Test all TypedDict contracts
- Test state boundary initialization
- Test validation in `__init__`
- Test ticket lifecycle (create → update → archive)
- Test note addition

### Integration Tests

- Test JSON persistence round-trip
- Test concurrent access scenarios
- Test archive operations
- Test CarlCore FiefdomContext integration

### Performance Tests

- Test bulk ticket retrieval
- Test large ticket counts (100+ tickets)
- Test fiefdom filtering performance
- Test operation history size impact on load time

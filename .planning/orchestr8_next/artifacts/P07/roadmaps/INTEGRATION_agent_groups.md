# Integration Roadmap: AgentGroups

**Feature:** Agent Group Presets for Collabor8 Deployment Controls  
**Source:** `IP/features/maestro/agent_groups.py`  
**Target:** Orchestr8 Core Integration  
**Status:** Planning  
**Created:** 2026-02-16

---

## 1. Feature Overview

AgentGroups defines the settlement agent tiers used in the Orchestr8 collaboration system. It provides preset configurations for different phases of the settlement workflow, from initial survey through strategic oversight. The module organizes agents into five functional groups: Explore, Plan, Execute, Monitor, and Strategic.

### Current Implementation Summary

The current implementation is a thin data layer with minimal integration hooks. It exports a single public function and relies on plain dictionary structures for agent definitions.

### Agent Tier Reference

| Tier | Role | Count |
|------|------|-------|
| 0 | Strategic Oversight (Luminary, City Manager, Civic Council) | 3 |
| 1 | Survey (Surveyor, Complexity Analyzer) | 2 |
| 2 | Pattern Analysis (Pattern Identifier, Import/Export Mapper) | 2 |
| 3 | Cartography (Cartographer, Border Agent) | 2 |
| 5 | Vision (Vision Walker) | 1 |
| 6 | Context (Context Analyst) | 1 |
| 7 | Architecture (Architect) | 1 |
| 8 | Work Orders (Work Order Compiler, Integration Synthesizer, Instruction Writer, Wiring Mapper) | 4 |
| 9 | Sentinel (Sentinel) | 1 |
| 10 | Post-mortem (Failure Pattern Logger) | 1 |

**Total Agents:** 18

---

## 2. GAP PATTERN Analysis

### 2.1 Type Contracts (TypedDict for Agent, AgentTier)

**Current State:**

The module uses plain Python dictionaries with implicit structure. Agent definitions follow this pattern:

```python
{
    "id": "surveyor",
    "name": "Surveyor",
    "tier": 1,
    "brief": "Comprehensive room/tokens/signature survey.",
}
```

**Gaps Identified:**

1. **Missing TypedDict definitions** - No explicit type contracts for `Agent` or `AgentTier`
2. **No validation layer** - Agent definitions are not validated at definition time
3. **Tier semantics unclear** - Integer tiers lack semantic meaning without an enum
4. **Group name typing** - Group names (Explore, Plan, etc.) are string literals with no type safety

**Required Type Contracts:**

```python
from typing import TypedDict, Literal

class AgentTier(TypedDict):
    """Semantic tier levels for settlement agents."""
    SURVEY: int          # Tier 1
    PATTERN: int         # Tier 2
    CARTOGRAPHY: int     # Tier 3
    VISION: int          # Tier 5
    CONTEXT: int         # Tier 6
    ARCHITECTURE: int    # Tier 7
    WORK_ORDERS: int     # Tier 8
    SENTINEL: int        # Tier 9
    POSTMORTEM: int      # Tier 10
    STRATEGIC: int       # Tier 0

class Agent(TypedDict):
    """Type contract for a settlement agent definition."""
    id: str
    name: str
    tier: int
    brief: str

class AgentGroup(TypedDict):
    """Type contract for an agent group collection."""
    agents: List[Agent]
```

**Integration Impact:** Adding TypedDict definitions will require updates to all consumer modules that import or process agent data. This is a breaking change that should be coordinated with dependent features.

### 2.2 State Boundary (_component_state dict)

**Current State:**

The module uses a module-level constant:

```python
_SETTLEMENT_AGENT_GROUPS: Dict[str, List[dict]] = { ... }
```

There is no component state management. The data is static and initialized at module load time.

**Gaps Identified:**

1. **No runtime state** - Agents cannot be dynamically added, removed, or modified
2. **No dirty tracking** - Changes to agent configurations are not tracked
3. **No persistence layer** - Agent state is not serializable to disk
4. **No observer pattern** - Dependent components cannot react to agent changes

**Required State Structure:**

```python
from typing import TypedDict, Optional
from datetime import datetime

class AgentGroupsState(TypedDict):
    """State boundary for AgentGroups component."""
    groups: Dict[str, List[Agent]]
    active_group: Optional[str]
    selected_agents: List[str]
    last_modified: datetime
    version: int
    is_dirty: bool

_component_state: AgentGroupsState = {
    "groups": {},
    "active_group": None,
    "selected_agents": [],
    "last_modified": datetime.now(),
    "version": 1,
    "is_dirty": False,
}
```

**Integration Impact:** Introducing state management will require integration with the broader Orchestr8 state management system. Consider alignment with existing patterns in other IP features.

### 2.3 Bridge (if any)

**Current State:**

No bridge pattern exists. The module operates as a pure data provider with a single export function.

**Gaps Identified:**

1. **No bridge interface** - Other components cannot subscribe to agent changes
2. **No event emission** - Agent selection, group switching, and other events are not broadcast
3. **No async support** - All operations are synchronous
4. **No remote sync** - Agent state cannot be synchronized across sessions

**Required Bridge Interface:**

```python
from typing import Protocol, Callable, List, Any
from dataclasses import dataclass

@dataclass
class AgentEvent:
    """Event emitted by the AgentGroups bridge."""
    event_type: str  # "group_selected", "agent_activated", "state_changed"
    payload: Any
    timestamp: datetime

class AgentGroupsBridge(Protocol):
    """Bridge interface for AgentGroups integration."""
    
    def subscribe(self, callback: Callable[[AgentEvent], None]) -> str:
        """Subscribe to agent events. Returns subscription ID."""
        ...
    
    def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from agent events."""
        ...
    
    def emit(self, event: AgentEvent) -> None:
        """Emit an agent event to all subscribers."""
        ...
    
    def get_state(self) -> AgentGroupsState:
        """Get current component state."""
        ...
    
    def update_state(self, partial_state: Partial[AgentGroupsState]) -> None:
        """Update component state with dirty tracking."""
        ...
```

**Integration Impact:** The bridge will enable reactive integrations with the Orchestr8 UI and other features. Plan for event-driven architecture compatibility.

### 2.4 Integration Logic (entry points)

**Current State:**

The module exposes one public function:

```python
def get_settlement_agent_groups() -> Dict[str, List[dict]]:
    """Return a defensive copy of the canonical agent group map."""
    return deepcopy(_SETTLEMENT_AGENT_GROUPS)
```

**Gaps Identified:**

1. **Limited entry points** - Only one getter function exists
2. **No mutation入口** - No way to modify agent state through the public API
3. **No filtering** - Cannot query agents by tier, group, or criteria
4. **No batch operations** - Bulk operations on agents are unsupported

**Required Entry Points:**

```python
# Read operations
def get_settlement_agent_groups() -> Dict[str, List[Agent]]: ...
def get_agents_by_tier(tier: int) -> List[Agent]: ...
def get_agents_by_group(group_name: str) -> List[Agent]: ...
def get_agent_by_id(agent_id: str) -> Optional[Agent]: ...
def get_all_tiers() -> List[int]: ...
def search_agents(query: str) -> List[Agent]: ...

# Write operations
def set_active_group(group_name: str) -> None: ...
def select_agents(agent_ids: List[str]) -> None: ...
def clear_selection() -> None: ...
def add_agent(group_name: str, agent: Agent) -> bool: ...
def remove_agent(agent_id: str) -> bool: ...
def update_agent(agent_id: str, updates: Partial[Agent]) -> bool: ...

# State management
def reset_state() -> None: ...
def serialize_state() -> str: ...
def deserialize_state(state_json: str) -> bool: ...

# Bridge integration
def get_bridge() -> AgentGroupsBridge: ...
```

**Integration Impact:** Additional entry points will expand integration surface area. Each new function represents a potential integration hook for other Orchestr8 components.

---

## 3. Integration Recommendations

### Priority 1: Type Safety (Immediate)

The highest-priority integration item is adding TypedDict contracts. This provides compile-time safety and documentation value without introducing significant architectural changes.

**Action Items:**
- Define `Agent`, `AgentGroup`, and `AgentTier` TypedDicts
- Add runtime validation using Pydantic or custom validators
- Update `get_settlement_agent_groups()` return type annotations
- Create type stubs for IDE support

**Dependencies:** None (self-contained change)

### Priority 2: State Management (Short-term)

Introduce component state with dirty tracking and persistence capabilities. This enables runtime agent configuration and session save/restore.

**Action Items:**
- Implement `_component_state` dictionary with typed structure
- Add dirty flag tracking and version incrementing
- Create serialization/deserialization functions
- Integrate with Orchestr8 state persistence layer

**Dependencies:** Priority 1 (TypedDict definitions required)

### Priority 3: Bridge Pattern (Medium-term)

Implement event-driven bridge for reactive integrations. This enables UI components and other features to respond to agent state changes.

**Action Items:**
- Define `AgentEvent` dataclass
- Implement `AgentGroupsBridge` protocol
- Add subscribe/unsubscribe/emit methods
- Emit events on state changes
- Document event types and payloads

**Dependencies:** Priority 2 (state management required)

### Priority 4: Extended Entry Points (Medium-term)

Expand the public API with filtering, querying, and mutation operations. This provides comprehensive access to agent group functionality.

**Action Items:**
- Implement tier-based and group-based queries
- Add search functionality by name or brief
- Create mutation methods (add, remove, update agents)
- Add batch operation support
- Implement state reset and serialization

**Dependencies:** Priority 2 (state management required)

---

## 4. Implementation Phases

### Phase 1: Foundation (Type Contracts)

**Duration:** 1 day  
**Scope:** Add TypedDict definitions and validation

**Deliverables:**
- `IP/features/maestro/agent_groups/types.py` (or inline)
- Validated agent definitions at module load
- Updated type annotations on existing functions
- Unit tests for validation logic

**Breaking Changes:** None (additive type annotations)

### Phase 2: State Boundary

**Duration:** 1-2 days  
**Scope:** Component state management

**Deliverables:**
- `_component_state` dictionary with full structure
- Dirty tracking in all mutation functions
- Serialization functions (JSON)
- State reset capability
- Integration with Orchestr8 state persistence (if available)

**Breaking Changes:** None (new functions, existing API unchanged)

### Phase 3: Bridge Implementation

**Duration:** 2 days  
**Scope:** Event-driven integration layer

**Deliverables:**
- `AgentGroupsBridge` implementation
- Event subscription management
- Event emission on state changes
- Documentation of event types
- Example integration (e.g., with Orchestr8 UI)

**Breaking Changes:** None (new functionality)

### Phase 4: API Expansion

**Duration:** 2-3 days  
**Scope:** Extended entry points

**Deliverables:**
- Tier-based and group-based query functions
- Agent search functionality
- Full CRUD operations for agents
- Batch operation support
- Comprehensive API documentation

**Breaking Changes:** None (additive functions)

---

## 5. Testing Strategy

### Unit Tests

- Type validation for Agent definitions
- State transition correctness
- Dirty flag tracking
- Serialization/deserialization roundtrips

### Integration Tests

- Bridge event emission and subscription
- Cross-feature integration with Orchestr8 state
- Concurrent access patterns

### Regression Tests

- Existing `get_settlement_agent_groups()` behavior preserved
- No breaking changes to dependent modules
- Performance benchmarks for state operations

---

## 6. Dependencies and Risks

### Dependencies

- **Orchestr8 State Management:** State boundary implementation should align with existing patterns in the codebase
- **Event System:** Bridge implementation may leverage existing event infrastructure if available
- **Type Checking:** Mypy or pyright integration for ongoing type safety

### Risks

1. **Scope Creep:** The feature is currently simple; adding full state management and bridge patterns may introduce unnecessary complexity if the use cases do not require it
2. **Breaking Changes:** Adding TypedDict definitions may cause type errors in dependent modules until they are updated
3. **Over-engineering:** The current static data approach may be sufficient for the intended use case; evaluate before implementing full state management

### Mitigation

- Implement incrementally, validating each phase before proceeding
- Maintain backward compatibility in all phases
- Document all public APIs thoroughly
- Gather requirements from dependent features before Phase 3 and beyond

---

## 7. Conclusion

AgentGroups is currently a minimal data layer providing static agent definitions. The integration roadmap identifies four priority areas for enhancement: type safety, state management, event-driven bridging, and expanded API surface. The recommended approach is incremental implementation, starting with type contracts and expanding to state and bridge patterns only as use cases demand.

The current implementation is functional for basic use cases. The proposed enhancements position AgentGroups for deeper integration with the Orchestr8 reactive system and UI layer.

---

*Generated: 2026-02-16*  
*Source: `IP/features/maestro/agent_groups.py`*  
*Target: Orchestr8 Core*

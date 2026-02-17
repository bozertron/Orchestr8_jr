# Integration Roadmap: connection_actions.py → a_codex_plan

**Source:** `/home/bozertron/Orchestr8_jr/IP/features/maestro/connection_actions.py`  
**Target:** `/home/bozertron/a_codex_plan`  
**Pattern:** DENSE + GAP  
**Date:** 2026-02-16

---

## 1. Feature Overview

ConnectionActions is the bridge layer that handles edge-level connection panel actions from the Code City visualization. It provides a safe, guardrailed workflow for rewiring import statements in source files without breaking the project graph. The feature supports two operations: dry-run validation and actual apply with rollback capability.

The primary use case is enabling developers to click on an import edge in Code City, specify a new target module, and either preview what would change (dry-run) or apply the rewire (apply). This creates a visual, interactive way to refactor import dependencies across the entire codebase.

---

## 2. Public API Surface

### 2.1 Main Entry Point

| Symbol | Type | Description |
|--------|------|-------------|
| `handle_connection_action` | `function` | Primary handler for connection panel actions; orchestrates validation, dry-run, and apply workflows |

**Function Signature:**

```python
def handle_connection_action(
    payload: dict,
    *,
    project_root_path: str | Path,
    validate_connection_action_event: Callable[[dict], Any],
    dry_run_patchbay_rewire: Callable[..., dict],
    apply_patchbay_rewire: Callable[..., dict],
    set_connection_action_result_payload: Callable[[str], None],
    log_action: Callable[[str], None],
) -> None
```

The function does not return a value; instead, it emits results back to the UI via the `set_connection_action_result_payload` callback. This design allows the function to be called from marimo's reactive system without blocking.

---

## 3. Type Contracts

### 3.1 ConnectionActionEvent (External Contract)

**Source:** `IP/contracts/connection_action_event.py`

| Field | Type | Description |
|-------|------|-------------|
| `action` | `ConnectionAction` | The operation to perform: `"dry_run_rewire"` or `"apply_rewire"` |
| `connection` | `ConnectionEdge` | The source-target edge being modified |
| `proposedTarget` | `Optional[str]` | The new target module path to rewire to |
| `actorRole` | `Optional[str]` | Role of the user performing the action (e.g., "operator", "founder") |
| `signalNodes` | `List[str]` | Additional context nodes for the action |
| `signalEdges` | `List[str]` | Additional context edges for the action |

### 3.2 ConnectionEdge (External Contract)

| Field | Type | Description |
|-------|------|-------------|
| `source` | `str` | Source file path (relative to project root) |
| `target` | `str` | Current target file path (relative to project root) |
| `resolved` | `bool` | Whether the import currently resolves to a valid file |
| `lineNumber` | `int` | Line number of the import statement in source file |
| `edgeType` | `str` | Type of edge (typically "import") |

### 3.3 PatchbayDryRunResult (External Contract)

**Source:** `IP/connection_verifier.py`

| Field | Type | Description |
|-------|------|-------------|
| `action` | `str` | The action that was validated |
| `source_file` | `str` | Normalized source file path |
| `current_target` | `str` | Normalized current target path |
| `proposed_target` | `str` | Normalized proposed target path |
| `import_type` | `str` | Type of source file (PYTHON, JAVASCRIPT, TYPESCRIPT) |
| `can_apply` | `bool` | Whether the rewire can be applied |
| `checks` | `Dict[str, bool]` | Validation check results |
| `issues` | `List[str]` | Validation failures |
| `warnings` | `List[str]` | Non-blocking warnings |
| `source_line` | `int` | Line number of import in source |
| `current_import_statement` | `str` | Original import statement |
| `proposed_import_statement` | `str` | Preview of new import statement |

### 3.4 Action Result Payload (Response Contract)

The handler emits result payloads back to the UI with this structure:

| Field | Type | Description |
|-------|------|-------------|
| `action` | `str` | The action that was processed |
| `ok` | `bool` | Whether the action succeeded |
| `source` | `str` | Source file path |
| `target` | `str` | Current target path |
| `proposedTarget` | `str` | Proposed target path |
| `actorRole` | `Optional[str]` | Role that performed the action |
| `allowedRoles` | `Optional[List[str]]` | Roles permitted for apply (when denied) |
| `lineNumber` | `Optional[int]` | Line number of import |
| `message` | `str` | Human-readable status message |
| `issues` | `List[str]` | List of failures |
| `warnings` | `List[str]` | List of warnings |
| `result` | `Optional[Dict]` | Full result from patchbay functions |
| `rolledBack` | `Optional[bool]` | Whether rollback occurred (apply only) |
| `timestamp` | `str` | ISO timestamp when result was generated |

---

## 4. State Boundary

### 4.1 Marimo State Management

The ConnectionActions feature uses marimo's state system to bridge JavaScript and Python execution contexts. All state is maintained at the plugin level in `06_maestro.py`.

| State Variable | Type | Purpose |
|----------------|------|----------|
| `connection_action_payload` | `mo.state("")` | Holds incoming action payloads from JavaScript bridge |
| `connection_action_result_payload` | `mo.state("")` | Holds outgoing result payloads to be sent back to JavaScript |

**Initialization in 06_maestro.py:**

```python
get_connection_action_payload, set_connection_action_payload = mo.state("")
get_connection_action_result_payload, set_connection_action_result_payload = mo.state("")
```

### 4.2 State Flow

The state flows in one direction for input (JavaScript → Python) and a separate state variable for output (Python → JavaScript). The input state is writable via the hidden text bridge element, while the output state is read-only from the JavaScript perspective and is polled for changes.

---

## 5. Bridge Architecture

### 5.1 JavaScript-to-Python Bridge

**Location:** `IP/plugins/06_maestro.py` (embedded JavaScript)

The JavaScript bridge listens for postMessage events from the Code City iframe and writes payloads to a hidden marimo input element.

**Inbound Message Types:**

| Message Type | Payload | Handler |
|--------------|---------|---------|
| `WOVEN_MAPS_CONNECTION_ACTION` | `ConnectionActionEvent` | `on_connection_action_bridge_change` |

**Bridge Element:**

```python
connection_action_bridge = mo.ui.text(
    value=get_connection_action_payload(),
    on_change=on_connection_action_bridge_change,
)
```

### 5.2 Python-to-JavaScript Bridge

**Outbound Flow:**

1. `handle_connection_action()` processes the payload
2. Result is written to `connection_action_result_payload` state via `set_connection_action_result_payload()`
3. JavaScript polls this state every 300ms via `relayConnectionResult()`
4. Result is broadcast to all iframes via `broadcastToCodeCityIframes()`

**Result Message Type:**

| Message Type | Payload |
|--------------|---------|
| `WOVEN_MAPS_CONNECTION_RESULT` | Action result payload |

**Bridge Element:**

```python
connection_action_result_bridge = mo.ui.text(
    value=get_connection_action_result_payload()
)
```

---

## 6. Integration Logic

### 6.1 Entry Points

| Entry Point | Location | Description |
|-------------|----------|-------------|
| `handle_connection_action` | `IP/features/maestro/connection_actions.py:12` | Primary handler, called from plugin |
| `process_connection_action` | `IP/plugins/06_maestro.py:387` | Wrapper in plugin that injects dependencies |
| `on_connection_action_bridge_change` | `IP/plugins/06_maestro.py:1027` | JavaScript bridge callback |

### 6.2 Processing Pipeline

The handler follows a strict validation pipeline:

1. **Payload Validation:** Parse and validate incoming JSON payload using `validate_connection_action_event()`. Return error result if invalid.

2. **Action Validation:** Ensure action is one of `{"dry_run_rewire", "apply_rewire"}`. Return error result if unknown.

3. **Target Validation:** Require `proposedTarget` to be non-empty. Return error result if missing.

4. **Dry-Run Execution (both actions):** Always execute dry-run first to validate compatibility:
   - Verify source file exists
   - Verify proposed target file exists
   - Verify source currently imports current target
   - Verify source does not already import proposed target
   - Verify file type compatibility (Python→Python, JS→JS/TS, TS→TS)
   - Generate import statement preview

5. **Apply Execution (apply_rewire only):**
   - Check `ORCHESTR8_PATCHBAY_APPLY` environment variable is enabled
   - Verify actor role is in `ORCHESTR8_PATCHBAY_ALLOWED_ROLES`
   - Execute rewrite on source file
   - Re-verify imports after write
   - Auto-rollback if post-write verification fails

### 6.3 Dependency Injection

The handler receives dependencies as callable parameters rather than importing directly. This enables testability and loose coupling.

| Dependency | Injected From | Type |
|------------|---------------|------|
| `validate_connection_action_event` | `IP/contracts/connection_action_event.py` | Contract validator |
| `dry_run_patchbay_rewire` | `IP/connection_verifier.py` | Feature rewire logic |
| `apply_patchbay_rewire` | `IP/connection_verifier.py` | Feature apply logic |
| `set_connection_action_result_payload` | `06_maestro.py` state | Result callback |
| `log_action` | `06_maestro.py` | Logging callback |

---

## 7. Environment Configuration

### 7.1 Feature Flags

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ORCHESTR8_PATCHBAY_APPLY` | `str` | (disabled) | Enable apply functionality; set to "1", "true", "yes", or "on" |
| `ORCHESTR8_PATCHBAY_ALLOWED_ROLES` | `str` | "founder,operator" | Comma-separated list of roles permitted to apply rewires |
| `ORCHESTR8_ACTOR_ROLE` | `str` | "operator" | Default role when not specified in payload |

### 7.2 Security Model

The apply operation is protected by two gates. First, a feature flag must be explicitly enabled via environment variable, preventing accidental writes. Second, the actor role must be in an allowlist, ensuring only authorized users can modify source files. The dry-run operation has no restrictions and can be performed by any user.

---

## 8. Data Flow Diagram

```
Code City (iframe)
       │
       │ postMessage: WOVEN_MAPS_CONNECTION_ACTION
       ▼
JavaScript Bridge (06_maestro.py)
       │
       │ write to connection_action_bridge input
       ▼
marimo State: connection_action_payload
       │
       │ on_change callback
       ▼
process_connection_action() → handle_connection_action()
       │
       ├─→ validate_connection_action_event()
       │         │
       │         └─→ ConnectionActionEvent
       │
       ├─→ dry_run_patchbay_rewire()
       │         │
       │         └─→ PatchbayDryRunResult
       │
       └─→ (conditional) apply_patchbay_rewire()
                 │
                 └─→ ApplyResult
       
       │
       │ set_connection_action_result_payload(json)
       ▼
marimo State: connection_action_result_payload
       │
       │ polling (300ms interval)
       ▼
JavaScript Relay (relayConnectionResult)
       │
       │ postMessage: WOVEN_MAPS_CONNECTION_RESULT
       ▼
Code City (iframe) → updates edge visualization
```

---

## 9. Dependencies

### 9.1 Internal Dependencies

| Module | Purpose |
|--------|---------|
| `IP/contracts/connection_action_event.py` | Type contracts and validation |
| `IP/connection_verifier.py` | Wrapper entry points for patchbay |
| `IP/features/connections/patchbay.py` | Core rewire logic (called via wrapper) |
| `IP/plugins/06_maestro.py` | Plugin integration, state, bridge |

### 9.2 External Dependencies

| Dependency | Purpose |
|------------|---------|
| `marimo` | Reactive framework and state management |
| `json` | Payload serialization |
| `os` | Environment variable access |
| `datetime` | Timestamp generation |

---

## 10. Testing Considerations

### 10.1 Contract Testing

The type contracts are tested in `IP/contracts/tests/test_connection_action_event.py`. Key test cases include valid payloads, missing required fields, invalid action types, and malformed connection objects.

### 10.2 Patchbay Integration Testing

Rewire operations are tested in `IP/contracts/tests/test_connection_verifier_patchbay.py`. Tests cover successful dry-runs, blocked rewires due to validation failures, apply operations with rollback, and cross-language rewire scenarios.

### 10.3 Bridge Testing

The JavaScript bridge can be tested by simulating postMessage events from the Code City iframe and verifying state transitions in marimo.

---

## 11. Error Handling Strategy

### 11.1 Validation Errors

When payload validation fails, the handler returns an error result with `ok: False` and populated `issues` array. The error is logged and sent back to the UI for display.

### 11.2 Runtime Errors

Unexpected exceptions are caught and converted to error results. The original exception message is included in the `issues` array to aid debugging.

### 11.3 Rollback Handling

When apply operations fail after file modification, the system automatically rolls back changes if `auto_rollback=True`. The result includes `rolledBack: True` to indicate this occurred.

---

## 12. Security Considerations

### 12.1 Write Protection

The apply operation is disabled by default and requires explicit opt-in via environment variable. This prevents automated systems or accidentally triggered actions from modifying source code.

### 12.2 Role-Based Access

Only roles explicitly listed in `ORCHESTR8_PATCHBAY_ALLOWED_ROLES` can perform apply operations. The default allowlist includes only "founder" and "operator", minimizing risk.

### 12.3 Path Validation

All file paths are normalized and validated against the project root. The system prevents directory traversal attacks by ensuring all paths remain within the project boundary.

---

## 13. Gap Analysis

### 13.1 Current Strengths

The ConnectionActions feature provides a clean separation between contract validation, business logic, and UI bridging. The dry-run before apply pattern ensures no unexpected changes occur. The environment-based feature flag allows safe production deployment with apply disabled. Role-based access control provides authorization without external dependencies.

### 13.2 Identified Gaps

The feature currently lacks audit logging to persistent storage; logs only go to the in-memory session log. There is no batch rewire capability for handling multiple similar changes. The polling-based result bridge (300ms interval) introduces latency compared to event-driven approaches. The role allowlist is static after startup; there is no runtime reconfiguration.

### 13.3 Future Opportunities

Consider adding a persistent audit log for rewire operations. Explore event-driven result delivery instead of polling for lower latency. Add batch rewire support for refactoring patterns across multiple files. Consider runtime allowlist updates via configuration reload.

---

## 14. Integration Checklist

- [x] Type contracts defined in `IP/contracts/connection_action_event.py`
- [x] Contract validator exported via `IP/contracts/__init__.py`
- [x] Patchbay logic implemented in `IP/features/connections/patchbay.py`
- [x] Wrapper functions exported via `IP/connection_verifier.py`
- [x] Handler function in `IP/features/maestro/connection_actions.py`
- [x] State management in `06_maestro.py`
- [x] JavaScript bridge implemented
- [x] Result relay implemented
- [x] Environment configuration documented
- [x] Unit tests for contracts
- [x] Integration tests for patchbay

---

*End of Integration Roadmap*

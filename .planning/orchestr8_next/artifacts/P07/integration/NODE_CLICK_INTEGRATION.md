# Node Click Integration Research

**Research Date:** 2026-02-16  
**Focus:** Node click → context payload pipeline

---

## 1. Exact Structure of the Context Payload

### 1.1 Full Payload Structure (from `code_city_context.py`)

```python
{
    "path": str,                      # Relative file path (e.g., "IP/woven_maps.py")
    "status": str,                    # "working" | "broken" | "combat"
    "context_scope": str,             # Derived scope key (e.g., "IP/", "IP/plugins/")
    "building_panel": {               # Full building inspection data
        "path": str,
        "status": str,
        "loc": int,                   # Lines of code
        "export_count": int,
        "building_height": float,
        "footprint": float,
        "imports": List[str],         # Module paths imported by this file
        "exports": List[str],         # Functions/classes exported
        "rooms": [                    # Functions/classes within file
            {
                "name": str,          # Function/class name
                "line_start": int,
                "line_end": int,
                "room_type": str,     # "function" | "class" | "method"
                "status": str,        # "working" | "broken" | "combat"
                "errors": List[str]   # Error messages for this room
            }
        ],
        "connections_in": List[str], # Files that import THIS file
        "connections_out": List[str], # Files THIS file imports
        "lock_state": str | None,     # Reason for lock (Louis protection)
        "locked": bool,
        "centrality": float,          # Graph centrality score
        "in_cycle": bool,             # Part of import cycle
        "health_errors": List[str]   # Merged health errors
    },
    "room_entry": {                  # Selected room for broken/combat workflows
        "trigger": str,               # "broken_room_click" | "combat_room_focus" | "broken_file_fallback"
        "name": str,
        "room_type": str,
        "line_start": int,
        "line_end": int,
        "status": str,
        "errors": List[str]
    } | None,
    "sitting_room": {                # Sitting room handoff config
        "mode": "sitting_room",
        "entry_trigger": str,
        "file_path": str,
        "room": room_entry,
        "return_mode": "city"
    } | None
}
```

### 1.2 Ticket Payload (for broken nodes only)

Generated in `06_maestro.py:handle_node_click()` for broken status:

```python
{
    "path": str,
    "status": "broken",
    "errors": List[str],              # Merged errors from node + Carl context
    "suggested_action": str,
    "context": {
        "health_status": str,        # From Carl context.health.status
        "broken_imports": List[dict],
        "tickets": List[str],
        "locks": List[dict],
        "combat_active": bool
    },
    "building_panel": dict,
    "room_entry": dict | None
}
```

### 1.3 JavaScript Input (from `woven_maps_template.html`)

```javascript
{
    type: 'WOVEN_MAPS_NODE_CLICK',
    node: {
        path: string,
        status: "working" | "broken" | "combat",
        loc: number,
        errors: string[],
        nodeType: string,
        centrality: number,
        inCycle: boolean,
        incomingCount: number,
        outgoingCount: number,
        exportCount: number,
        buildingHeight: number,
        footprint: number
    }
}
```

---

## 2. What Triggers Which Panel

### 2.1 Panel Selection Logic

| Status | Panel Shown | Trigger Code Location | Description |
|--------|-------------|----------------------|--------------|
| **broken** | `DeployPanel` | `06_maestro.py:448-509` | Blue node → deploy panel with LLM selection |
| **combat** | Status message | `06_maestro.py:511-518` | Purple node → show agent active message |
| **working** | Building info | `06_maestro.py:520-522` | Gold node → read-only inspection |

### 2.2 Broken Node Flow

```
User clicks blue building
         ↓
JavaScript posts WOVEN_MAPS_NODE_CLICK
         ↓
on_node_click_bridge_change() receives JSON
         ↓
process_node_click() validates via validate_code_city_node_event()
         ↓
handle_node_click() called with validated data
         ↓
carl.gather_context() fetches fiefdom context
         ↓
build_code_city_context_payload() assembles full payload
         ↓
set_code_city_context() stores in state
         ↓
ticket_payload generated with merged errors
         ↓
set_clicked_node(ticket_payload)
         ↓
deploy_panel.show(file_path, status, errors)
         ↓
set_show_deploy(True)
         ↓
Deploy Panel UI emerges
```

### 2.3 Combat Node Flow

```
User clicks purple building
         ↓
handle_node_click() receives status="combat"
         ↓
combat_tracker.get_deployment_info(file_path)
         ↓
Log agent active message (no panel shown)
```

### 2.4 Working Node Flow

```
User clicks gold building
         ↓
handle_node_click() receives status="working"
         ↓
set_selected(file_path) updates selection
         ↓
Log "Selected (working)" message (no panel shown)
```

---

## 3. How Summon Gets the Payload

### 3.1 IMPORTANT FINDING: Summon is SEPARATE from Node Click

**Summon does NOT receive node click payloads directly.** It is a standalone search feature accessed via `handle_summon()`:

```
User presses summon hotkey / clicks summon button
         ↓
handle_summon() toggles show_summon
         ↓
User types search query
         ↓
Summon searches codebase independently
         ↓
build_summon_results_view() renders cards
```

### 3.2 Current Summon Data Flow

Summon receives results from a search, displaying:
- `fiefdom` - directory path
- `health.status` - working/broken/combat
- `health.errors` - error count
- `health.warnings` - warning count

**Key insight:** Summon and node click are currently disconnected. There is NO automatic handoff of the node click payload to Summon.

---

## 4. What Data Is Missing

### 4.1 Context Data Gaps

| Data | Currently Available | Source | Gap |
|------|---------------------|--------|-----|
| **File content** | No | - | Need actual source code for LLM context |
| **Git history** | No | - | Need recent commits/changes |
| **Test associations** | No | - | Need linked test files |
| **Recent changes** | No | - | Need modification history |
| **AI context** | No | - | Need relevant docs/similar files |
| **Stack trace** | Partial | node.errors | Need full trace extraction |

### 4.2 Integration Gaps

| Gap | Description | Impact |
|-----|-------------|--------|
| **No node→Summon handoff** | Clicking a node doesn't prepopulate Summon | Can't use node context in AI search |
| **No Sitting Room auto-entry** | `sitting_room` config exists but not always used | Room-level inspection incomplete |
| **No context streaming** | Full payload loaded at once | Large codebases slow |
| **No incremental errors** | Errors extracted once | Dynamic error tracking missing |
| **No cross-file context** | Only single file context | Missing broader system understanding |

### 4.3 Data Fields Not Passed to DeployPanel

From `DeployPanel.show()` signature:
```python
def show(self, file_path: str, status: str, errors: List[str]) -> None:
```

**Missing that are available in ticket_payload:**
- `context.health_status`
- `context.broken_imports`
- `context.tickets`
- `context.locks`
- `building_panel` (stored but not rendered)
- `room_entry` (stored but not rendered)

---

## 5. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     JAVASCRIPT (woven_maps_template.html)            │
│                                                                      │
│  User clicks node                                                   │
│       ↓                                                             │
│  node.status determines color (working/broken/combat)               │
│       ↓                                                             │
│  window.parent.postMessage({type: 'WOVEN_MAPS_NODE_CLICK', node})  │
└─────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     06_maestro.py (Python Bridge)                   │
│                                                                      │
│  on_node_click_bridge_change(payload_json)                          │
│       ↓                                                             │
│  process_node_click(payload)                                       │
│       ↓                                                             │
│  validate_code_city_node_event() ──► CodeCityNodeEvent contract    │
│       ↓                                                             │
│  handle_node_click(node_data)                                       │
└─────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     Context Assembly Pipeline                       │
│                                                                      │
│  1. derive_context_scope(file_path)  → "IP/plugins/"               │
│  2. carl.gather_context(scope)         → FiefdomContext              │
│  3. build_code_city_context_payload()  → Full context dict           │
│       - build_building_panel_for_node()                             │
│       - select_room_entry()                                         │
└─────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     State Storage (mo.state)                         │
│                                                                      │
│  set_code_city_context()     → Building panel + room entry           │
│  set_clicked_node()         → Ticket payload (broken only)          │
│  set_show_deploy()          → Deploy panel visibility               │
│  set_selected()              → Current file selection               │
│  set_view_mode()            → city / sitting_room                   │
└─────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     Panel Rendering                                  │
│                                                                      │
│  if status == "broken":                                             │
│      deploy_panel.render()  → LLM deployment UI                     │
│                                                                      │
│  if status == "combat":                                             │
│      combat_tracker.get_deployment_info() → agent active message    │
│                                                                      │
│  if status == "working":                                            │
│      building info card (via code_city_context)                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Key Source Files

| File | Purpose |
|------|---------|
| `IP/features/maestro/code_city_context.py` | Context payload assembly |
| `IP/contracts/building_panel.py` | BuildingPanel schema |
| `IP/contracts/code_city_node_event.py` | Node click event contract |
| `IP/plugins/06_maestro.py` | Main handler + panel routing |
| `IP/plugins/components/deploy_panel.py` | LLM deployment UI |
| `IP/carl_core.py` | Context gathering (FiefdomContext) |
| `IP/static/woven_maps_template.html` | JS node click emission |

---

## 7. Recommendations for Integration

1. **Add node click → Summon handoff**: When clicking a node, prepopulate Summon with the file's context
2. **Pass full context to DeployPanel**: Use `building_panel` and `room_entry` in the deploy UI
3. **Add file content to payload**: Include first N lines of source for LLM context
4. **Stream Sitting Room entry**: Use the `sitting_room` config to auto-enter room view
5. **Add git context**: Include recent changes to the file

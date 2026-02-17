# Task ID: 8

**Title:** Implement node-click bridge in maestro plugin

**Status:** done

**Dependencies:** 2 ✓, 7 ✓

**Priority:** high

**Description:** Wire JS node click events to Python handle_node_click() callback with schema validation

**Details:**

Create a bridge channel in IP/plugins/06_maestro.py to receive node click events from the Code City iframe and invoke handle_node_click().

Implementation approach:
1. Add a hidden marimo state channel for clicked node data
2. Add JavaScript listener in Code City HTML template to post validated events
3. Parse and validate events using CodeCityNodeEvent schema
4. Invoke handle_node_click() on valid events

In 06_maestro.py, around line 300 (in render function):
```python
# Add state for node click bridge
get_clicked_node_raw, set_clicked_node_raw = mo.state(None)

# Bridge handler - validates and processes node clicks
def process_node_click(raw_payload):
    if not raw_payload:
        return
    
    try:
        from IP.contracts.code_city_node_event import validate_code_city_node_event
        
        # Validate payload
        validated = validate_code_city_node_event(raw_payload)
        
        # Update clicked node state
        set_clicked_node(validated.to_dict())
        
        # Invoke existing handler
        handle_node_click(validated.to_dict())
        
    except (ValueError, KeyError, TypeError) as e:
        # Log validation errors safely
        log_action(f"Invalid node click payload: {e}")
        return

# Add reactive effect to process clicks
if get_clicked_node_raw():
    process_node_click(get_clicked_node_raw())
```

Modify woven_maps.py template to post to the bridge channel instead of just window.parent.postMessage. This requires adding a marimo callback mechanism.

Alternative simpler approach using existing window.__clicked_node__:
Add JavaScript in maestro that polls window.frames and checks for clicked node, then validates and calls Python handler.

**Test Strategy:**

Manual test: (1) Run marimo run orchestr8.py, (2) Open Code City view, (3) Click a broken node, (4) Verify deploy panel opens with correct file path and status, (5) Click working node - no deploy panel, (6) Send malformed event - verify logged safely without crash

## Subtasks

### 8.1. Add hidden marimo state channel for clicked node data in maestro

**Status:** pending  
**Dependencies:** None  

Create a new mo.state pair (get_clicked_node_raw, set_clicked_node_raw) in the render function of 06_maestro.py to serve as the bridge channel for receiving raw node click events from the Code City iframe.

**Details:**

In IP/plugins/06_maestro.py around line 470 (near the existing get_clicked_node state), add:

```python
# Raw node click bridge channel - receives unvalidated events from iframe
get_clicked_node_raw, set_clicked_node_raw = mo.state(None)
```

This state variable will hold the raw payload from the iframe's postMessage before validation occurs. The existing get_clicked_node state (line 470-472) will continue to hold validated, processed node data. The separation allows the bridge to receive untrusted data while the main state only holds validated data.

### 8.2. Modify woven_maps.py JavaScript template to postMessage validated events to parent

**Status:** pending  
**Dependencies:** 8.1  

Update the canvas click handler in WOVEN_MAPS_TEMPLATE (around line 2680-2703) to emit a more structured event payload that includes all fields needed for CodeCityNodeEvent schema validation.

**Details:**

The current postMessage at line 2688-2701 already sends a structured payload with type 'WOVEN_MAPS_NODE_CLICK'. Enhance it to:

1. Add explicit field typing for the node object (ensure nodeType defaults to 'file' if undefined)
2. Ensure errors is always an array (never undefined/null)
3. Add timestamp to the event for debugging

Modify the postMessage in WOVEN_MAPS_TEMPLATE:
```javascript
window.parent.postMessage({
    type: 'WOVEN_MAPS_NODE_CLICK',
    timestamp: Date.now(),
    node: {
        path: node.path || '',
        status: node.status || 'working',
        loc: node.loc || 0,
        errors: Array.isArray(node.errors) ? node.errors : [],
        nodeType: node.nodeType || 'file',
        centrality: node.centrality || 0,
        inCycle: !!node.inCycle,
        incomingCount: node.incomingCount || 0,
        outgoingCount: node.outgoingCount || 0
    }
}, '*');
```

This ensures the payload always has all required fields with safe defaults.

### 8.3. Create process_node_click() bridge handler with schema validation using CodeCityNodeEvent

**Status:** pending  
**Dependencies:** 8.1  

Implement the process_node_click() function in 06_maestro.py that validates raw payloads using the CodeCityNodeEvent schema and safely handles validation errors without crashing the UI.

**Details:**

Add the bridge handler function in 06_maestro.py after the event handlers section (around line 875):

```python
def process_node_click(raw_payload: Optional[dict]) -> None:
    """Bridge handler - validates and processes node clicks from Code City iframe.
    
    Receives raw postMessage payload, validates against CodeCityNodeEvent schema,
    and invokes handle_node_click() on valid events. Invalid payloads are logged
    safely without crashing the UI.
    """
    if not raw_payload:
        return
    
    try:
        # Import validation function (Task 2 dependency)
        from IP.contracts.code_city_node_event import validate_code_city_node_event
        
        # Extract node data from postMessage wrapper
        node_data = raw_payload.get('node') if isinstance(raw_payload, dict) else None
        if not node_data:
            log_action("Invalid node click: missing node data")
            return
        
        # Validate payload against schema
        validated = validate_code_city_node_event(node_data)
        
        # Update validated clicked node state
        set_clicked_node(validated.to_dict() if hasattr(validated, 'to_dict') else validated)
        
        # Invoke existing handler
        handle_node_click(validated.to_dict() if hasattr(validated, 'to_dict') else validated)
        
    except ImportError:
        # Schema not yet implemented - fall back to direct pass-through
        log_action("CodeCityNodeEvent schema not available, using raw payload")
        if isinstance(raw_payload, dict) and 'node' in raw_payload:
            handle_node_click(raw_payload['node'])
    except (ValueError, KeyError, TypeError) as e:
        # Log validation errors safely - don't crash UI
        log_action(f"Invalid node click payload: {e}")
        return
```

This handler gracefully degrades when the schema contract (Task 2) isn't implemented yet.

### 8.4. Wire up reactive effect to invoke handle_node_click() on validated events and test integration end-to-end

**Status:** pending  
**Dependencies:** 8.1, 8.2, 8.3  

Connect the marimo state channel to the bridge handler using marimo's reactive pattern, and implement JavaScript-to-Python communication via the window.__clicked_node__ polling mechanism or marimo callback.

**Details:**

This is the most complex subtask as it bridges JS↔Python reactivity. Two implementation approaches:

**Approach A - Polling (simpler, works now):**
Add JavaScript in node_click_js (line 1711) to update a hidden input that marimo can observe:

```javascript
// Add after window.__clicked_node__ assignment
const hiddenInput = document.getElementById('__node_click_bridge__');
if (hiddenInput) {
    hiddenInput.value = JSON.stringify(event.data.node);
    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
}
```

Add hidden input element and reactive handler in maestro:
```python
# Hidden bridge input
node_click_bridge = mo.ui.text(
    value='',
    on_change=lambda v: process_node_click(json.loads(v) if v else None)
)
node_click_bridge_html = mo.Html(
    f'<div style="display:none">{node_click_bridge}</div>'
)
```

**Approach B - postMessage listener (cleaner, needs marimo support):**
Use mo.js to register a callback that marimo invokes on postMessage events.

Implement Approach A first as it's guaranteed to work with current marimo.

Add to the return vstack after node_click_js:
```python
node_click_bridge_html,  # Hidden bridge element
```

Test the full flow: click building → JS postMessage → hidden input update → on_change fires → process_node_click() → validate → handle_node_click() → deploy panel opens for broken nodes.

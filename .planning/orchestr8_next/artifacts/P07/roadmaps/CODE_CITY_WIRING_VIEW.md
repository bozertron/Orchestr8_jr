# Code City Wiring View Analysis

**Source**: grep for wiring in /home/bozertron/Orchestr8_jr/IP/
**Target**: a_codex_plan
**Focus**: Visualizing import/export connections between buildings

---

## 1. Edge/Wiring Data Structure

The wiring/edge data in Code City is built around the `EdgeData` dataclass defined in `IP/woven_maps.py` (lines 142-175). This structure captures all metadata necessary for visualizing and interacting with import relationships between source files in the codebase.

### Core EdgeData Schema

```python
@dataclass
class EdgeData:
    """Represents an import relationship between files."""
    
    source: str           # Source file path (importer)
    target: str          # Target file path (imported)
    resolved: bool = True            # Whether the import resolves
    bidirectional: bool = False      # Mutual imports (cycles)
    line_number: int = 0             # Source line of import
    
    # Fiefdom boundary crossing metadata
    from_fiefdom: str = ""           # Fiefdom of source file
    to_fiefdom: str = ""             # Fiefdom of target file
    is_boundary: bool = False        # True if edge crosses fiefdom boundary
    
    # Boundary contract metadata
    allowed_types: List[str] = field(default_factory=list)    # e.g., ["imports", "calls"]
    forbidden_crossings: List[str] = field(default_factory=list)  # e.g., ["cyclic_imports"]
    contract_status: str = ""         # "defined" | "draft" | "missing"
```

### Edge Serialization

The `EdgeData.to_dict()` method (lines 162-175) converts edges to JavaScript-friendly format with camelCase keys:

```python
def to_dict(self) -> Dict[str, Any]:
    return {
        "source": self.source,
        "target": self.target,
        "resolved": self.resolved,
        "bidirectional": self.bidirectional,
        "lineNumber": self.line_number,
        "fromFiefdom": self.from_fiefdom,
        "toFiefdom": self.to_fiefdom,
        "isBoundary": self.is_boundary,
        "allowedTypes": self.allowed_types,
        "forbiddenCrossings": self.forbidden_crossings,
        "contractStatus": self.contract_status,
    }
```

### Edge Key Generation

Edges are uniquely identified using a composite key in the frontend:

```javascript
function edgeKey(edge) {
    return `${edge.source}->${edge.target}:${edge.lineNumber || 0}`;
}
```

This key format (`source->target:lineNumber`) enables efficient lookups in Sets and Maps for highlighting and selection operations.

### GraphData Container

Edges are aggregated in the `GraphData` dataclass (lines 302-321):

```python
@dataclass
class GraphData:
    """Complete data structure for visualization."""
    
    nodes: List[CodeNode] = field(default_factory=list)
    edges: List[EdgeData] = field(default_factory=list)
    config: GraphConfig = field(default_factory=GraphConfig)
    neighborhoods: List[Neighborhood] = field(default_factory=list)
```

---

## 2. Gold/Teal/Purple Wiring Colors

The wiring color system in Code City follows the established Orchestr8 three-state color scheme, with additional colors for special edge conditions. The colors are defined in multiple locations and used consistently throughout the visualization pipeline.

### Color Constants Definition

The canonical colors are defined in `IP/woven_maps.py` (lines 56-77):

```python
COLORS = {
    "gold_metallic": "#D4AF37",   # Working code
    "blue_dominant": "#1fbdea",   # Broken code / Teal during scan
    "purple_combat": "#9D4EDD",   # Combat (LLM active)
    "bg_primary": "#0A0A0B",      # The Void
    "bg_elevated": "#121214",     # Elevated surfaces
    "gold_dark": "#B8860B",       # Secondary gold
    "gold_saffron": "#F4C430",    # Bright highlights
}

JS_COLORS = {
    "void": "#0A0A0B",
    "working": "#D4AF37",
    "broken": "#1fbdea",
    "combat": "#9D4EDD",
    "wireframe": "#333333",
    "teal": "#1fbdea",
    "gold": "#D4AF37",
    "cycle": "#ff4444",
    "edge": "#333333",
    "edge_broken": "#ff6b6b",
}
```

### Wiring Color Application Logic

The edge rendering logic in `IP/static/woven_maps_template.html` (lines 3368-3382) applies colors based on edge state:

```javascript
// Canonical color scheme: Gold for resolved, Teal for unresolved
if (!edge.resolved) {
    ctx.strokeStyle = COLORS.teal;      // Teal for broken imports
    ctx.setLineDash([4, 4]);             // Dashed for broken
    ctx.lineWidth = 1.0;
} else if (edge.bidirectional) {
    ctx.strokeStyle = COLORS.cycle;     // Red for mutual imports (cycle)
    ctx.setLineDash([]);
    ctx.lineWidth = 1.5;
} else {
    ctx.strokeStyle = COLORS.gold;       // Gold for working imports
    ctx.setLineDash([]);
    ctx.lineWidth = 0.8;
}
```

### Color State Matrix

| State | Color | Hex Code | Visual Treatment |
|-------|-------|----------|------------------|
| Working | Gold Metallic | #D4AF37 | Solid line, 0.8px width |
| Broken/Unresolved | Teal/Blue | #1fbdea | Dashed line (4,4), 1.0px width |
| Combat/Active | Purple | #9D4EDD | Highlighted during LLM operations |
| Cyclic Dependency | Red | #ff4444 | Solid line, 1.5px width |
| Selected Edge | Gold | #D4AF37 | Solid line, 2.8px width (highlighted) |
| Signal Path | Saffron Gold | #F4C430 | Solid line, 1.9px width |
| Dimmed/Background | Dark Gray | #333333 | 0.7px width, reduced opacity |

### Color Constants in Contracts

The color system is also codified in `IP/contracts/status_merge_policy.py` (lines 39-41) and `IP/contracts/__init__.py` (lines 9-11):

```python
# From contracts/__init__.py
# Gold   #D4AF37  = working
# Teal   #1fbdea  = broken
# Purple #9D4EDD  = combat
```

### Status Color Helper

A utility function in `IP/contracts/status_merge_policy.py` (lines 38-43) provides consistent status-to-color mapping:

```python
def get_status_color(status: str) -> str:
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
    }
    return colors.get(status, "#D4AF37")
```

---

## 3. Interactive Edge Clicking

Code City supports interactive edge selection through a combination of hit-testing, state management, and visual feedback. The interaction model allows users to click on any wire to inspect its properties and initiate rewire operations.

### Edge Hit Detection Algorithm

The hit detection is implemented in `findEdgeAt(x, y)` function in `IP/static/woven_maps_template.html` (lines 3025-3058):

```javascript
function findEdgeAt(x, y) {
    let best = null;
    let bestDistance = Number.POSITIVE_INFINITY;

    for (const edge of filteredEdges) {
        const sourcePos = getNodeRenderPosition(edge.source);
        const targetPos = getNodeRenderPosition(edge.target);
        if (!sourcePos || !targetPos) continue;

        const x1 = sourcePos.x;
        const y1 = sourcePos.y;
        const x2 = targetPos.x;
        const y2 = targetPos.y;
        
        // Calculate curve control point (matches rendering logic)
        const curveOffset = Math.min(dist * 0.15, 30);
        const perpX = (-dy / dist) * curveOffset;
        const perpY = (dx / dist) * curveOffset;
        const cx = ((x1 + x2) / 2) + perpX;
        const cy = ((y1 + y2) / 2) + perpY;
        
        // Distance to quadratic bezier curve
        const d = distanceToQuadraticCurve(x, y, x1, y1, cx, cy, x2, y2);

        if (d < bestDistance) {
            bestDistance = d;
            best = edge;
        }
    }

    // 8px hit detection threshold
    if (best && bestDistance <= 8) return best;
    return null;
}
```

### Click Event Handler

The canvas click handler in `IP/static/woven_maps_template.html` (lines 4500-4501) coordinates node and edge detection:

```javascript
const node = findNodeAt(x, y);
const edge = node ? null : findEdgeAt(x, y);
```

The logic prioritizes node selection over edge selection—when a user clicks on a node, no edge hit test is performed.

### Selection State Management

Selection state is tracked with module-level variables (lines 1648-1649):

```javascript
let selectedConnection = null;
let selectedConnectionKey = null;
```

When an edge is selected, the following happens:

1. **Selection Storage**: The edge object is stored in `selectedConnection`
2. **Key Generation**: A unique key is computed via `edgeKey(edge)` 
3. **Signal Path Computation**: Connected nodes and edges are identified for highlighting
4. **Panel Update**: The connection panel is populated with edge details

### Selection Clearing

Selection can be cleared via `clearSelectedConnection()` (lines 3017-3023):

```javascript
function clearSelectedConnection() {
    selectedConnection = null;
    selectedConnectionKey = null;
    highlightedNodeIds = new Set();
    highlightedEdgeKeys = new Set();
    updateConnectionPanel();
}
```

### Visual Feedback on Selection

When an edge is selected, the rendering code (lines 3356-3366) applies distinctive styling:

```javascript
if (hasSelection) {
    if (isSelected) {
        ctx.strokeStyle = COLORS.gold;
        ctx.lineWidth = 2.8;           // Thicker for selected
    } else if (isInSignalPath) {
        ctx.strokeStyle = '#F4C430';    // Saffron gold
        ctx.lineWidth = 1.9;
    } else {
        ctx.strokeStyle = COLORS.edge;  // Dimmed
        ctx.lineWidth = 0.7;
    }
    ctx.setLineDash(edge.resolved ? [] : [5, 4]);
}
```

### Signal Path Highlighting

When an edge is selected, the system identifies and highlights the connected subgraph:

- **Source and Target Nodes**: Highlighted with increased opacity
- **Direct Connections**: Other edges connecting the same nodes get highlighted
- **Propagation**: A breadth-first traversal identifies the neighborhood of related edges

The `highlightedNodeIds` and `highlightedEdgeKeys` Sets store the elements to emphasize.

---

## 4. Patchbay Integration

The Patchbay system provides a bridge between Code City's visual edge selection and actual import graph manipulation. It enables users to validate and apply import rewiring operations directly from the visualization interface.

### Architecture Overview

The Patchbay integration follows a three-layer architecture:

1. **Frontend Layer** (`woven_maps_template.html`): Connection panel UI and edge selection
2. **Bridge Layer** (`connection_actions.py`): Action validation and orchestration
3. **Backend Layer** (`patchbay.py`): Dry-run validation and file modification

### Connection Action Flow

#### Step 1: Edge Selection

When a user clicks an edge in Code City:
1. `findEdgeAt(x, y)` identifies the clicked edge
2. `selectedConnection` is updated with edge data
3. `updateConnectionPanel()` renders the connection panel with edge details

#### Step 2: Connection Panel UI

The connection panel (defined in CSS lines 104-278 of `woven_maps_template.html`) displays:

- Source file path
- Target file path  
- Import status (resolved/unresolved)
- Line number in source file
- Drop zone for rewire target
- Action buttons (Dry Run, Apply)

#### Step 3: Action Emission

When the user initiates an action:

```javascript
function emitConnectionAction(action) {
    if (!selectedConnection) return;
    
    const payload = {
        action: action,
        connection: {
            source: selectedConnection.source,
            target: selectedConnection.target,
            resolved: !!selectedConnection.resolved,
            lineNumber: selectedConnection.lineNumber || 0,
            edgeType: selectedConnection.type || 'import',
        },
        proposedTarget: input.value,
        actorRole: getCurrentActorRole(),
    };
    
    // Send to bridge via marimo text input
    bridgeElement.value = JSON.stringify(payload);
    bridgeElement.dispatchEvent(new Event('change'));
}
```

### Bridge Communication

The Python-JavaScript bridge uses marimo's reactive text inputs (lines 1086-1095 in `06_maestro.py`):

```python
connection_action_bridge = mo.ui.text(
    value=get_connection_action_payload(),
    on_change=on_connection_action_bridge_change,
)

connection_action_result_bridge = mo.ui.text(
    value=get_connection_action_result_payload()
)
```

### Action Handling in Python

The `handle_connection_action()` function in `IP/features/maestro/connection_actions.py` (lines 12-316) orchestrates the workflow:

#### Dry-Run Validation

```python
if event.action == "dry_run_rewire":
    dry_run = dry_run_patchbay_rewire(
        project_root=str(project_root_path),
        source_file=source,
        current_target=target,
        proposed_target=proposed,
    )
    
    if dry_run.get("canApply"):
        # Emit success result
        emit_connection_action_result({...})
    else:
        # Emit blocked result with issues
        emit_connection_action_result({...})
```

#### Apply Operation

```python
if event.action == "apply_rewire":
    # Check permissions
    if actor_role not in allowed_roles:
        emit_connection_action_result({
            "ok": False,
            "message": f"Denied for role '{actor_role}'"
        })
        return
    
    # Apply with rollback capability
    apply_result = apply_patchbay_rewire(
        project_root=str(project_root_path),
        source_file=source,
        current_target=target,
        proposed_target=proposed,
        auto_rollback=True,
    )
```

### Result Feedback Loop

Results flow back through the result bridge (lines 1094-1095, 1518-1522):

```javascript
const resultBridgeId = '{connection_action_result_bridge._id}';

// Poll for result changes
const intervalKey = '__orchestr8_connection_result_interval__';
if (!window[intervalKey]) {
    window[intervalKey] = setInterval(() => {
        const resultEl = document.getElementById(resultBridgeId);
        if (!resultEl || !resultEl.value) return;
        
        try {
            const payload = JSON.parse(resultEl.value);
            renderConnectionActionResult(payload);
        } catch (err) {
            console.warn('Invalid connection result payload:', err);
        }
    }, 300);
}
```

### Rewire Drag-and-Drop

Users can drag file paths from the connection panel onto other nodes to set a proposed rewire target:

```javascript
function handleRewireDrop(event) {
    event.preventDefault();
    setRewireDropActive(false);
    if (!selectedConnection) return;
    
    let droppedPath = String(event.dataTransfer.getData('text/orchestr8-path')).trim();
    if (!droppedPath) return;
    
    if (droppedPath === selectedConnection.source) {
        phaseEl.textContent = 'invalid rewire target: source file';
        return;
    }
    
    // Set input value and trigger dry-run
    input.value = droppedPath;
    emitConnectionAction('dry_run_rewire');
}
```

### Security and Guardrails

The Patchbay system implements several security measures:

1. **Apply Disabled by Default**: `ORCHESTR8_PATCHBAY_APPLY=1` must be set explicitly
2. **Role-Based Access**: Only configured roles (default: `founder`, `operator`) can apply changes
3. **Dry-Run Required**: Apply only proceeds if dry-run passes
4. **Auto-Rollback**: Failed applies automatically rollback changes
5. **Proposed Target Validation**: Cannot rewire to the source file itself

---

## 5. Technical Implementation Summary

### File Organization

| Component | File Path | Purpose |
|-----------|-----------|---------|
| Edge Data Model | `IP/woven_maps.py` (lines 142-175) | `EdgeData` dataclass definition |
| Graph Container | `IP/woven_maps.py` (lines 302-321) | `GraphData` aggregation |
| Edge Rendering | `IP/static/woven_maps_template.html` (lines 3330-3425) | Canvas-based edge drawing |
| Hit Detection | `IP/static/woven_maps_template.html` (lines 3025-3058) | `findEdgeAt()` implementation |
| Connection Panel | `IP/static/woven_maps_template.html` (lines 104-278) | CSS styling for panel UI |
| Action Bridge | `IP/features/maestro/connection_actions.py` | `handle_connection_action()` orchestrator |
| Event Contract | `IP/contracts/connection_action_event.py` | `ConnectionActionEvent` schema |
| Patchbay Backend | `IP/features/connections/patchbay.py` | `dry_run_patchbay_rewire()`, `apply_patchbay_rewire()` |
| Maestro Integration | `IP/plugins/06_maestro.py` (lines 103-109, 387-395) | Bridge setup and wiring |

### Key Functions and Methods

| Function/Method | Location | Signature |
|-----------------|----------|-----------|
| `EdgeData.to_dict()` | `IP/woven_maps.py:162` | `() -> Dict[str, Any]` |
| `GraphData.to_dict()` | `IP/woven_maps.py:311` | `() -> Dict[str, Any]` |
| `findEdgeAt(x, y)` | `woven_maps_template.html:3025` | `(x: number, y: number) -> Edge \| null` |
| `edgeKey(edge)` | `woven_maps_template.html:3025` | `(edge: Edge) -> string` |
| `updateConnectionPanel()` | `woven_maps_template.html:2874` | `() -> void` |
| `emitConnectionAction(action)` | `woven_maps_template.html:2976` | `(action: string) -> void` |
| `handle_connection_action()` | `connection_actions.py:12` | `(payload, *, ...) -> None` |
| `dry_run_patchbay_rewire()` | `patchbay.py:94` | `(...) -> PatchbayDryRunResult` |
| `apply_patchbay_rewire()` | `patchbay.py:226` | `(...) -> dict` |

### Performance Considerations

- **Edge Filtering**: Edges are filtered by `displayZone` before rendering (`filteredEdges` Set)
- **Hit Test Optimization**: Only visible edges are tested; 8px threshold balances precision vs. usability
- **Signal Path Limits**: Highlighting propagation is bounded to prevent performance degradation on dense graphs
- **Stream Budget**: Building data streams at configurable BPS (`ORCHESTR8_CODE_CITY_STREAM_BPS`, default: 5,000,000)

---

## 6. Interaction Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CODE CITY WIRING INTERACTION                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐     ┌─────────────┐     ┌──────────────────┐
    │  Canvas  │────▶│ findEdgeAt  │────▶│ selectedConnection│
    │  Click  │     │  (8px hit)  │     │   + key gen       │
    └──────────┘     └─────────────┘     └────────┬─────────┘
                                                   │
                                                   ▼
                                        ┌────────────────────┐
                                        │ updateConnection  │
                                        │      Panel        │
                                        └────────┬───────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
                    ▼                            ▼                            ▼
         ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
         │  User Views      │        │  User Drags      │        │  User Clicks     │
         │  Connection      │        │  Path to Rewire  │        │  Dry-Run/Apply   │
         └────────┬─────────┘        └────────┬─────────┘        └────────┬─────────┘
                  │                          │                          │
                  ▼                          ▼                          ▼
       ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
       │ Display:         │        │ handleRewire     │        │ emitConnection   │
       │ - Source/Target │        │     Drop()       │        │     Action()     │
       │ - Status/Line   │        │                  │        │                  │
       │ - Path List     │        │ Set input value  │        │ JSON → bridge    │
       └──────────────────┘        │ Trigger dry-run  │        └────────┬─────────┘
                                  └──────────────────┘                 │
                                                                      ▼
                                                      ┌────────────────────────────────┐
                                                      │   MARIMO BRIDGE                │
                                                      │   connection_action_bridge    │
                                                      └────────────┬───────────────────┘
                                                                       │
                                                                       ▼
                                                      ┌────────────────────────────────┐
                                                      │   handle_connection_action()  │
                                                      │   - validate payload           │
                                                      │   - route to patchbay          │
                                                      └────────────┬───────────────────┘
                                                                       │
                                                    ┌──────────────────┼──────────────────┐
                                                    │                  │                  │
                                                    ▼                  ▼                  ▼
                                         ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
                                         │ dry_run_         │ │ apply_       │ │ result           │
                                         │ patchbay_rewire  │ │ patchbay_    │ │ bridge           │
                                         │                  │ │ _rewire     │ │ (poll + render)  │
                                         └──────────────────┘ └──────────────┘ └──────────────────┘
```

---

## 7. Extension Points and Future Work

### Potential Enhancements

1. **Bidirectional Edge Visualization**: Currently cycles show as red edges; could add bidirectional arrows
2. **Fiefdom Boundary Highlighting**: Edges crossing neighborhood boundaries could have distinctive styling
3. **Contract Status Indicators**: Visual cues for defined/draft/missing border contracts
4. **Multi-Select Mode**: Allow selecting multiple edges for batch operations
5. **Undo/Redo Stack**: Full history of rewire operations with rollback capability
6. **Edge Weight Visualization**: Line thickness based on import frequency or token count

### Configuration Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ORCHESTR8_PATCHBAY_APPLY` | unset (disabled) | Enable apply operations |
| `ORCHESTR8_PATCHBAY_ALLOWED_ROLES` | `founder,operator` | Roles permitted to apply |
| `ORCHESTR8_CODE_CITY_MAX_BYTES` | 9,000,000 | Payload size guard |
| `ORCHESTR8_CODE_CITY_STREAM_BPS` | 5,000,000 | Building stream bandwidth |

---

## 8. References

- **Entry Point**: `orchestr8.py` -> `IP/plugins/06_maestro.py` -> `IP/woven_maps.py`
- **Color System**: `IP/contracts/status_merge_policy.py`
- **Event Schema**: `IP/contracts/connection_action_event.py`
- **Frontend Template**: `IP/static/woven_maps_template.html`
- **Patchbay Backend**: `IP/features/connections/patchbay.py`
- **Connection Actions**: `IP/features/maestro/connection_actions.py`

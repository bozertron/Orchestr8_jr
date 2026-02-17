# Code City Neighborhood/Town-Square System

**Source:** Search for neighborhood in /home/bozertron/Orchestr8_jr/IP/  
**Target:** a_codex_plan  
**Analysis Date:** 2026-02-16

---

## Overview

The Code City neighborhood/town-square system provides the organizational layer that groups files into fiefdoms/districts within the 3D visualization. This document analyzes how the city organizes files into neighborhoods, classifies the town square, handles border contracts between neighborhoods, and renders the visual layout.

---

## 1. Neighborhood/Fiefdom Detection

### Detection Mechanism

Neighborhoods are detected in `IP/features/code_city/graph_builder.py` via the `compute_neighborhoods()` function (lines 12-111).

**Algorithm:**
1. **Directory Grouping**: Files are grouped by their parent directory path
2. **Centroid Calculation**: Each neighborhood's center is the average position of all files in that directory
3. **Boundary Computation**: Rectangular boundaries are calculated from min/max X/Y coordinates of all nodes in the neighborhood with configurable padding
4. **Status Determination**: Neighborhood status is computed by majority vote:
   - If any node has `combat` status → neighborhood is `broken`
   - If broken nodes > working nodes → neighborhood is `broken`
   - Otherwise → neighborhood is `working`

### Key Data Structure

```python
@dataclass
class Neighborhood:
    name: str                    # Directory path as neighborhood name
    nodes: List[str]             # File paths in this neighborhood
    center_x: float              # Centroid X coordinate
    center_y: float              # Centroid Y coordinate
    boundary_points: List[Dict] # Polygon vertices for 2D boundary
    integration_count: int      # Edges crossing to other neighborhoods
    neighbors: List[Dict]       # Connected neighborhoods with crossing counts
    status: str                 # "working" | "broken"
```

### Integration Counting

The system tracks cross-neighborhood edges:
- For each edge, determine source and target neighborhoods
- If they differ, increment the integration count for the source neighborhood
- This creates a graph of neighborhood-to-neighborhood dependencies

### Fiefdom Extraction

Fiefdoms are extracted from file paths in `graph_builder.py` (lines 161-166):

```python
def _extract_fiefdom(file_path: str) -> str:
    """Extract fiefdom name from file path (first directory component)."""
    parts = Path(file_path).parts
    if len(parts) >= 2:
        return parts[0]
    return ""
```

This extracts the top-level directory as the fiefdom identifier (e.g., `IP`, `docs`, `Font`).

---

## 2. Town Square Classification

### Display Zone System

The town square classification is handled in `IP/woven_maps.py` (lines 378-531) with the `get_display_zone()` function. Files are assigned to one of four display zones:

| Zone | Description |
|------|-------------|
| `city` | Default - rendered as buildings in main Code City |
| `town_square` | Infrastructure files displayed in separate infra zone |
| `hidden` | Files not rendered (secrets, build artifacts) |
| `minimap_only` | Only visible in minimap, not main canvas |

### Classification Patterns

The `INFRA_PATTERNS` dictionary (lines 384-475) maps file patterns to classifications:

**Configuration Files** → `town_square`:
- `pyproject.toml`, `setup.py`, `requirements*.txt`
- `package.json`, `tsconfig*.json`
- `.github/**`, `.vscode/**`

**Infrastructure** → `town_square`:
- `Makefile`, `CMakeLists.txt`, `Dockerfile*`

**Documentation** → `town_square` / `minimap_only`:
- `README*`, `CHANGELOG*`, `LICENSE*` → `town_square`
- `*.md` → `minimap_only`

**Secrets/Build** → `hidden`:
- `.env*`, `node_modules/**`, `*.pyc`

**Assets** → `minimap_only` / `hidden`:
- `*.svg` → `minimap_only`
- `*.ico`, `*.png` → `hidden`

### Contract Schema

The classification contract is defined in `IP/contracts/town_square_classification.py`:

```python
Classification = Literal["infrastructure", "config", "build", "test", "docs", "asset"]
DisplayZone = Literal["town_square", "hidden", "minimap_only"]

@dataclass
class TownSquareClassification:
    path: str
    classification: Classification
    display_zone: DisplayZone = "town_square"
    reason: str = ""
    icon: str = ""
    group: str = ""
```

### Frontend Rendering

In `IP/static/woven_maps_template.html` (lines 656-663), nodes are filtered by display zone:

```javascript
const cityNodes = allNodes.filter(n => n.displayZone !== 'hidden' && n.displayZone !== 'town_square');
const townSquareNodes = allNodes.filter(n => n.displayZone === 'town_square');
```

---

## 3. Border Contracts Between Neighborhoods

### Contract Definition

Border contracts are defined in `IP/contracts/settlement_survey.py` (lines 24-30):

```python
@dataclass
class BoundaryContract:
    from_fiefdom: str           # Source fiefdom
    to_fiefdom: str             # Target fiefdom
    allowed_types: List[str]    # Permitted crossing types (e.g., ["imports", "calls"])
    forbidden_crossings: List[str]  # Prohibited patterns (e.g., ["cyclic_imports"])
    contract_status: str        # "defined" | "draft" | "missing"
```

### Contract Loading

Contracts are loaded from settlement survey JSON files in `graph_builder.py` (lines 251-277):

```python
survey_paths = [
    Path(project_root) / ".settlement" / "survey.json",
    Path(project_root) / ".planning" / "survey.json",
    Path(project_root) / "settlement_survey.json",
]
```

### Edge Classification

When building the import graph, each edge is classified as boundary or internal (lines 279-318):

```python
from_fiefdom = _extract_fiefdom(source)
to_fiefdom = _extract_fiefdom(target)
is_boundary = bool(from_fiefdom and to_fiefdom and from_fiefdom != to_fiefdom)

if is_boundary:
    contract = boundary_contracts_map.get((from_fiefdom, to_fiefdom))
    if contract:
        allowed_types = contract["allowed_types"]
        forbidden_crossings = contract["forbidden_crossings"]
        contract_status = contract["contract_status"]
    else:
        contract_status = "missing"
```

### Contract Status States

| Status | Meaning |
|--------|---------|
| `defined` | Contract exists and is validated |
| `draft` | Contract exists but needs review |
| `missing` | No contract defined for this fiefdom pair |

### Frontend Display

In `woven_maps_template.html` (lines 4627-4668), border contract metadata is displayed in the edge tooltip:

```javascript
const statusClass = edge.contractStatus === 'defined' ? 'working' : 
                    edge.contractStatus === 'draft' ? 'combat' : 'broken';
const fiefdomHtml = `<div style="margin-top:6px; padding-top:6px; border-top:1px solid #333;">
    From: ${edge.fromFiefdom} → To: ${edge.toFiefdom}
</div>`;
```

---

## 4. Visual Layout in 3D

### 2D Canvas Rendering

In `woven_maps_template.html` (lines 3227-3310), neighborhood boundaries are drawn on the 2D canvas:

```javascript
function drawNeighborhoodBoundaries(ctx, neighborhoods) {
    for (const neighborhood of neighborhoods) {
        const boundaryPoints = neighborhood.boundaryPoints;
        const isWorking = neighborhood.status === 'working';
        
        // Draw filled polygon with low opacity
        ctx.fillStyle = isWorking ? 'rgba(212, 175, 55, 0.08)' : 'rgba(31, 189, 234, 0.08)';
        
        // Draw boundary edges
        ctx.strokeStyle = isWorking ? '#D4AF37' : '#1fbdea';
        ctx.setLineDash([5, 5]); // Dashed lines for boundaries
        
        // Draw neighborhood label
        ctx.fillText(neighborhood.name, labelX, labelY);
        
        // Draw integration count badge
        if (neighborhood.integrationCount > 0) {
            // Badge showing cross-neighborhood connections
        }
    }
}
```

### 3D Boundary Rendering

In `IP/static/woven_maps_3d.js` (lines 612-724), neighborhoods are rendered as semi-transparent floor overlays:

```javascript
addNeighborhoodBoundaries(neighborhoods, scale = 10) {
    const LAYER_HEIGHT = 0.5; // Slightly above ground plane
    
    for (const neighborhood of neighborhoods) {
        const boundaryColor = neighborhood.status === "working" ? 
            CONFIG_3D.COLOR_WORKING : CONFIG_3D.COLOR_BROKEN;
        
        // Create boundary polygon shape
        const shape = new THREE.Shape();
        const points3D = boundaryPoints.map(p => 
            new THREE.Vector3(
                (p.x - 400) * (scale / 400),
                LAYER_HEIGHT,
                (p.y - 300) * (scale / 300)
            )
        );
        
        // Create mesh with low alpha for subtle overlay
        const material = new THREE.MeshBasicMaterial({
            color: boundaryColor,
            transparent: true,
            opacity: 0.15,
            side: THREE.DoubleSide,
            depthWrite: false,
        });
        
        // Create edge lines for visibility
        const edgeMaterial = new THREE.LineBasicMaterial({
            color: boundaryColor,
            transparent: true,
            opacity: 0.4,
        });
    }
}
```

### Navigation Levels

The system supports hierarchical navigation through neighborhoods (from `woven_maps_template.html` line 818):

```javascript
const NAVIGATION_LEVELS = ['overview', 'neighborhood', 'building', 'room', 'sitting_room'];
```

This allows drilling down from:
- **Overview**: Full city view with all neighborhoods
- **Neighborhood**: Single fiefdom focused view
- **Building**: Individual file/structure
- **Room**: Function/class within file
- **Sitting Room**: Deep code inspection

### Visual Styling

**Color Coding** (from `IP/woven_maps.py`):

| State | Color | Hex |
|-------|-------|-----|
| Working | Gold | #D4AF37 |
| Broken | Blue/Teal | #1fbdea |
| Combat | Purple | #9D4EDD |
| Town Square Border | Gray | #888888 |

**Boundary Appearance**:
- Filled polygon with 8-15% opacity
- Dashed edge lines (5px dash, 5px gap)
- Floating labels above boundaries
- Integration count badges showing cross-neighborhood connections

---

## Integration Points

### Key Modules

| Module | Responsibility |
|--------|----------------|
| `IP/features/code_city/graph_builder.py` | Neighborhood computation, fiefdom extraction, contract loading |
| `IP/woven_maps.py` | Display zone classification, infrastructure pattern matching |
| `IP/contracts/town_square_classification.py` | Classification schema/validation |
| `IP/contracts/settlement_survey.py` | Border contract schema |
| `IP/static/woven_maps_template.html` | 2D boundary rendering |
| `IP/static/woven_maps_3d.js` | 3D boundary overlays |

### Data Flow

```
File System Scan
       ↓
classify_infrastructure() → display_zone assignment
       ↓
calculate_layout() → X/Y positions
       ↓
compute_neighborhoods() → Neighborhood boundaries + integration counts
       ↓
load settlement_survey.json → BoundaryContract definitions
       ↓
build_from_connection_graph() → Edge classification with contract metadata
       ↓
Render (2D canvas + 3D scene)
```

---

## Future Enhancements (a_codex_plan)

### 1. Enhanced Fiefdom Detection
- Currently uses single top-level directory as fiefdom
- Could support multi-level fie fdom hierarchies (e.g., `IP/plugins` as sub-fiefdom of `IP`)

### 2. Contract Validation
- Add runtime validation that edges comply with boundary contracts
- Visual warnings for contract violations

### 3. Dynamic Neighborhood Clustering
- Allow users to manually group directories into custom neighborhoods
- Save custom groupings to user preferences

### 4. Town Square Expansion
- Currently town square is pattern-based only
- Could support explicit classification via config file
- Add more infrastructure categories (monitoring, deployment, etc.)

### 5. 3D Navigation
- Click-to-navigate to neighborhood in 3D
- Smooth camera transitions between neighborhoods
- Neighborhood-specific camera presets

### 6. Integration Metrics
- More sophisticated integration scoring
- Visualize integration direction (not just count)
- Highlight "bridge" files that connect neighborhoods

---

## Summary

The Code City neighborhood system provides a robust organizational layer for visualizing file relationships:

1. **Neighborhoods** are computed from directory structure with automatic boundary calculation
2. **Town Square** classification routes infrastructure files to a separate display zone
3. **Border Contracts** define typed agreements between fiefdoms with validation status
4. **Visual Layout** renders neighborhoods as semi-transparent overlays in both 2D and 3D views

The system is fully implemented and functional, with clear separation between data computation (Python) and visualization (JavaScript/Three.js).

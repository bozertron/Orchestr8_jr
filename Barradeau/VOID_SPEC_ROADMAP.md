# THE VOID: Codebase Visualization System

**Version:** 1.0 DRAFT  
**Date:** 2026-01-28  
**Authors:** Ben (Emperor) + Claude (Strategic Council)  
**Status:** SPEC + ROADMAP - Awaiting Approval

---

## I. Core Concept

### 1.1 The Dual-Purpose Visual

The Barradeau aesthetic serves two distinct audiences simultaneously:

| Audience | What They See | What It Does For Them |
|----------|---------------|----------------------|
| **Humans** | Ethereal fantasy cityscape | Intuitive spatial understanding of codebase health; blue blob = problem area |
| **LLMs** | Dense pixel grid with identifiable connection points | Architectural and syntax issues immediately visible; can parse structure humans cannot |

**This is the razor's edge:** The same visualization must be beautiful enough for humans to *want* to use it, while being data-dense enough for LLMs to extract actionable information.

### 1.2 The Three States

Every visual element exists in exactly one of three states:

| State | Color | Meaning |
|-------|-------|---------|
| **GOLD** | `#C9A962` | Healthy, working, connected properly |
| **PURPLE** | `#9B59B6` | Repair work needed OR underway (connected but inactive = needed; active = underway) |
| **BLUE** | `#1ABC9C` (teal) | Broken, disconnected, error state |

No other states. No gradients between states. Simple observation tells you what's working and what isn't.

---

## II. The Metaphor Mapping

### 2.1 Hierarchy

```
THE VOID (black canvas)
    └── FIEFDOM (subsystem directory, e.g., "P2P Messaging")
            └── BUILDING (single file, e.g., "messageHandler.ts")
                    ├── PANEL (utility interface showing all connections)
                    │       ├── Imports
                    │       ├── Exports  
                    │       ├── APIs
                    │       ├── Dependencies
                    │       └── Routines
                    │
                    └── ROOMS (interior spaces)
                            ├── Room = Logic block / Algorithm / Routine
                            └── THE SITTING ROOM (isolated workspace for focused editing)
```

### 2.2 Detailed Mapping

#### FIEFDOM = Subsystem Directory

- A fiefdom is a logical grouping: `src/modules/p2p/`, `src/auth/`, `src/llm/`
- Contains multiple buildings (files)
- Has a **MASTER PANEL** at its boundary showing connections to other fiefdoms
- Visually: A district or neighborhood of buildings

#### BUILDING = Single File

- One file = one building
- **Bigger file = bigger building** (more activity, more connections to showcase)
- Building size is proportional to file complexity/size
- Each building has:
  - Exterior (the Barradeau woven structure)
  - Panel (connection interface, visible from outside)
  - Interior rooms (accessible by clicking the door)

#### PANEL = File Interface

- Located on the building exterior
- Displays ALL file elements that "come or go":
  - Imports (what this file brings in)
  - Exports (what this file provides)
  - API endpoints (if applicable)
  - Dependencies (external packages)
  - Routines (callable functions)
- **Each connection point on the panel is gold, purple, or blue**
- If an import isn't connected → that connection point is blue
- If a connection is producing an error → blue

#### EDGES = Dynamic Connections

- **Edges are NOT pre-defined**
- Edges are rendered based on actual file activity
- An edge exists because a building USES something from another building
- Visual: Lines/threads connecting panels between buildings
- Edge color = health of that specific connection

#### ROOMS = Code Sections

- Interior of building contains rooms
- Each room = one logical block (function, algorithm, routine, class)
- Click building door → see all rooms
- Click room → contents transfer to THE SITTING ROOM

#### THE SITTING ROOM = Isolated Workspace

- When you want to work on a specific routine/algorithm
- Click the room → it becomes the focus
- **"The edges are perfectly clear"** — you know exactly what this code touches
- LLMs and humans work here in isolation
- Changes propagate back to the building when saved

### 2.3 Visual Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                           THE VOID                                   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              FIEFDOM: src/modules/p2p/                       │   │
│  │                                                              │   │
│  │    ┌─────────┐      ┌─────────────┐      ┌───────┐         │   │
│  │    │Building │──────│  Building   │──────│Building│         │   │
│  │    │ small   │      │   LARGE     │      │ medium │         │   │
│  │    │handler.ts      │connection.ts│      │types.ts│         │   │
│  │    │ [GOLD]  │      │  [BLUE]     │      │ [GOLD] │         │   │
│  │    └────┬────┘      └──────┬──────┘      └───┬────┘         │   │
│  │         │                  │                  │              │   │
│  │         └──────────────────┼──────────────────┘              │   │
│  │                            │                                  │   │
│  │                     ┌──────┴──────┐                          │   │
│  │                     │MASTER PANEL │                          │   │
│  │                     │ (to auth/)  │                          │   │
│  │                     │ (to core/)  │                          │   │
│  │                     └─────────────┘                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## III. Technical Specification

### 3.1 Building Generation (Barradeau Method)

Each file generates a building using the Barradeau woven technique:

```
INPUT:  File metadata
        - File size (bytes/lines) → Building footprint size
        - Number of exports → Building height
        - Number of imports → Panel complexity
        - Number of functions/routines → Number of rooms

OUTPUT: Barradeau particle structure
        - Points placed along Delaunay edges
        - Density inversely proportional to edge length
        - Vertical extrusion based on export count
        - Color determined by health state
```

**Building Size Formula:**
```
footprint_radius = BASE_SIZE + (file_lines / SCALE_FACTOR)
building_height = MIN_HEIGHT + (export_count * HEIGHT_PER_EXPORT)
particle_density = function(file_complexity)
```

### 3.2 Panel Data Structure

```typescript
interface BuildingPanel {
  fileId: string;
  filePath: string;
  
  connections: {
    imports: PanelConnection[];
    exports: PanelConnection[];
    apis: PanelConnection[];
    dependencies: PanelConnection[];
    routines: PanelConnection[];
  };
  
  overallHealth: 'gold' | 'purple' | 'blue';
}

interface PanelConnection {
  id: string;
  name: string;                    // e.g., "useState", "handleMessage"
  type: 'import' | 'export' | 'api' | 'dependency' | 'routine';
  target?: string;                 // What it connects to (if applicable)
  health: 'gold' | 'purple' | 'blue';
  position: { x: number, y: number }; // Position on panel
}
```

### 3.3 Room Data Structure

```typescript
interface BuildingRoom {
  id: string;
  name: string;                    // Function/class/routine name
  type: 'function' | 'class' | 'algorithm' | 'routine' | 'constant';
  lineStart: number;
  lineEnd: number;
  complexity: number;              // Cyclomatic complexity or similar
  connections: string[];           // IDs of panel connections this room uses
  health: 'gold' | 'purple' | 'blue';
}
```

### 3.4 Edge Rendering Rules

Edges are rendered dynamically based on actual relationships:

1. **Parse file** → Extract imports/exports
2. **Resolve targets** → Map import to exporting file's building
3. **Create edge** → Line from Panel Connection A to Panel Connection B
4. **Color edge** → Based on connection health (both endpoints must be gold for gold edge)
5. **Render** → Barradeau-style particle thread along edge path

**Edge Health Logic:**
```
IF source.health == 'gold' AND target.health == 'gold':
    edge.health = 'gold'
ELSE IF source.health == 'blue' OR target.health == 'blue':
    edge.health = 'blue'
ELSE:
    edge.health = 'purple'
```

### 3.5 Locked File Indicator

When a file is locked (e.g., by Louis in Orchestr8):

- **Gold padlock icon** appears at EACH connection point on the panel
- Padlock is visually distinct (solid, not particle-based)
- Indicates: "This connection cannot be modified right now"

---

## IV. User Interactions

### 4.1 Navigation

| Action | Result |
|--------|--------|
| **Pan/zoom the void** | Navigate between fiefdoms |
| **Click fiefdom** | Zoom into that district, see all buildings |
| **Click building** | See panel details, highlight connected buildings |
| **Click building door** | Enter interior, see all rooms |
| **Click room** | Open THE SITTING ROOM with that code isolated |
| **Right-click** | Context menu (depending on what's clicked) |

### 4.2 The Sitting Room

When a room is selected:

1. Void fades to background
2. Room contents appear in focused editor view
3. Panel shows ONLY the connections relevant to this room
4. User (human or LLM) can edit code
5. Save → propagates back to building
6. Building health recalculates
7. Edges update accordingly

### 4.3 Health Observation

The user observes health simply by looking:

- **See gold building** → It's working
- **See blue building** → It's broken, needs attention
- **See purple building** → Work is needed or happening
- **See blue connection on panel** → Specific connection is broken
- **See blue edge** → The link between two files is broken

No need to run diagnostics. Observation IS the diagnostic.

---

## V. Implementation Roadmap

### Phase 0: Foundation (CURRENT)
**Goal:** Nail the Barradeau visual style for buildings

| Task | Status | Notes |
|------|--------|-------|
| Implement Delaunay triangulation | ✅ Done | Working in barradeau-3d.html |
| Implement edge-based particle placement | ✅ Done | Barradeau technique correct |
| Implement density-by-edge-length | ✅ Done | Core insight implemented |
| Implement three-color system | 🔄 In Progress | Gold/Purple/Blue |
| Building size from file metadata | ⬜ Not Started | Footprint scaling |
| Single building renders correctly | ⬜ Not Started | End-to-end test |

**Exit Criteria:** One building renders from one file, sized correctly, colored by health state.

---

### Phase 1: The Panel
**Goal:** Buildings show their connection interfaces

| Task | Status | Notes |
|------|--------|-------|
| Parse file for imports/exports | ⬜ | TypeScript AST parsing |
| Generate panel layout | ⬜ | Position connections on building face |
| Render panel connections as nodes | ⬜ | Small particle clusters |
| Color connections by health | ⬜ | Gold/Purple/Blue per connection |
| Padlock indicator for locked files | ⬜ | Gold block icon |

**Exit Criteria:** Building panel shows all file connections, each colored by health.

---

### Phase 2: The Fiefdom
**Goal:** Multiple buildings in a district with edges

| Task | Status | Notes |
|------|--------|-------|
| Load all files in directory | ⬜ | File system scan |
| Generate building per file | ⬜ | Batch generation |
| Layout buildings in fiefdom | ⬜ | Spatial arrangement algorithm |
| Render edges between connected panels | ⬜ | Dynamic edge creation |
| Master panel at fiefdom boundary | ⬜ | Shows external connections |

**Exit Criteria:** One fiefdom renders with multiple buildings, edges showing relationships.

---

### Phase 3: The Rooms
**Goal:** Building interiors accessible

| Task | Status | Notes |
|------|--------|-------|
| Parse file for functions/classes | ⬜ | AST extraction |
| Generate room layout inside building | ⬜ | Interior space |
| Door interaction (click to enter) | ⬜ | Navigation |
| Room visualization | ⬜ | Show code block boundaries |
| Room-to-panel connection mapping | ⬜ | Which connections does this room use |

**Exit Criteria:** Can click building, see rooms, understand which connections each room uses.

---

### Phase 4: The Sitting Room
**Goal:** Isolated editing workspace

| Task | Status | Notes |
|------|--------|-------|
| Room selection → isolated view | ⬜ | Focus mode |
| Code editor integration | ⬜ | Monaco or similar |
| Relevant-connections-only panel | ⬜ | Filtered view |
| Save → propagate to building | ⬜ | Write-back |
| Health recalculation on save | ⬜ | Re-parse, re-color |

**Exit Criteria:** Can edit code in isolation, see changes reflected in building health.

---

### Phase 5: Multi-Fiefdom (The Void)
**Goal:** Navigate entire codebase

| Task | Status | Notes |
|------|--------|-------|
| Load all fiefdoms | ⬜ | Full project scan |
| Fiefdom-to-fiefdom edges | ⬜ | Master panel connections |
| Void navigation (pan/zoom) | ⬜ | Camera controls |
| Fiefdom health roll-up | ⬜ | District turns blue if any building is blue |

**Exit Criteria:** Full codebase visible as city, can navigate and observe health at any level.

---

### Phase 6: Orchestr8 Integration
**Goal:** Connect to agent coordination system

| Task | Status | Notes |
|------|--------|-------|
| Read CHECKPOINT.json | ⬜ | Current sprint state |
| Reflect agent deployment visually | ⬜ | Purple = agent working |
| Read FILE_LOCKS.json | ⬜ | Padlock indicators |
| Update on file system changes | ⬜ | Watch mode |
| Generate STATUS_REPORT visualization | ⬜ | For Emperor |

**Exit Criteria:** The Void IS the Orchestr8 dashboard.

---

### Future Phases (Post-MVP)

| Phase | Goal |
|-------|------|
| **Animations** | Breathing, particle drift, transition effects |
| **Building rotation** | Slow ambient rotation |
| **Agent visualization** | Show Scouts/Fixers/Validators as entities |
| **Map data integration** | OpenStreetMap for "keep it fresh" visual variety |
| **LOD system** | Level-of-detail for large codebases |
| **VR/AR mode** | Immersive navigation |

---

## VI. File Structure (Implementation)

```
src/
├── void/
│   ├── VoidCanvas.vue           # Main Three.js canvas
│   ├── VoidCamera.ts            # Navigation controls
│   └── VoidState.ts             # Global state (current focus, selection)
│
├── fiefdom/
│   ├── FiefdomLoader.ts         # Load directory → fiefdom data
│   ├── FiefdomLayout.ts         # Arrange buildings spatially
│   ├── FiefdomRenderer.ts       # Render fiefdom + master panel
│   └── MasterPanel.ts           # External connection interface
│
├── building/
│   ├── BuildingGenerator.ts     # File → Barradeau building
│   ├── BuildingPanel.ts         # Connection interface
│   ├── BuildingInterior.ts      # Rooms layout
│   └── BuildingRenderer.ts      # Three.js rendering
│
├── room/
│   ├── RoomParser.ts            # Extract functions/classes from file
│   ├── RoomLayout.ts            # Interior arrangement
│   └── SittingRoom.vue          # Isolated editing workspace
│
├── edge/
│   ├── EdgeResolver.ts          # Determine what connects to what
│   ├── EdgeRenderer.ts          # Barradeau-style edge threads
│   └── EdgeHealth.ts            # Calculate edge color
│
├── parser/
│   ├── TypeScriptParser.ts      # AST parsing for .ts/.tsx
│   ├── VueParser.ts             # SFC parsing for .vue
│   └── HealthChecker.ts         # Determine gold/purple/blue
│
└── barradeau/
    ├── Delaunay.ts              # Triangulation
    ├── ParticleSystem.ts        # CPU-based particles
    ├── WovenRenderer.ts         # Edge-based particle placement
    └── ColorSystem.ts           # Three-state color management
```

---

## VII. Open Questions

1. **Building layout algorithm** — How should buildings be arranged within a fiefdom? Grid? Force-directed? Organic clustering?

2. **Edge routing** — Should edges take straight paths or curve around buildings?

3. **Scale limits** — At what file count does this become unusable? 100 files? 1000?

4. **LLM integration method** — How exactly does an LLM "see" the dense pixels? Screenshot? Structured data export? Both?

5. **Real-time vs snapshot** — Does the visualization update in real-time as files change, or on explicit refresh?

---

## VIII. Success Criteria

The system succeeds when:

1. **Human looks at The Void** → Instantly knows which areas need attention (blue) vs working (gold)
2. **LLM analyzes The Void** → Can identify specific broken connections without reading code
3. **Developer clicks into Sitting Room** → Understands exactly what they're editing and what it touches
4. **Emperor reviews fiefdoms** → Sees entire codebase health at a glance
5. **General deploys to fiefdom** → Building turns purple, then gold when fixed

---

## IX. Signatures

**Pending Approval:**

- [ ] Ben (Human Emperor)
- [ ] Claude (Strategic Council)

---

*"The visualization IS the truth."*

---

**END SPEC + ROADMAP**

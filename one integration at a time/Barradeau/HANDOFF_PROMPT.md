# BRIEFING: THE VOID Codebase Visualization System

**Date:** 2026-01-28  
**Project:** stereOS / Orchestr8  
**Human:** Ben (Emperor)  
**Status:** Phase 0 COMPLETE — Ready for Phase 1

---

## I. CRITICAL CONTEXT (Read This First)

You are continuing work on **THE VOID**, a codebase visualization system that is part of **stereOS** (an internal development tool) and integrates with **Orchestr8** (a multi-agent coordination system for managing Claude Code instances across complex codebases).

**The core insight you must internalize:**

> The Barradeau visual aesthetic serves TWO audiences simultaneously:
> - **Humans** see an ethereal fantasy cityscape — intuitive, beautiful, "blue blob = problem"
> - **LLMs** see dense pixel grids with identifiable connection points — architectural issues immediately visible

This is the razor's edge. The visualization must be beautiful enough for humans to *want* to use it, while being data-dense enough for LLMs to extract actionable information. **Do not sacrifice one for the other.**

---

## II. THE METAPHOR (This Was Hard-Won — Do Not Deviate)

### Correct Mapping:

| Concept | Visual Representation | Notes |
|---------|----------------------|-------|
| **Fiefdom** | District/neighborhood | A subsystem directory (e.g., `src/modules/p2p/`) containing multiple buildings |
| **Building** | Single file | Bigger file = bigger building (more lines = larger footprint, more exports = taller) |
| **Panel** | Utility interface on building exterior | Shows ALL connections: imports, exports, APIs, dependencies, routines |
| **Rooms** | Interior spaces | Each room = one function/class/algorithm |
| **The Sitting Room** | Isolated editing workspace | Click a room → code isolated for focused editing |
| **Edges** | Dynamic connections between panels | NOT pre-defined; rendered from actual file relationships |
| **Town Square** | Scrolling panel in each fiefdom | node_modules, deps, .gitignore, config files — NOT buildings |

### The Three States (No Others):

| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| **GOLD** | Gold | `#C9A962` | Healthy, working, connected properly |
| **PURPLE** | Purple | `#9B59B6` | Repair needed OR underway |
| **BLUE** | Teal | `#1ABC9C` | Broken, disconnected, error |

### What Was REJECTED:

- ❌ Fiefdom = building (WRONG — fiefdom contains multiple buildings)
- ❌ File = particle cluster (WRONG — file = entire building)
- ❌ Pre-defined edges (WRONG — edges render from actual relationships)
- ❌ Red for errors (WRONG — blue indicates broken state)
- ❌ Animations in MVP (WRONG — roadmap item, not MVP)
- ❌ Complex state gradients (WRONG — three states only)

---

## III. WHAT PHASE 0 DELIVERED

A working HTML file (`void-phase0-buildings.html`) that demonstrates:

1. **Barradeau-style building generation** from file content
2. **File parsing** — extracts line count and export count
3. **Proportional sizing:**
   - `footprint = 2 + (lines × 0.008)`
   - `height = 3 + (exports × 0.8)`
4. **Two test buildings:**
   - Small: `utils.ts` (52 lines, 2 exports) → compact building
   - Large: `ConnectionManager.ts` (487 lines, 15 exports) → tall, wide building
5. **Barradeau technique correctly implemented:**
   - Delaunay triangulation of footprint
   - Particles placed along edges (not random)
   - Density inversely proportional to edge length
   - Higher layers filter out longer edges (ethereal fade)
6. **Gold color hardcoded** (health checking comes in Phase 1+)

**The visual quality matches Barradeau's reference images** — dense woven particles creating an ethereal architectural form.

---

## IV. DESIGN DECISIONS (Already Made — Do Not Revisit)

| Decision | MVP Answer | Roadmap |
|----------|------------|---------|
| Building layout | Grid | Organic/force-directed layouts |
| Edge routing | Straight lines | Intelligent physical routing |
| Scale limits | No limit (VS Code feeds data) | N/A |
| LLM integration | Whatever is easiest for LLM to see/actuate | Optimize based on results |
| Real-time vs snapshot | Match VS Code's behavior | Leverage existing debugging tools |

---

## V. THE ROADMAP (Where We Are)

### ✅ Phase 0: Foundation (COMPLETE)
- Barradeau visual style working
- Building scales from file metadata
- Single building renders correctly

### ⬜ Phase 1: The Panel (NEXT)
- Parse file for imports/exports/APIs/dependencies/routines
- Generate panel layout on building exterior
- Render panel connections as nodes
- Color each connection by health (gold/purple/blue)
- Padlock indicator for locked files (gold block icon)

**Exit Criteria:** Building panel shows all file connections, each colored by health.

### ⬜ Phase 2: The Fiefdom
- Load all files in directory
- Generate building per file
- Grid layout
- Render edges between connected panels
- Master panel at fiefdom boundary

### ⬜ Phase 3: The Rooms
- Parse file for functions/classes
- Interior room layout
- Door interaction (click to enter)
- Room-to-panel connection mapping

### ⬜ Phase 4: The Sitting Room
- Room selection → isolated view
- Code editor integration
- Save → propagate changes
- Health recalculation

### ⬜ Phase 5: Multi-Fiefdom (The Void)
- Full codebase navigation
- Fiefdom-to-fiefdom edges
- Pan/zoom controls

### ⬜ Phase 6: Orchestr8 Integration
- Read CHECKPOINT.json, FILE_LOCKS.json
- Reflect agent deployment visually
- The Void becomes the Orchestr8 dashboard

---

## VI. KEY FILES

| File | Location | Purpose |
|------|----------|---------|
| **Spec + Roadmap** | `VOID_SPEC_ROADMAP_v1.1.md` | Full specification and implementation plan |
| **Phase 0 Deliverable** | `void-phase0-buildings.html` | Working building generator |
| **Barradeau 2D Reference** | `barradeau-buildings.html` | Pure 2D canvas implementation |
| **Barradeau 3D Reference** | `barradeau-3d.html` | Three.js 3D adaptation |
| **Orchestr8 Roadmap** | `1_SOT.md` | The larger system this integrates with |

---

## VII. TECHNICAL NOTES

### Barradeau Technique (The Real One)

The magic is NOT random particles. It's:

1. **Points → Delaunay triangulation → edges with stored lengths**
2. **Render only edges where `length < threshold`**
3. **Small threshold = dense mesh (short edges only)**
4. **Large threshold = sparse mesh (all edges)**
5. **Stack vertically with decreasing opacity = "woven" illusion**

At higher layers, longer edges are filtered out first → structure fades into mist.

### File Parsing

Currently extracts:
- Line count (for footprint size)
- Export count (for building height)

Future phases need:
- Import statements (for panel connections)
- Function/class definitions (for rooms)
- API endpoints, dependencies, routines

### Three.js Stack

- Three.js r160
- OrbitControls
- EffectComposer + UnrealBloomPass
- Custom ShaderMaterial for particles
- Additive blending for glow effect

---

## VIII. BEN'S WORKING STYLE

From his user preferences and our conversation:

1. **"We don't mark things for later, we execute against them immediately"** — no stubs, no TODOs
2. **Refresh context at end of multi-step tasks** — always valuable as a guardrail
3. **Execution-first philosophy** — build it, don't just spec it
4. **Deep interest in efficient LLM orchestration** — "family unit" of specialized LLMs
5. **Appreciates when you "get it"** — he's been blocked on this concept for 24+ hours before our session
6. **stereOS aesthetic:** breathing 4s cycle, obsidian `#0A0A0B`, gold `#C9A962`, teal `#1ABC9C`, Futura actions, Avenir body

---

## IX. YOUR MISSION

If you are a fresh Claude instance picking this up:

1. **Read `VOID_SPEC_ROADMAP_v1.1.md`** — the full spec
2. **Open `void-phase0-buildings.html`** — see what Phase 0 looks like
3. **Confirm with Ben** which phase to execute next (likely Phase 1: The Panel)
4. **Execute immediately** — build working code, not specs

If Ben says "continue" or "next phase" without specifics, **execute Phase 1: The Panel**.

---

## X. PHASE 1 STARTER (If You're Executing Next)

The Panel needs to:

1. **Parse TypeScript/Vue files for:**
   ```typescript
   interface PanelConnection {
     id: string;
     name: string;                    // "useState", "handleMessage"
     type: 'import' | 'export' | 'api' | 'dependency' | 'routine';
     target?: string;                 // What it connects to
     health: 'gold' | 'purple' | 'blue';
     position: { x: number, y: number };
   }
   ```

2. **Render on building exterior** — connection points as small particle clusters or nodes

3. **Health determination logic:**
   - Import exists but target file missing → BLUE
   - Import exists, target exists, no errors → GOLD
   - Import being worked on by agent → PURPLE

4. **Locked file indicator** — gold padlock icon at connection points

Start by extending `void-phase0-buildings.html` to add panel data to the building, then render it.

---

## XI. FINAL NOTES

This project is the visual layer for a sophisticated multi-agent development system. The goal is:

> **Human looks at The Void → instantly knows what's broken**
> **LLM analyzes The Void → can identify specific broken connections without reading code**

The Barradeau aesthetic is not decoration — it's functional. Dense pixels hide structure from humans while revealing it to machines. That's the magic.

---

**Good luck. Build something beautiful.**

---

*"The visualization IS the truth."*

# Orchestr8 Master Roadmap

## Complete Sprint Plan

**Created:** 2026-01-30
**Status:** Active
**Source of Truth:** This document supersedes all other roadmap references

> 2026-02-15 checkpoint:
> Active execution authority for the transplant program is `.planning/orchestr8_next/` (PRDs P00-P06 with gate artifacts).
> `P05` and `P06` are complete/promoted; this document remains historical context for legacy wiring phases.

---

## Gap Analysis: GSD Roadmap vs SOT Documents

### Currently in GSD (Milestone 1: Phases 1-5)

| Phase | Topic | SOT Priority | Status |
|-------|-------|--------------|--------|
| 1 | Branding | P0 | ✅ Complete |
| 2 | Navigation | P1 | Pending |
| 3 | Health Integration | P2 | Pending |
| 4 | Briefing Data | P3 | Pending |
| 5 | Combat Cleanup | P6.2 | Pending |

### NOT in GSD (from WIRING_PLAN.md)

| Priority | Topic | Status |
|----------|-------|--------|
| P4 | State Synchronization (MissionManager) | → Phase 6 |
| P5.1 | Collabor8 panel wiring | → Phase 7 |
| P5.2 | Summon panel / Carl integration | → Phase 7 |
| P6.1 | Director thread disconnect | → Phase 9 |
| P7 | Platform documentation | → Phase 10 |
| P8 | Alias resolution config | → Phase 10 |

### NOT in GSD (from 14 Wiring Problems)

| # | Problem | Status |
|---|---------|--------|
| 2 | CarlContextualizer hollow | → Phase 8 |
| 3 | Generator phase persistence | → Phase 9 |
| 6 | Gatekeeper no rescan | → Phase 9 |
| 7 | Connie pandas fallback | → Phase 9 |

---

# MILESTONE 1: Core Wiring

## Phases 1-5 (In GSD)

### Phase 1: Branding ✅ COMPLETE

**Goal**: Replace all legacy brand references with "orchestr8"

**Completed:**

- Brand text in 06_maestro.py
- CSS class prefixes
- Comments and docstrings
- Application title

---

### Phase 2: Navigation

**Goal**: Top row buttons work correctly

**Tasks:**

1. `orchestr8` button → Returns to home state
2. `collabor8` button → Opens agent dropdown (slides LEFT)
3. `JFDI` button → Opens TicketPanel (slides RIGHT)
4. `gener8` button → Opens settings panel

**Success Criteria:**

- All four buttons functional
- Correct slide directions
- Active states visible

**Files:** `IP/plugins/06_maestro.py` (lines 892-920)

---

### Phase 3: Health Integration

**Goal**: HealthChecker influences Code City colors

**Tasks:**

1. Instantiate HealthChecker in 06_maestro.py
2. Pass health results to WovenMaps
3. Buildings show Gold/Blue/Purple based on health

**Success Criteria:**

- `health = HealthChecker(project_root)` exists
- Health data flows to Code City
- Color changes visible on file state change

**Files:** `IP/plugins/06_maestro.py`, `IP/health_checker.py`, `IP/woven_maps.py`

---

### Phase 4: Briefing Data

**Goal**: Campaign log parsing for briefing display

**Tasks:**

1. Parse existing campaign logs from `.orchestr8/campaigns/`
2. Display mission history in briefing panel
3. Link briefings to ticket IDs

**Success Criteria:**

- Historical missions visible
- Briefing panel populated with real data
- No placeholder text

**Files:** `IP/briefing_generator.py`, `IP/plugins/06_maestro.py`

---

### Phase 5: Combat Cleanup

**Goal**: Auto-cleanup of completed combat entries

**Tasks:**

1. Detect when General completes mission
2. Remove from active combat list
3. Archive to campaign log

**Success Criteria:**

- Completed missions auto-archive
- Combat tracker only shows active deployments
- No manual cleanup required

**Files:** `IP/combat_tracker.py`, `IP/plugins/06_maestro.py`

---

# MILESTONE 2: Full Integration

## Phases 6-10

### GSD Handoff Prompt

```
# Orchestr8 Milestone 2: Full Integration

## Context

Milestone 1 (Phases 1-5) completed the core wiring:
- ✅ Branding (orchestr8)
- ✅ Navigation (top row buttons)
- ✅ Health Integration (HealthChecker)
- ✅ Briefing Data (campaign log parsing)
- ✅ Combat Cleanup (auto-cleanup)

Milestone 2 addresses the remaining integration gaps identified in `SOT/WIRING_PLAN.md` and the 14 wiring problems in `SOT/CURRENT_STATE.md`.

## Source of Truth Documents

Read these before planning:
- `SOT/WIRING_PLAN.md` - Priorities P4-P8 not yet addressed
- `SOT/CURRENT_STATE.md` - Section IV: 14 Known Wiring Problems (#2, #3, #6, #7)
- `SOT/UI_SPECIFICATION.md` - Panel behavior specs
```

---

### Phase 6: State Synchronization

**Goal**: Unified mission flow linking Tickets, Combat, and Briefings

**Problem**: Currently three separate systems track the same mission. Creating a ticket doesn't link to combat deployment or campaign logging.

**Solution**: Create `MissionManager` class in `IP/mission_manager.py`:

```python
class MissionManager:
    def start_mission(fiefdom, ticket_id) -> creates briefing, marks combat, links ticket
    def complete_mission(fiefdom, success) -> updates ticket, clears combat, logs to campaign
```

**Success Criteria:**

- [ ] Deploying a General creates linked ticket + briefing + combat entry
- [ ] Completing mission updates all three systems atomically
- [ ] Campaign log shows mission history with ticket references

**Files:** New `IP/mission_manager.py`, update `IP/plugins/06_maestro.py`

---

### Phase 7: Panel Completion

**Goal**: Replace remaining placeholder panels with real functionality

**Problem**: Collabor8 and Summon panels show "coming soon" text instead of actual features.

**Tasks:**

1. **Collabor8 Panel** (Lines 1037-1057 in 06_maestro.py)
   - Wire to agent definitions from `Agent Deployment Strategy/`
   - Show available agents: Scout, Fixer, Validator, Git Agent
   - Allow agent selection for deployment

2. **Summon Panel** (Lines 1081-1095 in 06_maestro.py)
   - Wire to CarlContextualizer from `IP/carl_core.py`
   - Implement global search across codebase
   - Show search results with file links

**Success Criteria:**

- [ ] Collabor8 panel shows real agent list (not placeholder)
- [ ] Summon panel performs actual search via Carl
- [ ] No "coming soon" text remains in any panel

**Files:** `IP/plugins/06_maestro.py`, `IP/carl_core.py`

---

### Phase 8: Carl Integration

**Goal**: CarlContextualizer actively influences application state

**Problem**: Carl exists but only dumps JSON. It doesn't influence what the UI shows or what context gets passed to Generals.

**Tasks:**

1. Wire Carl to Summon/Search functionality
2. Use Carl for context gathering in briefing generation
3. Carl provides file relationships for Code City edges

**Success Criteria:**

- [ ] Search uses Carl's `gather_context()` method
- [ ] Briefings include Carl's context analysis
- [ ] Code City edges reflect actual import relationships from Carl

**Files:** `IP/carl_core.py`, `IP/briefing_generator.py`, `IP/plugins/06_maestro.py`

---

### Phase 9: Plugin Hardening

**Goal**: Fix fragile plugin behaviors

**Problems** (from 14 Wiring Problems):

- #3: Generator phase locking not persisted across sessions
- #6: Gatekeeper can't remove folders, no auto-refresh
- #7: Connie assumes pandas exists (crashes without it)
- #8: Director background thread doesn't trigger UI refresh

**Tasks:**

| Plugin | File | Fix |
|--------|------|-----|
| Generator | `01_generator.py` | Persist phase state to `.orchestr8/generator_state.json` |
| Gatekeeper | `03_gatekeeper.py` | Add remove folder, add refresh button |
| Connie | `04_connie_ui.py` | Graceful fallback when pandas missing |
| Director | `08_director.py` | Use Marimo polling or file-based signaling |

**Success Criteria:**

- [ ] Generator remembers phase after page refresh
- [ ] Gatekeeper can remove watched folders
- [ ] Connie works without pandas (degraded mode)
- [ ] Director updates visible without manual refresh

**Files:** All plugin files listed above

---

### Phase 10: Platform & Configuration

**Goal**: Make platform-specific behaviors configurable

**Problems:**

- Hardcoded `gnome-terminal` (has fallbacks, but not configurable)
- Hardcoded `npm run typecheck` (works for TS, but not all projects)
- Alias resolution assumes `@/` → `src/`

**Tasks:**

Add to `orchestr8_settings.toml`:

```toml
[platform]
terminal = "auto"  # or "gnome-terminal", "xterm", etc.

[health_check]
command = "npm run typecheck"  # or "mypy .", "ruff check", etc.

[paths]
alias_mappings = { "@" = "src" }
```

**Implementation:**

1. Update `IP/terminal_spawner.py` to read from settings
2. Update `IP/health_checker.py` to read from settings
3. Update `IP/connection_verifier.py` for configurable aliases

**Success Criteria:**

- [ ] Terminal preference configurable in settings
- [ ] Health check command configurable per-project
- [ ] Path aliases configurable for non-standard projects

**Files:** `orchestr8_settings.toml`, spawner, health_checker, connection_verifier

---

### Milestone 2 GSD Commands

```bash
/gsd:new-milestone "Full Integration"
/gsd:add-phase "State Synchronization - MissionManager linking Tickets/Combat/Briefings"
/gsd:add-phase "Panel Completion - Wire Collabor8 and Summon panels"
/gsd:add-phase "Carl Integration - Context gathering influences app state"
/gsd:add-phase "Plugin Hardening - Generator persistence, Gatekeeper refresh, Connie fallback, Director polling"
/gsd:add-phase "Platform Configuration - Settings-driven terminal, health check, and alias resolution"
```

Execute:

```bash
/gsd:plan-phase 6
/gsd:execute-phase 6
... repeat for 7-10 ...
/gsd:verify-work
/gsd:complete-milestone "2.0.0"
```

---

### Milestone 2 Validation Checklist

- [ ] MissionManager coordinates ticket/combat/briefing flow
- [ ] Collabor8 panel shows real agents
- [ ] Summon panel searches via Carl
- [ ] Carl context appears in briefings
- [ ] Generator remembers phase state
- [ ] Gatekeeper can remove folders
- [ ] Connie works without pandas
- [ ] Director updates without manual refresh
- [ ] Terminal preference in settings works
- [ ] Health check command configurable
- [ ] Path aliases configurable
- [ ] `marimo run orchestr8.py` runs clean with all features working

---

# MILESTONE 3: Code City 3D

## Phases 11-15 (Barradeau Integration)

### GSD Handoff Prompt

```
# Orchestr8 Milestone 3: Code City 3D

## Context

Milestones 1-2 completed core wiring and integration.
Milestone 3 transforms Code City from 2D canvas to 3D Barradeau particle visualization.

## Source of Truth Documents

Read these before planning:
- `SOT/BARRADEAU_INTEGRATION.md` - Complete integration strategy
- `SOT/UI_SPECIFICATION.md` - Control panel button specs
- `one integration at a time/Barradeau/` - HTML prototypes to extract from
```

---

### Phase 11: Building Generator

**Goal**: Extract and integrate BarradeauBuilding class

**Source:** `one integration at a time/Barradeau/void-phase0-buildings.html`

**Building Size Formula:**

```javascript
footprint_radius = 2 + (file_lines * 0.008)
building_height = 3 + (export_count * 0.8)
particles_per_unit = 1.2
layer_count = 15
taper = 0.015
```

**Tasks:**

1. Extract `BarradeauBuilding` class to `IP/woven_maps_3d.js`
2. Extract `Delaunay` triangulation logic
3. Create Python → JSON → Three.js data pipeline
4. Integrate with existing `woven_maps.py` code metrics

**Success Criteria:**

- [ ] Buildings render with correct footprint/height from code metrics
- [ ] Particle density matches layer_count setting
- [ ] Multiple buildings can coexist in scene

**Files:** New `IP/woven_maps_3d.js`, `IP/barradeau_builder.js`

---

### Phase 12: Edge Filter Shader

**Goal**: Implement Barradeau edge filter for particle visibility

**Source:** `one integration at a time/Barradeau/zsphere.html`

**Core Shader:**

```glsl
// Vertex Shader
attribute vec3 neighbor;
uniform float uThreshold;

void main() {
    float edgeLen = distance(position, neighbor);
    float alpha = 1.0 - smoothstep(uThreshold, uThreshold + 0.5, edgeLen);
    vAlpha = alpha;
}
```

**Tasks:**

1. Create `IP/shaders/barradeau.vert` and `barradeau.frag`
2. Add `densit8` slider to control panel (threshold 0.5-3.0)
3. Wire slider to `uThreshold` uniform

**Success Criteria:**

- [ ] Edge filter shader compiles and runs
- [ ] Density slider adjusts particle visibility in real-time
- [ ] Lower threshold = more detail, higher = sparse structure

**Files:** New `IP/shaders/`, update control panel in `IP/woven_maps.py`

---

### Phase 13: Three-Color Health System

**Goal**: Buildings change color based on health state

**Color System:**

| State | Color | Hex | Trigger |
|-------|-------|-----|---------|
| Working | Gold | #D4AF37 | Tests pass |
| Broken | Blue | #1fbdea | Tests fail |
| Combat | Purple | #9D4EDD | Active LLM deployment |

**Tasks:**

1. Wire HealthChecker results to building colors
2. Implement color transition animation (not instant swap)
3. Add color state buttons to control panel (filter by state)

**Success Criteria:**

- [ ] Buildings reflect actual health state
- [ ] Color transitions smoothly (0.5s)
- [ ] Gold/Teal/Purple filter buttons work

**Files:** `IP/woven_maps_3d.js`, `IP/health_checker.py`

---

### Phase 14: Dive-to-Building Interaction

**Goal**: Click building → camera dives to it → shows details

**Existing Pattern** (woven_maps.py:1891-1912):

```javascript
canvas.addEventListener('click', (e) => {
    type: 'WOVEN_MAPS_NODE_CLICK',
    // Opens file details
});
```

**Enhancement:**

```javascript
function diveToBuilding(building) {
    const targetPosition = building.position.clone();
    targetPosition.z += building.height * 1.5;

    gsap.to(camera.position, {
        x: targetPosition.x,
        y: targetPosition.y + 5,
        z: targetPosition.z,
        duration: 1.2,
        ease: "power2.inOut"
    });

    controls.target.copy(building.position);
    showBuildingDetails(building.metadata);
}
```

**Tasks:**

1. Add raycasting for 3D building selection
2. Implement smooth camera dive animation
3. Show building details panel on selection
4. Add `focus8` button to dive to selected building

**Success Criteria:**

- [ ] Click on building highlights it
- [ ] Camera smoothly dives to building
- [ ] Building details (file path, lines, exports, health) visible
- [ ] `focus8` button works with keyboard shortcut

**Files:** `IP/woven_maps_3d.js`, update control panel

---

### Phase 15: Real-Time Socket.io Integration

**Goal**: Carl health changes broadcast to Code City in real-time

**Architecture:**

```
Carl Health Monitor → Socket.io Broadcast → Code City Color Update
```

**Tasks:**

1. Add Socket.io server to orchestr8.py
2. Carl emits health change events
3. Code City listens and updates building colors
4. No page refresh required

**Success Criteria:**

- [ ] Health change in file → building color updates within 2s
- [ ] No manual refresh needed
- [ ] Multiple browser tabs stay in sync

**Files:** `orchestr8.py`, `IP/carl_core.py`, `IP/woven_maps_3d.js`

---

### Phase 15b: Control Panel Completion

**Goal**: All new buttons functional in bottom 5th

**New Buttons:**

| Button | Label | Action |
|--------|-------|--------|
| Density | `densit8` | Slider: Barradeau threshold |
| Dock | `dock8` | Toggle panel docked/floating |
| Overview | `orbit8` | Auto-rotate overview mode |
| Focus | `focus8` | Dive to selected building |
| Pulse | `pulse8` | Toggle breathing animation |
| Layer | `layer8` | Cycle layer visibility |

**Layout:**

```
┌─────────────────────────────────────────────────────────────────┐
│ [Gold] [Teal] [Purple]  │  [1][2][3][4]  │  [🔊]  │  [densit8] │
├─────────────────────────────────────────────────────────────────┤
│ [Re-Emerge] [Clear] [dock8] [orbit8] [focus8] [pulse8] [layer8] │
└─────────────────────────────────────────────────────────────────┘
```

**Success Criteria:**

- [ ] All buttons render correctly
- [ ] Each button performs its action
- [ ] Keyboard shortcuts for frequent actions

**Files:** `IP/woven_maps.py` control panel section

---

### Milestone 3 GSD Commands

```bash
/gsd:new-milestone "Code City 3D"
/gsd:add-phase "Building Generator - Extract BarradeauBuilding class"
/gsd:add-phase "Edge Filter Shader - Implement density-based visibility"
/gsd:add-phase "Three-Color Health - Wire health state to building colors"
/gsd:add-phase "Dive-to-Building - Click interaction with camera animation"
/gsd:add-phase "Socket.io Real-Time - Carl broadcasts health changes"
/gsd:add-phase "Control Panel Completion - All new buttons functional"
```

---

### Milestone 3 Validation Checklist

- [ ] Buildings render with correct size from code metrics
- [ ] Barradeau edge filter shader working
- [ ] Density slider adjusts particle visibility
- [ ] Three-color system reflects health state
- [ ] Click building → camera dives to it
- [ ] Building details panel shows on selection
- [ ] Socket.io broadcasts health changes
- [ ] Buildings update color without refresh
- [ ] All control panel buttons functional
- [ ] `marimo run orchestr8.py` shows 3D Code City

---

# MILESTONE 4: Later Roadmap

## Phases 16+ (Post-MVP)

These items are documented for future planning but not prioritized:

### Phase 16: Audio Reactivity

**Goal**: LLM conversations drive particle animation

```javascript
compute.simMaterial.uniforms.uAudioBass.value = uBass;
compute.simMaterial.uniforms.uAudioTreble.value = uTreble;
```

- Buildings pulse/breathe with voice input
- Combat mode has distinct audio signature

---

### Phase 17: Canvas Fallback

**Goal**: 2D canvas version for compatibility

- Zero-dependency mode (no Three.js)
- From `v4.html` prototype
- Auto-detect GPU capability, fallback to canvas

---

### Phase 18: GPGPU Particle Scale

**Goal**: 1M+ particle support

- GPU compute shaders for particle physics
- Data textures for structure mapping
- From `Architect.txt` patterns

---

### Phase 19: Global Stylization Control Plane

**Goal**: Make global UI behavior and styling switchable from a single desktop-friendly slider/toggle surface.

- Add a "Stylize" control panel with global toggles (fonts, motion mode, contrast, panel density, interaction pacing).
- Guarantee toggle changes propagate to all active surfaces without manual per-component edits.
- Provide preset packs and a "quick revert to canon" option for safe experimentation.
- Ensure settings persistence and instant visual application in `orchestr8.py` runtime.

---

# Summary: Complete Phase List

| Milestone | Phase | Name | Status |
|-----------|-------|------|--------|
| **1** | 1 | Branding | ✅ Complete |
| | 2 | Navigation | Pending |
| | 3 | Health Integration | Pending |
| | 4 | Briefing Data | Pending |
| | 5 | Combat Cleanup | Pending |
| **2** | 6 | State Synchronization | Planned |
| | 7 | Panel Completion | Planned |
| | 8 | Carl Integration | Planned |
| | 9 | Plugin Hardening | Planned |
| | 10 | Platform Configuration | Planned |
| **3** | 11 | Building Generator | Planned |
| | 12 | Edge Filter Shader | Planned |
| | 13 | Three-Color Health | Planned |
| | 14 | Dive-to-Building | Planned |
| | 15 | Socket.io Real-Time | Planned |
| | 15b | Control Panel Completion | Planned |
| **4** | 16 | Audio Reactivity | Later |
| | 17 | Canvas Fallback | Later |
| | 18 | GPGPU Particle Scale | Later |
| | 19 | Global Stylization Control Plane | Later |

---

**Total Phases:** 19
**Active Milestones:** 3
**Later Roadmap:** 1 milestone (4 phases)

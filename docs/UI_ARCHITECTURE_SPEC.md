# Orchestr8 UI Architecture Specification

**Created:** 2026-01-26  
**Status:** EMPEROR APPROVED  
**Reference:** maestroview.vue (canonical source)  
**Scope:** Complete UI interaction and feedback specification

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Layer 0: The Code Map](#layer-0-the-code-map)
3. [Layer 1: Top Panel (Mission Drop-Down)](#layer-1-top-panel-mission-drop-down)
4. [Layer 2: Bottom Panel (Human Ghetto)](#layer-2-bottom-panel-human-ghetto)
5. [Layer 3: Right Slider (JFDI Tickets)](#layer-3-right-slider-jfdi-tickets)
6. [Layer 4: Left Slider (SYSTEM)](#layer-4-left-slider-system)
7. [Layer 5: Settings (Waves)](#layer-5-settings-waves)
8. [Public Services (Memory Persistence)](#public-services-memory-persistence)
9. [Color System](#color-system)
10. [Animation Specifications](#animation-specifications)
11. [888 Skills Integration](#888-skills-integration)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  [Button 1]        [Button 2]        [Button 3]      [Waves]   │  ← Top Bar
├─────────────────────────────────────────────────────────────────┤
│                                                           │ J │
│                                                           │ F │
│                                                           │ D │
│                    THE CODE MAP                           │ I │
│              (Woven Maps Metropolis)                      │   │
│                                                           │ T │
│         Gold = Working    Blue = Broken                   │ I │
│                Purple = Combat                            │ C │
│                                                           │ K │
│                                                           │ E │
│                                                           │ T │
│                                                           │ S │
├─────────────────────────────────────────────────────────────────┤
│  [File] [Terminal] [Notepad] [___]  (m)  [___] [___] [___] [___]│  ← Bottom 5th
└─────────────────────────────────────────────────────────────────┘
                                 ↑
                            maestro
```

**Five Interaction Layers:**
1. **Code Map** - Central canvas (Woven Maps visualization)
2. **Top Panel** - Drops on blue-spot click (General assignment)
3. **Bottom Panel** - maestro + programmable button grid
4. **Right Slider** - JFDI button → Tickets
5. **Settings** - Waves icon

---

## 2. Layer 0: The Code Map

### Rendering Pipeline

```
Step 1: Source Material
├── Real cityscapes from around the world
└── 2D images as base reference

Step 2: 2D→3D Conversion
├── Convert cityscapes to 3D topography
└── Tool: [TBD - depth estimation / photogrammetry]

Step 3: Topographical Mold
├── Single color (contextually "invisible")
├── Visible to rendering bus only
└── Forms the terrain base

Step 4: Mesh Draping
├── Woven Maps style meshes
├── Delaunay triangulation
└── Gradient-based coloring

Step 5: Mermaid Underlay
├── Mermaid diagram drives proportions
├── District sizes = module complexity
└── Building sizes = file/component weight

Step 6: Dynamic Focus
├── Complexity weighting shifts dimensions
└── Point of interest moves toward viewer
└── Priority areas (LLMs, DBs) grow larger
```

### Visual States

| State | Color | Meaning | Interaction |
|-------|-------|---------|-------------|
| **Working** | Gold (#D4AF37) | Healthy code | Hover for details |
| **Broken** | Blue (#1fbdea) | Errors present | Click to zoom in |
| **Combat** | Purple (#9D4EDD) | Active debugging | Shows activity |

### Blue Spot Behavior

When code is broken:
1. Building/district turns blue
2. Errors float up like pollution (text particles)
3. Errors are easily legible
4. Examples:
   - `2 x Imports!? [fn]`
   - `"I'm lonely" - PrdGenerator` (no connections)

### Click Interaction

```
User clicks blue spot
    ↓
Camera "sucks into" that neighborhood
    ↓ synchronized with
Top Panel drops down
    ↓
Arrival = Panel fully deployed
```

---

## 3. Layer 1: Top Panel (Mission Drop-Down)

### Trigger

- **Activated by:** Clicking a blue spot on Code Map
- **Animation:** Synchronized with zoom - panel drops as you travel

### State: No General Present

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                   "House a Digital Native?"                     │
│                                                                 │
│    [Anthropic]  [OpenAI]  [OpenRouter]  [x.AI]  [OpenCode]     │
│    [Groq]  [Perplexity]  [Google]  [Mistral]  [Cerebras]       │
│    [Deepseek]  [Minimax]  [HuggingFace]  [Ollama]              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

- Shows providers configured in settings/toml
- User picks one → General "moves in"
- Sign goes up on building

### State: General Present (The Sign)

```
┌─────────────────────────────────────────────────────────────────┐
│  [General: claude-sonnet-4-20250514]              [Building: auth/]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SYSTEM: Error in auth/validator.py:42                         │
│  > ImportError: cannot import 'jwt_decode' from 'utils'        │
│  > Stack trace: ...                                            │
│                                                                 │
│  HUMAN: please check the whole directory, every time we        │
│  move something, something else breaks                          │
│                                                                 │
│  LLM: Analyzing auth/ directory structure...                   │
│  Found 3 circular import patterns:                             │
│  1. validator.py → utils.py → validator.py                     │
│  2. ...                                                        │
│                                                                 │
│  ────────────────────────────────────────────────────────────  │
│  [Type message...]                              [Send]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Features:**
- Infinite scroll for problem history
- Big up close (like small chat window)
- Three participants: Human, LLM, System
- Human gives direction
- LLM follows lead, contextualizes
- Loop until resolved

### On Resolution

```
Problem Solved
    ↓
Ship to Public Services
    ↓
├── SQLite (persistent storage)
├── Vector DB (semantic search)
└── Knowledge Graph (relationships)
    ↓
Future errors in neighborhood surface this content
```

---

## 4. Layer 2: Bottom Panel (Human Ghetto)

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ [File] [Term] [Note] [___]    (m)    [___] [___] [___] [Camp]  │
└─────────────────────────────────────────────────────────────────┘
   ↑                             ↑                           ↑
   Left Grid                 maestro                    Right Grid
```

### maestro (Center)

**The (m) Logo - 3 States:**

| State | Color | Behavior |
|-------|-------|----------|
| **OFF** | Blue (#1fbdea) | Inactive, no agency |
| **OBSERVE** | Dark Gold (#B8960C) | Planning mode, @ mentions only |
| **ON** | Bright Gold (#D4AF37) | Tier 2 access (full agency) |

**Click to cycle:** OFF → OBSERVE → ON → OFF

**OBSERVE Mode:**
- Like planning/read-only
- Can @ maestro (or any LLM) for explicit questions
- They answer/act on that explicit thing only

**ON Mode:**
- Tier 2 access (Standard)
- Full agency within tier restrictions
- Only computer owner has Tier 1 (nuke capability)

### Programmable Button Grid

**Left Side (confirmed):**
| Button | Source | Function |
|--------|--------|----------|
| **File** | stereOS File Explorer | Browse project files |
| **Term** | actu8 | Terminal interface |
| **Note** | Notepad | Quick notes |
| **[___]** | TBD | Open slot |

**Right Side (confirmed):**
| Button | Function |
|--------|----------|
| **[___]** | Open slot |
| **[___]** | Open slot |
| **[___]** | Open slot |
| **Camp** | Campaign/Sprint tracker |

### Campaign Button

- Ties to selected sprints
- Track progress across features
- On release/finish:
  - → Public Services Sprint Department
  - → Added to vector/graph memory
  - → Aids future development

---

## 5. Layer 3: Right Slider (JFDI Tickets)

### Trigger

- **Activated by:** JFDI button (top bar, Button 2?)
- **Animation:** Slides in from right

### Contents

```
┌──────────────────────┐
│  JFDI TICKETS        │
├──────────────────────┤
│  ▼ ACTIVE            │
│  ┌────────────────┐  │
│  │ #42 Auth Fix   │  │
│  │ Blue: auth/    │  │
│  │ Assigned: BP   │  │
│  └────────────────┘  │
│                      │
│  ▼ QUEUED            │
│  ┌────────────────┐  │
│  │ #43 DB Migrate │  │
│  │ Priority: High │  │
│  └────────────────┘  │
│                      │
│  ▼ RESOLVED          │
│  └── View Archive    │
│                      │
└──────────────────────┘
```

**Ticket Auto-Population:**
- Triggers on: Warnings, Errors, Test failures, Blue spots
- Contains: ALL data on that circuit
  - Error message(s)
  - Stack trace
  - Related file paths
  - Recent changes
  - Dependencies (upstream/downstream)
  - Last successful state
  - Related history
  - Suggested diagnostics

---

## 6. Layer 4: Left Slider (SYSTEM)

### Trigger

- **Activated by:** Button 1 (top bar)
- **Animation:** Slides in from left

### Contents: System State Macros

```
┌──────────────────────┐
│  SYSTEM              │
├──────────────────────┤
│  ▼ ENVIRONMENTS      │
│  ┌────────────────┐  │
│  │ [●] venv-main  │  │
│  │ [ ] venv-test  │  │
│  │ [ ] conda-ml   │  │
│  │ [+ New Env]    │  │
│  └────────────────┘  │
│                      │
│  ▼ HARDWARE          │
│  │ CPU: 34% ████░░░ │
│  │ RAM: 12GB/32GB   │
│  │ GPU: 2% █░░░░░░  │
│  │ [Adjust...]      │
│                      │
│  ▼ BROWSER           │
│  │ [Research Mode]  │
│  │ [Testing Mode]   │
│  │ [Preview App]    │
│                      │
│  ▼ MACROS            │
│  │ [Dev Setup]      │
│  │ [Build All]      │
│  │ [Clean Cache]    │
│  │ [+ New Macro]    │
│                      │
└──────────────────────┘
```

**Features:**
- **Environments:** Activate/deactivate venvs, conda, nvm, etc.
- **Hardware:** Monitor system resources, adjust settings
- **Browser:** Launch browser in different modes (research, testing, preview)
- **Macros:** Programmable system state shortcuts

---

## 7. Layer 5: Settings (Waves)

### Trigger

- **Activated by:** Waves icon (top bar, right side)

### Contents

```
┌─────────────────────────────────────────┐
│  SETTINGS                        [X]    │
├─────────────────────────────────────────┤
│                                         │
│  ▼ LLM PROVIDERS                        │
│  ┌─────────────────────────────────┐    │
│  │ Anthropic    [API Key] [✓]     │    │
│  │ OpenAI       [API Key] [✓]     │    │
│  │ OpenRouter   [API Key] [✓]     │    │
│  │ ...                            │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ▼ MODEL PREFERENCES                    │
│  │ Chat: [claude-sonnet-4-20250514 ▼]        │
│  │ Edit: [claude-sonnet-4-20250514 ▼]        │
│  │ Autocomplete: [ollama/codellama ▼]│
│                                         │
│  ▼ BUTTON GRID LAYOUT                   │
│  │ [Customize programmable buttons]     │
│                                         │
│  ▼ APPEARANCE                           │
│  │ Theme: [Void Dark ▼]                 │
│  │ Animations: [✓] Enabled              │
│                                         │
└─────────────────────────────────────────┘
```

---

## 8. Public Services (Memory Persistence)

### Architecture

```
Problem Resolution
        ↓
┌───────────────────────────────────────────┐
│           PUBLIC SERVICES                 │
├───────────────────────────────────────────┤
│                                           │
│  ┌─────────────┐                          │
│  │   SQLite    │ ← Persistent storage     │
│  │  (tickets)  │   Full conversation      │
│  └─────────────┘   history                │
│         ↓                                 │
│  ┌─────────────┐                          │
│  │  Vector DB  │ ← Semantic search        │
│  │ (embeddings)│   "Similar problems"     │
│  └─────────────┘                          │
│         ↓                                 │
│  ┌─────────────┐                          │
│  │  Knowledge  │ ← Relationship mapping   │
│  │    Graph    │   "This affects that"    │
│  └─────────────┘                          │
│                                           │
└───────────────────────────────────────────┘
```

### Living Memory Benefit

```
Future error in same neighborhood
        ↓
System checks Public Services
        ↓
Surfaces relevant past resolutions
        ↓
Shorter build times for new features
```

---

## 9. Color System

From maestroview.vue:

```css
:root {
  /* Status Colors */
  --gold-metallic: #D4AF37;    /* Working / ON */
  --gold-dark: #B8960C;        /* OBSERVE mode */
  --blue-dominant: #1fbdea;    /* Broken / OFF */
  --purple-combat: #9D4EDD;    /* Combat / Active debug */
  
  /* Background (The Void) */
  --bg-primary: #0A0A0B;
  --bg-elevated: #121214;
  --bg-surface: #1A1A1C;
  
  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #A0A0A0;
  --text-muted: #666666;
}
```

---

## 10. Animation Specifications

### Emergence Animations (from catalog)

| Trigger | Animation | Duration |
|---------|-----------|----------|
| Panel drop | emerge-void | 0.4s |
| Zoom into neighborhood | camera-suck | 0.6s |
| Error float up | pollution-rise | 2.0s loop |
| General moves in | materialize | 0.5s |
| Resolution ship | package-send | 0.3s |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 11. 888 Skills Integration

### Available Skills (from stereOS)

| Directory | Skills | Button Candidates |
|-----------|--------|-------------------|
| **director/** | OODA, Pattern Recognition, Predictive, Workflow Optimizer | Campaign insights |
| **senses/** | Speech, Gesture, Multimodal Fusion, Spell Manager | Voice commands |
| **actu8/** | Terminal adapter | Terminal button (confirmed) |
| **cre8/** | Creator/generator | Code generation |
| **communic8/** | Communication | Notifications |
| **integr8/** | Integration | External services |
| **innov8/** | Innovation | Experimental features |
| **panel_foundation/** | Base panel, Registry | UI infrastructure |

### Integration Priority

1. **actu8** - Terminal (confirmed for button grid)
2. **panel_foundation** - UI base infrastructure
3. **director/ooda_engine** - Decision loop integration
4. **senses/** - Future: voice/gesture control

---

## Implementation Phases

### Phase 1: Foundation
- [ ] Bottom panel with maestro + button grid
- [ ] Basic Code Map (Mermaid-driven, flat visualization)
- [ ] Settings panel (providers, keys)

### Phase 2: Interaction
- [ ] Blue spot click → top panel drop
- [ ] General assignment flow
- [ ] Chat interface in top panel

### Phase 3: Persistence
- [ ] SQLite ticket storage
- [ ] Vector embedding pipeline
- [ ] Knowledge graph structure

### Phase 4: Advanced Visualization
- [ ] 2D→3D cityscape conversion
- [ ] Mesh draping
- [ ] Error pollution particles

### Phase 5: Living Memory
- [ ] Past resolution surfacing
- [ ] Campaign/sprint memory
- [ ] Cross-project learning

---

**END SPECIFICATION**

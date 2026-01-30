# ORCHESTR8 STATUS REPORT: Cross-Instance Handoff Document

**Date:** 2026-01-26
**Purpose:** Enable coordination between Claude instances via "dead drop" pattern
**Intended Reader:** Another Claude Code instance providing feedback

---

## Executive Summary

Orchestr8 is a **Marimo-based command center** for codebase management. We're now integrating the spatial UI patterns from `MaestroView.vue` (stereOS) to evolve it from a tab-based dashboard into a **unified orchestration interface** for managing multiple Claude Code instances working on a codebase.

**The Core Insight:** MaestroView's "Void" + emergence panels provide the perfect canvas for visualizing:
1. The **Connection Graph** (codebase topology)
2. **Agent Deployment** (Emperor/General/Fiefdom pattern)
3. **Real-time Status** (via filesystem-based "dead drops")

---

## Part 1: What Has Been Built

### 1.1 The Marimo Application (`IP/orchestr8_app.py`)

A reactive Python notebook with **dynamic plugin architecture**:

```python
STATE_MANAGERS = {
    "root": (get_root, set_root),      # Project path
    "files": (get_files, set_files),    # DataFrame of files
    "selected": (get_selected, set_selected),  # Current file
    "logs": (get_logs, set_logs)        # Event log
}

# Plugins render via: module.render(STATE_MANAGERS)
```

**Plugin Loader Pattern:**
1. Scans `IP/plugins/*.py`
2. Imports dynamically via `importlib`
3. Reads `PLUGIN_NAME`, `PLUGIN_ORDER`
4. Builds `mo.ui.tabs` from plugin renders

### 1.2 Current Plugin Inventory

| Plugin | Purpose | Status |
|--------|---------|--------|
| `00_welcome.py` | Landing page | Working |
| `01_generator.py` | 7-Phase Build Wizard | Working |
| `02_explorer.py` | File tree + Carl integration | Working |
| `03_gatekeeper.py` | Louis file protection UI | Working |
| `04_connie_ui.py` | Database conversion tools | Working |
| `05_universal_bridge.py` | Registry-based tool execution | Working |
| `06_maestro.py` | **NEW** - The Void command center | Skeleton |

### 1.3 The Core Logic Modules

**Louis v2.1 (The Warden)** - `IP/louis_core.py`
- File locking via `os.chmod`
- Git pre-commit hook installation
- Config in `.louis-control/louis-config.json`

**Carl v2.0 (The Context Bridge)** - `IP/carl_core.py`
- Wraps TypeScript analyzers via subprocess
- Ingests JSON into pandas DataFrames

**Connie (The Converter)** - `IP/connie.py`
- SQLite to JSON/MD/CSV export
- Headless operation (no PyQt)

### 1.4 The Universal Bridge

**Key Innovation:** Dynamic tool discovery via registry:

```
frontend/tools/registry/*.json  →  Auto-generated UI
```

Each manifest declares:
- `name`, `base_command`, `description`
- `discovery.enabled` + `discovery.command` (for auto-discovery)
- `static_commands[]` (predefined buttons)

Orchestr8 scans the registry and builds accordion UI with execution buttons.

---

## Part 2: The MaestroView Contextualization

### 2.1 Spatial Layout Pattern

MaestroView.vue isn't a tab-based dashboard. It's a **spatial command center**:

```
┌─────────────────────────────────────────────────────────────────┐
│ TOP ROW - [stereOS] ──────────── [Collabor8][JFDI][Gener8]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     [PANELS EMERGE FROM TOP/RIGHT WHEN SUMMONED]               │
│                                                                 │
│                    ╔════════════════════╗                      │
│                    ║    THE VOID        ║                      │
│                    ║  Messages emerge   ║                      │
│                    ║  Graph renders     ║                      │
│                    ╚════════════════════╝                      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ BOTTOM FIFTH - The Overton Anchor                               │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ [Attachment Chips]                                          ││
│ │ [Chat Input - Full Width TextArea - NEVER MOVES]            ││
│ │ [Apps][Matrix][Files] ═[maestro]═ [Search][Terminal][Send]  ││
│ └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Key Design Principles (From MaestroView.vue)

1. **NO breathing animations** - Elements do not pulse
2. **Messages EMERGE** - Only show last 3 assistant messages
3. **Panels slide in from void** - Conditional rendering, not tabs
4. **Bottom Fifth is fixed** - The input bar NEVER moves
5. **Color System (EXACT):**
   - `#1fbdea` - Blue dominant (UI default)
   - `#D4AF37` - Gold metallic (UI highlight)
   - `#B8860B` - Gold dark (Maestro default)
   - `#0A0A0B` - The Void background

### 2.3 The Void's Purpose

Ben's insight: **The Void is the perfect space for the Connection Graph.**

The central canvas can display:
- **PyVis network graph** of codebase dependencies
- **Agent deployment overlay** showing active instances
- **LLM conversation** with context-aware responses

---

## Part 3: The Agent Orchestration Vision

### 3.1 The Problem Claude Code Instances Face

Each Claude Code instance can:
- Read/write files in its working directory
- Execute shell commands
- Read `CLAUDE.md` (standing orders)

Each Claude Code instance **CANNOT**:
- Spawn other Claude Code instances
- Send messages to other instances
- Know what other instances are doing in real-time

### 3.2 The "Dead Drop" Solution

**Since all instances share the filesystem, coordination happens through files:**

```
COMMAND_CENTER.json (at project root)
├── session_id: "2026-01-26-alpha"
├── emperor_directive: "Complete provider unification"
└── fiefdoms:
    ├── src/llm:
    │   ├── assigned: true
    │   ├── goal: "Single registry, all 10 providers working"
    │   └── status: "awaiting_general"
    └── src/modules:
        ├── assigned: false
        ├── goal: "Wire to unified provider system"
        └── status: "blocked_by_llm"
```

**Each fiefdom's CLAUDE.md instructs:**
```markdown
Before starting work, read `../../COMMAND_CENTER.json` to understand:
1. What session you're part of
2. What your goal is
3. What's blocked on your success

When you complete a task, update your fiefdom's status.
```

### 3.3 The Agent Hierarchy

From `Agent Deployment Strategy/orchestr8 Agents.md`:

```
MAIN CONTEXT (Claude)
    │ TASK_MANIFEST.json
    ▼
ORCHESTRATOR AGENT (Ralph Wiggum Loop)
    │ WAVE_PLAN.json
    ▼
DEPLOYMENT STRATEGIST AGENT
    │
    ├─► SCOUT (Read-only analysis)
    ├─► FIXER (Surgical changes)
    ├─► SYNTHESIZER (Pattern detection)
    ├─► VALIDATOR (Test runner)
    ├─► EPO HUMAN ADVOCACY (User delight guardian)
    └─► GIT COMMIT AGENT (Only agent that commits)
```

### 3.4 How MaestroView Serves This

**The Void becomes the Orchestration Dashboard:**

| MaestroView Element | Orchestration Purpose |
|---------------------|----------------------|
| The Void (center) | Connection Graph + Active Agents |
| Collabor8 panel (top-slides-down) | Agent roster + status |
| JFDI panel (right-slides-in) | Task queue + wave progress |
| Bottom chat input | Emperor directives |
| Message emergence | Agent status reports |

**Visual Concept:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [Home] stereOS ───────────── [Agents][Tasks][Generate]         │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────┐                            │
│ │ AGENTS PANEL (if open)          │                            │
│ │ • Scout-A: src/llm (ACTIVE)     │                            │
│ │ • Fixer-B: src/api (WAITING)    │                            │
│ │ • Validator-C: (PENDING)        │                            │
│ └─────────────────────────────────┘                            │
│                                                                 │
│         ┌───────────────────────────────────────────┐          │
│         │      CONNECTION GRAPH (PyVis)             │          │
│         │                                            │          │
│         │    [src/llm] ──────► [src/modules]        │          │
│         │        │                  │               │          │
│         │        ▼                  ▼               │          │
│         │   [providers]      [generator]            │          │
│         │                                            │          │
│         │   🟢 Agent active on highlighted node     │          │
│         └───────────────────────────────────────────┘          │
│                                                                 │
│ ┌─ LATEST AGENT REPORT ─────────────────────────────┐          │
│ │ Scout-A: "Found 3 missing provider implementations"│          │
│ │ Timestamp: 14:32:05                                │          │
│ └────────────────────────────────────────────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│ [Attached: src/llm/registry.ts]                                │
│ [Deploy scout to src/llm to analyze provider gaps___________]  │
│ [Files][Matrix][Graph] ═[maestro]═ [Search][Deploy][Send]      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 4: The Open Questions

### Q1: Real-Time vs Polling

The filesystem-based "dead drop" is **asynchronous**. Orchestr8 would need to:
- Poll `COMMAND_CENTER.json` on interval?
- Use filesystem watchers (watchdog)?
- Manual refresh button?

### Q2: Agent Deployment Mechanism

How does Orchestr8 actually **spawn** a Claude Code instance?

Option A: Manual (user opens terminal)
Option B: `subprocess.Popen(['gnome-terminal', '--', 'claude', ...])`
Option C: Integration with tmux/screen
Option D: Future Claude Code API (doesn't exist yet)

### Q3: Graph + Panels in Marimo

PyVis generates HTML strings. Overlaying panels on top requires:
- CSS z-index layering via `mo.Html()`
- Careful state management for panel visibility
- Possibly custom JavaScript injection

### Q4: The "Blast Radius" Visualization

When an agent proposes a change, Louis's "Diff Surgeon" concept:
- Highlight the changed node (yellow)
- Highlight connected nodes (orange) - the blast radius
- Show which locked files would be affected

**Is this the right UX for change approval?**

---

## Part 5: What We Need Feedback On

1. **Is the spatial UI pattern (Void + emergence) the right model for agent orchestration, or is the existing tab-based approach sufficient?**

2. **The Connection Graph in The Void - should it be:**
   - Always visible (background canvas)?
   - On-demand (toggle button)?
   - Contextual (appears when relevant)?

3. **Agent status representation:**
   - Overlay badges on graph nodes?
   - Separate panel listing?
   - Message emergence pattern (like LLM responses)?

4. **The "dead drop" pattern for coordination:**
   - Is `COMMAND_CENTER.json` at project root the right location?
   - Should each fiefdom have its own status file?
   - How granular should status updates be?

5. **Priority of implementation:**
   - Should we fully build The Void UI first?
   - Or prove the agent coordination pattern manually first?
   - Or build them in parallel?

---

## Part 6: Files to Review

For full context, the other Claude instance should read:

1. **Architecture:**
   - `/home/user/Orchestr8_jr/CLAUDE.md` - Project overview
   - `/home/user/Orchestr8_jr/PRDs/PRD Orchestr8 v3.md` - Technical spec
   - `/home/user/Orchestr8_jr/IP/The "IP" Protocol.md` - Directory structure

2. **Agent Strategy:**
   - `/home/user/Orchestr8_jr/Agent Deployment Strategy/orchestr8 Agents.md` - Full hierarchy
   - `/home/user/Orchestr8_jr/Agent Deployment Strategy/AGENT_DEF_ORCHESTRATOR.md`
   - `/home/user/Orchestr8_jr/Agent Deployment Strategy/AGENT_DEF_SCOUT.md`

3. **MaestroView Reference:**
   - `/home/user/Orchestr8_jr/UI Reference/MaestroView.vue` - The source
   - `/home/user/Orchestr8_jr/docs/MAESTROVIEW_MARIMO_CONTEXTUALIZATION.md` - Translation guide

4. **Current Implementation:**
   - `/home/user/Orchestr8_jr/IP/orchestr8_app.py` - Main app
   - `/home/user/Orchestr8_jr/IP/plugins/06_maestro.py` - The Void plugin

---

## Conclusion

**Where we are:** A working Marimo dashboard with 6 plugins and a robust architecture for tool integration.

**Where we're going:** A spatial command center that visualizes the codebase graph AND the agent deployment topology, enabling a human "Emperor" to orchestrate multiple Claude Code instances via filesystem-based coordination.

**The key insight:** MaestroView's "Void" isn't just empty space - it's a **canvas** that can render both the static topology (code connections) and the dynamic activity (agent status).

**The ask:** Feedback on whether this vision aligns with the practical constraints of Claude Code instances and Marimo's capabilities.

---

*Document prepared for cross-instance coordination via the "dead drop" pattern.*
*Session: 2026-01-26*

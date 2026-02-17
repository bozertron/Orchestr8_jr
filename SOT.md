# Orchestr8 Source of Truth

**Last Updated:** 2026-01-30
**Maintainer:** Ben (Emperor)

---

## Current State

| Item | Value |
|------|-------|
| **Entry Point** | `orchestr8.py` (root level) |
| **UI Goal** | `IP/plugins/06_maestro.py` (orchestr8 layout) |
| **Config** | `pyproject_orchestr8_settings.toml` |
| **Plugin Directory** | `IP/plugins/` |

---

## Active Codebase

```
Orchestr8_jr/
├── orchestr8.py                      # Entry point - loads plugins
├── pyproject_orchestr8_settings.toml # THE config file
├── CLAUDE.md                         # Claude Code guidance
├── SOT.md                            # This file
├── IP/                               # Implementation
│   ├── plugins/
│   │   ├── 00_welcome.py
│   │   ├── 01_generator.py
│   │   ├── 02_explorer.py
│   │   ├── 03_gatekeeper.py         # Louis UI
│   │   ├── 04_connie_ui.py
│   │   ├── 05_universal_bridge.py
│   │   ├── 06_maestro.py            ★ THE GOAL UI (orchestr8 layout)
│   │   ├── 07_settings.py
│   │   ├── 08_director.py
│   │   └── components/              # Panel components
│   │       ├── calendar_panel.py
│   │       ├── comms_panel.py
│   │       ├── deploy_panel.py
│   │       ├── file_explorer_panel.py
│   │       └── ticket_panel.py
│   ├── woven_maps.py                # Code City visualization (COMPLETE)
│   ├── combat_tracker.py            # LLM deployment tracking
│   ├── connection_verifier.py       # Import graph builder
│   ├── mermaid_generator.py         # Diagram generation
│   ├── terminal_spawner.py          # Terminal session management
│   ├── health_checker.py            # System health monitoring
│   ├── briefing_generator.py        # Context generation
│   ├── louis_core.py                # File protection system
│   ├── carl_core.py                 # [TBD]
│   ├── connie.py                    # Database converter
│   ├── ticket_manager.py            # Ticket system
│   └── styles/
│       └── orchestr8.css
└── one integration at a time/       # Staged for future integration
```

---

## The Goal: 06_maestro.py (orchestr8 Layout)

The UI should render as a full-screen orchestr8 interface:

```
┌─────────────────────────────────────────────────────────────────┐
│ [orchestr8]             [collabor8]              [JFDI]         │  ← Top Bar
├─────────────────────────────────────────────────────────────────┤
│                                                           │ P │
│                    THE VOID                               │ A │
│              (Woven Maps Code City)                       │ N │
│                                                           │ E │
│         Gold = Working    Blue = Broken                   │ L │
│                Purple = Combat                            │ S │
├─────────────────────────────────────────────────────────────────┤
│ [Attachment Bar]                                                │
│ [Control Surface - maestro input]                               │
│ [Status Bar]                                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Key Principles:**
- NO BREATHING ANIMATIONS (things EMERGE, not breathe)
- Colors are EXACT: Gold (#D4AF37), Blue (#1fbdea), Purple (#9D4EDD)
- The Void is THE central metaphor
- Errors float up like pollution
- The Emperor must see everything

---

## Color System

| State | Color | Hex | Usage |
|-------|-------|-----|-------|
| Working | Gold | #D4AF37 | Healthy code, imports resolve |
| Broken | Blue/Teal | #1fbdea | Has errors, needs attention |
| Combat | Purple | #9D4EDD | LLM "General" actively debugging |
| Void | Black | #0A0A0B | Background |
| Surface | Dark Gray | #121214 | Elevated elements |

---

## Integration Queue

**See:** `one integration at a time/INTEGRATION_QUEUE.md`

---

## Archived References

The following documents have been archived to `one integration at a time/` and can be referenced but should NOT be treated as active SOT:

| Document | Location | Purpose |
|----------|----------|---------|
| WOVEN_MAPS_EXECUTION_SPEC.md | `one integration at a time/docs/` | Woven Maps implementation spec |
| UI_ARCHITECTURE_SPEC.md | `one integration at a time/docs/` | UI layer definitions |
| LLM_BEHAVIOR_SPEC.md | `one integration at a time/docs/` | Model selection rules |
| ORCHESTR8_STATUS_HANDOFF.md | `one integration at a time/docs/` | Cross-instance coordination |
| PRD_ORCHESTR8_V4_CONSOLIDATED.md | `one integration at a time/PRDs/` | Product requirements v4 |
| orchestr8 Agents.md | `one integration at a time/Agent Deployment Strategy/` | Agent hierarchy |

---

## Validation Rules

After EVERY integration from `one integration at a time/`:

1. [ ] Update this SOT.md to reflect new active components
2. [ ] Remove integrated items from `one integration at a time/`
3. [ ] Update INTEGRATION_QUEUE.md to mark completed
4. [ ] Verify `orchestr8.py` still runs: `marimo run orchestr8.py`
5. [ ] Verify 06_maestro.py renders correctly
6. [ ] Get Ben's approval before proceeding to next integration

---

## Grand Vision: orchestr8 → ∅明nos

Orchestr8 is the initial settlement of ∅明nos — a collaborative spatial environment for human and machine intelligence. The pipeline:

1. **Orchestr8** (current) — Marimo dashboard + Code City visualization
2. **Orchestr8 Spatial UI** — Full Marimo-native reactive UI with correct methods and seamless integration
3. **vscode-marimo plugin** — Modified plugin at `vscode-marimo/` driving orchestr8 within VS Code
4. **∅明nos** — The destination: shared spatial experience at scale

See `GSD + Custom Agents/The_Story_of_Mingos_A_Tale_of_Emergence.md` for the origin story and vision.

---

## Settlement System

The multi-agent architecture for scaled codebase work. 30 agents across 10 tiers.

| Category | Count | Source |
|----------|-------|--------|
| New settlement agents | 19 | `GSD + Custom Agents/settlement-*.md` |
| Enhanced GSD agents | 11 | `GSD + Custom Agents/gsd-*-enhanced.md` |
| Settlement workflows | 5 | `GSD + Custom Agents/` (workflow files) |
| Settlement templates | 6 | `GSD + Custom Agents/` (template files) |

**Architecture spec:** `GSD + Custom Agents/SETTLEMENT_SYSTEM_PRESSURE_TEST.md`
**Integration spec:** `GSD + Custom Agents/INTEGRATION_PROMPT.md`

**Installation target:** Local `~/.claude/` (not upstream GSD repo)

---

## vscode-marimo Plugin

**Location:** `vscode-marimo/`
**Status:** Scaffold only (empty src/ directory)
**Purpose:** Modified Marimo VS Code plugin that integrates orchestr8 as the development environment
**Future work:** Build from Marimo's official VS Code extension, adapted for orchestr8 spatial UI

---

## Louis (File Protection)

Louis prevents accidental modification of critical files:
- Uses `chmod 444` to lock files
- Maintains protected-files.txt list
- Integrates with git pre-commit hooks
- UI in `03_gatekeeper.py`

---

## Running the Application

```bash
# Run the app
marimo run orchestr8.py

# Development mode with hot reloading
marimo edit orchestr8.py
```

---

## Dependencies

```bash
pip install marimo pandas networkx pyvis jinja2
```

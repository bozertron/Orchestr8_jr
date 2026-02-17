# AGENT DEPLOYMENT DIRECTIONS - CLEAN STRUCTURE FIRST
**Generated:** 2026-02-16
**Mode:** Option B - Clean Structure + Copy with Deep Analysis

---

## MISSION BRIEF

You are part of a **dedicated herd** tasked with integrating Orchestr8_jr into a_codex_plan. 

**PRIORITY 1:** Create clean module structure in a_codex_plan (BEFORE any UI integration)
**PRIORITY 2:** For each chunk of logic, analyze how it maps to marimo, 2D/3D files, and a_codex_plan

---

## STRUCTURE IMPERATIVE (CONFIRMED)

The structure is NOT negotiable. Clean first, then integrate:

```
a_codex_plan/
├── app/
│   ├── app.py              ← Entry point (NEW, clean)
│   └── modules/
│       ├── _state.py       ← All mo.state() (NEW)
│       ├── _services.py    ← Service instances (NEW)
│       ├── _handlers.py    ← Button handlers (NEW)
│       └── panels/         ← Panel outputs (NEW)
├── lib/                    ← Pure Python (migrated from IP/)
│   ├── health/
│   ├── combat/
│   ├── code_city/
│   └── contracts/
├── ui/                     ← UI components (NEW)
└── static/                 ← CSS, fonts (COPY from Orchestr8_jr)
```

---

## AGENT DEPLOYMENT PHASES

### PHASE 1: STRUCTURE SETUP (BLOCKING)

**No UI work until this is complete.**

| Agent | Task | Deliverable | Hours |
|-------|------|-------------|-------|
| S-1 | Create app/ module structure | `app/__init__.py`, `app/app.py`, `app/modules/__init__.py` | 2 |
| S-2 | Create lib/ directory structure | `lib/`, `lib/health/`, `lib/combat/`, `lib/code_city/`, `lib/contracts/` | 2 |
| S-3 | Create ui/ component library | `ui/__init__.py`, `ui/buttons.py`, `ui/panels.py`, `ui/layouts.py` | 3 |
| S-4 | Copy static assets | `orchestr8.css`, font files to `static/` | 1 |

**BLOCKER:** Cannot proceed to Phase 2 until Phase 1 tests pass:
```bash
# Should run without import errors
python -c "from app import app; print('OK')"
```

---

### PHASE 2: CHUNK ANALYSIS & MIGRATION

For each subsystem, agents must analyze:
1. **What it does** - Function/purpose
2. **Marimo mapping** - How to implement in marimo (state, handlers, outputs)
3. **2D/3D files** - What visual files it connects to
4. **Wiring** - Input/output contracts, dependencies
5. **Integration** - How it fits into a_codex_plan structure

#### Agent Task Template

```
ANALYZE: <subsystem name>
─────────────────────────────────────
FILE: <source file in Orchestr8_jr>
LOCATION: <exact path>

1. FUNCTION:
   - What does this code do?
   - What are its inputs?
   - What are its outputs?

2. MARIMO MAPPING:
   - What mo.state() variables does it need?
   - What handlers does it define?
   - What UI elements does it render?
   - Is this a "cell" output or a service?

3. 2D/3D FILES:
   - Does this connect to woven_maps_3d.js?
   - Does this connect to woven_maps_template.html?
   - What visual tokens does it use?

4. WIRING:
   - What does this depend on?
   - What depends on this?
   - What are the input/output contracts?

5. INTEGRATION:
   - How should this be structured in a_codex_plan?
   - Should it go in lib/, ui/, or app/modules/?
   - What changes needed for clean structure?

6. AMBIGUITIES:
   - What is unclear about this integration?
   - What needs clarification before implementation?
```

#### Subsystem Assignments

| Agent | Subsystem | Source File | Target |
|-------|-----------|-------------|--------|
| A-1 | Health Checking | `IP/health_checker.py` | `lib/health/` |
| A-2 | Health Watching | `IP/health_watcher.py` | `lib/health/` |
| A-3 | Combat Tracking | `IP/combat_tracker.py` | `lib/combat/` |
| A-4 | Code City Graph | `IP/features/code_city/graph_builder.py` | `lib/code_city/` |
| A-5 | Code City Render | `IP/features/code_city/render.py` | `lib/code_city/` |
| A-6 | Woven Maps Config | `IP/woven_maps.py` | `lib/code_city/` |
| A-7 | Contracts (all) | `IP/contracts/*.py` | `lib/contracts/` |
| A-8 | Contextualizer | `IP/carl_core.py` | `lib/context/` |
| A-9 | Connection Verify | `IP/connection_verifier.py` | `lib/connections/` |
| A-10 | Terminal Spawner | `IP/terminal_spawner.py` | `lib/terminal/` |

---

### PHASE 3: UI SURFACE PREPARATION

After Phase 2, prepare UI surfaces before integrating visual tokens.

| Agent | Task | Deliverable |
|-------|------|-------------|
| U-1 | Analyze 06_maestro state | Document all mo.state() calls in Orchestr8_jr |
| U-2 | Create _state.py | Centralized state management template |
| U-3 | Analyze 06_maestro handlers | Document all button handlers |
| U-4 | Create _handlers.py | Centralized handler template |
| U-5 | Analyze 06_maestro services | Document all service instantiations |
| U-6 | Create _services.py | Centralized service template |

---

### PHASE 4: VISUAL TOKEN INTEGRATION

After Phase 3, integrate visual tokens into clean structure.

| Agent | Task | Check |
|-------|------|-------|
| V-1 | Verify CSS tokens | All hex values match VISUAL_TOKEN_LOCK.md |
| V-2 | Verify typography tokens | Fonts match LOCK exactly |
| V-3 | Verify dimension tokens | Header 80px, buttons 50×160, etc. |
| V-4 | Verify effect tokens | Glows, shadows match LOCK |

---

## REPORTING REQUIREMENTS

### Each Agent Must Post to Shared Memory

**Observation format:**

```
ANALYSIS: <subsystem> - <source file>
─────────────────────────────────────
1. FUNCTION: <2-3 sentences>
2. MARIMO MAPPING: 
   - State needed: <list>
   - Handlers: <list>
   - UI outputs: <list>
3. 2D/3D CONNECTIONS:
   - Files: <list>
   - Tokens used: <list>
4. WIRING:
   - Dependencies: <list>
   - Consumers: <list>
5. INTEGRATION PLAN:
   - Target location: <path>
   - Changes needed: <list>
6. AMBIGUITIES:
   - <list questions that need answering>
```

---

## BLOCKING CRITERIA

### Cannot Proceed Without:

1. ✅ Phase 1 structure creates without errors
2. ✅ Each Phase 2 analysis posted to shared memory
3. ✅ All ambiguities documented and escalated
4. ✅ Phase 3 UI templates created
5. ✅ Visual token verification passes

---

## COMMUNICATION PROTOCOL

### Daily Standup (via shared memory)

Each agent posts:
```
STATUS: <agent-id> - <phase>
- Completed: <list>
- In Progress: <list>
- Blockers: <list>
- Ambiguities to resolve: <list>
```

### Escalation (when blocked)

If you encounter ambiguity:
1. Document it clearly
2. Post to shared memory with "NEEDS CLARIFICATION" tag
3. Continue with other work if possible
4. Wait for resolution before blocked work

---

## QUICK REFERENCE

### Visual Token Lock (CANONICAL)
- Source: `/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md`
- All visual decisions trace back to this

### Marimo Best Practices
- State must be global: `get_val, set_val = mo.state(default)`
- UI elements must be global: `button = mo.ui.button(...)`
- Handlers at module level: `def handle_click(): ...`
- No on_change for buttons: use `on_click`

### Integration Edges
1. VISUAL: CSS tokens → font_profiles → 06_maestro
2. CITY: graph_builder → woven_maps → Three.js
3. HEALTH: health_checker → CodeNode.status
4. COMBAT: tracker → JSON → purple building
5. PANEL: context → deploy_panel
6. CONTRACTS: schemas → all consumers

---

## START NOW

1. **Phase 1 agents:** Create structure immediately
2. **Phase 2 agents:** Begin analyzing subsystems in parallel
3. **Post all findings to shared memory**
4. **Flag all ambiguities**

Let's clean this structure and make it right.
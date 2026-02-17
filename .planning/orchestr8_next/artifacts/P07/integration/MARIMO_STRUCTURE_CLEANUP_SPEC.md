# MARIMO STRUCTURE CLEANUP SPECIFICATION
**Generated:** 2026-02-16
**Purpose:** Clean up file structure for a_codex_plan to follow marimo best practices

---

## MARIMO BEST PRACTICES (From Official Docs)

### Key Concepts
1. **Reactive execution** - Run a cell → marimo automatically runs all dependent cells
2. **No hidden state** - Variables automatically cleaned up when cells deleted
3. **Execution order** - Determined by variable references, NOT cell position
4. **Global variables for UI** - UI elements MUST be assigned to globals for tracking

### Best Practices (Official)
1. **Use global variables sparingly** - Keep small, prefix temp with `_`
2. **Use descriptive names** - Avoid name collisions
3. **Use functions** - Encapsulate logic, avoid polluting namespace
4. **Use Python modules** - Split complex logic into helper modules
5. **Minimize mutations** - Mutate in same cell that creates it
6. **Don't use on_change handlers** - Use reactive execution instead
7. **Write idempotent cells** - Same inputs → same outputs

---

## CURRENT STRUCTURE ISSUES

### Observed Issues in Orchestr8_jr (to fix in a_codex_plan)

| Issue | Location | Problem | Fix |
|-------|----------|---------|-----|
| Duplicate variable names | 06_maestro.py | `ip_root` defined multiple times | Unify to single definition |
| Large cell size | 06_maestro.py | 1300+ lines in one cell | Split into modules |
| Mixing declarations + mutations | Various | DataFrame appended in different cells | Combine in one cell |
| on_click vs on_change | Buttons | Using `on_change` for buttons | Use `on_click` |
| Missing module structure | IP/ | Flat structure | Organize by feature |

---

## TARGET STRUCTURE FOR A_CODEX_PLAN

### Recommended Directory Layout

```
a_codex_plan/
├── app/
│   ├── __init__.py
│   └── app.py              ← Main entry point (orchestr8.py equivalent)
├── app/modules/            ← Marimo cells as functions
│   ├── __init__.py
│   ├── _state.py           ← All mo.state() definitions
│   ├── _services.py        ← Service instances (once)
│   ├── _handlers.py        ← All event handlers
│   ├── header.py           ← Header cell output
│   ├── void.py             ← Main void/city output
│   ├── footer.py           ← Footer/control surface
│   └── panels/             ← Individual panel outputs
│       ├── __init__.py
│       ├── deploy.py
│       ├── ticket.py
│       └── [others]
├── lib/                    ← Pure Python modules (no marimo deps)
│   ├── __init__.py
│   ├── health/
│   │   ├── __init__.py
│   │   ├── checker.py
│   │   └── watcher.py
│   ├── combat/
│   │   ├── __init__.py
│   │   └── tracker.py
│   ├── code_city/
│   │   ├── __init__.py
│   │   ├── graph_builder.py
│   │   └── render.py
│   ├── context/
│   │   ├── __init__.py
│   │   └── contextualizer.py
│   └── contracts/
│       ├── __init__.py
│       └── [all contracts]
├── ui/                     ← UI component library
│   ├── __init__.py
│   ├── buttons.py
│   ├── panels.py
│   └── layouts.py
└── static/                 ← CSS, JS, assets
    ├── orchestr8.css
    └── [fonts, images]
```

### Cell Organization Pattern

```python
# app/app.py - Main entry point

import marimo as mo

app = marimo.App(width="full")

# ============================================================================
# CELL 1: Imports + Setup (run once)
# ============================================================================
@app.cell
def import_modules():
    """Import all modules - runs once at startup."""
    from app.modules import _state, _services, _handlers
    from app.modules import header, void, footer
    from lib.health import HealthChecker
    from lib.combat import CombatTracker
    return

# ============================================================================
# CELL 2: State initialization (run once)
# ============================================================================
@app.cell
def init_state(import_modules):
    """Initialize all state - runs once."""
    root_state, set_root = mo.state("/path/to/project")
    # ... all other state
    return

# ============================================================================
# CELL 3: Service instantiation (run once)
# ============================================================================
def init_services(root_state):
    """Create service instances once."""
    health = HealthChecker(root_state)
    combat = CombatTracker(root_state)
    return health, combat

# ============================================================================
# CELL 4-10: UI Output cells (reactive to state changes)
# ============================================================================
@app.cell
def render_header(state):
    """Header cell - reactive to state changes."""
    return header.render(state)

@app.cell
def render_void(state, services):
    """Main void/city - reactive to all dependencies."""
    return void.render(state, services)
```

---

## INTEGRATION REQUIREMENTS FOR A_CODEX_PLAN

### Phase 1: Prepare UI Surfaces BEFORE Integration

Before mapping visual tokens, the following must be prepared:

| Requirement | Status Needed | File to Create |
|-------------|---------------|----------------|
| **Entry point** | Ready | `app/app.py` with proper structure |
| **State management** | Clean | `app/modules/_state.py` - all mo.state() centralized |
| **Service layer** | Clean | `app/modules/_services.py` - all services |
| **Handler layer** | Clean | `app/modules/_handlers.py` - all button handlers |
| **Module reloading** | Enabled | Auto-reload for development |

### Phase 2: Match Visual Token Layout

After structure is clean, verify:

| Visual Token | Implementation | Check |
|--------------|----------------|-------|
| Header 80px | `header.py` renders with CSS | Height matches |
| Buttons 50×160 | `buttons.py` uses mo.ui.button | Dimensions match |
| Footer 36px input | `footer.py` render input | Height matches |
| Colors | CSS variables used | Exact hex from LOCK |
| Typography | Font tokens used | Exact fonts from LOCK |

---

## MIGRATION CHECKLIST FOR EACH INTEGRATION

### Pre-Integration Checklist (a_codex_plan)

- [ ] All mo.state() calls centralized in `_state.py`
- [ ] No duplicate variable names across cells
- [ ] All services instantiated in `_services.py` (once)
- [ ] All handlers defined in `_handlers.py`
- [ ] Complex logic extracted to `lib/` modules
- [ ] No on_change handlers (use on_click for buttons)
- [ ] Mutations combined with declarations in same cell
- [ ] CSS variables match VISUAL_TOKEN_LOCK exactly
- [ ] Layout dimensions match VISUAL_TOKEN_LOCK exactly

### Integration Testing Checklist

- [ ] Run `marimo run app/app.py` - should work without errors
- [ ] Verify no "multiple definitions" lint errors
- [ ] Verify no "cycle dependencies" lint errors
- [ ] Verify reactive execution works (change state → UI updates)
- [ ] Verify visual tokens applied (colors, fonts, dimensions)

---

## PHYSICAL FILE PLACEMENT RULES

### Critical Marimo Rules

1. **File path = cell execution order**
   - Cells are executed based on variable references, NOT file position
   - BUT file organization affects developer experience

2. **UI elements must be global**
   ```python
   # GOOD
   slider = mo.ui.slider(...)
   
   # BAD - won't track
   _slider = mo.ui.slider(...)
   ```

3. **State must be in global scope**
   ```python
   # GOOD - global state
   get_value, set_value = mo.state(default)
   
   # BAD - function-scoped won't persist
   def get_state():
       return mo.state(default)  # Won't work!
   ```

4. **Handler callbacks must be defined at module level**
   ```python
   # GOOD
   def handle_click():
       set_value(new_value)
   
   button = mo.ui.button(on_click=handle_click)
   
   # BAD - closure won't track
   button = mo.ui.button(on_click=lambda: set_value(new_value))
   ```

---

## AGENT TASKS FOR STRUCTURE CLEANUP

### Task 1: Create Module Structure

```
Agent: Create app/ directory structure
Files to create:
- app/__init__.py
- app/app.py (entry point)
- app/modules/__init__.py
- app/modules/_state.py
- app/modules/_services.py
- app/modules/_handlers.py
- lib/__init__.py
- lib/health/__init__.py
- lib/combat/__init__.py
- lib/code_city/__init__.py
- lib/context/__init__.py
- lib/contracts/__init__.py
```

### Task 2: Migrate State Management

```
Agent: Centralize mo.state() calls
From: 06_maestro.py (scattered)
To: app/modules/_state.py (centralized)
Verify: No duplicate state names
```

### Task 3: Extract Service Layer

```
Agent: Extract services to modules
From: 06_maestro.py (inline instantiation)
To: app/modules/_services.py + lib/*
Verify: Services created once, not on every render
```

### Task 4: Fix Button Handlers

```
Agent: Fix button callback patterns
From: on_change (deprecated)
To: on_click (correct)
Verify: All buttons use on_click
```

### Task 5: Verify Visual Token Alignment

```
Agent: Verify CSS tokens match LOCK
File: static/orchestr8.css
Check: All hex values match VISUAL_TOKEN_LOCK.md exactly
```

---

## DECISION REQUIRED

Before creating the cleanup plan:

1. **Should we use the exact same structure as Orchestr8_jr?**
   - Option A: Mirror exactly (faster to start)
   - Option B: Clean structure from scratch (cleaner long-term)

2. **Should we copy Orchestr8_jr's 06_maestro.py or rewrite?**
   - Option A: Copy + adapt (faster)
   - Option B: Rewrite with clean structure (more work)

3. **What's the priority order?**
   - A: Get UI working first, then clean structure
   - B: Clean structure first, then integrate UI

**Recommendation:** Option A + Copy + Adapt (fastest path to working UI)

---

## NEXT STEPS

1. **Confirm structure approach** (mirror or clean)
2. **Create migration script** (copy files with adaptations)
3. **Spawn agent** to create module structure in a_codex_plan
4. **Verify** structure before integration
5. **Integrate** visual tokens into clean structure
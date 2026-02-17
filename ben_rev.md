# TaskMaster Unfinished Tasks Review

**Generated:** 2026-02-15
**Total Unfinished Tasks:** 16

---

## Summary

| Source | Done | Unfinished | Total |
|--------|------|------------|-------|
| Main Repo (`Orchestr8_jr`) | 23 | 1 | 24 |
| Secondary (`one integration at a time`) | 9 | 15 | 24 |
| **GRAND TOTAL** | 32 | **16** | 48 |

---

## Part 1: Main Repo (1 Unfinished)

### Task #24: Integration Test - Full Style Pass Validation
**Status:** `pending`
**Priority:** HIGH
**Dependencies:** 14, 16, 18, 20, 22, 23

**What It Is:**
A comprehensive manual test pass to validate all styling changes work together. This is the final verification step before considering the style integration complete.

**Checklist to Execute:**
- [ ] Color palette matches canonical values
- [ ] Typography variables defined and applied
- [ ] Local fonts load and render
- [ ] Font selector in Settings works
- [ ] No CSS parsing errors in console
- [ ] 3D Code City renders without errors
- [ ] Desktop layout correct at 1280px, 1920px
- [ ] Narrow layout functional at 768px, 480px
- [ ] Button styles match MaestroView
- [ ] Lower-fifth rhythm improved
- [ ] Emergence animations correct timing

**Assessment:** This is a manual QA task. Likely quick to execute—just needs someone to run through the checklist and document results.

---

## Part 2: Secondary Repo - "one integration at a time" (15 Unfinished)

These tasks appear to be from an earlier planning phase for Carl/Maestro/Settlement System features. Many have dependency chains.

### Task #21: End-to-End Universal Bridge Integration Test
**Status:** `pending`
**Priority:** HIGH
**Depends On:** #18 (done)

**What It Is:**
Manual E2E test of the Universal Bridge plugin discovering and executing Scaffold Parsers.

**Test Steps:**
1. Open Universal Bridge tab in Marimo
2. Verify "Scaffold Parsers (TS)" accordion appears
3. Expand and verify discovered plugins as buttons
4. Execute "overview" parser
5. Verify JSON table rendering

**Assessment:** Test task. Quick to execute if Universal Bridge is functional.

---

### Task #22: Multi-Manifest and Dynamic UI Test
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #21

**What It Is:**
Test that multiple manifests work and UI updates dynamically when manifests are added/removed.

**Test Steps:**
1. Create test manifest (99_test.json)
2. Restart Marimo, verify both accordions appear
3. Remove test manifest
4. Restart, verify only Scaffold remains

**Assessment:** Test task. Depends on #21.

---

### Task #23: Apply MaestroView Color Palette to 06_maestro.py
**Status:** `pending`
**Priority:** HIGH
**Depends On:** None (root task)

**What It Is:**
Inject CSS variables for the canonical MaestroView color palette into the main maestro plugin.

**Colors to Implement:**
```
--blue-dominant: #1fbdea
--gold-metallic: #D4AF37
--gold-dark: #B8860B
--gold-saffron: #F4C430
--purple-combat: #9D4EDD
--bg-primary: #0A0A0B
--bg-elevated: #121214
```

**Assessment:** Foundation task for visual consistency. Other tasks (#24, #25, #28) depend on this.

---

### Task #24: Implement Mermaid Status Graph in Void Dashboard
**Status:** `pending`
**Priority:** HIGH
**Depends On:** #23

**What It Is:**
Create an interactive Mermaid graph showing fiefdom health states (gold/blue/purple) in the left panel.

**Implementation:**
- Use `mermaid==10.9.1` library
- Generate from Carl's `fiefdom-status.json`
- Nodes: src/llm, src/modules, src/platform, src/generator, src/maestro
- Click handlers open fiefdom details

**Assessment:** Feature implementation. Depends on color palette (#23).

---

### Task #25: Build Fiefdom List with Health Indicators
**Status:** `pending`
**Priority:** HIGH
**Depends On:** #23, #24

**What It Is:**
Right panel showing fiefdom cards with status indicators and Deploy button.

**Features:**
- Cards with emoji+color status (🟡🔵🟣)
- [DEPLOY ▼] dropdown per card
- Fixed height scrollable list
- Data from `Carl.get_fiefdom_status()`

**Assessment:** Feature implementation. Depends on #23 and #24.

---

### Task #26: Integrate Carl Health Checks with Status Aggregation
**Status:** `pending`
**Priority:** HIGH
**Depends On:** #24

**What It Is:**
Connect Carl's health check system to update fiefdom states and the Mermaid graph.

**Implementation:**
- Import `IP/carl_core.py`
- Add [🔄 REFRESH] button
- Call `carl.check_health_all_fiefdoms()`
- Parse `npm run typecheck` output for errors
- Auto-create tickets for broken fiefdoms

**Assessment:** Feature implementation. Core Carl integration.

---

### Task #27: Create Runtime Directories and Initial State Files
**Status:** `pending`
**Priority:** HIGH
**Depends On:** None (root task)

**What It Is:**
Setup the `.orchestr8/` runtime directory structure.

**Structure:**
```
.orchestr8/
├── tickets/
│   └── archive/
└── state/
    └── fiefdom-status.json
```

**Assessment:** Foundation task. Quick to implement. Other tasks (#29, #30, #31) depend on this.

---

### Task #28: Implement Fixed Overton Anchor Input Bar
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #23

**What It Is:**
Bottom fixed input bar with navigation buttons.

**Layout:**
```
[Files][Matrix][Graph]═══[maestro]═══[Search][Deploy][⏎]
```

**CSS:** `position: fixed; bottom: 0; height: 20vh`

**Assessment:** UI feature. Depends on color palette (#23).

---

### Task #29: Build Tickets Panel with Slide-Right Animation
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #25, #27

**What It Is:**
Slide-out panel showing ticket list from `.orchestr8/tickets/`.

**Features:**
- Slide-right animation
- List TICKET-###.md files as cards
- Search/filter by status
- States: PENDING|IN_PROGRESS|RESOLVED|BLOCKED

**Assessment:** Feature implementation. Depends on #25 and #27.

---

### Task #30: Generate BRIEFING.md for General Deployment
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #26, #27

**What It Is:**
Auto-generate mission briefing before deploying to a fiefdom.

**Combines:**
- CLAUDE.md for fiefdom
- Carl file inventory
- Open tickets
- Last 10 CAMPAIGN_LOG entries

**Assessment:** Feature implementation. Depends on #26 and #27.

---

### Task #31: Implement CAMPAIGN_LOG.md Wisdom System
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #27, #30

**What It Is:**
Append-only wisdom log per fiefdom for accumulated learnings.

**Format:**
```
[YYYY-MM-DD HH:MM] TICKET-###
General: ...
Status: ...
Duration: ...
Mission: ...
Actions Taken: ...
Lessons Learned: ...
Watch List: ...
```

**Assessment:** Feature implementation. Depends on #27 and #30.

---

### Task #32: Setup Git Hooks for Louis and Carl Enforcement
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #26

**What It Is:**
Git hooks for automated validation and health checks.

**Hooks:**
- `pre-commit`: Louis validates staged files
- `post-commit`: Carl runs health checks and updates graph

**Assessment:** DevOps task. Depends on #26.

---

### Task #34: Wire Terminal Spawner to Phreak Button
**Status:** `in-progress`
**Priority:** HIGH
**Depends On:** #33 (done)

**What It Is:**
Connect the Phreak> button to actually spawn an actu8 terminal.

**Implementation:**
- Create `handle_terminal()` function
- Call `TerminalSpawner.spawn_terminal()`
- Track in CombatTracker (purple status)

**Subtasks:**
- [ ] 34.1: Create handle_terminal function
- [ ] 34.2: Call TerminalSpawner.spawn_terminal
- [ ] 34.3: Track terminal in CombatTracker

**Assessment:** Partially started. 3 subtasks pending.

---

### Task #35: Wire Combat Status to Woven Maps Purple Glow
**Status:** `pending`
**Priority:** HIGH
**Depends On:** #34

**What It Is:**
Make files glow purple in Code City when they have active deployments.

**Implementation:**
- Import CombatTracker in woven_maps.py
- Query combat files in build_graph_data()
- Set node.status = 'combat' for active files

**Subtasks:**
- [ ] 35.1: Import CombatTracker in woven_maps.py
- [ ] 35.2: Query combat files in build_graph_data
- [ ] 35.3: Set node.status to combat for active files

**Assessment:** Depends on #34.

---

### Task #36: Wire Settings Panel to LLM Configuration
**Status:** `pending`
**Priority:** MEDIUM
**Depends On:** #33 (done)

**What It Is:**
Read model/API settings from orchestr8_settings.toml for LLM integration.

**Implementation:**
- Create `get_model_config()` function
- Use settings for model name and max_tokens
- Fallback to hardcoded defaults

**Subtasks:**
- [ ] 36.1: Create get_model_config function
- [ ] 36.2: Use config in API call

**Assessment:** Straightforward config integration.

---

## Dependency Graph

```
ROOT TASKS (no dependencies):
├── #23: Apply MaestroView Color Palette
├── #27: Create Runtime Directories
└── #34: Wire Terminal Spawner (in-progress)

CHAIN 1 - Visual System:
#23 (colors) → #24 (mermaid graph) → #25 (fiefdom list) → #29 (tickets panel)
                      ↓
                 #26 (carl health) → #30 (briefing) → #31 (campaign log)
                      ↓
                 #32 (git hooks)

CHAIN 2 - Combat Status:
#34 (terminal spawner) → #35 (purple glow)

CHAIN 3 - Settings:
#36 (settings panel) - standalone, depends on #33 (done)

TEST TASKS:
#21 (E2E bridge test) → #22 (multi-manifest test)
#24 (main repo) - standalone style validation
```

---

## Recommendations

### Quick Wins (Can Do Immediately)
1. **#27** - Create Runtime Directories (no deps, ~10 min)
2. **#23** - Apply Color Palette (no deps, ~30 min)
3. **#24 (main)** - Style Pass Validation (manual test, ~20 min)

### Blocking Issues
- **#34 is in-progress but has 3 pending subtasks** - needs completion before #35
- **#23 blocks 5 other tasks** - high leverage to complete first

### Potentially Stale
The tasks in "one integration at a time" reference features that may have evolved:
- Carl integration may have changed since planning
- Universal Bridge may work differently now
- The Settlement System concept has matured

### Suggested Approach
1. Validate which tasks are still relevant
2. Complete #23 (colors) and #27 (directories) as foundation
3. Finish #34 (terminal spawner) since it's in-progress
4. Run #24 (main) style validation to close out main repo
5. Re-evaluate remaining tasks based on current project direction

---

## File Locations

| Taskmaster File | Path |
|-----------------|------|
| Main | `.taskmaster/tasks/tasks.json` |
| Secondary | `one integration at a time/.taskmaster/tasks/tasks.json` |

To update task status:
```bash
task-master set-status --id=<id> --status=done
```

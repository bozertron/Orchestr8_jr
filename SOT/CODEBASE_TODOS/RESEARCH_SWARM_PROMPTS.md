# Research Swarm Prompts — Architecture Merge Validation

**Owner**: Antigravity (cross-lane synthesis)
**Date**: 2026-02-16
**Purpose**: 7 research agents + 1 synthesis agent. Deploy all research agents in parallel. Deploy synthesis agent after all 7 complete.
**Output location**: Each agent writes results to `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/research/`

---

## Agent Deployment Order

```
┌──────────────────────────────────────────────────────────────────────┐
│  PARALLEL RESEARCH PHASE (deploy all 7 simultaneously)              │
│                                                                      │
│  Agent 1: Color Token Drift Audit                                    │
│  Agent 2: sys.path Hack Elimination Plan                             │
│  Agent 3: orchestr8_next Structure Validation                        │
│  Agent 4: Founder Console Extraction Audit                           │
│  Agent 5: anywidget Code City Feasibility                            │
│  Agent 6: L1→L3 Violation Fix Design                                 │
│  Agent 7: Artifact Cleanup + Migration Order                         │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  SYNTHESIS PHASE (deploy after all 7 complete)                       │
│                                                                      │
│  Agent 8: Synthesis — compile all findings into final merge plan     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Shared Context (copy into every agent prompt)

```
SHARED CONTEXT — READ FIRST:

You are a research agent in the Orchestr8 project. You are executing ONE research task.

Key files for reference:
- Visual Token Lock: /home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md
- Agent Handbook: /home/bozertron/Orchestr8_jr/README.AGENTS
- Architecture Synthesis: /home/bozertron/a_codex_plan/.planning/research/ARCHITECTURE_SYNTHESIS.md
- Herd Deployment Plan: /home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/HERD_DEPLOYMENT_MVP.md
- MVP Roadmap: /home/bozertron/Orchestr8_jr/SOT/MVP_AUTOFORWARD_MASTER_ROADMAP.md
- Integration Strategy: /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/INTEGRATION_EXECUTION_STRATEGY.md
- P07 Status: /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/execution/checkins/P07/STATUS.md

Codebase locations:
- Orchestr8_jr (canonical): /home/bozertron/Orchestr8_jr/
- a_codex_plan (integration): /home/bozertron/a_codex_plan/
- or8_founder_console: /home/bozertron/or8_founder_console/
- mingos_settlement_lab: /home/bozertron/mingos_settlement_lab/
- 2ndFid_explorers: /home/bozertron/2ndFid_explorers/

Shared memory gateway: http://127.0.0.1:37888
Comms tool: /home/bozertron/Orchestr8_jr/scripts/agent_comms.sh

YOUR OUTPUT: Write your findings to a single markdown file at:
  /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/research/<YOUR_FILENAME>.md

When done, send a completion ping to shared memory via:
  /home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send <your_agent_id> codex P08 evidence false "<one-line summary of your findings>"
```

---

## AGENT 1: Color Token Drift Audit

**File**: `RESEARCH_01_COLOR_TOKEN_AUDIT.md`
**Mission**: Find every hardcoded color hex value across the entire codebase and identify which ones disagree with `VISUAL_TOKEN_LOCK.md`.

### Task

1. Read `/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md` — this is the single source of truth for all color tokens.

2. Search ALL of the following files/directories for hardcoded hex color values (#XXXXXX or 0xXXXXXX format):
   - `/home/bozertron/Orchestr8_jr/IP/` (all .py, .js, .css, .html files)
   - `/home/bozertron/a_codex_plan/orchestr8_next/` (all .py files)
   - `/home/bozertron/or8_founder_console/` (all .py files)
   - `/home/bozertron/mingos_settlement_lab/` (all files)

3. For each hex value found, determine:
   - Does this value match a locked token?
   - Which locked token does it correspond to?
   - If it doesn't match, what should it be?

4. **Known conflict to verify**: `06_maestro.py` line 20 uses `#B8860B` for `gold-dark`, but the token lock specifies `#C5A028`. `woven_maps.py` line 62 has the same `#B8860B`. Verify if ANY other files reference `#B8860B`.

5. Produce a table:

   ```
   | File | Line | Current Value | Should Be | Token Name | Status |
   ```

6. Count total conflicts and estimate fix effort (minutes per file).

### Deliverable

Complete audit table showing every color in every file, with PASS/FAIL status per locked token.

---

## AGENT 2: sys.path Hack Elimination Plan

**File**: `RESEARCH_02_SYSPATH_ELIMINATION.md`
**Mission**: For each of the 6 known `sys.path` hacks, design a specific fix that preserves functionality.

### Task

1. Read and understand each hack:
   - `/home/bozertron/Orchestr8_jr/IP/plugins/06_maestro.py` lines 52-53
   - `/home/bozertron/Orchestr8_jr/IP/plugins/04_connie_ui.py` lines 97, 208, 281
   - `/home/bozertron/Orchestr8_jr/IP/plugins/08_director.py` line 272

2. For each hack, answer:
   - What module does it need to import?
   - Why can't that module be imported normally?
   - What would break if this hack was removed?
   - What is the minimal fix (e.g., relative import, package restructure, `__init__.py` addition)?

3. Investigate whether the `notebooks/` directory proposal from ARCHITECTURE_SYNTHESIS.md would eliminate the need for ALL of these hacks. Specifically:
   - If `orchestr8.py` moved from `IP/plugins/` to a top-level `notebooks/` dir
   - And `orchestr8_next` was installed as a package (`pip install -e .`)
   - Would all 6 hacks become unnecessary?

4. Test (dry-run) by checking import chains:

   ```bash
   cd /home/bozertron/a_codex_plan && python -c "import orchestr8_next; print('OK')"
   ```

5. Check if `04_connie_ui.py` has ANY other import issues beyond sys.path (e.g., circular deps, missing modules).

### Deliverable

Per-hack fix plan with exact code changes, risk assessment, and a recommendation on whether to fix incrementally or do a wholesale move to `notebooks/`.

---

## AGENT 3: orchestr8_next Structure Validation

**File**: `RESEARCH_03_STRUCTURE_VALIDATION.md`
**Mission**: Validate the proposed canonical structure against what actually exists in `orchestr8_next/` and identify renames vs additions.

### Task

1. Map the current `orchestr8_next/` structure:

   ```bash
   find /home/bozertron/a_codex_plan/orchestr8_next -type f -name "*.py" | sort
   ```

2. Compare against the proposed structure in ARCHITECTURE_SYNTHESIS.md Section 6.

3. For each dir in the proposed structure, classify:
   - **EXISTS_ALIGNED**: Dir exists with the proposed name ✅
   - **EXISTS_RENAMED**: Dir exists but under a different name (identify both names)
   - **NEW**: Dir doesn't exist yet, needs to be created
   - **CONFLICT**: Proposed dir would conflict with existing structure

4. Specifically investigate these potential conflicts:
   - `bus/` (proposed) vs `shell/` (exists) — are these the same thing?
     - Compare `bus/actions.py` proposal against `shell/actions.py` that exists
     - Compare `bus/store.py` proposal against `shell/store.py` that exists
   - `bridge/` (proposed) vs `comms/` (exists) — are these the same thing?
     - Compare `bridge/envelopes.py` proposal against `comms/envelopes.py` that exists
   - `visualization/` (proposed) vs `city/` (exists) — what's the boundary?

5. For each conflict, recommend: rename, merge, or keep both?

6. Check import chains — how many existing test files would break if dirs were renamed?

   ```bash
   grep -r "from orchestr8_next.shell" /home/bozertron/a_codex_plan/tests/ | wc -l
   grep -r "from orchestr8_next.comms" /home/bozertron/a_codex_plan/tests/ | wc -l
   ```

### Deliverable

Side-by-side comparison table of proposed vs actual structure, with rename-impact counts, and a clear recommendation on what to keep/rename/create.

---

## AGENT 4: Founder Console Extraction Audit

**File**: `RESEARCH_04_FC_EXTRACTION_AUDIT.md`
**Mission**: Produce an accurate extraction manifest for `or8_founder_console` with correct file counts, layer assignments, and integration dependencies.

### Task

1. Inventory every Python file:

   ```bash
   find /home/bozertron/or8_founder_console -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" -not -path "*/.pytest_cache/*" | sort
   ```

2. For each file, determine:
   - Layer assignment (L1 presentation, L2 bus, L3 service, L4 visualization, L5 bridge)
   - External dependencies (what does it import?)
   - Shared memory integration (does it call the memory gateway?)
   - SettingsService consumability (could it use `get_setting`/`set_setting`?)

3. Read the B7 guidance to FC (obs #1732 in shared memory) and check:
   - Does `services/intent_scanner.py` exist and what does it do?
   - Does `routers/review.py` have an action schema compatible with `command_surface`?
   - Is there a config reader interface?

4. Evaluate: should FC remain a separate FastAPI app or merge into `orchestr8_next`?
   - Check if FC has its own `requirements.txt` / `pyproject.toml`
   - Check if FC tests run independently
   - Check what port FC runs on and whether it has its own `main.py`

5. Compare the ARCHITECTURE_SYNTHESIS.md FC manifest (Section 4.3) against your actual findings.

### Deliverable

Corrected extraction manifest with actual file count, accurate layer assignments, and a clear keep-separate vs merge recommendation with justification.

---

## AGENT 5: anywidget Code City Feasibility

**File**: `RESEARCH_05_ANYWIDGET_FEASIBILITY.md`
**Mission**: Determine exactly how to replace the current Code City HTML/JS injection with an anywidget, and estimate the effort.

### Task

1. Verify anywidget is installed and working:

   ```bash
   python3 -c "import anywidget; print(anywidget.__version__)"
   python3 -c "import marimo as mo; print(mo.__version__)"
   ```

2. Read the current Code City rendering pipeline (follow the full chain):
   - `/home/bozertron/Orchestr8_jr/IP/woven_maps.py` — data structures, HTML generation
   - `/home/bozertron/Orchestr8_jr/IP/static/woven_maps_3d.js` — Three.js rendering
   - `/home/bozertron/Orchestr8_jr/IP/static/woven_maps_template.html` — HTML template
   - `/home/bozertron/Orchestr8_jr/IP/features/code_city/graph_builder.py` — graph data
   - `/home/bozertron/Orchestr8_jr/IP/features/code_city/render.py` — rendering entry

3. Document the current data flow:

   ```
   graph_builder.py → woven_maps.py → HTML string → mo.Html() → browser
   ```

4. Design the anywidget replacement:
   - What Python class would wrap the Three.js Code City?
   - What traitlets would it expose? (node data, health status, camera state, click events)
   - How would `mo.ui.anywidget()` wrap it?
   - Would the existing `woven_maps_3d.js` work inside an anywidget ESM module?

5. Check if the current static asset 404 problem (`gradient.png`, `noise.png`, fonts, `main.tsx`) would be solved by anywidget (since anywidget bundles its own assets via ESM).

6. Research anywidget's binary data support (`traitlets.Bytes()`) — can it efficiently pass the graph data (how many nodes in typical Code City scan)?

   ```bash
   cd /home/bozertron/Orchestr8_jr && python3 -c "
   from IP.features.code_city.graph_builder import build_graph
   g = build_graph('.')
   print(f'nodes={len(g.get(\"nodes\",[]))}, edges={len(g.get(\"edges\",[]))}')
   "
   ```

7. Estimate effort (hours) for the migration and identify risks.

### Deliverable

Feasibility assessment with proposed anywidget class design, data flow diagram, effort estimate, and a GO/NO-GO recommendation with reasoning.

---

## AGENT 6: L1→L3 Violation Fix Design

**File**: `RESEARCH_06_L1_L3_FIX_DESIGN.md`
**Mission**: Design L2 service facades that fix the 4 cross-layer violations without breaking any existing functionality.

### Task

1. Read `06_maestro.py` (the entire file) and identify ALL direct imports that violate L1→L3:

   ```bash
   grep -n "^from IP\.\|^import IP\." /home/bozertron/Orchestr8_jr/IP/plugins/06_maestro.py
   ```

2. For each violating import, answer:
   - What exactly does the plugin use from this import? (functions, classes, constants)
   - Is it used for data or for side effects?
   - Could a thin L2 facade provide this?

3. Read `04_connie_ui.py` and `03_gatekeeper.py` — confirm the L1→L3 violations:

   ```bash
   grep -n "^from IP\.\|^import IP\." /home/bozertron/Orchestr8_jr/IP/plugins/04_connie_ui.py
   grep -n "^from IP\.\|^import IP\." /home/bozertron/Orchestr8_jr/IP/plugins/03_gatekeeper.py
   ```

4. Read `woven_maps.py` imports to check L4→L3/L5 violations:

   ```bash
   head -40 /home/bozertron/Orchestr8_jr/IP/woven_maps.py
   ```

5. Design L2 facade modules. For example:

   ```python
   # orchestr8_next/shell/health_facade.py (L2)
   from orchestr8_next.services.health import HealthChecker  # L3 → L3 OK
   
   class HealthFacade:
       def get_results(self) -> dict: ...
       def start_watching(self, root: Path) -> None: ...
   ```

6. For each facade, specify:
   - Exact file path
   - Interface (methods + return types)
   - Which L3 imports it wraps
   - Which L1 files would switch to importing it
   - Test plan

7. Check if `orchestr8_next/shell/` already has anything that acts as a facade — don't duplicate existing work.

### Deliverable

Facade design document with file paths, interfaces, implementation stubs, migration steps per violating file, and test verification plan.

---

## AGENT 7: Artifact Cleanup + Migration Order

**File**: `RESEARCH_07_CLEANUP_MIGRATION_ORDER.md`
**Mission**: Produce the exact cleanup commands and validated migration phase order.

### Task

1. Inventory ALL artifact clutter in `a_codex_plan/` root:

   ```bash
   ls -la /home/bozertron/a_codex_plan/*.txt /home/bozertron/a_codex_plan/*.md /home/bozertron/a_codex_plan/*.log 2>/dev/null
   ```

2. Classify each file:
   - **MOVE**: Should go to `.planning/artifacts/` (reports, test outputs)
   - **DELETE**: Temporary/disposable (log files, intermediate outputs)
   - **KEEP**: Legitimately belongs in root (README, requirements.txt, etc.)

3. Generate the exact `mv` and `mkdir -p` commands needed:

   ```bash
   mkdir -p /home/bozertron/a_codex_plan/.planning/artifacts/P07
   mv /home/bozertron/a_codex_plan/B1_INTEGRATION_SMOKE_REPORT.md /home/bozertron/a_codex_plan/.planning/artifacts/P07/
   # ... etc
   ```

4. Now research the MIGRATION PHASE ORDER. Read these files:
   - ARCHITECTURE_SYNTHESIS.md (Section: Migration Phases)
   - HERD_DEPLOYMENT_MVP.md (Sprint structure)
   - Current test count: `cd /home/bozertron/a_codex_plan && python -m pytest tests/ --co -q 2>/dev/null | tail -1`

5. Evaluate this proposed phase order and validate against risk:

   ```
   Phase 0: Fix color token hardcodes (2 files, ~4 lines)
   Phase 1: Clean artifact clutter (33 files, mv commands only)
   Phase 2: Fix 04_connie_ui.py sys.path hacks (1 file, 3 locations)
   Phase 3: Add L2 service facades for 06_maestro.py (new files, no breaking changes)
   Phase 4: woven_maps.py import restructure (harder, touches rendering)
   ```

6. For each phase:
   - What is the test gate? (which tests must pass after this phase?)
   - What is the rollback plan if tests break?
   - Can this phase be done independently of the others?
   - Estimated time (hours)?

7. Check if any phase has hidden dependencies on another (e.g., does Phase 3 require Phase 2 to be done first?).

### Deliverable

Exact cleanup commands (copy-pasteable), validated phase order with test gates and rollback plans, and a dependency graph between phases.

---

## AGENT 8: SYNTHESIS (Deploy AFTER Agents 1-7 complete)

**File**: `RESEARCH_08_SYNTHESIS_FINAL_PLAN.md`
**Mission**: Read all 7 research reports and compile into one actionable merge plan.

### Task

1. Read all 7 research reports from:

   ```
   /home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/research/
   ```

2. For the synthesis, produce these sections:

   **A. Executive Summary**
   - One paragraph: what is the overall state of merge readiness?
   - Top 3 risks
   - Top 3 quick wins

   **B. Validated Architecture**
   - Final structure diagram (incorporating Agent 3's findings)
   - Which dirs to keep as-is, which to create new
   - ANY naming changes (only if Agent 3 found compelling reason)

   **C. Color Token Reconciliation**
   - From Agent 1: complete list of fixes needed
   - Proposed implementation: should tokens be hardcoded or read from SettingsService via `get_visual_tokens()`?

   **D. Import Health Roadmap**
   - From Agents 2 + 6: combined sys.path + L1→L3 fix plan
   - Ordered by dependency and risk

   **E. anywidget Decision**
   - From Agent 5: GO/NO-GO with justification
   - If GO: which sprint in the herd plan does it fit?

   **F. FC Integration Decision**
   - From Agent 4: keep-separate vs merge, with evidence

   **G. Phased Migration Plan**
   - From Agent 7: validated phase order with gates
   - Cross-referenced with herd plan sprints
   - Timeline estimate

   **H. Acceptance Criteria**
   - From ARCHITECTURE_SYNTHESIS.md Section 7: are these still valid?
   - Any additions from the research?

3. Cross-reference findings for contradictions:
   - Does Agent 2 recommend something that conflicts with Agent 3?
   - Does Agent 5's anywidget plan change Agent 6's facade design?
   - Does Agent 4's FC recommendation affect Agent 7's migration order?

4. Resolve any contradictions with explicit reasoning.

5. Produce a final "EXECUTE THIS" section with numbered steps that an agent herd can immediately act on.

### Deliverable

Single authoritative merge plan that supersedes all prior documents. This becomes the canonical reference for the integration sprints.

### After completion

Post the final plan to shared memory:

```bash
/home/bozertron/Orchestr8_jr/scripts/agent_comms.sh send synthesis codex P08 evidence true "MERGE PLAN COMPLETE: <one-line summary with key decisions>"
```

---

## Quick Reference: Agent → Filename

| Agent | ID | Output File |
|-------|------|-------------|
| 1 | color_audit | `RESEARCH_01_COLOR_TOKEN_AUDIT.md` |
| 2 | syspath_fix | `RESEARCH_02_SYSPATH_ELIMINATION.md` |
| 3 | structure_val | `RESEARCH_03_STRUCTURE_VALIDATION.md` |
| 4 | fc_audit | `RESEARCH_04_FC_EXTRACTION_AUDIT.md` |
| 5 | anywidget | `RESEARCH_05_ANYWIDGET_FEASIBILITY.md` |
| 6 | l1l3_fix | `RESEARCH_06_L1_L3_FIX_DESIGN.md` |
| 7 | cleanup | `RESEARCH_07_CLEANUP_MIGRATION_ORDER.md` |
| 8 | synthesis | `RESEARCH_08_SYNTHESIS_FINAL_PLAN.md` |

All output goes to: `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/research/`

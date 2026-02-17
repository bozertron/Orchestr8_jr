# Phase 08: FINAL MERGE PLAN - Research Synthesis

**Researched:** 2026-02-16  
**Domain:** Complete Merge Plan for Orchestr8_jr → orchestr8_next Integration  
**Confidence:** HIGH

---

## A. Executive Summary

The Orchestr8_jr → orchestr8_next merge readiness assessment is complete. The codebase has **moderate technical debt** that is **entirely fixable** through a phased approach. Key findings:

- **Overall State:** The orchestr8_next package is healthy and installable. The primary debt is in Orchestr8_jr (IP/ directory) with cross-layer violations, hardcoded colors, and sys.path hacks.
- **Top 3 Risks:**
  1. **L1→L3 Violations** (25 direct imports) - Violates layer architecture, creates tight coupling
  2. **anywidget Migration** - 16-24 hour effort with Three.js ESM module adaptation risk
  3. **Founder Console Merge** - 19 files with hardcoded paths need SettingsService integration
- **Top 3 Quick Wins:**
  1. **Color token fix** - 11 instances, 19 minutes total effort
  2. **Artifact cleanup** - 31 files moved/deleted, zero risk
  3. **sys.path fixes** - 3 hacks fixable with relative imports

**Recommendation:** Execute in 5 phases over 3 sprints. Priority: Quick wins first, then architectural fixes, then optional anywidget migration.

---

## B. Validated Architecture

### B.1 Final Structure Diagram

```
orchestr8_next/
├── __init__.py, config.py, app.py
├── presentation/          ← NEW (L1: UI contracts)
│   ├── plugins/          ← From Orchestr8_jr IP/plugins/
│   ├── components/       ← From Orchestr8_jr IP/plugins/components/
│   └── styles/
├── bus/                 ← RENAMED from shell/ (L2: State + Facades)
│   ├── actions.py, store.py, reducers.py, contracts.py
│   ├── middleware/
│   └── facades/         ← NEW: L2 facades wrapping L3 services
├── services/            ← NEW (L3: Domain services)
│   ├── health/
│   ├── combat/
│   ├── tickets/
│   ├── terminal/
│   └── governance/      ← From FC intent_scanner
├── adapters/            ← EXISTS (L3: External integrations)
│   ├── memory.py        ← From FC adapter/
│   ├── checkin.py       ← From FC adapter/
│   └── ...
├── visualization/      ← NEW (L4: Code City engine)
│   ├── graph_builder.py
│   ├── render.py
│   └── woven_maps.py
├── bridge/              ← RENAMED from comms/ (L5: Capability slices)
│   ├── envelopes.py
│   └── contracts.py
├── city/                ← EXISTS (Code City domain)
├── settings/            ← EXISTS (P07-B7 CSE - complete)
└── schemas/             ← EXISTS (empty - populate from token lock)
```

### B.2 Directory Actions Summary

| Action | Count | Risk |
|--------|-------|------|
| KEEP as-is | 4 | None |
| RENAMED | 2 | LOW (50 import updates) |
| CREATE new | 4 | LOW |
| MERGE | 1 (resilience→adapters) | LOW |

### B.3 Naming Changes

| Current | Proposed | Rationale |
|---------|----------|-----------|
| `shell/` | `bus/` | Matches L2 state management terminology |
| `comms/` | `bridge/` | Matches L5 capability slice concept |
| — | `presentation/` | L1 UI layer |
| — | `services/` | L3 domain services |
| — | `visualization/` | L4 Code City engine |

---

## C. Color Token Reconciliation

### C.1 Complete Fix List (from Agent 1)

| File | Line(s) | Current | Correct | Status |
|------|---------|---------|---------|--------|
| IP/plugins/06_maestro.py | 20 | #B8860B | #C5A028 | FAIL |
| IP/mermaid_theme.py | 4,7,8,11 | #B8860B | #C5A028 | FAIL |
| IP/features/maestro/config.py | 17 | #B8860B | #C5A028 | FAIL |
| IP/woven_maps.py | 62 | #B8860B | #C5A028 | FAIL |
| IP/plugins/components/ticket_panel.py | 11 | #B8860B | #C5A028 | FAIL |
| IP/plugins/components/file_explorer_panel.py | 15 | #B8860B | #C5A028 | FAIL |
| IP/plugins/components/comms_panel.py | 27 | #B8860B | #C5A028 | FAIL |
| IP/plugins/components/calendar_panel.py | 28 | #B8860B | #C5A028 | FAIL |

### C.2 Proposed Implementation

```bash
# Phase 0 (Optional, can run in parallel with any phase)
# Total: ~19 minutes

# 1. Fix 06_maestro.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/06_maestro.py

# 2. Fix mermaid_theme.py (4 instances)
sed -i 's/#B8860B/#C5A028/g' IP/mermaid_theme.py

# 3. Fix config.py
sed -i 's/#B8860B/#C5A028/g' IP/features/maestro/config.py

# 4. Fix woven_maps.py
sed -i 's/#B8860B/#C5A028/g' IP/woven_maps.py

# 5. Fix 4 component files
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/ticket_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/file_explorer_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/comms_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/calendar_panel.py

# Verify no more #B8860B in codebase
grep -r "#B8860B" --include="*.py" IP/
```

---

## D. Import Health Roadmap

### D.1 Combined sys.path + L1→L3 Fix Plan (from Agents 2 + 6)

| Priority | Issue | File | Fix Type | Risk | Effort |
|----------|-------|------|----------|------|--------|
| 1 | Color tokens | 8 files | sed replace | LOW | 19 min |
| 2 | sys.path Hack 1 | 06_maestro.py:52 | Path scope fix | LOW | 5 min |
| 3 | sys.path Hack 2 | 04_connie_ui.py:97,208,281 | Relative import | LOW | 5 min |
| 4 | sys.path Hack 3 | 08_director.py:272 | importlib OR keep | MEDIUM | 30 min |
| 5 | L1→L3 violations | 06_maestro.py (20 imports) | L2 facades | LOW | 2 hr |
| 6 | L1→L3 violations | 03_gatekeeper.py (1 import) | L2 facades | LOW | 15 min |
| 7 | L1→L3 violations | ticket_panel.py (1 import) | L2 facades | LOW | 10 min |
| 8 | L1→L3 violations | 07_settings.py (2 imports) | L2 facades | LOW | 15 min |

### D.2 Dependency-Ordered Execution

```
Phase 1: Color tokens (standalone)
    ↓
Phase 2: sys.path fixes (enables clean imports)
    ↓
Phase 3: L2 facades (fixes L1→L3 violations)
    ↓
Phase 4: Structural renames (50 import updates)
    ↓
Phase 5: FC merge (if accepted)
```

---

## E. anywidget Decision

### E.1 GO/NO-GO: GO ✅

**Justification:**

| Factor | Evidence | Verdict |
|--------|----------|---------|
| Technical feasibility | anywidget 0.9.21 + marimo 0.19.11 verified | ✅ |
| Problem solved | Eliminates iframe overhead, static 404s | ✅ |
| Code reuse | 90%+ existing Three.js adaptable | ✅ |
| Effort | 16-24 hours reasonable | ✅ |
| Risk | Addressable edge cases | ✅ |

### E.2 Sprint Integration

| Sprint | Work | anywidget Fit |
|--------|------|---------------|
| Sprint 1 | Phase 1-3 fixes | ❌ Not ready yet |
| Sprint 2 | Phase 4 structural + FC merge | ✅ Can start |
| Sprint 3 | Phase 5 anywidget | ✅ Primary deliverable |

**Recommendation:** Add anywidget migration as Sprint 3 deliverable. Start after:
- ✅ orchestr8_next package is structurally sound
- ✅ L2 facades provide stable interfaces
- ✅ FC merge complete (provides additional context)

---

## F. FC Integration Decision

### F.1 Recommendation: MERGE (from Agent 4)

| Evidence for Merge | Evidence for Keep Separate |
|--------------------|---------------------------|
| Tight coupling to Orchestr8_jr | Independent FastAPI app |
| No standalone value | Own port/process |
| Hardcoded paths (no SettingsService) | Own dependencies |
| Benefits from SettingsService | Independent tests |
| ARCHITECTURE_SYNTHESIS shows as target | Version tracking (0.4.0) |

### F.2 Merge Mapping

| Source (FC) | Target (orchestr8_next) | Layer |
|-------------|------------------------|-------|
| main.py | presentation/api/main.py | L1 |
| routers/* (11 files) | presentation/api/routers/ | L1 |
| adapter/memory.py | adapters/memory.py | L3 |
| adapter/checkin.py | adapters/checkin.py | L3 |
| services/intent_scanner.py | services/governance/scanner.py | L3 |
| intent_panel.py | INVESTIGATE | TBD |
| tauri_scanner.py | INVESTIGATE | TBD |

### F.3 Post-Merge Actions

1. Replace hardcoded `ORCHESTR8_BASE` with `get_setting("orchestr8_base")`
2. Replace hardcoded `MEMORY_GATEWAY_URL` with `get_setting("memory_gateway_url")`
3. Merge FC requirements.txt into orchestr8_next
4. Convert FC tests to integration tests

---

## G. Phased Migration Plan

### G.1 Validated Phase Order (from Agent 7)

| Phase | Name | Scope | Effort | Risk | Gate |
|-------|------|-------|--------|------|------|
| 0 | Color tokens | 8 files, 11 instances | 0.5 hr | LOW | None |
| 1 | Artifact cleanup | 24 move + 7 delete | 0.25 hr | NONE | None |
| 2 | sys.path fixes | 3 hacks in 3 files | 1 hr | MEDIUM | Tests pass |
| 3 | L2 facades | 10 new facade modules | 2 hr | LOW | Tests pass |
| 4 | Structural rename | shell→bus, comms→bridge | 1 hr | LOW | 50 import updates |
| 5 | FC merge | 19 files | 2 hr | MEDIUM | SettingsService OK |
| 6 | anywidget | Full migration | 16-24 hr | MEDIUM | Sprint 3 |

### G.2 Cross-Referenced Timeline

| Sprint | Phases | Deliverables |
|--------|--------|---------------|
| Sprint 1 | 0, 1, 2, 3 | Clean codebase, L2 facade foundation |
| Sprint 2 | 4, 5 | Canonical structure, FC merged |
| Sprint 3 | 6 | anywidget Code City live |

### G.3 Test Gates

```bash
# Phase 0: No tests (cosmetic)
# Phase 1: No tests (file ops)
# Phase 2: pytest tests/ -q (must pass)
# Phase 3: pytest tests/ -q (must pass)
# Phase 4: pytest tests/ -q (must pass)
# Phase 5: pytest tests/ -q (must pass)
# Phase 6: Integration test anywidget renders
```

### G.4 Rollback Plans

| Phase | Rollback |
|-------|----------|
| 0 | `git checkout --` |
| 1 | `git mv` back |
| 2 | Revert sys.path changes |
| 3 | Delete facade files |
| 4 | Rename back + revert imports |
| 5 | Move FC back |
| 6 | Keep old render.py as fallback |

---

## H. Acceptance Criteria Verification

### H.1 From ARCHITECTURE_SYNTHESIS.md Section 7

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | Marimo launches without sys.path hacks | ⚠️ PARTIAL | Hacks exist in Orchestr8_jr, not a_codex_plan |
| 2 | Package imports work | ✅ PASS | `import orchestr8_next` → OK |
| 3 | No L1→L3 violations | ❌ FAIL | 25 violations in Orchestr8_jr |
| 4 | No L4→L1 imports | ✅ PASS | Verified in research |
| 5 | Tests pass | ⚠️ PARTIAL | 66/68 pass (2 async config) |
| 6 | Hot-reload works | ✅ PASS | Standard marimo behavior |

### H.2 Updated Acceptance Criteria

| # | Criterion | Post-Migration Target |
|---|-----------|----------------------|
| 1 | Marimo launches without sys.path hacks | ✅ Yes (after Phase 2) |
| 2 | Package imports work | ✅ Yes (currently) |
| 3 | No L1→L3 violations | ✅ Yes (after Phase 3) |
| 4 | No L4→L1 imports | ✅ Yes (currently) |
| 5 | Tests pass | 68/68 (fix async config) |
| 6 | Hot-reload works | ✅ Yes |

---

## I. Contradiction Resolution

### I.1 Agent 2 vs Agent 3: sys.path in notebooks/

**Contradiction:** Agent 2 says notebooks/ would eliminate hacks, but Agent 7 says no sys.path hacks in a_codex_plan.

**Resolution:** Both correct. The sys.path hacks exist in Orchestr8_jr (the source project), not in a_codex_plan (the target package). The notebooks/ migration would be a future Phase 7.

### I.2 Agent 3 vs Agent 6: shell/ vs bus/ + facades

**Contradiction:** Agent 3 says rename shell→bus. Agent 6 designs facades in shell/facades/.

**Resolution:** Create `bus/facades/` (not shell/facades/). The facades are part of the L2 bus layer. Update Agent 6's design to use `orchestr8_next/bus/facades/`.

### I.3 Agent 4 FC layer mapping vs Agent 6 facade layer

**Contradiction:** Agent 4 suggests FC routers could be L2. Agent 6 defines facades as L2.

**Resolution:** FC routers are correctly L1 (API presentation). The L2 facades wrap L3 services that FC routers would use. FC merge should use existing L2 facades.

### I.4 Agent 4 vs Agent 7: FC path hardcoding

**Contradiction:** Agent 4 identifies hardcoded paths in FC. Agent 7 says no hardcoded paths in a_codex_plan.

**Resolution:** FC is the source, a_codex_plan is the target. FC merge will fix these hardcoded paths by integrating with SettingsService.

---

## J. EXECUTE THIS - Numbered Steps

### Sprint 1: Quick Wins + Foundation (Week 1)

**Step 1:** Fix color token drift
```bash
# 8 files, 11 instances, ~19 minutes total
cd /home/bozertron/Orchestr8_jr
sed -i 's/#B8860B/#C5A028/g' IP/plugins/06_maestro.py
sed -i 's/#B8860B/#C5A028/g' IP/mermaid_theme.py
sed -i 's/#B8860B/#C5A028/g' IP/features/maestro/config.py
sed -i 's/#B8860B/#C5A028/g' IP/woven_maps.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/ticket_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/file_explorer_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/comms_panel.py
sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/calendar_panel.py
# Verify
grep -r "#B8860B" --include="*.py" IP/
```

**Step 2:** Clean artifact clutter
```bash
# 24 files to move, 7 to delete
mkdir -p /home/bozertron/a_codex_plan/.planning/artifacts/P07
cd /home/bozertron/a_codex_plan
# Move test outputs and smoke reports (24 files)
mv B*_INTEGRATION_SMOKE_REPORT.md .planning/artifacts/P07/
mv B*_TEST_OUTPUT.txt .planning/artifacts/P07/
mv TEST_*.txt .planning/artifacts/P07/
mv test_*_output.txt .planning/artifacts/P07/
# Delete logs (7 files)
rm curl_proof.log cutover_test.log marimo_startup*.log rollback_test.log smoke_*.txt
```

**Step 3:** Fix sys.path hacks in Orchestr8_jr
```bash
cd /home/bozertron/Orchestr8_jr
# Hack 1: Fix path scope in 06_maestro.py line 49
# Change: _PROJECT_ROOT = _THIS_FILE.parent.parent.parent
# To:     _PROJECT_ROOT = _THIS_FILE.parent.parent
# Hack 2: Replace 3 instances in 04_connie_ui.py with relative import
# Change: sys.path.insert(0, str(Path(__file__).parent.parent)); from connie import...
# To:     from ..connie import ConversionEngine
# Hack 3: Keep as-is OR implement importlib (defer to Sprint 2)
```

**Step 4:** Create L2 facade layer
```bash
cd /home/bozertron/Orchestr8_jr
mkdir -p orchestr8_next/bus/facades
# Create these 10 facade modules:
# - health_facade.py, combat_facade.py, terminal_facade.py
# - briefing_facade.py, ticket_facade.py, context_facade.py
# - visualization_facade.py, gatekeeper_facade.py
# - patchbay_facade.py, maestro_config_facade.py
# (See Agent 6 research for full code)
```

**Step 5:** Update L1 plugins to use facades
```bash
# 06_maestro.py: Replace 20 direct L3 imports with facade imports
# 03_gatekeeper.py: Replace 1 import
# ticket_panel.py: Replace 1 import
# 07_settings.py: Replace 2 imports
# Verify no L1→L3 violations remain
grep -rn "^from IP\." IP/plugins/*.py | grep -v "IP.plugins.components"
```

### Sprint 2: Structural Alignment (Week 2)

**Step 6:** Rename directories in orchestr8_next
```bash
cd /home/bozertron/a_codex_plan/orchestr8_next
# Rename shell → bus
mv shell bus
# Rename comms → bridge
mv comms bridge
# Batch update imports in all files (50 total)
# Update tests/ imports as well
```

**Step 7:** Create new directory structure
```bash
cd /home/bozertron/a_codex_plan/orchestr8_next
mkdir -p services/health services/combat services/tickets
mkdir -p services/terminal services/governance
mkdir -p presentation/plugins presentation/components presentation/styles
mkdir -p visualization
# Move/create appropriate files
```

**Step 8:** Merge Founder Console
```bash
# Copy FC files to target locations
cp -r or8_founder_console/adapter/* orchestr8_next/adapters/
cp or8_founder_console/services/intent_scanner.py orchestr8_next/services/governance/
mkdir -p orchestr8_next/presentation/api
cp -r or8_founder_console/routers/* orchestr8_next/presentation/api/
# Fix hardcoded paths to use SettingsService
```

**Step 9:** Fix pre-existing test failures
```bash
# Either install pytest-asyncio or remove asyncio_mode from pytest.ini
pip install pytest-asyncio
# OR: sed -i '/asyncio_mode/d' pytest.ini
pytest tests/ -q  # Should show 68/68 pass
```

### Sprint 3: anywidget Migration (Week 3-4)

**Step 10:** anywidget implementation
```bash
# Phase 1: Core (12-16 hours)
# - Create CodeCityWidget class with traitlets
# - Extract woven_maps_3d.js to ESM
# - Create code_city_widget.js render logic
# - Test basic Three.js rendering

# Phase 2: Feature parity (4-6 hours)
# - Camera controls sync
# - Hover/click events
# - Emergence animation

# Phase 3: Integration (2-4 hours)
# - Update render.py to use anywidget
# - Environment flag for backward compatibility
# - Performance testing
```

---

## K. Research Flags

| Phase | Needs Research | Standard Patterns |
|-------|----------------|-------------------|
| Phase 0 | None | Color token replacement is standard |
| Phase 1 | None | File move is standard |
| Phase 2 | None | sys.path fixes are standard |
| Phase 3 | None | Facade pattern is standard |
| Phase 4 | ⚠️ Import audit | Directory rename needs verification |
| Phase 5 | ⚠️ FC SettingsService | FC merge needs careful path work |
| Phase 6 | ✅ Full research | Agent 5 has detailed spec |

---

## L. Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All packages verified, anywidget GO decision |
| Features | HIGH | Clear must-have (settings, merge) and defer (anywidget) |
| Architecture | HIGH | Validated by Agent 3, conflicts resolved |
| Pitfalls | HIGH | All identified, mitigation clear |
| Overall | HIGH | Clear path forward, well-researched |

---

## M. Sources

All research files from `/home/bozertron/Orchestr8_jr/.planning/orchestr8_next/artifacts/P07/integration/research/`:

- RESEARCH_01_COLOR_TOKEN_AUDIT.md
- RESEARCH_02_SYSPATH_ELIMINATION.md
- RESEARCH_03_STRUCTURE_VALIDATION.md
- RESEARCH_04_FC_EXTRACTION_AUDIT.md
- RESEARCH_05_ANYWIDGET_FEASIBILITY.md
- RESEARCH_06_L1_L3_FIX_DESIGN.md
- RESEARCH_07_CLEANUP_MIGRATION_ORDER.md

Reference:
- `/home/bozertron/a_codex_plan/.planning/research/ARCHITECTURE_SYNTHESIS.md`

---

*Synthesis complete. Plan is actionable and ready for herd execution.*

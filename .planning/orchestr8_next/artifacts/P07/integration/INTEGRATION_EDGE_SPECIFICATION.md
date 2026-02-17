# Integration Edge Specification - Technical Stack Lock
**Generated:** 2026-02-16
**Status:** FOR FOUNDER APPROVAL

---

## Technical Stack Confirmed

### Runtime & Framework

| Component | Status | Source | Notes |
|-----------|--------|--------|-------|
| **Marimo** | ✅ PRIMARY | `orchestr8.py` entry point | Reactive Python notebook framework |
| **Tauri** | ✅ TARGET SHELL | Planned Phase C | Desktop packaging - NOT NOW |
| **Vite** | ❌ NOT USED | - | Not in current stack |
| **Vue/Collabkit** | ⚠️ REFERENCE ONLY | `/home/bozertron/JFDI - Collabkit/` | Source for patterns, NOT integrated |

### JavaScript Libraries

| Library | Status | Usage | Source |
|---------|--------|-------|--------|
| **Three.js r128** | ✅ ACTIVE | Code City 3D rendering | `IP/static/woven_maps_3d.js` |
| **Custom Particle System** | ✅ ACTIVE | Emergence effects | Built into `woven_maps_template.html` |
| **Particle.js** | ❌ NOT USED | - | Custom system used instead |
| **OrbitControls** | ✅ ACTIVE | 3D camera control | Loaded via CDN/local fallback |

### Python Dependencies

Current working set (minimal):
- `marimo` - Runtime framework
- `pandas` - Data handling
- `networkx` - Graph operations  
- `pyvis` - Visualization
- `jinja2` - Template rendering
- `toml` - Config parsing
- `anthropic` (optional) - LLM API

**No additional dependencies should be added without approval.**

### Settings System

| Component | Status | Location |
|-----------|--------|----------|
| **Settings Panel** | ✅ ACTIVE | `IP/plugins/07_settings.py` |
| **Settings Config** | ✅ ACTIVE | `pyproject_orchestr8_settings.toml` |
| **Font Profiles** | ✅ ACTIVE | `IP/styles/font_profiles.py` |

---

## Integration Edge Specification

### What is an "Integration Edge"?

An **integration edge** is a clearly defined boundary between two subsystems where:
1. Data contracts are explicit (input → output)
2. Development can happen in isolation
3. Integration testing is deterministic

### Edge Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION EDGES MAP                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐          │
│  │   SOURCE    │         │   STAGING   │         │   TARGET    │          │
│  │ (Orchestr8) │────────▶│  (2ndFid)   │────────▶│ (a_codex)   │          │
│  └─────────────┘         └─────────────┘         └─────────────┘          │
│        │                       │                       │                    │
│        ▼                       ▼                       ▼                    │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                    INTEGRATION EDGES                             │       │
│  │                                                                  │       │
│  │  EDGE-1: VISUAL TOKENS                                           │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ orchestr8.css   │──▶│ font_profiles.py │                   │       │
│  │  │ (tokens LOCKED) │   │ (runtime inject) │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ 06_maestro.py (render entry point)         │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  │  EDGE-2: CODE CITY RENDERING                                    │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ graph_builder   │──▶│ woven_maps.py    │                   │       │
│  │  │ (data model)    │   │ (render config)  │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ woven_maps_template.html (JS runtime)        │               │       │
│  │  │ - Three.js 3D                               │               │       │
│  │  │ - Custom particle system                    │               │       │
│  │  │ - WebGL/Canvas rendering                   │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  │  EDGE-3: HEALTH STATUS FLOW                                      │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ health_checker   │──▶│ health_watcher   │                   │       │
│  │  │ (analysis)      │   │ (state manager)  │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ graph_builder.build_from_health_results()   │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  │  EDGE-4: COMBAT TRACKING                                        │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ combat_tracker  │──▶│ combat_state.json │                   │       │
│  │  │ (write)         │   │ (persistence)     │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ graph_builder reads on rebuild               │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  │  EDGE-5: PANEL SYSTEM                                            │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ code_city_context│──▶│ deploy_panel.py  │                   │       │
│  │  │ (build payload)  │   │ (render)         │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ 06_maestro.py: handle_node_click()         │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  │  EDGE-6: CONTRACTS                                               │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ contracts/       │──▶│ All consumers    │                   │       │
│  │  │ *.py (schemas)  │   │ (read only)     │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │                                                                  │       │
│  │  EDGE-7: SETTINGS                                                │       │
│  │  ┌──────────────────┐   ┌──────────────────┐                   │       │
│  │  │ 07_settings.py  │──▶│ font_profiles   │                   │       │
│  │  │ (UI panel)       │   │ (runtime apply) │                   │       │
│  │  └──────────────────┘   └──────────────────┘                   │       │
│  │         │                         │                              │       │
│  │         ▼                         ▼                              │       │
│  │  ┌─────────────────────────────────────────────┐               │       │
│  │  │ orchestr8.css (tokens update)               │               │       │
│  │  └─────────────────────────────────────────────┘               │       │
│  │                                                                  │       │
│  └──────────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Edge-by-Edge Development Isolation

### EDGE-1: Visual Tokens

**Can be developed in isolation:** YES
**Test in isolation:** YES
**Integration test:** CSS variable changes reflected in 06_maestro

| Aspect | Details |
|--------|---------|
| Input | `VISUAL_TOKEN_LOCK.md` (source of truth) |
| Transform | `font_profiles.py` injects runtime tokens |
| Output | `orchestr8.css` applied to page |
| Test | Change token → refresh → verify color |
| Dev isolation | Edit CSS, reload marimo |

### EDGE-2: Code City Rendering

**Can be developed in isolation:** YES (with mock data)
**Test in isolation:** YES
**Integration test:** Full pipeline from graph to 3D render

| Aspect | Details |
|--------|---------|
| Input | `graph_builder.py` node/edge data |
| Transform | `woven_maps.py` config + template |
| Output | HTML with Three.js + particles |
| Test | Pass mock nodes → verify 3D output |
| Dev isolation | Unit test graph_builder, mock render |

### EDGE-3: Health Status Flow

**Can be developed in isolation:** PARTIAL
**Test in isolation:** YES (mock health results)
**Integration test:** Run health check → verify color

| Aspect | Details |
|--------|---------|
| Input | Health checker output (errors/warnings) |
| Transform | `graph_builder.build_from_health_results()` |
| Output | CodeNode with status |
| Test | Mock HealthCheckResult → verify status |
| Gap | Warnings not propagated (needs fix) |

### EDGE-4: Combat Tracking

**Can be developed in isolation:** YES
**Test in isolation:** YES
**Integration test:** Deploy → verify purple building

| Aspect | Details |
|--------|---------|
| Input | `combat_tracker.deploy(file, terminal, model)` |
| Transform | Write `combat_state.json` |
| Output | graph_builder reads, sets status="combat" |
| Test | Mock deploy → verify JSON → verify color |
| Gap | Refresh trigger (needs fix) |

### EDGE-5: Panel System

**Can be developed in isolation:** YES
**Test in isolation:** YES
**Integration test:** Click node → verify panel opens

| Aspect | Details |
|--------|---------|
| Input | `code_city_context.build_payload(node)` |
| Transform | `deploy_panel.show()` / `building info` |
| Output | Panel UI rendered |
| Test | Mock payload → verify panel content |
| Gap | Rich data not passed (needs fix) |

### EDGE-6: Contracts

**Can be developed in isolation:** YES
**Test in isolation:** YES
**Integration test:** Validate against contract schema

| Aspect | Details |
|--------|---------|
| Input | Data from any subsystem |
| Transform | `contracts/*.py` validate() |
| Output | Validated dict or raise |
| Test | Valid/invalid inputs → verify behavior |

### EDGE-7: Settings

**Can be developed in isolation:** YES
**Test in isolation:** YES
**Integration test:** Change setting → verify UI update

| Aspect | Details |
|--------|---------|
| Input | `pyproject_orchestr8_settings.toml` |
| Transform | `07_settings.py` reads/writes |
| Output | UI panel + CSS token injection |
| Test | Edit TOML → reload → verify |

---

## Agent Swarm Specification

### Swarm 1: Visual Stack (Mingos)

**Target:** EDGE-1, EDGE-2
**Goal:** Prove visual rendering in isolation

| Agent | Task | Deliverable |
|-------|------|-------------|
| V-1 | Token isolation test | Document showing CSS tokens work standalone |
| V-2 | Three.js render test | Prove 3D renders with mock data |
| V-3 | Particle system test | Verify particles render without full stack |
| V-4 | Settings → CSS flow | Verify font profile injection works |

### Swarm 2: Data Flow (2ndFid)

**Target:** EDGE-3, EDGE-4, EDGE-5
**Goal:** Prove data pipelines work

| Agent | Task | Deliverable |
|-------|------|-------------|
| D-1 | Health → color test | Document health→color works |
| D-2 | Combat → refresh test | Document deploy→refresh works |
| D-3 | Panel isolation test | Document panels render with mock |
| D-4 | Contract validation | Document contracts are complete |

### Swarm 3: Integration (a_codex)

**Target:** ALL EDGES
**Goal:** Full pipeline integration

| Agent | Task | Deliverable |
|-------|------|-------------|
| I-1 | Full stack test | End-to-end test document |
| I-2 | Performance test | Verify no regression |
| I-3 | Contract review | All contracts synced |
| I-4 | Visual parity | Match reference exactly |

---

## Decision Required: Foundation Reference

### Question: Which visual reference is canonical?

We have two final references:

| Reference | Location | Notes |
|-----------|----------|-------|
| **A** | `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html` | Human dashboard, static |
| **B** | `one integration at a time/UI Reference/MaestroView.vue` | Vue component, interactive |

**Current decision in SOT:** Reference A is canonical for layout/visuals.

---

## Recommended Agent Launch Order

### Phase 1: Technical Verification (1 day)

Send agents to verify:

1. **V-1:** Can we change a CSS token in orchestr8.css and see it in the UI without any other changes?
2. **V-2:** Can we render Three.js with mock data in isolation?
3. **D-6:** Are the contracts complete? Any missing schemas?

### Phase 2: Integration Prep (2 days)

Based on Phase 1 results:

1. **V-3:** Particle system isolation test
2. **D-1:** Health flow isolation test
3. **D-2:** Combat flow isolation test

### Phase 3: Full Integration (3 days)

1. **I-1:** Full stack end-to-end
2. **I-3:** Contract sync across all edges
3. **I-4:** Visual parity check

---

## Next Steps

**Requesting Founder Approval:**

1. ✅ Technical stack confirmed (Marimo + Three.js + Custom Particles)
2. ✅ Vite NOT used
3. ✅ Settings panel IS used from orchestr8_jr
4. ✅ Collabkit is REFERENCE ONLY, not integrated
5. ⚠️ **DECISION REQUIRED:** Which visual reference is canonical?

**Once approved, I can spawn the agent swarms with specific tasks.**

---

## Quick Reference Card (For Agents)

```
INTEGRATION EDGES (Memorize These):

1. VISUAL: VISUAL_TOKEN_LOCK.md → font_profiles.py → orchestr8.css → 06_maestro
2. CITY:   graph_builder → woven_maps → woven_maps_template.html (Three.js + particles)
3. HEALTH: health_checker → health_watcher → graph_builder → CodeNode.status
4. COMBAT: combat_tracker → combat_state.json → graph_builder → purple building
5. PANEL:  code_city_context → deploy_panel.py → UI
6. CONTRACTS: contracts/*.py → ALL (read-only consumers)
7. SETTINGS: 07_settings.py → font_profiles → orchestr8.css

DEPENDENCIES (What uses what):
- 06_maestro.py imports: ALL subsystems
- graph_builder imports: health_checker, combat_tracker, contracts
- woven_maps imports: NONE (pure config)
- 07_settings imports: font_profiles, contracts
```

---

**Ready to launch. Which visual reference (A or B) is canonical for the mingos_settlement_lab workspace to use?**
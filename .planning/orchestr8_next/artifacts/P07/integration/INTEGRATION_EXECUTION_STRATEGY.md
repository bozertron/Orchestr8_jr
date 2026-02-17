# Integration Execution Strategy - PoC Waves
**Generated:** 2026-02-16
**Status:** DRAFT - For Founder Alignment
**Argument A Confirmed:** Python + Frontend Scaffold First, Tauri Later

---

## Vision Recap

### Lane Responsibilities (CONFIRMED)

| Lane | Role |
|------|------|
| **Orchestr8_jr** | Canonical lane - UI contract authority, approval authority, final promotion |
| **a_codex_plan** | Core integration lane - marimo-first core integration, adapters, middleware, backend reliability |
| **2ndFid_explorers** | Extraction lane - component preparation staging ground, final QC before a_codex_plan |
| **mingos_settlement_lab** | PoC visual rendering - deliberate physical stack hierarchy to prevent transfer surprises |

### The Flow
```
Orchestr8_jr (source of truth)
    ↓ [component extraction]
2ndFid_explorers (staging + QC)
    ↓ [visual PoC]
mingos_settlement_lab (render validation)
    ↓ [final integration]
a_codex_plan (production integration)
```

---

## Subsystem Map - Current State

### Identified Working Subsystems in Orchestr8_jr

| # | Subsystem | Files | Status | Priority |
|---|-----------|-------|--------|----------|
| 1 | **Code City / Woven Maps** | `woven_maps.py`, `graph_builder.py`, `render.py` | Working | P0 |
| 2 | **Health Checking** | `health_checker.py`, `health_watcher.py` | Working | P0 |
| 3 | **Combat Tracking** | `combat_tracker.py` | Working | P0 |
| 4 | **File Lock (Louis)** | `louis_core.py` | Working | P1 |
| 5 | **Connection Verification** | `connection_verifier.py`, `patchbay.py` | Working | P1 |
| 6 | **Carl Contextualizer** | `carl_core.py` | Working | P1 |
| 7 | **Panel System** | `deploy_panel.py`, `ticket_panel.py`, etc. | Working | P0 |
| 8 | **Summon System** | In `06_maestro.py` | Working | P0 |
| 9 | **Mermaid Generator** | `mermaid_generator.py` | Working | P2 |
| 10 | **Terminal Spawner** | `terminal_spawner.py` | Working | P1 |
| 11 | **Settings System** | `07_settings.py`, `font_profiles.py` | Working | P1 |
| 12 | **Control Surface** | In `06_maestro.py` | Working | P0 |
| 13 | **Contracts** | `IP/contracts/*.py` | Working | P0 |
| 14 | **Audio/Effects** | `audio/*.py`, `effects/` | Experimental | P2 |

---

## Integration Wave Planning

### Wave Structure

Each wave = 1 integration checker agent analyzing 1 subsystem
Parallel execution within waves, sequential dependencies between waves

### Wave Assignments

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 0: FOUNDATION (Already Complete)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ - Visual Token Lock deployed to CSS                                    │
│ - Core test gates verified (11 passed)                                 │
│ - Health → Code City flow verified                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 1: CORE VISUAL STACK (Mingos Settlement Lab Focus)               │
├─────────────────────────────────────────────────────────────────────────┤
│ Subsystems: Code City, Health Checking, Combat Tracking               │
│ Purpose: Prove visual rendering stack before structural changes       │
│                                                                         │
│ 1.1 Code City + Graph Builder                                          │
│     - Status: Working (color mapping verified)                         │
│     - Gap: Combat refresh trigger (2-4 hrs)                            │
│     - Deliver: Visual PoC in mingos_settlement_lab                    │
│                                                                         │
│ 1.2 Health Checker Integration                                         │
│     - Status: Working                                                  │
│     - Gap: Warnings not propagated (8-11 hrs)                          │
│     - Deliver: Warning display in visual stack                         │
│                                                                         │
│ 1.3 Combat Tracker Visual                                              │
│     - Status: Working (purple buildings render)                        │
│     - Gap: Refresh trigger only                                        │
│     - Deliver: Proven deployment → refresh flow                        │
│                                                                         │
│ Owner: mingos_settlement_lab                                           │
│ Est: 2-3 days                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 2: INTERACTION LAYER (2ndFid_explorers Focus)                    │
├─────────────────────────────────────────────────────────────────────────┤
│ Subsystems: Panel System, Node Click Flow, Louis Lock                 │
│ Purpose: Prepare components for integration, QC before transfer       │
│                                                                         │
│ 2.1 Panel System (Deploy, Ticket, Comms, etc.)                        │
│     - Status: Working                                                  │
│     - Gap: Rich building data not passed to panels (4-6 hrs)          │
│     - Deliver: Staged in 2ndFid_explorers with contracts              │
│                                                                         │
│ 2.2 Node Click → Panel Flow                                            │
│     - Status: Working (broken → deploy panel)                          │
│     - Gap: Working nodes have no info panel (4-6 hrs)                 │
│     - Deliver: Complete click → panel flow in staging                 │
│                                                                         │
│ 2.3 Louis Lock Visual                                                  │
│     - Status: Data flows to building_panel                             │
│     - Gap: Not displayed in shell.py (1-2 hrs)                        │
│     - Deliver: Lock indicator in panel views                           │
│                                                                         │
│ Owner: 2ndFid_explorers                                                 │
│ Est: 2-3 days                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 3: CONNECTIVITY LAYER (2ndFid_explorers + a_codex_plan)          │
├─────────────────────────────────────────────────────────────────────────┤
│ Subsystems: Connection Verification, Carl Contextualizer, Terminal    │
│ Purpose: Backend integration, prepare for production                  │
│                                                                         │
│ 3.1 Connection Verifier / Patchbay                                     │
│     - Status: Working (dry_run and apply methods)                     │
│     - Integration: Needs clean contract interface                      │
│     - Deliver: Staged with API contracts in 2ndFid_explorers           │
│                                                                         │
│ 3.2 Carl Contextualizer                                                │
│     - Status: Working (gathers context, builds payload)               │
│     - Integration: Used by node click flow                             │
│     - Deliver: Context contracts defined, staged                       │
│                                                                         │
│ 3.3 Terminal Spawner                                                   │
│     - Status: Working                                                  │
│     - Integration: Called by deploy handlers                           │
│     - Deliver: Terminal API staged                                     │
│                                                                         │
│ Owner: 2ndFid_explorers → a_codex_plan                                 │
│ Est: 2-3 days                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 4: ORCHESTRATION (a_codex_plan Focus)                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Subsystems: Summon, Control Surface, Settings                         │
│ Purpose: Final integration in production workspace                     │
│                                                                         │
│ 4.1 Summon System                                                      │
│     - Status: Working                                                  │
│     - Integration: Wiring to context payload                           │
│     - Deliver: Full summon → context flow in a_codex_plan             │
│                                                                         │
│ 4.2 Control Surface                                                    │
│     - Status: Working                                                  │
│     - Integration: State management                                    │
│     - Deliver: Control deck in production                              │
│                                                                         │
│ 4.3 Settings System                                                    │
│     - Status: Working                                                  │
│     - Integration: Font profiles, visual config                        │
│     - Deliver: Settings in production                                  │
│                                                                         │
│ Owner: a_codex_plan                                                    │
│ Est: 2-3 days                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ WAVE 5: CONTRACT CONSOLIDATION (All Lanes)                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Purpose: Final QC, ensure no structural surprises                     │
│                                                                         │
│ 5.1 Contract Review                                                    │
│     - Verify all contracts in sync across lanes                        │
│     - Ensure no hidden wrapping problems                               │
│                                                                         │
│ 5.2 Test Gate Consolidation                                           │
│     - Canonical tests run in a_codex_plan                              │
│     - All 11 tests pass                                                │
│                                                                         │
│ 5.3 Visual Parity Check                                                │
│     - mingos_settlement_lab → a_codex_plan                             │
│     - No structural surprises                                          │
│                                                                         │
│ Owner: Orchestr8_jr (approval)                                         │
│ Est: 1-2 days                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points Matrix

```
SUBSYSTEM          ORCHESTR8_JR    2NDFID    MINGOS    A_CODEX_PLAN
                    (source)       (stage)   (visual)  (prod)
─────────────────────────────────────────────────────────────────────
Code City          ┌──────────┐
(Woven Maps)       │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 1    Wave 1      Wave 5

Health Checker     ┌──────────┐
                   │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 3    Wave 1      Wave 5

Combat Tracker     ┌──────────┐
                   │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 3    Wave 1      Wave 5

Panel System       ┌──────────┐
(Deploy, Ticket)   │ EXISTS   │──────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 2    Wave 2      Wave 4

Node Click Flow    ┌──────────┐
                   │ EXISTS   │──────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 2    Wave 2      Wave 4

Louis Lock         ┌──────────┐
                   │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 2    Wave 2      Wave 4

Connection Verify  ┌──────────┐
                   │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 3    -          Wave 4

Carl Context       ┌──────────┐
                   │ EXISTS   │───────────→ STAGE ──────→ INTEGRATE
                   └──────────┘   Wave 3    -          Wave 4

Summon System      ┌──────────┐
                   │ EXISTS   │───────────── - ────────→ INTEGRATE
                   └──────────┘              (skip)    Wave 4
```

---

## Physical Stack Hierarchy (Mingos Focus)

**Critical Requirement:** When building visual stack in mingos_settlement_lab, must mirror exact directory structure to prevent transfer surprises.

### Required Hierarchy Preservation

```
IP/                          (exact path required)
├── styles/
│   ├── orchestr8.css       ← Visual tokens live here
│   ├── font_profiles.py    ← Font injection
│   └── font_injection.py
├── static/
│   ├── woven_maps_*.js     ← 3D rendering (MUST MATCH)
│   └── woven_maps_template.html
├── features/
│   ├── code_city/
│   │   ├── graph_builder.py
│   │   └── render.py
│   └── maestro/
│       ├── code_city_context.py
│       └── views/
│           └── shell.py
├── plugins/
│   ├── 06_maestro.py       ← Entry point (MUST MATCH)
│   └── components/
│       └── *.py
└── contracts/
    └── *.py                ← All contracts sync
```

### Files That CANNOT Change Structure

| File | Why Critical |
|------|--------------|
| `IP/woven_maps.py` | Data structures define Code City schema |
| `IP/static/woven_maps_3d.js` | Client expects exact API |
| `IP/plugins/06_maestro.py` | Marimo cell reference |
| `IP/contracts/*.py` | Cross-lane contract agreements |
| `IP/styles/orchestr8.css` | Visual token lock |

---

## Gap Summary by Wave

### Wave 1 Gaps (Visual Stack)
| Gap | Hours | Owner |
|-----|-------|-------|
| Combat refresh trigger | 2-4 | mingos |
| Warnings propagation | 8-11 | mingos |
| Warning display in visual | 2-3 | mingos |

### Wave 2 Gaps (Interaction)
| Gap | Hours | Owner |
|-----|-------|-------|
| Rich data to deploy panel | 4-6 | 2ndFid |
| Working node info panel | 4-6 | 2ndFid |
| Lock display in shell | 1-2 | 2ndFid |

### Wave 3 Gaps (Connectivity)
| Gap | Hours | Owner |
|-----|-------|-------|
| Connection verifier contracts | 3-4 | 2ndFid |
| Carl context contracts | 2-3 | 2ndFid |

### Wave 4+5 (Orchestration)
| Gap | Hours | Owner |
|-----|-------|-------|
| Summon context wiring | 2-3 | a_codex |
| Test gate consolidation | 1 | a_codex |

---

## Execution Commands

### Phase Prep (Before Wave Start)
```bash
# Build collaboration spec
python scripts/phase_prep_builder.py init --output SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml

# Generate worklists
python scripts/phase_prep_builder.py render --spec SOT/CODEBASE_TODOS/NEXT_PHASE_COLLAB_WORKING.toml
```

### Wave 1 Launch (Mingos)
```bash
# Checkout wave 1
bash .taskmaster/tools/memory-gateway/memory-stack.sh start
bash scripts/packet_bootstrap.sh P07 WAVE1A mingos_settlement_lab
bash scripts/packet_lint.sh <prompt> <boundary>
```

### Wave 2 Launch (2ndFid)
```bash
# Parallel with wave 1
bash scripts/packet_bootstrap.sh P07 WAVE2A 2ndFid_explorers
```

### Validation Gate (After Each Wave)
```bash
# Run canonical tests
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py \
  tests/city/test_wiring_view.py tests/city/test_parity.py -q
# Expected: 11 passed
```

---

## Decision Points for Founder

### Before Wave 1
- [ ] Confirm Wave 1 scope for mingos_settlement_lab
- [ ] Confirm which gaps to fix now vs defer to Phase 08

### Before Wave 2  
- [ ] Confirm 2ndFid_explorers staging role
- [ ] Confirm QC checkpoint requirements

### Before Wave 3
- [ ] Confirm connectivity layer scope
- [ ] Confirm a_codex_plan integration readiness

### Before Wave 4
- [ ] Confirm production integration path
- [ ] Confirm Tauri packaging gate timing

---

## Total Timeline Estimate

| Phase | Days | Cumulative |
|-------|------|------------|
| Wave 1 (Visual) | 2-3 | 2-3 |
| Wave 2 (Interaction) | 2-3 | 4-6 |
| Wave 3 (Connectivity) | 2-3 | 6-9 |
| Wave 4 (Orchestration) | 2-3 | 8-12 |
| Wave 5 (Consolidation) | 1-2 | 9-14 |

**Total: 9-14 days for full integration pipeline**

---

## Next Step

**Requesting Founder Alignment:**

1. Do you approve this wave structure?
2. Should we start with Wave 1 (Visual Stack) in mingos_settlement_lab?
3. Which gaps should be prioritized vs deferred?
4. Any subsystem priority changes?

Once aligned, we can spawn integration checker agents for each wave to begin analysis in parallel.
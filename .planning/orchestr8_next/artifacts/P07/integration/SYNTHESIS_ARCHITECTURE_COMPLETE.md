# Architecture and Migration Research Synthesis

**Project:** Orchestr8_jr → orchestr8_next Integration  
**Generated:** 2026-02-16  
**Status:** COMPLETE  
**Confidence:** HIGH

---

## Executive Summary

This document synthesizes all architecture and migration research from multiple parallel research agents, consolidating findings from eight research files and five integration specifications. The research confirms that Orchestr8 adopts a five-layer architecture (L1-L5) with explicit boundaries enforced through contract testing and feature-flag-driven migration. The primary technical debt consists of 25 L1→L3 layer violations, color token drift across eight files, and three sys.path hacks that require remediation. The recommended approach follows a six-phase migration strategy spanning three sprints, prioritizing quick wins followed by architectural fixes and optional anywidget migration. The architecture is well-documented with clear acceptance gates, rollback procedures, and integration edge specifications that enable isolated development and deterministic testing.

---

## 1. Architecture Layers Defined

### 1.1 Layer Architecture Overview

The orchestr8_next system implements a five-layer architecture with explicit boundaries between each layer. This layered approach ensures that presentation logic remains decoupled from business logic, enabling independent evolution of each layer without cascading breakage across the system. The architecture has been validated through multiple research agents and represents the canonical approach for the project.

| Layer | Name | Location | Purpose |
|-------|------|----------|---------|
| L1 | Presentation Shell | `IP/plugins/` | Marimo UI contracts, renders canonical layout, emits typed actions only |
| L2 | Action Bus + Store | `orchestr8_next/bus/` | Single source of truth for state transitions, deterministic command routing |
| L3 | Service Adapter Layer | `orchestr8_next/services/`, `orchestr8_next/adapters/` | Normalizes external systems behind stable interfaces |
| L4 | Visualization Layer | `orchestr8_next/visualization/` | 3D Code City rendering, node and connection interactions |
| L5 | Bridge Layer | `orchestr8_next/bridge/` | Capability slices, external orchestration integration |

### 1.2 Layer Contracts

Each layer operates under explicit contracts that define what it must do, what it must not do, and what inputs and outputs it handles. These contracts serve as the architectural boundaries that prevent cross-layer contamination and enable independent testing of each layer.

**L1: Presentation Shell** serves as the user-facing interface that renders the canonical top row, center pane, and locked lower fifth of the application. This layer must emit typed actions only and must not call service backends directly, parse provider payloads, or mutate global state outside the reducer contract. The layer receives AppState snapshots and derived selectors as inputs and produces UIAction events to the Action Bus as outputs. The primary files in this layer include `06_maestro.py` as the main render target and `07_settings.py` for configuration management.

**L2: Action Bus + Store** provides the single source of truth for all state transitions within the application. This layer handles deterministic command routing to adapters and must not render UI or depend on provider-specific SDKs. It receives UIAction events from L1 and ServiceEvent notifications from L3, producing StatePatch updates and CommandIntent directives as outputs.

**L3: Service Adapter Layer** normalizes all external system interactions behind stable, consistent interfaces. This layer includes adapters for LLM, memory, workspace, IDE, audio, Code City, and capability bridge integrations. The layer must not own UI state schema or expose provider-specific payloads directly, ensuring that changes to external systems do not ripple through the presentation layer.

**L4: Visualization Layer** handles all 3D Code City rendering, including node interactions and connection interactions. This layer consumes CodeCitySceneModel data structures and emits CodeCityEvent notifications for node clicks, connection actions, and camera state changes. The layer must not access storage or LLM APIs directly, nor should it manage orchestration state.

**L5: Bridge Layer** moves high-value capability slices into shared runtime pathways for Orchestr8. It operates through typed BridgeRequest and BridgeResponse envelopes with feature flags enabling progressive rollout of new capabilities.

### 1.3 Canonical Data Models

The architecture defines several critical data models that enable consistent information flow between layers. The AppState model encompasses session metadata, control states, message streams, agent registries, panel visibility, scene metadata, integration health status, and telemetry counters. Action types include UIAction for user intent, SystemAction for startup and timer events, ServiceAction for adapter responses, and CityAction for visualization events.

---

## 2. Physical Directory Structure

### 2.1 Target Structure

The recommended directory layout for orchestr8_next follows the layered architecture with clear separation of concerns:

```
orchestr8_next/
├── orchestr8.py                    ← ENTRY POINT (CANNOT RELOCATE)
├── IP/
│   ├── plugins/
│   │   ├── 06_maestro.py          ← MAIN RENDER (CANNOT RELOCATE)
│   │   └── 07_settings.py
│   ├── styles/
│   │   ├── orchestr8.css          ← VISUAL TOKENS LIVE HERE
│   │   ├── font_profiles.py       ← FONT INJECTION
│   │   └── font_injection.py
│   ├── static/
│   │   ├── woven_maps_3d.js       ← THREE.JS RENDERER
│   │   ├── woven_maps_template.html
│   │   └── shaders/
│   ├── features/
│   │   ├── code_city/
│   │   └── maestro/
│   └── contracts/
├── Font/                           ← FONT ASSETS
├── presentation/                   ← NEW (L1: UI contracts)
├── bus/                            ← RENAMED from shell/ (L2: State + Facades)
│   └── facades/                    ← NEW: L2 facades wrapping L3 services
├── services/                       ← NEW (L3: Domain services)
├── adapters/                       ← EXISTS (L3: External integrations)
├── visualization/                  ← NEW (L4: Code City engine)
└── bridge/                         ← RENAMED from comms/ (L5: Capability slices)
```

### 2.2 Immutable Paths

Certain file paths cannot be changed due to hardcoded references in the Marimo runtime or external systems. These immutable paths serve as anchors for the entire architecture and must be preserved regardless of other structural changes.

| File | Reason |
|------|--------|
| `orchestr8.py` | Marimo entry point reference |
| `IP/plugins/06_maestro.py` | UI contract authority |
| `IP/woven_maps.py` | Data structure schema |
| `IP/static/woven_maps_3d.js` | Client API contract |
| `IP/contracts/*.py` | Cross-lane agreements |
| `IP/styles/orchestr8.css` | Visual token lock |

---

## 3. Migration Phases

### 3.1 Phase Structure Overview

The migration follows a structured six-phase approach designed to minimize risk through incremental changes with verifiable gates at each step. This approach enables early detection of issues and provides clear rollback points if any phase encounters problems.

| Phase | Name | Scope | Effort | Risk | Gate |
|-------|------|-------|--------|------|------|
| 0 | Color tokens | 8 files, 11 instances | 0.5 hr | LOW | None |
| 1 | Artifact cleanup | 24 move + 7 delete | 0.25 hr | NONE | None |
| 2 | sys.path fixes | 3 hacks in 3 files | 1 hr | MEDIUM | Tests pass |
| 3 | L2 facades | 10 new facade modules | 2 hr | LOW | Tests pass |
| 4 | Structural rename | shell→bus, comms→bridge | 1 hr | LOW | 50 import updates |
| 5 | FC merge | 19 files | 2 hr | MEDIUM | SettingsService OK |
| 6 | anywidget | Full migration | 16-24 hr | MEDIUM | Sprint 3 |

### 3.2 Phase 0: Color Token Reconciliation

This initial phase addresses visual inconsistency by standardizing color tokens across the codebase. Eight files contain the legacy color value `#B8860B` instead of the locked value `#C5A028`. The files requiring fixes include `IP/plugins/06_maestro.py`, `IP/mermaid_theme.py`, `IP/features/maestro/config.py`, `IP/woven_maps.py`, and four component panel files. This phase requires approximately 19 minutes of effort and carries no technical risk.

### 3.3 Phase 1: Artifact Cleanup

This phase removes technical clutter by moving 24 artifact files to the planning directory and deleting 7 log files. The artifacts consist of integration smoke reports, test outputs, and various logs that accumulated during development. This cleanup phase requires minimal effort and presents zero risk to the codebase.

### 3.4 Phase 2: sys.path Hack Elimination

Three sys.path hack instances exist in the codebase that violate Python best practices. Hack 1 in `06_maestro.py` involves incorrect path scope resolution. Hack 2 in `04_connie_ui.py` uses sys.path manipulation for relative imports. Hack 3 in `08_director.py` involves dynamic import handling that may need to remain as-is. This phase requires careful testing to ensure imports continue working correctly after the fixes.

### 3.5 Phase 3: L2 Facade Architecture

This critical phase creates ten new facade modules that sit between L1 plugins and L3 services, enforcing layer boundaries and eliminating direct cross-layer imports. The facades provide stable interfaces that shield L1 from implementation changes in L3, enabling independent evolution of each layer. The ten facades include HealthFacade, CombatFacade, TerminalFacade, BriefingFacade, TicketFacade, ContextFacade, VisualizationFacade, GatekeeperFacade, PatchbayFacade, and MaestroConfigFacade.

### 3.6 Phase 4: Structural Renames

This phase renames two directories to align with the layer terminology: `shell/` becomes `bus/` and `comms/` becomes `bridge`. The rename requires updating approximately 50 import statements throughout the codebase. This structural alignment ensures consistent terminology across the project.

### 3.7 Phase 5: Founder Console Merge

This phase integrates the Founder Console package with 19 source files into orchestr8_next, replacing hardcoded paths with SettingsService integration. The merge requires careful path mapping and configuration updates to ensure all features continue working correctly.

### 3.8 Phase 6: anywidget Migration

This optional phase migrates the Code City visualization to use anywidget, eliminating iframe overhead and static 404 errors. The migration requires adapting the Three.js ESM modules and is estimated to require 16-24 hours of effort. This phase is recommended for Sprint 3 after the structural foundation is sound.

---

## 4. Known Issues

### 4.1 Critical Issues Requiring Immediate Attention

Several critical issues have been identified that require immediate remediation to ensure system stability and maintainability. These issues represent architectural violations that create tight coupling and potential points of failure.

The first critical issue involves 25 L1→L3 violations across four plugin files. The `06_maestro.py` file alone contains 20 direct imports from L3 modules, violating the layer architecture. The `03_gatekeeper.py` file contains one violation, `ticket_panel.py` contains one violation, and `07_settings.py` contains two violations. These violations create tight coupling between presentation and service layers, making it difficult to modify one without affecting the other.

The second critical issue involves color token drift in eight files. The legacy color value `#B8860B` has been replaced with the locked value `#C5A028` in the canonical specification, but this change has not been propagated to all affected files. This inconsistency creates visual drift that undermines the design system.

The third critical issue involves sys.path hacks that represent fragile path handling. Three instances of sys.path manipulation exist in the codebase that should be replaced with proper relative imports or package structure.

### 4.2 Moderate Issues Requiring Future Attention

Several moderate issues have been identified that should be addressed in future iterations but do not pose immediate risk to system stability.

The default watch paths in HealthWatcher are limited to `["IP/"]`, which may miss changes in other fiefdoms or subsystems. This limitation could cause health status to become stale for components outside the default watch path.

The Neighborhood Status Bug in graph_builder causes confusion between combat and broken states. The code comments suggest neighborhoods mark combat as broken, but the implementation may not reflect this correctly.

The Carl run_deep_scan() function appears to be non-functional, potentially due to TypeScript tool placement issues. This requires investigation to determine whether the function should be fixed or removed.

### 4.3 Minor Issues and Ambiguities

Several minor issues and ambiguities exist that may require clarification from domain experts. The Fiefdom Extraction Fragility in `_extract_fiefdom()` only uses the first directory, causing nested fiefdoms to collapse into single entries. The Health Result Path Matching uses substring matching that can cause false positives when paths share common substrings. The Connection Verifier has hardcoded builtins that are not configurable, limiting flexibility for different environments.

---

## 5. Marimo-Specific Patterns

### 5.1 Core Principles

The Orchestr8 system relies on the Marimo reactive notebook framework, which imposes specific patterns that differ from traditional Python applications. Understanding these patterns is essential for correct implementation and maintenance.

The first principle involves reactive execution, where running a cell automatically triggers execution of all dependent cells. This creates a reactive graph where state changes propagate automatically through the dependency chain. The second principle involves no hidden state, as variables are automatically cleaned up when cells are deleted, preventing stale data accumulation.

The third principle involves execution order, which is determined by variable references rather than cell position in the file. This means the physical order of cells in the file does not determine execution order; instead, Marimo analyzes the dependency graph and executes cells in the correct order. The fourth principle requires global variables for UI elements, where all `mo.ui.*` elements must be assigned to global variables for Marimo to track them properly.

### 5.2 State Management Pattern

All mo.state() definitions must be centralized in a single module, typically named `_state.py`. The state must be defined at module level, as function-scoped mo.state() calls will not persist across renders.

```python
# _state.py - ALL state definitions must be here

import marimo as mo

# Global state definitions (module-level REQUIRED)
_root_state, _set_root = mo.state("/path/to/project")
_maestro_state, _set_maestro = mo.state("OFF")
_combat_state, _set_combat = mo.state([])

# Selector functions for derived state
def get_maestro_state() -> str:
    return _maestro_state()

def set_maestro_state(state: str) -> None:
    _set_maestro(state)
```

### 5.3 Handler Pattern

Button handlers must be defined at module level rather than as inline lambdas to ensure proper tracking by Marimo. The handler functions should use on_click rather than the deprecated on_change for button interactions.

```python
# _handlers.py

# Module-level function REQUIRED
def handle_toggle_orchestr8() -> None:
    current = get_maestro_state()
    states = ["ON", "OFF", "OBSERVE"]
    idx = states.index(current) if current in states else 0
    next_state = states[(idx + 1) % len(states)]
    set_maestro_state(next_state)

# Button uses on_click (NOT on_change)
toggle_btn = mo.ui.button(on_click=handle_toggle_orchestr8)
```

---

## 6. Visual Token Integration

### 6.1 Canonical Source

All visual decisions trace back to `SOT/VISUAL_TOKEN_LOCK.md`, which serves as the single source of truth for all visual tokens in the system. This file defines the exact color values, typography specifications, and dimension tokens that must be used throughout the application.

### 6.2 Color Tokens (LOCKED)

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-obsidian` | #050505 | Background base |
| `--gold-dark` | #C5A028 | Primary accent, borders |
| `--gold-light` | #F4C430 | Highlight accent, hover |
| `--teal` | #00E5E5 | Secondary accent |
| `--text-grey` | #CCC | Standard text |
| `--state-working` | #D4AF37 | Gold - operational |
| `--state-broken` | #1fbdea | Blue - needs attention |
| `--state-combat` | #9D4EDD | Purple - agents active |

### 6.3 Typography Tokens (LOCKED)

| Token | Value | Usage |
|-------|-------|-------|
| `--font-header` | 'Marcellus SC', serif | Headers, top buttons |
| `--font-ui` | 'Poiret One', cursive | UI labels, mini buttons |
| `--font-data` | 'VT323', monospace | Data, terminal |

### 6.4 Dimension Tokens (LOCKED)

| Token | Value |
|-------|-------|
| `--header-height` | 80px |
| `--top-btn-height` | 50px |
| `--top-btn-min-width` | 160px |
| `--btn-mini-height` | 22px |
| `--btn-mini-min-width` | 60px |
| `--btn-maestro-height` | 36px |

---

## 7. Integration Edge Specifications

### 7.1 What is an Integration Edge?

An integration edge represents a clearly defined boundary between two subsystems where data contracts are explicit, development can happen in isolation, and integration testing is deterministic. These edges enable parallel development by different teams or agents without interfering with each other's work.

### 7.2 The Seven Integration Edges

| Edge | From | To | Status |
|------|------|-----|--------|
| **EDGE-1: Visual Tokens** | `orchestr8.css` | `font_profiles.py` → `06_maestro` | ✅ ACTIVE |
| **EDGE-2: Code City Rendering** | `graph_builder` | `woven_maps` → Three.js | ✅ ACTIVE |
| **EDGE-3: Health Status Flow** | `health_checker` | `health_watcher` → `graph_builder` | ✅ ACTIVE |
| **EDGE-4: Combat Tracking** | `combat_tracker` | `combat_state.json` → graph | ⚠️ REFRESH NEEDED |
| **EDGE-5: Panel System** | `code_city_context` | `deploy_panel` | ⚠️ RICH DATA NEEDED |
| **EDGE-6: Contracts** | `contracts/*.py` | All consumers | ✅ ACTIVE |
| **EDGE-7: Settings** | `07_settings.py` | `font_profiles` → CSS | ✅ ACTIVE |

### 7.3 Edge-by-Edge Development Isolation

Each integration edge can be developed and tested in isolation, enabling parallel work across different parts of the system. EDGE-1 (Visual) supports yes for both development and testing isolation, with CSS token changes reflected immediately. EDGE-2 (City) supports yes for development isolation with mock data and yes for testing isolation with full pipeline verification. EDGE-3 (Health) supports partial development isolation with yes for testing using mocks. EDGE-4 through EDGE-7 all support yes for both development and testing in isolation.

---

## 8. Recommendations

### 8.1 Immediate Recommendations

The following recommendations should be addressed immediately to prevent further architectural degradation and ensure system stability.

**Fix L1→L3 Violations (Phase 3):** Create the ten L2 facade modules as designed in RESEARCH_06_L1_L3_FIX_DESIGN.md to eliminate direct cross-layer imports. This remediation is essential for maintaining architectural boundaries and enabling independent layer evolution.

**Reconcile Color Tokens (Phase 0):** Apply the sed replacement command to fix all eight files containing the legacy color value. This quick win requires minimal effort and eliminates visual inconsistency.

**Eliminate sys.path Hacks (Phase 2):** Replace the three sys.path instances with proper relative imports or package structure. This remediation improves import reliability and follows Python best practices.

### 8.2 Medium-Term Recommendations

The following recommendations should be addressed in the medium term to improve system maintainability and enable future capabilities.

**Implement Feature Flags:** Use feature flags for gradual migration rollout, allowing new and old implementations to coexist during transition periods. This approach reduces risk by enabling quick rollback if issues arise.

**Add Contract Testing:** Implement automated layer boundary tests that verify no L1→L3 imports exist in the codebase. This testing should be integrated into the CI pipeline to prevent future architectural violations.

**Migrate to anywidget (Phase 6):** After structural foundations are sound, migrate Code City visualization to use anywidget, eliminating iframe overhead and static 404 errors. This migration provides better performance and more direct integration with the Marimo runtime.

### 8.3 Long-Term Recommendations

The following recommendations represent future capabilities that should be considered for long-term system evolution.

**Establish API Versioning:** Implement API versioning for the L2 facades to enable independent evolution of L1 and L3 without breaking changes.

**Expand Bridge Capabilities:** Develop additional capability slices through the L5 Bridge layer, enabling integration with external systems without direct coupling.

---

## 9. Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Architecture Layers | HIGH | Validated by multiple research agents with conflicts resolved |
| Migration Phases | HIGH | Clear sequence with test gates and rollback plans |
| L2 Facade Design | HIGH | Based on verified L3 service interfaces |
| Visual Tokens | HIGH | Canonical source confirmed in VISUAL_TOKEN_LOCK.md |
| Marimo Patterns | HIGH | Based on official documentation and existing code |
| anywidget Feasibility | MEDIUM | Technical feasibility confirmed, implementation effort uncertain |
| Overall | HIGH | Clear path forward with well-researched components |

---

## 10. Sources

### Primary Research Files

All research files from the integration research directory provide comprehensive analysis of different aspects of the architecture and migration:

- RESEARCH_01_COLOR_TOKEN_AUDIT.md - Color token drift analysis
- RESEARCH_02_SYSPATH_ELIMINATION.md - sys.path hack identification
- RESEARCH_03_STRUCTURE_VALIDATION.md - Directory structure validation
- RESEARCH_04_FC_EXTRACTION_AUDIT.md - Founder Console analysis
- RESEARCH_05_ANYWIDGET_FEASIBILITY.md - anywidget migration feasibility
- RESEARCH_06_L1_L3_FIX_DESIGN.md - L2 facade design specifications
- RESEARCH_07_CLEANUP_MIGRATION_ORDER.md - Migration phase ordering
- RESEARCH_08_SYNTHESIS_FINAL_PLAN.md - Final synthesis and execution plan

### Integration Specification Files

The integration specifications provide detailed guidance for implementation:

- FINAL_ARCHITECTURE_PLAN.md - Complete architecture plan
- ARCHITECTURE_SYNTHESIS_FEEDBACK.md - Feedback and gap analysis
- MARIMO_STRUCTURE_CLEANUP_SPEC.md - Marimo-specific patterns
- INTEGRATION_EDGE_SPECIFICATION.md - Integration boundary definitions
- INTEGRATION_EXECUTION_STRATEGY.md - Migration execution strategy

### Reference Documents

- `/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md` - Canonical visual tokens
- `/home/bozertron/a_codex_plan/.planning/research/ARCHITECTURE_SYNTHESIS.md` - Original architecture synthesis

---

## Quick Reference Card

### Integration Edges (Memorize These)

1. **VISUAL:** VISUAL_TOKEN_LOCK.md → font_profiles.py → orchestr8.css → 06_maestro
2. **CITY:** graph_builder → woven_maps → woven_maps_template.html (Three.js + particles)
3. **HEALTH:** health_checker → health_watcher → graph_builder → CodeNode.status
4. **COMBAT:** combat_tracker → combat_state.json → graph_builder → purple building
5. **PANEL:** code_city_context → deploy_panel.py → UI
6. **CONTRACTS:** contracts/*.py → ALL (read-only consumers)
7. **SETTINGS:** 07_settings.py → font_profiles → orchestr8.css

### Dependencies (What uses what)

- 06_maestro.py imports: ALL subsystems
- graph_builder imports: health_checker, combat_tracker, contracts
- woven_maps imports: NONE (pure config)
- 07_settings imports: font_profiles, contracts

---

**STATUS: SYNTHESIS COMPLETE**

This synthesis is complete and ready for execution. The architecture is well-defined, migration phases are clear, and all known issues have been documented with recommended solutions.

*Synthesis complete. Plan is actionable and ready for herd execution.*

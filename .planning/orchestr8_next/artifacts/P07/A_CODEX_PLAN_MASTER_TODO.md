# A_CODEX_PLAN Integration Master TODO

**Generated:** 2026-02-16
**Purpose:** Consolidated integration roadmap with rationale

---

## WHAT WE BUILT

### Catalogs (3)
| Catalog | Location | Purpose |
|---------|----------|---------|
| Plugin Catalog | `PLUGIN_CATALOG.json` | Marimo plugin system reference |
| Rust P2P Catalog | `RUST_P2P_CATALOG.json` | libp2p-based P2P system |
| Python P2P Catalog | `PYTHON_P2P_CATALOG.json` | PyO3 adapter layer |

### Integration Pattern: DENSE + GAP
The core insight: **Dense logic with intentional gaps forces attention at boundaries**

```
┌─────────────────────────────────────────────────────┐
│  INTEGRATION FILE                                    │
├─────────────────────────────────────────────────────┤
│  # === GAP 1: TYPE CONTRACTS ===                    │ ← Forces contract review
│  # === GAP 2: STATE BOUNDARY ===                    │ ← Forces state audit
│  # === GAP 3: BRIDGE DEFINITIONS ===                │ ← Forces protocol review  
│  # === GAP 4: INTEGRATION LOGIC ===                 │ ← Forces usage review
└─────────────────────────────────────────────────────┘
```

---

## WAVE 1: CORE COMPONENT INTEGRATIONS (13 roadmaps)

| Component | Rationale | Priority |
|-----------|-----------|----------|
| **carl_core** | Context gathering - feeds all other systems | HIGH |
| **health_checker** | Error detection - triggers tickets | HIGH |
| **louis_core** | File protection - prevents accidents | HIGH |
| **connection_verifier** | Import graph - drives Code City wiring | HIGH |
| **combat_tracker** | Agent deployment tracking - purple status | HIGH |
| **contracts** | ALL type definitions - foundation | CRITICAL |
| **health_watcher** | Real-time file monitoring | MEDIUM |
| **ticket_manager** | Agent deployment triggers | HIGH |
| **connie** | Database conversion tools | LOW |
| **mermaid_generator** | Visual fiefdom maps | LOW |
| **terminal_spawner** | Embedded terminal | MEDIUM |
| **code_city_context** | Node click → context payloads | HIGH |
| **agent_groups** | Settlement agent tiers | HIGH |

---

## WAVE 2: CODE CITY DEPTH (8 roadmaps)

| Area | Rationale | Priority |
|------|-----------|----------|
| **woven_maps** | Main entry point - creates 3D city | CRITICAL |
| **3D_engine** | Three.js rendering - particle system | CRITICAL |
| **barradeau_builder** | Emergence animation - HOW buildings "EMERGE" | CRITICAL |
| **graph_builder** | Node/edge generation - data transformation | CRITICAL |
| **render_pipeline** | Marimo assembly + iframe integration | HIGH |
| **neighborhoods** | Fiefdom detection + borders | HIGH |
| **wiring_view** | Import visualization + interactive edges | HIGH |
| **payload_guard** | Handles oversized repos - reliability | CRITICAL |

---

## THE GAP PATTERN PRINCIPLE

**Why this works:**

1. **Dense logic** = LLM/human processes as "fluent" → tends to skip
2. **Explicit GAP markers** = Forces conscious crossing of boundaries
3. **Mistakes happen at boundaries** = That's where attention is needed

**What each GAP forces:**

| GAP | Forces Review Of |
|-----|------------------|
| Type Contracts | Input/output validation, duck typing elimination |
| State Boundary | Hidden globals, mutation points, caching needs |
| Bridge Definitions | Serialization, protocol mismatches, encoding |
| Integration Logic | Error handling, empty states, entry point contracts |

---

## KEY FINDINGS

### Code City Architecture
- **Stateless renderer**: 3D engine is STATELESS - interactions happen at 2D canvas level
- **Particle emergence**: Buildings "EMERGE" from void - NO breathing/pulsing
- **Status colors**: Gold (#D4AF37) = working, Teal (#1fbdea) = broken, Purple (#9D4EDD) = combat
- **Payload guard**: 9MB limit with IP/ fallback - prevents runtime crashes

### P2P System
- **Rust backend**: libp2p 0.52+ with TCP/WebSocket + Noise + Yamux
- **Python adapter**: Option B (primitives only) - PyO3 bindings not yet compiled
- **Discovery**: mDNS (local) + Kademlia DHT (distributed)

### Marimo Integration
- **Plugin contract**: PLUGIN_NAME, PLUGIN_ORDER, render(STATE_MANAGERS)
- **Button callbacks**: Use on_click NOT on_change
- **JS bridges**: Hidden mo.ui.text + postMessage pattern

---

## INTEGRATION ORDER RECOMMENDATION

```
PHASE 1: Foundation
├── contracts (ALL type definitions)
├── health_checker (error detection)
└── connection_verifier (graph data)

PHASE 2: Core Systems
├── carl_core (context)
├── combat_tracker (agent tracking)
├── ticket_manager (deployment triggers)
└── code_city_context (payload assembly)

PHASE 3: Visualization
├── woven_maps + graph_builder
├── barradeau_builder
├── neighborhoods
└── wiring_view

PHASE 4: Polish
├── terminal_spawner
├── health_watcher
├── agent_groups
└── connie
```

---

## FILE LOCATIONS

### Catalogs
- `.planning/orchestr8_next/artifacts/P07/PLUGIN_CATALOG.json`
- `.planning/orchestr8_next/artifacts/P07/RUST_P2P_CATALOG.json`
- `.planning/orchestr8_next/artifacts/P07/PYTHON_P2P_CATALOG.json`
- `.planning/orchestr8_next/artifacts/P07/A_CODEX_PLAN_INTEGRATION_CATALOG.md`

### Integration Roadmaps
- `.planning/orchestr8_next/artifacts/P07/roadmaps/`

**Wave 1:** `INTEGRATION_*.md` (13 files)
**Wave 2:** `CODE_CITY_*.md` (8 files)

---

## STATUS

- [x] Catalogs complete
- [x] Pattern defined
- [x] Wave 1 complete (13 roadmaps)
- [x] Wave 2 complete (8 roadmaps)
- [ ] Synthesis complete → **THIS DOCUMENT**

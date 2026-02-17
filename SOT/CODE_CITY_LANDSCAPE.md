# CODE CITY LANDSCAPE

Generated: 2026-02-12 23:38:39 PST  
Purpose: Durable, compact-safe integration context for blindly executing Code City features without losing vision.

> 2026-02-16 note:
> This matrix is valuable design context but contains pre-P07 implementation status values.
> Use `SOT/CODE_CITY_AGGREGATED_TODO.md` and active P07 check-ins for execution truth.

## 1. Cold-Start Rehydration Order

Load these in order before implementation:

1. `SOT/CODE_CITY_LANDSCAPE.md` (this file)
2. `SOT/CODE_CITY_PLAN_LOCK.md`
3. `SOT/todo.md`
4. `.planning/phases/CONTEXT.md`
5. `.planning/VISION-ALIGNMENT.md`
6. `.planning/phases/ARCHITECT-BARRADEAU.md`
7. `.planning/phases/WORKORDERS-BARRADEAU.json`

## 2. Blind Integration Matrix

| Unit | Type | Code Anchor | Context Needed To Integrate Blindly | Missing Context/Asset | Status |
|---|---|---|---|---|---|
| Canonical frame (`orchestr8/collabor8/JFDI`, no `gener8`) | behavior | `SOT/CODE_CITY_PLAN_LOCK.md:7`, `IP/plugins/06_maestro.py:1185` | Top-row labels, Void center, bottom control frame, no brand drift | UI regression check for top-row contract | partial |
| Three-state color contract | behavior | `SOT/CODE_CITY_PLAN_LOCK.md:22`, `IP/woven_maps.py:116` | Gold/Teal/Purple + Void/Surface, no extra states | Shared enum/constants module consumed by all renderers/services | partial |
| Building geometry formulas | feature | `SOT/CODE_CITY_PLAN_LOCK.md:31`, `IP/woven_maps.py:384` | Height=`3 + exports*0.8`, footprint=`2 + lines*0.008` | Runtime geometry currently uses LOC heuristics in layout, not locked formulas | missing |
| Hybrid backend (WebGPU primary + CPU fallback) | routine | `IP/woven_maps.py:852`, `IP/woven_maps.py:955` | Backend selection policy, capability detection, fallback behavior | Explicit backend-state contract exported to UI/state/logs | partial |
| Control semantics (`densit8/orbit8/focus8/layer8`) | routine | `IP/woven_maps.py:886`, `IP/woven_maps.py:1714` | Shared semantics and ranges across GPU/CPU | Cross-backend parity tests + control contract doc | partial |
| Entry overview camera (distant triage) | behavior | `SOT/todo.md:37`, `IP/woven_maps.py:2715` | Deterministic initial camera/frame showing whole landscape | No explicit overview camera state constants | missing |
| Warp dive to problem area | behavior | `SOT/todo.md:38`, `IP/woven_maps.py:1735`, `IP/woven_maps.py:2680` | Dive interpolation curve, target framing, particle fly-by effect, return route | No dive routine or camera transition contract in runtime path | missing |
| Camera keyframes | routine | `IP/woven_maps.py:894` | Slot semantics, load/save rules, keyboard trigger | 3D pose persistence + shortcut contract not defined | partial |
| Broken-node pollution effects | feature | `SOT/todo.md:45`, `IP/woven_maps.py:973` | Emission rule by error count/severity, rise/fade envelope | Severity mapping + deterministic particle budget not defined | partial |
| Tooltip + node click event contract | routine | `IP/woven_maps.py:2651`, `IP/woven_maps.py:2689`, `IP/plugins/06_maestro.py:1716` | Event schema (`path/status/errors/metrics`), routing to UI handlers | JS event arrives, but no Python bridge calling `handle_node_click()` | missing |
| Connection graph as edge truth source | routine | `IP/woven_maps.py:430`, `SOT/CODE_CITY_PLAN_LOCK.md:43` | ConnectionVerifier edges, unresolved states, line refs | `create_code_city()` currently uses `build_graph_data()` path, not connection graph pipeline | partial |
| Connection panel + full signal path glow | feature | `SOT/CODE_CITY_PLAN_LOCK.md:49` | Panel schema for imports/exports/routines + path traversal rules | Panel schema and path-highlight algorithm not implemented | missing |
| Patchbay rewiring | feature | `SOT/CODE_CITY_PLAN_LOCK.md:67` | Drag-to-rewire UX, import rewrite routine, validation/revert flow | Entire workflow absent | missing |
| Sitting Room transition + return | feature | `SOT/CODE_CITY_PLAN_LOCK.md:61` | Entry trigger, morph animation, context handoff to collaboration surface | No Sitting Room runtime implementation | missing |
| Health flow (`File Change -> HealthWatcher -> HealthChecker -> STATE -> Code City`) | routine | `IP/health_watcher.py:8`, `IP/plugins/06_maestro.py:1207`, `orchestr8.py:55`, `IP/woven_maps.py:527` | Global health state in app root, watcher lifecycle, merge function call in render pipeline | Root app state lacks `health` key; health merge function exists but not wired through `create_code_city()` | partial |
| Combat flow + status merge precedence | routine | `IP/woven_maps.py:409`, `IP/woven_maps.py:490`, `IP/combat_tracker.py:8` | Precedence contract (`combat > broken > working`) across all feeds | Centralized merge policy not codified in one function | partial |
| Settlement survey ingestion | feature | `SOT/todo.md:58` | Input schema for fiefdoms/boundaries/wiring/agent activity | Adapter function + loader path not implemented | missing |
| Neighborhood boundaries + contract badges | feature | `SOT/todo.md:51` | Boundary geometry, labeling, integration badge rules, hover contract text | No boundary renderer in current template | missing |
| Louis lock indicators on buildings/panels | feature | `SOT/todo.md:53`, `IP/carl_core.py:173`, `IP/louis_core.py:1` | Lock lookup per file and visual marker rules | Lock metadata not fed to Code City rendering (**LockOverlay schema IN PROGRESS - Wave A**) | missing |
| Town Square for infra files | behavior | `SOT/todo.md:54` | Classification rules for config/deps/ignore artifacts | No infra-zone representation in renderer/data model (**TownSquareClassification schema IN PROGRESS - Wave A**) | missing |
| Audio math contract (deterministic bands) | routine | `SOT/todo.md:84`, `IP/woven_maps.py:1630` | Band ranges and mapping functions (`high->amp`, `mid->offset`, `low->time`) | Runtime uses percent bins, not explicit Hz contract | partial |
| Effect math pack (curl, wave interference, volume seeding, ping-pong) | routine | `SOT/todo.md:73`, `SOT/todo.md:74`, `SOT/todo.md:76`, `SOT/todo.md:77` | Tunables, safety bounds, fallback behavior | Not integrated into production renderer as explicit modes | missing |
| Emergence phase machine | behavior | `SOT/todo.md:78`, `IP/woven_maps.py:1755` | Enumerated phase states and transitions with no post-ready oscillation | Runtime has basic emerged state, not explicit phase state machine | partial |
| Broken-node deploy + ticket generation flow | routine | `IP/plugins/06_maestro.py:678`, `IP/plugins/06_maestro.py:709`, `SOT/todo.md:102` | Ticket payload schema from Carl/health + deploy action chain | Auto-ticket generation from node click not wired end-to-end | partial |
| Acceptance + performance gates | routine | `SOT/CODE_CITY_PLAN_LOCK.md:91`, `SOT/todo.md:119` | Visual contract tests + telemetry thresholds | No explicit automated gate suite in repo | missing |

## 3. Missing Context Assets (Create These First)

These are the minimum contracts needed for blind implementation:

1. `CodeCityNodeEvent` schema:

- Required fields: `path`, `status`, `errors`, `nodeType`, `centrality`, `incomingCount`, `outgoingCount`.
- Transport: iframe `postMessage` payload + Marimo handler contract.

2. `CameraState` schema:

- `mode` (`overview`, `dive`, `focus`, `room`, `sitting_room`), `position`, `target`, `zoom`, `return_stack`.
- Includes warp-dive timing and easing parameters.

3. `BuildingPanel` + `BuildingRoom` schema:

- Explicit I/O lists, routine mapping, per-room connection references, lock state.

4. `SettlementSurvey` schema:

- `fiefdoms`, `boundary_contracts`, `wiring_state`, `agent_activity`.
- Merge policy into node/edge runtime metadata.

5. `StatusMergePolicy` routine:

- Single function that resolves all status inputs with precedence:
`combat > broken > working`.

6. `LockOverlay` schema (**IN PROGRESS - Wave A**):

- Visual rule for locked nodes/ports and Louis lock reasons.

7. `TownSquareClassification` schema (**IN PROGRESS - Wave A**):

- Rules for infra files excluded from building rendering and displayed in infra zone.

## 4. Execution Order (Blind-Safe)

1. Lock contracts: event, camera, panel/room, survey, merge policy.
2. Wire root state (`health`/`health_status`) in `orchestr8.py`.
3. Wire node-click bridge (`postMessage` -> `handle_node_click` path).
4. Switch Code City data path to connection graph + health merge + combat precedence.
5. Add camera overview + warp dive + return stack.
6. Add boundaries/contracts/locks/town-square overlays.
7. Add effect-math modes (curl/wave/ping-pong) behind feature flags.
8. Add acceptance gates + perf telemetry.

## 5. One-Line Truth

If a future run remembers only one file, it should remember this one: `SOT/CODE_CITY_LANDSCAPE.md`.

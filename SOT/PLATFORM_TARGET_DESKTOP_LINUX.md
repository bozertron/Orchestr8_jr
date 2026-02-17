# Platform Target: Desktop Linux Pressure Test

Last Updated: 2026-02-16
Owner: Mayor + Founder
Status: ACTIVE

## 1. Objective Lock

This MVP targets:
1. Desktop Linux (`x86_64`)
2. Fullscreen laptop workflows at high resolution
3. marimo-first runtime with a deterministic rollback path

Out of scope until explicitly unlocked:
1. Android target builds
2. Tablet/mobile-first layouts
3. WASM-only production deployment posture

## 2. Pressure-Test Evidence (Current Repo)

Executed on 2026-02-16:

```bash
pytest tests/city/test_parity.py -q
pytest tests/reliability/test_reliability.py -q
pytest tests/city/test_binary_payload.py tests/city/test_wiring_view.py -q
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py tests/city/test_wiring_view.py tests/city/test_parity.py -q
bash scripts/verify_rehearsal.sh
```

Observed results:
1. `3 passed` (`test_parity`)
2. `3 passed` (`test_reliability`)
3. `5 passed` (binary payload + wiring)
4. `11 passed` (canonical validation set)
5. Rehearsal PASS:
- `WIDGET Mode Verified: PASS`
- `IFRAME Mode Verified: PASS`

## 3. Current Runtime Contract (What We Keep)

1. Primary render mode remains `WIDGET` (`AnyWidget`).
2. Fallback remains `IFRAME` for rollback resilience.
3. Code City payload/stream guardrails stay enforced in canonical lane.
4. Cross-window parity tests remain required for acceptance.

## 4. Packaging Options Pressure Test

### Option A: Linux browser app-mode + marimo runtime (Recommended now)

Pros:
1. Lowest integration risk with current architecture.
2. Best time-to-value for desktop Linux MVP.
3. Reuses existing `WIDGET/IFRAME` contract and test harness directly.

Cons:
1. Not a single bundled desktop binary.
2. Requires launch/runtime management discipline.

Decision:
1. Use as immediate packaging baseline for MVP hardening.

### Option B: Tauri shell + Python sidecar (Recommended next)

Pros:
1. Native app shell UX for Linux desktop distribution.
2. Uses system webview runtime model.

Cons:
1. Higher integration complexity (process orchestration + packaging pipeline).
2. Linux webview capability depends on distro `webkit2gtk` versions, so web-platform feature parity is less predictable across machines.
3. Requires extra hardening across launch/update/debug paths.

Decision:
1. Prepare as Wave-5+ packaging track after baseline gates are stable.

### Option C: Electron shell + Python sidecar (Not recommended for near-term)

Pros:
1. Mature ecosystem and tooling.
2. Consistent Chromium renderer behavior across Linux targets.

Cons:
1. Heavier process/memory overhead profile versus Option A/B.
2. Adds avoidable packaging/runtime complexity for current MVP target.

Decision:
1. Keep as fallback for cases that require strict Chromium feature parity on Linux.

## 5. Accelerator Tooling Shortlist (Desktop/High-Res)

Priority-1 (adopt in canonical plan):
1. `three.js` instancing patterns for repeated geometry (`InstancedMesh`).
2. `three-mesh-bvh` for fast raycast/selection on complex geometry.
3. `Spector.js` for WebGL frame capture/profiling.
4. Keep WebGPU-first where supported with deterministic CPU/WebGL fallback.

Priority-2 (evaluate after Priority-1):
1. Explicit dynamic pixel-ratio caps per device profile.
2. Feature-flagged advanced GPU compute paths in city renderer.

## 6. Upstream Marimo Docs Snapshot (Pinned)

Imported planning snapshot:
1. `third_party_refs/marimo_docs_upstream_main_20260216/docs/`
2. `third_party_refs/marimo_docs_upstream_main_20260216/SOURCE_PIN.txt`

Pin metadata:
1. Source: `https://github.com/marimo-team/marimo/tree/main/docs`
2. Commit: `b6adf07d2a4fd616aeba6f38e4af4024b2a2cc84`
3. Clone timestamp: `2026-02-16T12:21:30Z`

## 7. Wave Execution Hooks

Orchestr8_jr:
1. Enforce desktop Linux target in acceptance decisions.
2. Keep `WIDGET` + `IFRAME` rehearsal gate mandatory.

a_codex_plan:
1. Add Linux desktop packaging baseline packet.
2. Add accelerator hooks behind feature flags with tests.

mingos_settlement_lab:
1. Provide style/component constraints that preserve high-res clarity and GPU-safe motion budgets.

2ndFid_explorers:
1. Extract performance-pattern references that reduce runtime overhead in city scene updates.

or8_founder_console:
1. Add platform target checklist to proposal/review bundle output.

## 8. Sources

1. https://docs.marimo.io/guides/deploying/programmatically/
2. https://docs.marimo.io/guides/package_management/using_uv/
3. https://docs.marimo.io/guides/configuration/index/
4. https://docs.marimo.io/guides/wasm/
5. https://v2.tauri.app/concept/architecture/
6. https://www.electronjs.org/docs/latest/tutorial/process-model
7. https://pyinstaller.org/en/stable/operating-mode.html
8. https://threejs.org/docs/#api/en/objects/InstancedMesh
9. https://github.com/gkjohnson/three-mesh-bvh
10. https://github.com/BabylonJS/Spector.js

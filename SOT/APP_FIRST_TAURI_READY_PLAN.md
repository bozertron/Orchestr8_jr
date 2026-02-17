# App-First, Tauri-Ready Plan

Last Updated: 2026-02-16
Owner: Mayor + Founder
Status: PROPOSED (ready to execute on approval)

## 1. Intent

Ship core product behavior and UI lock first, while deferring final desktop packaging glue until integration risk is reduced.

This means:
1. marimo remains the runtime core.
2. Frontend work continues now.
3. Tauri remains the target desktop shell, but is integrated in a controlled later gate.

## 2. Why This Path

1. Prevents spending cycles on shell/debug plumbing before product behavior is locked.
2. Preserves momentum on UI, visual systems, and interaction contracts.
3. Keeps final packaging aligned with founder preference (Tauri) without early coupling.

## 3. Canonical Inputs (Current)

Visual reference inputs:
1. `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html`
2. `one integration at a time/UI Reference/MaestroView.vue`
3. `one integration at a time/FileExplorer/FileExplorer.vue`
4. `Settings For Integration Referece/settings.html`
5. `Settings For Integration Referece/settings.js`
6. `Settings For Integration Referece/settings-advanced.html`
7. `Settings For Integration Referece/settings-advanced.js`

Current runtime/contract inputs:
1. `orchestr8_next/shell/contracts.py`
2. `orchestr8_next/city/contracts.py`
3. `orchestr8_next/city/notebook.py`
4. `SOT/PLATFORM_TARGET_DESKTOP_LINUX.md`

## 4. Non-Negotiable Implementation Rules

1. No direct `window.__TAURI__` calls inside shared UI components.
2. Use one host bridge interface (`OR8HostBridge`) with two adapters:
- `web_stub` (current development mode)
- `tauri_adapter` (packaging mode)
3. Keep render contract: `WIDGET` primary, `IFRAME` fallback rehearsed.
4. Preserve founder style lock:
- reduced palette
- dual-color particle transition baseline
- deco-future typography and component treatment
5. Linux desktop only (`x86_64`), Fedora + Linux Mint compatibility gates.

## 5. Execution Phases

## Phase A: Product/UI Lock (No Packaging)

Deliverables:
1. Tokenized visual contract (colors, typography, motion budget, particle transitions).
2. Component placement contract from reference HTML + Vue assets.
3. Settings interaction map (UI controls -> command intents -> runtime endpoints).

Acceptance:
1. Static layout parity sign-off from founder.
2. Command intent map approved with no unresolved ambiguity.

## Phase B: Frontend Scaffold (Packaging-Agnostic)

Deliverables:
1. `OR8HostBridge` interface spec.
2. `web_stub` adapter for immediate execution in current stack.
3. Event/command catalog for Phreak, settings, file explorer, and control deck actions.
4. Integration tests for bridge contract and event payload validation.

Acceptance:
1. UI runs without Tauri.
2. Zero direct shell-specific calls in shared components.
3. Existing canonical test gates remain green.

## Phase C: Core Wiring + Behavior

Deliverables:
1. Bind scaffolded UI intents into marimo/core surfaces.
2. Verify deterministic behavior for settings/state transitions.
3. Run replay gates plus focused interaction tests.

Acceptance:
1. Canonical reliability/city tests pass.
2. Phreak/settings/file actions route through bridge contract.

## Phase D: Tauri Shell Integration (After A-C Pass)

Deliverables:
1. Thin Tauri shell that launches and hosts the app.
2. `tauri_adapter` implementing the same bridge interface.
3. Fedora + Linux Mint package smoke tests.

Acceptance:
1. No core logic rewrites for shell adoption.
2. Same UI interaction contracts pass on shell.
3. Fullscreen high-resolution desktop performance meets target gate.

## 6. Immediate Work Queue (No Packaging Yet)

1. Extract visual token pack from reference assets.
2. Write `OR8HostBridge` contract spec and command catalog.
3. Refactor any direct Tauri-coupled frontend references into bridge calls.
4. Map settings pages to command intents and runtime ownership.
5. Publish a lock report with unresolved questions only.

## 7. Go/No-Go Gates Before Tauri Integration

1. UI contract stable across main surfaces.
2. Settings command map stable and test-backed.
3. Canonical replay gates green (`11 passed` + rehearsal pass).
4. No open severity-1 ambiguity in integration map.

## 8. Decision Log

Current recommendation:
1. Proceed immediately with Phases A-C.
2. Hold Phase D until gates pass.
3. Keep Tauri as target packaging endpoint.

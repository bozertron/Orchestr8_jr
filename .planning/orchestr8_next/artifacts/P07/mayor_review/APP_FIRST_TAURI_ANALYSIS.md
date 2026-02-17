# Mayor Review: App-First, Tauri-Ready Plan Analysis

**Source Document:** `SOT/APP_FIRST_TAURI_READY_PLAN.md`  
**Review Date:** 2026-02-16  
**Reviewer:** Mayor (via file search specialist)  
**Status:** ANALYSIS COMPLETE

---

## 1. Phase Structure and Sequencing

### Overview

The plan defines a **four-phase execution model** that deliberately defers desktop shell integration until product behavior is locked. This is a risk-mitigated approach that preserves development momentum while maintaining a clear path to Tauri packaging.

### Phase Breakdown

| Phase | Focus | Key Characteristic |
|-------|-------|---------------------|
| **A** | Product/UI Lock | Packaging-agnostic; visual and interaction contract definition |
| **B** | Frontend Scaffold | Bridge interface creation; event cataloguing |
| **C** | Core Wiring + Behavior | Marimo integration; deterministic behavior verification |
| **D** | Tauri Shell Integration | Desktop packaging; adapter implementation |

### Sequencing Logic

The phase ordering follows a **dependency-first** philosophy:

1. **Phase A (UI Lock)** must complete before any frontend scaffolding begins, ensuring visual contracts are frozen.
2. **Phase B (Scaffold)** creates the abstraction layer (OR8HostBridge) that Phase C binds against.
3. **Phase C (Wiring)** validates the abstraction works with the marimo core before Phase D introduces the shell.
4. **Phase D (Tauri)** is explicitly gated behind successful completion of Phases A-C.

**Assessment:** The sequencing is sound. It prevents the common failure mode of tightly coupling UI to shell before understanding the product behavior. The gate-at-phase-boundary model ensures each layer is stable before the next layer integrates.

---

## 2. OR8HostBridge Interface Concept

### Architecture

The OR8HostBridge is defined as a **single interface with dual adapters**:

```
OR8HostBridge (interface)
    |
    +-- web_stub adapter   (current development mode)
    +-- tauri_adapter      (packaging mode)
```

### Contract Responsibilities

The bridge is responsible for mediating:
- **Event dispatch** from UI to runtime
- **Command routing** from UI controls to backend endpoints
- **Platform abstraction** hiding shell-specific calls

### Immediate Work Queue Alignment

Per Section 6, the bridge work includes:
1. Writing the `OR8HostBridge` contract spec and command catalog
2. Refactoring any direct Tauri-coupled frontend references into bridge calls

### Assessment

The dual-adapter pattern is a well-established abstraction technique. Key strengths:
- **Separation of concerns**: UI components never see Tauri APIs
- **Testability**: The `web_stub` enables full testing without shell dependencies
- **Future-proofing**: Additional adapters (Electron, native, etc.) can be added without touching shared code

**Caveat:** The plan does not define the interface contract itself (method signatures, event types, payload schemas). This is identified as Phase B work, which is appropriate.

---

## 3. Tauri-Agnostic Design Rules

### Explicit Constraints (Section 4)

The plan establishes **four non-negotiable rules**:

1. **No direct `window.__TAURI__` calls** inside shared UI components.
   - This is the primary isolation rule. All Tauri access must route through the bridge.

2. **Use one host bridge interface** with two adapters.
   - Enforces the abstraction pattern described above.

3. **Keep render contract: `WIDGET` primary, `IFRAME` fallback rehearsed.**
   - Maintains the existing orchestr8 rendering strategy regardless of shell.

4. **Preserve founder style lock:**
   - Reduced palette
   - Dual-color particle transition baseline
   - Deco-future typography and component treatment
   - This ensures visual identity is not subject to shell-integration drift.

5. **Linux desktop only** (`x86_64`), Fedora + Linux Mint compatibility gates.
   - Constrains the packaging scope to reduce integration surface area.

### Assessment

The Tauri-agnostic rules are explicit and enforceable. The prohibition on `window.__TAURI__` in shared components is the critical boundary enforcement mechanism. Combined with the bridge abstraction, this creates a clear separation between:
- **Shell-agnostic UI code** (testable, portable)
- **Shell-specific adapter code** (isolated, minimal)

The style lock provision is particularly important: it prevents the common drift where visual identity gets compromised during platform adaptation work.

---

## 4. Acceptance Gates

### Phase-Gated Acceptances

| Phase | Gate Criteria |
|-------|---------------|
| **A** | 1. Static layout parity sign-off from founder<br>2. Command intent map approved with no unresolved ambiguity |
| **B** | 1. UI runs without Tauri<br>2. Zero direct shell-specific calls in shared components<br>3. Existing canonical test gates remain green |
| **C** | 1. Canonical reliability/city tests pass<br>2. Phreak/settings/file actions route through bridge contract |
| **D** | 1. No core logic rewrites for shell adoption<br>2. Same UI interaction contracts pass on shell<br>3. Fullscreen high-resolution desktop performance meets target gate |

### Go/No-Go Gates Before Tauri (Section 7)

The pre-Phase-D gates require:
1. UI contract stable across main surfaces
2. Settings command map stable and test-backed
3. Canonical replay gates green (`11 passed` + rehearsal pass)
4. No open severity-1 ambiguity in integration map

### Assessment

The gate structure is appropriately **conservative** for a project where the packaging layer is deferred. Key observations:

- **Phase A gates** rely on human sign-off (founder approval), which is appropriate for visual and intent contracts.
- **Phase B gates** include automated checks (zero shell calls, tests green) that can be enforced in CI.
- **Phase C gates** verify end-to-end behavior through existing canonical test infrastructure.
- **Phase D gates** emphasize **no core rewrites** — this is the key validation that the abstraction worked.

The "no severity-1 ambiguity" provision is critical: it prevents entering Tauri integration with unresolved command-routing or state-management questions.

---

## Summary Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Phase structure | **Strong** | Dependency-first, clear boundaries |
| OR8HostBridge concept | **Sound** | Dual-adapter pattern is industry-validated |
| Tauri-agnostic rules | **Clear** | Enforceable via code review + CI |
| Acceptance gates | **Robust** | Human + automated gates at each phase |

### Recommendation

The plan is **ready for execution** pending:
1. Founder approval of Phase A visual contract extraction (Section 6, item 1)
2. OR8HostBridge contract spec drafting (Section 6, item 2)

The "app-first, Tauri-ready" philosophy is correctly implemented: the product behavior drives the shell, not the reverse.

---

*Analysis generated from SOT/APP_FIRST_TAURI_READY_PLAN.md*

# Extraction Packet: MaestroWizard -> City Guide

**Packet ID**: P07-C3-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / UX & Onboarding
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `MaestroWizard` logic to create the "City Guide" - an interactive, step-by-step onboarding system for new users entering Code City. This system provides a modal-based, state-managed tour and setup process.

## 2. Orchestr8 + Code City Value

- **City Onboarding**: The wizard's step logic (`agent-selection` -> `directory-selection` -> `conversation`) maps perfectly to a "New City Construction" workflow.
- **Interactive Tour Guide**: The `MaestroWizard` can be repurposed as a 3D avatar (Orchestr8) that flies users through the city, explaining features.
- **Phase Review**: The `PhaseReviewScreen` logic is valuable for reviewing city blueprints before applying changes.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Wizard Engine** | `src/renderer/components/Wizard/MaestroWizard.tsx` | 1-734 | Core state machine and transitions. |
| **Context** | `src/renderer/components/Wizard/WizardContext.tsx` | (Ref) | State management (current step, history). |
| **Layer Stack** | `src/renderer/contexts/LayerStackContext.tsx` | (Ref) | Modal priority management (crucial for overlays). |

## 4. Conversion Plan (Clean-Room)

1. **Abstract Wizard Engine**: Create `orchestr8.ux.wizard`.
    - Decouple UI from logic (Step Machine).
    - Support "3D Steps" where the camera moves to different city sectors.
2. **Port Transitions**: Extract the CSS animations (`wizard-slide-up`, `wizard-fade-in`) into reusable `CityTransition` primitives.
3. **Visual Adaptation**:
    - Instead of a flat modal, the wizard becomes a "Holographic Overlay" in the 3D view.
    - Steps trigger camera flights (e.g., "Select Directory" zooms into the Foundation Layer).

## 5. Expected Target Contracts

- `Orchestr8.UX.TourService`: Manages guided tours.
- `Orchestr8.City.CameraService`: Controls view during steps.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "First Run Experience" implementation.

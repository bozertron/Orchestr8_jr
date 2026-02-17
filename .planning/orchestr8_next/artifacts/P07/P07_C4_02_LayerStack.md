# Extraction Packet: LayerStack -> Holographic Layers

**Packet ID**: P07-C4-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / UI Management
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `LayerStackContext` logic to create a "Holographic Projection System" for managing overlays in Code City. This system handles the z-indexing, focus trapping, and escape-hatch behavior of UI elements projected over the 3D world.

## 2. Orchestr8 + Code City Value

- **Holographic Overlays**: Managing 2D UI panels (modals) floating in 3D space requires distinct "Projection Planes".
- **Focus Management**: The "Capture Focus" logic is critical when users switch between navigating the 3D city (flight controls) and interacting with a 2D terminal (typing).
- **Escape Hatch**: A standardized global "Back/Close" mechanism (Escape key) that peels away the top-most holographic layer.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Layer Stack** | `src/renderer/contexts/LayerStackContext.tsx` | 1-90 | Context provider, escape handling, stack API. |
| **Hooks** | `src/renderer/hooks/useLayerStack.ts` | (Implied) | Implementation of stack logic. |

## 4. Conversion Plan (Clean-Room)

1. **Abstract Projection System**: Create `orchestr8.ui.projection`.
    - Define `ProjectionPlane` (z-index, opacity, interaction mode).
    - Implement `FocusController` to manage input routing (3D World vs. 2D Plane).
2. **Visual Adaptation**:
    - **Glass Panes**: Visualize layers as semi-transparent glass panes sliding in front of the camera.
    - **Depth of Field**: Blur the background city when a high-priority layer (modal) is active.

## 5. Expected Target Contracts

- `Orchestr8.UI.WindowManager`: Manages 2D/3D integration.
- `Orchestr8.Input.FocusManager`: Routes keyboard events.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "UI Infrastructure".

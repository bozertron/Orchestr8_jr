# Extraction Packet: QuickActions -> City Dispatch

**Packet ID**: P07-C4-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Orchestration
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `QuickActionsModal` logic to create "City Dispatch" - a centralized command center for broadcasting signals (actions) to various city systems. This system acts as a "Broadcast Tower" or "Emergency Dispatch" for user intent.

## 2. Orchestr8 + Code City Value

- **Broadcast Tower**: Visualized as a central tower in the city. When the user activates it (Cmd+K), it emits a "signal pulse" that highlights compatible buildings (systems).
- **Signal routing**: The logic decouples intent ("Open Settings") from execution ("SettingsModal.open()"), enabling a message-bus architecture for city systems.
- **Shortcut Registry**: Serves as the "City Codebook" for keyboard-driven navigation.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Quick Actions** | `src/renderer/components/QuickActionsModal.tsx` | 1-800+ | Command definition, filtering, execution logic. |
| **Shortcut Types** | `src/renderer/types/index.ts` | (Ref) | Standardized shortcut definitions. |

## 4. Conversion Plan (Clean-Room)

1. **Abstract Dispatch Engine**: Create `orchestr8.orchestration.dispatch`.
    - Define `DispatchSignal` (Intent, Payload, Target).
    - Implement `SignalRouter` to route signals to registered city systems.
2. **Visual Adaptation**:
    - **The Tower**: A tall structure in the city center.
    - **Signal Beams**: When active, beams of light connect the tower to available services (e.g., "Git Log" beam connects to the Version Control District).
3. **Search Logic**: Port the fuzzy matching logic for finding city addresses (commands) quickly.

## 5. Expected Target Contracts

- `Orchestr8.Signals.CommandBus`: Pub/sub system for commands.
- `Orchestr8.City.VFX`: Visualizing signal propagation.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Command & Control" infrastructure.

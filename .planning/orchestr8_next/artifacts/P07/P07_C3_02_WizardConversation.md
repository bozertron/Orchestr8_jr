# Extraction Packet: WizardConversation -> City Comms

**Packet ID**: P07-C3-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Communication & Feedback
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `WizardConversationView` logic to power "City Comms" - the in-world communication interface. This component handles streaming text, typing indicators, tool execution visualization, and error handling in a chat-like interface.

## 2. Orchestr8 + Code City Value

- **Agent Speech Bubbles**: The `WizardMessageBubble` and `TypingIndicator` logic can be projected above active agents in the city.
- **Thinking Visualization**: The `ThinkingDisplay` component (showing tool executions) is perfect for a "Brain Activity" overlay on agents, showing what they are working on real-time.
- **Streaming Response**: Robust logic for handling streaming token updates, essential for live agent feedback.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Conversation View** | `src/renderer/components/InlineWizard/WizardConversationView.tsx` | 1-790 | Main chat container, auto-scroll, streaming. |
| **Thinking** | `ThinkingDisplay` (internal) | 279-341 | Displays tool execution state/logs. |
| **Typing** | `TypingIndicator` (internal) | 85-194 | Animated "working" state. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Comms Logic**: Create `orchestr8.ux.comms`.
    - Standardize `Message`, `ToolExecution`, `Error` types.
2. **Visual Adaptation**:
    - **World-Space UI**: Project chat bubbles into 3D space above agents.
    - **HUD Mode**: Dock the conversation view as a "Heads Up Display" for detailed logs.
    - **Thinking Particles**: Map `ThinkingDisplay` tool events to particle effects around the agent (e.g., "Reading File" emits blue particles).

## 5. Expected Target Contracts

- `Orchestr8.City.AgentLayer`: Agent visualization and overlays.
- `Orchestr8.UX.NotificationService`: System-wide alerts/errors.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Agent Interaction" features.

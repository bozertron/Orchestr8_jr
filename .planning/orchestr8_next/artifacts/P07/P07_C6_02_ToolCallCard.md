# Extraction Packet: ToolCallCard -> Action Inspector

**Packet ID**: P07-C6-02
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Explainability
**Risk Class**: Low
**Licensing Concern**: No

## 1. Idea Summary

Extract the `ToolCallCard` component to create a "City Action Inspector". This component provides a deep-dive view into the inputs and outputs of every agent action, enabling forensic analysis of how a building was modified or why a specific plan was generated.

## 2. Orchestr8 + Code City Value

- **Building Forensics**: "Click into" a completed building to see the exact CLI commands or API calls used to construct it.
- **Explainable Failure**: When an agent fails to modify a city sector, the operator can see the literal error message and raw JSON output to debug the prompt or tool configuration.
- **Verification Confidence**: Collapsible input/output sections allow the operator to verify complex data structures (like geometry JSON or dependency graphs) at a glance.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **Tool Call Card** | `src/renderer/components/ToolCallCard.tsx` | 1-270 | Collapsible sections, status icons, and JSON formatting. |
| **Status Icons** | `StatusIcon` | 47-63 | Mapping of tool states (running, success, error) to visual cues. |
| **JSON Viewer** | `CollapsibleContent` | 68-118 | Smart truncation and expansion of large JSON payloads. |

## 4. Conversion Plan (Clean-Room)

1. **Extract Introspection Engine**: Create `orchestr8.explainability.inspector`.
    - Standardize the `ActionPayload` schema to include `tool_name`, `input_blob`, and `output_blob`.
    - Implement "Smart Diff" logic to highlight changes between input and output.
2. **Visual Adaptation**:
    - **The Inspection Lens**: A HUD element that appears when the operator's cursor hovers over a city object.
    - **The Ledger building**: A physical location in the city where "Architectural Action Cards" are archived.
3. **Contracts**: Define the `ActionProvider` interface for tools to push their payloads into the inspector.

## 5. Expected Target Contracts

- `Orchestr8.Explainability.IntrospectionService`: Retrieves historical action details.
- `Orchestr8.City.AuditTrail`: Connects city objects to their construction inspector cards.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "Introspection & Audit" implementation.

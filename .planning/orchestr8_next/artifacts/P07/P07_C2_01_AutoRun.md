# Extraction Packet: AutoRun -> City Automation

**Packet ID**: P07-C2-01
**Source**: 2ndFid (Explorer Lane)
**Theme**: Code City / Automation & Logistics
**Risk Class**: Low
**Licensing Concern**: No (Standard React/Markdown libs)

## 1. Idea Summary

Extract the `AutoRun` batch execution engine to power "City Logistics" and "Agent Traffic". This system manages file modification queues, undo/redo states, and automated task execution on markdown documents.

## 2. Orchestr8 + Code City Value

- **City Traffic**: The batch execution logic (`BatchRunnerModal`) maps to agents (vehicles) moving between buildings (files) to perform work.
- **Time Travel**: The `useAutoRunUndo` hook provides a robust "Undo/Redo" stack, enabling a "City Time Machine" feature to revert changes.
- **Construction Drones**: The `AutoRun` component itself acts as a "Construction Drone" interface, modifying building content (markdown) automatically.

## 3. Source Provenance

| Component | Path | Lines | Notes |
|-----------|------|-------|-------|
| **AutoRun Engine** | `src/renderer/components/AutoRun.tsx` | 1-2226 | Core execution logic, state management. |
| **Undo Logic** | `src/renderer/hooks/useAutoRunUndo.ts` | (Implied) | Undo/redo stack management. *High Value*. |
| **Batch Runner** | `src/renderer/components/BatchRunnerModal.tsx` | (Ref) | Multi-file execution queue. |

## 4. Conversion Plan (Clean-Room)

1. **Abstract Execution Engine**: Create `orchestr8.automation.engine`.
    - Decouple UI (`AutoRunInner`) from logic.
    - Input: `TaskQueue` (list of files + prompts).
    - Output: `ExecutionStream` (progress, diffs, errors).
2. **Port Undo/Redo**: Extract `useAutoRunUndo` into a generic `TemporalStateService`.
    - Enable "Snapshotting" of city state.
3. **Visual Adaptation**:
    - Instead of a modal, visualize `AutoRun` as "Construction Fleets" surrounding target files in the 3D city.
    - Visual cues: Scaffolding appears around files being edited.

## 5. Expected Target Contracts

- `Orchestr8.Automation.QueueService`: Manages batch jobs.
- `Orchestr8.City.TrafficLayer`: Visualizes active agents/jobs.
- `Orchestr8.State.TemporalService`: Manages history/undo.

## 6. Handoff Recommendation

Route to `a_codex_plan` for "City Life" (Traffic/Automation) feature set.

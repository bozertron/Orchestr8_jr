# PRD P03: Workspace + IDE Bridges (Optional Adapters)

## Phase

- ID: `P03`
- Name: Workspace + IDE Bridges (Optional Adapters)
- Goal: Provide integration with VS Code/Zed/Antigravity/workspace tools without making core runtime depend on them.

## In Scope

- Workspace session abstraction
- Optional IDE adapters and capability negotiation
- Unified command model for open file, reveal path, launch task
- Session multiplexing for multiple projects

## Out of Scope

- Embedding full IDE UIs inside Orchestr8
- Hard dependency on any IDE extension lifecycle

## Functional Requirements

- FR-03-01: Core controls function with zero IDE adapters loaded.
- FR-03-02: When adapter present, IDE commands execute through adapter contract.
- FR-03-03: Support multiple concurrent workspace sessions.
- FR-03-04: Maintain action trace by workspace/session context.

## Integration Modes

- Mode A: no IDE (core-only)
- Mode B: local adapter active
- Mode C: remote bridge adapter active

## Files (Target)

- `orchestr8_next/workspaces/session.py`
- `orchestr8_next/workspaces/router.py`
- `orchestr8_next/adapters/ide_vscode.py`
- `orchestr8_next/adapters/ide_zed.py`
- `orchestr8_next/adapters/ide_antigravity.py`
- `orchestr8_next/workspaces/contracts.py`

## Acceptance Criteria

1. Core shell fully operational in Mode A.
2. IDE actions execute in Mode B/C when adapter available.
3. Adapter absence handled with user-visible but non-blocking fallback.
4. Multi-workspace routing verified with no cross-session leaks.

## Test Plan

- Adapter present/absent matrix tests
- Multi-workspace command routing tests
- Permission and path sanitization tests

## Risks

- R-03-01: Adapter code leaks into UI handlers.
- R-03-02: IDE connection volatility destabilizes sessions.

## Mitigations

- M-03-01: strict action->intent->adapter pipeline
- M-03-02: circuit-breaker on repeated adapter failures

## Exit Gate `G-P03`

Required evidence:
- Mode matrix test report (A/B/C)
- Multi-workspace routing report
- Adapter fallback UX validation


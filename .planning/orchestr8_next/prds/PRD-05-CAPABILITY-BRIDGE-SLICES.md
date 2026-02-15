# PRD P05: Capability Bridge + Slice Migration

## Phase

- ID: `P05`
- Name: Capability Bridge + Slice Migration
- Goal: Integrate high-value Orchestr8 capabilities through bridge contracts, one vertical slice at a time.

## In Scope

- Bridge contract definitions for capability slices
- Slice selection framework (candidate -> pilot -> promoted)
- Feature-flagged execution paths
- Shared contract test harness

## Out of Scope

- Full import of large legacy modules in one phase
- Replacing all Python services immediately

## Migration Principle

Never bulk-import large module estates. Promote one capability slice at a time with test and rollback.

## Slice Lifecycle

1. Select candidate capability
2. Define bridge request/response schema
3. Build shim adapter in orchestr8_next
4. Run in pilot mode behind feature flag
5. Compare outputs against legacy path
6. Promote or roll back

## Functional Requirements

- FR-05-01: Bridge request envelope has strict schema and version.
- FR-05-02: Bridge supports timeout/retry and deterministic fallback.
- FR-05-03: Each slice has explicit owner and test matrix.
- FR-05-04: Promotion requires parity and performance evidence.

## Files (Target)

- `orchestr8_next/capability_bridge/contracts.py`
- `orchestr8_next/capability_bridge/client.py`
- `orchestr8_next/capability_bridge/feature_flags.py`
- `orchestr8_next/capability_bridge/slices/` (per-slice adapters)
- `orchestr8_next/capability_bridge/tests/`

## Candidate Slice Categories

- code graph normalization
- health signal merge policy
- import/wiring analysis transforms
- ticket synthesis utilities
- deployment queue orchestration helpers

## Acceptance Criteria

1. At least one capability slice integrated in pilot mode.
2. Legacy and bridge outputs are comparable by contract tests.
3. Failure in bridge path auto-falls back to legacy adapter.
4. Promotion checklist completed for pilot slice.

## Risks

- R-05-01: Contract mismatch between legacy and bridge structures.
- R-05-02: Latency overhead negates expected gains.

## Mitigations

- M-05-01: Contract versioning + golden test fixtures
- M-05-02: Benchmark gate before promotion

## Exit Gate `G-P05`

Required evidence:
- Pilot slice parity report
- Bridge reliability test report
- Promotion decision memo


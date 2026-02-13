# PHASE-6-MODULE-AUDIT-SUMMARY.md Integration Guide

- Source: `.planning/codebase/PHASE-6-MODULE-AUDIT-SUMMARY.md`
- Total lines: `116`
- SHA256: `4660da207ea39ed37cdbcb838cac2d82bf072a8dcbb9a8f0aa7284a5b347a913`
- Memory chunks: `1`
- Observation IDs: `1018..1018`

## Why This Is Painful

- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `.planning/codebase/PHASE-6-MODULE-AUDIT-SUMMARY.md:35` **Issue:** Imported in maestro.py but NEVER instantiated
- `.planning/codebase/PHASE-6-MODULE-AUDIT-SUMMARY.md:40` **Issue:** Doesn't accept health data from HealthChecker
- `.planning/codebase/PHASE-6-MODULE-AUDIT-SUMMARY.md:53` │  HealthChecker ──❌──> 06_maestro.py                        │
- `.planning/codebase/PHASE-6-MODULE-AUDIT-SUMMARY.md:56` │  HealthChecker ──❌──> woven_maps.py                        │

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

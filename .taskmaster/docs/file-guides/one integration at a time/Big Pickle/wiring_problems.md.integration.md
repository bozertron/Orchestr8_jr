# wiring_problems.md Integration Guide

- Source: `one integration at a time/Big Pickle/wiring_problems.md`
- Total lines: `191`
- SHA256: `b85f0b059cf0f447814dd6fee9e456bb5588fc801d2eada626e79b64eae8b614`
- Memory chunks: `2`
- Observation IDs: `370..371`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/Big Pickle/wiring_problems.md:5` This audit focuses on the plugin architecture used in `IP/orchestr8_app.py` (v3.0). It identifies disconnected UI elements, hollow integrations, and architectural fragility.
- `one integration at a time/Big Pickle/wiring_problems.md:55` - **File:** `IP/plugins/06_maestro.py` (Line 691-757)
- `one integration at a time/Big Pickle/wiring_problems.md:58` - `JFDI` (Tasks Panel)
- `one integration at a time/Big Pickle/wiring_problems.md:78` - **File:** `IP/plugins/06_maestro.py` (Line 558, 811, 815, 819)
- `one integration at a time/Big Pickle/wiring_problems.md:90` - **Problem:** These buttons should trigger tab switches or open specific panels, but they are currently dead-ends that only provide log feedback.
- `one integration at a time/Big Pickle/wiring_problems.md:163` - **Integration Point:** `.orchestr8/combat_state.json`
- `one integration at a time/Big Pickle/wiring_problems.md:164` - **Problem:** `cleanup_stale_deployments` must be called explicitly. If the app crashes or is closed, "Combat" status (Purple) will persist indefinitely on files until a manual cleanup is triggered, leading to a "ghost in the machine" UI where files look active but aren't.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

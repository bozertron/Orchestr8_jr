# UI_PRESSURE_TEST_REPORT.md Integration Guide

- Source: `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md`
- Total lines: `225`
- SHA256: `19ff84c1671199976a7a577c0c1df853e5f91497fe8b3df6ac43e95da40eb0ac`
- Memory chunks: `2`
- Observation IDs: `479..480`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:1` # UI Pressure Test Report: 06_maestro.py
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:6` **Subject:** `IP/plugins/06_maestro.py` (The Void plugin)
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:12` The `06_maestro.py` plugin has a solid foundation but requires updates to align with the authoritative MaestroView.vue style guide. The plugin is **functional** but **incomplete** for production use.
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:86` The Void should display:
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:88` 2. **Status Overlays** - Three-color node states (Gold/Blue/Purple)
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:138` .maestro-top-row {
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:171` ✓ STATE_MANAGERS pattern correctly implemented
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:174` ✓ 06_maestro.py render() executes without errors
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:202` - Plugin architecture with `STATE_MANAGERS` injection
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:204` - Event handler pattern (toggle_collabor8, toggle_jfdi, etc.)
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:208` - The Void center should default to **graph view**, not chat
- `one integration at a time/docs/UI_PRESSURE_TEST_REPORT.md:209` - Chat should be a **secondary mode** or overlay

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

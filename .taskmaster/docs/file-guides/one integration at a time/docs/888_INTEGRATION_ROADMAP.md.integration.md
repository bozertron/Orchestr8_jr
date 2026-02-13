# 888_INTEGRATION_ROADMAP.md Integration Guide

- Source: `one integration at a time/docs/888_INTEGRATION_ROADMAP.md`
- Total lines: `505`
- SHA256: `cf5be6d5ae3e702af9bfea12ed40fe7745d4abca7c51a4b4acce2ce4265f60b4`
- Memory chunks: `5`
- Observation IDs: `402..406`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:56` **Integration Point:** Runs continuously in background, reports to maestro
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:67` - Surfaces insights to Emperor and maestro
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:126` **Revised:** Assigned to maestro (intrusive stuff needs visibility)
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:132` - ALL senses data surfaces through maestro panel
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:135` **Why maestro?** Privacy - intrusive capabilities need clear visibility
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:143` **Integration Point:** maestro panel, clearly labeled "SENSES ACTIVE" indicator
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:266` **What it is:** Base architecture that ALL [name]8 tools must implement
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:274` **Why it matters:** Lets maestro talk to ALL tools consistently
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:287` # orchestr8_settings.toml
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:313` assigned_to = "maestro"
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:385` **Action:** Create `orchestr8_settings.toml` with all tool/agent settings
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:405` - Connect to maestro for reporting
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:434` #### BP-888-008: senses → maestro Assignment
- `one integration at a time/docs/888_INTEGRATION_ROADMAP.md:437` - Move senses controls to maestro panel

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# LLM_INFLUENCE_REFERENCE.md Integration Guide

- Source: `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md`
- Total lines: `482`
- SHA256: `aaab6807e7d98366e828429837747038dc1ee3fe98a2e78314115f52a76af92e`
- Memory chunks: `5`
- Observation IDs: `451..455`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:76` base_url = "http://127.0.0.1:11434/v1"  # MUST include /v1
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:122` 1. All code must be complete and runnable
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:155` - 00_welcome.py through 06_maestro.py
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:163` - All plugins must apply MaestroView color variables
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:212` - Gold accents for interactive elements
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:214` - Purple for active/combat states
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:227` When you type `@df` in a prompt, Marimo injects the actual value/schema of that variable:
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:304` - status must be one of: 'working', 'broken', 'combat'
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:349` │   │   └── orchestr8.css     # CSS variables AI should reference
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:351` │   │   └── orchestr8.md      # Prompt templates (Layer 3)
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:392` - Gold/Working: All imports resolve, typecheck passes
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:394` - Purple/Combat: General currently deployed and active
- `one integration at a time/docs/LLM_INFLUENCE_REFERENCE.md:441` - **Q:** How verbose should global rules be? Token cost vs. consistency trade-off.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

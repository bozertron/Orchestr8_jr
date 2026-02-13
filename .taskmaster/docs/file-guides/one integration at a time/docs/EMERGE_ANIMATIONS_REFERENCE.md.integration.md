# EMERGE_ANIMATIONS_REFERENCE.md Integration Guide

- Source: `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md`
- Total lines: `802`
- SHA256: `5f082d4cd3c4672412aaf870255f863835f9a8151f1cb754ec90c3bf4c4f1747`
- Memory chunks: `7`
- Observation IDs: `415..421`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:24` /* IP/styles/orchestr8.css */
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:125` custom_css = ["IP/styles/orchestr8.css"]
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:269` **IMPORTANT:** The `.style()` method wraps content in a `<div>`. The animation CSS must already be defined (via custom CSS file or earlier mo.Html injection).
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:288` /* In orchestr8.css */
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:632` | Infinite loops | UI should be static after emerge |
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:642` /* IP/styles/animations.css - Import via orchestr8.css */
- `one integration at a time/docs/EMERGE_ANIMATIONS_REFERENCE.md:761` - **Q:** CSS file vs. inline mo.Html() - which should be primary?

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# PRD1.md Integration Guide

- Source: `one integration at a time/PRD1.md`
- Total lines: `150`
- SHA256: `c428ac94aa3558157d593ddf3e4d085cc70f1f1b42c393bf6e19a7df1770f696`
- Memory chunks: `2`
- Observation IDs: `22..23`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/PRD1.md:59` * **Constraint:** The table must be selectable (`selection='single'`). When a row is clicked, update `selected_file`.
- `one integration at a time/PRD1.md:75` * **Rendering:** Create a helper `render_badge(status)` that returns HTML spans (Green/Orange/Purple) for the table view.
- `one integration at a time/PRD1.md:89` * **Marimo Integration:** The graph must return an HTML string (`net.generate_html()`) and be wrapped in `mo.Html()`.
- `one integration at a time/PRD1.md:91` * The graph must auto-update when `scan_button` is pressed.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

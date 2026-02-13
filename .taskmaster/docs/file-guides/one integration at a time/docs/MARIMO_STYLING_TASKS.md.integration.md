# MARIMO_STYLING_TASKS.md Integration Guide

- Source: `one integration at a time/docs/MARIMO_STYLING_TASKS.md`
- Total lines: `539`
- SHA256: `fdbb82b5b8ae9c1939563e4e3fb052b5733ded6689682ad7a3b8ae65a3b9a8e5`
- Memory chunks: `5`
- Observation IDs: `461..465`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:3` **Target:** Match MaestroView.vue aesthetic within Marimo constraints
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:12` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:17` /* orchestr8.css - MaestroView.vue Alignment */
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:66` custom_css = ["IP/styles/orchestr8.css"]
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:91` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:114` ### Task 1.2: Style All Buttons - Gold Theme
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:115` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:118` /* Primary buttons - Gold */
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:148` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:174` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:201` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:207` [data-cell-name='maestro_header'] {
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:244` | 06_maestro.py | `maestro_header` | Top navigation |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:245` | 06_maestro.py | `mermaid_graph` | Status visualization |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:246` | 06_maestro.py | `fiefdom_list` | Fiefdom sidebar |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:247` | 06_maestro.py | `command_input` | Bottom input bar |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:258` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:347` ### Task 5.1: Style 06_maestro.py (The Void)
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:348` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:399` **File:** `IP/styles/orchestr8.css`
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:413` /* Note: Mermaid node colors should be set in the diagram definition, not CSS */
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:486` | Button hover | Gold fill | ☐ |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:488` | Working badge | Gold | ☐ |
- `one integration at a time/docs/MARIMO_STYLING_TASKS.md:490` | Combat badge | Purple | ☐ |

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

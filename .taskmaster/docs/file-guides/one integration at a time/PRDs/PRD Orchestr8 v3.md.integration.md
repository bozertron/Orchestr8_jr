# PRD Orchestr8 v3.md Integration Guide

- Source: `one integration at a time/PRDs/PRD Orchestr8 v3.md`
- Total lines: `135`
- SHA256: `44c518ab8b33787000574928a51bfb55b7628f23d29afe499140e09d3cbe303e`
- Memory chunks: `2`
- Observation IDs: `673..674`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.

## Anchor Lines

- `one integration at a time/PRDs/PRD Orchestr8 v3.md:6` The system relies on a rigid directory layout. The Agent must verify this structure exists.
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:12` │   ├── orchestr8_app.py    # (Host) The Main Marimo Application
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:21` │       └── 05_cli_bridge.py# (New) The TypeScript Scaffold Bridge
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:31` ## 2. The Host Application (`orchestr8_app.py`)
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:35` The Host must initialize a `STATE_MANAGERS` dictionary passed to every plugin.
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:46` 4.  Execute `module.render(STATE_MANAGERS)`.
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:102` ## 5. The Scaffold Bridge (`05_cli_bridge.py`)
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:128` 3.  **Host Creation:** Write `IP/orchestr8_app.py` with the dynamic loader.
- `one integration at a time/PRDs/PRD Orchestr8 v3.md:130` 5.  **Bridge Implementation:** Ensure `05_cli_bridge.py` correctly calls the `list-plugins` command defined in `scaffold-cli.ts`.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

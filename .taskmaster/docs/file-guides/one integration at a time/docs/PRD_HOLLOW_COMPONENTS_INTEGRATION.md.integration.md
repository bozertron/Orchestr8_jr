# PRD_HOLLOW_COMPONENTS_INTEGRATION.md Integration Guide

- Source: `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md`
- Total lines: `263`
- SHA256: `eee2ce20d2d2b35a32b83b75c72a2200cd5e50e9f22fe6b49c8ee772fb030770`
- Memory chunks: `3`
- Observation IDs: `471..473`

## Why This Is Painful

- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:25` Combat Tracker → Purple Glow in Code City
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:34` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:47` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:59` **Current:** Nodes only show Gold (working) or Blue (broken)
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:60` **Needed:** Query CombatTracker and show Purple for files with active LLM
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:70` **Needed:** LLM integration should read model/API key from settings
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:78` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:124` tracker.deploy(selected, "maestro-chat", "claude-sonnet-4")
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:145` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:162` title=f"actu8 - {selected or 'maestro'}"
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:191` node.status = "combat"  # Will render as Purple
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:198` **File:** `IP/plugins/06_maestro.py`
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:207` settings_file = Path("orchestr8_settings.toml")
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:227` | Working | Gold | `#D4AF37` | All imports resolve, no active LLM |
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:229` | Combat | Purple | `#9D4EDD` | LLM currently deployed to this file |
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:255` - `IP/plugins/06_maestro.py` - Main integration point
- `one integration at a time/docs/PRD_HOLLOW_COMPONENTS_INTEGRATION.md:263` - `orchestr8_settings.toml` - Settings source

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

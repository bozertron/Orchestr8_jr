# orchestr8_standalone.py Integration Guide

- Source: `one integration at a time/orchestr8_standalone.py`
- Total lines: `708`
- SHA256: `13f7d98b0f98c5e3c2f58d55c996e294f949cb1a5db1b7be66705c9ed454730c`
- Memory chunks: `6`
- Observation IDs: `665..670`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/orchestr8_standalone.py:143` files_df.at[index, "status"] = "COMPLEX"  # Purple - high complexity
- `one integration at a time/orchestr8_standalone.py:145` files_df.at[index, "status"] = "NORMAL"  # Gold - working
- `one integration at a time/orchestr8_standalone.py:233` "NORMAL": "#D4AF37",   # Gold - working (matches Woven Maps)
- `one integration at a time/orchestr8_standalone.py:235` "COMPLEX": "#a855f7",  # Purple - high complexity
- `one integration at a time/orchestr8_standalone.py:236` "ERROR": "#1fbdea",    # Teal/Blue - broken (matches Woven Maps)
- `one integration at a time/orchestr8_standalone.py:237` "COMBAT": "#9D4EDD",   # Purple - LLM deployed (matches Woven Maps)
- `one integration at a time/orchestr8_standalone.py:513` """Load available models from orchestr8_settings.toml."""
- `one integration at a time/orchestr8_standalone.py:517` settings_file = Path("orchestr8_settings.toml")
- `one integration at a time/orchestr8_standalone.py:526` # Fallback - user should configure in settings

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

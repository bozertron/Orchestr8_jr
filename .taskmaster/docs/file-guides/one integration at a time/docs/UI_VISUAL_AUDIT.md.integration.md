# UI_VISUAL_AUDIT.md Integration Guide

- Source: `one integration at a time/docs/UI_VISUAL_AUDIT.md`
- Total lines: `311`
- SHA256: `037864627ff35fcc1344bf9dc7f889005af8ade6db799c3af0bf41ee469e4efb`
- Memory chunks: `3`
- Observation IDs: `481..483`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/UI_VISUAL_AUDIT.md:14` | **Layer 1: Top Panel** | Fully specified | Partial (06_maestro.py) | MEDIUM |
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:15` | **Layer 2: Bottom Panel** | Fully specified | Partial (06_maestro.py) | MEDIUM |
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:16` | **Layer 3: Right Slider (JFDI)** | Fully specified | Placeholder only | HIGH |
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:33` - Gold = Working, Blue = Broken, Purple = Combat
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:41` - `orchestr8_mcp.py` can generate Mermaid text diagrams
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:65` **Implementation (06_maestro.py):**
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:84` - maestro (m) logo with 3 states: OFF/OBSERVE/ON
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:90` **Implementation (06_maestro.py):**
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:93` # Has: Apps, Matrix, Files, maestro, Search, Terminal, Send, Attach
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:95` # Missing: 3-state maestro toggle (OFF/OBSERVE/ON)
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:105` - maestro 3-state cycle (currently just a button)
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:108` - Color states for maestro logo
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:114` ### Layer 3: Right Slider (JFDI Tickets)
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:124` **Implementation (06_maestro.py):**
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:126` # Lines 424-443: JFDI panel
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:149` - No left slider in 06_maestro.py
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:172` - Reads/writes orchestr8_settings.toml
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:211` **Implementation (06_maestro.py lines 43-49):**
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:255` | maestro | State toggle |
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:263` | maestro | Summon toggle (wrong behavior) |
- `one integration at a time/docs/UI_VISUAL_AUDIT.md:272` 1. **maestro 3-state toggle** - Core UX

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

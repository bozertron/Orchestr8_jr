# Color Normalization Audit (Task 11)

Date: 2026-02-14  
Scope: `IP/styles/orchestr8.css`, `IP/plugins/06_maestro.py`, `IP/woven_maps.py`, `IP/static/woven_maps_3d.js`

## Canonical Palette

- `gold_metallic`: `#D4AF37`
- `blue_dominant`: `#1fbdea`
- `purple_combat`: `#9D4EDD`
- `gold_dark`: `#B8860B`
- `gold_saffron`: `#F4C430`
- `bg_primary`: `#0A0A0B`
- `bg_elevated`: `#121214`

## Root Causes Found

1. **Status-color logic drift in Maestro panel rendering**
- `build_summon_results()` treated every non-`working` status as `broken` blue.
- Effect: `combat` state rendered with incorrect color semantics.

2. **Hardcoded inline grays bypassing theme variables**
- Several inline styles in `06_maestro.py` used direct `#666`/`#888` values.
- Effect: visual drift from central theme tokens (`--text-secondary`, `--text-muted`).

3. **Python/JS wireframe mismatch in Woven Maps**
- `JS_COLORS["wireframe"]` was `#333333`, while embedded JS `COLORS.wireframe` was `#2a2a2a`.
- Effect: two rendering paths could produce different wireframe tones.

4. **Duplicate raw literals in `ColorScheme` dataclass**
- `ColorScheme` repeated raw canonical hex values instead of referencing `COLORS`.
- Effect: future drift risk if canonical constants change.

## Corrections Applied

### `IP/plugins/06_maestro.py`
- Updated summon loading color to canonical constant (`GOLD_METALLIC`).
- Replaced binary status color with full map:
  - `working -> GOLD_METALLIC`
  - `broken -> BLUE_DOMINANT`
  - `combat -> PURPLE_COMBAT`
- Replaced inline gray hex values in panel text with CSS vars:
  - `var(--text-secondary)` and `var(--text-muted)`
- Replaced inline canonical hex values in panels with module constants where appropriate.

### `IP/woven_maps.py`
- Extended `JS_COLORS` to include `cycle`, `edge`, and `edge_broken` for parity with embedded JS usage.
- Bound `ColorScheme` defaults to canonical `COLORS` map instead of repeated hex literals.
- Normalized embedded JS `COLORS.wireframe` from `#2a2a2a` to `#333333` to match Python-side config.

### `IP/styles/orchestr8.css`
- Replaced one hardcoded content text color with tokenized value:
  - `.emerged-message .content` now uses `var(--text-primary)`.

## Intentional Non-Canonical Colors (Kept)

These are intentional semantic accents, not canonical state palette colors:
- `#ff4444` for cycle highlighting
- `#ff6b6b` for broken-edge emphasis
- gray neutral text shades in Woven Maps overlays used for hierarchy/readability

## Validation

- `python -m py_compile IP/plugins/06_maestro.py IP/woven_maps.py` passed.
- Hex scan confirmed canonical state colors remain dominant and drift points above were corrected.

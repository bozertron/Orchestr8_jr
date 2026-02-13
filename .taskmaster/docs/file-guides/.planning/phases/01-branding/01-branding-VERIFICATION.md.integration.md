# 01-branding-VERIFICATION.md Integration Guide

- Source: `.planning/phases/01-branding/01-branding-VERIFICATION.md`
- Total lines: `139`
- SHA256: `d3f6d054910918392464a628c08155a3344d70c7ba24713883f1d7fa2fc7b751`
- Memory chunks: `2`
- Observation IDs: `1043..1044`

## Why This Is Painful

- Constraint-heavy document: treat as canonical rules, not optional guidance.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `.planning/phases/01-branding/01-branding-VERIFICATION.md:5` score: 3/3 must-haves verified
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:10` **Phase Goal:** Application consistently displays "orchestr8" branding across all visible text, CSS classes, and documentation
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:22` | 1 | User sees 'orchestr8' in top row brand display (not 'stereOS') | ✓ VERIFIED | `06_maestro.py:873-875` - HTML displays `orchestr8-brand` with split `orchestr` + `8` |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:23` | 2 | Browser DevTools shows CSS classes prefixed with '.orchestr8-*' (not '.stereos-*') | ✓ VERIFIED | `06_maestro.py:189-201` - CSS defines `.orchestr8-brand`, `.orchestr8-prefix`, `.orchestr8-suffix` |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:24` | 3 | Developer reading docstrings sees 'orchestr8' references (not 'stereOS') | ✓ VERIFIED | `06_maestro.py:7`, `woven_maps.py:110`, `woven_maps_nb.py:118` - All reference "orchestr8" |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:32` | `IP/plugins/06_maestro.py` | Brand display and CSS classes | ✓ VERIFIED | 1297 lines, contains `orchestr8-brand` in HTML (873-875) and CSS (189-201), NO_STUBS, exports render() |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:33` | `IP/woven_maps.py` | Code City visualization | ✓ VERIFIED | 1981 lines, contains "orchestr8" in ColorScheme docstring (110), NO_STUBS, exports classes |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:34` | `IP/woven_maps_nb.py` | Code City notebook | ✓ VERIFIED | 1996 lines, contains "orchestr8" in ColorScheme docstring (118), NO_STUBS, exports Marimo cells |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:38` **IP/plugins/06_maestro.py:**
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:46` - Level 3 (Wired): ✓ WIRED (imported and used by 06_maestro.py for Code City rendering)
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:57` | `IP/plugins/06_maestro.py` | Browser rendering | HTML template string | ✓ WIRED | CSS classes defined (189-201), injected via `css_injection` (1275), HTML brand uses classes (873-875) |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:63` .orchestr8-brand {
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:69` .orchestr8-prefix {
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:73` .orchestr8-suffix {
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:74` color: #D4AF37;  # Gold
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:78` <div class="orchestr8-brand">
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:79` <span class="orchestr8-prefix">orchestr</span><span class="orchestr8-suffix">8</span>
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:83` The CSS is injected via `mo.Html(MAESTRO_CSS)` and the brand HTML is rendered in the `top_row` component. The pattern `orchestr8-brand.*orchestr8-prefix` is present and correctly wired.
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:89` | BRAND-01: Application displays "orchestr8" instead of "stereOS" in all visible text | ✓ SATISFIED | None - brand HTML verified in `06_maestro.py:873-875` |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:90` | BRAND-02: CSS classes use `.orchestr8-*` prefix instead of `.stereos-*` | ✓ SATISFIED | None - CSS classes verified in `06_maestro.py:189-201` |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:91` | BRAND-03: Docstrings reference "orchestr8" not "stereOS" | ✓ SATISFIED | None - docstrings verified in all three files |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:99` | `IP/plugins/06_maestro.py` | 317, 927, 940, 957, 1145 | `placeholder` keyword | ℹ️ INFO | Legitimate use - CSS class names (`.void-placeholder`) and UI placeholder text, not stub code |
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:106` - `grep -in "stereos" IP/plugins/06_maestro.py` → 0 results
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:112` **ALL MUST-HAVES VERIFIED ✓**
- `.planning/phases/01-branding/01-branding-VERIFICATION.md:114` Phase 1 goal is ACHIEVED. The application now consistently displays "orchestr8" branding across all visible text, CSS classes, and documentation.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.

# CSS Compatibility Fixes (Task 15)

Date: 2026-02-14  
Scope: source-level and served static bundle compatibility fixes for Firefox-first runtime.

## Root Cause

Most console CSS warnings were not from `IP/styles/orchestr8.css`; they came from marimo frontend/generated assets:
- nested markdown CSS selectors emitted in shipped `markdown-renderer-*.css`
- modern/experimental declarations in bundled `index-*.css` (`text-wrap`, print-only properties)
- stale prefixed text-size-adjust variants in previous builds

## Fixes Applied

### 1) Flatten markdown renderer CSS (remove nested syntax)
- File: `marimo/frontend/src/components/markdown/markdown-renderer.css`
- Change: replaced nested selectors with explicit selectors (`.mo-markdown-renderer h1`, `.mo-markdown-renderer li > input`, etc.)
- Why: prevents parser/bad-selector warnings in stricter engines.

### 2) Normalize print CSS for broader parser support
- File: `marimo/frontend/src/css/app/print.css`
- Change:
  - `break-after: avoid-page` -> `break-after: avoid` + `page-break-after: avoid`
  - removed `orphans` and `widows` declarations from print block
- Why: avoids unsupported-value/property warnings while preserving print intent.

### 3) Extend PostCSS normalization pass
- File: `marimo/frontend/postcss.config.cjs`
- Change:
  - remove `font-smooth` and `-moz-osx-font-smoothing`
  - remove `-moz-text-size-adjust`
  - convert `text-wrap` to `overflow-wrap` with sane fallback values
- Why: ensures generated CSS avoids known compatibility pain points at build time.

### 4) Immediate runtime patch to shipped static assets
- Files:
  - `marimo/marimo/_static/assets/markdown-renderer-k9pRl-fK.css`
  - `marimo/marimo/_static/assets/index-GQcFJc44.css`
- Change:
  - replaced markdown asset with flattened selector source
  - rewrote bundled declarations in-place:
    - `text-wrap:*` -> `overflow-wrap: break-word`
    - `break-after: avoid-page` -> `break-after: avoid; page-break-after: avoid`
    - removed `orphans`, `widows`, `font-smooth`, `-moz-osx-font-smoothing`, `-moz-text-size-adjust`
- Why: applies fixes immediately without waiting for a frontend rebuild.

## Validation

Pattern scans after patching:
- No `@source` in shipped markdown renderer asset.
- No nested `&` selectors in shipped markdown renderer asset.
- No `-moz-text-size-adjust`, `font-smooth`, `-moz-osx-font-smoothing` in shipped `index-*.css`.
- `text-wrap` declarations replaced by `overflow-wrap`.
- print block now uses `break-after: avoid` + `page-break-after: avoid`.

## Notes

- Source files are now corrected; static bundle was also patched for immediate runtime effect.
- If/when frontend assets are rebuilt, these source-level changes should persist the compatibility behavior.

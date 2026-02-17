# Phase: Color Token Drift Audit - Research

**Researched:** 2026-02-16
**Domain:** Color Token Compliance
**Confidence:** HIGH

## Summary

Audited all hardcoded hex color values across the Orchestr8 codebase against `VISUAL_TOKEN_LOCK.md` (the single source of truth). 

**Primary conflict found:** 8 files use `#B8860B` (dark goldenrod) for `gold-dark` but the token lock specifies `#C5A028` (a richer, more saturated gold). This is a legacy value from the original MaestroView.vue that was never updated when the token lock was established on 2026-02-15.

Most other color usages correctly match the locked tokens. The main drift is isolated to the `#B8860B` vs `#C5A028` conflict.

**Primary recommendation:** Replace all instances of `#B8860B` with `#C5A028` across the 8 identified files to achieve full token compliance.

## Standard Stack

### Locked Color Tokens (from VISUAL_TOKEN_LOCK.md)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `--bg-obsidian` | #050505 | 5,5,5 | Background base |
| `--gold-dark` | #C5A028 | 197,160,40 | Primary accent, borders |
| `--gold-light` | #F4C430 | 244,196,48 | Highlight accent, hover |
| `--teal` | #00E5E5 | 0,229,229 | Secondary accent, text |
| `--text-grey` | #CCC | 204,204,204 | Standard text |

### State Colors

| State | Token | Hex |
|-------|-------|-----|
| Working | `--state-working` | #D4AF37 |
| Broken | `--state-broken` | #1fbdea |
| Combat | `--state-combat` | #9D4EDD |

## Architecture Patterns

### Color Constant Pattern

All Python files should import colors from a centralized source or define constants matching the token lock:

```python
# CORRECT - matches token lock
GOLD_DARK = "#C5A028"

# INCORRECT - legacy value
GOLD_DARK = "#B8860B"
```

### CSS Variable Pattern

CSS should use CSS custom properties with token lock values:

```css
:root {
    --gold-dark: #C5A028;  /* CORRECT */
    --gold-light: #F4C430;
}
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| Color definitions | Hardcode values in each file | Reference token lock constants |
| State colors | Use arbitrary colors | Use `--state-working`, `--state-broken`, `--state-combat` |

## Common Pitfalls

### Pitfall 1: Legacy Color Values

**What goes wrong:** Files still use `#B8860B` (dark goldenrod) instead of `#C5A028` (locked gold-dark)

**Why it happens:** Historical drift from original MaestroView.vue reference - the lock was only recently established (2026-02-15)

**How to avoid:** Use grep to audit: `grep -r "#B8860B" --include="*.py"`

**Warning signs:** Comments like "Maestro default" or "from MaestroView.vue" indicate legacy values

### Pitfall 2: CSS Variable Naming Inconsistency

**What goes wrong:** Some files use `--status-*` prefix instead of `--state-*`

**Why it happens:** Parallel naming conventions developed

**How to avoid:** Use token lock naming exactly

## Code Examples

### Python Color Constants (CORRECT)

```python
# From IP/city/settings_service.py - CORRECT
COLOR_TOKENS = {
    "--state-working": "#D4AF37",
    "--state-broken": "#1fbdea",
    "--state-combat": "#9D4EDD",
    "--bg-obsidian": "#050505",
    "--gold-dark": "#C5A028",
    "--gold-light": "#F4C430",
    "--teal": "#00E5E5",
    "--text-grey": "#CCC",
}
```

### Python Color Constants (INCORRECT - Needs Fix)

```python
# From IP/features/maestro/config.py - NEEDS FIX
GOLD_DARK = "#B8860B"  # Should be "#C5A028"
```

## Complete Audit Results

### CONFLICTS FOUND (8 files, 10 instances)

| File | Line | Current Value | Should Be | Token Name | Status |
|------|------|---------------|-----------|------------|--------|
| IP/plugins/06_maestro.py | 20 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/mermaid_theme.py | 4 | #B8860B | #C5A028 | gold-dark (stroke) | **FAIL** |
| IP/mermaid_theme.py | 7 | #B8860B | #C5A028 | gold-dark (stroke) | **FAIL** |
| IP/mermaid_theme.py | 8 | #B8860B | #C5A028 | gold-dark (stroke) | **FAIL** |
| IP/mermaid_theme.py | 11 | #B8860B | #C5A028 | gold-dark (stroke) | **FAIL** |
| IP/features/maestro/config.py | 17 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/woven_maps.py | 62 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/plugins/components/ticket_panel.py | 11 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/plugins/components/file_explorer_panel.py | 15 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/plugins/components/comms_panel.py | 27 | #B8860B | #C5A028 | gold-dark | **FAIL** |
| IP/plugins/components/calendar_panel.py | 28 | #B8860B | #C5A028 | gold-dark | **FAIL** |

### CORRECT USAGES (Representative Sample)

| File | Line | Value | Token | Status |
|------|------|-------|-------|--------|
| IP/city/settings_service.py | 40 | #C5A028 | gold-dark | **PASS** |
| IP/plugins/components/deploy_panel.py | 23 | #C5A028 | gold-dark | **PASS** |
| IP/features/maestro/views/shell.py | 9 | #C5A028 | gold-dark | **PASS** |
| IP/styles/orchestr8.css | 12 | #C5A028 | gold-dark | **PASS** |
| IP/barradeau_builder.py | 32 | 0xD4AF37 | COLOR_WORKING | **PASS** |
| IP/static/woven_maps_3d.js | 16 | 0xD4AF37 | COLOR_WORKING | **PASS** |

### OTHER DIRECTORIES SCAN

| Directory | Files Scanned | Conflicts Found |
|-----------|---------------|-----------------|
| a_codex_plan/orchestr8_next/ | 35 hex values | 0 conflicts |
| mingos_settlement_lab/ | 99 hex values | 0 conflicts |
| or8_founder_console/ | 2301 hex values | 0 conflicts (in source code; venv excluded) |

Note: The `or8_founder_console` results include many values from installed dependencies (textual, pygments, pyvis) which are external libraries and not subject to the token lock.

## Fix Effort Estimate

| File | Changes Needed | Estimated Minutes |
|------|----------------|-------------------|
| IP/plugins/06_maestro.py | 1 instance | 2 min |
| IP/mermaid_theme.py | 4 instances | 5 min |
| IP/features/maestro/config.py | 1 instance | 2 min |
| IP/woven_maps.py | 1 instance | 2 min |
| IP/plugins/components/ticket_panel.py | 1 instance | 2 min |
| IP/plugins/components/file_explorer_panel.py | 1 instance | 2 min |
| IP/plugins/components/comms_panel.py | 1 instance | 2 min |
| IP/plugins/components/calendar_panel.py | 1 instance | 2 min |
| **TOTAL** | **11 instances across 8 files** | **~19 minutes** |

## Open Questions

1. **Should mermaid_theme.py strokes use #C5A028 or a darker shade?**
   - Current: `#B8860B` is used for stroke (outlines)
   - Locked token is `#C5A028` for gold-dark
   - Recommendation: Use `#C5A028` for consistency, but verify visual appearance in Mermaid diagrams

2. **Should documentation files be updated?**
   - Some documentation references `#B8860B` as historical reference
   - These are not runtime code but may cause confusion
   - Recommendation: Update documentation to note the token lock change

## Sources

### Primary (HIGH confidence)
- `/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md` - Token lock (authoritative)
- Direct file inspection of all Python files in scope

### Secondary (MEDIUM confidence)
- Codebase grep searches for hex patterns
- Cross-reference verification against token lock values

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Token lock is authoritative document
- Architecture: HIGH - Clear pattern for color constants
- Pitfalls: HIGH - Confirmed 8 files with legacy values

**Research date:** 2026-02-16
**Valid until:** Until token lock is updated (no expiration for static audit)

# Task ID: 11

**Title:** CSS Color System Audit and Normalization

**Status:** pending

**Dependencies:** None

**Priority:** high

**Description:** Audit all CSS color values across IP/styles/orchestr8.css, IP/plugins/06_maestro.py, and IP/woven_maps.py to ensure exact compliance with canonical color palette. Normalize any deviations to match MaestroView.vue color spec.

**Details:**

1. Read canonical color definitions from MaestroView.vue lines 11-17:
   - --blue-dominant: #1fbdea
   - --gold-metallic: #D4AF37
   - --gold-dark: #B8860B
   - --gold-saffron: #F4C430
   - --bg-primary: #0A0A0B
   - --bg-elevated: #121214

2. Audit IP/styles/orchestr8.css:
   - Verify :root CSS variables match canonical values exactly
   - Check all hardcoded hex values for compliance
   - Ensure --purple-combat: #9D4EDD is present

3. Audit IP/plugins/06_maestro.py:
   - Verify BLUE_DOMINANT, GOLD_METALLIC, GOLD_DARK, GOLD_SAFFRON, BG_PRIMARY, BG_ELEVATED, PURPLE_COMBAT constants match
   - Check any inline styles in mo.Html() calls

4. Audit IP/woven_maps.py:
   - Verify COLORS dict matches canonical values
   - Verify JS_COLORS dict matches

5. Audit IP/static/woven_maps_3d.js:
   - Check CONFIG_3D color constants (hex format as integers)

6. Create color-normalization.md report listing:
   - All locations with color values
   - Any deviations found
   - Corrections made

Pseudo-code:
```python
CANONICAL = {
    'gold_metallic': '#D4AF37',
    'blue_dominant': '#1fbdea',
    'gold_dark': '#B8860B',
    'gold_saffron': '#F4C430',
    'bg_primary': '#0A0A0B',
    'bg_elevated': '#121214',
    'purple_combat': '#9D4EDD'
}
for file in FILES:
    for color_ref in extract_colors(file):
        if color_ref.value not in CANONICAL.values():
            flag_deviation(color_ref)
```

**Test Strategy:**

1. grep -r for all hex color patterns (#[0-9A-Fa-f]{6}) across IP/ directory
2. Verify each found value against canonical palette
3. Run marimo run orchestr8.py and visually confirm gold/blue/purple rendering
4. Check browser DevTools computed styles for key elements

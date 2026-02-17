# Task ID: 13

**Title:** Local Font Registration System for Settings UI

**Status:** pending

**Dependencies:** 12

**Priority:** high

**Description:** Create font registration infrastructure to expose local fonts from Font/ directory as selectable options in Settings UI. Include Cal Sans (woff), HardCompn (ttf), and mini_pixel-7 (ttf) as available deco-style options.

**Details:**

1. Create font face declarations for local fonts:
```css
/* IP/styles/fonts.css */
@font-face {
    font-family: 'Cal Sans';
    src: url('/static/fonts/CalSans-SemiBold.woff') format('woff');
    font-weight: 600;
    font-display: swap;
}

@font-face {
    font-family: 'HardCompn';
    src: url('/static/fonts/HardCompn.ttf') format('truetype');
    font-weight: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Mini Pixel 7';
    src: url('/static/fonts/mini_pixel-7.ttf') format('truetype');
    font-weight: normal;
    font-display: swap;
}
```

2. Create font configuration in pyproject_orchestr8_settings.toml:
```toml
[ui.fonts]
available = ['Cal Sans', 'HardCompn', 'Mini Pixel 7', 'JetBrains Mono', 'IBM Plex Mono']
default_headline = 'Cal Sans'
default_body = 'IBM Plex Sans'
default_mono = 'JetBrains Mono'
```

3. Create static file serving for fonts:
   - Copy Font/*.ttf and Font/*.woff to IP/static/fonts/
   - Ensure marimo serves static files from IP/static/

4. Create font loader helper in 06_maestro.py:
```python
def load_font_css() -> str:
    fonts_path = Path(__file__).parent.parent / 'styles' / 'fonts.css'
    if fonts_path.exists():
        return f'<style>{fonts_path.read_text()}</style>'
    return ''
```

5. Add font injection to render() function alongside CSS injection

**Test Strategy:**

1. Verify @font-face rules load without 404 errors
2. Test each font renders correctly by setting as primary font
3. Verify fallback behavior when font file missing
4. Check font-display: swap prevents FOIT

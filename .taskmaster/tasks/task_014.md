# Task ID: 14

**Title:** Settings UI Font Selector Implementation

**Status:** pending

**Dependencies:** 13

**Priority:** medium

**Description:** Add font selection dropdown to Settings panel in 06_maestro.py that persists preference and applies selected font to appropriate CSS variables at runtime.

**Details:**

1. Add font state management in render():
```python
get_selected_headline_font, set_selected_headline_font = mo.state('Cal Sans')
get_selected_body_font, set_selected_body_font = mo.state('IBM Plex Sans')
get_selected_mono_font, set_selected_mono_font = mo.state('JetBrains Mono')
```

2. Load available fonts from settings:
```python
def get_available_fonts() -> dict:
    settings = load_settings()
    return settings.get('ui', {}).get('fonts', {
        'available': ['Cal Sans', 'HardCompn', 'Mini Pixel 7'],
        'default_headline': 'Cal Sans'
    })
```

3. Add font selectors to Settings panel section:
```python
if get_show_settings():
    headline_font_picker = mo.ui.dropdown(
        options=available_fonts,
        value=get_selected_headline_font(),
        label='Headline Font',
        on_change=set_selected_headline_font
    )
    # Similar for body_font and mono_font
```

4. Generate runtime CSS override:
```python
def build_font_override_css() -> str:
    return f'''
    :root {{
        --font-headline: '{get_selected_headline_font()}', monospace;
        --font-body: '{get_selected_body_font()}', sans-serif;
        --font-mono: '{get_selected_mono_font()}', monospace;
    }}
    '''
```

5. Inject font override after base CSS in render()

**Test Strategy:**

1. Change font selection and verify visual update
2. Refresh page and verify preference persists (if using localStorage)
3. Test fallback when selected font unavailable
4. Verify font changes apply to correct element categories

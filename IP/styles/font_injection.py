"""HTML Head injection backup method for fonts and CSS."""


def get_font_head_html() -> str:
    """Return HTML head injection for Google Fonts."""
    return """
<!-- Font preload and fallback -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<!-- Font fallback CSS -->
<style>
/* Fallback fonts in case Google Fonts fail */
:root {
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'Courier New', monospace;
    --font-ui: 'IBM Plex Mono', 'Courier New', monospace;
}

/* Force font loading */
body, button, input, textarea, select, code, pre {
    font-family: var(--font-mono) !important;
}
</style>
"""


def get_theme_meta_tags() -> str:
    """Return meta tags for theme consistency."""
    return """
<!-- Theme meta tags -->
<meta name="theme-color" content="#0A0A0B">
<meta name="color-scheme" content="dark">

<!-- Prevent FOUC (Flash of Unstyled Content) -->
<style>
/* Prevent flash of unstyled content */
body {
    background-color: #0A0A0B !important;
    color: #e8e8e8 !important;
}
</style>
"""


def get_complete_head_injection() -> str:
    """Return complete HTML head injection for Orchestr8."""
    return get_font_head_html() + "\n" + get_theme_meta_tags()

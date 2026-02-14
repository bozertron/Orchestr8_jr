"""HTML head injection backup method for fonts and CSS."""

from IP.styles.font_profiles import build_font_profile_css, resolve_font_profile_name


def get_font_head_html(profile: str | None = None) -> str:
    """Return HTML head injection for the selected local font profile."""
    resolved = resolve_font_profile_name(profile)
    return f"<style>{build_font_profile_css(resolved)}</style>"


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


def get_complete_head_injection(profile: str | None = None) -> str:
    """Return complete HTML head injection for Orchestr8."""
    return get_font_head_html(profile) + "\n" + get_theme_meta_tags()

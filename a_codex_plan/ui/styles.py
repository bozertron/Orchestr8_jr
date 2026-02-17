"""CSS integration helpers for a_codex_plan.

Simplified CSS loading inspired by Orchestr8 patterns.
"""

import os


def load_css() -> str:
    """Load orchestr8 CSS for component styling.

    Returns:
        HTML string with CSS style tag
    """
    # Try to load from IP/styles/orchestr8.css
    css_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "IP",
        "styles",
        "orchestr8.css",
    )

    # Also check relative to project root
    if not os.path.exists(css_path):
        css_path = "IP/styles/orchestr8.css"

    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            css_content = f.read()
        return f"<style>{css_content}</style>"

    # Fallback: return empty style tag
    return "<style>/* orchestr8.css not found */</style>"


def inject_css() -> str:
    """Inject CSS into the page.

    Returns:
        HTML string for CSS injection
    """
    return load_css()


def get_css_path() -> str:
    """Get the path to orchestr8.css.

    Returns:
        Path string to CSS file
    """
    return "IP/styles/orchestr8.css"

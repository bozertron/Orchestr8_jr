"""Status HTML helpers for consistent styling across Orchestr8."""


def status_badge(status: str) -> str:
    """Return styled HTML badge for status."""
    status_lower = status.lower()
    if status_lower == "working":
        return '<span class="badge-working">WORKING</span>'
    elif status_lower == "broken":
        return '<span class="badge-broken">BROKEN</span>'
    elif status_lower == "combat":
        return '<span class="badge-combat">COMBAT</span>'
    elif status_lower == "normal":
        return '<span class="badge-working">NORMAL</span>'
    elif status_lower == "warning":
        return '<span class="badge-working">WARNING</span>'
    elif status_lower == "complex":
        return '<span class="badge-combat">COMPLEX</span>'
    elif status_lower == "error":
        return '<span class="badge-broken">ERROR</span>'
    else:
        return f'<span class="badge-broken">{status.upper()}</span>'


def fiefdom_indicator(status: str) -> str:
    """Return colored circle indicator."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
        "normal": "#D4AF37",
        "warning": "#D4AF37",
        "complex": "#9D4EDD",
        "error": "#1fbdea",
    }
    color = colors.get(status.lower(), "#1fbdea")
    return f'<span style="color: {color}; font-size: 1.5rem;">●</span>'


def status_icon(status: str) -> str:
    """Return appropriate icon for status."""
    status_lower = status.lower()
    icons = {
        "working": "[WORKING]",
        "broken": "[BROKEN]",
        "combat": "[COMBAT]",
        "normal": "[NORMAL]",
        "warning": "[WARNING]",
        "complex": "[COMPLEX]",
        "error": "[ERROR]",
    }
    return icons.get(status_lower, "[UNKNOWN]")


def status_color(status: str) -> str:
    """Return hex color for status."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
        "normal": "#D4AF37",
        "warning": "#D4AF37",
        "complex": "#9D4EDD",
        "error": "#1fbdea",
    }
    return colors.get(status.lower(), "#666666")


def styled_status_text(status: str, text: str = "") -> str:
    """Return status text with appropriate color."""
    if text is None:
        text = status.upper()
    color = status_color(status)
    return f'<span style="color: {color}; font-weight: 500;">{text}</span>'


def progress_bar(current: int, total: int, status: str = "working") -> str:
    """Generate a simple progress bar with status color."""
    if total == 0:
        percentage = 0
    else:
        percentage = min(100, max(0, (current / total) * 100))

    color = status_color(status)
    return f"""
    <div style="
        width: 100%;
        height: 8px;
        background-color: var(--bg-elevated);
        border: 1px solid var(--bg-surface);
        border-radius: 4px;
        overflow: hidden;
    ">
        <div style="
            width: {percentage}%;
            height: 100%;
            background-color: {color};
            transition: width 0.3s ease;
        "></div>
    </div>
    """

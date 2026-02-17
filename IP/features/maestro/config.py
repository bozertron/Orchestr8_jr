"""Canonical Maestro configuration and styling helpers."""

from __future__ import annotations

from pathlib import Path

from IP.styles.font_profiles import build_font_profile_css, resolve_font_profile_name

# Canonical identity lock: "maestro" refers only to the flagship Orchestr8 agent.
FLAGSHIP_AGENT_SLUG = "maestro"

PLUGIN_NAME = "The Void"
PLUGIN_ORDER = 6

BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_PRIMARY = "#050505"
BG_ELEVATED = "#121214"
PURPLE_COMBAT = "#9D4EDD"
MAESTRO_STATES = ("ON", "OFF", "OBSERVE")


def get_model_config() -> dict:
    """Get model configuration from pyproject_orchestr8_settings.toml."""
    try:
        import toml

        settings_file = Path("pyproject_orchestr8_settings.toml")
        if settings_file.exists():
            settings = toml.load(settings_file)
            doctor = settings.get("agents", {}).get("doctor", {})
            return {
                "model": doctor.get("model", "claude-sonnet-4-20250514"),
                "max_tokens": doctor.get("max_tokens", 8192),
            }
    except Exception:
        pass

    return {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8192,
    }


def get_ui_font_profile() -> str:
    """Get the configured UI font profile from settings."""
    try:
        import toml

        settings_file = Path("pyproject_orchestr8_settings.toml")
        if settings_file.exists():
            settings = toml.load(settings_file)
            ui_general = settings.get("ui", {}).get("general", {})
            return resolve_font_profile_name(ui_general.get("font_profile"))
    except Exception:
        pass

    return resolve_font_profile_name(None)


def load_orchestr8_css() -> str:
    """Load consolidated CSS from IP/styles/orchestr8.css."""
    css_path = Path(__file__).resolve().parents[2] / "styles" / "orchestr8.css"
    try:
        css_content = css_path.read_text(encoding="utf-8")
        selected_font_profile = get_ui_font_profile()
        font_css = build_font_profile_css(selected_font_profile)
        return f"<style>{font_css}\n\n{css_content}</style>"
    except Exception as e:
        return f"<style>/* CSS load failed: {e} */</style>"

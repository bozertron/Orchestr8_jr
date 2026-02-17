"""Font profile helpers for Orchestr8 runtime CSS injection."""

from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_FONT_DIR = _REPO_ROOT / "Font"

_FONT_SOURCES: dict[str, tuple[Path, str, str]] = {
    "hardcompn": (
        _FONT_DIR / "HardCompn.ttf",
        "Orchestr8 HardCompn",
        "font/ttf",
    ),
    "calsans": (
        _FONT_DIR / "CalSans-SemiBold.woff",
        "Orchestr8 CalSans",
        "font/woff",
    ),
    "mini_pixel_7": (
        _FONT_DIR / "mini_pixel-7.ttf",
        "Orchestr8 Mini Pixel",
        "font/ttf",
    ),
}

_PROFILE_DEFINITIONS: dict[str, dict[str, str]] = {
    "phreak_nexus": {
        "label": "Phreak Nexus (Marcellus SC + Poiret One + VT323)",
        "headline": "'Marcellus SC', serif",
        "body": "'Poiret One', cursive",
        "mono": "'VT323', monospace",
    },
    "regal_deco": {
        "label": "Regal Deco (HardCompn + CalSans + Mini Pixel)",
        "headline": "'Orchestr8 HardCompn', 'Orchestr8 CalSans', 'Trebuchet MS', sans-serif",
        "body": "'Orchestr8 CalSans', 'Segoe UI', 'Helvetica Neue', sans-serif",
        "mono": "'Orchestr8 Mini Pixel', 'Orchestr8 HardCompn', 'Courier New', monospace",
    },
    "deco_console": {
        "label": "Deco Console (HardCompn + Mini Pixel)",
        "headline": "'Orchestr8 HardCompn', 'Trebuchet MS', sans-serif",
        "body": "'Orchestr8 HardCompn', 'Segoe UI', sans-serif",
        "mono": "'Orchestr8 Mini Pixel', 'Courier New', monospace",
    },
    "clean_utility": {
        "label": "Clean Utility (CalSans + Mini Pixel)",
        "headline": "'Orchestr8 CalSans', 'Segoe UI', sans-serif",
        "body": "'Orchestr8 CalSans', 'Segoe UI', sans-serif",
        "mono": "'Orchestr8 Mini Pixel', 'Courier New', monospace",
    },
}

DEFAULT_FONT_PROFILE = "phreak_nexus"


# Google Fonts CDN URL for Phreak fonts
GOOGLE_FONTS_URL = "https://fonts.googleapis.com/css2?family=Marcellus+SC&family=Poiret+One&family=VT323&display=swap"

# Google Fonts profile - uses CDN instead of local files
_GOOGLE_FONTS_PROFILES = {"phreak_nexus"}


def _build_google_fonts_import() -> str:
    """Return CSS @import for Google Fonts."""
    return f"@import url('{GOOGLE_FONTS_URL}');"


def resolve_font_profile_name(value: str | None) -> str:
    """Normalize persisted profile values to a known profile key."""
    if not isinstance(value, str):
        return DEFAULT_FONT_PROFILE

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in _PROFILE_DEFINITIONS:
        return normalized
    return DEFAULT_FONT_PROFILE


def available_font_profile_labels() -> dict[str, str]:
    """Return dict of available font profile keys to display labels."""
    return {
        profile_key: profile_def.get("label", profile_key)
        for profile_key, profile_def in _PROFILE_DEFINITIONS.items()
    }


def _build_font_face(source_key: str) -> str:
    path, family, mime = _FONT_SOURCES[source_key]
    if not path.exists():
        return ""

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    format_hint = "woff" if mime == "font/woff" else "truetype"
    return (
        "@font-face {"
        f"font-family: '{family}';"
        f"src: url(data:{mime};base64,{encoded}) format('{format_hint}');"
        "font-style: normal;"
        "font-weight: 400;"
        "font-display: swap;"
        "}"
    )


@lru_cache(maxsize=1)
def _hardcompn_available() -> bool:
    """Return True when HardCompn is present as a distinct font asset."""
    hard_path = _FONT_SOURCES["hardcompn"][0]
    mini_path = _FONT_SOURCES["mini_pixel_7"][0]

    if not hard_path.exists():
        return False

    # Guard against accidental duplicate payloads mislabeled as HardCompn.
    if mini_path.exists() and hard_path.read_bytes() == mini_path.read_bytes():
        return False

    return True


def _strip_hardcompn(stack: str) -> str:
    return (
        stack.replace("'Orchestr8 HardCompn', ", "")
        .replace(", 'Orchestr8 HardCompn'", "")
        .replace("'Orchestr8 HardCompn'", "")
    )


@lru_cache(maxsize=8)
def build_font_profile_css(profile_name: str | None = None) -> str:
    """Build CSS for runtime font-face declarations and variable overrides."""
    resolved_profile = resolve_font_profile_name(profile_name)
    profile = dict(_PROFILE_DEFINITIONS[resolved_profile])

    # Handle Google Fonts profiles specially
    if resolved_profile in _GOOGLE_FONTS_PROFILES:
        google_import = _build_google_fonts_import()
        return f"""/* Orchestr8 font profile: {resolved_profile} */
{google_import}
:root,
.light,
.light-theme,
body.light,
body.light-theme {{
    --orchestr8-font-headline: {profile["headline"]};
    --orchestr8-font-body: {profile["body"]};
    --orchestr8-font-mono: {profile["mono"]};
}}
""".strip()

    # Legacy profiles use local font files
    include_hardcompn = _hardcompn_available()

    if not include_hardcompn:
        profile["headline"] = _strip_hardcompn(profile["headline"])
        profile["body"] = _strip_hardcompn(profile["body"])
        profile["mono"] = _strip_hardcompn(profile["mono"])

    source_keys = ["calsans", "mini_pixel_7"]
    if include_hardcompn:
        source_keys.insert(0, "hardcompn")

    font_faces = "\n".join(
        _build_font_face(source_key) for source_key in source_keys
    ).strip()

    if not font_faces:
        font_faces = (
            "/* Orchestr8 custom font files not found; using system fallbacks. */"
        )

    return f"""/* Orchestr8 font profile: {resolved_profile} */
{font_faces}
:root,
.light,
.light-theme,
body.light,
body.light-theme {{
    --orchestr8-font-headline: {profile["headline"]};
    --orchestr8-font-body: {profile["body"]};
    --orchestr8-font-mono: {profile["mono"]};
}}
""".strip()

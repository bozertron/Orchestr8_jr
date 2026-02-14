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

DEFAULT_FONT_PROFILE = "regal_deco"


def available_font_profile_labels() -> dict[str, str]:
    """Return profile keys and labels for UI dropdowns."""
    return {key: profile["label"] for key, profile in _PROFILE_DEFINITIONS.items()}


def resolve_font_profile_name(value: str | None) -> str:
    """Normalize persisted profile values to a known profile key."""
    if not isinstance(value, str):
        return DEFAULT_FONT_PROFILE

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in _PROFILE_DEFINITIONS:
        return normalized
    return DEFAULT_FONT_PROFILE


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


@lru_cache(maxsize=8)
def build_font_profile_css(profile_name: str | None = None) -> str:
    """Build CSS for runtime font-face declarations and variable overrides."""
    resolved_profile = resolve_font_profile_name(profile_name)
    profile = _PROFILE_DEFINITIONS[resolved_profile]

    font_faces = "\n".join(
        _build_font_face(source_key)
        for source_key in ("hardcompn", "calsans", "mini_pixel_7")
    ).strip()

    if not font_faces:
        font_faces = "/* Orchestr8 custom font files not found; using system fallbacks. */"

    return f"""
/* Orchestr8 font profile: {resolved_profile} */
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

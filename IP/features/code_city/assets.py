"""Shared Code City asset and template loading helpers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path


def script_safe(source: str) -> str:
    """Escape literal </script> sequences for inline script embedding."""
    return source.replace("</script", "<\\/script")


def read_text_if_exists(path: Path) -> str:
    """Read a UTF-8 file when present; otherwise return an empty string."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def script_tag(local_source: str, fallback_src: str) -> str:
    """Build a script tag preferring inline local source with CDN fallback."""
    if local_source.strip():
        return f"<script>{script_safe(local_source)}</script>"
    return f'<script src="{fallback_src}"></script>'


@lru_cache(maxsize=1)
def load_woven_maps_template() -> str:
    """Load the canonical Woven Maps iframe template from static assets."""
    template_path = Path(__file__).resolve().parents[2] / "static" / "woven_maps_template.html"
    return template_path.read_text(encoding="utf-8")


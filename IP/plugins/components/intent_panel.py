# IP/plugins/components/intent_panel.py
"""
Intent Panel - C2P Intent Scanner Visualization

Displays harvested intents from the Founder Console backend.
Uses locked visual tokens:
- Labels: --font-ui (Poiret One, cursive)
- Intent text: --teal (#00E5E5)
- Borders: --gold-dark (#C5A028)
"""

from datetime import datetime
from typing import Any, List, Optional
import marimo as mo
import json
import os

# Locked Visual Tokens
TEAL = "#00E5E5"
GOLD_DARK = "#C5A028"
GOLD_LIGHT = "#F4C430"
BG_ELEVATED = "#121214"
FONT_UI = "'Poiret One', cursive"

# Intent panel CSS - slides from RIGHT
INTENT_PANEL_CSS = f"""
<style>
.intent-panel-overlay {{
    position: fixed;
    top: 0;
    right: 0;
    width: 450px;
    height: 100vh;
    background: {BG_ELEVATED};
    border-left: 2px solid {GOLD_DARK};
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.intent-panel-header {{
    padding: 16px;
    border-bottom: 2px solid {GOLD_DARK};
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.intent-panel-title {{
    color: {GOLD_LIGHT};
    font-family: {FONT_UI};
    font-size: 18px;
    letter-spacing: 0.05em;
}}

.intent-panel-close {{
    background: transparent;
    border: 1px solid {GOLD_DARK};
    color: {TEAL};
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 11px;
}}

.intent-panel-close:hover {{
    background: {GOLD_DARK};
    color: {BG_ELEVATED};
}}

.intent-panel-body {{
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}}

.intent-filter-bar {{
    margin-bottom: 16px;
    display: flex;
    gap: 8px;
    align-items: center;
}}

.intent-filter-select {{
    background: transparent;
    border: 1px solid {GOLD_DARK};
    color: {TEAL};
    padding: 6px 10px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 11px;
}}

.intent-scan-button {{
    background: {GOLD_DARK};
    border: none;
    color: {BG_ELEVATED};
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-family: {FONT_UI};
    font-size: 12px;
}}

.intent-scan-button:hover {{
    background: {GOLD_LIGHT};
}}

.intent-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.intent-card {{
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid {GOLD_DARK};
    border-radius: 6px;
    padding: 12px;
}}

.intent-card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}}

.intent-type-badge {{
    font-family: {FONT_UI};
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 3px;
    background: {GOLD_DARK};
    color: {BG_ELEVATED};
}}

.intent-source {{
    font-family: monospace;
    font-size: 10px;
    color: #888;
}}

.intent-text {{
    color: {TEAL};
    font-family: {FONT_UI};
    font-size: 14px;
    line-height: 1.4;
    margin-bottom: 8px;
}}

.intent-meta {{
    display: flex;
    justify-content: space-between;
    font-family: monospace;
    font-size: 10px;
    color: #666;
}}

.intent-actions {{
    display: flex;
    gap: 6px;
    margin-top: 8px;
}}

.intent-action-btn {{
    background: transparent;
    border: 1px solid {GOLD_DARK};
    color: {GOLD_LIGHT};
    padding: 4px 8px;
    border-radius: 3px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
}}

.intent-action-btn:hover {{
    background: {GOLD_DARK};
    color: {BG_ELEVATED};
}}

.intent-empty {{
    text-align: center;
    color: #666;
    font-family: {FONT_UI};
    padding: 40px;
}}

.intent-loading {{
    text-align: center;
    color: {TEAL};
    font-family: monospace;
    padding: 20px;
}}
</style>
"""


class IntentPanel:
    """
    Panel for displaying C2P intents from the Founder Console.
    """

    def __init__(self, project_root: str):
        self.project_root = project_root
        self._visible = False
        self._intents = []
        self._loading = False
        self._error = None

    def set_visible(self, visible: bool) -> None:
        """Show or hide the panel."""
        self._visible = visible

    def is_visible(self) -> bool:
        """Check if panel is visible."""
        return self._visible

    def set_loading(self, loading: bool) -> None:
        """Set loading state."""
        self._loading = loading

    def set_intents(self, intents: List[dict]) -> None:
        """Set intents data."""
        self._intents = intents
        self._loading = False

    def set_error(self, error: str) -> None:
        """Set error message."""
        self._error = error
        self._loading = False

    def render(self) -> Any:
        """Render the intent panel."""
        if not self._visible:
            return mo.md("")

        # Build filter options
        status_options = ["ALL", "UNPROCESSED", "PROCESSED", "PROPOSED", "DISCARDED"]

        # Build intent cards
        intent_cards = []
        if self._loading:
            intent_cards.append(
                mo.Html(f'<div class="intent-loading">Scanning repositories...</div>')
            )
        elif self._error:
            intent_cards.append(
                mo.Html(f'<div class="intent-empty">Error: {self._error}</div>')
            )
        elif not self._intents:
            intent_cards.append(
                mo.Html(
                    f'<div class="intent-empty">No intents found.<br/>Click "Scan Repos" to harvest intents.</div>'
                )
            )
        else:
            for intent in self._intents:
                card = self._build_intent_card(intent)
                intent_cards.append(card)

        # Panel HTML
        panel_html = f"""
        <div class="intent-panel-overlay">
            <div class="intent-panel-header">
                <span class="intent-panel-title">C2P INTENT QUEUE</span>
                <button class="intent-panel-close" onclick="this.closest('.intent-panel-overlay').remove()">CLOSE</button>
            </div>
            <div class="intent-panel-body">
                <div class="intent-list">
                    {"".join([str(c) for c in intent_cards])}
                </div>
            </div>
        </div>
        """

        return mo.Html(INTENT_PANEL_CSS + panel_html)

    def _build_intent_card(self, intent: dict) -> str:
        """Build HTML for a single intent card."""
        intent_type = intent.get("type", "TODO")
        source = intent.get("source_repo", "unknown")
        text = intent.get("intent_text", "")
        file_path = intent.get("file_path", "")
        line_number = intent.get("line_number", "")
        status = intent.get("status", "UNPROCESSED")

        return f"""
        <div class="intent-card">
            <div class="intent-card-header">
                <span class="intent-type-badge">{intent_type}</span>
                <span class="intent-source">{source}</span>
            </div>
            <div class="intent-text">{text}</div>
            <div class="intent-meta">
                <span>{file_path}:{line_number}</span>
                <span>{status}</span>
            </div>
        </div>
        """

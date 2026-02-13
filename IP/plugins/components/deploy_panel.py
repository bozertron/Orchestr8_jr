# IP/plugins/components/deploy_panel.py
"""
House a Digital Native? - LLM General Deployment Panel

This panel appears when a user clicks on a blue (broken) building in Code City.
It allows them to select which LLM "general" to deploy to fix the code.

The visceral experience:
1. Click blue building → panel emerges anchored near the click
2. See available generals (Claude, GPT-4, Gemini, etc.)
3. Pick one → building goes PURPLE (combat state)
4. General is deployed → terminal spawns or background task starts
5. When fixed → building turns GOLD (victory, dopamine)
"""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
import marimo as mo

# Maestro colors - EXACT, NO EXCEPTIONS
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_ELEVATED = "#121214"
PURPLE_COMBAT = "#9D4EDD"

# Panel CSS - emerges from void, anchored to click position
DEPLOY_PANEL_CSS = f"""
<style>
.deploy-panel-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(10, 10, 11, 0.7);
    backdrop-filter: blur(4px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: deploy-fade-in 0.2s ease-out;
}}

@keyframes deploy-fade-in {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

.deploy-panel {{
    background: {BG_ELEVATED};
    border: 1px solid {BLUE_DOMINANT};
    border-radius: 8px;
    padding: 0;
    min-width: 320px;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(31, 189, 234, 0.2);
    animation: deploy-emerge 0.3s ease-out;
}}

@keyframes deploy-emerge {{
    from {{
        opacity: 0;
        transform: scale(0.9) translateY(10px);
    }}
    to {{
        opacity: 1;
        transform: scale(1) translateY(0);
    }}
}}

.deploy-header {{
    padding: 16px 20px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.deploy-title {{
    color: {BLUE_DOMINANT};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}

.deploy-close {{
    background: transparent;
    border: none;
    color: #666;
    font-size: 18px;
    cursor: pointer;
    padding: 0;
    line-height: 1;
}}

.deploy-close:hover {{
    color: {GOLD_METALLIC};
}}

.deploy-target {{
    padding: 12px 20px;
    background: rgba(31, 189, 234, 0.05);
    border-bottom: 1px solid rgba(31, 189, 234, 0.1);
}}

.deploy-target-label {{
    color: #666;
    font-family: monospace;
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
}}

.deploy-target-path {{
    color: {BLUE_DOMINANT};
    font-family: monospace;
    font-size: 11px;
    word-break: break-all;
}}

.deploy-target-status {{
    display: inline-block;
    padding: 2px 8px;
    background: rgba(31, 189, 234, 0.15);
    border-radius: 3px;
    color: {BLUE_DOMINANT};
    font-size: 9px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 8px;
}}

.deploy-body {{
    padding: 16px 20px;
}}

.deploy-section-title {{
    color: {GOLD_DARK};
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
}}

.general-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.general-option {{
    display: flex;
    align-items: center;
    padding: 12px 16px;
    background: rgba(18, 18, 20, 0.8);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease-out;
}}

.general-option:hover {{
    border-color: {GOLD_METALLIC};
    background: rgba(212, 175, 55, 0.05);
}}

.general-option.selected {{
    border-color: {PURPLE_COMBAT};
    background: rgba(157, 78, 221, 0.1);
}}

.general-icon {{
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    margin-right: 12px;
    background: rgba(31, 189, 234, 0.1);
}}

.general-info {{
    flex: 1;
}}

.general-name {{
    color: #e8e8e8;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 2px;
}}

.general-desc {{
    color: #666;
    font-size: 10px;
}}

.general-badge {{
    padding: 3px 8px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 8px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

.general-badge.recommended {{
    background: rgba(212, 175, 55, 0.2);
    color: {GOLD_METALLIC};
}}

.general-badge.fast {{
    background: rgba(31, 189, 234, 0.2);
    color: {BLUE_DOMINANT};
}}

.general-badge.local {{
    background: rgba(157, 78, 221, 0.2);
    color: {PURPLE_COMBAT};
}}

.deploy-footer {{
    padding: 16px 20px;
    border-top: 1px solid rgba(31, 189, 234, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.deploy-mode {{
    display: flex;
    gap: 8px;
}}

.mode-btn {{
    padding: 6px 12px;
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #666;
    font-family: monospace;
    font-size: 9px;
    cursor: pointer;
    transition: all 0.15s;
}}

.mode-btn:hover {{
    border-color: {BLUE_DOMINANT};
    color: {BLUE_DOMINANT};
}}

.mode-btn.active {{
    border-color: {GOLD_METALLIC};
    color: {GOLD_METALLIC};
    background: rgba(212, 175, 55, 0.1);
}}

.deploy-btn {{
    padding: 10px 24px;
    background: rgba(157, 78, 221, 0.15);
    border: 1px solid {PURPLE_COMBAT};
    border-radius: 4px;
    color: {PURPLE_COMBAT};
    font-family: monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 0.15s;
}}

.deploy-btn:hover {{
    background: rgba(157, 78, 221, 0.25);
    box-shadow: 0 0 15px rgba(157, 78, 221, 0.3);
}}

.deploy-btn:disabled {{
    opacity: 0.5;
    cursor: not-allowed;
}}

.deploy-btn.deploying {{
    animation: deploy-pulse 1s ease-in-out infinite;
}}

@keyframes deploy-pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.6; }}
}}
</style>
"""


class DeployPanel:
    """
    House a Digital Native? - The LLM deployment panel.

    Appears when clicking a blue (broken) building in Code City.
    Lets user choose which general to deploy.
    """

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._is_visible = False
        self._target_file: Optional[str] = None
        self._target_status: str = "broken"
        self._target_errors: List[str] = []
        self._selected_general: Optional[str] = None
        self._deploy_mode: str = "terminal"  # "terminal" | "background"
        self._is_deploying = False

        # Available generals - loaded from settings
        self._generals = self._load_generals()

    def _load_generals(self) -> List[Dict[str, Any]]:
        """Load available generals from pyproject_orchestr8_settings.toml."""
        generals = [
            {
                "id": "claude-sonnet-4-20250514",
                "name": "Claude Sonnet",
                "desc": "Fast, capable - good for most tasks",
                "icon": "C",
                "badge": "recommended",
            },
            {
                "id": "claude-opus-4-20250514",
                "name": "Claude Opus",
                "desc": "Most capable - complex problems",
                "icon": "C",
                "badge": None,
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "desc": "OpenAI's flagship model",
                "icon": "G",
                "badge": None,
            },
            {
                "id": "gemini",
                "name": "Gemini Pro",
                "desc": "Google's reasoning model",
                "icon": "G",
                "badge": "fast",
            },
            {
                "id": "local",
                "name": "Local LLM",
                "desc": "Ollama / LM Studio",
                "icon": "L",
                "badge": "local",
            },
        ]

        # Try to load from settings
        try:
            import toml
            settings_file = self.project_root / "pyproject_orchestr8_settings.toml"
            if not settings_file.exists():
                settings_file = Path("pyproject_orchestr8_settings.toml")

            if settings_file.exists():
                settings = toml.load(settings_file)
                models = settings.get("tools", {}).get("communic8", {}).get("multi_llm", {}).get("default_models", [])
                if models:
                    # Use configured models as primary, keep defaults as fallback
                    configured = []
                    for model_id in models:
                        # Find matching default or create new entry
                        match = next((g for g in generals if g["id"] == model_id), None)
                        if match:
                            configured.append(match)
                        else:
                            configured.append({
                                "id": model_id,
                                "name": model_id.replace("-", " ").title(),
                                "desc": "Configured model",
                                "icon": model_id[0].upper(),
                                "badge": None,
                            })
                    if configured:
                        return configured
        except Exception:
            pass

        return generals

    def show(self, file_path: str, status: str, errors: List[str]) -> None:
        """Show the deploy panel for a target file."""
        self._is_visible = True
        self._target_file = file_path
        self._target_status = status
        self._target_errors = errors
        self._selected_general = self._generals[0]["id"] if self._generals else None
        self._is_deploying = False

    def hide(self) -> None:
        """Hide the deploy panel."""
        self._is_visible = False
        self._target_file = None
        self._is_deploying = False

    def is_visible(self) -> bool:
        """Check if panel is visible."""
        return self._is_visible

    def select_general(self, general_id: str) -> None:
        """Select a general for deployment."""
        self._selected_general = general_id

    def set_deploy_mode(self, mode: str) -> None:
        """Set deployment mode (terminal or background)."""
        if mode in ["terminal", "background"]:
            self._deploy_mode = mode

    def deploy(self) -> Dict[str, Any]:
        """
        Deploy the selected general to fix the target file.

        Returns deployment info for the caller to handle.
        """
        if not self._target_file or not self._selected_general:
            return {"success": False, "error": "No target or general selected"}

        self._is_deploying = True

        return {
            "success": True,
            "file_path": self._target_file,
            "general": self._selected_general,
            "mode": self._deploy_mode,
            "errors": self._target_errors,
        }

    def render(self) -> Any:
        """Render the deploy panel."""
        if not self._is_visible:
            return mo.md("")

        # Build generals list
        generals_html = ""
        for general in self._generals:
            is_selected = general["id"] == self._selected_general
            badge_html = ""
            if general.get("badge"):
                badge_html = f'<span class="general-badge {general["badge"]}">{general["badge"]}</span>'

            generals_html += f"""
            <div class="general-option {'selected' if is_selected else ''}"
                 data-general="{general['id']}">
                <div class="general-icon">{general['icon']}</div>
                <div class="general-info">
                    <div class="general-name">{general['name']}</div>
                    <div class="general-desc">{general['desc']}</div>
                </div>
                {badge_html}
            </div>
            """

        # Build errors display
        errors_html = ""
        if self._target_errors:
            errors_html = "<div style='margin-top: 8px; color: #666; font-size: 10px;'>"
            for err in self._target_errors[:3]:
                errors_html += f"<div>• {err}</div>"
            if len(self._target_errors) > 3:
                errors_html += f"<div>... and {len(self._target_errors) - 3} more</div>"
            errors_html += "</div>"

        panel_html = f"""
        <div class="deploy-panel-overlay">
            <div class="deploy-panel">
                <div class="deploy-header">
                    <span class="deploy-title">House a Digital Native?</span>
                    <button class="deploy-close" onclick="window.location.reload()">&times;</button>
                </div>

                <div class="deploy-target">
                    <div class="deploy-target-label">Target</div>
                    <div class="deploy-target-path">{self._target_file}</div>
                    <span class="deploy-target-status">{self._target_status}</span>
                    {errors_html}
                </div>

                <div class="deploy-body">
                    <div class="deploy-section-title">Select General</div>
                    <div class="general-list">
                        {generals_html}
                    </div>
                </div>

                <div class="deploy-footer">
                    <div class="deploy-mode">
                        <button class="mode-btn {'active' if self._deploy_mode == 'terminal' else ''}"
                                data-mode="terminal">Terminal</button>
                        <button class="mode-btn {'active' if self._deploy_mode == 'background' else ''}"
                                data-mode="background">Background</button>
                    </div>
                    <button class="deploy-btn {'deploying' if self._is_deploying else ''}"
                            {'disabled' if self._is_deploying else ''}>
                        {'DEPLOYING...' if self._is_deploying else 'DEPLOY AGENT'}
                    </button>
                </div>

                <div style="padding: 12px 20px; border-top: 1px solid rgba(31, 189, 234, 0.1); display: flex; gap: 8px; flex-wrap: wrap;">
                    <button class="mode-btn" style="flex: 1;" onclick="alert('View File: {self._target_file}')">
                        View File
                    </button>
                    <button class="mode-btn" style="flex: 1;" onclick="alert('Show Connections for: {self._target_file}')">
                        Show Connections
                    </button>
                    <button class="mode-btn" onclick="window.location.reload()">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
        """

        return mo.Html(DEPLOY_PANEL_CSS + panel_html)

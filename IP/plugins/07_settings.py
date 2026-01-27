"""
IP/plugins/07_settings.py - Settings Panel (Waves Icon)
Orchestr8 v4.0 - Complete 888 settings integration

Provides comprehensive settings UI for all agents, tools, and system configuration.
Integrates with orchestr8_settings.toml and provides live editing capabilities.
"""

from typing import Any, Dict, Optional
import toml
import os
from pathlib import Path

PLUGIN_NAME = "Settings"
PLUGIN_ORDER = 7

# ============================================================================
# SETTINGS CSS - Waves theme
# ============================================================================
SETTINGS_CSS = """
<style>
.settings-container {
    min-height: 70vh;
    background: linear-gradient(135deg, #0A0A0B 0%, #121214 100%);
    border-radius: 8px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
}

.settings-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
}

.settings-title {
    color: #D4AF37;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.05em;
}

.settings-waves {
    font-size: 24px;
    animation: waves 3s ease-in-out infinite;
}

@keyframes waves {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
}

.settings-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.settings-tab {
    padding: 8px 16px;
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #1fbdea;
    cursor: pointer;
    transition: all 150ms ease-out;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.settings-tab:hover {
    border-color: #D4AF37;
    color: #D4AF37;
    background: rgba(212, 175, 55, 0.1);
}

.settings-tab.active {
    background: rgba(212, 175, 55, 0.2);
    border-color: #D4AF37;
    color: #F4C430;
}

.settings-section {
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(31, 189, 234, 0.2);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}

.settings-section-title {
    color: #D4AF37;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.settings-section-icon {
    font-size: 16px;
}

.settings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
}

.settings-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.settings-label {
    color: #e8e8e8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.8;
}

.settings-input {
    background: rgba(31, 189, 234, 0.1);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #e8e8e8;
    padding: 8px 12px;
    font-family: inherit;
    font-size: 11px;
    transition: all 150ms ease-out;
}

.settings-input:focus {
    outline: none;
    border-color: #D4AF37;
    background: rgba(212, 175, 55, 0.1);
}

.settings-select {
    background: rgba(31, 189, 234, 0.1);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #e8e8e8;
    padding: 8px 12px;
    font-family: inherit;
    font-size: 11px;
    cursor: pointer;
}

.settings-checkbox {
    width: 16px;
    height: 16px;
    accent-color: #D4AF37;
}

.settings-button {
    background: rgba(31, 189, 234, 0.2);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: #1fbdea;
    padding: 8px 16px;
    font-family: inherit;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    cursor: pointer;
    transition: all 150ms ease-out;
}

.settings-button:hover {
    background: rgba(31, 189, 234, 0.3);
    border-color: #D4AF37;
    color: #D4AF37;
}

.settings-button.primary {
    background: rgba(212, 175, 55, 0.2);
    border-color: #D4AF37;
    color: #D4AF37;
}

.settings-button.primary:hover {
    background: rgba(212, 175, 55, 0.3);
    color: #F4C430;
}

.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 8px;
}

.status-enabled { background: #22c55e; }
.status-disabled { background: #6b7280; }
.status-warning { background: #f59e0b; }
.status-error { background: #ef4444; }

.help-text {
    color: #999;
    font-size: 10px;
    margin-top: 4px;
    font-style: italic;
}
</style>
"""


class SettingsManager:
    """Manages loading, editing, and saving orchestr8_settings.toml"""

    def __init__(self):
        self.settings_file = Path("orchestr8_settings.toml")
        self.settings = self.load_settings()

    def load_settings(self) -> Dict:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                return toml.load(self.settings_file)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.get_default_settings()
        else:
            return self.get_default_settings()

    def get_default_settings(self) -> Dict:
        """Get default empty settings structure"""
        return {
            "agents": {},
            "tools": {},
            "local_models": {},
            "integration": {},
            "ui": {},
            "privacy": {},
            "performance": {},
            "logging": {},
            "experimental": {},
            "backup": {},
        }

    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            toml.dump(self.settings, self.settings_file)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_section(self, section_name: str) -> Dict:
        """Get a specific section of settings"""
        return self.settings.get(section_name, {})

    def set_value(self, path: str, value: Any) -> None:
        """Set a specific setting value using dotted path notation.

        Args:
            path: Dotted path like "agents.director.enabled"
            value: Value to set
        """
        parts = path.split(".")
        if len(parts) < 2:
            return

        # Navigate to the parent dict, creating nested dicts as needed
        current = self.settings
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the final value
        current[parts[-1]] = value

    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """Get a specific setting value"""
        return self.settings.get(section, {}).get(key, default)


def render(STATE_MANAGERS: Dict) -> Any:
    """
    Render the Settings panel with waves icon

    Provides comprehensive configuration for all 888 tools and agents.
    """
    import marimo as mo

    # Get global state
    get_root, _ = STATE_MANAGERS["root"]

    # Initialize settings manager
    settings_mgr = SettingsManager()

    # Get available models from settings
    def get_available_models() -> list:
        """Get available models from settings."""
        multi_llm = settings_mgr.get_section("tools").get("communic8", {}).get("multi_llm", {})
        models = multi_llm.get("default_models", [])
        if models:
            return models
        # Fallback - these should be configured in settings
        return ["claude", "gpt-4", "gemini", "local"]

    available_models = get_available_models()

    # Local state for UI
    get_active_tab, set_active_tab = mo.state("agents")
    get_modified, set_modified = mo.state(False)

    def update_setting(path: str, value: Any) -> None:
        """Update a setting value and mark as modified."""
        settings_mgr.set_value(path, value)
        set_modified(True)

    # Tab definitions
    tabs = {
        "agents": ("Agents", "Configure AI agents (Director, Professor, Doctor)"),
        "tools": ("Tools", "Configure 888 tools (actu8, senses, cre8, etc.)"),
        "models": ("Models", "Configure local AI models"),
        "integration": ("Integration", "External application settings"),
        "ui": ("UI", "User interface preferences"),
        "privacy": ("Privacy", "Privacy and security settings"),
        "performance": ("Performance", "System performance tuning"),
        "experimental": ("Experimental", "Cutting-edge features"),
        "backup": ("Backup", "Backup and recovery"),
    }

    def tab_button(tab_key: str, label: str):
        return mo.ui.button(
            label=label,
            on_change=lambda _: set_active_tab(tab_key),
            style={
                "background": "rgba(212, 175, 55, 0.2)"
                if get_active_tab() == tab_key
                else "transparent"
            },
        )

    def render_agents_tab():
        """Render agents configuration"""
        agents_config = settings_mgr.get_section("agents")

        return mo.vstack(
            [
                mo.md("### Director - The General"),
                mo.hstack(
                    [
                        mo.ui.checkbox(
                            label="Enable Director",
                            value=agents_config.get("director", {}).get(
                                "enabled", False
                            ),
                            on_change=lambda v: update_setting(
                                "agents.director.enabled", v
                            ),
                        ),
                        mo.ui.text(
                            label="Check Interval (seconds)",
                            value=str(
                                agents_config.get("director", {}).get(
                                    "check_interval_seconds", 30
                                )
                            ),
                            on_change=lambda v: update_setting(
                                "agents.director.check_interval_seconds", int(v) if str(v).isdigit() else 30
                            ),
                        ),
                    ]
                ),
                mo.md("### Professor - Breakthrough Analyzer"),
                mo.hstack(
                    [
                        mo.ui.checkbox(
                            label="Enable Professor",
                            value=agents_config.get("professor", {}).get(
                                "enabled", False
                            ),
                            on_change=lambda v: update_setting(
                                "agents.professor.enabled", v
                            ),
                        ),
                        mo.ui.text(
                            label="Analysis Interval (hours)",
                            value=str(
                                agents_config.get("professor", {}).get(
                                    "analysis_interval_hours", 24
                                )
                            ),
                            on_change=lambda v: update_setting(
                                "agents.professor.analysis_interval_hours", int(v) if str(v).isdigit() else 24
                            ),
                        ),
                    ]
                ),
                mo.md("### Doctor - Deep Debugging"),
                mo.hstack(
                    [
                        mo.ui.checkbox(
                            label="Enable Doctor",
                            value=agents_config.get("doctor", {}).get("enabled", False),
                            on_change=lambda v: update_setting(
                                "agents.doctor.enabled", v
                            ),
                        ),
                        mo.ui.dropdown(
                            options=available_models,
                            value=agents_config.get("doctor", {}).get(
                                "model", available_models[0] if available_models else "claude"
                            ),
                            label="Model",
                            on_change=lambda v: update_setting(
                                "agents.doctor.model", v
                            ),
                        ),
                    ]
                ),
            ]
        )

    def render_tools_tab():
        """Render tools configuration"""
        tools_config = settings_mgr.get_section("tools")

        return mo.vstack(
            [
                mo.md("### actu8 - Document Generation"),
                mo.hstack(
                    [
                        mo.ui.text(
                            label="Default Mode",
                            value=tools_config.get("actu8", {}).get(
                                "default_mode", "choice"
                            ),
                            on_change=lambda v: update_setting(
                                "tools.actu8.default_mode", v
                            ),
                        ),
                        mo.ui.checkbox(
                            label="Auto Save",
                            value=tools_config.get("actu8", {}).get("auto_save", True),
                            on_change=lambda v: update_setting(
                                "tools.actu8.auto_save", v
                            ),
                        ),
                    ]
                ),
                mo.md("### senses - Multimodal Input"),
                mo.hstack(
                    [
                        mo.ui.checkbox(
                            label="Enable Senses",
                            value=tools_config.get("senses", {}).get("enabled", False),
                            on_change=lambda v: update_setting(
                                "tools.senses.enabled", v
                            ),
                        ),
                        mo.ui.checkbox(
                            label="Privacy Mode",
                            value=tools_config.get("senses", {}).get(
                                "privacy_indicator", True
                            ),
                            on_change=lambda v: update_setting(
                                "tools.senses.privacy_indicator", v
                            ),
                        ),
                    ]
                ),
                mo.md("### cre8 - Creative Suite"),
                mo.hstack(
                    [
                        mo.ui.text(
                            label="Image Editor",
                            value=tools_config.get("cre8", {}).get(
                                "image_editor", "gimp"
                            ),
                            on_change=lambda v: update_setting(
                                "tools.cre8.image_editor", v
                            ),
                        ),
                        mo.ui.text(
                            label="Audio Editor",
                            value=tools_config.get("cre8", {}).get(
                                "audio_editor", "audacity"
                            ),
                            on_change=lambda v: update_setting(
                                "tools.cre8.audio_editor", v
                            ),
                        ),
                    ]
                ),
            ]
        )

    def render_ui_tab():
        """Render UI configuration"""
        ui_config = settings_mgr.get_section("ui")

        return mo.vstack(
            [
                mo.md("### General Appearance"),
                mo.hstack(
                    [
                        mo.ui.text(
                            label="Theme",
                            value=ui_config.get("general", {}).get("theme", "maestro"),
                            on_change=lambda v: update_setting(
                                "ui.general.theme", v
                            ),
                        ),
                        mo.ui.text(
                            label="Font Size",
                            value=str(
                                ui_config.get("general", {}).get("font_size", 12)
                            ),
                            on_change=lambda v: update_setting(
                                "ui.general.font_size", int(v) if str(v).isdigit() else 12
                            ),
                        ),
                    ]
                ),
                mo.md("### Maestro Settings"),
                mo.hstack(
                    [
                        mo.ui.checkbox(
                            label="Show Agent Status",
                            value=ui_config.get("maestro", {}).get(
                                "show_agent_status", True
                            ),
                            on_change=lambda v: update_setting(
                                "ui.maestro.show_agent_status", v
                            ),
                        ),
                        mo.ui.checkbox(
                            label="Show System Health",
                            value=ui_config.get("maestro", {}).get(
                                "show_system_health", True
                            ),
                            on_change=lambda v: update_setting(
                                "ui.maestro.show_system_health", v
                            ),
                        ),
                    ]
                ),
            ]
        )

    def save_settings():
        """Save current settings"""
        if settings_mgr.save_settings():
            set_modified(False)
            return mo.md("Settings saved successfully!")
        else:
            return mo.md("Error saving settings!")

    def render_content():
        """Render content based on active tab"""
        active_tab = get_active_tab()

        if active_tab == "agents":
            return render_agents_tab()
        elif active_tab == "tools":
            return render_tools_tab()
        elif active_tab == "ui":
            return render_ui_tab()
        else:
            return mo.md(
                f"### {tabs.get(active_tab, ['', ''])[0]}\n\n{tabs.get(active_tab, ['', ''])[1]}\n\n*Configuration coming soon...*"
            )

    # Build tabs
    tab_buttons = []
    for tab_key, (label, _) in tabs.items():
        is_active = get_active_tab() == tab_key
        button_class = "settings-tab active" if is_active else "settings-tab"
        tab_buttons.append(
            mo.ui.button(
                label=label,
                on_change=lambda v, tk=tab_key: set_active_tab(tk),
                style={
                    "background": "rgba(212, 175, 55, 0.2)"
                    if is_active
                    else "transparent"
                },
            )
        )

    return mo.vstack(
        [
            mo.Html(SETTINGS_CSS),
            mo.md("## Settings"),
            mo.md("*Configure Orchestr8 agents, tools, and system settings*"),
            mo.md("---"),
            # Header with waves
            mo.hstack(
                [
                    mo.md("### Configuration Center"),
                    mo.md("~~~"),  # Simple waves
                ],
                justify="space-between",
            ),
            # Tabs
            mo.hstack(tab_buttons, gap="0.5rem"),
            mo.md("---"),
            # Content area
            render_content(),
            mo.md("---"),
            # Save button
            mo.hstack(
                [
                    mo.ui.button(
                        label="Save Settings",
                        on_change=lambda _: save_settings(),
                        style={"background": "rgba(212, 175, 55, 0.2)"},
                    ),
                    mo.md(f"*Modified: {get_modified()}*"),
                ]
            ),
        ]
    )

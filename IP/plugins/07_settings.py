"""
IP/plugins/07_settings.py - Settings Panel (Void Design System)
Orchestr8 v4.0 - Complete 888 settings integration

Provides comprehensive settings UI for all agents, tools, and system configuration.
Integrates with pyproject_orchestr8_settings.toml and provides live editing capabilities.

Void Design System: Emergence-only animations, exact color tokens, diamond dismiss.

CSE Architecture: Single-pass wiring with SettingsService for typesafe access.
"""

from typing import Any, Dict, Optional, List, Callable
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
import toml
import os
from pathlib import Path
from IP.styles.font_profiles import (
    available_font_profile_labels,
    resolve_font_profile_name,
)
from IP.features.maestro import load_orchestr8_css

PLUGIN_NAME = "Settings"
PLUGIN_ORDER = 7


# ============================================================================
# Pydantic Models for Settings Validation
# ============================================================================


class AgentDirectorConfig(BaseModel):
    """Director (The General) agent configuration"""

    enabled: bool = False
    check_interval_seconds: int = Field(default=30, ge=1, le=3600)
    stuck_threshold_minutes: int = Field(default=5, ge=1, le=60)
    max_concurrent_generals: int = Field(default=10, ge=1, le=100)
    escalation_to_doctor: bool = True


class AgentProfessorConfig(BaseModel):
    """Professor (Breakthrough Analyzer) agent configuration"""

    enabled: bool = False
    analysis_interval_hours: int = Field(default=24, ge=1, le=168)
    breakthrough_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    report_to_emperor: bool = True
    learning_rate: float = Field(default=0.1, ge=0.0, le=1.0)


class AgentDoctorConfig(BaseModel):
    """Doctor (Deep Debugging) agent configuration"""

    enabled: bool = False
    model: str = Field(default="claude")
    max_tokens: int = Field(default=100000, ge=1000, le=1000000)
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    deep_analysis_enabled: bool = True
    escalation_only: bool = False


class AgentConfig(BaseModel):
    """Agents section configuration"""

    director: AgentDirectorConfig = Field(default_factory=AgentDirectorConfig)
    professor: AgentProfessorConfig = Field(default_factory=AgentProfessorConfig)
    doctor: AgentDoctorConfig = Field(default_factory=AgentDoctorConfig)


class ToolActu8Config(BaseModel):
    """actu8 - Document Generation tool configuration"""

    default_mode: str = Field(default="choice")
    document_model: str = Field(default="[local_doc_model]")
    fallback_app: str = Field(default="onlyoffice")
    barbara_model: str = Field(default="[APIlikethis]")
    auto_save: bool = True
    backup_enabled: bool = True


class ToolSensesConfig(BaseModel):
    """senses - Multimodal Input tool configuration"""

    enabled: bool = False
    assigned_to: str = Field(default="maestro")
    gesture_enabled: bool = True
    speech_enabled: bool = True
    spell_manager_enabled: bool = True
    privacy_indicator: bool = True
    capture_warning: bool = True


class ToolCre8ModelsConfig(BaseModel):
    """cre8 AI models sub-configuration"""

    image_model: str = Field(default="[local_image_model]")
    audio_model: str = Field(default="[local_audio_model]")
    video_model: str = Field(default="[local_video_model]")
    three_d_model: str = Field(default="[local_3d_model]")
    auto_enhance: bool = True
    batch_processing: bool = True


class ToolCre8Config(BaseModel):
    """cre8 - Creative Suite configuration"""

    image_editor: str = Field(default="gimp")
    audio_editor: str = Field(default="audacity")
    video_editor: str = Field(default="blender")
    three_d_editor: str = Field(default="blender")
    models: ToolCre8ModelsConfig = Field(default_factory=ToolCre8ModelsConfig)


class ToolCommunic8MultiLLMConfig(BaseModel):
    """communic8 multi-LLM sub-configuration"""

    enabled: bool = True
    default_models: List[str] = Field(
        default_factory=lambda: ["claude", "gpt-4", "gemini"]
    )
    consolidation_mode: str = Field(default="opinions")
    parallel_queries: bool = True
    response_timeout_seconds: int = Field(default=60, ge=10, le=300)


class ToolCommunic8Config(BaseModel):
    """communic8 - ALL Communications configuration"""

    default_mode: str = Field(default="choice")
    email_client: str = Field(default="thunderbird")
    p2p_enabled: bool = True
    calendar_integration: bool = True
    contacts_integration: bool = True
    multi_llm: ToolCommunic8MultiLLMConfig = Field(
        default_factory=ToolCommunic8MultiLLMConfig
    )


class ToolInnov8Config(BaseModel):
    """innov8 - The Ultimate Looper configuration"""

    enabled: bool = True
    experiment_timeout_hours: int = Field(default=4, ge=1, le=48)
    auto_loop: bool = True
    animation_testing: bool = True
    hypothesis_validation: bool = True
    performance_benchmarking: bool = True


class ToolConfig(BaseModel):
    """Tools section configuration"""

    actu8: ToolActu8Config = Field(default_factory=ToolActu8Config)
    senses: ToolSensesConfig = Field(default_factory=ToolSensesConfig)
    cre8: ToolCre8Config = Field(default_factory=ToolCre8Config)
    communic8: ToolCommunic8Config = Field(default_factory=ToolCommunic8Config)
    innov8: ToolInnov8Config = Field(default_factory=ToolInnov8Config)


class LocalModelsConfig(BaseModel):
    """Local models configuration"""

    document: Dict[str, Any] = Field(default_factory=dict)
    image: Dict[str, Any] = Field(default_factory=dict)
    audio: Dict[str, Any] = Field(default_factory=dict)
    video: Dict[str, Any] = Field(default_factory=dict)
    embedding: Dict[str, Any] = Field(default_factory=dict)


class IntegrationConfig(BaseModel):
    """Integration section configuration"""

    onlyoffice: Dict[str, Any] = Field(default_factory=dict)
    thunderbird: Dict[str, Any] = Field(default_factory=dict)
    audacity: Dict[str, Any] = Field(default_factory=dict)
    gimp: Dict[str, Any] = Field(default_factory=dict)
    blender: Dict[str, Any] = Field(default_factory=dict)


class UIGeneralConfig(BaseModel):
    """UI general settings"""

    theme: str = Field(default="maestro")
    font_profile: str = Field(default="regal_deco")
    animation_speed: str = Field(default="normal")
    font_size: int = Field(default=12, ge=8, le=24)
    compact_mode: bool = False


class UIMaestroConfig(BaseModel):
    """UI maestro panel settings"""

    show_senses_indicator: bool = True
    show_agent_status: bool = True
    show_system_health: bool = True
    auto_hide_panels: bool = False
    panel_animation_speed: int = Field(default=300, ge=100, le=1000)


class UINotificationsConfig(BaseModel):
    """UI notifications settings"""

    agent_alerts: bool = True
    system_alerts: bool = True
    tool_alerts: bool = True
    breakthrough_alerts: bool = True
    escalation_alerts: bool = True


class UIConfig(BaseModel):
    """UI section configuration"""

    general: UIGeneralConfig = Field(default_factory=UIGeneralConfig)
    maestro: UIMaestroConfig = Field(default_factory=UIMaestroConfig)
    notifications: UINotificationsConfig = Field(default_factory=UINotificationsConfig)


class LoggingGeneralConfig(BaseModel):
    """Logging general settings"""

    level: str = Field(default="INFO")
    file_path: str = Field(default=".orchestr8/logs/system.log")
    max_file_size_mb: int = Field(default=100, ge=1, le=1000)
    backup_count: int = Field(default=5, ge=1, le=50)


class LoggingAgentsConfig(BaseModel):
    """Logging agents settings"""

    director_logging: bool = True
    professor_logging: bool = True
    doctor_logging: bool = True
    escalation_logging: bool = True


class LoggingToolsConfig(BaseModel):
    """Logging tools settings"""

    tool_startup_logging: bool = True
    integration_logging: bool = True
    error_logging: bool = True
    performance_logging: bool = False


class LoggingConfig(BaseModel):
    """Logging section configuration"""

    general: LoggingGeneralConfig = Field(default_factory=LoggingGeneralConfig)
    agents: LoggingAgentsConfig = Field(default_factory=LoggingAgentsConfig)
    tools: LoggingToolsConfig = Field(default_factory=LoggingToolsConfig)


class PrivacySensesConfig(BaseModel):
    """Privacy senses settings"""

    require_explicit_consent: bool = True
    show_capture_indicator: bool = True
    retain_recordings: bool = False
    encryption_enabled: bool = True
    data_retention_days: int = Field(default=0, ge=0)


class PrivacyCommunic8Config(BaseModel):
    """Privacy communic8 settings"""

    encrypt_p2p: bool = True
    log_messages: bool = False
    share_contacts: bool = False
    anonymize_queries: bool = True


class PrivacyConfig(BaseModel):
    """Privacy section configuration"""

    senses: PrivacySensesConfig = Field(default_factory=PrivacySensesConfig)
    communic8: PrivacyCommunic8Config = Field(default_factory=PrivacyCommunic8Config)


class PerformanceGeneralConfig(BaseModel):
    """Performance general settings"""

    max_concurrent_operations: int = Field(default=5, ge=1, le=50)
    memory_limit_mb: int = Field(default=8192, ge=512, le=65536)
    cpu_limit_percent: int = Field(default=80, ge=10, le=100)
    auto_cleanup: bool = True


class PerformanceAIModelsConfig(BaseModel):
    """Performance AI models settings"""

    model_cache_size_mb: int = Field(default=2048, ge=256, le=16384)
    preload_models: List[str] = Field(default_factory=lambda: ["document", "embedding"])
    batch_processing: bool = True
    gpu_utilization_target: float = Field(default=0.8, ge=0.0, le=1.0)


class PerformanceConfig(BaseModel):
    """Performance section configuration"""

    general: PerformanceGeneralConfig = Field(default_factory=PerformanceGeneralConfig)
    ai_models: PerformanceAIModelsConfig = Field(
        default_factory=PerformanceAIModelsConfig
    )


class BackupGeneralConfig(BaseModel):
    """Backup general settings"""

    enabled: bool = True
    interval_hours: int = Field(default=6, ge=1, le=168)
    compression: bool = True
    encryption: bool = True
    retention_days: int = Field(default=30, ge=1, le=365)


class BackupLocationsConfig(BaseModel):
    """Backup locations settings"""

    primary_backup: str = Field(default="~/.orchestr8/backups/")
    secondary_backup: str = Field(default="[external_drive_path]/orchestr8_backups/")
    cloud_backup: bool = False


class BackupConfig(BaseModel):
    """Backup section configuration"""

    general: BackupGeneralConfig = Field(default_factory=BackupGeneralConfig)
    locations: BackupLocationsConfig = Field(default_factory=BackupLocationsConfig)


class ExperimentalInnov8Config(BaseModel):
    """Experimental innov8 settings"""

    auto_experiments: bool = True
    hypothesis_testing: bool = True
    animation_prototyping: bool = True
    performance_benchmarking: bool = True
    report_findings: bool = True


class ExperimentalAIConfig(BaseModel):
    """Experimental AI settings"""

    multi_model_comparison: bool = True
    automatic_model_selection: bool = True
    context_optimization: bool = True
    token_efficiency_mode: bool = False


class ExperimentalConfig(BaseModel):
    """Experimental section configuration"""

    innov8: ExperimentalInnov8Config = Field(default_factory=ExperimentalInnov8Config)
    ai: ExperimentalAIConfig = Field(default_factory=ExperimentalAIConfig)


class Orchestr8Settings(BaseModel):
    """Root Pydantic model for all Orchestr8 settings"""

    agents: AgentConfig = Field(default_factory=AgentConfig)
    tools: ToolConfig = Field(default_factory=ToolConfig)
    local_models: LocalModelsConfig = Field(default_factory=LocalModelsConfig)
    integration: IntegrationConfig = Field(default_factory=IntegrationConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    privacy: PrivacyConfig = Field(default_factory=PrivacyConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    experimental: ExperimentalConfig = Field(default_factory=ExperimentalConfig)
    backup: BackupConfig = Field(default_factory=BackupConfig)

    @model_validator(mode="before")
    @classmethod
    def convert_legacy_format(cls, data):
        """Convert legacy dict format to Pydantic model structure"""
        if not isinstance(data, dict):
            return data

        # Handle nested structures that came from TOML
        converted = {}
        for key, value in data.items():
            if isinstance(value, dict):
                # Flatten single-key dicts that represent nested sections
                if key in (
                    "agents",
                    "tools",
                    "ui",
                    "logging",
                    "privacy",
                    "performance",
                    "experimental",
                    "backup",
                ):
                    converted[key] = value
                else:
                    converted[key] = value
            else:
                converted[key] = value
        return converted

    def to_toml_dict(self) -> Dict[str, Any]:
        """Convert Pydantic model back to TOML-serializable dict"""
        return self.model_dump(mode="json", exclude_none=True)


# ============================================================================
# Settings Manager with Pydantic Validation
# ============================================================================


class SettingsManager:
    """Manages loading, editing, and saving pyproject_orchestr8_settings.toml with Pydantic validation"""

    def __init__(self):
        self.settings_file = Path("pyproject_orchestr8_settings.toml")
        self._pydantic_model: Optional[Orchestr8Settings] = None
        self._validation_errors: List[str] = []
        self.settings = self.load_settings()

    def load_settings(self) -> Dict:
        """Load settings from file with Pydantic validation"""
        raw_data: Dict = {}
        if self.settings_file.exists():
            try:
                raw_data = toml.load(self.settings_file)
            except Exception as e:
                print(f"Error loading settings: {e}")
                self._validation_errors.append(f"Failed to parse TOML: {e}")
                raw_data = self.get_default_settings()

        # Validate with Pydantic
        try:
            self._pydantic_model = Orchestr8Settings.model_validate(raw_data)
            self._validation_errors = []
            # Return validated data (in case defaults were filled)
            return self._pydantic_model.to_toml_dict()
        except Exception as e:
            print(f"Pydantic validation error: {e}")
            self._validation_errors.append(f"Validation error: {e}")
            # Try to continue with raw data but warn
            return raw_data

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

    def get_validation_errors(self) -> List[str]:
        """Return any validation errors from last load"""
        return self._validation_errors

    def validate_value(self, path: str, value: Any) -> tuple[bool, str]:
        """Validate a single setting value against its Pydantic field.

        Returns:
            (is_valid, error_message)
        """
        if self._pydantic_model is None:
            return True, ""  # No validation if model not loaded

        parts = path.split(".")
        if len(parts) < 2:
            return True, ""

        try:
            # Get the section and field
            section = parts[0]
            field_name = parts[-1]

            # Validate based on known fields (basic type checks)
            if section == "agents":
                if field_name in ("enabled", "escalation_to_doctor"):
                    if not isinstance(value, bool):
                        return False, f"{field_name} must be a boolean"
                elif field_name in (
                    "check_interval_seconds",
                    "stuck_threshold_minutes",
                    "max_concurrent_generals",
                    "analysis_interval_hours",
                ):
                    if not isinstance(value, int):
                        return False, f"{field_name} must be an integer"
                    if value < 1:
                        return False, f"{field_name} must be positive"
                elif field_name == "model":
                    if not isinstance(value, str):
                        return False, "model must be a string"
                elif field_name == "temperature":
                    if not isinstance(value, (int, float)):
                        return False, "temperature must be a number"
                    if not 0 <= value <= 2:
                        return False, "temperature must be between 0 and 2"
                elif field_name == "max_tokens":
                    if not isinstance(value, int):
                        return False, "max_tokens must be an integer"
            elif section == "ui":
                if field_name == "font_size":
                    if not isinstance(value, int):
                        return False, "font_size must be an integer"
                    if not 8 <= value <= 24:
                        return False, "font_size must be between 8 and 24"
                elif field_name == "theme":
                    if value not in ("maestro", "light", "dark"):
                        return False, "theme must be 'maestro', 'light', or 'dark'"
                # Note: font_profile validation deferred to runtime (needs font_profile_options)

            return True, ""
        except Exception as e:
            return False, str(e)

    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            # Re-validate before saving
            if self._pydantic_model:
                validated = self._pydantic_model.model_validate(self.settings)
                toml_dict = validated.to_toml_dict()
            else:
                toml_dict = self.settings

            # Convert Path to string for toml
            with open(self.settings_file, "w") as f:
                toml.dump(toml_dict, f)
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


# ============================================================================
# SettingsService - CSE Single-Pass Wiring
# ============================================================================


class SettingsService:
    """
    Typesafe source of truth for Orchestr8 settings.

    Combines logic + persistence + UI in single-pass wiring per PHREAK_CSE_RESEARCH_REPORT.md.
    Provides real-time sync (<50ms target), audit trail, and validation feedback.
    """

    def __init__(self):
        self._manager = SettingsManager()
        self._subscribers: List[Callable[[Dict], None]] = []
        self._audit_trail: List[Dict] = []
        self._last_sync_time: Optional[datetime] = None

    # =========================================================================
    # Typesafe Getters
    # =========================================================================

    def get_font_profile(self) -> str:
        """Get current font profile."""
        return (
            self._manager.settings.get("ui", {})
            .get("general", {})
            .get("font_profile", "phreak_nexus")
        )

    def get_animation_enabled(self) -> bool:
        """Check if emergence animations are enabled."""
        return (
            self._manager.settings.get("ui", {})
            .get("general", {})
            .get("animation_enabled", True)
        )

    def get_theme(self) -> str:
        """Get current UI theme."""
        return (
            self._manager.settings.get("ui", {})
            .get("general", {})
            .get("theme", "maestro")
        )

    def get_font_size(self) -> int:
        """Get current font size."""
        return (
            self._manager.settings.get("ui", {}).get("general", {}).get("font_size", 12)
        )

    def get_code_city_max_bytes(self) -> int:
        """Get Code City maximum payload size."""
        return (
            self._manager.settings.get("ui", {})
            .get("code_city", {})
            .get("max_bytes", 9000000)
        )

    def get_code_city_stream_bps(self) -> int:
        """Get Code City streaming rate (bytes per second)."""
        return (
            self._manager.settings.get("ui", {})
            .get("code_city", {})
            .get("stream_bps", 5000000)
        )

    def get_agent_enabled(self, agent_name: str) -> bool:
        """Check if an agent is enabled."""
        return (
            self._manager.settings.get("agents", {})
            .get(agent_name, {})
            .get("enabled", False)
        )

    def get_tool_enabled(self, tool_name: str) -> bool:
        """Check if a tool is enabled."""
        return (
            self._manager.settings.get("tools", {})
            .get(tool_name, {})
            .get("enabled", True)
        )

    # =========================================================================
    # Typesafe Setters with Immediate Sync
    # =========================================================================

    def set_font_profile(self, profile: str) -> None:
        """Set font profile with immediate UI sync."""
        self._set_nested(["ui", "general", "font_profile"], profile)
        self._notify_subscribers()

    def set_theme(self, theme: str) -> None:
        """Set UI theme with immediate sync."""
        self._set_nested(["ui", "general", "theme"], theme)
        self._notify_subscribers()

    def set_font_size(self, size: int) -> None:
        """Set font size with immediate sync."""
        self._set_nested(["ui", "general", "font_size"], size)
        self._notify_subscribers()

    def set_code_city_max_bytes(self, max_bytes: int) -> None:
        """Set Code City max bytes with immediate sync."""
        self._set_nested(["ui", "code_city", "max_bytes"], max_bytes)
        self._notify_subscribers()

    def set_code_city_stream_bps(self, bps: int) -> None:
        """Set Code City stream rate with immediate sync."""
        self._set_nested(["ui", "code_city", "stream_bps"], bps)
        self._notify_subscribers()

    def set_agent_enabled(self, agent_name: str, enabled: bool) -> None:
        """Set agent enabled state with immediate sync."""
        self._set_nested(["agents", agent_name, "enabled"], enabled)
        self._notify_subscribers()

    def set_tool_enabled(self, tool_name: str, enabled: bool) -> None:
        """Set tool enabled state with immediate sync."""
        self._set_nested(["tools", tool_name, "enabled"], enabled)
        self._notify_subscribers()

    def set_value(self, path: str, value: Any) -> None:
        """
        Set a specific setting using dotted path notation.

        Args:
            path: Dotted path like "agents.director.enabled"
            value: Value to set
        """
        self._record_action(path, value)
        self._manager.set_value(path, value)
        self._notify_subscribers()
        self._last_sync_time = datetime.now()

    # =========================================================================
    # Real-time Sync (<50ms target)
    # =========================================================================

    def subscribe(self, callback: Callable[[Dict], None]) -> None:
        """Subscribe to settings changes. Callback receives full settings dict."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Dict], None]) -> None:
        """Remove a subscriber."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def _notify_subscribers(self) -> None:
        """Notify all subscribers of change. Target: <50ms."""
        for callback in self._subscribers:
            try:
                callback(self._manager.settings)
            except Exception as e:
                print(f"SettingsService subscriber error: {e}")

    def get_last_sync_time(self) -> Optional[datetime]:
        """Get timestamp of last sync operation."""
        return self._last_sync_time

    # =========================================================================
    # Persistence
    # =========================================================================

    def save(self) -> bool:
        """Persist settings to TOML."""
        success = self._manager.save_settings()
        if success:
            self._record_action("_system", "save", note="Settings persisted to TOML")
        return success

    def reload(self) -> None:
        """Reload settings from TOML."""
        self._manager.load_settings()
        self._notify_subscribers()
        self._record_action("_system", "reload", note="Settings reloaded from TOML")

    def get_raw_settings(self) -> Dict:
        """Get raw settings dict (for advanced access)."""
        return self._manager.settings

    # =========================================================================
    # Quantum Commit - Audit Trail
    # =========================================================================

    def quantum_commit(self, key: str, value: Any) -> Dict:
        """
        Commit a setting with audit trail.

        Returns: {key, value, timestamp, status}
        """
        # Record action for audit
        self._record_action(key, value)

        # Apply immediately
        self.set_value(key, value)

        return {
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "status": "committed",
        }

    def _record_action(self, key: str, value: Any, note: str = "") -> None:
        """Record action for audit trail."""
        # Get old value for comparison
        old_value = self._get_nested_value(key)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "key": key,
            "old_value": old_value,
            "new_value": value,
            "source": "settings_service",
            "note": note,
        }
        self._audit_trail.append(entry)

        # Keep only last 1000 entries to prevent memory bloat
        if len(self._audit_trail) > 1000:
            self._audit_trail = self._audit_trail[-1000:]

    def _get_nested_value(self, path: str) -> Any:
        """Get value at dotted path, returns sentinel if not found."""
        parts = path.split(".")
        current = self._manager.settings
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def _set_nested(self, parts: List[str], value: Any) -> None:
        """Set nested value from parts list."""
        self._manager.set_value(".".join(parts), value)

    def get_audit_trail(self) -> List[Dict]:
        """Get audit trail of all setting changes."""
        return self._audit_trail.copy()

    # =========================================================================
    # Validation with Glitch Feedback
    # =========================================================================

    def validate_setting(self, key: str, value: Any) -> tuple[bool, str]:
        """
        Validate a setting value.

        Returns: (is_valid, error_message)
        - Invalid: triggers teal/glitch effect
        - Valid: triggers gold glow
        """
        return self._manager.validate_value(key, value)

    def validate_and_commit(self, key: str, value: Any) -> Dict:
        """
        Validate a setting and commit if valid.

        Returns validation result plus commit status.
        """
        is_valid, error_msg = self.validate_setting(key, value)

        if is_valid:
            result = self.quantum_commit(key, value)
            result["validation"] = "valid"
            result["feedback"] = "gold"  # Gold glow for valid
        else:
            result = {
                "key": key,
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "status": "rejected",
                "validation": "invalid",
                "error": error_msg,
                "feedback": "glitch",  # Teal glitch for invalid
            }

        return result


# Global SettingsService instance for CSE single-pass wiring
_settings_service: Optional[SettingsService] = None


def get_settings_service() -> SettingsService:
    """Get or create the global SettingsService instance."""
    global _settings_service
    if _settings_service is None:
        _settings_service = SettingsService()
    return _settings_service


def render(STATE_MANAGERS: Dict) -> Any:
    """
    Render the Settings panel with Void Design System

    Provides comprehensive configuration for all 888 tools and agents.
    Uses SettingsService for CSE single-pass wiring with real-time sync.
    """
    import marimo as mo

    # Get global state
    get_root, _ = STATE_MANAGERS["root"]

    # Initialize settings service (CSE single-pass wiring)
    settings_service = get_settings_service()
    settings_mgr = settings_service._manager

    # Get validation errors from load
    validation_errors = settings_mgr.get_validation_errors()

    # Get available models from settings
    def get_available_models() -> list[str]:
        """Get available models from settings."""
        multi_llm = (
            settings_mgr.get_section("tools").get("communic8", {}).get("multi_llm", {})
        )
        models = multi_llm.get("default_models", [])
        if models:
            clean_models = [
                str(model).strip() for model in models if str(model).strip()
            ]
            if clean_models:
                return clean_models
        # Fallback - these should be configured in settings
        return ["claude", "gpt-4", "gemini", "local"]

    available_models = get_available_models()
    font_profile_labels = available_font_profile_labels()
    font_profile_options = list(font_profile_labels.keys())

    # Keep renamed model values from breaking dropdown rendering.
    LEGACY_MODEL_ALIASES = {
        "claude-opus": "claude",
        "claude-sonnet": "claude",
        "claude-3-opus": "claude",
        "claude-3.5-sonnet": "claude",
        "gpt-4o": "gpt-4",
        "gpt-4.1": "gpt-4",
        "gemini-pro": "gemini",
        "gemini-1.5-pro": "gemini",
    }

    def resolve_model_option(value: Any) -> str:
        """Normalize persisted model value to a valid dropdown option."""
        default_model = available_models[0] if available_models else "claude"
        if value in available_models:
            return value
        if isinstance(value, str):
            mapped = LEGACY_MODEL_ALIASES.get(value.strip().lower())
            if mapped and mapped in available_models:
                return mapped
        return default_model

    # Local state for UI
    get_active_tab, set_active_tab = mo.state("agents")
    get_modified, set_modified = mo.state(False)

    # Real-time preview state for font profile
    get_preview_font, set_preview_font = mo.state(None)

    def apply_font_preview(font_profile: str) -> None:
        """Apply font profile change immediately for real-time preview.

        This triggers the CSS injection to update fonts without saving.
        Uses SettingsService for immediate sync (<50ms target).
        """
        resolved = resolve_font_profile_name(font_profile)
        # Use SettingsService for immediate sync
        settings_service.set_font_profile(resolved)
        set_preview_font(resolved)
        set_modified(True)

    def update_setting(path: str, value: Any) -> None:
        """Update a setting value and mark as modified.

        Uses SettingsService for typesafe access and real-time sync.
        """
        # Special handling for font profile - apply preview immediately
        if path == "ui.general.font_profile":
            apply_font_preview(value)
            return

        # Special handling for font size - validate range
        if path == "ui.general.font_size":
            try:
                size = int(value)
                if not (8 <= size <= 24):
                    print(f"Warning: font_size {size} out of range (8-24), clamping")
                    size = max(8, min(24, size))
                value = size
            except (ValueError, TypeError):
                value = 12

        # Validate other numeric values
        if "check_interval" in path or "threshold" in path or "max_concurrent" in path:
            try:
                value = int(value)
                if value < 1:
                    value = 1
            except (ValueError, TypeError):
                pass

        # Use SettingsService for typesafe set with audit trail
        settings_service.set_value(path, value)
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
        # Note: style param removed (not supported in marimo 0.19.6)
        # Active state indicated by label prefix instead
        is_active = get_active_tab() == tab_key
        display_label = f"[{label}]" if is_active else label
        return mo.ui.button(
            label=display_label,
            on_click=lambda _: set_active_tab(tab_key),
        )

    def render_agents_tab():
        """Render agents configuration"""
        agents_config = settings_mgr.get_section("agents")
        doctor_model_value = resolve_model_option(
            agents_config.get("doctor", {}).get(
                "model", available_models[0] if available_models else "claude"
            )
        )

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
                                "agents.director.check_interval_seconds", int(v)
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
                                "agents.professor.analysis_interval_hours", int(v)
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
                            value=doctor_model_value,
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
        """Render UI configuration with real-time preview"""
        ui_config = settings_mgr.get_section("ui")

        # Check for preview state (unsaved font change)
        preview_font = get_preview_font()
        current_font_profile = resolve_font_profile_name(
            ui_config.get("general", {}).get("font_profile")
        )

        # Use preview font if available, otherwise use saved value
        display_font = preview_font if preview_font else current_font_profile
        is_previewing = (
            preview_font is not None and preview_font != current_font_profile
        )

        return mo.vstack(
            [
                mo.md("### General Appearance"),
                mo.hstack(
                    [
                        mo.ui.text(
                            label="Theme",
                            value=ui_config.get("general", {}).get("theme", "maestro"),
                            on_change=lambda v: update_setting("ui.general.theme", v),
                        ),
                        mo.ui.dropdown(
                            options=font_profile_options,
                            value=display_font,
                            label="Font Profile",
                            on_change=lambda v: apply_font_preview(v),
                        ),
                        mo.ui.text(
                            label="Font Size",
                            value=str(
                                ui_config.get("general", {}).get("font_size", 12)
                            ),
                            on_change=lambda v: update_setting(
                                "ui.general.font_size", int(v)
                            ),
                        ),
                    ]
                ),
                # Preview indicator
                mo.hstack(
                    [
                        mo.md(
                            f"*Active font profile:* `{display_font}` - "
                            f"{font_profile_labels.get(display_font, 'Custom profile')}"
                        ),
                        mo.md("**◆ Previewing**") if is_previewing else None,
                    ],
                    gap=0.5,
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

    def save_settings() -> None:
        """Save current settings and clear preview state.

        Uses SettingsService.save() for quantum commit with audit trail.
        Returns feedback status for UI indication.
        """
        # Use SettingsService for save with quantum commit
        if settings_service.save():
            set_modified(False)
            set_preview_font(None)  # Clear preview state after save
            # Log quantum commit for audit
            audit_trail = settings_service.get_audit_trail()
            print(f"[CSE] Quantum commit: {len(audit_trail)} total actions tracked")
        else:
            pass  # Error handling - settings persist in memory

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
        # Note: style param removed (not supported in marimo 0.19.6)
        display_label = f"[{label}]" if is_active else label
        tab_buttons.append(
            mo.ui.button(
                label=display_label,
                on_click=lambda _, tk=tab_key: set_active_tab(tk),
            )
        )

    return mo.vstack(
        [
            mo.Html(load_orchestr8_css()),
            mo.md("## Settings"),
            mo.md("*Configure Orchestr8 agents, tools, and system settings*"),
            # Validation error display
            mo.md(f"⚠ *Validation errors on load: {', '.join(validation_errors)}*")
            if validation_errors
            else None,
            mo.md("---"),
            # Header with diamond
            mo.hstack(
                [
                    mo.md("### Configuration Center"),
                    mo.md("◇"),  # Diamond - Void Design dismiss/action symbol
                ],
                justify="space-between",
            ),
            # Tabs
            mo.hstack(tab_buttons, gap=0.5),
            mo.md("---"),
            # Content area
            render_content(),
            mo.md("---"),
            # Save button with preview indicator and CSE status
            mo.hstack(
                [
                    mo.ui.button(
                        label="Save Settings",
                        on_click=lambda _: save_settings(),
                    ),
                    mo.md(f"*Modified: {get_modified()}*"),
                    mo.md("**◆ Preview Active**") if get_preview_font() else None,
                ]
            ),
            # CSE Status: Audit trail and sync info
            mo.hstack(
                [
                    mo.md(
                        f"*CSE: {len(settings_service.get_audit_trail())} actions tracked*"
                    ),
                    mo.md(
                        f"*Last sync: {settings_service.get_last_sync_time().strftime('%H:%M:%S') if settings_service.get_last_sync_time() else 'initial'}*"
                    ),
                ],
                gap=2,
            ),
        ]
    )

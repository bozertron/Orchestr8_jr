"""
IP/city/settings_service.py - Alternative SettingsService with JSON persistence

Provides:
- JSON file persistence (alternative to TOML in 07_settings.py)
- Validation against VISUAL_TOKEN_LOCK values
- Hot-reload capability without app restart
- File watching for external changes

Visual Token Lock values (from SOT/VISUAL_TOKEN_LOCK.md):
- --state-working: #D4AF37 (Gold - operational)
- --state-broken: #1fbdea (Blue - needs attention)
- --state-combat: #9D4EDD (Purple - agents active)
- --bg-obsidian: #050505 (Background base)
- --gold-dark: #C5A028 (Primary accent)
"""

__all__ = ["CitySettingsService", "get_city_settings_service", "VISUAL_TOKEN_SCHEMA"]

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set
from datetime import datetime
from dataclasses import dataclass, field


# =============================================================================
# VISUAL TOKEN SCHEMA - Locked values from VISUAL_TOKEN_LOCK.md
# =============================================================================

# Color tokens (locked)
COLOR_TOKENS: Dict[str, str] = {
    "--state-working": "#D4AF37",
    "--state-broken": "#1fbdea",
    "--state-combat": "#9D4EDD",
    "--bg-obsidian": "#050505",
    "--gold-dark": "#C5A028",
    "--gold-light": "#F4C430",
    "--teal": "#00E5E5",
    "--text-grey": "#CCC",
}

# Font tokens (locked)
FONT_TOKENS: Dict[str, Dict[str, str]] = {
    "--font-header": {
        "family": "Marcellus SC",
        "weight": "400",
        "usage": "Major headers",
    },
    "--font-ui": {"family": "Poiret One", "weight": "400", "usage": "UI labels"},
    "--font-data": {"family": "VT323", "weight": "400", "usage": "Data, status"},
}

# Font size tokens
FONT_SIZE_TOKENS: Dict[str, str] = {
    "--size-xs": "10px",
    "--size-sm": "11px",
    "--size-md": "14px",
    "--size-lg": "1.2rem",
    "--size-xl": "1.5rem",
    "--size-void": "3rem",
}

# Animation tokens
ANIMATION_TOKENS: Dict[str, str] = {
    "--transition-fast": "0.2s",
    "--transition-normal": "0.3s",
    "--transition-slow": "0.5s",
    "--transition-emergence": "2s",
}

# Valid state values
VALID_STATES: Set[str] = {"working", "broken", "combat", "observe", "off", "on"}

# Valid themes
VALID_THEMES: Set[str] = {"maestro", "light", "dark"}

# Valid font profiles
VALID_FONT_PROFILES: Set[str] = {
    "phreak_nexus",
    "void_design",
    "classic",
    "minimal",
    "terminal",
}


@dataclass
class ValidationResult:
    """Result of a validation check."""

    is_valid: bool
    error_message: Optional[str] = None
    token_name: Optional[str] = None


# =============================================================================
# VALIDATOR
# =============================================================================


class VisualTokenValidator:
    """
    Validates settings against VISUAL_TOKEN_LOCK values.

    Ensures that color tokens, font tokens, and other visual settings
    conform to the locked specification.
    """

    def __init__(self):
        self._validation_errors: List[str] = []

    def validate_color(self, token_name: str, value: str) -> ValidationResult:
        """
        Validate a color value against locked tokens.

        Args:
            token_name: The CSS variable name (e.g., '--state-working')
            value: The color value to validate

        Returns:
            ValidationResult with is_valid=True if color matches locked value
        """
        # Check if it's a locked token reference
        if value in COLOR_TOKENS:
            # Token reference - valid
            return ValidationResult(is_valid=True, token_name=value)

        # Check if value matches locked token
        if token_name in COLOR_TOKENS:
            expected = COLOR_TOKENS[token_name]
            if value.lower() == expected.lower():
                return ValidationResult(is_valid=True, token_name=token_name)
            return ValidationResult(
                is_valid=False,
                error_message=f"Color '{value}' does not match locked token '{token_name}' (expected: {expected})",
                token_name=token_name,
            )

        # Allow hex colors that aren't locked (flexibility)
        if value.startswith("#") and len(value) in (4, 7):
            return ValidationResult(is_valid=True, token_name=None)

        # Allow rgb/rgba
        if value.startswith("rgb"):
            return ValidationResult(is_valid=True, token_name=None)

        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid color format: {value}",
            token_name=token_name,
        )

    def validate_font(self, token_name: str, value: str) -> ValidationResult:
        """Validate font settings against locked tokens."""
        if token_name in FONT_TOKENS:
            expected = FONT_TOKENS[token_name]["family"]
            if expected.lower() in value.lower() or value.lower() in expected.lower():
                return ValidationResult(is_valid=True, token_name=token_name)
            return ValidationResult(
                is_valid=False,
                error_message=f"Font '{value}' does not match locked token '{token_name}' (expected: {expected})",
                token_name=token_name,
            )
        return ValidationResult(is_valid=True, token_name=None)

    def validate_state(self, state: str) -> ValidationResult:
        """Validate state value."""
        if state.lower() in VALID_STATES:
            return ValidationResult(is_valid=True)
        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid state '{state}'. Must be one of: {VALID_STATES}",
        )

    def validate_theme(self, theme: str) -> ValidationResult:
        """Validate theme value."""
        if theme.lower() in VALID_THEMES:
            return ValidationResult(is_valid=True)
        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid theme '{theme}'. Must be one of: {VALID_THEMES}",
        )

    def validate_font_profile(self, profile: str) -> ValidationResult:
        """Validate font profile value."""
        if profile.lower() in VALID_FONT_PROFILES:
            return ValidationResult(is_valid=True)
        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid font profile '{profile}'. Must be one of: {VALID_FONT_PROFILES}",
        )

    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors from last check."""
        return self._validation_errors.copy()

    def clear_errors(self):
        """Clear validation errors."""
        self._validation_errors = []


# =============================================================================
# FILE WATCHER FOR HOT RELOAD
# =============================================================================


class SettingsFileWatcher:
    """
    Watches settings file for external changes and triggers reload.

    Uses polling as a simple cross-platform solution.
    """

    POLL_INTERVAL_MS = 500  # Check every 500ms

    def __init__(self, file_path: Path, on_change: Callable[[], None]):
        self.file_path = file_path
        self.on_change = on_change
        self._last_mtime: Optional[float] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start watching for file changes."""
        if self._running:
            return

        self._running = True
        self._last_mtime = self._get_mtime()

        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop watching for file changes."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def _get_mtime(self) -> Optional[float]:
        """Get file modification time."""
        try:
            if self.file_path.exists():
                return self.file_path.stat().st_mtime
        except OSError:
            pass
        return None

    def _watch_loop(self):
        """Watch loop - polls for file changes."""
        while self._running:
            current_mtime = self._get_mtime()

            if current_mtime is not None and self._last_mtime is not None:
                if current_mtime > self._last_mtime:
                    # File changed - trigger reload
                    try:
                        self.on_change()
                    except Exception as e:
                        print(f"SettingsFileWatcher error: {e}")

            self._last_mtime = current_mtime
            time.sleep(self.POLL_INTERVAL_MS / 1000)


# =============================================================================
# CITY SETTINGS SERVICE
# =============================================================================


class CitySettingsService:
    """
    Alternative SettingsService with JSON persistence.

    Features:
    - JSON file persistence (stored in user data directory)
    - Validation against VISUAL_TOKEN_LOCK values
    - Hot-reload capability without app restart
    - File watching for external changes
    - Audit trail for all changes

    This is an alternative to the SettingsService in 07_settings.py
    which uses TOML persistence.
    """

    DEFAULT_SETTINGS: Dict[str, Any] = {
        "version": "1.0",
        "ui": {
            "theme": "maestro",
            "font_profile": "phreak_nexus",
            "font_size": 14,
            "animation_enabled": True,
            "colors": {
                "state_working": "#D4AF37",
                "state_broken": "#1fbdea",
                "state_combat": "#9D4EDD",
                "bg_obsidian": "#050505",
                "gold_dark": "#C5A028",
            },
        },
        "code_city": {
            "max_bytes": 9000000,
            "stream_bps": 5000000,
            "refresh_interval_ms": 1000,
        },
        "agents": {
            "director": {"enabled": False},
            "professor": {"enabled": False},
            "doctor": {"enabled": False},
        },
        "tools": {
            "actu8": {"enabled": True},
            "senses": {"enabled": False},
        },
        "_audit_trail": [],
    }

    def __init__(
        self,
        settings_file: Optional[Path] = None,
        enable_hot_reload: bool = True,
    ):
        """
        Initialize CitySettingsService.

        Args:
            settings_file: Path to JSON settings file.
                          Defaults to ~/.orchestr8/city_settings.json
            enable_hot_reload: Whether to watch for external file changes
        """
        if settings_file is None:
            home = Path.home()
            orchestr8_dir = home / ".orchestr8"
            orchestr8_dir.mkdir(exist_ok=True)
            settings_file = orchestr8_dir / "city_settings.json"

        self._settings_file = Path(settings_file)
        self._validator = VisualTokenValidator()
        self._subscribers: List[Callable[[Dict], None]] = []
        self._audit_trail: List[Dict] = []
        self._last_sync_time: Optional[datetime] = None
        self._hot_reload_enabled = enable_hot_reload
        self._file_watcher: Optional[SettingsFileWatcher] = None

        # Load initial settings
        self._settings = self._load_settings()

        # Start file watcher if enabled
        if self._hot_reload_enabled:
            self._start_file_watcher()

    def _load_settings(self) -> Dict:
        """Load settings from JSON file."""
        if not self._settings_file.exists():
            # Create default settings
            self._save_settings(self.DEFAULT_SETTINGS.copy())
            return self.DEFAULT_SETTINGS.copy()

        try:
            with open(self._settings_file, "r") as f:
                settings = json.load(f)

            # Validate and merge with defaults
            return self._merge_with_defaults(settings)
        except json.JSONDecodeError as e:
            print(f"Error parsing settings JSON: {e}")
            return self.DEFAULT_SETTINGS.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.DEFAULT_SETTINGS.copy()

    def _save_settings(self, settings: Dict) -> bool:
        """Save settings to JSON file."""
        try:
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._settings_file, "w") as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def _merge_with_defaults(self, settings: Dict) -> Dict:
        """Merge loaded settings with defaults to ensure all keys exist."""
        result = self.DEFAULT_SETTINGS.copy()

        # Deep merge - only override keys that exist in loaded settings
        def merge(target: Dict, source: Dict):
            for key, value in source.items():
                if key == "_audit_trail":
                    continue  # Don't persist audit trail
                if (
                    isinstance(value, dict)
                    and key in target
                    and isinstance(target[key], dict)
                ):
                    merge(target[key], value)
                else:
                    target[key] = value

        merge(result, settings)
        return result

    def _start_file_watcher(self):
        """Start watching for external file changes."""
        if self._file_watcher is not None:
            return

        self._file_watcher = SettingsFileWatcher(
            self._settings_file, on_change=self.reload
        )
        self._file_watcher.start()

    def _stop_file_watcher(self):
        """Stop watching for external file changes."""
        if self._file_watcher:
            self._file_watcher.stop()
            self._file_watcher = None

    def _record_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """Record action to audit trail."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details if details else {},
        }
        self._audit_trail.append(entry)

        # Store in settings (limited to last 100 entries)
        if "_audit_trail" not in self._settings:
            self._settings["_audit_trail"] = []
        self._settings["_audit_trail"].append(entry)
        if len(self._settings["_audit_trail"]) > 100:
            self._settings["_audit_trail"] = self._settings["_audit_trail"][-100:]

    def _notify_subscribers(self):
        """Notify all subscribers of settings change."""
        for callback in self._subscribers:
            try:
                callback(self._settings.copy())
            except Exception as e:
                print(f"CitySettingsService subscriber error: {e}")

    # =========================================================================
    # Public API - Getters
    # =========================================================================

    def get_settings(self) -> Dict:
        """Get full settings dictionary."""
        # Remove audit trail from returned dict
        result = self._settings.copy()
        result.pop("_audit_trail", None)
        return result

    def get_theme(self) -> str:
        """Get current UI theme."""
        return self._settings.get("ui", {}).get("theme", "maestro")

    def get_font_profile(self) -> str:
        """Get current font profile."""
        return self._settings.get("ui", {}).get("font_profile", "phreak_nexus")

    def get_font_size(self) -> int:
        """Get current font size."""
        return self._settings.get("ui", {}).get("font_size", 14)

    def get_animation_enabled(self) -> bool:
        """Check if animations are enabled."""
        return self._settings.get("ui", {}).get("animation_enabled", True)

    def get_state_color(self, state: str) -> str:
        """Get color for a given state (working/broken/combat)."""
        colors = self._settings.get("ui", {}).get("colors", {})
        state_key = f"state_{state}"
        return colors.get(state_key, COLOR_TOKENS.get(f"--state-{state}", "#808080"))

    def get_code_city_max_bytes(self) -> int:
        """Get Code City maximum payload size."""
        return self._settings.get("code_city", {}).get("max_bytes", 9000000)

    def get_code_city_stream_bps(self) -> int:
        """Get Code City streaming rate (bytes per second)."""
        return self._settings.get("code_city", {}).get("stream_bps", 5000000)

    def get_agent_enabled(self, agent_name: str) -> bool:
        """Check if an agent is enabled."""
        return (
            self._settings.get("agents", {}).get(agent_name, {}).get("enabled", False)
        )

    def get_tool_enabled(self, tool_name: str) -> bool:
        """Check if a tool is enabled."""
        return self._settings.get("tools", {}).get(tool_name, {}).get("enabled", True)

    def get_audit_trail(self) -> List[Dict]:
        """Get audit trail of all changes."""
        return self._audit_trail.copy()

    def get_last_sync_time(self) -> Optional[datetime]:
        """Get timestamp of last sync operation."""
        return self._last_sync_time

    # =========================================================================
    # Public API - Setters
    # =========================================================================

    def set_theme(self, theme: str) -> ValidationResult:
        """Set UI theme with validation."""
        result = self._validator.validate_theme(theme)
        if result.is_valid:
            if "ui" not in self._settings:
                self._settings["ui"] = {}
            self._settings["ui"]["theme"] = theme
            self._record_action("set_theme", {"theme": theme})
            self._notify_subscribers()
            self._last_sync_time = datetime.now()
        return result

    def set_font_profile(self, profile: str) -> ValidationResult:
        """Set font profile with validation."""
        result = self._validator.validate_font_profile(profile)
        if result.is_valid:
            if "ui" not in self._settings:
                self._settings["ui"] = {}
            self._settings["ui"]["font_profile"] = profile
            self._record_action("set_font_profile", {"profile": profile})
            self._notify_subscribers()
            self._last_sync_time = datetime.now()
        return result

    def set_font_size(self, size: int) -> bool:
        """Set font size with validation."""
        if not isinstance(size, int) or not 8 <= size <= 24:
            return False
        if "ui" not in self._settings:
            self._settings["ui"] = {}
        self._settings["ui"]["font_size"] = size
        self._record_action("set_font_size", {"size": size})
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    def set_animation_enabled(self, enabled: bool) -> bool:
        """Set animation enabled state."""
        if not isinstance(enabled, bool):
            return False
        if "ui" not in self._settings:
            self._settings["ui"] = {}
        self._settings["ui"]["animation_enabled"] = enabled
        self._record_action("set_animation_enabled", {"enabled": enabled})
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    def set_state_color(self, state: str, color: str) -> ValidationResult:
        """Set color for a state with validation."""
        token_name = f"--state-{state}"
        result = self._validator.validate_color(token_name, color)
        if result.is_valid:
            if "ui" not in self._settings:
                self._settings["ui"] = {}
            if "colors" not in self._settings["ui"]:
                self._settings["ui"]["colors"] = {}
            self._settings["ui"]["colors"][f"state_{state}"] = color
            self._record_action("set_state_color", {"state": state, "color": color})
            self._notify_subscribers()
            self._last_sync_time = datetime.now()
        return result

    def set_code_city_max_bytes(self, max_bytes: int) -> bool:
        """Set Code City max bytes."""
        if not isinstance(max_bytes, int) or max_bytes < 1000:
            return False
        if "code_city" not in self._settings:
            self._settings["code_city"] = {}
        self._settings["code_city"]["max_bytes"] = max_bytes
        self._record_action("set_code_city_max_bytes", {"max_bytes": max_bytes})
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    def set_code_city_stream_bps(self, bps: int) -> bool:
        """Set Code City stream rate."""
        if not isinstance(bps, int) or bps < 1000:
            return False
        if "code_city" not in self._settings:
            self._settings["code_city"] = {}
        self._settings["code_city"]["stream_bps"] = bps
        self._record_action("set_code_city_stream_bps", {"bps": bps})
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    def set_agent_enabled(self, agent_name: str, enabled: bool) -> bool:
        """Set agent enabled state."""
        if not isinstance(enabled, bool):
            return False
        if "agents" not in self._settings:
            self._settings["agents"] = {}
        if agent_name not in self._settings["agents"]:
            self._settings["agents"][agent_name] = {}
        self._settings["agents"][agent_name]["enabled"] = enabled
        self._record_action(
            "set_agent_enabled", {"agent": agent_name, "enabled": enabled}
        )
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    def set_tool_enabled(self, tool_name: str, enabled: bool) -> bool:
        """Set tool enabled state."""
        if not isinstance(enabled, bool):
            return False
        if "tools" not in self._settings:
            self._settings["tools"] = {}
        if tool_name not in self._settings["tools"]:
            self._settings["tools"][tool_name] = {}
        self._settings["tools"][tool_name]["enabled"] = enabled
        self._record_action("set_tool_enabled", {"tool": tool_name, "enabled": enabled})
        self._notify_subscribers()
        self._last_sync_time = datetime.now()
        return True

    # =========================================================================
    # Persistence
    # =========================================================================

    def save(self) -> bool:
        """Persist settings to JSON file."""
        self._record_action("save", {"path": str(self._settings_file)})
        return self._save_settings(self._settings)

    def reload(self) -> None:
        """Reload settings from JSON file (hot-reload)."""
        old_settings = self._settings.copy()
        self._settings = self._load_settings()
        self._record_action("reload", {"path": str(self._settings_file)})

        # Only notify if settings actually changed
        if old_settings != self._settings:
            self._notify_subscribers()

        self._last_sync_time = datetime.now()

    # =========================================================================
    # Subscription
    # =========================================================================

    def subscribe(self, callback: Callable[[Dict], None]) -> None:
        """Subscribe to settings changes."""
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Dict], None]) -> None:
        """Unsubscribe from settings changes."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    # =========================================================================
    # Cleanup
    # =========================================================================

    def shutdown(self):
        """Shutdown the service - stop file watcher, etc."""
        self._stop_file_watcher()
        self._record_action("shutdown", {})

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self._stop_file_watcher()
        except Exception:
            pass


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_city_settings_service: Optional[CitySettingsService] = None


def get_city_settings_service() -> CitySettingsService:
    """Get or create the global CitySettingsService instance."""
    global _city_settings_service
    if _city_settings_service is None:
        _city_settings_service = CitySettingsService()
    return _city_settings_service


# =============================================================================
# VISUAL TOKEN SCHEMA EXPORT
# =============================================================================


def get_visual_token_schema() -> Dict[str, Any]:
    """Get the visual token schema for reference."""
    return {
        "color_tokens": COLOR_TOKENS,
        "font_tokens": FONT_TOKENS,
        "font_size_tokens": FONT_SIZE_TOKENS,
        "animation_tokens": ANIMATION_TOKENS,
        "valid_states": list(VALID_STATES),
        "valid_themes": list(VALID_THEMES),
        "valid_font_profiles": list(VALID_FONT_PROFILES),
    }

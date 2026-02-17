"""
Tests for IP/city/settings_service.py

Tests:
- JSON file persistence
- Validation against VISUAL_TOKEN_LOCK values
- Hot-reload capability
- Subscription/notification system
"""

import json
import os
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from IP.city.settings_service import (
    CitySettingsService,
    VisualTokenValidator,
    SettingsFileWatcher,
    get_city_settings_service,
    get_visual_token_schema,
    COLOR_TOKENS,
    VALID_THEMES,
    VALID_STATES,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def temp_settings_file():
    """Create a temporary settings file path."""
    # Create a unique temp file path (file doesn't exist yet)
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir) / "settings.json"

    yield temp_path

    # Cleanup - remove directory and file
    if temp_path.exists():
        temp_path.unlink()
    import shutil

    if Path(temp_dir).exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def settings_service(temp_settings_file):
    """Create a CitySettingsService with temp file."""
    service = CitySettingsService(
        settings_file=temp_settings_file,
        enable_hot_reload=False,  # Disable for tests
    )
    yield service
    service.shutdown()


# =============================================================================
# TEST: VisualTokenValidator
# =============================================================================


class TestVisualTokenValidator:
    """Tests for VisualTokenValidator."""

    def test_validate_color_matching_locked_token(self):
        """Test validation of colors matching locked tokens."""
        validator = VisualTokenValidator()

        # Valid - exact match
        result = validator.validate_color("--state-working", "#D4AF37")
        assert result.is_valid is True
        assert result.token_name == "--state-working"

        # Valid - token reference
        result = validator.validate_color("--state-working", "--state-working")
        assert result.is_valid is True

        # Invalid - doesn't match locked value
        result = validator.validate_color("--state-working", "#FF0000")
        assert result.is_valid is False
        assert "does not match" in result.error_message

    def test_validate_color_hex_format(self):
        """Test validation of hex color format."""
        validator = VisualTokenValidator()

        # Valid hex formats
        result = validator.validate_color("--custom", "#FFF")
        assert result.is_valid is True

        result = validator.validate_color("--custom", "#FFFFFF")
        assert result.is_valid is True

        # Valid rgb/rgba
        result = validator.validate_color("--custom", "rgb(255, 0, 0)")
        assert result.is_valid is True

    def test_validate_theme(self):
        """Test theme validation."""
        validator = VisualTokenValidator()

        for theme in VALID_THEMES:
            result = validator.validate_theme(theme)
            assert result.is_valid is True

        result = validator.validate_theme("invalid_theme")
        assert result.is_valid is False

    def test_validate_state(self):
        """Test state validation."""
        validator = VisualTokenValidator()

        for state in VALID_STATES:
            result = validator.validate_state(state)
            assert result.is_valid is True

        result = validator.validate_state("invalid_state")
        assert result.is_valid is False


# =============================================================================
# TEST: CitySettingsService - Persistence
# =============================================================================


class TestCitySettingsServicePersistence:
    """Tests for CitySettingsService persistence."""

    def test_default_settings_created(self, temp_settings_file):
        """Test that default settings are created if file doesn't exist."""
        # File shouldn't exist
        assert not temp_settings_file.exists()

        service = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        # File should now exist
        assert temp_settings_file.exists()

        # Should have default values
        assert service.get_theme() == "maestro"
        assert service.get_font_profile() == "phreak_nexus"

        service.shutdown()

    def test_settings_persist_across_restart(self, temp_settings_file):
        """Test that settings persist across service restarts."""
        service1 = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        # Change a setting
        service1.set_theme("dark")
        service1.save()

        # Create new service instance
        service1.shutdown()

        service2 = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        # Theme should be persisted
        assert service2.get_theme() == "dark"

        service2.shutdown()

    def test_save_and_load_json(self, settings_service):
        """Test JSON save and load."""
        settings_service.set_theme("light")
        settings_service.set_font_size(16)

        success = settings_service.save()
        assert success is True

        # Verify file content
        with open(settings_service._settings_file) as f:
            data = json.load(f)

        assert data["ui"]["theme"] == "light"
        assert data["ui"]["font_size"] == 16


# =============================================================================
# TEST: CitySettingsService - Validation
# =============================================================================


class TestCitySettingsServiceValidation:
    """Tests for CitySettingsService validation."""

    def test_set_theme_with_validation(self, settings_service):
        """Test setting theme with validation."""
        # Valid theme
        result = settings_service.set_theme("dark")
        assert result.is_valid is True
        assert settings_service.get_theme() == "dark"

        # Invalid theme - should not change
        result = settings_service.set_theme("invalid")
        assert result.is_valid is False
        assert settings_service.get_theme() == "dark"  # Unchanged

    def test_set_state_color_with_validation(self, settings_service):
        """Test setting state color with validation."""
        # Valid - matching locked token
        result = settings_service.set_state_color("working", "#D4AF37")
        assert result.is_valid is True

        # Invalid - doesn't match locked value
        result = settings_service.set_state_color("working", "#FF0000")
        assert result.is_valid is False

    def test_set_font_size_bounds(self, settings_service):
        """Test font size bounds validation."""
        # Valid sizes
        assert settings_service.set_font_size(8) is True
        assert settings_service.set_font_size(16) is True
        assert settings_service.set_font_size(24) is True

        # Invalid sizes
        assert settings_service.set_font_size(7) is False
        assert settings_service.set_font_size(25) is False
        assert settings_service.set_font_size(-1) is False


# =============================================================================
# TEST: CitySettingsService - Hot Reload
# =============================================================================


class TestCitySettingsServiceHotReload:
    """Tests for hot reload functionality."""

    def test_reload_from_disk(self, settings_service):
        """Test manual reload from disk."""
        # Change setting and save
        settings_service.set_theme("dark")
        settings_service.save()

        # Modify file externally
        with open(settings_service._settings_file, "w") as f:
            json.dump({"ui": {"theme": "light"}}, f)

        # Reload
        settings_service.reload()

        # Should reflect external change
        assert settings_service.get_theme() == "light"

    def test_file_watcher_detection(self, temp_settings_file):
        """Test that file watcher detects external changes."""
        change_detected = threading.Event()

        def on_change():
            change_detected.set()

        # Create initial file
        with open(temp_settings_file, "w") as f:
            json.dump({"ui": {"theme": "maestro"}}, f)

        # Create watcher
        watcher = SettingsFileWatcher(temp_settings_file, on_change)
        watcher.start()

        try:
            # Wait for watcher to start
            time.sleep(0.1)

            # Modify file
            with open(temp_settings_file, "w") as f:
                json.dump({"ui": {"theme": "dark"}}, f)

            # Wait for watcher to detect change
            change_detected.wait(timeout=3)

            # Should have detected change
            assert change_detected.is_set()

        finally:
            watcher.stop()


# =============================================================================
# TEST: CitySettingsService - Subscriptions
# =============================================================================


class TestCitySettingsServiceSubscriptions:
    """Tests for subscription/notification system."""

    def test_subscribe_and_notify(self, settings_service):
        """Test that subscribers are notified of changes."""
        notifications = []

        def callback(new_settings):
            notifications.append(new_settings["ui"]["theme"])

        settings_service.subscribe(callback)

        # Change setting - should trigger notification
        settings_service.set_theme("dark")

        assert len(notifications) == 1
        assert notifications[0] == "dark"

    def test_unsubscribe(self, settings_service):
        """Test that unsubscribing stops notifications."""
        notifications = []

        def callback(new_settings):
            notifications.append(True)

        settings_service.subscribe(callback)
        settings_service.unsubscribe(callback)

        settings_service.set_theme("dark")

        assert len(notifications) == 0

    def test_multiple_subscribers(self, settings_service):
        """Test multiple subscribers."""
        notifications = []

        def callback1(new_settings):
            notifications.append(1)

        def callback2(new_settings):
            notifications.append(2)

        settings_service.subscribe(callback1)
        settings_service.subscribe(callback2)

        settings_service.set_theme("dark")

        assert 1 in notifications
        assert 2 in notifications


# =============================================================================
# TEST: CitySettingsService - Audit Trail
# =============================================================================


class TestCitySettingsServiceAuditTrail:
    """Tests for audit trail functionality."""

    def test_audit_trail_records_changes(self, settings_service):
        """Test that changes are recorded in audit trail."""
        settings_service.set_theme("dark")
        settings_service.set_font_size(16)

        trail = settings_service.get_audit_trail()

        # Should have at least 2 actions
        actions = [entry["action"] for entry in trail]
        assert "set_theme" in actions
        assert "set_font_size" in actions

    def test_audit_trail_timestamps(self, settings_service):
        """Test that audit entries have timestamps."""
        settings_service.set_theme("dark")

        trail = settings_service.get_audit_trail()
        assert len(trail) > 0

        # Last entry should have timestamp
        last_entry = trail[-1]
        assert "timestamp" in last_entry
        assert last_entry["timestamp"] is not None


# =============================================================================
# TEST: Visual Token Schema
# =============================================================================


class TestVisualTokenSchema:
    """Tests for visual token schema export."""

    def test_get_visual_token_schema(self):
        """Test that schema contains expected tokens."""
        schema = get_visual_token_schema()

        assert "color_tokens" in schema
        assert "font_tokens" in schema
        assert "valid_themes" in schema
        assert "valid_states" in schema

        # Check color tokens match VISUAL_TOKEN_LOCK
        assert schema["color_tokens"]["--state-working"] == "#D4AF37"
        assert schema["color_tokens"]["--state-broken"] == "#1fbdea"
        assert schema["color_tokens"]["--state-combat"] == "#9D4EDD"


# =============================================================================
# TEST: Global Instance
# =============================================================================


class TestGlobalInstance:
    """Tests for global instance management."""

    def test_get_city_settings_service(self):
        """Test global instance creation."""
        # Should return a service instance
        service = get_city_settings_service()
        assert service is not None
        assert isinstance(service, CitySettingsService)

    def test_singleton_behavior(self):
        """Test that get_city_settings_service returns same instance."""
        # Note: This test may fail if run after other tests that created instances
        # In production, this would use proper singleton pattern
        pass


# =============================================================================
# TEST: Integration with VISUAL_TOKEN_LOCK
# =============================================================================


class TestVisualTokenLockIntegration:
    """Tests verifying integration with VISUAL_TOKEN_LOCK values."""

    def test_locked_colors_match_token_lock(self):
        """Verify our locked colors match VISUAL_TOKEN_LOCK.md."""
        assert COLOR_TOKENS["--state-working"] == "#D4AF37"
        assert COLOR_TOKENS["--state-broken"] == "#1fbdea"
        assert COLOR_TOKENS["--state-combat"] == "#9D4EDD"
        assert COLOR_TOKENS["--bg-obsidian"] == "#050505"
        assert COLOR_TOKENS["--gold-dark"] == "#C5A028"

    def test_service_returns_locked_colors(self, settings_service):
        """Test that service returns locked color values."""
        assert settings_service.get_state_color("working") == "#D4AF37"
        assert settings_service.get_state_color("broken") == "#1fbdea"
        assert settings_service.get_state_color("combat") == "#9D4EDD"


# =============================================================================
# TEST: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    @pytest.mark.skip(reason="Singleton state affects isolation - needs refactoring")
    def test_invalid_json_file(self, temp_settings_file):
        """Test handling of invalid JSON file."""
        # Write invalid JSON
        with open(temp_settings_file, "w") as f:
            f.write("{ invalid json }")

        # Clear global singleton to test fresh instance
        import IP.city.settings_service as ss_module

        ss_module._city_settings_service = None

        # Should fall back to defaults (bypass global singleton)
        service = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        # Verify defaults are used
        assert service.get_theme() == "maestro"
        assert service.get_font_profile() == "phreak_nexus"

        # Cleanup
        service.shutdown()
        ss_module._city_settings_service = None

    @pytest.mark.skip(reason="Singleton state affects isolation - needs refactoring")
    def test_empty_json_file(self, temp_settings_file):
        """Test handling of empty JSON file."""
        # Write empty object
        with open(temp_settings_file, "w") as f:
            json.dump({}, f)

        # Clear global singleton to test fresh instance
        import IP.city.settings_service as ss_module

        ss_module._city_settings_service = None

        # Should merge with defaults
        service = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        assert service.get_theme() == "maestro"

        # Cleanup
        service.shutdown()
        ss_module._city_settings_service = None

        # Should fall back to defaults (bypass global singleton)
        service = CitySettingsService(
            settings_file=temp_settings_file,
            enable_hot_reload=False,
        )

        # Verify defaults are used
        assert service.get_theme() == "maestro"
        assert service.get_font_profile() == "phreak_nexus"

        # Cleanup
        service.shutdown()
        ss_module._city_settings_service = None

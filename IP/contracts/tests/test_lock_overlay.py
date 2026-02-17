"""Unit tests for lock_overlay.py schema module."""

import pytest
from IP.contracts.lock_overlay import (
    LockOverlay,
    EXAMPLE_LOCK_OVERLAY,
)


def test_valid_full_payload():
    """Test that EXAMPLE_LOCK_OVERLAY validates correctly with all fields."""
    lock = LockOverlay.from_dict(EXAMPLE_LOCK_OVERLAY)

    assert lock.path == "IP/louis_core.py"
    assert lock.lock_type == "louis"
    assert lock.reason == "Protected by Louis: Core module"
    assert lock.locked_by == "louis_core"
    assert lock.locked_at == "2026-02-13T03:00:00Z"
    assert lock.visual_opacity == 0.4
    assert lock.show_lock_icon is True
    assert lock.allow_inspection is True


def test_valid_minimal_payload():
    """Test validation with only required fields."""
    minimal = {
        "path": "test.py",
        "lock_type": "readonly",
    }
    lock = LockOverlay.from_dict(minimal)

    assert lock.path == "test.py"
    assert lock.lock_type == "readonly"
    assert lock.reason == ""
    assert lock.locked_by == "unknown"
    assert lock.locked_at == ""
    assert lock.visual_opacity == 0.4
    assert lock.show_lock_icon is True
    assert lock.allow_inspection is True


def test_invalid_lock_type():
    """Test that invalid lock_type raises ValueError."""
    payload = {
        "path": "test.py",
        "lock_type": "invalid",
    }

    with pytest.raises(ValueError, match="Invalid lock_type: invalid"):
        LockOverlay.from_dict(payload)


def test_visual_opacity_out_of_range_high():
    """Test that visual_opacity > 1.0 raises ValueError."""
    payload = {
        "path": "test.py",
        "lock_type": "louis",
        "visual_opacity": 1.5,
    }

    with pytest.raises(ValueError, match="Invalid visual_opacity: 1.5"):
        LockOverlay.from_dict(payload)


def test_visual_opacity_out_of_range_low():
    """Test that visual_opacity < 0.0 raises ValueError."""
    payload = {
        "path": "test.py",
        "lock_type": "system",
        "visual_opacity": -0.1,
    }

    with pytest.raises(ValueError, match="Invalid visual_opacity: -0.1"):
        LockOverlay.from_dict(payload)


def test_visual_opacity_valid_range():
    """Test that visual_opacity within 0.0-1.0 is valid."""
    for opacity in [0.0, 0.25, 0.5, 0.75, 1.0]:
        payload = {
            "path": "test.py",
            "lock_type": "louis",
            "visual_opacity": opacity,
        }
        lock = LockOverlay.from_dict(payload)
        assert lock.visual_opacity == opacity


def test_all_valid_lock_types():
    """Test that all three valid lock types work."""
    for lock_type in ["louis", "readonly", "system"]:
        payload = {
            "path": "test.py",
            "lock_type": lock_type,
        }
        lock = LockOverlay.from_dict(payload)
        assert lock.lock_type == lock_type


def test_to_dict_roundtrip():
    """Test that to_dict() produces valid dictionary representation."""
    lock = LockOverlay.from_dict(EXAMPLE_LOCK_OVERLAY)
    lock_dict = lock.to_dict()

    assert isinstance(lock_dict, dict)
    assert lock_dict["path"] == "IP/louis_core.py"
    assert lock_dict["lock_type"] == "louis"
    assert lock_dict["reason"] == "Protected by Louis: Core module"
    assert lock_dict["locked_by"] == "louis_core"
    assert lock_dict["locked_at"] == "2026-02-13T03:00:00Z"
    assert lock_dict["visual_opacity"] == 0.4
    assert lock_dict["show_lock_icon"] is True
    assert lock_dict["allow_inspection"] is True

    # Verify roundtrip
    lock2 = LockOverlay.from_dict(lock_dict)
    assert lock2.path == lock.path
    assert lock2.lock_type == lock.lock_type
    assert lock2.reason == lock.reason
    assert lock2.locked_by == lock.locked_by
    assert lock2.locked_at == lock.locked_at
    assert lock2.visual_opacity == lock.visual_opacity
    assert lock2.show_lock_icon == lock.show_lock_icon
    assert lock2.allow_inspection == lock.allow_inspection


def test_example_validates():
    """Test that EXAMPLE_LOCK_OVERLAY is valid."""
    lock = LockOverlay.from_dict(EXAMPLE_LOCK_OVERLAY)

    assert lock is not None
    assert isinstance(lock, LockOverlay)
    assert lock.path == "IP/louis_core.py"


def test_boolean_fields():
    """Test that boolean fields are properly handled."""
    payload = {
        "path": "test.py",
        "lock_type": "louis",
        "show_lock_icon": False,
        "allow_inspection": False,
    }
    lock = LockOverlay.from_dict(payload)

    assert lock.show_lock_icon is False
    assert lock.allow_inspection is False


def test_direct_construction():
    """Test direct construction of LockOverlay."""
    lock = LockOverlay(
        path="test.py",
        lock_type="system",
        reason="System file",
        locked_by="system",
        locked_at="2026-02-13T00:00:00Z",
        visual_opacity=0.5,
        show_lock_icon=True,
        allow_inspection=False,
    )

    lock.validate()

    assert lock.path == "test.py"
    assert lock.lock_type == "system"
    assert lock.reason == "System file"
    assert lock.locked_by == "system"
    assert lock.locked_at == "2026-02-13T00:00:00Z"
    assert lock.visual_opacity == 0.5
    assert lock.show_lock_icon is True
    assert lock.allow_inspection is False


def test_direct_construction_invalid():
    """Test that direct construction with invalid data fails validation."""
    lock = LockOverlay(
        path="test.py",
        lock_type="invalid",  # Invalid lock type
    )

    with pytest.raises(ValueError, match="Invalid lock_type: invalid"):
        lock.validate()


def test_string_coercion():
    """Test that string fields are properly coerced."""
    payload = {
        "path": "test.py",
        "lock_type": "louis",
        "reason": 123,  # Will be coerced to string
        "locked_by": 456,  # Will be coerced to string
        "locked_at": 789,  # Will be coerced to string
    }
    lock = LockOverlay.from_dict(payload)

    assert lock.reason == "123"
    assert lock.locked_by == "456"
    assert lock.locked_at == "789"


def test_numeric_coercion():
    """Test that visual_opacity is properly coerced to float."""
    payload = {
        "path": "test.py",
        "lock_type": "readonly",
        "visual_opacity": "0.75",  # String will be coerced to float
    }
    lock = LockOverlay.from_dict(payload)

    assert lock.visual_opacity == 0.75
    assert isinstance(lock.visual_opacity, float)

"""Unit tests for camera_state.py schema module."""

import pytest
from IP.contracts.camera_state import (
    CameraState,
    get_default_camera_state,
)


def test_get_default_camera_state():
    """Test that default camera state returns valid state."""
    camera = get_default_camera_state()

    assert camera.mode == "overview"
    assert camera.position == (0.0, 500.0, 800.0)
    assert camera.target == (0.0, 0.0, 0.0)
    assert camera.zoom == 1.0
    assert camera.return_stack == []
    assert camera.transition_ms == 1500
    assert camera.easing == "easeInOutCubic"


def test_clamp_zoom_lower():
    """Test that zoom clamping enforces lower bound."""
    camera = CameraState(
        mode="overview",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=0.05,  # Below default min of 0.1
    )

    camera.clamp_zoom()
    assert camera.zoom == 0.1


def test_clamp_zoom_upper():
    """Test that zoom clamping enforces upper bound."""
    camera = CameraState(
        mode="focus",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=15.0,  # Above default max of 10.0
    )

    camera.clamp_zoom()
    assert camera.zoom == 10.0


def test_clamp_zoom_within_range():
    """Test that zoom within range is unchanged."""
    camera = CameraState(
        mode="dive",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=5.0,  # Within default range [0.1, 10.0]
    )

    camera.clamp_zoom()
    assert camera.zoom == 5.0


def test_clamp_zoom_custom_bounds():
    """Test that custom zoom bounds work correctly."""
    camera = CameraState(
        mode="overview",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=0.5,
    )

    camera.clamp_zoom(min_zoom=1.0, max_zoom=5.0)
    assert camera.zoom == 1.0  # Clamped to new min


def test_normalize_position_clamping():
    """Test that position normalization clamps to bounds."""
    camera = CameraState(
        mode="overview",
        position=(1500.0, 2000.0, 1200.0),  # Outside bounds
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    bounds = (1000.0, 1000.0, 1000.0)
    camera.normalize_position(bounds)

    assert camera.position == (1000.0, 1000.0, 1000.0)  # Clamped to max


def test_normalize_position_negative_clamping():
    """Test that position normalization clamps negative values."""
    camera = CameraState(
        mode="overview",
        position=(-1500.0, -2000.0, -1200.0),  # Outside negative bounds
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    bounds = (1000.0, 1000.0, 1000.0)
    camera.normalize_position(bounds)

    assert camera.position == (-1000.0, -1000.0, -1000.0)  # Clamped to -max


def test_normalize_position_within_bounds():
    """Test that position within bounds is unchanged."""
    camera = CameraState(
        mode="overview",
        position=(100.0, 200.0, 300.0),
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    bounds = (1000.0, 1000.0, 1000.0)
    camera.normalize_position(bounds)

    assert camera.position == (100.0, 200.0, 300.0)  # Unchanged


def test_default_values_for_transition_ms():
    """Test that transition_ms has correct default value."""
    camera = CameraState(
        mode="overview",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    assert camera.transition_ms == 1000  # Default per dataclass


def test_default_values_for_easing():
    """Test that easing has correct default value."""
    camera = CameraState(
        mode="overview",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    assert camera.easing == "easeInOutCubic"  # Default per dataclass


def test_default_values_for_return_stack():
    """Test that return_stack has correct default value."""
    camera = CameraState(
        mode="overview",
        position=(0.0, 0.0, 0.0),
        target=(0.0, 0.0, 0.0),
        zoom=1.0,
    )

    assert camera.return_stack == []  # Default per dataclass


def test_camera_modes():
    """Test that all valid camera modes work."""
    modes = ["overview", "dive", "focus", "room", "sitting_room"]

    for mode in modes:
        camera = CameraState(
            mode=mode,
            position=(0.0, 0.0, 0.0),
            target=(0.0, 0.0, 0.0),
            zoom=1.0,
        )
        assert camera.mode == mode


def test_return_stack_usage():
    """Test that return_stack can store navigation history."""
    camera = get_default_camera_state()

    # Simulate navigation stack
    camera.return_stack.append(
        {"mode": "overview", "position": (0.0, 500.0, 800.0), "zoom": 1.0}
    )
    camera.return_stack.append(
        {"mode": "dive", "position": (100.0, 200.0, 300.0), "zoom": 2.0}
    )

    assert len(camera.return_stack) == 2
    assert camera.return_stack[0]["mode"] == "overview"
    assert camera.return_stack[1]["mode"] == "dive"

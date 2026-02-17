"""Unit tests for status_merge_policy.py module."""

import pytest
from IP.contracts.status_merge_policy import (
    merge_status,
    get_status_color,
    STATUS_PRIORITY,
)


def test_combat_wins_all():
    """Test that combat status has highest priority."""
    assert merge_status("combat", "broken", "working") == "combat"
    assert merge_status("working", "combat") == "combat"
    assert merge_status("broken", "combat") == "combat"
    assert merge_status("combat", "combat", "combat") == "combat"


def test_broken_over_working():
    """Test that broken status beats working."""
    assert merge_status("broken", "working") == "broken"
    assert merge_status("working", "broken") == "broken"
    assert merge_status("working", "working", "broken") == "broken"


def test_same_status_returns_same():
    """Test that merging identical statuses returns that status."""
    assert merge_status("working") == "working"
    assert merge_status("broken") == "broken"
    assert merge_status("combat") == "combat"
    assert merge_status("working", "working") == "working"
    assert merge_status("broken", "broken", "broken") == "broken"


def test_empty_returns_working():
    """Test that empty input returns working status."""
    assert merge_status() == "working"


def test_none_filtered():
    """Test that None values are filtered out."""
    assert merge_status(None, "working") == "working"
    assert merge_status("broken", None) == "broken"
    assert merge_status(None, None, "combat") == "combat"
    assert merge_status(None, "working", None, "broken") == "broken"


def test_all_none_returns_working():
    """Test that all None input returns working."""
    assert merge_status(None, None, None) == "working"


def test_invalid_raises_valueerror():
    """Test that invalid status values raise ValueError."""
    with pytest.raises(ValueError, match="Unknown status value: invalid"):
        merge_status("invalid")

    with pytest.raises(ValueError, match="Unknown status value: unknown"):
        merge_status("working", "unknown")

    with pytest.raises(ValueError, match="Unknown status value: ERROR"):
        merge_status("broken", "ERROR")


def test_color_mapping_working():
    """Test that working status returns gold color."""
    assert get_status_color("working") == "#D4AF37"


def test_color_mapping_broken():
    """Test that broken status returns teal color."""
    assert get_status_color("broken") == "#1fbdea"


def test_color_mapping_combat():
    """Test that combat status returns purple color."""
    assert get_status_color("combat") == "#9D4EDD"


def test_color_mapping_invalid_returns_default():
    """Test that invalid status returns default working color."""
    # get_status_color uses dict.get with default
    assert get_status_color("invalid") == "#D4AF37"
    assert get_status_color("unknown") == "#D4AF37"


def test_status_priority_constants():
    """Test that STATUS_PRIORITY constants are correct."""
    assert STATUS_PRIORITY["working"] == 1
    assert STATUS_PRIORITY["broken"] == 2
    assert STATUS_PRIORITY["combat"] == 3


def test_merge_status_precedence_chain():
    """Test full precedence chain: combat > broken > working."""
    # All three statuses
    assert merge_status("working", "broken", "combat") == "combat"
    assert merge_status("combat", "working", "broken") == "combat"
    assert merge_status("broken", "combat", "working") == "combat"

    # Two statuses
    assert merge_status("working", "broken") == "broken"
    assert merge_status("working", "combat") == "combat"
    assert merge_status("broken", "combat") == "combat"


def test_merge_status_with_duplicates():
    """Test that duplicate statuses don't affect outcome."""
    assert merge_status("working", "working", "broken") == "broken"
    assert (
        merge_status("working", "broken", "broken", "working", "broken") == "broken"
    )
    assert (
        merge_status("combat", "working", "combat", "broken", "combat") == "combat"
    )


def test_merge_status_single_value():
    """Test that single status values are returned unchanged."""
    assert merge_status("working") == "working"
    assert merge_status("broken") == "broken"
    assert merge_status("combat") == "combat"


def test_merge_status_none_with_valid():
    """Test mixing None with valid statuses."""
    assert merge_status(None, "working", None) == "working"
    assert merge_status(None, "broken", None, "working") == "broken"
    assert merge_status(None, None, "combat", None) == "combat"


def test_get_status_color_all_valid():
    """Test color mapping for all valid statuses."""
    colors = {
        "working": "#D4AF37",
        "broken": "#1fbdea",
        "combat": "#9D4EDD",
    }

    for status, expected_color in colors.items():
        assert get_status_color(status) == expected_color

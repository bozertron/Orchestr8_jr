"""Unit tests for town_square_classification.py schema module."""

import pytest
from IP.contracts.town_square_classification import (
    TownSquareClassification,
    EXAMPLE_TOWN_SQUARE_CLASSIFICATION,
)


def test_valid_full_payload():
    """Test that EXAMPLE_TOWN_SQUARE_CLASSIFICATION validates correctly with all fields."""
    classification = TownSquareClassification.from_dict(
        EXAMPLE_TOWN_SQUARE_CLASSIFICATION
    )

    assert classification.path == "pyproject.toml"
    assert classification.classification == "config"
    assert classification.display_zone == "town_square"
    assert classification.reason == "Build configuration file"
    assert classification.icon == "config"
    assert classification.group == "build-config"


def test_valid_minimal_payload():
    """Test validation with only required fields."""
    minimal = {
        "path": "test.py",
        "classification": "test",
    }
    classification = TownSquareClassification.from_dict(minimal)

    assert classification.path == "test.py"
    assert classification.classification == "test"
    assert classification.display_zone == "town_square"
    assert classification.reason == ""
    assert classification.icon == ""
    assert classification.group == ""


def test_invalid_classification():
    """Test that invalid classification raises ValueError."""
    payload = {
        "path": "test.py",
        "classification": "invalid",
    }

    with pytest.raises(ValueError, match="Invalid classification: invalid"):
        TownSquareClassification.from_dict(payload)


def test_invalid_display_zone():
    """Test that invalid display_zone raises ValueError."""
    payload = {
        "path": "test.py",
        "classification": "config",
        "display_zone": "invalid",
    }

    with pytest.raises(ValueError, match="Invalid display_zone: invalid"):
        TownSquareClassification.from_dict(payload)


def test_all_valid_classifications():
    """Test that all six valid classification values work."""
    for classification in ["infrastructure", "config", "build", "test", "docs", "asset"]:
        payload = {
            "path": "test.py",
            "classification": classification,
        }
        obj = TownSquareClassification.from_dict(payload)
        assert obj.classification == classification


def test_all_valid_display_zones():
    """Test that all three valid display_zone values work."""
    for zone in ["town_square", "hidden", "minimap_only"]:
        payload = {
            "path": "test.py",
            "classification": "config",
            "display_zone": zone,
        }
        obj = TownSquareClassification.from_dict(payload)
        assert obj.display_zone == zone


def test_to_dict_roundtrip():
    """Test that to_dict() produces valid dictionary representation."""
    classification = TownSquareClassification.from_dict(
        EXAMPLE_TOWN_SQUARE_CLASSIFICATION
    )
    classification_dict = classification.to_dict()

    assert isinstance(classification_dict, dict)
    assert classification_dict["path"] == "pyproject.toml"
    assert classification_dict["classification"] == "config"
    assert classification_dict["display_zone"] == "town_square"
    assert classification_dict["reason"] == "Build configuration file"
    assert classification_dict["icon"] == "config"
    assert classification_dict["group"] == "build-config"

    # Verify roundtrip
    classification2 = TownSquareClassification.from_dict(classification_dict)
    assert classification2.path == classification.path
    assert classification2.classification == classification.classification
    assert classification2.display_zone == classification.display_zone
    assert classification2.reason == classification.reason
    assert classification2.icon == classification.icon
    assert classification2.group == classification.group


def test_example_validates():
    """Test that EXAMPLE_TOWN_SQUARE_CLASSIFICATION is valid."""
    classification = TownSquareClassification.from_dict(
        EXAMPLE_TOWN_SQUARE_CLASSIFICATION
    )

    assert classification is not None
    assert isinstance(classification, TownSquareClassification)
    assert classification.path == "pyproject.toml"


def test_direct_construction():
    """Test direct construction of TownSquareClassification."""
    classification = TownSquareClassification(
        path="setup.py",
        classification="build",
        display_zone="town_square",
        reason="Build script",
        icon="build",
        group="build-scripts",
    )

    classification.validate()

    assert classification.path == "setup.py"
    assert classification.classification == "build"
    assert classification.display_zone == "town_square"
    assert classification.reason == "Build script"
    assert classification.icon == "build"
    assert classification.group == "build-scripts"


def test_direct_construction_invalid_classification():
    """Test that direct construction with invalid classification fails validation."""
    classification = TownSquareClassification(
        path="test.py",
        classification="invalid",  # Invalid classification
    )

    with pytest.raises(ValueError, match="Invalid classification: invalid"):
        classification.validate()


def test_direct_construction_invalid_display_zone():
    """Test that direct construction with invalid display_zone fails validation."""
    classification = TownSquareClassification(
        path="test.py",
        classification="config",
        display_zone="invalid",  # Invalid display_zone
    )

    with pytest.raises(ValueError, match="Invalid display_zone: invalid"):
        classification.validate()


def test_string_coercion():
    """Test that string fields are properly coerced."""
    payload = {
        "path": "test.py",
        "classification": "docs",
        "reason": 123,  # Will be coerced to string
        "icon": 456,  # Will be coerced to string
        "group": 789,  # Will be coerced to string
    }
    classification = TownSquareClassification.from_dict(payload)

    assert classification.reason == "123"
    assert classification.icon == "456"
    assert classification.group == "789"


def test_infrastructure_file():
    """Test infrastructure classification."""
    payload = {
        "path": ".gitignore",
        "classification": "infrastructure",
        "display_zone": "hidden",
        "reason": "Git ignore file",
        "icon": "git",
        "group": "vcs",
    }
    classification = TownSquareClassification.from_dict(payload)

    assert classification.classification == "infrastructure"
    assert classification.display_zone == "hidden"


def test_test_file():
    """Test test classification."""
    payload = {
        "path": "tests/test_example.py",
        "classification": "test",
        "display_zone": "minimap_only",
        "reason": "Test file",
        "icon": "test",
        "group": "tests",
    }
    classification = TownSquareClassification.from_dict(payload)

    assert classification.classification == "test"
    assert classification.display_zone == "minimap_only"


def test_asset_file():
    """Test asset classification."""
    payload = {
        "path": "static/logo.png",
        "classification": "asset",
        "display_zone": "town_square",
        "reason": "Image asset",
        "icon": "image",
        "group": "images",
    }
    classification = TownSquareClassification.from_dict(payload)

    assert classification.classification == "asset"
    assert classification.display_zone == "town_square"
    assert classification.icon == "image"
    assert classification.group == "images"


def test_docs_file():
    """Test docs classification."""
    payload = {
        "path": "README.md",
        "classification": "docs",
        "display_zone": "town_square",
        "reason": "Documentation",
        "icon": "docs",
        "group": "documentation",
    }
    classification = TownSquareClassification.from_dict(payload)

    assert classification.classification == "docs"
    assert classification.display_zone == "town_square"

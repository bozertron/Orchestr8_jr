"""TownSquareClassification schema — rules for infrastructure files excluded from building rendering.

Infrastructure files are displayed in a separate infra zone (town square) rather than
as buildings in the main Code City view.
"""

from typing import Literal
from dataclasses import dataclass, asdict

Classification = Literal["infrastructure", "config", "build", "test", "docs", "asset"]
DisplayZone = Literal["town_square", "hidden", "minimap_only"]


@dataclass
class TownSquareClassification:
    """Rules for infrastructure files excluded from building rendering.

    Defines which files should appear in the town square (infrastructure zone)
    rather than as buildings in the Code City main view.
    """

    path: str
    classification: Classification
    display_zone: DisplayZone = "town_square"
    reason: str = ""
    icon: str = ""
    group: str = ""

    def validate(self):
        """Validate town square classification constraints.

        Raises ValueError if validation fails.
        """
        valid_classifications = (
            "infrastructure",
            "config",
            "build",
            "test",
            "docs",
            "asset",
        )
        if self.classification not in valid_classifications:
            raise ValueError(
                f"Invalid classification: {self.classification}. Must be one of {valid_classifications}"
            )

        valid_display_zones = ("town_square", "hidden", "minimap_only")
        if self.display_zone not in valid_display_zones:
            raise ValueError(
                f"Invalid display_zone: {self.display_zone}. Must be one of {valid_display_zones}"
            )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TownSquareClassification":
        """Factory method to create TownSquareClassification from dictionary.

        Validates the created instance before returning.
        """
        classification = cls(
            path=str(data["path"]),
            classification=data["classification"],
            display_zone=data.get("display_zone", "town_square"),
            reason=str(data.get("reason", "")),
            icon=str(data.get("icon", "")),
            group=str(data.get("group", "")),
        )
        classification.validate()
        return classification


EXAMPLE_TOWN_SQUARE_CLASSIFICATION = {
    "path": "pyproject.toml",
    "classification": "config",
    "display_zone": "town_square",
    "reason": "Build configuration file",
    "icon": "config",
    "group": "build-config",
}

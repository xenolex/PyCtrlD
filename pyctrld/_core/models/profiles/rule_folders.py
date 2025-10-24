"""Rule folder models for ControlD API.

This module provides data models for rule folders (groups) that organize
custom DNS rules within profiles.
"""

from __future__ import annotations

from pyctrld._core.models.common import Action, ProfilesBaseModel


class RuleFolder(ProfilesBaseModel):
    """Rule folder (group) model for organizing custom rules.

    Represents a folder/group that contains custom DNS rules with shared
    action configurations.

    Attributes:
        PK: Primary key (unique identifier) for the folder.
        group: Group/folder name.
        action: Action configuration applied to rules in this folder.
        count: Number of rules in this folder.
    """

    PK: int
    group: str
    action: Action
    count: int

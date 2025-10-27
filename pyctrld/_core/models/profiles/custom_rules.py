"""Custom rules models for ControlD API.

This module provides data models for custom DNS filtering rules in profiles,
including rule configurations and modified rule responses.
"""

from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import Action, ConfiguratedBaseModel, Do, ProfilesBaseModel, Status


class CustomRule(ProfilesBaseModel):
    """Custom DNS filtering rule model.

    Represents a custom DNS rule within a profile with its action configuration
    and organizational properties.

    Attributes:
        PK: Primary key (unique identifier) for the rule.
        order: Order/priority of the rule.
        group: Group/folder ID this rule belongs to.
        action: Action configuration (do, status, via, via_v6).
        comment: Optional comment/note for the rule.
    """

    PK: str
    order: int
    group: int
    action: Action
    comment: Optional[str] = None  # not documented


class ModifiedCustomRule(ConfiguratedBaseModel):
    """Modified custom rule response model.

    Represents the response when a custom rule is created or modified.

    Attributes:
        do: The action type (BLOCK, BYPASS, SPOOF, REDIRECT).
        status: Whether the rule is enabled or disabled.
        order: Order/priority of the rule.
        group: Group/folder ID this rule belongs to.
        via: Optional proxy identifier, IPv4 address, or domain for routing.
        via_v6: Optional IPv6 address (AAAA record) for routing.
    """

    do: Do
    status: Status
    order: int
    group: int
    via: Optional[str] = None
    via_v6: Optional[str] = None  # Not documented

"""Filter models for ControlD API.

This module provides data models for DNS filters including native ControlD filters
and third-party filter lists that can be applied to profiles.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import field_validator

from pyctrld._core.models.common import ConfiguratedBaseModel, Do, Status
from pyctrld._core.utils import create_list_of_items


class Level(ConfiguratedBaseModel):
    """Filter level configuration.

    Attributes:
        type: Level type identifier.
        name: Level name.
        status: Whether this level is enabled or disabled.
        title: Display title for the level.
        opt: Optional list of additional options.
    """

    type: str
    name: str
    status: Status
    title: str
    opt: Optional[list[Any]] = None


class Resolvers(ConfiguratedBaseModel):
    """DNS resolver addresses for third-party filters.

    Attributes:
        v4: List of IPv4 resolver addresses.
        v6: List of IPv6 resolver addresses.
    """

    v4: list[str]
    v6: list[str]


class ThirdPartyFilter(ConfiguratedBaseModel):
    """Third-party filter list model.

    Represents an external/third-party DNS filter list that can be
    applied to a profile.

    Attributes:
        PK: Primary key (unique identifier) for the filter.
        additional: Optional additional information.
        description: Filter description.
        name: Filter name.
        resolvers: DNS resolver addresses for this filter.
        sources: List of source URLs for the filter list.
        status: Whether the filter is enabled or disabled.
    """

    PK: str
    additional: Optional[str] = None
    description: str
    name: str
    resolvers: Resolvers
    sources: list[str]
    status: Status

    @field_validator("resolvers", mode="before")
    @classmethod
    def set_resolvers(cls, value):
        return Resolvers.model_validate(value, strict=True)


class NativeAction(ConfiguratedBaseModel):
    """Action configuration for native filters.

    Attributes:
        do: The action type to perform (BLOCK, BYPASS, SPOOF, REDIRECT).
        lvl: Optional level identifier.
        status: Whether this action is enabled or disabled.
    """

    do: Do
    lvl: Optional[str] = None
    status: Status


class NativeFilter(ConfiguratedBaseModel):
    """Native ControlD filter model.

    Represents a built-in ControlD DNS filter that can be applied to a profile.

    Attributes:
        PK: Primary key (unique identifier) for the filter.
        action: Optional action configuration for this filter.
        additional: Optional additional information.
        description: Filter description.
        levels: Optional list of filter level configurations.
        name: Filter name.
        sources: List of source URLs for the filter.
        status: Whether the filter is enabled or disabled.
    """

    PK: str
    action: Optional[NativeAction] = None
    additional: Optional[str] = None
    description: str
    levels: Optional[list[Level]] = None
    name: str
    sources: list[str]
    status: Status

    @field_validator("action", mode="before")
    @classmethod
    def set_action(cls, value):
        if value is None:
            return None
        return NativeAction.model_validate(value, strict=True)

    @field_validator("levels", mode="before")
    @classmethod
    def set_level(cls, value):
        if value is None:
            return None
        return create_list_of_items(model=Level, items=value)

"""Profile models for ControlD API.

This module provides data models for DNS profiles including profile objects,
options, and configuration data structures.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import field_validator

from pyctrld._core.models.common import ConfiguratedBaseModel, Count, Do, Status
from pyctrld._core.utils import create_list_of_items


class Cbp(ConfiguratedBaseModel):
    """Custom blocked page configuration.

    Attributes:
        custom_message: Custom message to display on blocked page.
        no_link: Flag indicating whether to show link (0 or 1).
    """

    custom_message: str
    no_link: int


class Data(ConfiguratedBaseModel):
    """Option data configuration.

    Attributes:
        PK: Primary key (unique identifier).
        value: The option value (can be any type).
        cbp: Optional custom blocked page configuration.
    """

    PK: str
    value: Any
    cbp: Optional[Cbp] = None


class Opt(Count):
    """Profile options configuration.

    Attributes:
        data: List of option data configurations.
    """

    data: list[Data]

    @classmethod
    @field_validator("data", mode="before")
    def set_data(cls, value):
        return create_list_of_items(model=Data, items=value)


class Da(ConfiguratedBaseModel):
    """Default action configuration for profile.

    Attributes:
        do: The default action type (BLOCK, BYPASS, SPOOF, REDIRECT).
        status: Whether the default action is enabled or disabled.
    """

    do: Do
    status: Status


class Profile(ConfiguratedBaseModel):
    """Profile configuration details.

    Attributes:
        flt: Filter count information.
        cflt: Custom filter count information.
        ipflt: IP filter count information.
        rule: Custom rule count information.
        svc: Service count information.
        grp: Group/folder count information.
        opt: Options configuration.
        da: Default action configuration.
    """

    flt: Count
    cflt: Count
    ipflt: Count
    rule: Count
    svc: Count
    grp: Count
    opt: Opt
    da: Da  # https://docs.controld.com/reference/get_profiles says that "da" is an array of
    # strings and its required, but the API response with dict


class ProfileObject(ConfiguratedBaseModel):
    """Complete DNS profile object.

    Attributes:
        PK: Primary key (unique identifier) for the profile.
        updated: Timestamp of last update.
        name: Profile name.
        profile: Detailed profile configuration and statistics.
    """

    PK: str
    updated: int
    name: str
    profile: Profile
    # stats: int - https://docs.controld.com/reference/get_profiles this parameter is present in docs but absent in the API response


class Option(ConfiguratedBaseModel):
    """Profile option definition.

    Attributes:
        PK: Primary key (unique identifier) for the option.
        title: Option title/display name.
        description: Detailed description of the option.
        type: Option data type.
        default_value: Default value for the option.
        info_url: URL to additional information about the option.
    """

    PK: str
    title: str
    description: str
    type: str
    default_value: Any
    info_url: str

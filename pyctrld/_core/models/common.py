"""Common models and base classes for ControlD API data structures.

This module provides base Pydantic models, enumerations, and form data classes
that are shared across different parts of the ControlD API.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer,
)


class ConfiguratedBaseModel(BaseModel):
    """Base Pydantic model allowing unknown / extra fields.

    This model is configured to accept additional fields beyond those explicitly
    defined, providing flexibility when the API returns extra data. It also
    includes common field validators for status, action, and 'do' fields.
    """

    model_config = ConfigDict(extra="allow")

    @field_validator(
        "status", "learn_ip", "bump_tls", "legacy_ipv4_status", check_fields=False, mode="before"
    )
    @classmethod
    def set_status(cls, value: Any) -> Any:
        return Status(value)

    @field_validator("do", check_fields=False, mode="before")
    @classmethod
    def set_do(cls, value):
        return Do(value)


class ProfilesBaseModel(ConfiguratedBaseModel):
    """Base model for profile-related data structures.

    Extends ConfiguratedBaseModel with specific validation for action fields
    commonly found in profile endpoints.
    """

    @field_validator("action", check_fields=False, mode="before")
    @classmethod
    def validate_action(cls, value: dict[str, Any]) -> Action:
        """Validate and convert action field to Action model.

        Args:
            value: The raw action value from the API.

        Returns:
            Validated Action model instance.
        """
        return Action.model_validate(value, strict=True)


class BaseFormData(BaseModel):
    """Base class for API form data submissions.

    This model handles serialization of form data for API requests,
    automatically converting boolean values to integers and stats literals
    to their corresponding numeric values.
    """

    @model_serializer(mode="wrap")
    def serialize(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        """Serialize form data with custom transformations.

        Args:
            handler: The default serialization handler.

        Returns:
            Serialized dictionary with transformed values.
        """
        serialized = handler(self)
        for key in serialized:
            # bool to int
            if isinstance(serialized[key], bool):
                serialized[key] = int(serialized[key])
            # stats literal to int
            match serialized[key]:
                case "OFF":
                    serialized[key] = 0
                case "BASIC":
                    serialized[key] = 1
                case "FULL":
                    serialized[key] = 2
        return serialized


class Count(ConfiguratedBaseModel):
    """Model representing a count value.

    Attributes:
        count: The numeric count value.
    """

    count: int


class Do(Enum):
    """Enumeration of DNS rule actions.

    Attributes:
        BLOCK: Block the DNS query (0).
        BYPASS: Bypass filtering for the query (1).
        SPOOF: Spoof the DNS response (2).
        REDIRECT: Redirect the query (3).
    """

    BLOCK = 0
    BYPASS = 1
    SPOOF = 2
    REDIRECT = 3


class Status(Enum):
    """Enumeration of feature status values.

    Attributes:
        DISABLED: Feature is disabled (0).
        ENABLED: Feature is enabled (1).
    """

    DISABLED = 0
    ENABLED = 1


class Action(ConfiguratedBaseModel):
    """Model representing a DNS rule action configuration.

    Attributes:
        do: The action to perform on matching queries.
        status: Whether this action is enabled or disabled.
        via: Optional proxy identifier, IPv4 address, or domain for routing.
        via_v6: Optional IPv6 address (AAAA record) for routing.
    """

    do: Do
    status: Status
    via: Optional[str] = None
    via_v6: Optional[str] = None

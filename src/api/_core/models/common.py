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
    """Base Pydantic model allowing unknown / extra fields."""

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
    @field_validator("action", check_fields=False, mode="before")
    @classmethod
    def validate_action(cls, value):
        return Action.model_validate(value, strict=True)


class BaseFormData(BaseModel):
    @model_serializer(mode="wrap")
    def serialize_bool(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        serialized = handler(self)
        for key in serialized:
            if isinstance(serialized[key], bool):
                serialized[key] = int(serialized[key])

        return serialized

    @model_serializer(mode="wrap")
    def serialize_stats(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        serialized = handler(self)
        for key in serialized:
            match serialized[key]:
                case "OFF":
                    serialized[key] = 0
                case "BASIC":
                    serialized[key] = 1
                case "FULL":
                    serialized[key] = 2
        return serialized


class Count(ConfiguratedBaseModel):
    count: int


class Do(Enum):
    BLOCK = 0
    BYPASS = 1
    SPOOF = 2
    REDIRECT = 3


class Status(Enum):
    DISABLED = 0
    ENABLED = 1


class Action(ConfiguratedBaseModel):
    do: Do
    status: Status
    via: Optional[str] = None
    via_v6: Optional[str] = None

from __future__ import annotations

from typing import Any, Optional

from pydantic import field_validator

from api._core.models.common import ConfiguratedBaseModel, Do, Status
from api._core.utils import create_list_of_items


class Level(ConfiguratedBaseModel):
    type: str
    name: str
    status: Status
    title: str
    opt: Optional[list[Any]] = None


class Resolvers(ConfiguratedBaseModel):
    v4: list[str]
    v6: list[str]


class ThirdPartyFilter(ConfiguratedBaseModel):
    """ThirdPartyFilterItem Pydantic model definition"""

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
    do: Do
    lvl: Optional[str] = None
    status: Status


class NativeFilter(ConfiguratedBaseModel):
    """NativeFilterItem Pydantic model definition"""

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

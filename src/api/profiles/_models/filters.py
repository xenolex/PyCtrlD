from typing import Any, List, Optional

from pydantic import field_validator

from api._core import ConfiguratedBaseModel, create_list_of_items
from api.profiles._base import Do, Status


class Level(ConfiguratedBaseModel):
    type: str
    name: str
    status: Status
    title: str
    opt: Optional[List[Any]] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class Resolvers(ConfiguratedBaseModel):
    v4: List[str]
    v6: List[str]


class ThirdPartyFilter(ConfiguratedBaseModel):
    """ThirdPartyFilterItem Pydantic model definition"""

    PK: str
    additional: Optional[str] = None
    description: str
    name: str
    resolvers: Resolvers
    sources: List[str]
    status: Status

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)

    @field_validator("resolvers", mode="before")
    @classmethod
    def validate_resolvers(cls, v):
        return Resolvers.model_validate(v, strict=True)


class NativeAction(ConfiguratedBaseModel):
    do: Do
    lvl: Optional[str] = None
    status: Status

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class NativeFilter(ConfiguratedBaseModel):
    """NativeFilterItem Pydantic model definition"""

    PK: str
    action: Optional[NativeAction] = None
    additional: Optional[str] = None
    description: str
    levels: Optional[List[Level]] = None
    name: str
    sources: List[str]
    status: Status

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, v):
        if v is None:
            return None
        return NativeAction.model_validate(v, strict=True)

    @field_validator("levels", mode="before")
    @classmethod
    def validate_level(cls, v):
        if v is None:
            return None
        return create_list_of_items(model=Level, items=v)

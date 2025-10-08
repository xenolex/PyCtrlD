from typing import Any, List, Optional

from pydantic import field_validator

from api.profiles._base import ConfiguratedBaseModel, Do, Status, create_list_of_items


class LevelItem(ConfiguratedBaseModel):
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


class ThirdPartyFilterItem(ConfiguratedBaseModel):
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


class NativeActionItem(ConfiguratedBaseModel):
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


class NativeFilterItem(ConfiguratedBaseModel):
    """NativeFilterItem Pydantic model definition"""

    PK: str
    action: Optional[NativeActionItem] = None
    additional: Optional[str] = None
    description: str
    levels: Optional[List[LevelItem]] = None
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
        return NativeActionItem.model_validate(v, strict=True)

    @field_validator("levels", mode="before")
    @classmethod
    def validate_level(cls, v):
        if v is None:
            return None
        return create_list_of_items(model=LevelItem, items=v)

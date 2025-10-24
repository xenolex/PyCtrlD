from __future__ import annotations

from typing import Any, Optional

from pydantic import field_validator

from pyctrld._core.models.common import ConfiguratedBaseModel, Count, Do, Status
from pyctrld._core.utils import create_list_of_items


class Cbp(ConfiguratedBaseModel):
    custom_message: str
    no_link: int


class Data(ConfiguratedBaseModel):
    PK: str
    value: Any
    cbp: Optional[Cbp] = None


class Opt(Count):
    data: list[Data]

    @classmethod
    @field_validator("data", mode="before")
    def set_data(cls, value):
        return create_list_of_items(model=Data, items=value)


class Da(ConfiguratedBaseModel):
    do: Do
    status: Status


class Profile(ConfiguratedBaseModel):
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
    PK: str
    updated: int
    name: str
    profile: Profile
    # stats: int - https://docs.controld.com/reference/get_profiles this parameter is present in docs but absent in the API response


class Option(ConfiguratedBaseModel):
    PK: str
    title: str
    description: str
    type: str
    default_value: Any
    info_url: str

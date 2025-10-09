from typing import Any, List, Optional

from pydantic import field_validator

from api.profiles._base import ConfiguratedBaseModel, create_list_of_items
from api.profiles.constants import Do, Status


class Cbp(ConfiguratedBaseModel):
    custom_message: str
    no_link: int


class CountData(ConfiguratedBaseModel):
    count: int


class Data(ConfiguratedBaseModel):
    PK: str
    value: Any
    cbp: Optional[Cbp] = None


class OptData(ConfiguratedBaseModel):
    count: int
    data: List[Data]

    @classmethod
    @field_validator("data", mode="before")
    def validate_data(cls, v):
        return create_list_of_items(model=Data, items=v)


class DAData(ConfiguratedBaseModel):
    do: Do
    status: Status

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


class ProfileData(ConfiguratedBaseModel):
    flt: CountData
    cflt: CountData
    ipflt: CountData
    rule: CountData
    svc: CountData
    grp: CountData
    opt: OptData
    da: DAData  # https://docs.controld.com/reference/get_profiles says that "da" is an array of
    # strings and its required, but the API response with dict


class ProfileItem(ConfiguratedBaseModel):
    PK: str
    updated: int
    name: str
    profile: ProfileData
    # stats: int - https://docs.controld.com/reference/get_profiles this parameter is present in docs but absent in the API response


class OptionItem(ConfiguratedBaseModel):
    PK: str
    title: str
    description: str
    type: str
    default_value: Any
    info_url: str

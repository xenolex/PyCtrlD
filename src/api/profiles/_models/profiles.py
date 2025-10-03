from typing import List

from pydantic import BaseModel, field_validator, model_validator

from api.profiles.constants import Do, Status


class CountData(BaseModel):
    count: int


class OptItem(BaseModel):
    PK: str
    value: int


class OptData(BaseModel):
    count: int
    data: List[OptItem]


class DAData(BaseModel):
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


class ProfileData(BaseModel):
    flt: CountData
    cflt: CountData
    ipflt: CountData
    rule: CountData
    svc: CountData
    grp: CountData
    opt: OptData
    da: DAData  # https://docs.controld.com/reference/get_profiles says that "da" is an array of
    # strings and its required, but the API response with dict


class ProfileItem(BaseModel):
    PK: str
    updated: int
    name: str
    profile: ProfileData
    # stats: int - https://docs.controld.com/reference/get_profiles this parameter is present in docs but absent in the API response

    @model_validator(mode="before")
    @classmethod
    def validate_profile_item(cls, values):
        if isinstance(values, dict) and "profile" in values and isinstance(values["profile"], dict):
            profile_dict = values["profile"]

            # Process opt items
            opt_items = [
                OptItem(PK=item["PK"], value=item["value"]) for item in profile_dict["opt"]["data"]
            ]

            # Build the profile data
            profile_data = ProfileData(
                flt=CountData(count=profile_dict["flt"]["count"]),
                cflt=CountData(count=profile_dict["cflt"]["count"]),
                ipflt=CountData(count=profile_dict["ipflt"]["count"]),
                rule=CountData(count=profile_dict["rule"]["count"]),
                svc=CountData(count=profile_dict["svc"]["count"]),
                grp=CountData(count=profile_dict["grp"]["count"]),
                opt=OptData(count=profile_dict["opt"]["count"], data=opt_items),
                da=DAData(do=profile_dict["da"]["do"], status=profile_dict["da"]["status"]),
            )

            values["profile"] = profile_data

        return values


class OptionItem(BaseModel):
    PK: str
    title: str
    description: str
    type: str
    default_value: int
    info_url: str

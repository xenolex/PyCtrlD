from dataclasses import dataclass
from typing import List

from api.profiles.constants import Do, Status


@dataclass
class CountData:
    count: int


@dataclass
class OptItem:
    PK: str
    value: int


@dataclass
class OptData:
    count: int
    data: List[OptItem]


@dataclass
class DAData:
    do: Do
    status: Status

    def __init__(self, do: Do, status: Status) -> None:
        self.do = Do(do)
        self.status = Status(status)


@dataclass
class ProfileData:
    flt: CountData
    cflt: CountData
    ipflt: CountData
    rule: CountData
    svc: CountData
    grp: CountData
    opt: OptData
    da: DAData  # https://docs.controld.com/reference/get_profiles says that "da" is an array of
    # strings and its required, but the API response with dict


@dataclass
class ProfileItem:
    PK: str
    updated: int
    name: str
    profile: ProfileData
    # stats: int - https://docs.controld.com/reference/get_profiles this parameter is present in docs but absent in the API response

    def __init__(self, PK: str, updated: int, name: str, profile: dict):
        self.PK = PK
        self.updated = updated
        self.name = name

        opt_items = [OptItem(PK=item["PK"], value=item["value"]) for item in profile["opt"]["data"]]

        self.profile = ProfileData(
            flt=CountData(count=profile["flt"]["count"]),
            cflt=CountData(count=profile["cflt"]["count"]),
            ipflt=CountData(count=profile["ipflt"]["count"]),
            rule=CountData(count=profile["rule"]["count"]),
            svc=CountData(count=profile["svc"]["count"]),
            grp=CountData(count=profile["grp"]["count"]),
            opt=OptData(count=profile["opt"]["count"], data=opt_items),
            da=DAData(do=profile["da"]["do"], status=profile["da"]["status"]),
        )


@dataclass
class OptionItem:
    PK: str
    title: str
    description: str
    type: str
    default_value: int
    info_url: str

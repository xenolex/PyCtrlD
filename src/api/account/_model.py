from typing import Any, List

from api._base import ConfiguratedBaseModel
from api.profiles.constants import Status


class UserData(ConfiguratedBaseModel):
    last_active: int
    proxy_access: int
    email_status: int
    status: Status
    email: str
    date: str
    PK: str
    twofa: int
    v: int
    sso: str
    stats_endpoint: str
    debug: List[Any]

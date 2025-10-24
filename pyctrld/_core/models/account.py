from __future__ import annotations

from typing import Any

from pyctrld._core.models.common import ConfiguratedBaseModel, Status


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
    debug: list[Any]

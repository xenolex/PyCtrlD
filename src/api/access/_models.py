from __future__ import annotations

from api._base import ConfiguratedBaseModel


class Ips(ConfiguratedBaseModel):
    ip: str
    ts: int
    country: str
    city: str
    isp: str
    asn: int
    as_name: str

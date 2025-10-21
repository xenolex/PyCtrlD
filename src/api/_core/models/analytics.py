from __future__ import annotations

from api._core.models.common import ConfiguratedBaseModel


class Level(ConfiguratedBaseModel):
    PK: int
    title: str


class Endpoint(ConfiguratedBaseModel):
    PK: str
    country_code: str
    title: str

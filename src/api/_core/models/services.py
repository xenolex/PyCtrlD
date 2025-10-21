from __future__ import annotations

from typing import Optional

from api._core.models.common import ConfiguratedBaseModel


class Category(ConfiguratedBaseModel):
    PK: str
    name: str
    description: str
    count: int


class Service(ConfiguratedBaseModel):
    PK: str
    category: str
    name: str
    unlock_location: str
    locations: Optional[list[str]] = None
    warning: Optional[str] = None

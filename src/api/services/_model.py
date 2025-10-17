from __future__ import annotations

from typing import List, Optional

from api._core import ConfiguratedBaseModel


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
    locations: Optional[List[str]] = None
    warning: Optional[str] = None

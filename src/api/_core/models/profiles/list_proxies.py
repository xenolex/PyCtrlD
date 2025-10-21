from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from api._core.models.common import ConfiguratedBaseModel

if TYPE_CHECKING:
    from typing import Optional


class Proxie(ConfiguratedBaseModel):
    # Important: The response format is not documented in source doc
    PK: str
    city: str
    country: str
    country_name: str
    gps_lat: float
    gps_long: float
    uid: str
    hidden: Optional[bool] = False

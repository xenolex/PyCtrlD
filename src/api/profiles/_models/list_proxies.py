from typing import Optional

from api.profiles._base import ConfiguratedBaseModel


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

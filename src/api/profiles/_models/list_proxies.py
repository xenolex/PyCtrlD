from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProxieItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    # Important: The response format is not documented in source doc
    PK: str
    city: str
    country: str
    country_name: str
    gps_lat: float
    gps_long: float
    uid: str
    hidden: Optional[bool] = False

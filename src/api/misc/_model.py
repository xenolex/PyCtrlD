from typing import Any

from pydantic import field_validator

from api._base import ConfiguratedBaseModel


class Ip(ConfiguratedBaseModel):
    ip: str
    type: str
    org: str
    asn: int
    country: str
    handler: str
    pop: str


class Location(ConfiguratedBaseModel):
    lat: float
    long: float


class FeatureStatus(ConfiguratedBaseModel):
    api: int
    dns: int
    pxy: int


class Network(ConfiguratedBaseModel):
    iata_code: str
    city_name: str
    country_name: str
    location: Location
    status: FeatureStatus

    @field_validator("status", check_fields=False, mode="before")
    @classmethod
    def set_status(cls, value: Any) -> Any:
        return FeatureStatus.model_validate(value, strict=True)

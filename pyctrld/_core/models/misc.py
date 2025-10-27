"""Miscellaneous models for ControlD API.

This module provides data models for miscellaneous utility endpoints including
IP information and network statistics across ControlD points of presence.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import field_validator

from pyctrld._core.models.common import ConfiguratedBaseModel

if TYPE_CHECKING:
    from typing import Any


class Ip(ConfiguratedBaseModel):
    """IP information model.

    Attributes:
        ip: The IP address.
        type: IP address type.
        org: Organization/ISP name.
        asn: Autonomous System Number.
        country: Country code.
        handler: Handler/datacenter identifier.
        pop: Point of presence identifier.
    """

    ip: str
    type: str
    org: str
    asn: int
    country: str
    handler: str
    pop: str


class Location(ConfiguratedBaseModel):
    """Geographic location coordinates.

    Attributes:
        lat: Latitude coordinate.
        long: Longitude coordinate.
    """

    lat: float
    long: float


class FeatureStatus(ConfiguratedBaseModel):
    """Feature availability status at a network location.

    Attributes:
        api: API service status.
        dns: DNS service status.
        pxy: Proxy service status.
    """

    api: int
    dns: int
    pxy: int


class Network(ConfiguratedBaseModel):
    """Network point of presence (POP) information.

    Attributes:
        iata_code: IATA airport code for the location.
        city_name: City name where the POP is located.
        country_name: Country name where the POP is located.
        location: Geographic coordinates of the POP.
        status: Feature availability status at this POP.
    """

    iata_code: str
    city_name: str
    country_name: str
    location: Location
    status: FeatureStatus

    @field_validator("status", check_fields=False, mode="before")
    @classmethod
    def set_status(cls, value: dict[str, Any]) -> FeatureStatus:
        """Validate and convert status field to FeatureStatus model.

        Args:
            value: The raw status value from the API.

        Returns:
            Validated FeatureStatus model instance.
        """
        return FeatureStatus.model_validate(value, strict=True)

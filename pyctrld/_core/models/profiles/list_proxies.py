"""Proxy models for ControlD API.

This module provides data models for proxy servers that can be used for
DNS traffic redirection in custom rules and filters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pyctrld._core.models.common import ConfiguratedBaseModel

if TYPE_CHECKING:
    from typing import Optional


class Proxie(ConfiguratedBaseModel):
    """Proxy server model.

    Represents a proxy server location that can be used to redirect DNS traffic
    through different geographic locations.

    Note:
        The response format is not fully documented in the official API documentation.

    Attributes:
        PK: Primary key (unique identifier) for the proxy.
        city: City where the proxy is located.
        country: Country code where the proxy is located.
        country_name: Full country name where the proxy is located.
        gps_lat: GPS latitude coordinate of the proxy location.
        gps_long: GPS longitude coordinate of the proxy location.
        uid: Unique identifier/code for the proxy (3-letter code).
        hidden: Whether this proxy is hidden from general listing.
    """

    PK: str
    city: str
    country: str
    country_name: str
    gps_lat: float
    gps_long: float
    uid: str
    hidden: Optional[bool] = False

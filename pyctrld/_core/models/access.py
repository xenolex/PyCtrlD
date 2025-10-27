"""Access models for ControlD API.

This module provides data models for IP access control and learned IPs
that are authorized to use devices.
"""

from __future__ import annotations

from pyctrld._core.models.common import ConfiguratedBaseModel


class Ips(ConfiguratedBaseModel):
    """Model representing a learned/authorized IP address.

    Contains information about an IP address that has been authorized to
    access a device, including geolocation and ISP details.

    Attributes:
        ip: The IP address (IPv4 or IPv6).
        ts: Timestamp when the IP was learned.
        country: Country code where the IP is located.
        city: City where the IP is located.
        isp: Internet Service Provider name.
        asn: Autonomous System Number.
        as_name: Autonomous System name.
    """

    ip: str
    ts: int
    country: str
    city: str
    isp: str
    asn: int
    as_name: str

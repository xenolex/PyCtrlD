import ipaddress
import re
from typing import Optional

from pydantic import field_validator

from api._core import ConfiguratedBaseModel
from api.profiles.constants import Do, Status


class Action(ConfiguratedBaseModel):
    do: Do
    status: Status
    via: Optional[str] = None
    via_v6: Optional[str] = None

    @field_validator("do", mode="before")
    @classmethod
    def validate_do(cls, v):
        return Do(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        return Status(v)


def check_via_is_proxy_identifier(via: str | None):
    """Check that via field contains a valid 3-letter uppercase proxy identifier."""
    if not all((via is not None, str(via).isupper(), len(str(via)) == 3)):
        raise ValueError(f"via field must be a valid proxy identifier, got: {via}")


def check_via_is_record_or_cname(via: str | None):
    """Check that via field contains either a valid IPv4 address or domain name."""
    if via is None:
        raise ValueError("via field is required when do=SPOOF")

    is_ipv4 = True
    is_cname = True

    try:
        ipaddress.IPv4Address(via)
    except ipaddress.AddressValueError:
        is_ipv4 = False

    # Basic domain name validation regex
    domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(domain_pattern, via):
        is_cname = False

    if not is_ipv4 and not is_cname:
        raise ValueError(f"via field must be a valid IPv4 address or domain name, got: {via}")


def check_via_v6_is_aaaa_record(via_v6: str | None):
    """Check that via_v6 field contains a valid IPv6 address (AAAA record)."""
    if via_v6 is not None:
        try:
            ipaddress.IPv6Address(via_v6)
        except ipaddress.AddressValueError:
            raise ValueError(f"via_v6 field must be a valid IPv6 address, got: {via_v6}")

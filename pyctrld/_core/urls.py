"""ControlD API endpoint URL definitions.

This module contains the enumeration of all API endpoints used by the ControlD API client.
Each endpoint is defined as a string constant that can be used to make HTTP requests to
the ControlD API service.
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


class Endpoints(StrEnum):
    """Enumeration of ControlD API endpoint URLs.

    This enum provides type-safe access to all ControlD API endpoints.
    URLs may contain template variables (e.g., {profile_id}, {device_id})
    that should be formatted with actual values before use.
    """

    BASE = "https://api.controld.com"
    LIST_PROXIES = "https://api.controld.com/proxies"
    DEFAULT_RULE = "https://api.controld.com/profiles/{profile_id}/default"
    CUSTOM_RULES = "https://api.controld.com/profiles/{profile_id}/rules"
    RULE_FOLDERS = "https://api.controld.com/profiles/{profile_id}/groups"
    PROFILES_SERVICES = "https://api.controld.com/profiles/{profile_id}/services"
    FILTERS = "https://api.controld.com/profiles/{profile_id}/filters"
    PROFILES = "https://api.controld.com/profiles"
    DEVICES = "https://api.controld.com/devices"
    ACCESS = "https://api.controld.com/access"
    SERVICES = "https://api.controld.com/services/categories"
    ANALYTICS = "https://api.controld.com/analytics"
    ACCOUNT = "https://api.controld.com/users"
    MOBILE_CONFIG = "https://api.controld.com/mobileconfig/{device_id}"
    BILLING = "https://api.controld.com/billing"
    ORGANIZATION = "https://api.controld.com/organizations"

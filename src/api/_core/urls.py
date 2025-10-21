from __future__ import annotations

from enum import StrEnum


class Endpoints(StrEnum):
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

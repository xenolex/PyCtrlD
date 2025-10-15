from enum import Enum, StrEnum


class Endpoints(StrEnum):
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


class Do(Enum):
    BLOCK = 0
    BYPASS = 1
    SPOOF = 2
    REDIRECT = 3


class Status(Enum):
    DISABLED = 0
    ENABLED = 1

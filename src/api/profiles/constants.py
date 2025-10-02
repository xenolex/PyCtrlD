from enum import Enum

LIST_PROXIES_ENDPOINT_URL = "https://api.controld.com/proxies"
DEFAULT_RULE_ENDPOINT_URL = "https://api.controld.com/profiles/{profile_id}/default"


class Do(Enum):
    BLOCK = 0
    BYPASS = 1
    SPOOF = 2
    REDIRECT = 3


class Status(Enum):
    ENABLED = 0
    DISABLED = 1

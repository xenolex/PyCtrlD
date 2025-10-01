from enum import Enum


class Do(Enum):
    BLOCK = 0
    BYPASS = 1
    SPOOF = 2
    REDIRECT = 3


class Status(Enum):
    ENABLED = 0
    DISABLED = 1

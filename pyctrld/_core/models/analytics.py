"""Analytics models for ControlD API.

This module provides data models for analytics-related configurations including
logging levels and storage endpoints.
"""

from __future__ import annotations

from pyctrld._core.models.common import ConfiguratedBaseModel


class Level(ConfiguratedBaseModel):
    """Analytics logging level configuration.

    Attributes:
        PK: Primary key (unique identifier) for the level.
        title: Display name/title of the logging level.
    """

    PK: int
    title: str


class Endpoint(ConfiguratedBaseModel):
    """Analytics storage endpoint/region configuration.

    Attributes:
        PK: Primary key (unique identifier) for the endpoint.
        country_code: Country code where the endpoint is located.
        title: Display name/title of the storage region.
    """

    PK: str
    country_code: str
    title: str

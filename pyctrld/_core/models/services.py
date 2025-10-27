"""Services models for ControlD API.

This module provides data models for service categories and individual services
that can be used in DNS filtering rules.
"""

from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import ConfiguratedBaseModel


class Category(ConfiguratedBaseModel):
    """Service category model.

    Attributes:
        PK: Primary key (unique identifier) for the category.
        name: Category name.
        description: Category description.
        count: Number of services in this category.
    """

    PK: str
    name: str
    description: str
    count: int


class Service(ConfiguratedBaseModel):
    """Individual service model.

    Attributes:
        PK: Primary key (unique identifier) for the service.
        category: Category identifier this service belongs to.
        name: Service name.
        unlock_location: Location unlock information.
        locations: Optional list of available locations.
        warning: Optional warning message about the service.
    """

    PK: str
    category: str
    name: str
    unlock_location: str
    locations: Optional[list[str]] = None
    warning: Optional[str] = None

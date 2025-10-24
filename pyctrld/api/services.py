"""Services endpoint for ControlD API.

This module provides access to service categories and individual services
that can be used in DNS filtering rules.
"""

from __future__ import annotations

from pyctrld._core.models.services import Category, Service
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class ServicesEndpoint(BaseEndpoint):
    """Endpoint for managing service categories and services.

    This endpoint provides methods to list service categories and retrieve
    all services within a specific category. Services can be used to create
    filtering rules in DNS profiles.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Services endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.SERVICES

    def list_service_categories(self) -> list[Category]:
        """List all available service categories.

        Retrieves a list of all service categories that contain filterable
        services for DNS rules.

        Returns:
            A list of Category objects representing available service categories.

        Reference:
            https://docs.controld.com/reference/get_services-categories
        """
        return self._list(url=self._url, model=Category, key="categories")

    def list_all_services(self, category: str) -> list[Service]:
        """List all services within a specific category.

        Retrieves all services belonging to the specified category. These services
        can be used to create filtering rules in DNS profiles.

        Args:
            category: The category identifier to list services from.

        Returns:
            A list of Service objects within the specified category.

        Reference:
            https://docs.controld.com/reference/get_services-categories-category
        """

        return self._list(url=f"{self._url}/{category}", model=Service, key="services")

"""Analytics endpoint for ControlD API.

This module provides access to analytics-related functionality including
log levels and storage regions for analytics data.
"""

from __future__ import annotations

from pyctrld._core.models.analytics import Endpoint, Level
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class AnalyticsEndpoint(BaseEndpoint):
    """Endpoint for managing analytics settings and configurations.

    This endpoint provides methods to retrieve analytics log levels and
    storage region information for the ControlD service.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Analytics endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.ANALYTICS

    def list_log_levels(self) -> list[Level]:
        """Returns Analytics log levels which can be enabled on Devices.

        Retrieves the available analytics logging levels that can be configured
        on devices to control the amount of data collected.

        Returns:
            A list of Level objects representing available log levels.

        Reference:
            https://docs.controld.com/reference/get_analytics-levels
        """

        return self._list(url=self._url + "/levels", model=Level, key="levels")

    def list_storage_regions(self) -> list[Endpoint]:
        """Returns Analytics storage regions that can be set on the account or organization.

        Retrieves the available storage regions for analytics data, which can be
        configured at the account or organization level.

        Returns:
            A list of Endpoint objects representing available storage regions.

        Reference:
            https://docs.controld.com/reference/get_analytics-endpoints
        """

        return self._list(url=self._url + "/endpoints", model=Endpoint, key="endpoints")

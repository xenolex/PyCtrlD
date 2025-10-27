"""List proxies endpoint for ControlD API.

This module provides functionality for retrieving the list of available
proxy servers that can be used for DNS traffic redirection.
"""

from __future__ import annotations

from pyctrld._core.models.profiles.list_proxies import Proxie
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class ListProxiesEndpoint(BaseEndpoint):
    """Endpoint for listing available proxy servers.

    This endpoint provides methods to retrieve the list of proxy servers
    that can be used to redirect DNS traffic through different locations.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the ListProxies endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.LIST_PROXIES

    def list(self) -> list[Proxie]:
        """Returns list of usable proxies that traffic can be redirected through.

        Retrieves all available proxy servers that can be used for DNS traffic
        redirection in rules with the REDIRECT action.

        Returns:
            A list of Proxie objects representing available proxy servers.

        Reference:
            https://docs.controld.com/reference/get_proxies
        """

        return self._list(url=self._url, model=Proxie, key="proxies")

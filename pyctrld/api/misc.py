"""Miscellaneous endpoint for ControlD API.

This module provides access to utility functions including IP information
and network statistics across ControlD points of presence.
"""

from __future__ import annotations

from pyctrld._core.models.misc import Ip, Network
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class MiscEndpoint(BaseEndpoint):
    """Endpoint for miscellaneous utility functions.

    This endpoint provides access to utility methods such as retrieving
    current IP information and network statistics.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Misc endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)

        self._url = Endpoints.BASE

    def ip(self) -> Ip:
        """Returns current IP and datacenter information.

        Retrieves the current IP address and the datacenter that was used
        to handle the API request.

        Returns:
            Ip object containing IP address and datacenter information.

        Reference:
            https://docs.controld.com/reference/get_ip
        """
        data = self._request(method="GET", url=self._url + "/ip")

        return Ip.model_validate(data, strict=True)

    def network_stats(self) -> list[Network]:
        """Returns network stats on available services in different POPs.

        Retrieves network statistics and availability information for
        ControlD services across different points of presence (POPs).

        Returns:
            A list of Network objects containing statistics for each POP.

        Reference:
            https://docs.controld.com/reference/get_network
        """

        return self._list(url=self._url + "/network", model=Network, key="network")

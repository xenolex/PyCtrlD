from __future__ import annotations

from api._core.models.profiles.list_proxies import Proxie
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint


class ListProxiesEndpoint(BaseEndpoint):
    """Endpoint for listing available proxy servers."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.LIST_PROXIES

    def list(self) -> list[Proxie]:
        """Returns list of usable proxies that traffic can be redirected through.

        Returns:
            Dict[str, Any]: Response data containing available proxy information.

        Reference:
            https://docs.controld.com/reference/get_proxies
        """

        return self._list(url=self._url, model=Proxie, key="proxies")

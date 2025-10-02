from typing import Any, Dict

from api.profiles._base import BaseEndpoint


class ListProxiesEndpoint(BaseEndpoint):
    """Endpoint for listing available proxy servers."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = "https://api.controld.com/proxies"

    def list(self) -> Dict[str, Any]:
        """Returns list of usable proxies that traffic can be redirected through.

        Returns:
            Dict[str, Any]: Response data containing available proxy information.

        Reference:
            https://docs.controld.com/reference/get_proxies
        """
        # TODO: The response format is not documented, need to check it
        response = self._session.get(self._url)
        response.raise_for_status()
        return response.json()

from typing import List

from api._core import BaseEndpoint, check_response, create_list_of_items
from api.profiles._models.list_proxies import Proxie
from api.profiles.constants import Endpoints


class ListProxiesEndpoint(BaseEndpoint):
    """Endpoint for listing available proxy servers."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.LIST_PROXIES

    def list(self) -> List[Proxie]:
        """Returns list of usable proxies that traffic can be redirected through.

        Returns:
            Dict[str, Any]: Response data containing available proxy information.

        Reference:
            https://docs.controld.com/reference/get_proxies
        """

        response = self._session.get(self._url)
        check_response(response)
        data = response.json()
        # Important: The response format is not documented in source doc
        return create_list_of_items(Proxie, data["body"]["proxies"])

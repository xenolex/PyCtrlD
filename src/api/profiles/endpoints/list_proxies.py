from typing import List

from api.profiles._base import BaseEndpoint, check_response
from api.profiles._models.list_proxies import ProxieItem
from api.profiles.constants import LIST_PROXIES_ENDPOINT_URL


class ListProxiesEndpoint(BaseEndpoint):
    """Endpoint for listing available proxy servers."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = LIST_PROXIES_ENDPOINT_URL

    def list(self) -> List[ProxieItem]:
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
        return [ProxieItem.model_validate(item, strict=True) for item in data["body"]["proxies"]]

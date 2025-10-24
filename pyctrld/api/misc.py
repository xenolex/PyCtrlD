from __future__ import annotations

from pyctrld._core.models.misc import Ip, Network
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class MiscEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)

        self._url = Endpoints.BASE

    def ip(self) -> Ip:
        """
        Returns current IP and datacenter that was used to handle the API request.
        Reference:
            https://docs.controld.com/reference/get_ip
        """
        data = self._request(method="GET", url=self._url + "/ip")

        return Ip.model_validate(data, strict=True)

    def network_stats(self) -> list[Network]:
        """
        Returns network stats on available services in different POPs.
        Reference:
            https://docs.controld.com/reference/get_network
        """

        return self._list(url=self._url + "/network", model=Network, key="network")

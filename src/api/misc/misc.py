from api._base import BaseEndpoint, check_response, create_list_of_items
from api.misc._model import Ip, Network
from api.profiles.constants import Endpoints


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

        url = self._url + "/ip"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return Ip.model_validate(data["body"], strict=True)

    def network_stats(self) -> list[Network]:
        """
        Returns network stats on available services in different POPs.
        Reference:
            https://docs.controld.com/reference/get_network
        """

        url = self._url + "/network"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Network, data["body"]["network"])

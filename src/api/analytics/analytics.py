from typing_extensions import List

from api._base import BaseEndpoint, check_response, create_list_of_items
from api.analytics._model import Endpoint, Level
from api.profiles.constants import Endpoints


class AnalyticsEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.ANALYTICS

    def list_log_levels(self) -> List[Level]:
        """Returns Analytics log levels which can be enabled on Devices.
        https://docs.controld.com/reference/get_analytics-levels
        """
        url = self._url + "/levels"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Level, data["body"]["levels"])

    def list_storage_regions(self) -> List[Endpoint]:
        """Returns Analytics storage regions that can be set on the account or organization.

        https://docs.controld.com/reference/get_analytics-endpoints
        """

        url = self._url + "/endpoints"
        response = self._session.get(url)
        check_response(response)
        data = response.json()

        return create_list_of_items(Endpoint, data["body"]["endpoints"])

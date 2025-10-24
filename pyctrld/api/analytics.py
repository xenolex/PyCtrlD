from __future__ import annotations

from pyctrld._core.models.analytics import Endpoint, Level
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class AnalyticsEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.ANALYTICS

    def list_log_levels(self) -> list[Level]:
        """Returns Analytics log levels which can be enabled on Devices.
        https://docs.controld.com/reference/get_analytics-levels
        """

        return self._list(url=self._url + "/levels", model=Level, key="levels")

    def list_storage_regions(self) -> list[Endpoint]:
        """Returns Analytics storage regions that can be set on the account or organization.

        https://docs.controld.com/reference/get_analytics-endpoints
        """

        return self._list(url=self._url + "/endpoints", model=Endpoint, key="endpoints")

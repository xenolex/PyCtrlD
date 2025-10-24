from __future__ import annotations

from pyctrld._core.models.account import UserData
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class AccountEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.ACCOUNT

    def user_data(self) -> UserData:
        """
        https://docs.controld.com/reference/get_users
        """
        data = self._request(method="GET", url=self._url)
        return UserData.model_validate(data, strict=True)

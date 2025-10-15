from api._base import BaseEndpoint, check_response
from api.account._model import UserData
from api.profiles.constants import Endpoints


class AccountEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.ACCOUNT

    def user_data(self) -> UserData:
        """
        https://docs.controld.com/reference/get_users
        """
        response = self._session.get(self._url)
        check_response(response)

        data = response.json()

        return UserData.model_validate(data["body"], strict=True)

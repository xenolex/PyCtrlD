from typing_extensions import List

from api._core import BaseEndpoint, check_response, create_list_of_items
from api.profiles.constants import Endpoints
from api.services._model import Category, Service


class ServicesEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.SERVICES

    def list_service_categories(self) -> List[Category]:
        """
        https://docs.controld.com/reference/get_services-categories
        """
        response = self._session.get(self._url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Category, data["body"]["categories"])

    def list_all_services(self, category: str) -> List[Service]:
        """
        https://docs.controld.com/reference/get_services-categories-category
        """

        url = f"{self._url}/{category}"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Service, data["body"]["services"])

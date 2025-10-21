from __future__ import annotations

from api._core.models.services import Category, Service
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint, check_response, create_list_of_items


class ServicesEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.SERVICES

    def list_service_categories(self) -> list[Category]:
        """
        https://docs.controld.com/reference/get_services-categories
        """
        response = self._session.get(self._url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Category, data["body"]["categories"])

    def list_all_services(self, category: str) -> list[Service]:
        """
        https://docs.controld.com/reference/get_services-categories-category
        """

        url = f"{self._url}/{category}"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return create_list_of_items(Service, data["body"]["services"])

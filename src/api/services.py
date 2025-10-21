from __future__ import annotations

from api._core.models.services import Category, Service
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint


class ServicesEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.SERVICES

    def list_service_categories(self) -> list[Category]:
        """
        https://docs.controld.com/reference/get_services-categories
        """
        return self._list(url=self._url, model=Category, key="categories")

    def list_all_services(self, category: str) -> list[Service]:
        """
        https://docs.controld.com/reference/get_services-categories-category
        """

        return self._list(url=f"{self._url}/{category}", model=Service, key="services")

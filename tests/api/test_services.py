from __future__ import annotations

import sys
from pprint import pprint

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.models.services import Category, Service
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.services import ServicesEndpoint
from tests.api.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")


class TestAccessEndpoint:
    """Test the AccessEndpoint class."""

    api = ServicesEndpoint(token)

    def test_list_service_categories(self):
        check_api_list_endpoint(
            self.api,
            model=Category,
            method_name="list_service_categories",
        )

    def test_list_all_services(self):
        for category in self.api.list_service_categories():
            check_api_list_endpoint(
                self.api,
                model=Service,
                method_name="list_all_services",
                api_kwargs={"category": category.PK},
            )

    def test_list_all_services_not_changed(self):
        api = BaseEndpoint(token)
        for cat in self.api.list_service_categories():
            response = api.get_raw_response(Endpoints.SERVICES + f"/{cat.PK}")

            data = response.json()
            items = data["body"]["services"]
            for category in items:
                pprint(category)
                for key in category:
                    check_key_in_model(key, Service)


def test_list_service_categories_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.SERVICES)

    data = response.json()
    items = data["body"]["categories"]
    for category in items:
        pprint(category)
        for key in category:
            check_key_in_model(key, Category)

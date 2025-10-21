from __future__ import annotations

import sys
from pprint import pprint

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.models.analytics import Endpoint, Level
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.analytics import AnalyticsEndpoint
from tests.api.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")
test_device_id = os.getenv("TEST_DEVICE_ID", "")
test_device_id2 = os.getenv("TEST_DEVICE_ID2", "")


class TestAnalyticsEndpoint:
    """Test the AnalyticsEndpoint class."""

    api = AnalyticsEndpoint(token)

    def test_list_log_levels(self):
        check_api_list_endpoint(
            self.api,
            model=Level,
            method_name="list_log_levels",
        )

    def test_list_storage_regions(self):
        check_api_list_endpoint(
            self.api,
            model=Endpoint,
            method_name="list_storage_regions",
        )


def test_list_log_levels_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.ANALYTICS + "/levels")

    data = response.json()
    items = data["body"]["levels"]
    for ip in items:
        pprint(ip)
        for key in ip:
            check_key_in_model(key, Level)


def test_list_storage_regions_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.ANALYTICS + "/endpoints")

    data = response.json()
    items = data["body"]["endpoints"]
    for ip in items:
        pprint(ip)
        for key in ip:
            check_key_in_model(key, Endpoint)

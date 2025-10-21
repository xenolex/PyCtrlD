from __future__ import annotations

import sys
from pprint import pprint

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.models.access import Ips
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.access import AccessEndpoint, AccessFormData
from tests.api.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")
test_device_id = os.getenv("TEST_DEVICE_ID", "")
test_device_id2 = os.getenv("TEST_DEVICE_ID2", "")


class TestAccessEndpoint:
    """Test the AccessEndpoint class."""

    api = AccessEndpoint(token)
    test_ips = ["8.8.8.8", "1.1.1.1"]

    def test_list_known_ips(self):
        check_api_list_endpoint(
            self.api,
            model=Ips,
            method_name="list_known_ips",
            api_kwargs={"device_id": test_device_id},
        )

    def test_learn_new_ip(self):
        form_data = AccessFormData(ips=self.test_ips, device_id=test_device_id2)
        assert self.api.learn_new_ip(form_data)

    def test_delete_learned_ip(self):
        form_data = AccessFormData(ips=self.test_ips, device_id=test_device_id2)
        assert self.api.delete_learned_ip(form_data)


def test_list_known_ips_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.ACCESS, params={"device_id": test_device_id})

    data = response.json()
    items = data["body"]["ips"]
    for ip in items:
        pprint(ip)
        for key in ip:
            check_key_in_model(key, Ips)

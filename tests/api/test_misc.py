from __future__ import annotations

import sys

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.logger import logger
from api._core.models.misc import FeatureStatus, Ip, Location, Network
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.misc import MiscEndpoint
from tests.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")


class TestMiscEndpoint:
    """Test the BillingEndpoint class."""

    api = MiscEndpoint(token)

    def test_ip(self):
        assert self.api.ip()

    def test_network_stats(self):
        check_api_list_endpoint(self.api, Network, method_name="network_stats")


def test_ip_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.BASE + "/ip")

    data = response.json()
    item = data["body"]
    assert Ip.model_validate(item, strict=True)
    for key in item:
        check_key_in_model(key, Ip)


def test_network_stats_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.BASE + "/network")

    data = response.json()
    items = data["body"]["network"]
    for network in items:
        logger.info(network)
        for key in network:
            check_key_in_model(key, Network)
            if key == "location" and network[key] is not None:
                for l_key in network[key]:
                    check_key_in_model(l_key, Location)
            if key == "status" and network[key] is not None:
                for s_key in network[key]:
                    check_key_in_model(s_key, FeatureStatus)

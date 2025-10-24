from __future__ import annotations

import os

from dotenv import load_dotenv

from pyctrld._core.logger import logger
from pyctrld._core.models.profiles.list_proxies import Proxie
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint
from pyctrld.api.profiles.list_proxies import ListProxiesEndpoint
from tests.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")


def test_list_proxies_serialization():
    check_api_list_endpoint(ListProxiesEndpoint(token), model=Proxie)


def test_list_proxies_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.LIST_PROXIES)
    data = response.json()
    proxies = data["body"]["proxies"]
    for proxie_item in proxies:
        logger.info(proxie_item)
        for key in proxie_item:
            check_key_in_model(key, Proxie)

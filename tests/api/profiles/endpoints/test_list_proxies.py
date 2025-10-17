import sys

sys.path.extend(["./", "./src/"])


import os
from pprint import pprint

from dotenv import load_dotenv

from api._core import BaseEndpoint
from api.profiles._models.list_proxies import Proxie
from api.profiles.constants import Endpoints
from api.profiles.endpoints.list_proxies import ListProxiesEndpoint
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

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
        pprint(proxie_item)
        for key in proxie_item:
            check_key_in_model(key, Proxie)

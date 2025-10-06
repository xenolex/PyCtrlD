import sys

sys.path.append("./")
sys.path.append("./src/")


import os
from pprint import pprint

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.list_proxies import ProxieItem
from api.profiles.constants import LIST_PROXIES_ENDPOINT_URL
from api.profiles.endpoints.list_proxies import ListProxiesEndpoint
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")


def test_list_proxies_serialization():
    check_api_list_endpoint(ListProxiesEndpoint(token), model=ProxieItem)


def test_list_proxies_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(LIST_PROXIES_ENDPOINT_URL)
    data = response.json()
    proxies = data["body"]["proxies"]
    for proxie_item in proxies:
        pprint(proxie_item)
        for key in proxie_item:
            check_key_in_model(key, ProxieItem)

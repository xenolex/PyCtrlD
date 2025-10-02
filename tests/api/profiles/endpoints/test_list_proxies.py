import os
import sys

sys.path.append("./src/")

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.list_proxies import ProxieItem
from api.profiles.constants import LIST_PROXIES_ENDPOINT_URL
from api.profiles.endpoints.list_proxies import ListProxiesEndpoint

load_dotenv()
token = os.environ.get("TOKEN", "")


def test_list_proxies_serialization():
    api = ListProxiesEndpoint(token)
    proxies = api.list()
    item_to_check = proxies[-1]
    assert isinstance(item_to_check, ProxieItem)


def test_list_proxies_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(LIST_PROXIES_ENDPOINT_URL)
    data = response.json()
    proxies = data["body"]["proxies"]
    for proxie_item in proxies:
        for key in proxie_item:
            assert key in ProxieItem.__match_args__, (  # ty: ignore[unresolved-attribute]
                f"Key '{key}' not found in 'ProxieItem' class\n {proxie_item}"
            )

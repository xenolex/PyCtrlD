import sys

sys.path.extend(["./", "./src/"])

import os
from pprint import pprint

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.filters import (
    LevelItem,
    NativeActionItem,
    NativeFilterItem,
    Resolvers,
    ThirdPartyFilterItem,
)
from api.profiles.constants import FILTERS_ENDPOINT_URL, Status
from api.profiles.endpoints.filters import (
    FiltersEndpoint,
    ModifyFilterFormData,
)
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestFilters:
    api = FiltersEndpoint(token)

    def test_list_native(self):
        check_api_list_endpoint(
            api=self.api,
            model=NativeFilterItem,
            api_kwargs={"profile_id": profile_id},
            method_name="list_native",
        )

    def test_list_third_party(self):
        check_api_list_endpoint(
            api=self.api,
            model=ThirdPartyFilterItem,
            api_kwargs={"profile_id": profile_id},
            method_name="list_third_party",
        )

    def test_modify(self):
        filter = self.api.list_native(profile_id)[-1]
        for status in [Status.ENABLED, Status.DISABLED]:
            form_data = ModifyFilterFormData(status=status)
            modifed_data = self.api.modify(profile_id, filter.PK, form_data=form_data)

            modifed_filter = modifed_data.get(filter.PK)
            pprint(modifed_filter)
            if status == Status.DISABLED:
                assert modifed_filter is None
            else:
                assert status == modifed_filter.status  # type: ignore

                if filter.action is not None:
                    assert filter.action.do == modifed_filter.do  # type: ignore
                    assert filter.action.status != modifed_filter.status  # type: ignore

                assert filter.status != modifed_filter.status  # type: ignore


def test_list_native_filters_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(FILTERS_ENDPOINT_URL.format(profile_id=profile_id))

    data = response.json()
    items = data["body"]["filters"]

    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, NativeFilterItem)
            if key == "action":
                for k in item[key]:
                    check_key_in_model(k, NativeActionItem)
            if key == "levels":
                for level in item[key]:
                    for k in level:
                        check_key_in_model(k, LevelItem)


def test_list_third_party_filters_not_changed():
    api = BaseEndpoint(token)
    url = FILTERS_ENDPOINT_URL.format(profile_id=profile_id)
    response = api.get_raw_response(url + "/external")

    data = response.json()
    items = data["body"]["filters"]

    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, ThirdPartyFilterItem)
            if key == "resolvers":
                for k in item[key]:
                    check_key_in_model(k, Resolvers)

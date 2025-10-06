import sys

sys.path.append("./")
sys.path.append("./src/")

import os
from pprint import pprint
from random import randint

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.custom_rules import CustomRuleItem, CustomRulesActionItem
from api.profiles.constants import CUSTOM_RULES_ENDPOINT_URL, Do, Status
from api.profiles.endpoints.custom_rules import (
    CreateCustomRuleFormData,
    CustomRulesEndpoint,
    ListCustomRuleItem,
    ModifyCustomRuleFormData,
)
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestDefaultRule:
    api = CustomRulesEndpoint(token)
    prefix = "create_site"

    def test_list(self):
        check_api_list_endpoint(
            self.api, model=ListCustomRuleItem, api_kwargs={"profile_id": profile_id}
        )

        check_api_list_endpoint(
            self.api,
            model=ListCustomRuleItem,
            api_kwargs={"profile_id": profile_id, "folder_id": 1},
        )

    def test_create(self):
        data = [
            {
                "do": Do.BLOCK,
                "status": Status.ENABLED,
                "hostnames": [f"{self.prefix}{randint(0, 999999)}.com"],
                "via": "127.0.0.1",
                "via_v6": "::1",
                "group": 0,
            },
            {
                "do": Do.BYPASS,
                "status": Status.ENABLED,
                "hostnames": [f"{self.prefix}{randint(0, 999999)}.com"],
                "via": "127.0.0.1",
                "via_v6": "::1",
                "group": 0,
            },
            {
                "do": Do.SPOOF,
                "status": Status.ENABLED,
                "hostnames": [f"{self.prefix}{randint(0, 999999)}.com"],
                "via": "127.0.0.1",
                "via_v6": "::1",
                "group": 0,
            },
            {
                "do": Do.REDIRECT,
                "status": Status.ENABLED,
                "hostnames": [f"{self.prefix}{randint(0, 999999)}.com"],
                "via": "JFK",
                "group": 0,
            },
        ]
        for item in data:
            form_data = CreateCustomRuleFormData.model_validate(item)
            created_rule = self.api.create(profile_id, form_data)

            pprint(created_rule)

            assert item["do"] == created_rule[-1].do
            assert item["status"] == created_rule[-1].status
            assert item["group"] == created_rule[-1].group

            for key in created_rule[-1].model_dump():
                check_key_in_model(key, CustomRuleItem)

    def test_modify(self):
        present_data = self.api.list(profile_id)
        for item in present_data:
            if item.PK.startswith(self.prefix):
                form_data = ModifyCustomRuleFormData(status=Status.DISABLED, hostnames=[item.PK])
                modifed_data = self.api.modify(profile_id, form_data)

                pprint(modifed_data)

                assert item.action.do == modifed_data[-1].do
                assert item.action.status != modifed_data[-1].status
                assert item.order == modifed_data[-1].order
                assert item.group == modifed_data[-1].group
                for key in modifed_data[-1].model_dump():
                    check_key_in_model(key, CustomRuleItem)

    def test_delete(self):
        present_data = self.api.list(profile_id)
        for item in present_data:
            if item.PK.startswith("create_site"):
                assert self.api.delete(profile_id, item.PK)

        present_data = self.api.list(profile_id)
        for item in present_data:
            assert not item.PK.startswith("create_site")


def test_list_custom_rules_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(CUSTOM_RULES_ENDPOINT_URL.format(profile_id=profile_id))

    data = response.json()
    items = data["body"]["rules"]

    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, ListCustomRuleItem)
            if key == "action":
                for k in item[key]:
                    check_key_in_model(k, CustomRulesActionItem)

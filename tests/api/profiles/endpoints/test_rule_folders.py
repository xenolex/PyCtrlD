import sys

sys.path.append("./")
sys.path.append("./src/")

import os
from pprint import pprint
from random import randint

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.rule_folders import RuleFolderActionItem, RuleFolderItem
from api.profiles.constants import RULE_FOLDERS_ENDPOINT_URL, Do, Status
from api.profiles.endpoints.rule_folders import (
    CreateRuleFoldersFormData,
    RuleFoldersEndpoint,
    RuleFoldersFormData,
)
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestRuleFolders:
    api = RuleFoldersEndpoint(token)
    prefix = "create_folder"

    def test_list(self):
        check_api_list_endpoint(
            api=self.api, model=RuleFolderItem, api_kwargs={"profile_id": profile_id}
        )

    def test_create(self):
        data = [
            {
                "do": Do.BLOCK,
                "status": Status.ENABLED,
                "name": f"{self.prefix}{randint(0, 999999)}.com",
                "via": "127.0.0.1",
                "via_v6": "::1",
            },
            {
                "do": Do.BYPASS,
                "status": Status.ENABLED,
                "name": f"{self.prefix}{randint(0, 999999)}.com",
                "via": "127.0.0.1",
                "via_v6": "::1",
            },
            {
                "do": Do.SPOOF,
                "status": Status.ENABLED,
                "name": f"{self.prefix}{randint(0, 999999)}.com",
                "via": "127.0.0.1",
                "via_v6": "::1",
            },
            {
                "do": Do.REDIRECT,
                "status": Status.ENABLED,
                "name": f"{self.prefix}{randint(0, 999999)}.com",
                "via": "JFK",
            },
        ]
        for item in data:
            form_data = CreateRuleFoldersFormData.model_validate(item)
            created_folder = self.api.create(profile_id, form_data)

            pprint(created_folder)

            for folder in created_folder:
                assert folder.action.do == form_data.do
                assert folder.action.status == form_data.status
                assert folder.group == form_data.name
                assert folder.count == 0

                for key in folder.model_dump():
                    check_key_in_model(key, RuleFolderItem)
                    if key == "action":
                        action_item = folder.model_dump()[key]
                        for k in action_item:
                            check_key_in_model(k, RuleFolderActionItem)

    def test_modify(self):
        present_data = self.api.list(profile_id)
        for item in present_data:
            if item.group.startswith(self.prefix):
                form_data = RuleFoldersFormData(status=Status.DISABLED)
                modifed_data = self.api.modify(profile_id, item.PK, form_data)

                pprint(modifed_data)

                assert item.PK == modifed_data[-1].PK
                assert item.group == modifed_data[-1].group
                assert item.count == modifed_data[-1].count
                assert item.action.do == modifed_data[-1].action.do
                assert Status.DISABLED == modifed_data[-1].action.status

                for key in modifed_data[-1].model_dump():
                    check_key_in_model(key, RuleFolderItem)
                    if key == "action":
                        action_item = modifed_data[-1].model_dump()[key]
                        for k in action_item:
                            check_key_in_model(k, RuleFolderActionItem)

    def test_delete(self):
        present_data = self.api.list(profile_id)
        for item in present_data:
            if item.group.startswith(self.prefix):
                assert self.api.delete(profile_id, item.PK)

        present_data = self.api.list(profile_id)
        for item in present_data:
            assert not item.group.startswith(self.prefix)


def test_list_custom_rules_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(RULE_FOLDERS_ENDPOINT_URL.format(profile_id=profile_id))

    data = response.json()
    items = data["body"]["groups"]

    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, RuleFolderItem)
            if key == "action":
                for k in item[key]:
                    check_key_in_model(k, RuleFolderActionItem)

import os
import sys

sys.path.append("./src/")

from dotenv import load_dotenv

from api.profiles._base import Status
from api.profiles.endpoints.custom_rules import (
    CustomRulesEndpoint,
    ModifyCustomRuleFormData,
)

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestDefaultRule:
    api = CustomRulesEndpoint(token)
    to_delete = []
    # @pytest.fixture
    # def current_default_rule_settings(self):
    #     data = self.api.list(profile_id)
    #     yield data
    #     self.api.modify(
    #         profile_id,
    #         CustomRuleFormData(do=data.do, status=data.status, via=data.via),
    #     )

    # def test_list(self):
    #     root_rules = self.api.list(profile_id)
    #     for rule in root_rules:
    #         pprint(rule)
    #         assert isinstance(rule, ListCustomRuleItem)

    #     foldered_rules = self.api.list(profile_id, folder_id=1)
    #     for foldered_rule in foldered_rules:
    #         pprint(foldered_rule)
    #         assert isinstance(foldered_rule, ListCustomRuleItem)

    # def test_create(self):
    #     prefix = "create_site"
    #     data = [
    #         {
    #             "do": Do.BLOCK,
    #             "status": Status.ENABLED,
    #             "hostnames": [f"{prefix}{randint(0, 999999)}.com"],
    #             "via": "127.0.0.1",
    #             "via_v6": "::1",
    #             "group": 0,
    #         },
    #         {
    #             "do": Do.BYPASS,
    #             "status": Status.ENABLED,
    #             "hostnames": [f"{prefix}{randint(0, 999999)}.com"],
    #             "via": "127.0.0.1",
    #             "via_v6": "::1",
    #             "group": 0,
    #         },
    #         {
    #             "do": Do.SPOOF,
    #             "status": Status.ENABLED,
    #             "hostnames": [f"{prefix}{randint(0, 999999)}.com"],
    #             "via": "127.0.0.1",
    #             "via_v6": "::1",
    #             "group": 0,
    #         },
    #         {
    #             "do": Do.REDIRECT,
    #             "status": Status.ENABLED,
    #             "hostnames": [f"{prefix}{randint(0, 999999)}.com"],
    #             "via": "JFK",
    #             "group": 0,
    #         },
    #     ]
    #     for item in data:
    #         form_data = CustomRuleFormData.model_validate(item)
    #         created_rule = self.api.create(profile_id, form_data)

    #         pprint(created_rule)

    #         assert item["do"] == form_data.do
    #         assert item["status"] == form_data.status
    #         assert item["group"] == form_data.group

    #         for key in created_rule[-1].model_dump():
    #             assert key in CreatedCustomRuleItem.model_fields, (
    #                 f"Key '{key}' not found in 'CreatedCustomRuleItem' class\n {created_rule[-1]}"
    #             )

    def test_modify(self):
        present_data = self.api.list(profile_id)
        breakpoint()
        for item in present_data:
            if item.PK.startswith("create_site"):
                form_data = ModifyCustomRuleFormData(status=Status.DISABLED, hostnames=[item.PK])
                modifed_data = self.api.modify(profile_id, form_data)

        assert preset_data.do != modifed_data.do
        assert preset_data.status == modifed_data.status
        assert preset_data.via == modifed_data.via


# def test_list_custom_rules_not_changed():
#     api = BaseEndpoint(token)
#     response = api.get_raw_response(CUSTOM_RULES_ENDPOINT_URL.format(profile_id=profile_id))

#     data = response.json()
#     items = data["body"]["rules"]

#     for item in items:
#         pprint(item)
#         for key in item:
#             assert key in ListCustomRuleItem.model_fields, (
#                 f"Key '{key}' not found in 'ListCustomRuleItem' class\n {item}"
#             )
#             if key == "action":
#                 for k in item[key]:
#                     assert k in CustomRulesActionItem.model_fields, (
#                         f"Key '{k}' not found in 'ActionItem' class\n {item}"
#                     )

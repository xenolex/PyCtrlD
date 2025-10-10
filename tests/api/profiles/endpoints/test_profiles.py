import sys

sys.path.extend(["./", "./src/"])

import os
from pprint import pprint
from random import randint

from dotenv import load_dotenv

from api.profiles._base import BaseEndpoint
from api.profiles._models.profiles import (
    Count,
    Option,
    Profile,
    ProfileObject,
    Da,
    Opt,
    Data,
    Cbp,
)
from api.profiles.constants import PROFILES_ENDPOINT_URL, Status
from api.profiles.endpoints.profiles import (
    CreateProfileFormData,
    ModifyOptionFormData,
    ModifyProfileFormData,
    ProfilesEndpoint,
)
from tests.api.profiles.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")


class TestProfiles:
    api = ProfilesEndpoint(token)
    to_delete = []
    default_name = "Developer Profile"

    def test_list(self):
        check_api_list_endpoint(self.api, model=ProfileObject)

    def test_create(self):
        name = "test"
        form_data = CreateProfileFormData(name=name)
        created_profile = self.api.create(form_data)[-1]
        self.to_delete.append(created_profile.PK)

        assert name == created_profile.name

        form_data = CreateProfileFormData(clone_profile_id=profile_id)
        created_profile = self.api.create(form_data)[-1]
        self.to_delete.append(created_profile.PK)

        assert created_profile.name.startswith(self.default_name)

    def test_modify(self):
        name = f"test_{randint(0, 99999)}"
        form_data = ModifyProfileFormData(name=name)
        updated_profile = self.api.modify(profile_id, form_data)[-1]

        assert name == updated_profile.name

        form_data = ModifyProfileFormData(name=self.default_name)
        updated_profile = self.api.modify(profile_id, form_data)[-1]

        assert self.default_name == updated_profile.name

    def test_delete(self):
        for to_delete_id in self.to_delete:
            assert self.api.delete(to_delete_id)

    def test_list_options(self):
        check_api_list_endpoint(self.api, Option, method_name="list_options")

    def test_modify_option(self):
        for status in [Status.ENABLED, Status.DISABLED]:
            for option in self.api.list_options():
                if isinstance(option.default_value, int):
                    form_data = ModifyOptionFormData(status=status)
                    updated_option = self.api.modify_options(profile_id, option.PK, form_data)[-1]

                    assert status.value == updated_option.value


def test_list_profiles_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(PROFILES_ENDPOINT_URL)

    data = response.json()
    items = data["body"]["profiles"]

    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, ProfileObject)
            if key == "profile":
                p = item[key]
                for k in p:
                    check_key_in_model(k, Profile)

                    pd = p[k]

                    match k:
                        case "opt":
                            model = Opt
                            for item in pd["data"]:
                                for kkk in item:
                                    check_key_in_model(kkk, Data)
                                    if kkk == "cbp":
                                        for kkkk in item[kkk]:
                                            check_key_in_model(kkkk, Cbp)
                        case "da":
                            model = Da
                        case _:
                            model = Count
                    for kk in pd:
                        check_key_in_model(kk, model)


def test_list_options_profiles_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(PROFILES_ENDPOINT_URL + "/options")

    data = response.json()
    items = data["body"]["options"]
    for item in items:
        pprint(item)
        for key in item:
            check_key_in_model(key, Option)

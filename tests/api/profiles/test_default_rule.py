from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

from pyctrld._core.logger import logger
from pyctrld._core.models.common import Action, Do, Status
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint
from pyctrld.api.profiles.default_rule import DefaultRuleEndpoint, DefaultRuleFormData
from tests.checks import check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestDefaultRule:
    api = DefaultRuleEndpoint(token)

    @pytest.fixture
    def current_default_rule_settings(self):
        data = self.api.list(profile_id)
        yield data
        self.api.modify(
            profile_id,
            DefaultRuleFormData(do=data.do, status=data.status, via=data.via),
        )

    def test_list(self):
        default = self.api.list(profile_id)
        logger.info(default)
        assert isinstance(default, Action)

    def test_modify(self, current_default_rule_settings):
        preset_data = current_default_rule_settings

        form_data = DefaultRuleFormData(do=Do.BLOCK, status=Status.ENABLED)
        modifed_data = self.api.modify(profile_id, form_data)

        assert preset_data.do != modifed_data.do
        assert preset_data.status == modifed_data.status
        assert preset_data.via == modifed_data.via


def test_list_default_rule_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.DEFAULT_RULE.format(profile_id=profile_id))
    data = response.json()
    default = data["body"]["default"]
    for key in default:
        check_key_in_model(key, Action)

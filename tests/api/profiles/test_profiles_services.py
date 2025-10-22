from __future__ import annotations

import sys

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api._core.logger import logger
from api._core.models.common import Action, Status
from api._core.models.profiles.services import Service
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint
from api.profiles.services import (
    ModifyServiceFormData,
    ServicesEndpoint,
)
from tests.checks import check_api_list_endpoint, check_key_in_model

load_dotenv()
token = os.environ.get("TOKEN", "")
profile_id = os.environ.get("TEST_PROFILE_ID", "")


class TestServices:
    api = ServicesEndpoint(token)

    def test_list(self):
        check_api_list_endpoint(api=self.api, model=Service, api_kwargs={"profile_id": profile_id})

    def test_modify(self):
        for service in self.api.list(profile_id):
            for status in [Status.DISABLED, Status.ENABLED]:
                form_data = ModifyServiceFormData(status=status)
                modifed_data = self.api.modify(profile_id, service=service.PK, form_data=form_data)

                logger.info(modifed_data)

                assert service.action.do == modifed_data[-1].do
                assert status == modifed_data[-1].status

                for key in modifed_data[-1].model_dump():
                    check_key_in_model(key, Action)


def test_list_rule_folders_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.PROFILES_SERVICES.format(profile_id=profile_id))

    data = response.json()
    items = data["body"]["services"]

    for item in items:
        logger.info(item)
        for key in item:
            check_key_in_model(key, Service)
            if key == "action":
                for k in item[key]:
                    check_key_in_model(k, Action)

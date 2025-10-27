from __future__ import annotations

import os

from dotenv import load_dotenv

from pyctrld._core.logger import logger
from pyctrld._core.models.account import UserData
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint
from pyctrld.api.account import AccountEndpoint
from tests.checks import check_key_in_model

load_dotenv()
token = os.getenv("TOKEN", "")


class TestAccountEndpoint:
    api = AccountEndpoint(token)

    def test_user_data(self):
        account = self.api.user_data()
        assert isinstance(account, UserData), (
            f"Api returns items is not an instance of {UserData.__name__}"
        )


def test_user_data_not_changed():
    api = BaseEndpoint(token)
    response = api.get_raw_response(Endpoints.ACCOUNT)

    data = response.json()
    account = data["body"]
    logger.info(account)
    for key in account:
        check_key_in_model(key, UserData)

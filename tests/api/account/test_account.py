import sys

sys.path.extend(["./", "./src/"])

import os
from pprint import pprint

from dotenv import load_dotenv

from api._base import BaseEndpoint
from api.account._model import UserData
from api.account.account import AccountEndpoint
from api.profiles.constants import Endpoints
from tests.api.profiles.checks import check_key_in_model

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
    pprint(account)
    for key in account:
        check_key_in_model(key, UserData)

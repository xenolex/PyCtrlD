import os
import sys

from dotenv import load_dotenv

sys.path.append("./src/")
from api.profiles.profiles import ProfilesApi

load_dotenv()


class TestProfiles:
    api = ProfilesApi(os.getenv("TOKEN", ""))

    def test_list(self):
        profiles = self.api.list()
        assert isinstance(profiles, list)

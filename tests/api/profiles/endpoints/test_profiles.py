import sys

sys.path.extend(["./", "./src/"])

import os

from dotenv import load_dotenv

from api.profiles.endpoints.profiles import ProfilesEndpoint

load_dotenv()
token = os.getenv("TOKEN", "")


class TestProfiles:
    api = ProfilesEndpoint(token)

    def test_list(self):
        profiles = self.api.list()

        assert isinstance(profiles, list)


if __name__ == "__main__":
    api = ProfilesEndpoint(token)
    profiles = api.list()

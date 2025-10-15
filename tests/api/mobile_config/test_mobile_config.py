import sys

sys.path.extend(["./", "./src/"])

import os
import shutil

from dotenv import load_dotenv

from api.mobile_config.mobile_config import MobileConfigEndpoint

load_dotenv()
token = os.getenv("TOKEN", "")
profile_id = os.getenv("TEST_PROFILE_ID", "")
test_device_id = os.getenv("TEST_DEVICE_ID", "")
test_device_id2 = os.getenv("TEST_DEVICE_ID2", "")


class TestMobileConfigEndpoint:
    """Test the MobileConfigEndpoint class."""

    api = MobileConfigEndpoint(token)

    def test_generate_profile(self):
        dir = "tmp"
        path = dir + "/mc.mobileconfig"
        file = self.api.generate_profile(
            device_id=test_device_id,
            filepath=path,
            exclude_wifi=["wifi1", "wifi2"],
            exclude_domain=["domain1", "domain2"],
            dont_sign=False,
            exclude_common=False,
            client_id="test_client",
        )

        assert file.exists()

        shutil.rmtree(dir)

        assert not file.exists()

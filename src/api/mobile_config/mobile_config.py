from pathlib import Path

from api._base import BaseEndpoint, check_response
from api.profiles.constants import Endpoints


class MobileConfigEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.MOBILE_CONFIG

    def generate_profile(self, device_id: str, filepath: str | Path) -> Path:
        """
        This endpoint will returned a signed .mobileconfig
        Apple DNS profile which can be configured on any modern Apple device.
        https://docs.controld.com/reference/get_mobileconfig-device-id
        """
        response = self._session.get(self._url.format(device_id=device_id))
        check_response(response)

        filepath = Path(filepath).resolve()
        if not filepath.exists():
            filepath.parent.mkdir(parents=True)

        with filepath.open("wb") as f:
            f.write(response.content)

        return filepath

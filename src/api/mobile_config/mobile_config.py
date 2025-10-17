from pathlib import Path
from typing import Optional

from api._core import BaseEndpoint, check_response
from api.profiles.constants import Endpoints


class MobileConfigEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.MOBILE_CONFIG

    def generate_profile(
        self,
        device_id: str,
        filepath: str | Path,
        *,
        exclude_wifi: Optional[list[str]] = None,
        exclude_domain: Optional[list[str]] = None,
        dont_sign: bool = True,
        exclude_common: bool = True,
        client_id: Optional[str] = None,
    ) -> Path:
        """
        This endpoint will returned a signed .mobileconfig
        Apple DNS profile which can be configured on any modern Apple device.

        Args:
            device_id (str): Device/Resolver ID.
            filepath (str | Path): The path to save the profile to.
            exclude_wifi (Optional[list[str]]): Array of Wi-Fi SSIDs to exclude from using Control D.
            exclude_domain (Optional[list[str]]): Array of domain names to exclude from using Control D.
            dont_sign (bool): Supply value of 'False' to not sign the profile.
            exclude_common (bool): Supply value of 'False' to not include common captive portal hostnames into exclude_wifi list.
            client_id (Optional[str]): Optional client name.

        Returns:
            Path: The path to the generated profile.

        https://docs.controld.com/reference/get_mobileconfig-device-id
        """
        params = {}
        if exclude_wifi:
            params["exclude_wifi[]"] = exclude_wifi
        if exclude_domain:
            params["exclude_domain[]"] = exclude_domain
        if not dont_sign:
            params["dont_sign"] = int(dont_sign)
        if not exclude_common:
            params["exclude_common"] = int(exclude_common)
        if client_id:
            params["client_id"] = client_id

        response = self._session.get(self._url.format(device_id=device_id), params=params)
        check_response(response)

        filepath = Path(filepath).resolve()
        if not filepath.exists():
            filepath.parent.mkdir(parents=True)

        with filepath.open("wb") as f:
            f.write(response.content)

        return filepath

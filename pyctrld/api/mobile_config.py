"""Mobile config endpoint for ControlD API.

This module provides functionality for generating Apple .mobileconfig profiles
for DNS configuration on iOS, iPadOS, and macOS devices.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint, check_response

if TYPE_CHECKING:
    from typing import Optional


class MobileConfigEndpoint(BaseEndpoint):
    """Endpoint for generating Apple mobile configuration profiles.

    This endpoint provides methods to generate signed .mobileconfig files
    that configure DNS settings on Apple devices (iOS, iPadOS, macOS).

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the MobileConfig endpoint.

        Args:
            token: Bearer token for API authentication.
        """
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
        """Generate a signed .mobileconfig Apple DNS profile.

        This endpoint generates a configuration profile that can be installed on
        any modern Apple device to configure DNS settings for the specified device.

        Args:
            device_id: Device/Resolver ID to generate the profile for.
            filepath: The file path where the profile should be saved.
            exclude_wifi: Array of Wi-Fi SSIDs to exclude from using Control D.
            exclude_domain: Array of domain names to exclude from using Control D.
            dont_sign: If False, the profile will not be signed. Defaults to True.
            exclude_common: If False, common captive portal hostnames will not be
                included in the exclude_wifi list. Defaults to True.
            client_id: Optional client name identifier.

        Returns:
            Path object pointing to the saved .mobileconfig file.

        Reference:
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

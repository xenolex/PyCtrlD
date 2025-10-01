import ipaddress
import re
from dataclasses import asdict, dataclass
from typing import List, Optional

from api.profiles._base import BaseApi

from ._models.services import ServiceItem, ServiceModifedItem
from .constants import Do, Status


@dataclass
class ModifyServiceFormData:
    """Form data for modifying service settings.

    Args:
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (Optional[str], optional): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                                    If REDIRECT, this must be a valid proxy identifier. Defaults to None.
        via_v6 (Optional[str], optional): If SPOOF this can be a valid IPv6 address (AAAA record). Defaults to None.
    """

    do: Do
    status: Status
    via: Optional[str]
    via_v6: Optional[str]

    def __init__(
        self, do: Do, status: Status, via: Optional[str] = None, via_v6: Optional[str] = None
    ):
        self.do = do
        self.status = status
        self.via = via
        self.via_v6 = via_v6

        if do == Do.SPOOF:
            self._check_via_is_record_or_cname()
            self._check_via_v6_is_aaaa_record()

        if do == Do.REDIRECT:
            self._check_via_is_proxy_identifier()
            if via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")

    def _check_via_is_proxy_identifier(self):
        """Check that via field contains a valid 3-letter uppercase proxy identifier."""
        if not all((self.via is not None, str(self.via).isupper(), len(str(self.via)) == 3)):
            raise ValueError(f"via field must be a valid proxy identifier, got: {self.via}")

    def _check_via_is_record_or_cname(self):
        """Check that via field contains either a valid IPv4 address or domain name."""
        if self.via is None:
            raise ValueError("via field is required when do=SPOOF")

        is_ipv4 = True
        is_cname = True

        try:
            ipaddress.IPv4Address(self.via)
        except ipaddress.AddressValueError:
            is_ipv4 = False

        # Basic domain name validation regex
        domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"

        if not re.match(domain_pattern, self.via):
            is_cname = False

        if not is_ipv4 and not is_cname:
            raise ValueError(
                f"via field must be a valid IPv4 address or domain name, got: {self.via}"
            )

    def _check_via_v6_is_aaaa_record(self):
        """Check that via_v6 field contains a valid IPv6 address (AAAA record)."""
        if self.via_v6 is not None:
            try:
                ipaddress.IPv6Address(self.via_v6)
            except ipaddress.AddressValueError:
                raise ValueError(f"via_v6 field must be a valid IPv6 address, got: {self.via_v6}")


class ServicesApi(BaseApi):
    """API client for managing profile services."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = self._url + "{profile_id}/services"

    def list(self, profile_id: str) -> List[ServiceItem]:
        """This returns services that have any kind of rule associated with it.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            List[ServiceItem]: List of service items for the profile.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-services
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url)
        response.raise_for_status()

        data = response.json()
        return [
            ServiceItem(
                locations=item["locations"],
                name=item["name"],
                unlock_location=item["unlock_location"],
                category=item["category"],
                warning=item.get("warning"),
                PK=item["PK"],
                action=item["action"],
            )
            for item in data["body"]["services"]
        ]

    def modify(
        self, profile_id: str, service: str, form_data: ModifyServiceFormData
    ) -> List[ServiceModifedItem]:
        """Create or modify a rule for a {service} in a {profile}.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            service (str): Service name.
            form_data (ModifyServiceFormData): Form data for service modification/ creation.

        Returns:
            List[ServiceModifedItem]: List of modified service items.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-services-service
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(f"{url}/{service}", data=asdict(form_data), headers=headers)
        response.raise_for_status()

        data = response.json()

        return [
            ServiceModifedItem(
                do=item.get("do"),
                status=item.get("status"),
                via=item.get("via"),
            )
            for item in data["body"]["services"]
        ]

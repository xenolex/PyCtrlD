from dataclasses import asdict, dataclass
from typing import List, Optional

from api.profiles._base import (
    BaseEndpoint,
    check_response,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
)
from api.profiles._models.services import ServiceItem, ServiceModifedItem
from api.profiles.constants import Do, Status


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
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via_v6)
            if via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")


class ServicesEndpoint(BaseEndpoint):
    """Endpoint for managing profile services."""

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
        check_response(response)

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
        check_response(response)

        data = response.json()

        return [
            ServiceModifedItem(
                do=item.get("do"),
                status=item.get("status"),
                via=item.get("via"),
            )
            for item in data["body"]["services"]
        ]

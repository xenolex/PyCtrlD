from typing import List, Optional

from pydantic import model_validator

from api.profiles._base import (
    ActionItem,
    BaseEndpoint,
    ConfiguratedBaseModel,
    check_response,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
)
from api.profiles._models.services import ServiceItem
from api.profiles.constants import SERVICES_ENDPOINT_URL, Do, Status


class ModifyServiceFormData(ConfiguratedBaseModel):
    """Form data for modifying service settings.

    Args:
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (Optional[str], optional): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                                    If REDIRECT, this must be a valid proxy identifier. Defaults to None.
        via_v6 (Optional[str], optional): If SPOOF this can be a valid IPv6 address (AAAA record). Defaults to None.
    """

    do: Optional[Do] = None
    status: Optional[Status] = None
    via: Optional[str] = None
    via_v6: Optional[str] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.do == Do.SPOOF:
            check_via_is_record_or_cname(self.via)
            check_via_v6_is_aaaa_record(self.via_v6)

        if self.do == Do.REDIRECT:
            check_via_is_proxy_identifier(self.via_v6)
            if self.via_v6 is not None:
                # todo add logger
                # logger.warning("via_v6 has no effect for REDIRECT")
                print("via_v6 has no effect for REDIRECT")

        return self


class ServicesEndpoint(BaseEndpoint):
    """Endpoint for managing profile services."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = SERVICES_ENDPOINT_URL

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
        return [ServiceItem.model_validate(item, strict=True) for item in data["body"]["services"]]

    def modify(
        self, profile_id: str, service: str, form_data: ModifyServiceFormData
    ) -> List[ActionItem]:
        """Create or modify a rule for a {service} in a {profile}.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            service (str): Service name.
            form_data (ModifyServiceFormData): Form data for service modification/ creation.

        Returns:
            List[ActionItem]: List of modified service items.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-services-service
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.put(
            f"{url}/{service}", data=form_data.model_dump_json(), headers=headers
        )
        check_response(response)

        data = response.json()

        return [ActionItem.model_validate(item, strict=True) for item in data["body"]["services"]]

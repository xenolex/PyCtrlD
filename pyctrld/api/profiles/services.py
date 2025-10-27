"""Profile services endpoint for ControlD API.

This module provides functionality for managing service-based DNS filtering rules
in profiles, allowing control over predefined service categories.
"""

from __future__ import annotations

from typing import Optional

from pydantic import model_validator

from pyctrld._core.logger import logger
from pyctrld._core.models.common import Action, BaseFormData, Do, Status
from pyctrld._core.models.profiles.services import Service
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import (
    BaseEndpoint,
    check_via_is_proxy_identifier,
    check_via_is_record_or_cname,
    check_via_v6_is_aaaa_record,
)


class ModifyServiceFormData(BaseFormData):
    """Form data for modifying service settings.

    Args:
        do (Do | int): Rule type. (BLOCK = 0, BYPASS = 1, SPOOF = 2, REDIRECT = 3).
        status (bool): Rule status. (ENABLED or DISABLED).
        via (Optional[str], optional): Spoof/Redirect target. If SPOOF, this can be an IPv4 or hostname.
                                    If REDIRECT, this must be a valid proxy identifier. Defaults to None.
        via_v6 (Optional[str], optional): If SPOOF this can be a valid IPv6 address (AAAA record). Defaults to None.
    """

    do: Optional[Do | int] = None
    status: Optional[bool | Status] = None
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
                logger.warning('"via_v6" has no effect for REDIRECT')

        return self


class ServicesEndpoint(BaseEndpoint):
    """Endpoint for managing service-based DNS rules in profiles.

    This endpoint provides methods to list and modify DNS filtering rules
    for predefined service categories within a profile.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Services endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.PROFILES_SERVICES

    def list(self, profile_id: str) -> list[Service]:
        """Returns services that have any kind of rule associated with them.

        Retrieves all services in the profile that have DNS filtering rules
        configured, along with their current action settings.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            A list of Service objects representing services with configured rules.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-services
        """

        return self._list(
            url=self._url.format(profile_id=profile_id), model=Service, key="services"
        )

    def modify(
        self, profile_id: str, service: str, form_data: ModifyServiceFormData
    ) -> list[Action]:
        """Create or modify a rule for a service in a profile.

        Creates a new DNS filtering rule for a service, or modifies an existing one,
        with the specified action type, status, and routing settings.

        Args:
            profile_id: Primary key (PK) of the profile.
            service: Service identifier/name.
            form_data: Form data containing rule configuration.

        Returns:
            A list of Action objects representing the updated service rules.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-services-service
        """
        url = self._url.format(profile_id=profile_id)
        return self._modify(
            url=url + f"/{service}",
            model=Action,
            key="services",
            form_data=form_data.model_dump_json(),
        )

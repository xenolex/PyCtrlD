"""Default rule endpoint for ControlD API.

This module provides functionality for managing the default DNS rule in profiles,
which acts as a fallback for queries that don't match any custom rules.
"""

from __future__ import annotations

from typing import Optional

from pyctrld._core.models.common import Action, BaseFormData, Do, Status
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class DefaultRuleFormData(BaseFormData):
    """Form data for modifying default rule settings.

    Args:
        do (Do): Rule type. (BLOCK = 0, BYPASS = 1, SPOOF = 2, REDIRECT = 3).
        status (bool | Status): Rule status. (ENABLED or DISABLED).
        via (Optional[str], optional): Spoof/Redirect target. Defaults to None.
    """

    do: Do
    status: bool | Status
    via: Optional[str] = None


class DefaultRuleEndpoint(BaseEndpoint):
    """Endpoint for managing the default DNS rule in profiles.

    This endpoint provides methods to view and modify the default rule,
    which is applied to DNS queries that don't match any custom rules.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the DefaultRule endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.DEFAULT_RULE

    def list(self, profile_id: str) -> Action:
        """Returns status of the default rule.

        Retrieves the current configuration of the default DNS rule for the
        specified profile, including its action type, status, and routing settings.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            Action object containing the default rule configuration.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-default
        """
        data = self._request(method="GET", url=self._url.format(profile_id=profile_id))
        return Action.model_validate(data["default"], strict=True)

    def modify(self, profile_id: str, form_data: DefaultRuleFormData) -> Action:
        """Modify the default rule for a profile.

        Updates the default DNS rule configuration with new action type, status,
        and optional routing settings.

        Args:
            profile_id: Primary key (PK) of the profile.
            form_data: Form data containing the new default rule settings.

        Returns:
            Action object with the updated default rule configuration.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-default
        """

        data = self._request(
            method="PUT",
            url=self._url.format(profile_id=profile_id),
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return Action.model_validate(data["default"], strict=True)

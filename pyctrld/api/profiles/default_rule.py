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
    """Endpoint for managing profile default rules."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.DEFAULT_RULE

    def list(self, profile_id: str) -> Action:
        """Returns status of the Default Rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            ActionItem: Default rule item with current settings.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-default
        """
        data = self._request(method="GET", url=self._url.format(profile_id=profile_id))
        return Action.model_validate(data["default"], strict=True)

    def modify(self, profile_id: str, form_data: DefaultRuleFormData) -> Action:
        """Modify the Default Rule for a profile.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (DefaultRuleFormData): Form data for default rule modification.

        Returns:
            ActionItem: Modified default rule item with updated settings.

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

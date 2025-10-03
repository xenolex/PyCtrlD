from typing import Optional

from api.profiles._base import ActionItem, BaseEndpoint, check_response
from api.profiles._models.default_rule import DefaultRuleItem
from api.profiles.constants import DEFAULT_RULE_ENDPOINT_URL, Do, Status


class DefaultRuleFormData(ActionItem):
    """Form data for modifying default rule settings.

    Args:
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (Optional[str], optional): Spoof/Redirect target. Defaults to None.
    """

    do: Do
    status: Status
    via: Optional[str] = None


class DefaultRuleEndpoint(BaseEndpoint):
    """Endpoint for managing profile default rules."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = DEFAULT_RULE_ENDPOINT_URL

    def list(self, profile_id: str) -> DefaultRuleItem:
        """Returns status of the Default Rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            DefaultRuleItem: Default rule item with current settings.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-default
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url)
        check_response(response)
        data = response.json()
        default_data = data["body"]["default"]
        return DefaultRuleItem.model_validate(default_data)

    def modify(self, profile_id: str, form_data: DefaultRuleFormData) -> DefaultRuleItem:
        """Modify the Default Rule for a profile.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (DefaultRuleFormData): Form data for default rule modification.

        Returns:
            DefaultRuleItem: Modified default rule item with updated settings.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-default
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(url, headers=headers, data=form_data.model_dump_json())
        check_response(response)
        data = response.json()
        default_data = data["body"]["default"]
        return DefaultRuleItem.model_validate(default_data)

from typing import List, Optional

from pydantic import BaseModel, field_validator

from api.profiles._base import BaseEndpoint, check_response, create_list_of_items
from api.profiles._models.rule_folders import RuleFolder
from api.profiles.constants import Do, Endpoints, Status


class RuleFoldersFormData(BaseModel):
    """Base form data for rule folder operations.

    Args:
        name: Name of the folder.
        do: Rule type (BLOCK, BYPASS, SPOOF, REDIRECT).
        status: Rule status (ENABLED or DISABLED).
        via: Spoof/Redirect target for IPv4.
        via_v6: Spoof/Redirect target for IPv6.
    """

    name: Optional[str] = None
    do: Optional[Do] = None
    status: Optional[Status] = None
    via: Optional[str] = None
    via_v6: Optional[str] = None


class CreateRuleFoldersFormData(RuleFoldersFormData):
    """Form data for creating new rule folders.

    Args:
        name: Name of the folder.
        do: Rule type for the folder. All rules inside will inherit this type
            (BLOCK, BYPASS, SPOOF, REDIRECT).
        status: Status of the folder and all rules inside (ENABLED or DISABLED).
        via: Spoof IP or hostname, or proxy identifier if do=SPOOF or do=REDIRECT.
        via_v6: IPv6 spoof target or proxy identifier if do=SPOOF or do=REDIRECT.
    """

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError("Name is required")
        return v


class RuleFoldersEndpoint(BaseEndpoint):
    """Endpoint for managing profile rule folders (groups)."""

    def __init__(self, token: str) -> None:
        """Initialize the rule folders endpoint.

        Args:
            token: Authentication token for API access.
        """
        super().__init__(token)
        self._url = Endpoints.RULE_FOLDERS

    def list(self, profile_id: str) -> List[RuleFolder]:
        """Return all folders in a profile. These can be used to group custom rules.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            List of rule folder items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-groups
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url)
        check_response(response)

        data = response.json()
        return create_list_of_items(RuleFolder, data["body"]["groups"])

    def modify(
        self, profile_id: str, folder: int, form_data: RuleFoldersFormData
    ) -> List[RuleFolder]:
        """Modify an existing folder.

        Args:
            profile_id: Primary key (PK) of the profile.
            folder: Folder ID.
            form_data: Form data for folder modification.

        Returns:
            List of all rule folder items after modification.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-groups-folder
        """
        url = self._url.format(profile_id=profile_id)
        url = url + f"/{folder}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.put(url, data=form_data.model_dump_json(), headers=headers)
        check_response(response)
        data = response.json()
        return create_list_of_items(RuleFolder, data["body"]["groups"])

    def create(self, profile_id: str, form_data: CreateRuleFoldersFormData) -> List[RuleFolder]:
        """Create a new folder and assign it an optional rule.

        Args:
            profile_id: Primary key (PK) of the profile.
            form_data: Form data for folder creation.

        Returns:
            List of all rule folder items after creation.

        Reference:
            https://docs.controld.com/reference/post_profiles-profile-id-groups
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(url, data=form_data.model_dump_json(), headers=headers)
        check_response(response)

        data = response.json()
        return create_list_of_items(RuleFolder, data["body"]["groups"])

    def delete(
        self,
        profile_id: str,
        folder: int,
    ) -> bool:
        """Delete folder and all custom rules inside it.

        Args:
            profile_id: Primary key (PK) of the profile.
            folder: Folder ID.

        Returns:
            True if folder was deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id-groups-folder
        """
        url = self._url.format(profile_id=profile_id)
        url = url + f"/{folder}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.delete(
            url,
            headers=headers,
        )
        check_response(response)
        return True

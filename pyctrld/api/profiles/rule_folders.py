from __future__ import annotations

from typing import Optional

from pydantic import field_validator

from pyctrld._core.models.common import BaseFormData, Do, Status
from pyctrld._core.models.profiles.rule_folders import RuleFolder
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class RuleFoldersFormData(BaseFormData):
    """Base form data for rule folder operations.

    Args:
        name: Name of the folder.
        do: Rule type (BLOCK = 0, BYPASS = 1, SPOOF = 2, REDIRECT = 3).
        status: Rule status (ENABLED or DISABLED).
        via: Spoof/Redirect target for IPv4.
        via_v6: Spoof/Redirect target for IPv6.
    """

    name: Optional[str] = None
    do: Optional[Do | int] = None
    status: Optional[Status | bool] = None
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
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name is required")
        return value


class RuleFoldersEndpoint(BaseEndpoint):
    """Endpoint for managing profile rule folders (groups)."""

    def __init__(self, token: str) -> None:
        """Initialize the rule folders endpoint.

        Args:
            token: Authentication token for API access.
        """
        super().__init__(token)
        self._url = Endpoints.RULE_FOLDERS

    def list(self, profile_id: str) -> list[RuleFolder]:
        """Return all folders in a profile. These can be used to group custom rules.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            list of rule folder items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-groups
        """

        return self._list(
            url=self._url.format(profile_id=profile_id), model=RuleFolder, key="groups"
        )

    def modify(
        self, profile_id: str, folder: int, form_data: RuleFoldersFormData
    ) -> list[RuleFolder]:
        """Modify an existing folder.

        Args:
            profile_id: Primary key (PK) of the profile.
            folder: Folder ID.
            form_data: Form data for folder modification.

        Returns:
            list of all rule folder items after modification.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-groups-folder
        """
        url = self._url.format(profile_id=profile_id)

        return self._modify(
            url=url + f"/{folder}",
            model=RuleFolder,
            key="groups",
            form_data=form_data.model_dump_json(),
        )

    def create(self, profile_id: str, form_data: CreateRuleFoldersFormData) -> list[RuleFolder]:
        """Create a new folder and assign it an optional rule.

        Args:
            profile_id: Primary key (PK) of the profile.
            form_data: Form data for folder creation.

        Returns:
            list of all rule folder items after creation.

        Reference:
            https://docs.controld.com/reference/post_profiles-profile-id-groups
        """
        return self._create(
            url=self._url.format(profile_id=profile_id),
            model=RuleFolder,
            key="groups",
            form_data=form_data.model_dump_json(),
        )

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
        self._delete(url + f"/{folder}")
        return True

from dataclasses import asdict, dataclass
from typing import List, Optional

from api.profiles._base import BaseEndpoint, check_response
from api.profiles._models.rule_folders import CreateRuleFolderItem, ListRuleFolderItem
from api.profiles.constants import Do, Status


@dataclass
class RuleFoldersFormData:
    """Base form data for rule folder operations.

    Args:
        name (Optional[str]): Name of your folder.
        do (Optional[Do]): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Optional[Status]): Rule status. (ENABLED or DISABLED).
        via (Optional[str]): Spoof/Redirect target.
    """

    name: Optional[str]
    do: Optional[Do]
    status: Optional[Status]
    via: Optional[str]


@dataclass
class CreateRuleFoldersFormData(RuleFoldersFormData):
    """Form data for creating new rule folders.

    Args:
        name (str): Name of your folder.
        do (Do): Add a rule type to a folder. All rules inside will inherit rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Status of the folder and all rules inside.(ENABLED or DISABLED).
        via (Optional[str], optional): Add spoof IP or hostname, or proxy identiifer if do=SPOOF or do=REDIRECT. Defaults to None.
    """

    def __init__(self, name: str, do: Do, status: Status, via: Optional[str] = None) -> None:
        self.name = name
        self.do = Do(do)
        self.status = Status(status)
        if via is not None:
            self.via = via


@dataclass
class ModifyRuleFoldersFormData(RuleFoldersFormData):
    """Form data for modifying existing rule folders.

    Args:
        do (Do): Add a rule type to a folder. All rules inside will inherit rule type.(BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Status of the folder and all rules inside.(ENABLED or DISABLED).
        name (Optional[str], optional): Rename the folder to this name. Defaults to None.
        via (Optional[str], optional): Add spoof IP or hostname, or proxy identiifer if do=SPOOF or do=REDIRECT. Defaults to None.
    """

    def __init__(
        self, do: Do, status: Status, name: Optional[str] = None, via: Optional[str] = None
    ) -> None:
        self.do = Do(do)
        self.status = Status(status)
        if via is not None:
            self.via = via
        if name is not None:
            self.name = name


@dataclass
class DeleteRuleFoldersFormData(RuleFoldersFormData):
    """Form data for deleting rule folders.

    Args:
        name (str): Name of your folder.
        do (Do): Rule type. (BLOCK, BYPASS, SPOOF, REDIRECT).
        status (Status): Rule status. (ENABLED or DISABLED).
        via (str): Spoof/Redirect target.
    """

    def __init__(self, name: str, do: Do, status: Status, via: str) -> None:
        super().__init__(name=name, do=do, status=status, via=via)


class RuleFoldersEndpoint(BaseEndpoint):
    """Endpoint for managing profile rule folders (groups)."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = self._url + "/{profile_id}/groups"

    def list(self, profile_id: str) -> List[ListRuleFolderItem]:
        """Return all folders in a profile. These can be used to group custom rules.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            List[ListRuleFoldersItem]: List of rule folder items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-groups
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url)
        check_response(response)

        data = response.json()
        return [
            ListRuleFolderItem(
                PK=item["PK"],
                group=item["name"],
                action=item["action"],
                count=item["count"],
            )
            for item in data["body"]["groups"]
        ]

    def modify(self, profile_id: str, folder: str, form_data: ModifyRuleFoldersFormData) -> bool:
        """Modify an existing folder.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            folder (str): Folder ID.
            form_data (ModifyRuleFoldersFormData): Form data for folder modification.

        Returns:
            bool: True if folder was modified successfully.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-groups-folder
        """
        url = self._url.format(profile_id=profile_id)
        url = url + f"/{folder}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.put(url, data=asdict(form_data), headers=headers)
        check_response(response)
        return True

    def create(
        self, profile_id: str, form_data: CreateRuleFoldersFormData
    ) -> List[CreateRuleFolderItem]:
        """Create a new folder and assign it an optional rule.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (CreateRuleFoldersFormData): Form data for folder creation.

        Returns:
            List[CreateRuleFoldersItem]: List containing the created rule folder item.

        Reference:
            https://docs.controld.com/reference/post_profiles-profile-id-groups
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(url, data=asdict(form_data), headers=headers)
        check_response(response)

        data = response.json()
        return [
            CreateRuleFolderItem(
                PK=item["PK"],
                group=item["name"],
                action=item["action"],
                count=item["count"],
            )
            for item in data["body"]["groups"]
        ]

    def delete(self, profile_id: str, folder: str, form_data: DeleteRuleFoldersFormData) -> bool:
        """Delete folder and all custom rules inside it.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            folder (str): Folder ID.
            form_data (DeleteRuleFoldersFormData): Form data for folder deletion.

        Returns:
            bool: True if folder was deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id-groups-folder
        """
        url = self._url.format(profile_id=profile_id)
        url = url + f"/{folder}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.delete(url, data=asdict(form_data), headers=headers)
        check_response(response)
        return True

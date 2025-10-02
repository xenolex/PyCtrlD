from dataclasses import asdict, dataclass
from typing import List, Optional

from api.profiles._base import BaseEndpoint
from api.profiles._models.profiles import OptionItem, ProfileItem
from api.profiles.constants import Status


@dataclass
class CreateProfileFormData:
    """Form data for creating a new profile.

    Args:
        name (str): Name of the new profile.
        clone_profile_id (Optional[str], optional): Primary key of profile to clone.
            If omitted, a blank profile is created. Defaults to None.
    """

    name: str
    clone_profile_id: Optional[str] = None

    def __post_init__(self):
        if self.clone_profile_id is None:
            del self.__dict__["clone_profile_id"]


@dataclass
class ModifyProfileFormData:
    """Form data for modifying an existing profile.

    Args:
        name (Optional[str], optional): Rename profile to this name. Defaults to None.
        disable_ttl (Optional[int], optional): Disable profile until specified unix timestamp.
            ttl = 0 disables previous deactivation. Defaults to None.
        lock_status (Optional[int], optional): Lock/unlock a profile from being edited. Defaults to None.
        lock_message (Optional[str], optional): Optional message to error out with when locked
            profile is modified. Defaults to None.
        password (Optional[str], optional): Account password when unlocking a profile. Defaults to None.
    """

    name: Optional[str] = None
    disable_ttl: Optional[int] = None
    lock_status: Optional[int] = None
    lock_message: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self):
        for item in vars(self):
            if item is None:
                del self.__dict__[item]


@dataclass
class ModifyOptionFormData:
    """Form data for modifying profile options.

    Args:
        status (Status): Status of the Profile Option. ENABLED to enable, DISABLED to disable.
        value (Optional[str], optional): Optional value of the option to set. Defaults to None.
    """

    status: Status
    value: Optional[str] = None

    def __post_init__(self):
        if self.value is None:
            del self.__dict__["value"]


class ProfilesEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)

    def list(self) -> List[ProfileItem]:
        """List all profiles associated with an account.

        Returns:
            List[ProfileItem]: List of profile items.

        Reference:
            https://docs.controld.com/reference/get_profiles
        """
        response = self._session.get(self._url)
        response.raise_for_status()
        data = response.json()
        return [
            ProfileItem(
                PK=item["PK"], updated=item["updated"], name=item["name"], profile=item["profile"]
            )
            for item in data["body"]["profiles"]
        ]

    def create(self, form_data: CreateProfileFormData) -> bool:
        """Create a new blank profile, or clone an existing one.

        Args:
            form_data (CreateProfileFormData): Form data for profile creation.

        Returns:
            bool: True if profile was created successfully.

        Reference:
            https://docs.controld.com/reference/post_profiles
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(self._url, data=asdict(form_data), headers=headers)
        response.raise_for_status()

        return True

    def modify(self, profile_id: str, form_data: ModifyProfileFormData):
        """Modify an existing profile.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            form_data (ModifyProfileFormData): Form data for profile modification.

        Returns:
            dict: Response data from the API.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(
            f"{self._url}/{profile_id}", data=asdict(form_data), headers=headers
        )
        response.raise_for_status()

        return response.json()

    def delete(self, profile_id: str) -> bool:
        """Delete profile based on the primary key (PK).
        Profile cannot be enforced by a device to be deleted successfully (must be orphaned profile).

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            bool: True if profile was deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id
        """
        response = self._session.delete(f"{self._url}/{profile_id}")
        response.raise_for_status()

        return True

    def list_options(self):
        """Get all profile options.

        Returns:
            List[OptionItem]: List of available profile options.

        Reference:
            https://docs.controld.com/reference/get_profiles-options
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.get(f"{self._url}/options", headers=headers)
        response.raise_for_status()
        data = response.json()

        return [
            OptionItem(
                PK=item["PK"],
                title=item["title"],
                description=item["description"],
                type=item["type"],
                default_value=item["default_value"],
                info_url=item["info_url"],
            )
            for item in data["body"]["options"]
        ]

    def modify_options(self, profile_id: str, name: str, form_data: ModifyOptionFormData):
        """Set an option on a profile.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            name (str): Option name.
            form_data (ModifyOptionFormData): Form data for option modification.

        Returns:
            bool:  True if profile was modified successfully.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-options-name
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(
            f"{self._url}/{profile_id}/options/{name}", data=asdict(form_data), headers=headers
        )
        response.raise_for_status()

        return True

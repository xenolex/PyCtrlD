"""Profiles endpoint for ControlD API.

This module provides functionality for managing DNS profiles including
creating, modifying, deleting profiles and managing profile options.
"""

from __future__ import annotations

from typing import Optional

from pydantic import model_validator

from pyctrld._core.logger import logger
from pyctrld._core.models.common import BaseFormData, Status
from pyctrld._core.models.profiles.profiles import Data, Option, ProfileObject
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import (
    BaseEndpoint,
)


class CreateProfileFormData(BaseFormData):
    """Form data for creating a new profile.

    Args:
        name (str): Name of the new profile.
        clone_profile_id (Optional[str], optional): Primary key of profile to clone.
            If omitted, a blank profile is created. Defaults to None.
    """

    name: Optional[str] = None
    clone_profile_id: Optional[str] = None

    @model_validator(mode="after")
    def validate_name(self):
        if self.name is not None and self.clone_profile_id is not None:
            logger.warning('"name" will not be set because "clone_profile_id" is provided')

        return self


class ModifyProfileFormData(BaseFormData):
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


class ModifyOptionFormData(BaseFormData):
    """Form data for modifying profile options.

    Args:
        status (bool): Status of the Profile Option. True to enable, False to disable.
        value (Optional[str], optional): Optional value of the option to set. Defaults to None.
    """

    status: bool | Status
    value: Optional[str] = None


class ProfilesEndpoint(BaseEndpoint):
    """Endpoint for managing DNS profiles.

    This endpoint provides methods to list, create, modify, and delete DNS profiles,
    as well as manage profile options and settings.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Profiles endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.PROFILES

    def list(self) -> list[ProfileObject]:
        """List all profiles associated with an account.

        Retrieves all DNS profiles that are configured for the authenticated account.

        Returns:
            A list of ProfileObject instances representing each profile.

        Reference:
            https://docs.controld.com/reference/get_profiles
        """

        return self._list(url=self._url, model=ProfileObject, key="profiles")

    def create(self, form_data: CreateProfileFormData) -> list[ProfileObject]:
        """Create a new blank profile, or clone an existing one.

        Creates either a new blank DNS profile or clones an existing profile
        with all its rules and settings.

        Args:
            form_data: Form data for profile creation containing name and optional clone ID.

        Returns:
            A list containing the newly created ProfileObject.

        Reference:
            https://docs.controld.com/reference/post_profiles
        """
        return self._create(
            url=self._url,
            model=ProfileObject,
            key="profiles",
            form_data=form_data.model_dump_json(),
        )

    def modify(self, profile_id: str, form_data: ModifyProfileFormData) -> list[ProfileObject]:
        """Modify an existing profile.

        Updates profile settings such as name, lock status, or disable timer.

        Args:
            profile_id: Primary key (PK) of the profile to modify.
            form_data: Form data containing fields to update.

        Returns:
            A list containing the modified ProfileObject.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id
        """
        return self._modify(
            url=f"{self._url}/{profile_id}",
            model=ProfileObject,
            key="profiles",
            form_data=form_data.model_dump_json(),
        )

    def delete(self, profile_id: str) -> bool:
        """Delete profile based on the primary key (PK).

        Deletes the specified profile. The profile must not be enforced by any device
        (must be an orphaned profile) for deletion to succeed.

        Args:
            profile_id: Primary key (PK) of the profile to delete.

        Returns:
            True if profile was deleted successfully.

        Reference:
            https://docs.controld.com/reference/delete_profiles-profile-id
        """
        self._delete(f"{self._url}/{profile_id}")
        return True

    def list_options(self) -> list[Option]:
        """Get all profile options.

        Retrieves all available profile options that can be configured on DNS profiles.

        Returns:
            A list of Option objects representing available profile options.

        Reference:
            https://docs.controld.com/reference/get_profiles-options
        """
        return self._list(url=self._url + "/options", model=Option, key="options")

    def modify_options(
        self, profile_id: str, name: str, form_data: ModifyOptionFormData
    ) -> list[Data]:
        """Set an option on a profile.

        Updates a specific option on the given profile with new status and/or value.

        Args:
            profile_id: Primary key (PK) of the profile.
            name: Name of the option to modify.
            form_data: Form data containing option status and optional value.

        Returns:
            A list of Data objects containing the updated option information.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-options-name
        """

        return self._modify(
            url=f"{self._url}/{profile_id}/options/{name}",
            model=Data,
            key="options",
            form_data=form_data.model_dump_json(),
        )

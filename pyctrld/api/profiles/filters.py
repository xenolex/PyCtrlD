"""Filters endpoint for ControlD API.

This module provides functionality for managing DNS filters in profiles,
including both native ControlD filters and third-party filter lists.
"""

from __future__ import annotations

from pyctrld._core.models.common import Action, BaseFormData, Status
from pyctrld._core.models.profiles.filters import NativeFilter, ThirdPartyFilter
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint


class ModifyFilterFormData(BaseFormData):
    """Form data for modifying filter.

    Args:
        status (bool): Status of the filter. True to enable, False to disable.
    """

    status: bool | Status


class FiltersEndpoint(BaseEndpoint):
    """Endpoint for managing DNS filters in profiles.

    This endpoint provides methods to list and modify both native ControlD filters
    and third-party filter lists that can be applied to DNS profiles.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Filters endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)
        self._url = Endpoints.FILTERS

    def list_native(self, profile_id: str) -> list[NativeFilter]:
        """Returns all native ControlD filters for this profile and their states.

        Retrieves all built-in ControlD filters available for the specified profile,
        along with their current enabled/disabled status.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            A list of NativeFilter objects representing available native filters.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters
        """

        return self._list(
            url=self._url.format(profile_id=profile_id), model=NativeFilter, key="filters"
        )

    def list_third_party(self, profile_id: str) -> list[ThirdPartyFilter]:
        """Returns all third-party filters for this profile and their states.

        Retrieves all external/third-party filter lists available for the specified
        profile, along with their current enabled/disabled status.

        Args:
            profile_id: Primary key (PK) of the profile.

        Returns:
            A list of ThirdPartyFilter objects representing available third-party filters.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters-external
        """
        url = self._url.format(profile_id=profile_id)

        return self._list(url=url + "/external", model=ThirdPartyFilter, key="filters")

    def modify(
        self, profile_id: str, filter: str, form_data: ModifyFilterFormData
    ) -> dict[str, Action]:
        """Enables or disables a filter on a specified profile.

        Updates the status of a specific filter (identified by its PK value from
        the list endpoint) on the given profile.

        Args:
            profile_id: Primary key (PK) of the profile.
            filter: Filter identifier (PK value from list endpoint).
            form_data: Form data containing the new filter status.

        Returns:
            Dictionary mapping filter identifiers to their Action configurations.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-filters-filter-filter
        """
        data = self._request(
            method="PUT",
            url=self._url.format(profile_id=profile_id) + f"/filter/{filter}",
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        return {
            key: Action.model_validate(value, strict=True) for key, value in data["filters"].items()
        }

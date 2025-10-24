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
    """Endpoint for managing profile filters."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.FILTERS

    def list_native(self, profile_id: str) -> list[NativeFilter]:
        """Returns all Native filters for this profile and their states.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            list[FilterItem]: list of native filter items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters
        """

        return self._list(
            url=self._url.format(profile_id=profile_id), model=NativeFilter, key="filters"
        )

    def list_third_party(self, profile_id: str) -> list[ThirdPartyFilter]:
        """Returns all 3rd party filters for this profile and their states.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            list[FilterItem]: list of third-party filter items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters-external
        """
        url = self._url.format(profile_id=profile_id)

        return self._list(url=url + "/external", model=ThirdPartyFilter, key="filters")

    def modify(
        self, profile_id: str, filter: str, form_data: ModifyFilterFormData
    ) -> dict[str, Action]:
        """Enables or disables a {filter} on a specified {profile}, which is the value of PK from the list endpoint.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            filter (str): Filter identifier.
            form_data (ModifyFilterFormData): Form data for filter modification.

        Returns:
           dict[str, ActionItem]: Response data from the API containing filter information.

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

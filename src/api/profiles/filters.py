from dataclasses import asdict, dataclass
from typing import List

from ._base import BaseApi
from ._models.filters import FilterItem
from .constants import Status


@dataclass
class ModifyFilterFormData:
    """Form data for modifying filter.

    Args:
        status (Status): Status of the filter. ENABLED to enable, DISABLED to disable.
    """

    status: Status


class FiltersApi(BaseApi):
    """API client for managing profile filters."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = self._url + "/{profile_id}/filters"

    def list_native(self, profile_id: str) -> List[FilterItem]:
        """Returns all Native filters for this profile and their states.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            List[FilterItem]: List of native filter items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url)
        response.raise_for_status()

        data = response.json()
        return [
            FilterItem(
                PK=item["PK"],
                name=item["name"],
                description=item["description"],
                additional=item["additional"],
                sources=item["sources"],
                options=item["options"],
            )
            for item in data["body"]["filters"]
        ]

    def list_third_party(self, profile_id: str) -> List[FilterItem]:
        """Returns all 3rd party filters for this profile and their states.

        Args:
            profile_id (str): Primary key (PK) of the profile.

        Returns:
            List[FilterItem]: List of third-party filter items.

        Reference:
            https://docs.controld.com/reference/get_profiles-profile-id-filters-external
        """
        url = self._url.format(profile_id=profile_id)
        response = self._session.get(url + "/external")
        response.raise_for_status()

        data = response.json()
        return [
            FilterItem(
                PK=item["PK"],
                name=item["name"],
                description=item["description"],
                additional=item["additional"],
                sources=item["sources"],
                options=item["options"],
            )
            for item in data["body"]["filters"]
        ]

    def modify(self, profile_id: str, filter: str, form_data: ModifyFilterFormData) -> List[str]:
        """Enables or disables a {filter} on a specified {profile}, which is the value of PK from the List endpoint.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            filter (str): Filter identifier.
            form_data (ModifyFilterFormData): Form data for filter modification.

        Returns:
            List[str]: Response data from the API containing filter information.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-filters-filter-filter
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(
            url + f"/filter/{filter}", data=asdict(form_data), headers=headers
        )
        response.raise_for_status()

        data = response.json()
        return data["body"]["filter"]

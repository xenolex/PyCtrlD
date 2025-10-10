from typing import List

from typing_extensions import Dict

from api.profiles._base import (
    Action,
    BaseEndpoint,
    ConfiguratedBaseModel,
    check_response,
    create_list_of_items,
)
from api.profiles._models.filters import NativeFilter, ThirdPartyFilter
from api.profiles.constants import FILTERS_ENDPOINT_URL, Status


class ModifyFilterFormData(ConfiguratedBaseModel):
    """Form data for modifying filter.

    Args:
        status (Status): Status of the filter. ENABLED to enable, DISABLED to disable.
    """

    status: Status


class FiltersEndpoint(BaseEndpoint):
    """Endpoint for managing profile filters."""

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = FILTERS_ENDPOINT_URL

    def list_native(self, profile_id: str) -> List[NativeFilter]:
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
        check_response(response)

        data = response.json()
        return create_list_of_items(NativeFilter, data["body"]["filters"])

    def list_third_party(self, profile_id: str) -> List[ThirdPartyFilter]:
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
        check_response(response)

        data = response.json()

        return create_list_of_items(ThirdPartyFilter, data["body"]["filters"])

    def modify(
        self, profile_id: str, filter: str, form_data: ModifyFilterFormData
    ) -> Dict[str, Action]:
        """Enables or disables a {filter} on a specified {profile}, which is the value of PK from the List endpoint.

        Args:
            profile_id (str): Primary key (PK) of the profile.
            filter (str): Filter identifier.
            form_data (ModifyFilterFormData): Form data for filter modification.

        Returns:
           Dict[str, ActionItem]: Response data from the API containing filter information.

        Reference:
            https://docs.controld.com/reference/put_profiles-profile-id-filters-filter-filter
        """
        url = self._url.format(profile_id=profile_id)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.put(
            url + f"/filter/{filter}", data=form_data.model_dump_json(), headers=headers
        )
        check_response(response)

        data = response.json()

        return {
            key: Action.model_validate(value, strict=True)
            for key, value in data["body"]["filters"].items()
        }

from __future__ import annotations

from typing import TYPE_CHECKING

from api._core.models.organization import Member, Organization, SubOrganization
from api._core.urls import Endpoints
from api._core.utils import BaseEndpoint, check_response
from api.devices import BaseFormData

if TYPE_CHECKING:
    from typing import Optional


def __print_warning():
    print("======================================================================")
    print("Warning!!! Use on your own risk!!! Author haven't organization profile")
    print("======================================================================")


class CreateSubOrganizationFromData(BaseFormData):
    name: str
    contact_email: str
    twofa_req: bool
    stats_endpoint: str
    max_users: int
    max_routers: int
    address: Optional[str] = None
    website: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    parent_profile: Optional[str] = None


class ModifyOrganizationFromData(BaseFormData):
    name: Optional[str] = None
    contact_email: Optional[str] = None
    twofa_req: Optional[bool] = None
    stats_endpoint: Optional[str] = None
    max_users: Optional[int] = None
    max_routers: Optional[int] = None
    max_devices: Optional[int] = None
    address: Optional[str] = None
    website: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    parent_profile: Optional[str] = None


class OrganizationEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)

        self._url = Endpoints.ORGANIZATION

    def view_organization_info(self) -> Organization:
        """
        View details of an organization.
        Reference:
            https://docs.controld.com/reference/get_organizations-organization
        """
        __print_warning()

        url = self._url + "/organization"
        response = self._session.get(url)
        check_response(response)

        data = response.json()

        return Organization.model_validate(data["body"]["organization"], strict=True)

    def view_members(self) -> list[Member]:
        """
        View organization membership.
        Reference:
            https://docs.controld.com/reference/get_organizations-members
        """
        __print_warning()

        return self._list(url=self._url + "/members", model=Member, key="members")

    def view_sub_organizations(self) -> list[SubOrganization]:
        """
        View sub-organizations and their details.
        Reference:
            https://docs.controld.com/reference/get_organizations-sub-organizations
        """

        __print_warning()

        return self._list(
            url=self._url + "/sub_organizations", model=SubOrganization, key="sub_organizations"
        )

    def create_sub_organization(self, form_data: CreateSubOrganizationFromData) -> SubOrganization:
        """
        Create a new Sub-Organization.
        Reference:
            https://docs.controld.com/reference/post_organizations-suborg
        """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        url = f"{self._url}/suborg"
        response = self._session.post(url, data=form_data.model_dump_json(), headers=headers)

        check_response(response)

        data = response.json()

        return SubOrganization.model_validate(data["body"]["sub_organization"], strict=True)

    def modify_organization(self, form_data: ModifyOrganizationFromData) -> Organization:
        """
        Create a new Sub-Organization.
        Reference:
            https://docs.controld.com/reference/put_organizations
        """

        __print_warning()

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        url = f"{self._url}"
        response = self._session.put(url, data=form_data.model_dump_json(), headers=headers)

        check_response(response)

        data = response.json()

        return Organization.model_validate(data["body"]["organization"], strict=True)

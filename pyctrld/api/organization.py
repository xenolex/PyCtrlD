from __future__ import annotations

from typing import TYPE_CHECKING

from pyctrld._core.logger import logger
from pyctrld._core.models.organization import Member, Organization, SubOrganization
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint
from pyctrld.api.devices import BaseFormData

if TYPE_CHECKING:
    from typing import Optional


def __print_warning():
    logger.warning("======================================================================")
    logger.warning("Warning!!! Use on your own risk!!! Author haven't organization profile")
    logger.warning("======================================================================")


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

        data = self._request(method="GET", url=self._url + "/organization")

        return Organization.model_validate(data["organization"], strict=True)

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
        __print_warning()

        data = self._request(
            method="POST",
            url=self._url + "/suborg",
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        return SubOrganization.model_validate(data["sub_organization"], strict=True)

    def modify_organization(self, form_data: ModifyOrganizationFromData) -> Organization:
        """
        Create a new Sub-Organization.
        Reference:
            https://docs.controld.com/reference/put_organizations
        """

        __print_warning()

        data = self._request(
            method="PUT",
            url=self._url,
            data=form_data.model_dump_json(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        return Organization.model_validate(data["organization"], strict=True)

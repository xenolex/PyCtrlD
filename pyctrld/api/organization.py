"""Organization endpoint for ControlD API.

This module provides access to organization management functionality including
viewing organization details, members, sub-organizations, and creating new sub-organizations.

Warning:
    This endpoint has limited testing as the author does not have an organization profile.
    Use at your own risk.
"""

from __future__ import annotations

import shutil
from typing import Optional

from pyctrld._core.logger import logger
from pyctrld._core.models.organization import Member, Organization, SubOrganization
from pyctrld._core.urls import Endpoints
from pyctrld._core.utils import BaseEndpoint
from pyctrld.api.devices import BaseFormData


def __print_warning() -> None:
    """Print warning message about untested organization functionality."""
    width = shutil.get_terminal_size().columns

    logger.warning("=" * width)
    logger.warning("Warning!!! Use on your own risk!!! Author haven't organization profile")
    logger.warning("=" * width)


class CreateSubOrganizationFromData(BaseFormData):
    """Form data for creating a sub-organization.

    Attributes:
        name: Name of the sub-organization.
        contact_email: Contact email address.
        twofa_req: Whether two-factor authentication is required.
        stats_endpoint: Analytics/statistics endpoint URL.
        max_users: Maximum number of users allowed.
        max_routers: Maximum number of routers allowed.
        address: Optional physical address.
        website: Optional website URL.
        contact_name: Optional contact person name.
        contact_phone: Optional contact phone number.
        parent_profile: Optional parent profile identifier.
    """

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
    """Form data for modifying an organization.

    All fields are optional, only provided fields will be updated.

    Attributes:
        name: Updated organization name.
        contact_email: Updated contact email address.
        twofa_req: Updated two-factor authentication requirement.
        stats_endpoint: Updated analytics/statistics endpoint URL.
        max_users: Updated maximum number of users allowed.
        max_routers: Updated maximum number of routers allowed.
        max_devices: Updated maximum number of devices allowed.
        address: Updated physical address.
        website: Updated website URL.
        contact_name: Updated contact person name.
        contact_phone: Updated contact phone number.
        parent_profile: Updated parent profile identifier.
    """

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
    """Endpoint for managing organizations and sub-organizations.

    This endpoint provides methods to view and manage organization details,
    members, and sub-organizations.

    Warning:
        This endpoint has limited testing. Use at your own risk.

    Args:
        token: The API authentication bearer token.
    """

    def __init__(self, token: str) -> None:
        """Initialize the Organization endpoint.

        Args:
            token: Bearer token for API authentication.
        """
        super().__init__(token)

        self._url = Endpoints.ORGANIZATION

    def view_organization_info(self) -> Organization:
        """View details of an organization.

        Retrieves detailed information about the organization associated
        with the authenticated account.

        Returns:
            Organization object containing organization details.

        Reference:
            https://docs.controld.com/reference/get_organizations-organization
        """
        __print_warning()

        data = self._request(method="GET", url=self._url + "/organization")

        return Organization.model_validate(data["organization"], strict=True)

    def view_members(self) -> list[Member]:
        """View organization membership.

        Retrieves a list of all members belonging to the organization.

        Returns:
            A list of Member objects representing organization members.

        Reference:
            https://docs.controld.com/reference/get_organizations-members
        """
        __print_warning()

        return self._list(url=self._url + "/members", model=Member, key="members")

    def view_sub_organizations(self) -> list[SubOrganization]:
        """View sub-organizations and their details.

        Retrieves a list of all sub-organizations and their configuration details.

        Returns:
            A list of SubOrganization objects.

        Reference:
            https://docs.controld.com/reference/get_organizations-sub-organizations
        """

        __print_warning()

        return self._list(
            url=self._url + "/sub_organizations", model=SubOrganization, key="sub_organizations"
        )

    def create_sub_organization(self, form_data: CreateSubOrganizationFromData) -> SubOrganization:
        """Create a new sub-organization.

        Creates a new sub-organization with the specified configuration.

        Args:
            form_data: Form data containing sub-organization details.

        Returns:
            SubOrganization object representing the created sub-organization.

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
        """Modify organization settings.

        Updates the configuration of the organization with the provided data.

        Args:
            form_data: Form data containing fields to update.

        Returns:
            Organization object with updated information.

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

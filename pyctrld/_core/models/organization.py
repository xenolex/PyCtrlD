"""Organization models for ControlD API.

This module provides data models for organization and sub-organization structures,
including members, permissions, and resource limits.
"""

from __future__ import annotations

from pyctrld._core.models.common import ConfiguratedBaseModel, Count, Status


class Members(Count):
    """Member count information.

    Inherits from Count to provide member count data.
    """

    pass


class Profiles(Count):
    """Profile count and limit information.

    Attributes:
        max: Maximum number of profiles allowed.
    """

    max: int


class Users(Profiles):
    """User count, limit, and pricing information.

    Attributes:
        price: Price per user.
    """

    price: int


class Routers(Users):
    """Router count, limit, and pricing information.

    Inherits pricing and limit fields from Users.
    """

    pass


class SubOrganizations(Profiles):
    """Sub-organization count and limit information.

    Inherits count and limit fields from Profiles.
    """

    pass


class BaseOrganization(ConfiguratedBaseModel):
    """Base organization model with common fields.

    Attributes:
        website: Organization website URL.
        address: Physical address.
        max_profiles: Maximum number of profiles allowed.
        status: Organization status (enabled/disabled).
        stats_endpoint: Analytics/statistics endpoint URL.
        max_users: Maximum number of users allowed.
        max_legacy_resolvers: Maximum number of legacy resolvers.
        name: Organization name.
        date: Creation date.
        max_routers: Maximum number of routers allowed.
        contact_email: Contact email address.
        PK: Primary key (unique identifier).
        members: Member count information.
        profiles: Profile count and limit information.
        users: User count and limit information.
        routers: Router count and limit information.
        sub_organizations: Sub-organization count information.
    """

    website: str
    address: str
    max_profiles: int
    status: Status
    stats_endpoint: str
    max_users: int
    max_legacy_resolvers: int
    name: str
    date: str
    max_routers: int
    contact_email: str
    PK: int
    members: Members
    profiles: Profiles
    users: Users
    routers: Routers
    sub_organizations: SubOrganizations


class Organization(BaseOrganization):
    """Full organization model with pricing information.

    Attributes:
        price_users: Price per user.
        price_routers: Price per router.
        max_sub_orgs: Maximum number of sub-organizations allowed.
    """

    price_users: int
    price_routers: int
    max_sub_orgs: int


class Permission(ConfiguratedBaseModel):
    """Member permission configuration.

    Attributes:
        level: Permission level (numeric).
        printable: Whether permission is printable/displayable.
    """

    level: int
    printable: bool


class Member(ConfiguratedBaseModel):
    """Organization member model.

    Attributes:
        PK: Primary key (unique identifier).
        email: Member email address.
        last_active: Timestamp of last activity.
        twofa: Two-factor authentication status.
        status: Member status (enabled/disabled).
        permission: Permission configuration.
    """

    PK: str
    email: str
    last_active: int
    twofa: int
    status: Status
    permission: Permission


class ParentOrg(ConfiguratedBaseModel):
    """Parent organization reference.

    Attributes:
        name: Parent organization name.
        PK: Primary key (unique identifier) of parent organization.
    """

    name: str
    PK: str


class ParentProfile(ConfiguratedBaseModel):
    """Parent profile reference.

    Attributes:
        name: Parent profile name.
        PK: Primary key (unique identifier) of parent profile.
        updated: Timestamp of last update.
    """

    name: str
    PK: str
    updated: int


class SubOrganization(BaseOrganization):
    """Sub-organization model with parent references.

    Attributes:
        contact_name: Contact person name.
        parent_org: Parent organization reference.
        twofa_req: Two-factor authentication requirement flag.
        parent_profile: Parent profile reference.
    """

    contact_name: str
    parent_org: ParentOrg
    twofa_req: int
    parent_profile: ParentProfile
